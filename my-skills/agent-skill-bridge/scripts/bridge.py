#!/usr/bin/env python3
"""兼容旧调用名，转交按范围管理的唯一实现。"""
import argparse
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mode', choices=['dry', 'apply', 'verify', 'cn'], default='dry')
parser.add_argument('--no-sync', action='store_true', help='兼容旧参数；所有模式都不自动发布')
parser.add_argument('--cn-scope', default='managed', choices=['managed', 'all'],
                    help='cn 模式校验范围：managed=登记表内（默认）；all=并查未登记条目')
parser.add_argument('--fix', action='store_true',
                    help='已废弃：cn 模式只做只读校验。自动改写 description 需先备份再人工确认，'
                         '不接受无人审阅的自动写入。')
args = parser.parse_args()
if args.fix:
    parser.error('cn --fix 已移除：守护只做只读校验并如实报告，不自动改写文件。'
                 '请按报告用 Edit 逐项翻译为中文。')
repo = Path(__file__).resolve().parents[3]
script = repo / 'scripts/manage-skills.py'
if not script.is_file():
    parser.error('维护仓库缺失，请恢复 my-agent-skills；不要用安装副本覆盖维护源')
mode = {'dry': 'plan', 'apply': 'apply', 'verify': 'check', 'cn': 'cn'}[args.mode]
command = [sys.executable, str(script), mode]
if mode == 'cn':
    command += ['--cn-scope', args.cn_scope]
sys.exit(subprocess.call(command))
