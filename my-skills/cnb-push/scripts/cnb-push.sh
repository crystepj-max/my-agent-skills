#!/usr/bin/env bash
# cnb-push — 把本地仓库推送到 CNB（cnb.cool）
#
# 设计目的：让任何 Agent 用一条命令正确推送，不必记住 4 个 git -c 参数。
#
# 内置修正（2026-09-09 实测踩坑，详见 SKILL.md）：
#   1. SOCKS5 代理 —— iKuuuVPN 的 TUN fake-ip 会劫持 cnb.cool 的 DNS（解析成 198.18.x），
#      直连被限速到 ~14 KiB/s；走 ClashX SOCKS5（代理端解析真实 DNS）实测 131 MiB/s。
#   2. HTTP/1.1   —— 大 pack（>100MB）走 HTTP/2 必报 "curl 16 Error in the HTTP2 framing layer"。
#   3. postBuffer —— 默认 1M 装不下大 pack，提到 500M。
#   4. 重试        —— SOCKS5 偶发 "SSL bad record mac"，重试可过。
#
# 安全护栏（硬约束，不可绕过）：
#   - 绝不传 --force / -f，历史不可覆盖
#   - 绝不自动 commit / stash，工作区改动原样保留
#   - 绝不修改或删除 origin（GitHub 灾备地址）
#   - token 只通过 http.extraHeader 传递，不写入 .git/config，不出现在日志
#
# 用法：
#   cnb-push.sh [仓库目录] [--all] [--tags] [--dry] [--direct] [--org 组织] [--set-default] [分支...]
#
# 示例：
#   cnb-push.sh                          # 推当前分支
#   cnb-push.sh --all                    # 推全部分支 + 标签
#   cnb-push.sh /path/to/repo --all      # 指定仓库
#   cnb-push.sh --dry --all              # 空跑，只看计划
#   cnb-push.sh --set-default --all      # 顺带把 remote.pushDefault 设为 cnb

set -uo pipefail

ORG_DEFAULT="chris.ai"
TOKEN_FILE="${CNB_TOKEN_FILE:-$HOME/.cnb/token}"
PROXY_PORT="${CNB_PROXY_PORT:-7890}"

# ---------- 参数解析 ----------
REPO_DIR=""; PUSH_ALL=0; PUSH_TAGS_ONLY=0; DRY=0; FORCE_DIRECT=0; SET_DEFAULT=0
ORG="$ORG_DEFAULT"; BRANCHES=()

while [ $# -gt 0 ]; do
  case "$1" in
    --all)          PUSH_ALL=1; shift ;;
    --tags)         PUSH_TAGS_ONLY=1; shift ;;
    --dry|-n)       DRY=1; shift ;;
    --direct)       FORCE_DIRECT=1; shift ;;
    --set-default)  SET_DEFAULT=1; shift ;;
    --org)          ORG="${2:?--org 需要参数}"; shift 2 ;;
    -h|--help)      sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*)             echo "❌ 未知参数：$1（用 -h 看用法）" >&2; exit 2 ;;
    *)
      if [ -z "$REPO_DIR" ] && [ -d "$1" ]; then REPO_DIR="$1"
      else BRANCHES+=("$1"); fi
      shift ;;
  esac
done

[ -z "$REPO_DIR" ] && REPO_DIR="$PWD"
cd "$REPO_DIR" 2>/dev/null || { echo "❌ 无法进入目录：$REPO_DIR" >&2; exit 1; }
REPO_DIR="$PWD"

# ---------- 基础校验 ----------
if [ ! -d ".git" ]; then
  echo "❌ 不是 git 仓库：$REPO_DIR" >&2; exit 1
fi

NAME="$(basename "$REPO_DIR")"
echo "═══ cnb-push: ${NAME} ═══"

# 目标 URL：优先复用已配置的 cnb remote，否则按 组织/目录名 拼
CNB_URL="$(git remote get-url cnb 2>/dev/null || true)"
if [ -z "$CNB_URL" ]; then
  CNB_URL="https://cnb.cool/${ORG}/${NAME}.git"
  echo "  目标（推测）: ${CNB_URL}"
  echo "  ⚠️  本仓库未配置 cnb remote；若仓库名与目录名不一致，请用 --org 或在仓库内先执行："
  echo "      git remote add cnb https://cnb.cool/<组织>/<仓库名>.git"
else
  echo "  目标: ${CNB_URL}"
fi

# ---------- 安全护栏自检 ----------
DIRTY="$(git status --porcelain 2>/dev/null | grep -c . || true)"
DIRTY="${DIRTY:-0}"
if [ "$DIRTY" -gt 0 ]; then
  echo "  🟡 工作区有 ${DIRTY} 项未提交改动 → 不会被推送（push 只传已提交内容），改动原样保留"
fi
if git remote get-url origin >/dev/null 2>&1; then
  echo "  🟢 origin 保留: $(git remote get-url origin)"
fi

# ---------- token ----------
if [ ! -f "$TOKEN_FILE" ]; then
  echo "❌ 找不到 CNB 凭据：${TOKEN_FILE}" >&2
  echo "   处理：登录 https://cnb.cool → 头像 → 访问令牌，或重新授权 cnb CLI" >&2
  exit 1
fi
PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then echo "❌ 未找到 python，无法解析 token" >&2; exit 1; fi
TOKEN="$("$PY" -c "
import json,sys
try:
    d=json.load(open('$TOKEN_FILE'))
    print(d.get('access_token') or d.get('token') or '')
except Exception as e:
    sys.stderr.write('token 解析失败: %s\n' % e); sys.exit(1)
")" || { echo "❌ token 解析失败" >&2; exit 1; }
if [ -z "$TOKEN" ]; then echo "❌ token 为空，凭据可能已失效" >&2; exit 1; fi

# ---------- 代理决策 ----------
PROXY_ARGS=()
MODE="直连"
if [ "$FORCE_DIRECT" -eq 0 ]; then
  if (exec 3<>"/dev/tcp/127.0.0.1/${PROXY_PORT}") 2>/dev/null; then
    PROXY_ARGS=(-c "http.proxy=socks5://127.0.0.1:${PROXY_PORT}")
    MODE="SOCKS5 代理(127.0.0.1:${PROXY_PORT})"
  fi
fi
# DNS 被 fake-ip 劫持时给出明确提示
RESOLVED="$(nslookup cnb.cool 2>/dev/null | awk '/^Address: /{print $NF}' | tail -1)"
case "$RESOLVED" in
  198.18.*)
    echo "  🟡 DNS 被 fake-ip 劫持（cnb.cool → ${RESOLVED}），必须走代理才能满速"
    [ ${#PROXY_ARGS[@]} -eq 0 ] && echo "     ⚠️  但未检测到 ${PROXY_PORT} 端口代理，将直连（可能极慢）"
    ;;
esac
echo "  网络: ${MODE}"

# ---------- 通用 git 参数 ----------
GIT_ARGS=(
  -c "http.version=HTTP/1.1"          # 大 pack 必须降级，否则 HTTP2 framing 错误
  -c "http.postBuffer=524288000"      # 500M，默认 1M 装不下大仓库
  -c "pack.compression=1"             # 压得快，上传体积换时间
  -c "http.extraHeader=Authorization: Bearer ${TOKEN}"
  "${PROXY_ARGS[@]}"
)

# ---------- 空跑 ----------
if [ "$DRY" -eq 1 ]; then
  echo "  🔍 空跑模式，不执行任何推送"
  echo "     git ${GIT_ARGS[*]/Bearer*/Bearer ***} push ..."
  if [ "$PUSH_ALL" -eq 1 ]; then
    echo "     将推送分支: $(git branch --format='%(refname:short)' | tr '\n' ' ')"
    echo "     将推送标签: $(git tag | tr '\n' ' ')"
  else
    echo "     将推送: ${BRANCHES[*]:-$(git branch --show-current)}"
  fi
  echo "     pushDefault 现状: $(git config --get remote.pushDefault || echo '未设置')"
  exit 0
fi

# ---------- 推送 ----------
run_push() {
  local label="$1"; shift
  local attempt rc=1
  for attempt in 1 2 3; do
    if [ "$attempt" -gt 1 ]; then echo "     ↻ 第 ${attempt} 次尝试…"; sleep 3; fi
    git "${GIT_ARGS[@]}" push "$@" 2>&1 | sed "s|${TOKEN}|***TOKEN***|g" | \
      grep -vE "对象中|remote: (Resolving|Counting|Compressing)|^Total |^总共|Delta compression|使用 [0-9]+ 个线程|Writing objects|写入对象中" | \
      sed '/^$/d'
    rc="${PIPESTATUS[0]}"
    [ "$rc" -eq 0 ] && { echo "  ✅ ${label} 成功"; return 0; }
  done
  echo "  ❌ ${label} 失败（已重试 3 次）" >&2
  return 1
}

START="$(date +%s)"
FAILED=0

if [ "$SET_DEFAULT" -eq 1 ]; then
  git config remote.pushDefault cnb && echo "  ✅ remote.pushDefault = cnb"
fi

# 标签数量：为 0 时跳过（实测：空 push --tags 会触发 LibreSSL "bad record mac"，
# 直连/HTTP代理/SOCKS5 三种方式均复现，属协议边缘故障，跳过即可）
TAG_COUNT="$(git tag 2>/dev/null | grep -c . || true)"
TAG_COUNT="${TAG_COUNT:-0}"

if [ "$PUSH_TAGS_ONLY" -eq 1 ]; then
  if [ "$TAG_COUNT" -eq 0 ]; then
    echo "  ⚪ 无标签，跳过"
  else
    run_push "标签" --tags "$CNB_URL" || FAILED=1
  fi
else
  if [ "$PUSH_ALL" -eq 1 ]; then
    run_push "全部分支" --all "$CNB_URL" || FAILED=1
    if [ "$TAG_COUNT" -eq 0 ]; then
      echo "  ⚪ 无标签，跳过"
    else
      run_push "标签" --tags "$CNB_URL" || FAILED=1
    fi
  elif [ ${#BRANCHES[@]} -gt 0 ]; then
    for b in "${BRANCHES[@]}"; do
      run_push "分支 ${b}" "$CNB_URL" "$b" || FAILED=1
    done
  else
    CUR="$(git branch --show-current)"
    [ -z "$CUR" ] && { echo "❌ 处于分离 HEAD，请指定分支名或 --all" >&2; exit 1; }
    run_push "分支 ${CUR}" "$CNB_URL" "$CUR" || FAILED=1
  fi
fi

END="$(date +%s)"
echo "  耗时: $((END-START)) 秒"

if [ "$FAILED" -eq 0 ]; then
  echo "═══ ✅ ${NAME} 推送完成 ═══"
  exit 0
else
  echo "═══ ❌ ${NAME} 推送未完全成功 ═══" >&2
  echo "  排查：① 仓库是否已在 CNB 建好且为空 ② token 是否有写权限 ③ 见 SKILL.md 故障表" >&2
  exit 1
fi
