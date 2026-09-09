#!/usr/bin/env bash
# 按登记范围恢复，保留不同的本机修改；不自动提交或推送。
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$REPO_DIR/scripts/restore-bundle.py"
python3 "$REPO_DIR/scripts/manage-skills.py" apply "$@"
echo "已核验登记入口；重新打开会话后可加载新目录。"
