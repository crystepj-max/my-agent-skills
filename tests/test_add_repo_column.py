#!/usr/bin/env python3
"""add_repo_column 的行为约束测试。

核心保护对象：翻译表是多表、列数不一的 Markdown 表格。旧实现按固定
「3 列 → 4 列」重写整行，会把第 4 列之后全部吞进 description 再压掉——
**破坏数据**。这里用真实结构的样本守住该行为。
"""
import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / 'tools' / 'add_repo_column.py'
spec = importlib.util.spec_from_file_location('add_repo_column', TOOL)
add_repo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(add_repo)

# 与真实翻译表一致：7 列（第一方）与 8 列（第三方）并存
SEVEN_COL = ('| # | Skill 名称 | 中文描述 | 参考的 skill | 参考日期 | skill 范围 | 最新更新 |\n'
             '|---|---|---|---|---|---|---|\n'
             '| 1 | `agent-skill-bridge` | 中文描述甲 | find-skills | 2026-10-05 | 用户级 | 平台内置 |\n')

EIGHT_COL = ('| # | Skill 名称 | 中文描述 | 仓库链接 / 来源 | 作者 | 仓库简介 | skill 范围 | 最新更新 |\n'
             '|---|---|---|---|---|---|---|---|\n'
             '| 1 | `ask-matt` | 中文描述乙 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) '
             '| Matt Pocock | 简介 | 用户级 | 2026-10-05 |\n'
             '| 2 | `implement-spec` | 中文描述丙 |  |  |  | 用户级 | 2026-10-05 |\n')


class ProcessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_on(self, text):
        md = self.root / 'skill-desc-translation.md'
        md.write_text(text, encoding='utf-8', newline='\n')
        return add_repo.process(md)

    def test_wide_table_is_not_collapsed_to_four_columns(self):
        """旧实现的致命缺陷：整行重写导致第 4 列之后丢失。"""
        raw, new, _, stats, _ = self.run_on(EIGHT_COL)
        before = [l for l in raw.split('\n') if l.strip().startswith('|')]
        after = [l for l in new.split('\n') if l.strip().startswith('|')]
        self.assertEqual([l.count('|') for l in before], [l.count('|') for l in after])
        # 作者 / 仓库简介等后续列必须仍在
        self.assertIn('Matt Pocock', new)
        self.assertIn('简介', new)

    def test_mixed_width_tables_both_survive(self):
        raw, new, _, _, _ = self.run_on(SEVEN_COL + '\n' + EIGHT_COL)
        self.assertIn('参考的 skill', new)
        self.assertIn('仓库链接 / 来源', new)
        self.assertIn('find-skills', new)
        self.assertIn('Matt Pocock', new)

    def test_blank_source_is_filled(self):
        _, new, changes, stats, _ = self.run_on(EIGHT_COL)
        self.assertEqual(stats['filled'], 1)
        self.assertEqual(changes[0][0], 'implement-spec')
        self.assertIn('mattpocock/skills', new)

    def test_existing_source_is_never_overwritten(self):
        """本脚本的映射表是历史快照，覆盖会抹掉后续人工核实的来源。"""
        row = ('| 1 | `neat-freak` | 中文描述 | [github.com/KKKKhazix/khazix-skills]'
               '(https://github.com/KKKKhazix/khazix-skills) | 数字生命 | 简介 | 用户级 | 2026-10-05 |\n')
        _, new, _, stats, _ = self.run_on(
            '| # | Skill 名称 | 中文描述 | 仓库链接 / 来源 | 作者 | 仓库简介 | skill 范围 | 最新更新 |\n'
            '|---|---|---|---|---|---|---|---|\n' + row)
        self.assertEqual(stats['filled'], 0)
        self.assertEqual(stats['kept'], 1)
        self.assertIn('KKKKhazix', new)

    def test_conflict_is_reported_but_value_kept(self):
        row = ('| 1 | `pr` | 中文描述 | [github.com/mattpocock/skills/tree/main/skills/engineering/pr]'
               '(https://github.com/mattpocock/skills/tree/main/skills/engineering/pr) '
               '| Matt | 简介 | 用户级 | 2026-10-05 |\n')
        _, new, _, stats, conflicts = self.run_on(
            '| # | Skill 名称 | 中文描述 | 仓库链接 / 来源 | 作者 | 仓库简介 | skill 范围 | 最新更新 |\n'
            '|---|---|---|---|---|---|---|---|\n' + row)
        # 同仓库不同子路径不应算冲突
        self.assertEqual(stats['conflict'], 0, conflicts)
        self.assertIn('/tree/main/skills/engineering/pr', new)

    def test_builtin_vs_upstream_is_reported_as_conflict(self):
        row = ('| 1 | `skills-security-check` | 中文描述 | WorkBuddy 内置 / 应用市场（腾讯云鼎实验室） '
               '| 腾讯 | 简介 | 用户级 | 2026-10-05 |\n')
        _, new, _, stats, conflicts = self.run_on(
            '| # | Skill 名称 | 中文描述 | 仓库链接 / 来源 | 作者 | 仓库简介 | skill 范围 | 最新更新 |\n'
            '|---|---|---|---|---|---|---|---|\n' + row)
        self.assertEqual(stats['conflict'], 1)
        self.assertEqual(conflicts[0][0], 'skills-security-check')
        self.assertIn('腾讯云鼎实验室', new, '冲突项须保留现值')

    def test_table_without_target_column_is_untouched(self):
        raw, new, _, stats, _ = self.run_on(SEVEN_COL)
        self.assertEqual(raw, new)
        self.assertEqual(stats['filled'], 0)

    def test_prose_and_blank_lines_survive(self):
        text = '# 标题\n\n> 说明段落。\n\n' + EIGHT_COL + '\n尾部文字。\n'
        _, new, _, _, _ = self.run_on(text)
        for keep in ('# 标题', '> 说明段落。', '尾部文字。'):
            self.assertIn(keep, new)

    def test_default_path_is_repo_relative(self):
        """原实现硬编码 macOS 绝对路径，在本机会写错地方或直接崩。"""
        self.assertTrue(add_repo.DEFAULT_MD.is_file())
        self.assertNotIn('/Users/chris', str(add_repo.DEFAULT_MD))


class NormalizeTests(unittest.TestCase):
    def test_equivalent_forms_match(self):
        pairs = [
            ('[github.com/o/r](https://github.com/o/r)', 'https://github.com/o/r'),
            ('https://www.github.com/o/r/', 'http://github.com/o/r'),
            ('[github.com/o/r](https://github.com/o/r/tree/main/skills/x/y)', 'github.com/o/r'),
            ('WorkBuddy 内置 / 应用市场（腾讯云鼎实验室）', 'WorkBuddy 内置/应用市场'),
        ]
        for left, right in pairs:
            self.assertEqual(add_repo.normalize(left), add_repo.normalize(right), left)


if __name__ == '__main__':
    unittest.main()
