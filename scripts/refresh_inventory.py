#!/usr/bin/env python3
"""刷新公共 skill 清单的「最新更新」列（布局安全版）。

设计约束（防止再次回滚人工排版优化）：
- 只更新表格最后一列「最新更新」，绝不改动列结构、章节顺序或任何文字描述。
- 表格为 7 列：# | 名称 | 中文描述 | 仓库链接 / 来源 | 作者 | 仓库简介 | 最新更新。
- 非表格行（标题、前言、表头、分隔符、元数据章节、合计、说明）一律原样保留。

读取 inventory/skill-desc-translation.md，按「仓库链接 / 来源」列重新拉取
GitHub 仓库 pushed_at，仅重写最后一列后写回同一文件。
无公开仓库（平台内置 / 市场 skill）标记为「平台内置」。

依赖：gh CLI 已登录（用于 GitHub API）。
用法：python3 scripts/refresh_inventory.py
"""
import os, re, subprocess, json

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
INV = os.path.join(REPO, "inventory", "skill-desc-translation.md")

# 7 列数据行：# | name | desc | src | author | repo_desc | upd（布局安全：不吃掉任何列）
ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$"
)
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

    out = []
    refreshed = 0
    for ln in lines:
        m = ROW_RE.match(ln)
        if not m:
            out.append(ln)  # 非数据行：原样保留（不触碰排版 / 章节 / 描述）
            continue
        num, name, desc, src, author, repo_desc, upd = m.groups()
        r = repo_of(src)
        if r:
            data = gh_api(f"repos/{r}")
            new_upd = (data.get("pushed_at", "N/A")[:10]
                       if (data and data.get("pushed_at")) else "N/A")
            if new_upd != "N/A":
                upd = new_upd
                refreshed += 1
        out.append(f"| {num} | `{name}` | {desc} | {src} | {author} | {repo_desc} | {upd} |")

    with open(INV, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"已刷新「最新更新」列（仅更新数据，未改动 7 列排版与章节）：刷新 {refreshed} 行。文件: {INV}")


if __name__ == "__main__":
    main()
