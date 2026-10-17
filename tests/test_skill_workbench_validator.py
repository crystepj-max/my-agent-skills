from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


STAGE_ROOT = Path(__file__).resolve().parents[1]


def repo_root() -> Path | None:
    for ancestor in Path(__file__).resolve().parents:
        if (ancestor / "scripts" / "manage-skills.py").is_file():
            return ancestor
    return None


def validator_path() -> Path:
    candidates = [STAGE_ROOT / "first-party" / "skill-workbench" / "scripts" / "quick_validate.py"]
    root = repo_root()
    if root:
        candidates.append(root / "my-skills" / "skill-workbench" / "scripts" / "quick_validate.py")
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("skill-workbench validator not found in staging or repository")


def run_validator(skill_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(validator_path()), str(skill_dir)],
        text=True, capture_output=True, check=False,
    )


class SkillWorkbenchValidatorTests(unittest.TestCase):
    def run_frontmatter(self, text: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "sample"
            skill.mkdir()
            (skill / "SKILL.md").write_text(text)
            return run_validator(skill)

    def test_valid_invocation_fields_are_preserved_and_accepted(self) -> None:
        result = self.run_frontmatter(
            "---\n"
            "name: sample-skill\n"
            "description: A test skill.\n"
            "disable-model-invocation: true\n"
            "user-invocable: false\n"
            "argument-hint: \"Topic to discuss\"\n"
            "---\n\nBody.\n"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_known_host_and_vendor_extension_fields_are_accepted(self) -> None:
        result = self.run_frontmatter(
            "---\n"
            "name: sample-skill\n"
            "description: A test skill.\n"
            "version: 1.2.0\n"
            "disable: true\n"
            "agent_created: false\n"
            "namespace: aiwg\n"
            "platforms: [all, codex]\n"
            "commandHint:\n"
            "  argumentHint: '<project-name>'\n"
            "---\n\nBody.\n"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_invocation_field_types_are_rejected(self) -> None:
        invalid = {
            "disable-model-invocation: \"true\"": "disable-model-invocation must be a boolean",
            "user-invocable: 1": "user-invocable must be a boolean",
            "argument-hint: [topic, goal]": "argument-hint must be a string",
            "version: 1": "version must be a string",
            "disable: \"true\"": "disable must be a boolean",
            "agent_created: 0": "agent_created must be a boolean",
            "namespace: 4": "namespace must be a string",
            "platforms: all": "platforms must be a list of strings",
            "platforms: [all, 4]": "platforms must be a list of strings",
            "commandHint: []": "commandHint must be a mapping",
            "commandHint:\n  argumentHint: 4": "commandHint.argumentHint must be a string",
        }
        for field, error in invalid.items():
            with self.subTest(field=field):
                result = self.run_frontmatter(
                    "---\nname: sample-skill\ndescription: A test skill.\n"
                    f"{field}\n---\nBody.\n"
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn(error, result.stdout)

    def test_unknown_top_level_frontmatter_fields_stay_rejected(self) -> None:
        result = self.run_frontmatter(
            "---\nname: sample-skill\ndescription: A test skill.\nunknown-field: true\n---\nBody.\n"
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown-field", result.stdout)

    def test_teach_package_with_explicit_invocation_metadata_validates(self) -> None:
        candidates = [STAGE_ROOT / "first-party" / "teach"]
        if STAGE_ROOT.parent.joinpath("engineering-assist", "teach").is_dir():
            candidates.append(STAGE_ROOT.parent / "engineering-assist" / "teach")
        root = repo_root()
        if root:
            candidates.append(root / "my-skills" / "teach")
        skill_dir = next((p for p in candidates if (p / "SKILL.md").is_file()), None)
        self.assertIsNotNone(skill_dir, "teach package not found in staging or repository")
        result = run_validator(skill_dir)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_first_party_clashx_and_lark_packages_keep_compatible_fields(self) -> None:
        candidates = [STAGE_ROOT / "first-party" / "clashx-openai-sse-debug"]
        lark_root = STAGE_ROOT.parent / "lark"
        candidates.extend([
            lark_root / "lark-approval" / "first-party",
            lark_root / "lark-minutes" / "first-party",
        ])
        root = repo_root()
        if root:
            candidates.extend([
                root / "my-skills" / "clashx-openai-sse-debug",
                root / "my-skills" / "lark-approval",
                root / "my-skills" / "lark-minutes",
            ])
        for skill_dir in (p for p in candidates if (p / "SKILL.md").is_file()):
            with self.subTest(skill=skill_dir.name):
                result = run_validator(skill_dir)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
