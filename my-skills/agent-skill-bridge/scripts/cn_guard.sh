#!/usr/bin/env bash
# 中文化守护：校验已登记技能的 description 是否仍为中文。
# 从上游更新/重装 skill 后跑一次，防止官方英文覆盖掉中文描述。
#
# 用法：
#   bash ~/.agents/skills/agent-skill-bridge/scripts/cn_guard.sh          # 登记表内技能
#   bash ~/.agents/skills/agent-skill-bridge/scripts/cn_guard.sh --all    # 并查未登记条目
#
# 退出码（直接来自 manage-skills.py cn 模式，不做二次推断）：
#   0 = 守护通过
#   1 = 有纯英文 / 缺失 description，需 LLM 翻译
#   2 = 环境异常（维护源缺失、目标不可读、校验范围为空）

set -uo pipefail

BRIDGE_DIR=~/.agents/skills/agent-skill-bridge/scripts
BRIDGE="$BRIDGE_DIR/bridge.py"

if [ ! -f "$BRIDGE" ]; then
  echo "✗ 未找到 bridge.py: $BRIDGE" >&2
  echo "  请恢复 my-agent-skills 维护源；不要用安装副本反向覆盖仓库。" >&2
  exit 2
fi

SCOPE_FLAG=()
if [ "${1:-}" = "--all" ]; then
  SCOPE_FLAG=(--cn-scope all)
fi

cd "$BRIDGE_DIR" || exit 2

# 关键：直接透传子进程退出码，不解析输出文本。
# 旧实现用 `grep -qE '\[需 LLM 翻译\] [1-9]...'` 判断，工具报错时 grep 无匹配 →
# 误判「守护通过」并 exit 0，形成假绿灯。退出码是唯一可信信号。
# 本模式只读：不做自动改写，避免无人审阅地覆盖已核对的中文描述。
python3 bridge.py --mode cn "${SCOPE_FLAG[@]+"${SCOPE_FLAG[@]}"}"
exit $?
