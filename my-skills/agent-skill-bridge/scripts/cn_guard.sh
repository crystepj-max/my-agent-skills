#!/usr/bin/env bash
# 中文化守护（A 方案落地）：从上游更新/重装 skill 后跑一次，
# 确保 description 不被官方英文覆盖。封装 bridge.py --mode cn 的闭环。
#
# 用法：
#   bash ~/.agents/skills/agent-skill-bridge/scripts/cn_guard.sh
#
# 退出码：
#   0 = 全部中文（守护通过）
#   1 = 仍有纯英文/空 description 待翻译（见上方清单）
#   2 = 环境异常（未找到 bridge.py）

set -uo pipefail

BRIDGE_DIR=~/.agents/skills/agent-skill-bridge/scripts
BRIDGE="$BRIDGE_DIR/bridge.py"

if [ ! -f "$BRIDGE" ]; then
  echo "未找到 bridge.py: $BRIDGE" >&2
  exit 2
fi

cd "$BRIDGE_DIR" || exit 2

echo "== 步骤1：自动归一化中英夹杂项（写入公共池 + WorkBuddy 原生 skill）=="
OUT=$(python3 bridge.py --mode cn --fix)
echo "$OUT"

if echo "$OUT" | grep -qE '\[需 LLM 翻译\] [1-9][0-9]* 项'; then
  echo ""
  echo "⚠️ 仍有纯英文/空 description（见上方 [需 LLM 翻译] 清单）。"
  echo "   处理：用 Edit 把清单里每个 skill 的 description 译为中文，然后重跑本脚本直到显示 ✅。"
  exit 1
else
  echo ""
  echo "✅ 守护通过：你维护的 skill 描述全部为中文，无被覆盖回英文的项。"
  exit 0
fi
