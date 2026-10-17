#!/usr/bin/env python3
"""Fail-closed compatibility entry point for the retired installer.

The old command downloaded upstream files directly into ~/.agents/skills,
which can now point at first-party maintained sources. Keep this filename as
a safe stop so old instructions cannot reactivate or overwrite those sources.
"""

import sys


def main() -> int:
    print("此旧安装入口已停用：不会联网、写入或覆盖任何技能目录。")
    print("如需查看上游变化，请使用只读工具：python3 tools/compare_skill_reference.py。")
    print("需要获取独立快照时，请使用：python3 tools/fetch_skill_reference.py。")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
