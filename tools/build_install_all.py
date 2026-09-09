#!/usr/bin/env python3
"""构建按登记范围选择的离线资料包，不重新启用全部技能。"""
import importlib.util
import json
import tarfile
from pathlib import Path

repo=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('manager',repo/'scripts/manage-skills.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
config=json.loads((repo/'inventory/skill-policy.json').read_text())
manager=module.Manager(repo,config)
def included(item):
    ignored={'.git','__pycache__','.DS_Store','node_modules','.venv'}
    return None if any(p in ignored for p in Path(item.name).parts) else item
with tarfile.open(repo/'tools/skills-bundle.tar.gz','w:gz',dereference=True) as archive:
    for entry in config['skills']:
        if entry['origin']!='third-party' or entry['scope']!='global' or entry['state'] not in {'transition','reference'}:
            continue
        source=manager.expand(entry['source'])
        if not source.exists() and entry.get('migrate'):
            source=manager.pool/entry['name']
        if not source.exists():
            raise SystemExit('登记来源缺失：'+str(source))
        archive.add(source,arcname='skills/'+entry['name'],filter=included)
    for entry in config.get('reference_copies',[]):
        source=manager.expand(entry['destination'])
        if not source.exists(): source=manager.expand(entry['source'])
        if module.fingerprint(source)!=entry['fingerprint']:
            raise SystemExit('原参考版本不匹配：'+str(source))
        archive.add(source,arcname='references/'+entry['name'],filter=included)
print('已生成按范围恢复包；第一方直接使用仓库来源，专业大型资料留在工作空间')
