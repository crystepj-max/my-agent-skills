#!/usr/bin/env bash
# 仅发布用户已明确要求且已经暂存的改动；不收集其他文件，不强推主分支。
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"
if [ "${1:-}" != "--publish-staged" ] || [ -z "${2:-}" ]; then
  echo '本地管理不自动发布。明确授权发布后：先审阅并暂存指定文件，再运行 sync.sh --publish-staged "提交说明"。'
  exit 2
fi
branch=$(git symbolic-ref --quiet --short HEAD)
[ -n "$branch" ] || exit 1
git diff --cached --check
if git diff --cached --quiet; then
  echo '没有暂存改动。'
  exit 0
fi
git commit -m "$2"
git push origin "HEAD:refs/heads/$branch"
