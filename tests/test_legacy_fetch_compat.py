from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


STAGE_ROOT = Path(__file__).resolve().parents[1]


def legacy_entrypoint() -> Path:
    candidate = STAGE_ROOT / "tool-patch" / "legacy_fetch_new_skills.py"
    if candidate.is_file():
        return candidate
    for ancestor in Path(__file__).resolve().parents:
        if (ancestor / "scripts" / "manage-skills.py").is_file():
            return ancestor / "tools" / "fetch_new_skills.py"
    raise FileNotFoundError("legacy fetch compatibility entry point not found")


class LegacyFetchCompatibilityTests(unittest.TestCase):
    def test_retired_installer_stops_without_network_or_symlink_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = root / "home"
            repo = root / "repo"
            sitecustomize = root / "mock-python"
            for directory in (home, repo, sitecustomize):
                directory.mkdir()

            maintained = repo / "my-skills" / "wizard"
            maintained.mkdir(parents=True)
            marker = maintained / "SKILL.md"
            marker.write_text("first-party maintained content\n")
            pool = home / ".agents" / "skills"
            pool.mkdir(parents=True)
            (pool / "wizard").symlink_to(maintained, target_is_directory=True)
            before_hash = hashlib.sha256(marker.read_bytes()).hexdigest()
            before_files = sorted(str(p.relative_to(maintained)) for p in maintained.rglob("*"))

            network_marker = root / "network-called"
            (sitecustomize / "sitecustomize.py").write_text(
                "import os\n"
                "from pathlib import Path\n"
                "import urllib.request\n"
                "fixture_home = Path(os.environ['FIXTURE_HOME'])\n"
                "Path.home = classmethod(lambda cls: fixture_home)\n"
                "_expanduser = os.path.expanduser\n"
                "def fixture_expanduser(path):\n"
                "    if path == '~': return str(fixture_home)\n"
                "    if path.startswith('~/'): return str(fixture_home / path[2:])\n"
                "    return _expanduser(path)\n"
                "os.path.expanduser = fixture_expanduser\n"
                "def blocked(*args, **kwargs):\n"
                "    Path(os.environ['NETWORK_MARKER']).write_text('called')\n"
                "    raise AssertionError('network must not be called')\n"
                "urllib.request.urlopen = blocked\n"
            )
            result = subprocess.run(
                [sys.executable, str(legacy_entrypoint())],
                cwd=repo,
                env={
                    **os.environ,
                    "PYTHONPATH": str(sitecustomize),
                    "FIXTURE_HOME": str(home),
                    "NETWORK_MARKER": str(network_marker),
                },
                text=True, capture_output=True, check=False,
            )

            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("已停用", result.stdout)
            self.assertFalse(network_marker.exists())
            self.assertEqual(hashlib.sha256(marker.read_bytes()).hexdigest(), before_hash)
            self.assertEqual(
                sorted(str(p.relative_to(maintained)) for p in maintained.rglob("*")),
                before_files,
            )
            self.assertTrue((pool / "wizard").is_symlink())


if __name__ == "__main__":
    unittest.main()
