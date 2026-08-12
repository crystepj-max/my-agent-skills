#!/usr/bin/env bash
# 自动同步：将本仓库（my-agent-skills）的变更提交并推送到 GitHub main 分支。
# 用法：bash scripts/sync.sh
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

# 仅在确有变更时提交
if git diff --quiet && git diff --cached --quiet; then
  echo "无变更，跳过提交。"
  exit 0
fi

git add -A
DATE=$(date +%Y-%m-%d)
git commit -m "sync: 更新自有 skill 与清单 ($DATE)"
# 推送到远端 main（不论本地分支名）
git push origin HEAD:main
echo "已推送到 main。"
