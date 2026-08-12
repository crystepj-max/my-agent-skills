#!/usr/bin/env bash
# 跨设备恢复：在全新/存量电脑上恢复我的常用 skill。
# 用法：bash scripts/restore.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS=~/.agents/skills
mkdir -p "$AGENTS"

echo "==> 仓库根: $REPO_DIR"
echo "==> 公共池: $AGENTS"

# 1) 自有 skill（完整数据）软链进公共池
echo
echo "=== [1/4] 软链自有 skill -> $AGENTS ==="
for d in "$REPO_DIR"/my-skills/*/; do
  [ -d "$d" ] || continue
  name=$(basename "$d")
  target="$AGENTS/$name"
  if [ -L "$target" ] || [ -e "$target" ]; then
    echo "  跳过已存在: $name"
  else
    ln -s "$d" "$target"
    echo "  软链: $name -> $target"
  fi
done

# 2) 第三方轻量 skill（一键原样，字节级一致）
echo
echo "=== [2/4] 安装 65 个轻量第三方 skill ==="
if [ -f "$REPO_DIR/tools/install_all_skills.sh" ]; then
  bash "$REPO_DIR/tools/install_all_skills.sh"
else
  echo "  未找到 install_all_skills.sh，跳过"
fi

# 3) 桥接到 claude / codex / workbuddy
echo
echo "=== [3/4] 桥接各 agent ==="
BRIDGE="$REPO_DIR/my-skills/agent-skill-bridge/scripts/bridge.py"
if [ -f "$BRIDGE" ]; then
  if command -v python3 >/dev/null 2>&1; then
    python3 "$BRIDGE" --mode apply || echo "  桥接失败，请检查 python3 与 bridge.py"
  else
    echo "  未找到 python3，跳过桥接（请手动运行 bridge.py --mode apply）"
  fi
else
  echo "  未找到 agent-skill-bridge，跳过桥接"
fi

# 4) 手动步骤提示
echo
echo "=== [4/4] 需手动处理的部分 ==="
echo "  • 5 个大体积第三方 skill（走仓库链接安装，体积约 139MB，不建议入库）："
echo "      ppt-master / humanize-ppt / beautiful-html-templates / baoyu-slide-deck / guizang-ppt-skill"
echo "  • 15 个 WorkBuddy 内置/市场 skill（在 WorkBuddy 技能市场安装）："
echo "      edit-article、find-skills、frontend-design、git-guardrails-claude-code、hatch-pet、"
echo "      migrate-to-shoehorn、neat-freak、obsidian-vault、remotion-best-practices、"
echo "      remotion-video-production、scaffold-exercises、setup-pre-commit、skill-creator、"
echo "      storage-analyzer、video-production"
echo
echo "完成。请重启 claude / codex / workbuddy 会话，使 / 命令刷新。"
