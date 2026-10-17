#!/usr/bin/env python3
"""为 inventory/skills/descriptions-zh.md 补齐「仓库链接 / 来源」列，保留中文描述与其余列。

历史：该脚本初版为一次性迁移工具，硬编码 macOS 绝对路径，且按固定「3 列 → 4 列」
重写整行。当前翻译表已演进为多张表、列数不一（第一方 7 列、第三方 8 列），
原实现会把匹配行的第 4 列之后全部吞进 description 再压成 4 列——**破坏数据**。
故改为：按表头实际列名定位/插入目标列，只改这一列，其余列原样保留。

默认 dry-run；--apply 才写盘，并先备份。退出码 0/1/2。
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

DEFAULT_MD = Path(__file__).resolve().parent.parent / 'inventory' / 'skills' / 'descriptions-zh.md'
TARGET_HEADER = '仓库链接 / 来源'

MATT = 'https://github.com/mattpocock/skills'
BAOYU = 'https://github.com/JimLiu/baoyu-skills'
BERK = 'https://github.com/xbtlin/ai-berkshire'
BUNDLE = 'WorkBuddy 内置/应用市场'

MATT_NAMES = {
    'ask-matt', 'code-review', 'codebase-design', 'diagnosing-bugs', 'domain-modeling',
    'grill-me', 'grilling', 'handoff', 'implement', 'improve-codebase-architecture',
    'prototype', 'resolving-merge-conflicts', 'teach', 'to-spec', 'to-tickets', 'triage',
    'tdd', 'wayfinder', 'writing-great-skills', 'grill-with-docs', 'research',
    'setup-matt-pocock-skills', 'pr', 'retro', 'implement-spec', 'wait-what', 'wizard',
    'to-questionnaire',
}
BAOYU_NAMES = {'baoyu-comic', 'baoyu-image-gen', 'baoyu-infographic', 'baoyu-slide-deck'}
BERK_NAMES = {
    'bottleneck-hunter', 'deep-company-series', 'dyp-ask', 'earnings-review', 'earnings-team',
    'financial-data', 'income-investment', 'industry-funnel', 'industry-research',
    'investment-checklist', 'investment-memo-craft', 'investment-research', 'investment-team',
    'management-deep-dive', 'portfolio-review', 'private-company-research', 'quality-screen',
    'thesis-drift', 'thesis-tracker', 'wechat-article', 'news-pulse',
}
EXPLICIT = {
    'agnes-ai-generation-skill': 'https://github.com/Yacey/agnes-ai-generation-skill',
    'beautiful-html-templates': 'https://github.com/zarazhangrui/beautiful-html-templates',
    'eli5': 'https://github.com/Companion-Inc/feynman',
    'frontend-slides': 'https://github.com/zarazhangrui/frontend-slides',
    'guizang-ppt-skill': 'https://github.com/op7418/guizang-ppt-skill',
    'humanize-ppt': 'https://github.com/LearnPrompt/humanize-ppt',
    'llm-wiki': 'https://github.com/nashsu/llm_wiki_skill',
    'llm-wiki-app': 'https://github.com/nashsu/llm_wiki_skill',
    'neat-freak': 'https://github.com/KKKKhazix/khazix-skills',
    'hatch-pet': 'https://github.com/openai/skills',
    'skills-security-check': 'https://github.com/TencentCloudADP/agent-skills-security',
    'storage-analyzer': 'https://github.com/KKKKhazix/khazix-skills',
    'remotion-video-production': 'https://github.com/akillness/jeo-skills',
    'remotion-video-toolkit': 'https://github.com/shreefentsar/remotion-video-toolkit',
    'typesafe-ai': 'https://github.com/typesafe-ai/skills',
    'video-production': 'https://github.com/jmagly/aiwg',
    'ppt-master': 'https://github.com/hugohe3/ppt-master',
    'skill-creator': 'https://github.com/anthropics/skills',
    'frontend-design': 'https://github.com/anthropics/skills',
    'writing-great-skills': 'https://github.com/sickn33/agentic-awesome-skills',
}
# 体积大或含二进制资产：建议用仓库链接安装，未打包进安装脚本
HEAVY = {'beautiful-html-templates', 'guizang-ppt-skill', 'humanize-ppt', 'ppt-master',
         'baoyu-slide-deck'}

NAME_RE = re.compile(r'`([^`]+)`')


def source_for(name):
    if name in EXPLICIT:
        return EXPLICIT[name]
    if name in MATT_NAMES:
        return MATT
    if name in BAOYU_NAMES:
        return BAOYU
    if name in BERK_NAMES:
        return BERK
    return BUNDLE


def fmt(url, name):
    if not url.startswith('http'):
        return url
    if name in HEAVY:
        url += '（体积大，建议用仓库链接安装，未打包进脚本）'
    found = re.match(r'https?://(github\.com/[^/]+/[^/]+)', url)
    label = found.group(1) if found else url
    return f'[{label}]({url})'


def split_row(line):
    """拆表格行。返回 None 表示不是数据行。"""
    stripped = line.strip()
    if not (stripped.startswith('|') and stripped.endswith('|')):
        return None
    return [cell.strip() for cell in stripped[1:-1].split('|')]


def is_data_row(cells):
    return bool(cells) and cells[0].isdigit() and len(cells) > 2


def normalize(value):
    """比较来源时忽略 markdown 链接语法、提示后缀与常见写法差异。

    表格里同一仓库可能写成 `[github.com/o/r](https://github.com/o/r)`、
    `WorkBuddy 内置 / 应用市场（腾讯云鼎实验室）` 等形式，只要仓库一致就不该报冲突。
    """
    text = value.strip().lower()
    # 去掉 markdown 链接的显示文本，只留 URL
    found = re.search(r'\((https?://[^)]+)\)', text)
    if found:
        text = found.group(1)
    # 去掉「（…）」提示后缀与首尾空格
    text = re.sub(r'[（(][^）)]*[）)]', '', text)
    text = text.replace(' ', '').replace('，', ',')
    for prefix in ('https://', 'http://', 'www.'):
        if text.startswith(prefix):
            text = text[len(prefix):]
    # 去掉 /tree/main/<分类>/<skill> 这类子路径：同仓库不同层级仍算同一来源
    text = re.sub(r'/tree/[^/]+/.*$', '', text)
    return text.rstrip('/').replace('workbuddy内置/应用市场', 'workbuddy内置')


def process(md_path):
    raw = md_path.read_text(encoding='utf-8')
    lines = raw.split('\n')
    out = list(lines)
    changes = []
    conflicts = []
    index = 0
    stats = {'filled': 0, 'kept': 0, 'conflict': 0, 'untouched': 0}

    while index < len(lines):
        cells = split_row(lines[index])
        if not cells or TARGET_HEADER not in cells:
            index += 1
            continue

        target = cells.index(TARGET_HEADER)
        header_span = len(cells)
        # 分隔行与表头列数一致，按它确认边界更稳
        sep = split_row(lines[index + 1]) if index + 1 < len(lines) else None
        if sep and all(set(c) <= set('-: ') and c for c in sep):
            header_span = len(sep)
        index += 2

        while index < len(lines):
            row = split_row(lines[index])
            if not row or not is_data_row(row):
                break
            found = NAME_RE.search(row[1])
            if not found:
                index += 1
                continue
            name = found.group(1)
            if len(row) < header_span:
                # 列数不足：补齐到表头宽度（不丢已有内容）
                row = row + [''] * (header_span - len(row))
            if len(row) > header_span:
                # 比表头宽：不动，避免误判
                stats['untouched'] += 1
                index += 1
                continue

            desired = fmt(source_for(name), name)
            current = row[target].strip()
            if not current:
                row[target] = desired
                out[index] = '| ' + ' | '.join(row) + ' |'
                stats['filled'] += 1
                changes.append((name, '补齐来源', '(空)', desired))
            else:
                # 已有值一律保留。脚本内的映射表是历史快照、不完整，
                # 覆盖会抹掉后续人工核实的来源（neat-freak 的 khazix、
                # pr/retro 的 mattpocock、eli5 的 Companion-Inc 等）。
                # 与映射不一致时只提示冲突，交人工判断，不自动改写。
                stats['kept'] += 1
                if normalize(current) != normalize(desired):
                    stats['conflict'] += 1
                    conflicts.append((name, current, desired))
            index += 1

    return raw, '\n'.join(out), changes, stats, conflicts


def main():
    parser = argparse.ArgumentParser(description='补齐翻译表的「仓库链接 / 来源」列')
    parser.add_argument('md', nargs='?', default=str(DEFAULT_MD),
                        help=f'翻译表路径（默认 {DEFAULT_MD}）')
    parser.add_argument('--apply', action='store_true', help='写盘；缺省仅 dry-run 报告')
    args = parser.parse_args()

    md = Path(args.md).expanduser()
    if not md.is_file():
        print(f'找不到文件：{md}', file=sys.stderr)
        return 2

    raw, new, changes, stats, conflicts = process(md)
    print(f'翻译表：{md}')
    print('=' * 78)
    for name, kind, old, desired in changes:
        print(f'  [{kind}] {name}\n      现: {old}\n      拟: {desired}')
    print('=' * 78)
    print(f'补齐 {stats["filled"]} 行，保留已有 {stats["kept"]} 行，'
          f'列数异常跳过 {stats["untouched"]} 行')

    if conflicts:
        print()
        print(f'⚠ 以下 {len(conflicts)} 行的现有来源与本脚本映射不一致，**已保留现值**，'
              '需人工确认：')
        for name, current, desired in conflicts:
            print(f'  {name:34s} 现: {current[:44]}')
            print(f'  {"":34s} 映: {desired[:44]}')

    if raw == new:
        print('内容无需变更（未写盘）')
        return 0

    if not args.apply:
        print('dry-run：未写盘。加 --apply 执行。')
        return 0

    backup = md.with_suffix(md.suffix + '.bak')
    shutil.copy(md, backup)
    # newline='\n'：Windows 下文本模式默认会把 \n 转成 \r\n，产生整文件行尾 diff
    with open(md, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(new)
    print(f'\n已写盘，备份：{backup}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
