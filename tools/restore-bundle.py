#!/usr/bin/env python3
"""Compatibility entry point for scripts/restore-bundle.py."""
import runpy
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
canonical = repo / "scripts" / "restore-bundle.py"
if not canonical.is_file():
    raise SystemExit(f"canonical restore script not found: {canonical}")
runpy.run_path(str(canonical), run_name="__main__")
