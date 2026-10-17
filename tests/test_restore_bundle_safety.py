import json
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

TEST_ROOT = Path(__file__).resolve().parents[1]
MANAGER_ROOTS = (TEST_ROOT / "scripts", TEST_ROOT / "tool-patch")
RESTORE_ROOTS = (TEST_ROOT / "scripts", TEST_ROOT / "tool-patch")
RESTORE_SCRIPT = next(root / "restore-bundle.py" for root in RESTORE_ROOTS if (root / "restore-bundle.py").is_file())
WRAPPER_ROOTS = (TEST_ROOT / "tools", TEST_ROOT / "tool-patch")
WRAPPER_SCRIPT = next(
    path for root in WRAPPER_ROOTS
    for path in (root / "restore-bundle.py", root / "restore-bundle-wrapper.py")
    if path.is_file() and path != RESTORE_SCRIPT
)
MANAGER_SCRIPT = next(root / "manage-skills.py" for root in MANAGER_ROOTS if (root / "manage-skills.py").is_file())


def install_fixture_scripts(repo: Path) -> None:
    (repo / "scripts").mkdir(parents=True, exist_ok=True)
    (repo / "inventory").mkdir(exist_ok=True)
    (repo / "tools").mkdir(exist_ok=True)
    shutil.copy2(MANAGER_SCRIPT, repo / "scripts" / "manage-skills.py")
    shutil.copy2(RESTORE_SCRIPT, repo / "scripts" / "restore-bundle.py")
    shutil.copy2(WRAPPER_SCRIPT, repo / "tools" / "restore-bundle.py")


class RestoreBundleSafetyTests(unittest.TestCase):
    def test_legacy_name_restores_only_to_reference_mapping_not_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            install_fixture_scripts(repo)

            maintained = repo / "my-skills" / "skill-workbench"
            maintained.mkdir(parents=True)
            (maintained / "SKILL.md").write_text("first-party maintained source\n")
            policy = {
                "pool": str(Path(tmp) / ".agents" / "skills"),
                "agent_roots": [str(Path(tmp) / ".codex" / "skills")],
                "projects": {},
                "project_entry_roots": [],
                "skills": [
                    {
                        "name": "skill-workbench",
                        "state": "active",
                        "scope": "global",
                        "source": str(maintained),
                        "origin": "first-party",
                    },
                    {
                        "name": "skill-creator",
                        "state": "reference",
                        "scope": "global",
                        "source": str(Path(tmp) / "share" / "references" / "skill-creator"),
                        "origin": "third-party",
                        "replacement": "skill-workbench",
                    },
                ],
                "reference_copies": [{
                    "name": "skill-creator",
                    "maps_to": "skill-workbench",
                    "source": str(Path(tmp) / "upstream-original" / "skill-creator"),
                    "destination": str(Path(tmp) / "share" / "references" / "skill-creator"),
                    "fingerprint": "old-original-fingerprint",
                }],
            }
            (repo / "inventory" / "skill-policy.json").write_text(json.dumps(policy))

            with tarfile.open(repo / "tools" / "skills-bundle.tar.gz", "w:gz") as archive:
                for prefix in ("skills", "references"):
                    info = tarfile.TarInfo(f"{prefix}/skill-creator/SKILL.md")
                    data = b"old upstream skill-creator original\n"
                    info.size = len(data)
                    import io
                    archive.addfile(info, io.BytesIO(data))

            result = subprocess.run(
                ["python3", str(repo / "scripts" / "restore-bundle.py")],
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertIn("references/skill-creator", result.stdout)
            self.assertEqual((maintained / "SKILL.md").read_text(), "first-party maintained source\n")
            self.assertFalse((Path(tmp) / ".agents" / "skills" / "skill-workbench").exists())
            self.assertFalse((Path(tmp) / ".agents" / "skills" / "skill-creator").exists())
            self.assertEqual(
                (Path(tmp) / "share" / "references" / "skill-creator" / "SKILL.md").read_text(),
                "old upstream skill-creator original\n",
            )
            self.assertFalse((Path(tmp) / ".agents" / "skills" / "skill-creator").exists())

            shutil.rmtree(Path(tmp) / "share" / "references" / "skill-creator")
            wrapper_result = subprocess.run(
                ["python3", str(repo / "tools" / "restore-bundle.py")],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("share/references/skill-creator", wrapper_result.stdout)
            self.assertEqual(
                (Path(tmp) / "share" / "references" / "skill-creator" / "SKILL.md").read_text(),
                "old upstream skill-creator original\n",
            )
            self.assertEqual((maintained / "SKILL.md").read_text(), "first-party maintained source\n")
            self.assertFalse((Path(tmp) / ".agents" / "skills" / "skill-creator").exists())

    def test_third_party_reference_target_inside_discovery_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            install_fixture_scripts(repo)
            pool = Path(tmp) / ".agents" / "skills"
            policy = {
                "pool": str(pool),
                "agent_roots": [str(Path(tmp) / ".codex" / "skills")],
                "projects": {},
                "project_entry_roots": [],
                "skills": [{
                    "name": "old-third-party",
                    "state": "reference",
                    "scope": "global",
                    "source": str(pool / "old-third-party"),
                    "origin": "third-party",
                }],
                "reference_copies": [],
            }
            (repo / "inventory" / "skill-policy.json").write_text(json.dumps(policy))
            with tarfile.open(repo / "tools" / "skills-bundle.tar.gz", "w:gz") as archive:
                info = tarfile.TarInfo("skills/old-third-party/SKILL.md")
                data = b"old third-party original\n"
                info.size = len(data)
                import io
                archive.addfile(info, io.BytesIO(data))

            for script in (repo / "scripts" / "restore-bundle.py", repo / "tools" / "restore-bundle.py"):
                with self.subTest(script=script):
                    result = subprocess.run(
                        ["python3", str(script)],
                        capture_output=True,
                        text=True,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("拒绝把第三方参考恢复到技能发现/执行目录", result.stderr)
                    self.assertFalse((pool / "old-third-party").exists())

    def test_project_execution_root_reference_copy_is_rejected_by_both_restore_entrypoints(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            install_fixture_scripts(repo)
            project_root = Path(tmp) / "gawain"
            target = project_root / ".agents" / "skills" / "sample"
            policy = {
                "pool": str(Path(tmp) / ".agents" / "skills"),
                "agent_roots": [],
                "projects": {"gawain": str(project_root)},
                "project_entry_roots": [".agents/skills", ".claude/skills"],
                "skills": [],
                "reference_copies": [{
                    "name": "sample",
                    "source": str(Path(tmp) / "upstream-original" / "sample"),
                    "destination": str(target),
                    "fingerprint": "unused-by-offline-restore",
                }],
            }
            (repo / "inventory" / "skill-policy.json").write_text(json.dumps(policy))
            with tarfile.open(repo / "tools" / "skills-bundle.tar.gz", "w:gz") as archive:
                info = tarfile.TarInfo("references/sample/SKILL.md")
                data = b"original reference\n"
                info.size = len(data)
                import io
                archive.addfile(info, io.BytesIO(data))

            for script in (repo / "scripts" / "restore-bundle.py", repo / "tools" / "restore-bundle.py"):
                with self.subTest(script=script):
                    result = subprocess.run(
                        ["python3", str(script)], capture_output=True, text=True,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("拒绝把参考副本恢复到技能发现/执行目录", result.stderr)
                    self.assertFalse(target.exists())

    def test_project_assets_reference_remains_restorable_through_both_entrypoints(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            install_fixture_scripts(repo)
            project_root = Path(tmp) / "gawain"
            target = project_root / ".agent-assets" / "references" / "sample"
            policy = {
                "pool": str(Path(tmp) / ".agents" / "skills"),
                "agent_roots": [],
                "projects": {"gawain": str(project_root)},
                "project_entry_roots": [".agents/skills", ".claude/skills"],
                "skills": [],
                "reference_copies": [{
                    "name": "sample",
                    "source": str(Path(tmp) / "upstream-original" / "sample"),
                    "destination": str(target),
                    "fingerprint": "unused-by-offline-restore",
                }],
            }
            (repo / "inventory" / "skill-policy.json").write_text(json.dumps(policy))
            with tarfile.open(repo / "tools" / "skills-bundle.tar.gz", "w:gz") as archive:
                info = tarfile.TarInfo("references/sample/SKILL.md")
                data = b"original project asset reference\n"
                info.size = len(data)
                import io
                archive.addfile(info, io.BytesIO(data))

            for script in (repo / "scripts" / "restore-bundle.py", repo / "tools" / "restore-bundle.py"):
                with self.subTest(script=script):
                    result = subprocess.run(
                        ["python3", str(script)], capture_output=True, text=True, check=True,
                    )
                    self.assertIn("references/sample", result.stdout)
                    self.assertEqual((target / "SKILL.md").read_bytes(), data)
                    shutil.rmtree(target)

    def test_project_reference_skill_row_source_is_rejected_by_both_restore_entrypoints(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            install_fixture_scripts(repo)
            project_root = Path(tmp) / "gawain"
            target = project_root / ".agents" / "skills" / "sample"
            policy = {
                "pool": str(Path(tmp) / ".agents" / "skills"),
                "agent_roots": [],
                "projects": {"gawain": str(project_root)},
                "project_entry_roots": [".agents/skills", ".claude/skills"],
                "skills": [{
                    "name": "sample",
                    "state": "reference",
                    "scope": "gawain",
                    "origin": "third-party",
                    "source": str(target),
                }],
                "reference_copies": [],
            }
            (repo / "inventory" / "skill-policy.json").write_text(json.dumps(policy))
            with tarfile.open(repo / "tools" / "skills-bundle.tar.gz", "w:gz") as archive:
                info = tarfile.TarInfo("skills/sample/SKILL.md")
                data = b"original reference source\n"
                info.size = len(data)
                import io
                archive.addfile(info, io.BytesIO(data))

            for state, expected_message in (
                ("reference", "拒绝把第三方参考恢复到技能发现/执行目录"),
                ("retired", "拒绝把参考/退役来源恢复到技能发现/执行目录"),
            ):
                with self.subTest(state=state):
                    policy["skills"][0]["state"] = state
                    (repo / "inventory" / "skill-policy.json").write_text(json.dumps(policy))
                    for script in (repo / "scripts" / "restore-bundle.py", repo / "tools" / "restore-bundle.py"):
                        with self.subTest(script=script):
                            result = subprocess.run(
                                ["python3", str(script)], capture_output=True, text=True,
                            )
                            self.assertNotEqual(result.returncode, 0)
                            self.assertIn(expected_message, result.stderr)
                            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
