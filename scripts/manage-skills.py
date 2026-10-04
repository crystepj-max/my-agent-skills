#!/usr/bin/env python3
"""按登记的状态、来源和范围恢复技能；只移动已核对的入口，保留异动。

模式：
  plan / apply / check  —— 技能入口治理（唯一实现，bridge.py 转交到这里）
  cn                    —— 中文化守护：校验已登记技能的 description 是否仍为中文
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def is_link(path):
    """软链与 Windows 目录联接都是合规入口；未开启开发者模式时只能建联接。"""
    if path.is_symlink():
        return True
    is_junction = getattr(path, 'is_junction', None)
    return bool(is_junction and is_junction())


def make_link(path, source):
    path.symlink_to(source, target_is_directory=True)
    if path.is_symlink():
        return
    if os.name != 'nt':
        raise OSError(f'无法建立入口：{path}')
    # Windows 未开启开发者模式时 symlink_to 会被降级；退回目录联接，仍是单一入口。
    path.rmdir()
    subprocess.run(['cmd', '/c', 'mklink', '/J', str(path), str(source)],
                   check=True, capture_output=True)


def fingerprint(path):
    digest = hashlib.sha256()
    ignored = {'.git', '__pycache__', '.DS_Store', 'node_modules', '.venv'}
    for item in sorted(Path(path).rglob('*')):
        relative = item.relative_to(path)
        if any(part in ignored for part in relative.parts):
            continue
        if item.is_symlink():
            value = ('link:' + os.readlink(item)).encode()
        elif item.is_file():
            value = item.read_bytes()
        else:
            continue
        digest.update(str(relative).encode() + b'\0' + value + b'\0')
    return digest.hexdigest()


class Manager:
    def __init__(self, repo, config, apply=False, user_home=None):
        self.repo = Path(repo).resolve()
        self.home_dir = Path(user_home or Path.home()).resolve()
        self.config = config
        self.apply = apply
        self.rows = []
        self.backup_root = self.home_dir / '.local/share/agent-skills/backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        self.pool = self.expand(config['pool'])
        self.alias_roots = [self.expand(p) for p in config['agent_roots']]

    def expand(self, value):
        if value.startswith('~/'):
            return self.home_dir / value[2:]
        if value.startswith('project:'):
            project, relative = value[8:].split('/', 1)
            return self.expand(self.config['projects'][project]) / relative
        p = Path(value)
        return p if p.is_absolute() else self.repo / p

    def note(self, status, path, detail):
        self.rows.append(dict(status=status, path=str(path), detail=detail))

    def archive(self, path):
        try:
            relative = path.relative_to(self.home_dir)
        except ValueError:
            relative = Path('external') / str(path).lstrip('/')
        dest = self.backup_root / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), dest)
        return dest

    def accepted(self, path, entry):
        if is_link(path):
            return path.resolve() in {(self.pool / entry['name']).resolve(), self.expand(entry['source']).resolve()}
        return path.is_dir() and fingerprint(path) in entry.get('accepted_fingerprints', [])

    def ensure_link(self, path, source, entry):
        if is_link(path) and path.resolve() == source.resolve():
            self.note('OK', path, '来源一致；完整配套材料随正式源更新')
            return
        if path == source:
            self.note('OK', path, '过渡期公共源')
            return
        exists = os.path.lexists(path)
        if exists and not self.accepted(path, entry):
            self.note('CONFLICT', path, '与核对版本不同，保留本机修改')
            return
        self.note('CHANGE', path, f'接入 {source}')
        if self.apply:
            if exists:
                self.archive(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            make_link(path, source)

    def remove_entry(self, path, entry, source):
        if not os.path.lexists(path):
            return
        if not self.accepted(path, entry):
            self.note('CONFLICT', path, '非受管理入口，保留并报告')
            return
        self.note('CHANGE', path, f"退出执行目录；资料保留于 {source}")
        if self.apply:
            self.archive(path)

    def run(self):
        for plugin in self.config.get('owned_plugins', []):
            source = self.expand(plugin['source'])
            if not (source / '.codex-plugin/plugin.json').is_file():
                self.note('MISSING', source, '第一方插件来源缺失')
                continue
            entry = self.expand(plugin['marketplace_entry'])
            if entry.is_symlink() and entry.resolve() == source.resolve():
                self.note('OK', entry, '个人插件市场引用正式维护源')
            elif os.path.lexists(entry):
                self.note('CONFLICT', entry, '保留已有插件来源，不覆盖')
            else:
                self.note('CHANGE', entry, f'恢复个人插件正式来源 {source}')
                if self.apply:
                    entry.parent.mkdir(parents=True, exist_ok=True)
                    entry.symlink_to(source, target_is_directory=True)
        for ref in self.config.get('reference_copies', []):
            source, dest = self.expand(ref['source']), self.expand(ref['destination'])
            if dest.exists():
                if fingerprint(dest) != ref['fingerprint']:
                    self.note('CONFLICT', dest, '参考资料与保留版本不同，未覆盖')
                continue
            if not source.exists() or fingerprint(source) != ref['fingerprint']:
                self.note('MISSING', dest, '未找到原参考版本；不拿新版第一方冒充原资料')
                continue
            self.note('CHANGE', dest, '保留被替代的第三方完整资料')
            if self.apply:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source, dest, symlinks=True)
        for override in self.config.get('overrides', []):
            target = self.expand(override['path'])
            patch = json.loads(self.expand(override['patch']).read_text())
            if not target.is_file():
                if override.get('optional'):
                    continue
                self.note('MISSING', target, '定点修正对象不存在')
                continue
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if digest == patch['updated_sha256']:
                continue
            if digest != patch['original_sha256']:
                self.note('CONFLICT', target, '上游内容改变，需重新审阅修正，不自动套用')
                continue
            content = target.read_text()
            for old, new in patch['replacements']:
                content = content.replace(old, new)
            if hashlib.sha256(content.encode()).hexdigest() != patch['updated_sha256']:
                self.note('CONFLICT', target, '修正产物与已审阅版本不一致')
                continue
            self.note('CHANGE', target, '应用已审阅的定点规则修正')
            if self.apply:
                self.archive(target)
                target.write_text(content)
        names = set()
        for entry in self.config['skills']:
            name = entry['name']
            if name in names or '/' in name or name in {'.', '..'}:
                raise ValueError(f'无效或重复目录名：{name}')
            names.add(name)
            source = self.expand(entry['source'])
            pool_entry = self.pool / name
            global_active = entry['scope'] == 'global' and entry['state'] in {'active', 'transition'}
            project_active = entry['scope'] != 'global' and entry['state'] == 'active'
            if not (source / 'SKILL.md').is_file():
                if entry.get('migrate') and (pool_entry / 'SKILL.md').is_file():
                    if not self.accepted(pool_entry, entry):
                        self.note('CONFLICT', pool_entry, '迁移前内容改变，未覆盖')
                        continue
                    if os.path.lexists(source):
                        self.note('CONFLICT', source, '目标已有不完整或不同资料，未覆盖')
                        continue
                    self.note('CHANGE', source, f'保留完整资料，从 {pool_entry} 迁入')
                    if self.apply:
                        source.parent.mkdir(parents=True, exist_ok=True)
                        # 公共入口若为软链，只复制目标内容；不移动外部拥有的来源。
                        if pool_entry.is_symlink():
                            shutil.copytree(pool_entry, source, symlinks=True)
                        else:
                            shutil.move(str(pool_entry), source)
                else:
                    self.note('MISSING', source, '来源缺失；请恢复已登记资料，不重新启用参考或退役项')
                    continue
            if global_active:
                self.ensure_link(pool_entry, source, entry)
                for target_root in self.alias_roots:
                    if str(target_root) in {str(self.expand(p)) for p in entry.get("excluded_agent_roots", [])}:
                        self.note("EXEMPT", target_root / name, entry.get("exclusion_reason", "登记的宿主独有范围"))
                        continue
                    if target_root.parent.exists():
                        self.ensure_link(target_root / name, source, entry)
            else:
                self.remove_entry(pool_entry, entry, source)
                for target_root in self.alias_roots:
                    self.remove_entry(target_root / name, entry, source)
                if project_active:
                    project_root = self.expand(self.config['projects'][entry['scope']])
                    if not project_root.exists():
                        self.note('MISSING', project_root, '请设置已存在的专业工作空间')
                        continue
                    for relative in self.config['project_entry_roots']:
                        self.ensure_link(project_root / relative / name, source, entry)
            if (source / 'SKILL.md').is_file():
                self.note('SOURCE', source, fingerprint(source))
                manifest = source / 'source-manifest.json'
                if manifest.is_file():
                    for relative, expected in json.loads(manifest.read_text())['files'].items():
                        asset = source / relative
                        if not asset.is_file() or hashlib.sha256(asset.read_bytes()).hexdigest() != expected:
                            self.note('CONFLICT', asset, '配套资产与正式同步版本不同，请从维护源重新同步')
        # 未登记对象只报告；备份和同名发现按实际声明核对，不凭文件夹名称判定。
        declared = {}
        for folder in sorted(self.pool.iterdir()) if self.pool.exists() else []:
            if not (folder / 'SKILL.md').is_file():
                continue
            if folder.name not in names:
                self.note('UNMANAGED', folder, '未登记，未自动改动')
            import re
            match = re.search(r'^name:\s*[\"\']?([^\n\"\']+)', (folder / 'SKILL.md').read_text(), re.M)
            if match:
                declared.setdefault(match[1].strip(), []).append(str(folder))
        for name, paths in declared.items():
            if len(paths) > 1:
                self.note('CONFLICT', name, '同名执行入口：' + ', '.join(paths))
        return self.rows


CJK_RE = re.compile(r'[\u4e00-\u9fff]')
# 「连续 4 个以上英文单词」才判为英文句子；避免把 `skills/foo.md`、`GPT-5.6` 误判。
ENGLISH_SENTENCE = re.compile(r"(?:[A-Za-z][A-Za-z'\-]*\s+){3,}[A-Za-z][A-Za-z'\-]*")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)
DESCRIPTION_RE = re.compile(r"^description:\s*(.*)$", re.M)
BLOCK_SCALAR = ('', '>', '|', '>-', '|-', '>+', '|+')
# 技术类中文描述常内嵌成串英文（报错原文、API 名、CLI 参数），中文占比达标即放行。
CJK_THRESHOLD = 0.15


def cjk_ratio(text):
    body = re.sub(r'\s', '', text or '')
    return len(CJK_RE.findall(body)) / len(body) if body else 0.0


def needs_translation(text):
    """判定 description 是否仍是英文（需 LLM 翻译）。顺序不可颠倒。"""
    if cjk_ratio(text) >= CJK_THRESHOLD:
        return False
    return bool(ENGLISH_SENTENCE.search(text or ''))


def read_description(text):
    """返回 (描述文本, 是否块标量)；无 description 字段时返回 (None, False)。

    块标量（`>`/`|`）会把后续缩进行折叠进来，必须一并读出，否则误判为空。
    """
    matched = FRONTMATTER_RE.match(text)
    if not matched:
        return None, False
    frontmatter = matched.group(1)
    line = DESCRIPTION_RE.search(frontmatter)
    if not line:
        return None, False
    if line.group(1).strip() not in BLOCK_SCALAR:
        return line.group(1).strip(), False
    lines = frontmatter.splitlines()
    for index, current in enumerate(lines):
        if re.match(r'^description:\s*', current):
            cursor, block = index + 1, []
            while cursor < len(lines) and lines[cursor][:1] in (' ', '\t'):
                block.append(lines[cursor].strip())
                cursor += 1
            return '\n'.join(block), True
    return '', True


def cn_targets(config, scope):
    """列出待校验的 (技能名, SKILL.md 路径)。

    managed：登记表内且状态会进入执行目录的技能（active/transition）。
    all：再加上公共池里未登记的发现目录条目，用于发现新装未登记的英文 skill。
    """
    pool = Path(config['pool']).expanduser()
    rows = []
    for entry in config['skills']:
        if entry['state'] not in {'active', 'transition'}:
            continue
        source = Path(entry['source']).expanduser()
        skill_md = source / 'SKILL.md'
        if skill_md.is_file():
            rows.append((entry['name'], skill_md, 'managed'))
    if scope == 'all' and pool.is_dir():
        registered = {name for name, _, _ in rows}
        for folder in sorted(pool.iterdir()):
            skill_md = folder / 'SKILL.md'
            if folder.is_dir() and skill_md.is_file() and folder.name not in registered:
                rows.append((folder.name, skill_md, 'unmanaged'))
    return rows


def cn_guard(config, scope='managed', report=None):
    """校验已登记技能的 description 是否仍为中文。

    退出码：0=全部中文；1=有需翻译/缺失项；2=环境异常。
    这里不做任何自动翻译写入——翻译需要 LLM 判断，脚本只负责如实报告。
    """
    print('中文化守护 - 校验技能 description 是否仍为中文')
    print('=' * 72)
    print(f'范围：{scope}（managed=登记表内 active/transition 技能）')
    print('-' * 72)
    targets = cn_targets(config, scope)
    if not targets:
        print('未找到可校验的技能（登记表与公共池均为空？请检查维护源是否完整）。')
        print('=' * 72)
        return 2
    already_cn, needs, missing, unreadable = [], [], [], []
    for name, skill_md, kind in targets:
        try:
            text = skill_md.read_text(encoding='utf-8')
        except OSError as error:
            unreadable.append((name, kind, str(error)))
            continue
        description, _ = read_description(text)
        if description is None:
            missing.append((name, kind, '无 description 字段'))
        elif not description.strip():
            missing.append((name, kind, 'description 为空'))
        elif needs_translation(description):
            needs.append((name, kind, description[:70]))
        else:
            already_cn.append(name)
    print(f'已是中文：{len(already_cn)} 项')
    if needs:
        print(f'\n[需 LLM 翻译] {len(needs)} 项（纯英文，脚本无法自动翻译）：')
        for name, kind, current in needs:
            print(f'   - {name} ({kind}): {current}')
    if missing:
        print(f'\n[缺失描述] {len(missing)} 项：')
        for name, kind, reason in missing:
            print(f'   - {name} ({kind}): {reason}')
    if unreadable:
        print(f'\n[读取失败] {len(unreadable)} 项：')
        for name, kind, reason in unreadable:
            print(f'   - {name} ({kind}): {reason}')
    print('=' * 72)
    result = dict(mode='cn', scope=scope, already_cn=len(already_cn),
                  needs=[name for name, _, _ in needs],
                  missing=[name for name, _, _ in missing],
                  unreadable=[name for name, _, _ in unreadable])
    if report:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    if unreadable:
        print('⚠️ 有技能无法读取，守护结论不可信，请先修复文件权限。')
        return 2
    if needs or missing:
        print('⚠️ 守护未通过：请用 Edit 把上述技能的 description 译为中文，然后重跑本模式。')
        return 1
    print('✅ 守护通过：已登记技能的 description 全部为中文，无被上游覆盖回英文的项。')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['plan', 'apply', 'check', 'cn'])
    parser.add_argument('--config', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--cn-scope', default='managed',
                        choices=['managed', 'all'],
                        help='managed=只查登记表内技能（默认）；all=并查未登记的发现目录条目')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    config = json.loads((args.config or repo/'inventory/skill-policy.json').read_text())
    if args.mode == 'cn':
        return cn_guard(config, scope=args.cn_scope, report=args.report)
    manager = Manager(repo, config, apply=args.mode == 'apply')
    rows = manager.run()
    if args.mode == 'apply':
        final = Manager(repo, config).run()
    else:
        final = rows
    counts = {key: sum(r['status'] == key for r in final) for key in ('OK', 'CHANGE', 'CONFLICT', 'MISSING', 'UNMANAGED', 'SOURCE')}
    result = dict(mode=args.mode, counts=counts, backup=str(manager.backup_root), changes=rows, final=final)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(counts, ensure_ascii=False))
    for row in final:
        if row['status'] in {'CONFLICT', 'MISSING', 'UNMANAGED'}:
            print(f"{row['status']} {row['path']}: {row['detail']}")
    failed = counts['CONFLICT'] or counts['MISSING'] or (args.mode != 'plan' and counts['CHANGE'])
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
