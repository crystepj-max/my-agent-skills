#!/usr/bin/env python3
"""只读扫描：导出 skill 池中每个 skill 的 name/description。"""
import os
import re
import sys

POOLS = sys.argv[1:] or [r"C:\Users\22487\.workbuddy\skills"]


def parse_frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return {}
    fm = m.group(1)
    out = {}
    lines = fm.split("\n")
    key = None
    buf = []
    for line in lines:
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km:
            if key:
                out[key] = "\n".join(buf).strip()
            key = km.group(1)
            buf = [km.group(2)]
        elif key:
            buf.append(line)
    if key:
        out[key] = "\n".join(buf).strip()
    for k, v in out.items():
        v = v.strip()
        if v.startswith(("|", ">", '"', "'")):
            v = v.lstrip("|>\"'").strip()
        if v.endswith(('"', "'")):
            v = v[:-1]
        out[k] = re.sub(r"\s+", " ", v)
    return out


for pool in POOLS:
    print(f"### POOL: {pool}")
    if not os.path.isdir(pool):
        print("  (not found)")
        continue
    for name in sorted(os.listdir(pool)):
        p = os.path.join(pool, name)
        if not os.path.isdir(p):
            continue
        skill_md = os.path.join(p, "SKILL.md")
        if not os.path.isfile(skill_md):
            print(f"  {name:<38} | (NO SKILL.md)")
            continue
        with open(skill_md, encoding="utf-8", errors="replace") as f:
            txt = f.read()
        fm = parse_frontmatter(txt)
        desc = fm.get("description", "(no desc)")
        print(f"  {name:<38} | {desc[:260]}")
    print()
