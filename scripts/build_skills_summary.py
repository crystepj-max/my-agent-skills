#!/usr/bin/env python3
"""从机器登记 inventory/skill-policy.json 生成人读总表。"""
from __future__ import annotations

from collections import Counter
from datetime import date
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "inventory/skill-policy.json"
OUTPUT = ROOT / "inventory/skills-summary.md"

STATE_ZH = {
    "active": "启用",
    "transition": "迁移中",
    "reference": "仅参考",
    "retired": "已退役",
}
ORIGIN_ZH = {"first-party": "第一方维护", "third-party": "第三方来源"}


def main() -> None:
    config = json.loads(POLICY.read_text(encoding="utf-8"))
    entries = sorted(config["skills"], key=lambda row: row["name"].casefold())
    states = Counter(row["state"] for row in entries)
    origins = Counter(row["origin"] for row in entries)
    scopes = Counter(row["scope"] for row in entries)

    lines = [
        "# Skills 总览",
        "",
        "> 本文件由 `scripts/build_skills_summary.py` 根据 `inventory/skill-policy.json` 生成，请勿手工编辑。",
        "> 机器操作以 JSON 策略为准；中文描述、来源证据和重要修订分别维护在下列人读子表。",
        "",
        "## 查阅入口",
        "",
        "| 内容 | 文件 |",
        "|---|---|",
        "| 中文描述 | [skills/descriptions-zh.md](skills/descriptions-zh.md) |",
        "| 作者、来源与上游版本 | [skills/provenance.md](skills/provenance.md) |",
        "| 重要修订记录 | [skills/revision-history.md](skills/revision-history.md) |",
        "| 机器登记与执行策略 | [skill-policy.json](skill-policy.json) |",
        "",
        "## 登记概况",
        "",
        f"共 **{len(entries)}** 项：第一方维护 **{origins['first-party']}** 项，第三方来源 **{origins['third-party']}** 项。",
        "",
        "| 状态 | 数量 |",
        "|---|---:|",
    ]
    for state in ("active", "transition", "reference", "retired"):
        lines.append(f"| {STATE_ZH[state]} | {states[state]} |")
    lines.extend(["", "| 使用范围 | 数量 |", "|---|---:|"])
    for scope, count in sorted(scopes.items()):
        lines.append(f"| `{scope}` | {count} |")

    lines.extend([
        "",
        "## Skills 总表",
        "",
        "来源列展示当前正式维护/保留路径；它不单独证明最初作者或原创性。来源细节及证据见来源子表。",
        "",
        "| Skill | 归属 | 状态 | 范围 | 正式来源/维护源 | 描述 | 来源档案 |",
        "|---|---|---|---|---|---|---|",
    ])
    for row in entries:
        name = row["name"]
        source = row.get("source", "—").replace("|", "\\|")
        lines.append(
            f"| `{name}` | {ORIGIN_ZH.get(row.get('origin'), row.get('origin', '未登记'))} "
            f"| {STATE_ZH.get(row.get('state'), row.get('state', '未登记'))} "
            f"| `{row.get('scope', '—')}` | `{source}` "
            f"| [描述](skills/descriptions-zh.md) "
            f"| [来源](skills/provenance.md) |"
        )
    lines.append("")
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成 {OUTPUT.relative_to(ROOT)}：{len(entries)} 项；日期 {date.today().isoformat()}")


if __name__ == "__main__":
    main()
