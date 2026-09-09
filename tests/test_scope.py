import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('manager', Path(__file__).resolve().parents[1]/'scripts/manage-skills.py')
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
        (self.alias/'sample').symlink_to(old)
        self.config['skills']=[dict(name='sample', source='my-skills/sample', state='active', scope='global', accepted_fingerprints=[module.fingerprint(old)])]
        self.run_manager(True)
        self.assertEqual((self.alias/'sample/SKILL.md').read_text(),(source/'SKILL.md').read_text())
        (source/'helper.py').write_text('new helper')
        self.assertEqual((self.alias/'sample/helper.py').read_text(),'new helper')
        self.assertFalse(any(r['status']=='CHANGE' for r in self.run_manager()))
        self.assertTrue(list((self.home/'.local/share/agent-skills/backups').rglob('helper.py')))

    def test_reference_and_backup_leave_discovery_and_do_not_return(self):
        old=self.skill(self.pool/'sample')
        (self.alias/'sample').symlink_to(old)
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


if __name__=='__main__':
    unittest.main()
