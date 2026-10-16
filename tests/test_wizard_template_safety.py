from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


STAGE_ROOT = Path(__file__).resolve().parents[1]


def template_path() -> Path:
    candidates = [STAGE_ROOT / "first-party" / "wizard" / "template.sh"]
    for ancestor in Path(__file__).resolve().parents:
        if (ancestor / "scripts" / "manage-skills.py").is_file():
            candidates.append(ancestor / "my-skills" / "wizard" / "template.sh")
            break
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError("wizard template not found in staging or repository")


class WizardTemplateSafetyTests(unittest.TestCase):
    def test_unwritten_template_exits_without_opening_urls_or_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            log = root / "external-calls.log"
            for name in ("open", "xdg-open", "explorer.exe", "wslview", "gh"):
                command = bin_dir / name
                command.write_text(f"#!/bin/sh\nprintf '%s\\n' '{name}' >> '{log}'\n")
                command.chmod(0o755)

            script = root / "template.sh"
            script.write_bytes(template_path().read_bytes())
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
            result = subprocess.run(
                ["bash", str(script)], cwd=root, env=env, text=True,
                capture_output=True, check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("template only", result.stdout)
            self.assertFalse((root / ".env").exists())
            self.assertFalse(log.exists())

    def test_authored_but_noninteractive_wizard_stops_before_stage_actions(self) -> None:
        source = template_path().read_text()
        placeholder = "TOTAL_STAGES=0\nWIZARD_READY=0"
        self.assertIn(placeholder, source)
        source = source.replace(placeholder, "TOTAL_STAGES=1\nWIZARD_READY=1", 1)
        source = source.replace(
            "# Author the stages here. Keep external writes behind confirm gates.\n"
            "# Example:\n"
            "# banner \"Project setup\"\n"
            "# stage \"Capture a value\"\n"
            "# open_url \"https://service.example/settings\"\n"
            "# ask_secret API_TOKEN \"Paste the token:\"\n"
            "# write_env API_TOKEN \"$API_TOKEN\"\n\n"
            "finish",
            "stage \"Mock external action\"\n"
            "open_url \"https://service.example/settings\"\n"
            "set_secret API_TOKEN test-value\n"
            "finish",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            log = root / "external-calls.log"
            for name in ("open", "xdg-open", "explorer.exe", "wslview", "gh"):
                command = bin_dir / name
                if name == "gh":
                    body = (
                        "#!/bin/sh\n"
                        f"printf '%s\\n' \"gh $*\" >> '{log}'\n"
                        "case \"$1 $2\" in\n"
                        "  'auth status') exit 0 ;;\n"
                        "  'repo view') printf 'example/repo\\n'; exit 0 ;;\n"
                        "  'secret set') cat >/dev/null; exit 0 ;;\n"
                        "esac\n"
                        "exit 1\n"
                    )
                else:
                    body = f"#!/bin/sh\nprintf '%s\\n' '{name}' >> '{log}'\n"
                command.write_text(body)
                command.chmod(0o755)
            script = root / "generated.sh"
            script.write_text(source)
            result = subprocess.run(
                ["bash", str(script)], cwd=root,
                env={**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"},
                text=True, capture_output=True, check=False,
            )

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("requires an interactive terminal", result.stdout)
            self.assertFalse((root / ".env").exists())
            self.assertFalse(log.exists())


if __name__ == "__main__":
    unittest.main()
