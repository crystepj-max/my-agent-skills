#!/usr/bin/env python3
"""Build a compact self-extracting installer for the LIGHTWEIGHT skills
(all skills except the 5 with large binary assets). Those 5 are installed
from their repo links instead. Uses ~ so it works on any machine.
"""
import os
import io
import tarfile
import base64

SRC = os.path.expanduser("~/.agents/skills")
OUT = "/Users/chris/WorkBuddy/2026-08-01-16-08-33/install_all_skills.sh"

# 5 heavy skills that ship large local binary assets (templates/images/build).
# Reinstall these from their repo links instead of bundling.
HEAVY = {
    "ppt-master", "humanize-ppt", "beautiful-html-templates",
    "baoyu-slide-deck", "guizang-ppt-skill",
}

def make_archive() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        tar.add(SRC, arcname="skills", recursive=True,
                filter=lambda ti: None if (
                    os.sep + ".git" in ti.name
                    or ti.name.endswith(".git")
                    or any(("/" + h + "/") in ti.name or ti.name.endswith("/" + h) for h in HEAVY)
                ) else ti)
    return buf.getvalue()

data = make_archive()
b64 = base64.b64encode(data).decode()

# list what got bundled for the summary
with tarfile.open(fileobj=io.BytesIO(data)) as t:
    bundled = sorted({m.name.split("/")[1] for m in t.getmembers() if m.name.count("/") >= 1 and m.name != "skills/"})

script = r'''#!/usr/bin/env bash
set -euo pipefail
# install_all_skills.sh
# 一键将「轻量」公共池 skill 原样安装到 ~/.agents/skills/，并桥接到已存在的 agent 目录。
# 注：5 个含大型二进制资源的 skill（ppt-master / humanize-ppt / beautiful-html-templates /
#     baoyu-slide-deck / guizang-ppt-skill）请用其仓库链接安装，本脚本不打包它们。
B64='B64_PLACEHOLDER'

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

printf '%s' "$B64" | base64 -d | tar -xz -C "$TMP"

POOL=~/.agents/skills
mkdir -p "$POOL"
n=0
for d in "$TMP"/skills/*/; do
  [ -d "$d" ] || continue
  name=$(basename "$d")
  dest="$POOL/$name"
  rm -rf "$dest"
  cp -R "$d" "$dest"
  n=$((n+1))
done

bridge_into() {
  local dir="$1"
  [ -d "$dir" ] || return 0
  for d in "$POOL"/*/; do
    [ -d "$d" ] || continue
    name=$(basename "$d")
    target="$dir/$name"
    if [ -L "$target" ] || [ ! -e "$target" ]; then
      rm -rf "$target" 2>/dev/null || true
      ln -s "$d" "$target"
    fi
  done
}
bridge_into ~/.workbuddy/skills
bridge_into ~/.claude/skills
bridge_into ~/.config/claude/skills
bridge_into ~/.codex/skills

echo "✅ 已安装 $n 个轻量 skill 到 $POOL"
echo "   余下 5 个含大体积资源的 skill 请用 skill-desc-translation.md 中的仓库链接安装。"
'''.replace("B64_PLACEHOLDER", b64)

with open(OUT, "w") as f:
    f.write(script)
os.chmod(OUT, 0o755)
print(f"archive={len(data)}B  script={len(script)}B  bundled_skills={len(bundled)}")
print("bunded:", ", ".join(bundled))
