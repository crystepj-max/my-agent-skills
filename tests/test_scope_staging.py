import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

TEST_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_CANDIDATES = (TEST_ROOT/'scripts/manage-skills.py', TEST_ROOT/'tool-patch/manage-skills.py')
MANAGER_PATH = next(path for path in SCRIPT_CANDIDATES if path.is_file())
spec = importlib.util.spec_from_file_location('manager', MANAGER_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ScopeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.repo = self.home/'repo'
        self.pool = self.home/'.agents/skills'
        self.alias = self.home/'.codex/skills'
        self.alias.mkdir(parents=True)
        self.config = dict(pool='~/.agents/skills', agent_roots=['~/.codex/skills'], projects={'ppt':'~/vault'}, project_entry_roots=['.agents/skills'], skills=[])
        (self.home/'vault').mkdir()

    def skill(self, path, body='old'):
        path.mkdir(parents=True)
        (path/'SKILL.md').write_text('---\nname: sample\n---\n'+body)
        (path/'helper.py').write_text('old helper')
        return path

    def run_manager(self, apply=False):
        return module.Manager(self.repo, self.config, apply, self.home).run()

    def test_firstparty_updates_all_files_and_repeat_has_no_changes(self):
        source = self.skill(self.repo/'my-skills/sample', 'new')
        old = self.skill(self.pool/'sample')
        module.make_link(self.alias/'sample', old)
        self.config['skills']=[dict(name='sample', source='my-skills/sample', state='active', scope='global', accepted_fingerprints=[module.fingerprint(old)])]
        self.run_manager(True)
        self.assertEqual((self.alias/'sample/SKILL.md').read_text(),(source/'SKILL.md').read_text())
        (source/'helper.py').write_text('new helper')
        self.assertEqual((self.alias/'sample/helper.py').read_text(),'new helper')
        self.assertFalse(any(r['status']=='CHANGE' for r in self.run_manager()))
        self.assertTrue(list((self.home/'.local/share/agent-skills/backups').rglob('helper.py')))

    def test_reference_and_backup_leave_discovery_and_do_not_return(self):
        old=self.skill(self.pool/'sample')
        module.make_link(self.alias/'sample', old)
        self.config['skills']=[dict(name='sample',source='~/.local/share/refs/sample',state='reference',scope='global',migrate=True,accepted_fingerprints=[module.fingerprint(old)])]
        self.run_manager(True)
        self.assertFalse((self.pool/'sample').exists())
        self.assertFalse((self.alias/'sample').is_symlink())
        self.assertTrue((self.home/'.local/share/refs/sample/helper.py').exists())
        self.assertFalse(any(r['status']=='CHANGE' for r in self.run_manager()))

    def test_unreviewed_local_changes_are_preserved(self):
        self.skill(self.repo/'my-skills/sample','new')
        old=self.skill(self.pool/'sample')
        self.config['skills']=[dict(name='sample',source='my-skills/sample',state='active',scope='global',accepted_fingerprints=[module.fingerprint(old)])]
        (old/'helper.py').write_text('unreviewed user change')
        rows=self.run_manager(True)
        self.assertTrue(any(r['status']=='CONFLICT' for r in rows))
        self.assertEqual((old/'helper.py').read_text(),'unreviewed user change')

    def test_project_reference_is_not_a_global_or_project_executable(self):
        old=self.skill(self.pool/'sample')
        self.config['skills']=[dict(name='sample',source='project:ppt/.agent-assets/sample',state='reference',scope='ppt',migrate=True,accepted_fingerprints=[module.fingerprint(old)])]
        self.run_manager(True)
        self.assertTrue((self.home/'vault/.agent-assets/sample/helper.py').exists())
        self.assertFalse((self.pool/'sample').exists())
        self.assertFalse((self.home/'vault/.agents/skills/sample').exists())

    def test_same_frontmatter_name_is_reported_even_with_backup_directory_name(self):
        self.skill(self.pool/'sample')
        self.skill(self.pool/'sample.bak-2020')
        self.assertTrue(any(r['status']=='CONFLICT' for r in self.run_manager()))

    def test_reference_copy_cannot_be_restored_into_a_discovery_root(self):
        source=self.skill(self.repo/'preserved/sample')
        self.config['reference_copies']=[dict(
            name='sample', source='preserved/sample', destination=str(self.pool/'sample'),
            fingerprint=module.fingerprint(source))]
        rows=self.run_manager(True)
        self.assertTrue(any(r['status']=='CONFLICT' and r['path']==str(self.pool/'sample') for r in rows))
        self.assertFalse((self.pool/'sample').exists())

    def test_project_execution_roots_and_their_ancestors_reject_reference_copies(self):
        source = self.skill(self.repo/'preserved/sample')
        self.config['projects'] = {'ppt': '~/vault', 'gawain': '~/gawain'}
        self.config['project_entry_roots'] = ['.agents/skills', '.claude/skills']
        destinations = [
            self.home/'vault/.agents/skills/sample',
            self.home/'vault/.claude/skills/sample',
            self.home/'gawain/.agents/skills/sample',
            self.home/'gawain/.claude/skills/sample',
            self.home/'vault/.agents',
        ]
        for destination in destinations:
            with self.subTest(destination=destination):
                self.config['reference_copies'] = [dict(
                    name='sample', source='preserved/sample', destination=str(destination),
                    fingerprint=module.fingerprint(source))]
                rows = self.run_manager(True)
                self.assertTrue(any(
                    row['status'] == 'CONFLICT' and row['path'] == str(destination)
                    for row in rows
                ))
                self.assertFalse(destination.exists())

    def test_project_execution_root_symlink_rejects_reference_copy(self):
        source = self.skill(self.repo/'preserved/sample')
        project_entry = self.home/'vault/.agents/skills'
        project_entry.mkdir(parents=True)
        alias = self.home/'entry-alias'
        alias.symlink_to(project_entry, target_is_directory=True)
        destination = alias/'sample'
        self.config['reference_copies'] = [dict(
            name='sample', source='preserved/sample', destination=str(destination),
            fingerprint=module.fingerprint(source))]

        rows = self.run_manager(True)

        self.assertTrue(any(
            row['status'] == 'CONFLICT' and row['path'] == str(destination)
            for row in rows
        ))
        self.assertFalse(destination.exists())
        self.assertFalse((project_entry/'sample').exists())

    def test_active_project_maintenance_source_is_protected_and_assets_remain_restorable(self):
        project_source = self.skill(self.home/'gawain/skills/regression')
        reference_source = self.skill(self.repo/'preserved/reference')
        self.config['projects'] = {'gawain': '~/gawain'}
        self.config['project_entry_roots'] = ['.agents/skills']
        self.config['skills'] = [dict(
            name='regression', source='project:gawain/skills/regression',
            state='active', scope='gawain', accepted_fingerprints=[])]
        for state in ('active', 'transition'):
            with self.subTest(state=state):
                self.config['skills'][0]['state'] = state
                nested_reference = project_source/f'reference-copy-{state}'
                self.config['reference_copies'] = [dict(
                    name='reference', source='preserved/reference',
                    destination=str(nested_reference),
                    fingerprint=module.fingerprint(reference_source))]
                rows = self.run_manager(True)
                self.assertTrue(any(
                    row['status'] == 'CONFLICT' and row['path'] == str(nested_reference)
                    for row in rows
                ))
                self.assertFalse(nested_reference.exists())

        assets_reference = self.home/'gawain/.agent-assets/references/reference'
        self.config['reference_copies'][0]['destination'] = str(assets_reference)
        rows = self.run_manager(True)
        self.assertTrue(assets_reference.is_dir())
        self.assertEqual(
            (assets_reference/'SKILL.md').read_text(),
            (reference_source/'SKILL.md').read_text(),
        )
        self.assertFalse(any(
            row['status'] == 'CONFLICT' and row['path'] == str(assets_reference)
            for row in rows
        ))

    def test_reference_and_retired_project_sources_are_not_execution_roots(self):
        original = self.skill(self.repo/'preserved/original')
        self.config['projects'] = {'ppt': '~/vault'}
        self.config['project_entry_roots'] = ['.agents/skills']

        for state in ('reference', 'retired'):
            with self.subTest(state=state):
                destination = self.home/f'vault/.agent-assets/{state}/sample'
                self.config['skills'] = [dict(
                    name='sample', source=str(destination), state=state, scope='ppt')]
                self.config['reference_copies'] = [dict(
                    name='sample', source='preserved/original',
                    destination=str(destination), fingerprint=module.fingerprint(original))]

                rows = self.run_manager(True)

                self.assertTrue(destination.is_dir())
                self.assertEqual(
                    (destination/'SKILL.md').read_text(),
                    (original/'SKILL.md').read_text(),
                )
                self.assertFalse(any(
                    row['status'] == 'CONFLICT' and row['path'] == str(destination)
                    for row in rows
                ))

    def test_reference_and_retired_skill_rows_cannot_migrate_into_project_execution_roots(self):
        self.config['projects'] = {'ppt': '~/vault'}
        self.config['project_entry_roots'] = ['.agents/skills']

        for state in ('reference', 'retired'):
            with self.subTest(state=state):
                name = f'sample-{state}'
                original = self.skill(self.pool/name)
                destination = self.home/f'vault/.agents/skills/{name}'
                self.config['skills'] = [dict(
                    name=name,
                    source=f'project:ppt/.agents/skills/{name}',
                    state=state,
                    scope='ppt',
                    origin='third-party',
                    migrate=True,
                    accepted_fingerprints=[module.fingerprint(original)],
                )]

                rows = self.run_manager(True)

                self.assertTrue(any(
                    row['status'] == 'CONFLICT' and row['path'] == str(destination.resolve())
                    for row in rows
                ))
                self.assertTrue(original.is_dir())
                self.assertEqual((original/'SKILL.md').read_text(), '---\nname: sample\n---\nold')
                self.assertFalse(destination.exists())


if __name__=='__main__':
    unittest.main()
