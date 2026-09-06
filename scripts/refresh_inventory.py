#!/usr/bin/env python3
"""刷新公共 skill 清单的「最新更新」列（布局安全版，自适应列数）。

设计约束（防止再次回滚人工排版优化）：
- 只更新表格最后一列「最新更新」，绝不改动列结构、章节顺序或任何文字描述。
- 清单现为三块表（第一方 7 列 / 第三方 8 列 / 参考 8 列），本脚本按行首数字 + 名称
  识别数据行，按「单元格数 - 1」定位最后一列（最新更新），与具体列数无关。
- 非表格行（标题、前言、表头、分隔符、元数据章节、合计、说明）一律原样保留。

读取 inventory/skill-desc-translation.md，按「仓库链接 / 来源」列（名称列之后的第 2 格）
重新拉取 GitHub 仓库 pushed_at，仅重写最后一列后写回同一文件。
无公开仓库（平台内置 / 市场 skill）标记为「平台内置」。

依赖：gh CLI 已登录（用于 GitHub API）。
用法：python3 scripts/refresh_inventory.py
"""
import os, re, subprocess, json

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
INV = os.path.join(REPO, "inventory", "skill-desc-translation.md")

# 匹配任意列数的数据行：首列数字、次列 `name`、其后为单元格，最后以 `|` 结尾。
# 组1=序号，组2=名称，组3=名称之后的全部内容（含各单元格与末尾 `|`）。
ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|(.*)\|\s*$")
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
        num, name, rest = m.groups()
        # 拆分名称之后的单元格（去掉首尾空格），最后一格即「最新更新」
        cells = [c.strip() for c in rest.strip().split("|")]
        if not cells:
            out.append(ln)
            continue
        upd = cells[-1]
        # 「仓库链接 / 来源」位于名称之后的第 2 格（第一方为「参考的 skill」，无链接则跳过）
        src_cell = cells[1] if len(cells) >= 2 else ""
        r = repo_of(src_cell)
        if r:
            data = gh_api(f"repos/{r}")
            new_upd = (data.get("pushed_at", "N/A")[:10]
                       if (data and data.get("pushed_at")) else "N/A")
            if new_upd != "N/A":
                upd = new_upd
                refreshed += 1
        cells[-1] = upd
        out.append(f"| {num} | `{name}` | {' | '.join(cells)} |")

    with open(INV, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"已刷新「最新更新」列（仅更新数据，未改动排版与章节）：刷新 {refreshed} 行。文件: {INV}")


if __name__ == "__main__":
    main()
