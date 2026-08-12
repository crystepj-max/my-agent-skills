#!/usr/bin/env python3
"""刷新公共 skill 清单的「最新更新」列（仓库自包含版）。

读取本仓库 inventory/skill-desc-translation.md，按「仓库链接 / 来源」列
重新拉取各 GitHub 仓库的 pushed_at，重写「最新更新」列并写回同一文件。

无公开仓库（平台内置/市场 skill）标记为「平台内置」。
依赖：gh CLI 已登录（用于 GitHub API）。
用法：python3 scripts/refresh_inventory.py
"""
import os, re, subprocess, json
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
INV = os.path.join(REPO, "inventory", "skill-desc-translation.md")

# 5 列表格行： # | name | desc | src | upd
ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$"
)
HDR_RE = re.compile(r"^\|\s*#\s*\|")
LINK_RE = re.compile(r"github\.com/([A-Za-z0-9._-]+)/([A-Za-z0-9._-]+)")


def gh_api(path):
    try:
        out = subprocess.run(["gh", "api", path], capture_output=True,
                             text=True, timeout=30)
        if out.returncode != 0:
            return None
        return json.loads(out.stdout)
    except Exception:
        return None


def repo_of(cell):
    m = LINK_RE.search(cell or "")
    return f"{m.group(1)}/{m.group(2)}" if m else None


def main():
    with open(INV, encoding="utf-8") as f:
        lines = f.read().splitlines()

    intro, table_header, rows = [], None, []
    for ln in lines:
        if HDR_RE.match(ln):
            table_header = ln
            continue
        m = ROW_RE.match(ln)
        if m:
            rows.append(m)
        else:
            if "合计" in ln:
                continue
            intro.append(ln)

    # 拉取去重后的仓库最新推送时间
    repos = {}
    for m in rows:
        r = repo_of(m.group(4))
        if r and r not in repos:
            repos[r] = None
    print(f"distinct repos: {len(repos)}")
    for r in sorted(repos):
        data = gh_api(f"repos/{r}")
        repos[r] = (data.get("pushed_at", "N/A")[:10]
                    if (data and data.get("pushed_at")) else "N/A")
        print(f"  {r} -> {repos[r]}")

    n = len(rows)
    out = []
    for ln in intro:
        ln = ln.replace("共 70 个", f"共 {n} 个")
        ln = ln.replace("合计：70 个", f"合计：{n} 个")
        out.append(ln)
    out.append(table_header)
    out.append("|---|---|---|---|---|")
    for m in rows:
        num, name, desc, src_cell, _old = m.groups()
        r = repo_of(src_cell)
        upd = "平台内置" if r is None else repos.get(r, "N/A")
        out.append(f"| {num} | `{name}` | {desc} | {src_cell} | {upd} |")
    out.append("")
    out.append(f"**合计：{n} 个 skill 描述已全部中文化，并标注最新更新。**")
    out.append("")
    out.append("> **「最新更新」列**：通过各仓库 `pushed_at` 自动获取，按来源分类展示。无公开仓库的 WorkBuddy 内置/市场 skill 标记为「平台内置」。可运行 `scripts/refresh_inventory.py` 刷新。")

    with open(INV, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"\nwritten: {INV}  ({n} rows)")


if __name__ == "__main__":
    main()
