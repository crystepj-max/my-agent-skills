#!/usr/bin/env python3
"""只恢复登记表需要且本机缺失的资料，不运行历史全量安装器。"""
import importlib.util
import json
import tarfile
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('manager', repo/'scripts/manage-skills.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
config = json.loads((repo/'inventory/skill-policy.json').read_text())
manager = module.Manager(repo, config)
bundle = repo/'tools/skills-bundle.tar.gz'
if not bundle.is_file():
    raise SystemExit('恢复包缺失；未运行旧全量安装器')

targets = {}
for entry in config['skills']:
    if entry['origin'] == 'third-party' and entry['scope'] == 'global' and entry['state'] in {'transition', 'reference'}:
        targets['skills/'+entry['name']] = manager.expand(entry['source'])
for entry in config.get('reference_copies', []):
    targets['references/'+entry['name']] = manager.expand(entry['destination'])

with tarfile.open(bundle) as archive:
    members = archive.getmembers()
    for prefix, target in targets.items():
        if target.exists() or target.is_symlink():
            continue
        selected = [item for item in members if item.name.startswith(prefix+'/')]
        if not selected:
            continue
        for item in selected:
            rel = Path(item.name[len(prefix)+1:])
            if rel.is_absolute() or '..' in rel.parts or not (item.isfile() or item.isdir()):
                raise SystemExit(f'恢复包包含不允许的路径或类型：{item.name}')
        for item in selected:
            dest = target / item.name[len(prefix)+1:]
            if item.isdir():
                dest.mkdir(parents=True, exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(archive.extractfile(item).read())
                dest.chmod(item.mode & 0o777)
        print('恢复资料：'+str(target))
