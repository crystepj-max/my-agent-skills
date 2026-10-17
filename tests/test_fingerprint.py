"""fingerprint 跨平台一致性回归。

背景：曾用 str(relative) 直接进哈希，Windows 得 `agents\\openai.yaml`、
macOS 得 `agents/openai.yaml`，同一份内容两端指纹必然不同，
导致 check 在 Windows 上长期误报。现归一化为 POSIX 形式。
"""
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path, PurePosixPath, PureWindowsPath

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('manager', REPO / 'scripts/manage-skills.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def build(root, files):
    """files: {相对路径(posix): 内容}

    用 write_bytes 显式写入，避免 write_text 在 Windows 上把 \\n 转成 \\r\\n，
    导致期望值与实际字节不一致。
    """
    for rel, text in files.items():
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode('utf-8'))
    return root


class RelativeKeyTests(unittest.TestCase):
    def test_posix_and_windows_parts_produce_same_key(self):
        posix = PurePosixPath('agents/openai.yaml')
        windows = PureWindowsPath('agents\\openai.yaml')
        self.assertEqual(module.relative_key(posix), 'agents/openai.yaml')
        self.assertEqual(module.relative_key(windows), 'agents/openai.yaml')
        self.assertEqual(module.relative_key(posix), module.relative_key(windows))

    def test_nested_and_flat_keys_are_distinct(self):
        self.assertNotEqual(
            module.relative_key(PurePosixPath('a/b/c.md')),
            module.relative_key(PurePosixPath('abc.md')))


class FingerprintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_nested_layout_is_stable_and_platform_independent(self):
        """指纹必须与手写 posix 拼接的结果一致，即不含平台分隔符。"""
        a = build(self.root / 'a', {
            'SKILL.md': '---\nname: x\n---\n',
            'agents/openai.yaml': 'interface: {}\n',
            'references/deep/note.md': 'note\n',
        })
        got = module.fingerprint(a)

        expect = hashlib.sha256()
        for rel, text in sorted({
            'SKILL.md': '---\nname: x\n---\n',
            'agents/openai.yaml': 'interface: {}\n',
            'references/deep/note.md': 'note\n',
        }.items()):
            expect.update(rel.encode() + b'\0' + text.encode() + b'\0')
        self.assertEqual(got, expect.hexdigest())

    def test_same_content_same_fingerprint(self):
        a = build(self.root / 'a', {'SKILL.md': 'x', 'sub/y.md': 'z'})
        b = build(self.root / 'b', {'SKILL.md': 'x', 'sub/y.md': 'z'})
        self.assertEqual(module.fingerprint(a), module.fingerprint(b))

    def test_content_change_is_detected(self):
        a = build(self.root / 'a', {'SKILL.md': 'x', 'sub/y.md': 'z'})
        b = build(self.root / 'b', {'SKILL.md': 'x', 'sub/y.md': 'changed'})
        self.assertNotEqual(module.fingerprint(a), module.fingerprint(b))

    def test_ignored_directories_do_not_count(self):
        base = {'SKILL.md': 'x'}
        a = build(self.root / 'a', base)
        b = build(self.root / 'b', base)
        (b / '.git').mkdir()
        (b / '.git' / 'HEAD').write_bytes(b'ref: refs/heads/main\n')
        (b / 'node_modules').mkdir()
        (b / 'node_modules' / 'pkg.js').write_bytes(b'var a=1;\n')
        self.assertEqual(module.fingerprint(a), module.fingerprint(b))

    def test_file_move_between_directories_changes_fingerprint(self):
        """路径进入哈希：同一内容挪到别的目录应视为不同版本。"""
        a = build(self.root / 'a', {'SKILL.md': 'x'})
        b = build(self.root / 'b', {'nested/SKILL.md': 'x'})
        self.assertNotEqual(module.fingerprint(a), module.fingerprint(b))


if __name__ == '__main__':
    unittest.main()
