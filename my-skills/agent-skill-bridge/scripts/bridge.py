#!/usr/bin/env python3
"""兼容旧调用名，转交按范围管理的唯一实现。"""
import argparse
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mode', choices=['dry', 'apply', 'verify'], default='dry')
parser.add_argument('--no-sync', action='store_true', help='兼容旧参数；所有模式都不自动发布')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
script = repo / 'scripts/manage-skills.py'
if not script.is_file():
    parser.error('维护仓库缺失，请恢复 my-agent-skills；不要用安装副本覆盖维护源')
sys.exit(subprocess.call([sys.executable, str(script), {'dry':'plan', 'apply':'apply', 'verify':'check'}[args.mode]]))
