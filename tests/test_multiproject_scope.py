import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('manager', ROOT / 'scripts/manage-skills.py')
manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manager)


class MultiProjectScopeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name).resolve()
        self.repo = self.home / 'repo'
        self.repo.mkdir()
        self.projects = {
            'gawain': self.home / 'Gawain',
            'autotest': self.home / 'AUTOTEST',
        }
        for path in self.projects.values():
            path.mkdir()
        self.config = {
            'pool': '~/.agents/skills',
            'agent_roots': ['~/.codex/skills'],
            'projects': {key: str(value) for key, value in self.projects.items()},
            'project_entry_roots': ['.agents/skills', '.claude/skills'],
            'skills': [],
            'reference_copies': [],
        }

    def skill(self, path, marker, description='用于生成和检查中文报告。'):
        path.mkdir(parents=True)
        (path / 'SKILL.md').write_text(
            '---\nname: test-report-html\ndescription: ' + description + '\n---\n\n步骤\n'
        )
        (path / 'module-marker.txt').write_text(marker + '\n')
        return path

    def entry(self):
        return {
            'name': 'test-report-html',
            'state': 'active',
            'scope': 'gawain',
            'source': 'project:gawain/skills/test-report-html',
            'project_sources': {
                'gawain': 'project:gawain/skills/test-report-html',
                'autotest': 'project:autotest/skills/test-report-html',
            },
            'accepted_fingerprints': [],
        }

    def source_paths(self):
        return {
            key: root / 'skills' / 'test-report-html'
            for key, root in self.projects.items()
        }

    def run_manager(self, apply=False):
        instance = manager.Manager(self.repo, self.config, apply=apply, user_home=self.home)
        paths = [instance.repo, instance.pool, *instance.alias_roots,
                 instance.backup_root, *(instance.expand(p) for p in self.config['projects'].values())]
        for path in paths:
            self.assertTrue(path.resolve(strict=False).is_relative_to(self.home), path)
        return instance.run()

    def test_two_projects_get_distinct_complete_sources_without_global_alias(self):
        sources = self.source_paths()
        self.skill(sources['gawain'], 'gawain bundle')
        self.skill(sources['autotest'], 'autotest bundle')
        self.config['skills'] = [self.entry()]

        rows = self.run_manager(apply=True)

        for project, source in sources.items():
            for entry_root in self.config['project_entry_roots']:
                alias = self.projects[project] / entry_root / 'test-report-html'
                self.assertTrue(alias.is_symlink(), alias)
                self.assertEqual(alias.resolve(), source.resolve())
                self.assertEqual((alias / 'module-marker.txt').read_text(), f'{project} bundle\n')
        self.assertFalse((self.home / '.agents/skills/test-report-html').exists())
        self.assertFalse((self.home / '.codex/skills/test-report-html').exists())
        self.assertFalse(any(row['status'] == 'MISSING' for row in rows))

        repeated = self.run_manager()
        self.assertFalse(any(row['status'] == 'CHANGE' for row in repeated))

    def test_missing_second_project_source_is_reported_and_neither_alias_is_created(self):
        sources = self.source_paths()
        self.skill(sources['gawain'], 'gawain bundle')
        self.config['skills'] = [self.entry()]

        rows = self.run_manager(apply=True)

        missing = [row for row in rows if row['status'] == 'MISSING']
        self.assertEqual(len(missing), 1)
        self.assertEqual(Path(missing[0]['path']), sources['autotest'])
        for project in self.projects.values():
            for entry_root in self.config['project_entry_roots']:
                self.assertFalse((project / entry_root / 'test-report-html').exists())
        self.assertFalse((self.home / '.agents/skills/test-report-html').exists())

    def test_unknown_project_and_primary_source_mismatch_reject_before_writes(self):
        entry = self.entry()
        entry['project_sources']['unknown'] = 'project:unknown/skills/test-report-html'
        self.config['skills'] = [entry]
        with self.assertRaises(ValueError):
            self.run_manager(apply=True)
        self.assertFalse((self.home / '.agents/skills').exists())
        self.assertFalse((self.home / '.codex/skills').exists())
        for project in self.projects.values():
            self.assertFalse((project / '.agents/skills').exists())

        entry = self.entry()
        entry['project_sources'].pop('gawain')
        self.config['skills'] = [entry]
        with self.assertRaises(ValueError):
            self.run_manager(apply=True)
        self.assertFalse((self.home / '.agents/skills').exists())

        entry = self.entry()
        entry['source'] = 'project:gawain/skills/other'
        self.config['skills'] = [entry]
        with self.assertRaises(ValueError):
            self.run_manager(apply=True)
        self.assertFalse((self.home / '.agents/skills').exists())
        for project in self.projects.values():
            self.assertFalse((project / '.agents/skills').exists())

        entry = self.entry()
        entry['scope'] = 'global'
        self.config['skills'] = [entry]
        with self.assertRaises(ValueError):
            self.run_manager(apply=True)
        self.assertFalse((self.home / '.agents/skills').exists())
        for project in self.projects.values():
            self.assertFalse((project / '.agents/skills').exists())

    def test_parent_traversal_project_source_is_rejected_before_writes(self):
        self.skill(self.source_paths()['gawain'], 'gawain bundle')
        escaped = self.home / 'outside' / 'test-report-html'
        self.skill(escaped, 'escaped autotest bundle')
        self.projects['autotest'] = self.home / 'AUTOTEST' / 'nested'
        self.projects['autotest'].mkdir(parents=True)
        entry = self.entry()
        entry['project_sources']['autotest'] = 'project:autotest/../../outside/test-report-html'
        self.config['projects']['autotest'] = str(self.projects['autotest'])
        self.config['skills'] = [entry]

        rejected = False
        try:
            self.run_manager(apply=True)
        except ValueError:
            rejected = True
        escaped_alias = self.projects['autotest'] / '.agents/skills/test-report-html'
        resolved_alias = escaped_alias.resolve() if escaped_alias.is_symlink() else None
        self.assertTrue(rejected, f'escaped path was accepted; resulting alias resolved to {resolved_alias}')
        self.assertFalse(escaped_alias.exists())
        self.assertFalse((self.home / '.agents/skills/test-report-html').exists())

    def test_project_local_symlink_to_external_source_is_rejected_before_writes(self):
        self.skill(self.source_paths()['gawain'], 'gawain bundle')
        escaped = self.home / 'outside' / 'test-report-html'
        self.skill(escaped, 'escaped autotest bundle')
        self.projects['autotest'] = self.home / 'AUTOTEST'
        self.config['projects']['autotest'] = str(self.projects['autotest'])
        linked_source = self.projects['autotest'] / 'skills/test-report-html'
        linked_source.parent.mkdir(parents=True, exist_ok=True)
        linked_source.symlink_to(escaped, target_is_directory=True)
        entry = self.entry()
        self.config['skills'] = [entry]
        rejected = False
        try:
            self.run_manager(apply=True)
        except ValueError:
            rejected = True
        linked_alias = self.projects['autotest'] / '.agents/skills/test-report-html'
        resolved_alias = linked_alias.resolve() if linked_alias.is_symlink() else None
        self.assertTrue(rejected, f'symlink source was accepted; resulting alias resolved to {resolved_alias}')
        self.assertFalse(linked_alias.exists())
        self.assertTrue(linked_source.is_symlink())
        self.assertEqual((escaped / 'module-marker.txt').read_text(), 'escaped autotest bundle\n')

    def test_source_that_is_itself_a_project_entry_is_left_in_place(self):
        source = self.projects['gawain'] / '.agents/skills/test-report-html'
        self.skill(source, 'gawain in-place bundle')
        other_source = self.source_paths()['autotest']
        self.skill(other_source, 'autotest bundle')
        entry = self.entry()
        entry['source'] = 'project:gawain/.agents/skills/test-report-html'
        entry['project_sources']['gawain'] = entry['source']
        self.config['skills'] = [entry]

        rows = self.run_manager(apply=True)

        self.assertTrue(source.is_dir())
        self.assertFalse(source.is_symlink())
        self.assertEqual((source / 'module-marker.txt').read_text(), 'gawain in-place bundle\n')
        self.assertTrue((self.projects['gawain'] / '.claude/skills/test-report-html').is_symlink())
        self.assertEqual(
            (self.projects['gawain'] / '.claude/skills/test-report-html').resolve(),
            source.resolve(),
        )
        self.assertFalse((self.home / '.agents/skills/test-report-html').exists())
        self.assertTrue(any(row['status'] == 'OK' and Path(row['path']) == source for row in rows))

    def test_legacy_project_reference_helper_without_scope_remains_supported(self):
        source = self.skill(self.source_paths()['gawain'], 'legacy reference bundle')
        self.config['skills'] = [{
            'name': 'sample',
            'source': 'project:gawain/skills/test-report-html',
        }]

        instance = manager.Manager(self.repo, self.config, user_home=self.home)

        self.assertEqual(instance.config['skills'][0]['source'], 'project:gawain/skills/test-report-html')
        self.assertTrue(source.is_dir())

    def test_reference_copy_target_inside_secondary_maintenance_source_is_refused(self):
        sources = self.source_paths()
        self.skill(sources['gawain'], 'gawain bundle')
        self.skill(sources['autotest'], 'autotest bundle')
        reference = self.skill(self.repo / 'preserved' / 'reference', 'reference bundle')
        destination = sources['autotest'] / 'references' / 'old'
        self.config['skills'] = [self.entry()]
        self.config['reference_copies'] = [{
            'name': 'old',
            'source': str(reference),
            'destination': str(destination),
            'fingerprint': manager.fingerprint(reference),
        }]

        rows = self.run_manager(apply=True)

        self.assertTrue(any(
            row['status'] == 'CONFLICT' and Path(row['path']) == destination
            for row in rows
        ))
        self.assertFalse(destination.exists())

    def test_unreviewed_local_project_entry_is_preserved(self):
        sources = self.source_paths()
        self.skill(sources['gawain'], 'gawain bundle')
        self.skill(sources['autotest'], 'autotest bundle')
        local = self.projects['autotest'] / '.agents/skills/test-report-html'
        local.mkdir(parents=True)
        (local / 'SKILL.md').write_text('local reviewed-later version\n')
        (local / 'private-note.txt').write_text('keep this local change\n')
        self.config['skills'] = [self.entry()]

        rows = self.run_manager(apply=True)

        self.assertTrue(any(row['status'] == 'CONFLICT' and Path(row['path']) == local for row in rows))
        self.assertFalse(local.is_symlink())
        self.assertEqual((local / 'private-note.txt').read_text(), 'keep this local change\n')
        self.assertEqual((local / 'SKILL.md').read_text(), 'local reviewed-later version\n')

    def test_chinese_guard_checks_both_project_skill_files(self):
        sources = self.source_paths()
        self.skill(sources['gawain'], 'gawain bundle', '用于生成中文测试报告。')
        self.skill(
            sources['autotest'], 'autotest bundle',
            'Build reliable HTML reports with charts and test summaries.'
        )
        self.config['skills'] = [self.entry()]

        targets = manager.cn_targets(self.config, 'managed')
        self.assertEqual({path.resolve() for _, path, _ in targets}, {
            (sources['gawain'] / 'SKILL.md').resolve(),
            (sources['autotest'] / 'SKILL.md').resolve(),
        })
        output = io.StringIO()
        with redirect_stdout(output):
            result = manager.cn_guard(self.config)
        self.assertEqual(result, 1)
        self.assertIn('[需 LLM 翻译] 1 项', output.getvalue())


if __name__ == '__main__':
    unittest.main()
