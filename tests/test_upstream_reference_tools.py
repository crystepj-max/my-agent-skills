import hashlib
import importlib.util
import json
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import Mock

TEST_ROOT = Path(__file__).resolve().parents[1]
TOOL_ROOTS = (TEST_ROOT / "tools", TEST_ROOT / "tool-patch")
TOOLS = next(root for root in TOOL_ROOTS if (root / "compare_skill_reference.py").is_file())


def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fetch = load("fetch_skill_reference")
compare_tool = load("compare_skill_reference")


class FakeResponse(BytesIO):
    pass


class ReferenceToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.home = self.root / "home"
        self.repo = self.root / "repo"
        self.home.mkdir()
        self.repo.mkdir()
        (self.repo / "inventory").mkdir()
        (self.repo / "inventory/skill-policy.json").write_text(json.dumps({
            "pool": "~/.agents/skills",
            "agent_roots": ["~/.codex/skills", "~/.claude/skills", "~/.config/claude/skills",
                            "~/.workbuddy/skills", "~/.openclaw/skills", "~/.hermes/skills",
                            "~/custom-agent-root"],
            "skills": [{"name": "wizard", "source": "my-skills/wizard"}],
        }))
        (self.home / ".agents/skills/wizard").mkdir(parents=True)
        (self.home / ".codex/skills").mkdir(parents=True)
        (self.home / ".workbuddy/skills").mkdir(parents=True)
        (self.home / "custom-agent-root").mkdir()
        (self.repo / "my-skills/wizard").mkdir(parents=True)
        (self.repo / "my-skills/wizard/SKILL.md").write_text("maintained first party\n")

    def tearDown(self):
        self.temp.cleanup()

    def test_guard_rejects_active_roots_descendants_and_ancestors(self):
        blocked = fetch.protected_roots(self.home, self.repo)
        candidates = [
            self.home / ".agents/skills",
            self.home / ".agents/skills/wizard",
            self.home / ".agents",
            self.home,
            self.home / ".workbuddy/skills",
            self.home / ".workbuddy/skills/unmanaged",
            self.home / ".workbuddy",
            self.home / "custom-agent-root",
            self.repo / "my-skills",
            self.repo / "my-skills/wizard",
            self.repo,
        ]
        for candidate in candidates:
            with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                fetch.validate_output_root(candidate, blocked)

    def test_guard_includes_project_roots_sources_and_project_entry_roots(self):
        project_root = self.home / "gawain"
        source = project_root / "skills" / "regression"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text("project maintenance source\n")
        (self.repo / "inventory/skill-policy.json").write_text(json.dumps({
            "pool": "~/.agents/skills",
            "agent_roots": ["~/.codex/skills"],
            "projects": {"gawain": "~/gawain"},
            "project_entry_roots": [".agents/skills", ".claude/skills"],
            "skills": [{"name": "regression", "source": "project:gawain/skills/regression"}],
        }))
        blocked = fetch.protected_roots(self.home, self.repo)
        for candidate in (
            project_root,
            source,
            project_root / ".agents/skills/new-skill",
            project_root / ".claude/skills/new-skill",
        ):
            with self.subTest(candidate=candidate), self.assertRaises(ValueError):
                fetch.validate_output_root(candidate, blocked)
        (self.repo / "inventory/skill-policy.json").write_text(json.dumps({
            "pool": "~/.agents/skills",
            "agent_roots": [],
            "projects": {"gawain": "~/gawain"},
            "skills": [{"name": "regression", "source": "project:gawain/../outside"}],
        }))
        with self.assertRaisesRegex(ValueError, "越出登记根目录"):
            fetch.protected_roots(self.home, self.repo, self.repo / "inventory/skill-policy.json")

    def test_guard_resolves_symlink_and_symlinked_parent_before_network(self):
        symlink = self.root / "alias"
        symlink.symlink_to(self.home / ".agents/skills", target_is_directory=True)
        opener = Mock(side_effect=AssertionError("network must not be called"))
        with self.assertRaises(ValueError):
            fetch.tree_snapshot("main", symlink, opener, self.home, self.repo)
        self.assertEqual(opener.call_count, 0)

        parent = self.root / "parent-alias"
        parent.symlink_to(self.home / ".agents", target_is_directory=True)
        with self.assertRaises(ValueError):
            fetch.validate_output_root(parent / "skills" / "future", fetch.protected_roots(self.home, self.repo))

        custom_alias = self.root / "custom-alias"
        custom_alias.symlink_to(self.home / "custom-agent-root", target_is_directory=True)
        with self.assertRaises(ValueError):
            fetch.validate_output_root(custom_alias / "snapshot", fetch.protected_roots(self.home, self.repo))

    def test_fetch_writes_only_separate_reference_snapshot_and_never_overwrites(self):
        content = {
            "skills/engineering/wizard/SKILL.md": b"name: wizard\n",
            "skills/productivity/to-questionnaire/SKILL.md": b"name: to-questionnaire\n",
            "skills/productivity/wait-what/SKILL.md": b"name: wait-what\n",
        }
        commit_sha = "c" * 40
        tree = {
            "sha": "a" * 40,
            "tree": [{"type": "blob", "path": path} for path in content],
            "truncated": False,
        }
        calls = []

        def opener(request, timeout=30):
            url = request.full_url
            calls.append(url)
            if "/commits/" in url:
                return FakeResponse(json.dumps({"sha": commit_sha}).encode())
            if "/git/trees/" in url:
                return FakeResponse(json.dumps(tree).encode())
            for path, value in content.items():
                if url.endswith(path):
                    return FakeResponse(value)
            raise AssertionError(f"unexpected URL: {url}")

        output = self.root / "references"
        snapshot = fetch.tree_snapshot("main", output, opener, self.home, self.repo)
        self.assertEqual(len(calls), 5)
        self.assertIn(f"/git/trees/{commit_sha}?recursive=1", calls[1])
        self.assertTrue(all(commit_sha in url for url in calls[2:]))
        for skill in fetch.SKILLS:
            self.assertTrue((snapshot / skill / "SKILL.md").is_file())
        metadata = json.loads((snapshot / "snapshot.json").read_text())
        self.assertEqual(metadata["kind"], "reference-only")
        self.assertEqual(metadata["commit_sha"], commit_sha)
        self.assertEqual(metadata["tree_sha"], "a" * 40)
        self.assertIn("retrieved_at", metadata)
        self.assertEqual((self.repo / "my-skills/wizard/SKILL.md").read_text(), "maintained first party\n")
        self.assertFalse((self.home / ".agents/skills/wizard/SKILL.md").exists())
        with self.assertRaises(FileExistsError):
            fetch.tree_snapshot("main", output, opener, self.home, self.repo)
        self.assertEqual((snapshot / "wizard/SKILL.md").read_bytes(), content["skills/engineering/wizard/SKILL.md"])

    def test_truncated_tree_is_not_written_as_complete_snapshot(self):
        commit_sha = "d" * 40
        tree = {"sha": "e" * 40, "tree": [], "truncated": True}

        def opener(request, timeout=30):
            if "/commits/" in request.full_url:
                return FakeResponse(json.dumps({"sha": commit_sha}).encode())
            return FakeResponse(json.dumps(tree).encode())

        output = self.root / "refs"
        with self.assertRaisesRegex(ValueError, "截断"):
            fetch.tree_snapshot("main", output, opener, self.home, self.repo)
        self.assertFalse(any(p.name.startswith("mattpocock-skills-") for p in output.iterdir()))

    def test_compare_uses_registered_mapping_and_reports_without_writing(self):
        old = self.root / "references/wizard"
        new = self.root / "new-snapshot/wizard"
        old.mkdir(parents=True)
        new.mkdir(parents=True)
        (old / "SKILL.md").write_text("old\n")
        (old / "guide.md").write_text("same\n")
        (new / "SKILL.md").write_text("new\n")
        (new / "guide.md").write_text("same\n")
        (new / "new-tool.py").write_text("new asset\n")
        renamed_source = self.repo / "my-skills/skill-workbench"
        renamed_source.mkdir(parents=True)
        (renamed_source / "SKILL.md").write_text("maintained workbench\n")
        policy = self.root / "policy.json"
        policy.write_text(json.dumps({
            "skills": [{"name": "skill-workbench", "source": "my-skills/skill-workbench", "upstream": "https://example.invalid/skill-workbench"}],
            "reference_copies": [{
                "name": "skill-creator", "maps_to": "skill-workbench", "source": "~/.agents/skills/skill-creator",
                "destination": str(old), "fingerprint": compare_tool.manager_fingerprint(old),
            }],
        }))
        before = compare_tool.manager_fingerprint(old)
        report = compare_tool.compare(policy, "skill-workbench", new, self.repo, self.home)
        self.assertEqual(report["changes"]["added"], ["new-tool.py"])
        self.assertEqual(report["changes"]["changed"], ["SKILL.md"])
        self.assertEqual(report["changes"]["unchanged"], ["guide.md"])
        self.assertEqual(report["first_party_source"], str(renamed_source.resolve()))
        self.assertEqual(report["preserved_reference"], str(old.resolve()))
        self.assertIn("no copy", report["action"])
        self.assertEqual(compare_tool.manager_fingerprint(old), before)

    def test_compare_rejects_drifted_mapping_and_snapshot_inside_skill_tree(self):
        old = self.root / "refs/wizard"
        new = self.root / "new/wizard"
        old.mkdir(parents=True)
        new.mkdir(parents=True)
        (old / "SKILL.md").write_text("changed after mapping\n")
        (new / "SKILL.md").write_text("upstream\n")
        policy = self.root / "policy.json"
        policy.write_text(json.dumps({
            "skills": [{"name": "wizard", "source": "my-skills/wizard"}],
            "reference_copies": [{"name": "wizard", "source": "~/.agents/skills/wizard",
                                  "destination": str(old), "fingerprint": "0" * 64}],
        }))
        with self.assertRaisesRegex(ValueError, "指纹"):
            compare_tool.compare(policy, "wizard", new, self.repo, self.home)
        with self.assertRaisesRegex(ValueError, "独立"):
            compare_tool.compare(policy, "wizard", self.repo / "my-skills/wizard", self.repo, self.home)

    def test_compare_resolves_and_protects_project_skill_sources(self):
        project_root = self.home / "Obsidian-Chris-Vault"
        first_party = project_root / "skills" / "sample"
        first_party.mkdir(parents=True)
        (first_party / "SKILL.md").write_text("project maintained source\n")
        old = self.root / "references/sample"
        new = self.root / "new-reference/sample"
        entry_snapshot = project_root / ".agents/skills/reference-snapshot"
        old.mkdir(parents=True)
        new.mkdir(parents=True)
        (old / "SKILL.md").write_text("upstream original\n")
        (new / "SKILL.md").write_text("new upstream snapshot\n")
        policy = self.root / "project-policy.json"
        policy.write_text(json.dumps({
            "pool": "~/.agents/skills",
            "agent_roots": ["~/.codex/skills"],
            "projects": {"presentations": "~/Obsidian-Chris-Vault"},
            "skills": [{
                "name": "sample",
                "source": "project:presentations/skills/sample",
            }],
            "reference_copies": [{
                "name": "sample",
                "destination": str(old),
                "source": "~/.agents/skills/sample",
                "fingerprint": compare_tool.manager_fingerprint(old),
            }],
        }))

        report = compare_tool.compare(policy, "sample", new, self.repo, self.home)
        self.assertEqual(report["first_party_source"], str(first_party.resolve()))
        with self.assertRaisesRegex(ValueError, "独立"):
            compare_tool.compare(policy, "sample", first_party, self.repo, self.home)
        with self.assertRaisesRegex(ValueError, "独立"):
            compare_tool.compare(policy, "sample", project_root, self.repo, self.home)
        entry_snapshot.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "独立"):
            compare_tool.compare(policy, "sample", entry_snapshot, self.repo, self.home)
        with self.assertRaisesRegex(ValueError, "越出"):
            compare_tool.expand(
                "project:presentations/../outside", self.repo, self.home,
                {"presentations": "~/Obsidian-Chris-Vault"},
            )


if __name__ == "__main__":
    unittest.main()
