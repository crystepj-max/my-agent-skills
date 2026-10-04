"""假绿灯回归：验证 cn 守护在各种异常下不会误报通过。

旧实现靠 grep 输出文本判断，工具报错时 grep 无匹配 → exit 0「守护通过」。
本测试直接针对退出码，锁死该行为。
"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('manager', REPO / 'scripts/manage-skills.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def skill(path, description, block=False):
    path.mkdir(parents=True)
    if block:
        body = 'description: >\n  ' + description + '\n'
    else:
        body = 'description: ' + json.dumps(description, ensure_ascii=False) + '\n'
    (path / 'SKILL.md').write_text('---\nname: sample\n' + body + '---\n\n正文\n')
    return path


class CnGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.pool = self.home / '.agents/skills'
        self.config = {'pool': str(self.pool), 'agent_roots': [], 'projects': {},
                       'project_entry_roots': [], 'skills': []}

    def register(self, name, folder):
        self.config['skills'].append(
            {'name': name, 'state': 'transition', 'scope': 'global', 'source': str(folder)})

    def test_chinese_description_passes(self):
        folder = skill(self.pool / 'cn-ok', '把 AI 智能做成可组合的编程原语，用于路由与抽取。')
        self.register('cn-ok', folder)
        self.assertEqual(module.cn_guard(self.config), 0)

    def test_english_description_fails(self):
        folder = skill(self.pool / 'en-bad', 'Build AI powered software with composable units of intelligence.')
        self.register('en-bad', folder)
        self.assertEqual(module.cn_guard(self.config), 1)

    def test_block_scalar_english_is_detected(self):
        """块标量必须被折叠读出，否则会误判为「空」而漏报。"""
        folder = skill(self.pool / 'blk-bad', 'Build AI powered software with composable units.', block=True)
        self.register('blk-bad', folder)
        self.assertEqual(module.cn_guard(self.config), 1)

    def test_block_scalar_chinese_passes(self):
        folder = skill(self.pool / 'blk-ok', '把 AI 智能做成可组合的编程原语。', block=True)
        self.register('blk-ok', folder)
        self.assertEqual(module.cn_guard(self.config), 0)

    def test_missing_description_fails(self):
        folder = self.pool / 'no-desc'
        folder.mkdir(parents=True)
        (folder / 'SKILL.md').write_text('---\nname: no-desc\n---\n\n正文\n')
        self.register('no-desc', folder)
        self.assertEqual(module.cn_guard(self.config), 1)

    def test_empty_scope_returns_error_not_pass(self):
        """核心回归：校验范围为空必须报错，不能当成「全部通过」。"""
        self.assertEqual(module.cn_guard(self.config), 2)

    def test_unreadable_skill_returns_error(self):
        """读取失败必须让守护结论不可信（exit 2），不能报通过。"""
        folder = skill(self.pool / 'locked', '把 AI 智能做成可组合的编程原语。')
        self.register('locked', folder)
        (folder / 'SKILL.md').unlink()
        (folder / 'SKILL.md').mkdir()  # 目录占位，read_text 抛 IsADirectoryError
        self.assertEqual(module.cn_guard(self.config), 2)

    def test_retired_entry_not_checked(self):
        """退役条目不在执行目录，不该被校验；范围内仍需至少一个有效技能。"""
        folder = skill(self.pool / 'old', 'Build AI powered software with composable units.')
        self.config['skills'].append(
            {'name': 'old', 'state': 'retired', 'scope': 'global', 'source': str(folder)})
        active = skill(self.pool / 'live', '把 AI 智能做成可组合的编程原语。')
        self.register('live', active)
        # 退役的英文条目若被误纳入校验，这里会返回 1
        self.assertEqual(module.cn_guard(self.config), 0)

    def test_retired_only_scope_is_error(self):
        """全部条目都已退役 → 范围为空，报错而非「通过」。"""
        folder = skill(self.pool / 'old', '把 AI 智能做成可组合的编程原语。')
        self.config['skills'].append(
            {'name': 'old', 'state': 'retired', 'scope': 'global', 'source': str(folder)})
        self.assertEqual(module.cn_guard(self.config), 2)

    def test_cjk_threshold_allows_embedded_english(self):
        """技术类中文描述内嵌成串英文（报错原文/API 名）不应误判为英文。"""
        text = ('排查 ClashX 代理导致 stream closed before response.completed 的问题，'
                '覆盖热重载引发的 DNS 崩溃与节点选择。')
        self.assertFalse(module.needs_translation(text))

    def test_cjk_ratio_and_sentence_detection(self):
        self.assertEqual(module.cjk_ratio('全是中文内容'), 1.0)
        self.assertEqual(module.cjk_ratio(''), 0.0)
        self.assertTrue(module.needs_translation('Build AI powered software with units.'))
        self.assertFalse(module.needs_translation('来源：skills/bottleneck-hunter.md 的说明'))


if __name__ == '__main__':
    unittest.main()
