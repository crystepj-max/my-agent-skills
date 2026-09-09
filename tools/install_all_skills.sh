#!/usr/bin/env bash
# 旧命令的兼容入口；禁止重新启用历史包中的全量技能。
set -euo pipefail
TASK_REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
exec bash "$TASK_REPO_DIR/scripts/restore.sh" "$@"
