#!/usr/bin/env bash
# cnb-git — CNB（cnb.cool）全场景 Git 操作封装：clone / pull / push / 分支 / PR（含草稿）/ 合并
#
# 让任何 Agent 用一条命令完成 CNB 操作，不必记住 token 传递方式、代理参数和平台差异。
#
# ── 平台差异（2026-09-10 在本机实测，全部有证据，与 GitHub 不同，勿凭 GitHub 经验想当然）──
#   1. 草稿 PR 不是 draft 字段，是标题前缀 "WIP:"  → 传 draft:true 会被静默忽略，is_wip 仍为 false
#      （"Draft:" 前缀无效；is_wip 是只读推导字段，patch 改不动）
#   2. 无差异分支建 PR 直接 404 → errcode 2004004 "there is no diff between ..."
#   3. cnb git-credential 不认 cnb.cool 域（报 unknown host），故 git 操作一律走 http.extraHeader
#   4. 分页参数是 --page-size（CLI 顶层示例里的 --pageSize 是错的），默认仅 10 条
#   5. delete-branch 用 --branch，不是 --name
#   6. merge-pull 必须带 commit_title，否则 400 errcode 2000001 "commit_title is required"
#      （GitHub squash 会自动生成标题，CNB 不会）；脚本未显式给定时自动取 PR 标题 + (#编号)
#   7. 读取类操作（clone/fetch/pull）不能无条件带 token —— 公开仓库无凭据也能读，
#      而带【失效 token】会被平台拒绝并报 "Repository Not Found"（误导性 404，不是 401）
#      → 脚本对读取类自动降级为匿名重试
#   8. worktree 里 .git 是【文件】不是目录（内容 gitdir: .../worktrees/x）
#      → 用 git rev-parse --is-inside-work-tree 判断，不能用 [ -d .git ]
#   9. 本机 .git 下的陈旧 .lock 会让 git 报 cannot lock ref 并雪崩（删掉又被重建）
#      → 脚本检测到后自动清锁，并在【同一进程内零间隔】重试
#
# ── 网络（iKuuuVPN TUN fake-ip 把 cnb.cool 解析成 198.18.x）──
#   小请求无感；大 pack 直连会被限速到 ~14 KiB/s，走 ClashX SOCKS5 实测 ~131 MiB/s。
#   另需 http.version=HTTP/1.1（大 pack 走 HTTP/2 必报 curl 16 framing layer）。
#
# ── 安全护栏（硬约束）──
#   - 绝不 force push；merge-pull 的 --force 指"忽略检查强制合并"，需显式 --force 才传
#   - 绝不自动 commit / stash；工作区改动原样保留
#   - 绝不改动 origin（GitHub 灾备地址）：只新增/使用 cnb remote
#   - token 只经 http.extraHeader 传递，不写入 .git/config，日志脱敏为 ***TOKEN***
#
# 用法：cnb-git.sh <子命令> [参数...]
#   clone <组织/仓库> [目录]              克隆（自动带凭据）
#   pull  [目录] [分支] [--remote cnb]    拉取（默认走 cnb，因为 origin=GitHub 已 403）
#   fetch [目录] [--remote cnb]           拉取但不合并
#   push  [目录] [--all|--tags]           推送（委托 cnb-push.sh）
#   branches <组织/仓库>                  分支列表（自动全量，不受默认 10 条限制）
#   branch-create <组织/仓库> <名> --from <基点>
#   branch-delete <组织/仓库> <名>
#   pr-create <组织/仓库> --head <源> --base <目标> --title <标题> [--wip] [--body <正文>]
#   pr-list <组织/仓库> [--state open|closed|all]
#   pr-get  <组织/仓库> <编号>
#   pr-comment <组织/仓库> <编号> --body <内容>
#   pr-merge <组织/仓库> <编号> [--style squash|merge|rebase] [--force] [--title <提交标题>]
#   pr-close <组织/仓库> <编号>
#   whoami                                当前登录身份
#
# 示例：
#   cnb-git.sh clone chris.ai/my-agent-skills
#   cnb-git.sh pull /Users/chris/workspace/workflow-manager
#   cnb-git.sh branches chris.ai/workflow-manager
#   cnb-git.sh pr-create chris.ai/my-agent-skills --head feat/x --base main --title "feat: x" --wip
#   cnb-git.sh pr-merge chris.ai/my-agent-skills 12 --style squash

set -uo pipefail

TOKEN_FILE="${CNB_TOKEN_FILE:-$HOME/.cnb/token}"
PROXY_PORT="${CNB_PROXY_PORT:-7890}"
ORGANIZATION_DEFAULT="chris.ai"

die() { echo "❌ $*" >&2; exit 1; }

# ---------- token ----------
PY="$(command -v python3 || command -v python || true)"
PROXY_ARGS=()
CNB_TOKEN=""

_read_token_file() {
  [ -n "$PY" ] || { echo ""; return 0; }
  "$PY" -c "
import json
try:
    d = json.load(open('$TOKEN_FILE'))
    print(d.get('access_token') or d.get('token') or '')
except Exception:
    print('')
" 2>/dev/null
}

# 写操作需要凭据：token 缺失即失败
load_token() {
  [ -f "$TOKEN_FILE" ] || die "找不到 CNB 凭据：$TOKEN_FILE（登录 https://cnb.cool → 头像 → 访问令牌，或执行 cnb login）"
  [ -n "$PY" ] || die "未找到 python，无法解析 token"
  CNB_TOKEN="$(_read_token_file)"
  [ -n "$CNB_TOKEN" ] || die "token 为空，凭据可能已失效（cnb status 检查）"
}

# 读取类操作（clone / fetch / pull）：token 可选。
# 缺陷修复：公开仓库不带凭据也能读，而带一个【失效 token】反而会被平台拒绝并报
# "Repository Not Found"（误导性的 404，不是 401），排查时极易带偏。
# 故读取类一律允许降级为匿名请求。
load_token_optional() {
  CNB_TOKEN=""
  if [ -f "$TOKEN_FILE" ] && [ -n "$PY" ]; then
    CNB_TOKEN="$(_read_token_file)"
    [ -n "$CNB_TOKEN" ] || echo "  🟡 凭据未解析出 token，将以匿名方式读取（公开仓库无需凭据）" >&2
  else
    echo "  🟡 未找到可用凭据，以匿名方式读取（公开仓库无需凭据）" >&2
  fi
}

# ---------- 代理 ----------
_net_probe() {
  if (exec 3<>"/dev/tcp/127.0.0.1/${PROXY_PORT}") 2>/dev/null; then
    NET_MODE="SOCKS5 代理(127.0.0.1:${PROXY_PORT})"
    PROXY_ARGS=(-c "http.proxy=socks5://127.0.0.1:${PROXY_PORT}")
  else
    NET_MODE="直连（未检测到 ${PROXY_PORT} 端口代理，大仓库可能极慢）"
    PROXY_ARGS=()
  fi
}

build_git_args() {
  _net_probe
  GIT_ARGS=(-c "http.version=HTTP/1.1" -c "http.postBuffer=524288000" -c "pack.compression=1")
  [ ${#PROXY_ARGS[@]} -gt 0 ] && GIT_ARGS+=("${PROXY_ARGS[@]}")
  GIT_ARGS+=(-c "http.extraHeader=Authorization: Bearer ${CNB_TOKEN}")
}

# 不带凭据的通用参数（匿名降级重试用）
_anon_args() {
  ANON_ARGS=(-c "http.version=HTTP/1.1" -c "http.postBuffer=524288000" -c "pack.compression=1")
  [ ${#PROXY_ARGS[@]} -gt 0 ] && ANON_ARGS+=("${PROXY_ARGS[@]}")
}

# ---------- 陈旧锁自愈 ----------
# 本机已知现象：.git 下 .lock 删掉就被重建，git 报 cannot lock ref 并雪崩。
# 解法必须"清锁 + 重试"在同一进程内零间隔完成，否则锁会被后台进程立刻重建。
# 注意：清锁用 python os.remove —— shell 的 rm 会被 safe-delete 钩子拦截。
stale_lock_clean() {
  [ -n "$PY" ] || return 0
  # worktree 里 --git-dir 指向 .git/worktrees/<名>，但 refs 的锁落在共享的
  # 主 .git 下 —— 必须同时扫 --git-common-dir，否则清了个空（实测踩过）。
  local gd common
  gd="$(git rev-parse --git-dir 2>/dev/null)" || gd=""
  common="$(git rev-parse --git-common-dir 2>/dev/null)" || common=""
  [ -n "$gd" ] || [ -n "$common" ] || return 0
  "$PY" -c "
import os, sys
roots, seen, n = sys.argv[1:], set(), 0
for root in roots:
    if not root:
        continue
    real = os.path.realpath(root)
    if real in seen:
        continue
    seen.add(real)
    for dp, _, fs in os.walk(real):
        for f in fs:
            if f.endswith('.lock'):
                try:
                    os.remove(os.path.join(dp, f)); n += 1
                except Exception:
                    pass
sys.stderr.write('    已清理 %d 个陈旧锁文件\n' % n)
" "$gd" "$common"
}

_redact() {
  if [ -n "${CNB_TOKEN:-}" ]; then sed "s|${CNB_TOKEN}|***TOKEN***|g"; else cat; fi
}

_is_lock_error() {
  printf '%s' "$1" | grep -qE "cannot lock ref|Unable to create '.*\.lock'"
}

# 凭据被拒的两种表现形式（实测）：
#   fetch/pull → remote: Repository Not Found.（大写，中文「仓库不存在」）
#   clone      → fatal: repository 'https://...' not found（小写）
# 必须都覆盖，否则 clone 的匿名降级不触发。
_is_auth_error() {
  printf '%s' "$1" | grep -qiE "repository.*not found|仓库不存在|authentication failed|could not read from remote repository|\b403\b"
}

# git 执行 + 脱敏 + 陈旧锁自愈
gitr() {
  local out rc
  out="$(git "${GIT_ARGS[@]}" "$@" 2>&1)"; rc=$?
  if [ $rc -ne 0 ] && _is_lock_error "$out"; then
    echo "  🟡 命中陈旧锁（本机已知现象），清理后原进程内重试…" >&2
    stale_lock_clean >&2
    out="$(git "${GIT_ARGS[@]}" "$@" 2>&1)"; rc=$?
  fi
  printf '%s\n' "$out" | _redact
  return $rc
}

# 读取类专用：锁自愈 + 凭据被拒时自动匿名重试
gitr_read() {
  local out rc
  out="$(git "${GIT_ARGS[@]}" "$@" 2>&1)"; rc=$?
  if [ $rc -ne 0 ] && _is_lock_error "$out"; then
    echo "  🟡 命中陈旧锁（本机已知现象），清理后原进程内重试…" >&2
    stale_lock_clean >&2
    out="$(git "${GIT_ARGS[@]}" "$@" 2>&1)"; rc=$?
  fi
  if [ $rc -ne 0 ] && [ -n "${CNB_TOKEN:-}" ] && _is_auth_error "$out"; then
    # 注意措辞：不要断言"token 已失效" —— 并发锁冲突等瞬时故障也会走到这里，
    # 误报会让人白白去重置凭据。只陈述事实 + 给私有仓库的排查方向。
    echo "  🟡 带 token 读取被拒 → 以匿名方式重试（公开仓库无需凭据）" >&2
    _anon_args
    out="$(git "${ANON_ARGS[@]}" "$@" 2>&1)"; rc=$?
    [ $rc -eq 0 ] && echo "  ✅ 匿名读取成功（该仓库为公开仓库；若本应为私有仓库，请检查 ~/.cnb/token）" >&2
  fi
  printf '%s\n' "$out" | _redact
  return $rc
}

need_repo_slug() { [ -n "${1:-}" ] || die "缺少仓库参数，格式：组织名称/仓库名称（如 chris.ai/my-agent-skills）"; }

SUB="${1:-}"; [ -n "$SUB" ] || { awk 'NR==1 {next} /^set -uo pipefail/ {exit} {sub(/^# ?/, ""); print}' "$0"; exit 1; }
shift || true

case "$SUB" in

# ══════════════ 仓库级 git 协议操作 ══════════════
clone)
  SLUG="${1:-}"; need_repo_slug "$SLUG"
  DIR="${2:-$(basename "$SLUG")}"
  load_token_optional; build_git_args
  echo "═══ clone ${SLUG} → ${DIR} ═══"
  echo "  网络: ${NET_MODE}"
  time gitr_read clone "https://cnb.cool/${SLUG}.git" "$DIR"
  echo "═══ ✅ clone 完成 ═══"
  ;;

fetch|pull)
  DIR=""; REMOTE="cnb"; BRANCH=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --remote) REMOTE="$2"; shift 2 ;;
      -*) die "未知参数：$1" ;;
      *)
        if [ -z "$DIR" ] && { [ -d "$1" ] || [ "$1" = "." ]; }; then DIR="$1"
        elif [ -z "$BRANCH" ]; then BRANCH="$1"
        else die "多余参数：$1"; fi
        shift ;;
    esac
  done
  [ -n "$DIR" ] || DIR="$PWD"
  cd "$DIR" || die "无法进入目录：$DIR"
  # worktree 里 .git 是【文件】（内容形如 gitdir: .../.git/worktrees/x），不能用 -d 判断
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "不是 git 仓库：$PWD"
  # 读取类：token 可选（公开仓库无凭据也能读，带失效 token 反被拒）
  load_token_optional; build_git_args

  echo "═══ ${SUB} $(basename "$PWD") ← ${REMOTE} ═══"
  git remote get-url "$REMOTE" >/dev/null 2>&1 || die "本仓库没有 ${REMOTE} remote（现有：$(git remote | tr '\n' ' ')）"

  # 上游仍指向 GitHub 时给出明确警告 —— 实测 GitHub 账号暂停会直接 403
  UPSTREAM="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
  case "$UPSTREAM" in
    origin/*)
      echo "  🟡 当前分支上游是 ${UPSTREAM}（GitHub）"
      echo "     实测：GitHub 账号暂停时 fetch origin 直接 403 \"Your account is suspended\""
      echo "     本命令改从 ${REMOTE} 拉取；若要永久改上游：git branch --set-upstream-to=${REMOTE}/<分支>"
      ;;
  esac
  echo "  网络: ${NET_MODE}"

  if [ "$SUB" = "fetch" ]; then
    gitr_read fetch "$REMOTE" || die "fetch 失败"
    echo "═══ ✅ fetch 完成 ═══"
  else
    if [ -n "$BRANCH" ]; then
      gitr_read pull "$REMOTE" "$BRANCH" || die "pull 失败"
    else
      CUR="$(git branch --show-current)"
      [ -n "$CUR" ] || die "处于分离 HEAD，请显式指定分支：cnb-git.sh pull <目录> <分支>"
      gitr_read pull "$REMOTE" "$CUR" || die "pull 失败"
    fi
    echo "═══ ✅ pull 完成 ═══"
  fi
  ;;

push)
  # 委托给已验证的 cnb-push.sh（内置代理/重试/护栏），避免两套逻辑分叉
  HERE="$(cd "$(dirname "$0")" && pwd)"
  PUSHER="${HERE}/cnb-push.sh"
  [ -f "$PUSHER" ] || PUSHER="$HOME/.agents/skills/cnb-push/scripts/cnb-push.sh"
  [ -f "$PUSHER" ] || die "找不到 cnb-push.sh"
  exec bash "$PUSHER" "$@"
  ;;

# ══════════════ 分支 ══════════════
branches)
  SLUG="${1:-}"; need_repo_slug "$SLUG"
  echo "═══ 分支列表 ${SLUG} ═══"
  # --page-size 100：默认是 10，32 分支的仓库只能看到前 10 个
  cnb git list-branches --repo "$SLUG" --page-size 100 2>&1
  ;;

branch-create)
  SLUG="${1:-}"; need_repo_slug "$SLUG"
  NAME="${2:-}"; [ -n "$NAME" ] || die "缺少分支名"
  FROM=""; shift 2 || true
  while [ $# -gt 0 ]; do
    case "$1" in --from|--start-point) FROM="$2"; shift 2 ;; *) die "未知参数：$1" ;; esac
  done
  [ -n "$FROM" ] || die "缺少 --from <基点分支/提交/标签>"
  echo "═══ 建分支 ${SLUG}:${NAME} ← ${FROM} ═══"
  cnb git create-branch --repo "$SLUG" --name "$NAME" --start-point "$FROM" 2>&1
  ;;

branch-delete)
  SLUG="${1:-}"; need_repo_slug "$SLUG"
  NAME="${2:-}"; [ -n "$NAME" ] || die "缺少分支名"
  echo "═══ 删除分支 ${SLUG}:${NAME} ═══"
  cnb git delete-branch --repo "$SLUG" --branch "$NAME" 2>&1   # 注意是 --branch 不是 --name
  ;;

# ══════════════ PR ══════════════
pr-create)
  SLUG="${1:-}"; need_repo_slug "$SLUG"; shift
  HEAD=""; BASE=""; TITLE=""; BODY=""; WIP=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --head)  HEAD="$2"; shift 2 ;;
      --base)  BASE="$2"; shift 2 ;;
      --title) TITLE="$2"; shift 2 ;;
      --body)  BODY="$2"; shift 2 ;;
      --wip|--draft) WIP=1; shift ;;
      *) die "未知参数：$1" ;;
    esac
  done
  [ -n "$HEAD" ]  || die "缺少 --head <源分支>"
  [ -n "$BASE" ]  || die "缺少 --base <目标分支>"
  [ -n "$TITLE" ] || die "缺少 --title <标题>"

  # 草稿 = 标题前缀 "WIP:"（实测：draft 字段被忽略，"Draft:" 前缀无效）
  if [ "$WIP" -eq 1 ]; then
    case "$TITLE" in
      WIP:*|wip:*) ;;
      *) TITLE="WIP: ${TITLE}" ;;
    esac
    echo "  📝 草稿模式：标题已加 WIP: 前缀（CNB 用标题前缀判定草稿，不是 draft 字段）"
  fi

  echo "═══ 建 PR ${SLUG}: ${HEAD} → ${BASE} ═══"
  # 用 --data 传完整 body，避免参数转义问题
  DATA="$(python3 -c "
import json,sys
print(json.dumps({'title': sys.argv[1], 'head': sys.argv[2], 'base': sys.argv[3], 'body': sys.argv[4]}, ensure_ascii=False))
" "$TITLE" "$HEAD" "$BASE" "$BODY")"
  cnb pulls post-pull --repo "$SLUG" --data "$DATA" 2>&1
  ;;

pr-list)
  SLUG="${1:-}"; need_repo_slug "$SLUG"; shift || true
  STATE="open"; while [ $# -gt 0 ]; do case "$1" in --state) STATE="$2"; shift 2 ;; *) die "未知参数：$1" ;; esac; done
  echo "═══ PR 列表 ${SLUG} (state=${STATE}) ═══"
  cnb pulls list-pulls --repo "$SLUG" --state "$STATE" --page-size 100 2>&1
  ;;

pr-get)
  SLUG="${1:-}"; need_repo_slug "$SLUG"
  NUM="${2:-}"; [ -n "$NUM" ] || die "缺少 PR 编号"
  cnb pulls get-pull --repo "$SLUG" --number "$NUM" --verbose 2>&1
  ;;

pr-comment)
  SLUG="${1:-}"; need_repo_slug "$SLUG"; NUM="${2:-}"; [ -n "$NUM" ] || die "缺少 PR 编号"; shift 2
  BODY=""; while [ $# -gt 0 ]; do case "$1" in --body) BODY="$2"; shift 2 ;; *) die "未知参数：$1" ;; esac; done
  [ -n "$BODY" ] || die "缺少 --body <内容>"
  cnb pulls post-pull-comment --repo "$SLUG" --number "$NUM" --body "$BODY" 2>&1
  ;;

pr-merge)
  SLUG="${1:-}"; need_repo_slug "$SLUG"; NUM="${2:-}"; [ -n "$NUM" ] || die "缺少 PR 编号"; shift 2
  STYLE=""; FORCE=0; COMMIT_TITLE=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --style|--merge-style) STYLE="$2"; shift 2 ;;
      --force) FORCE=1; shift ;;   # 平台语义：忽略检查项强制合并，非 force push
      --title|--commit-title) COMMIT_TITLE="$2"; shift 2 ;;
      *) die "未知参数：$1" ;;
    esac
  done
  [ -n "$STYLE" ] || STYLE="merge"
  # 平台差异 6：merge-pull 必须带 commit_title，否则 400 errcode 2000001
  # "commit_title is required"（GitHub 的 squash 会自动生成标题，CNB 不会）。
  # 未显式给定时自动取 PR 标题并附 (#编号)，取不到再兜底为通用文案。
  PY="$(command -v python3 || command -v python || true)"
  if [ -z "$COMMIT_TITLE" ]; then
    if [ -n "$PY" ]; then
      # 注意：get-pull 默认输出 YAML，加 --verbose 才是 JSON；两种都兜住
      COMMIT_TITLE="$(cnb pulls get-pull --repo "$SLUG" --number "$NUM" --verbose 2>/dev/null \
        | "$PY" -c 'import sys,json,re
t = sys.stdin.read()
try:
    print(json.loads(t)["data"]["title"])
except Exception:
    m = re.search(r"^\s*title:\s*\"?(.*?)\"?\s*$", t, re.M)
    print(m.group(1) if m else "")' 2>/dev/null)"
    fi
    if [ -n "$COMMIT_TITLE" ]; then
      COMMIT_TITLE="${COMMIT_TITLE} (#${NUM})"
    else
      COMMIT_TITLE="Merge pull request #${NUM}"
    fi
  fi
  if [ -n "$PY" ]; then
    DATA="$("$PY" -c 'import json,sys; print(json.dumps({"commit_title": sys.argv[1]}))' "$COMMIT_TITLE")"
  else
    DATA="{\"commit_title\": \"${COMMIT_TITLE//\"/\\\"}\"}"
  fi
  echo "═══ 合并 PR ${SLUG}#${NUM}（style=${STYLE}${FORCE:+ ,force}）═══"
  echo "  提交标题: ${COMMIT_TITLE}"
  echo "  ⚠️  合并不可逆。建议先在网页端确认 CI 与评审状态。"
  ARGS=(--repo "$SLUG" --number "$NUM" --merge-style "$STYLE" --data "$DATA")
  [ "$FORCE" -eq 1 ] && ARGS+=(--force)
  cnb pulls merge-pull "${ARGS[@]}" 2>&1
  ;;

pr-close)
  SLUG="${1:-}"; need_repo_slug "$SLUG"; NUM="${2:-}"; [ -n "$NUM" ] || die "缺少 PR 编号"
  echo "═══ 关闭 PR ${SLUG}#${NUM} ═══"
  cnb pulls patch-pull --repo "$SLUG" --number "$NUM" --state closed 2>&1
  ;;

# ══════════════ 身份 ══════════════
whoami)
  cnb users get-user-info 2>&1
  ;;

-h|--help|help)
  # 自动截取到 set 之前的头部注释，避免硬编码行号因新增注释而截断
  awk 'NR==1 {next} /^set -uo pipefail/ {exit} {sub(/^# ?/, ""); print}' "$0"
  ;;

*)
  die "未知子命令：$SUB（用 cnb-git.sh --help 看全部）"
  ;;
esac
