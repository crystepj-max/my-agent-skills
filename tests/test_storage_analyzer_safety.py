import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

TEST_ROOT = Path(__file__).resolve().parents[1]
SKILL_CANDIDATES = (
    TEST_ROOT / "my-skills" / "storage-analyzer",
    TEST_ROOT / "first-party" / "storage-analyzer",
)
SKILL_ROOT = next((path for path in SKILL_CANDIDATES if path.is_dir()), None)
if SKILL_ROOT is None:
    raise RuntimeError(f"storage-analyzer skill not found near {__file__}")
SERVER_PATH = SKILL_ROOT / "scripts" / "server.py"
spec = importlib.util.spec_from_file_location("storage_server_under_test", SERVER_PATH)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class StorageAnalyzerMutationGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = tempfile.TemporaryDirectory(dir=server.HOME)
        self.target = Path(self.temp_root.name) / "cache-item"
        self.target.mkdir()
        server.TOKEN = "test-token"
        server.RM_ALLOW = {str(self.target.resolve())}
        server.TRASH_ALLOW = {str(self.target.resolve())}
        server.OPEN_ALLOW = {str(self.target.resolve())}
        server.DATA = {"green": [{"name": "fixture", "trash_paths": [str(self.target)]}]}
        server.TPL = (SERVER_PATH.parent.parent / "assets" / "report_template.html").read_text()

    def tearDown(self):
        self.temp_root.cleanup()

    def request(self, mode, path=None, token=None, host=None):
        srv = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        thread = threading.Thread(target=srv.serve_forever, daemon=True)
        thread.start()
        try:
            payload = json.dumps({"token": token or server.TOKEN, "mode": mode, "paths": [str(path or self.target)]}).encode()
            headers = {"Content-Type": "application/json"}
            if host:
                headers["Host"] = host
            req = Request(f"http://127.0.0.1:{srv.server_address[1]}/action", data=payload, headers=headers)
            try:
                with urlopen(req, timeout=3) as response:
                    return response.status, json.loads(response.read())
            except HTTPError as exc:
                body = json.loads(exc.read())
                status = exc.code
                exc.close()
                return status, body
        finally:
            srv.shutdown()
            srv.server_close()
            thread.join(timeout=3)

    def test_default_server_blocks_trash_and_hard_delete_without_calling_mutators(self):
        server.ACTIONS_ENABLED = False
        server.HARD_DELETE_ENABLED = False
        with patch.object(server, "move_to_trash") as trash, patch.object(server, "hard_delete") as hard_delete:
            trash_status, _ = self.request("trash")
            hard_status, _ = self.request("rm")
        self.assertEqual(trash_status, 403)
        self.assertEqual(hard_status, 403)
        trash.assert_not_called()
        hard_delete.assert_not_called()
        self.assertTrue(self.target.exists())

    def test_enabled_actions_reach_only_the_mocked_trash_function(self):
        server.ACTIONS_ENABLED = True
        server.HARD_DELETE_ENABLED = False
        with patch.object(server, "move_to_trash") as trash, patch.object(server, "hard_delete") as hard_delete:
            status, body = self.request("trash")
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        trash.assert_called_once_with(str(self.target.resolve()))
        hard_delete.assert_not_called()
        self.assertTrue(self.target.exists())

    def test_host_token_and_mode_specific_allowlists_still_guard_mutations(self):
        server.ACTIONS_ENABLED = True
        server.HARD_DELETE_ENABLED = True
        outside_path = "/Applications/fixture.app"
        server.TRASH_ALLOW.add(str(Path(outside_path).resolve()))
        with patch.object(server, "move_to_trash") as trash, patch.object(server, "hard_delete") as hard_delete:
            bad_host, _ = self.request("trash", host="attacker.example")
            bad_token, _ = self.request("trash", token="wrong-token")
            outside_home, _ = self.request("trash", path=outside_path)
        self.assertEqual(bad_host, 403)
        self.assertEqual(bad_token, 403)
        self.assertEqual(outside_home, 403)
        trash.assert_not_called()
        hard_delete.assert_not_called()

    def test_hard_delete_requires_separate_enable_flag_and_calls_only_mock(self):
        server.ACTIONS_ENABLED = True
        server.HARD_DELETE_ENABLED = False
        with patch.object(server, "hard_delete") as hard_delete:
            status, _ = self.request("rm")
        self.assertEqual(status, 403)
        hard_delete.assert_not_called()
        server.HARD_DELETE_ENABLED = True
        with patch.object(server, "hard_delete") as hard_delete:
            status, body = self.request("rm")
        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        hard_delete.assert_called_once_with(str(self.target.resolve()))
        self.assertTrue(self.target.exists())

    def test_report_template_hides_delete_controls_when_actions_are_disabled(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js is needed to execute the report's browser rendering functions")

        html = (SERVER_PATH.parent.parent / "assets" / "report_template.html").read_text()
        function_sources = []
        for name in ("delBlock", "greenBatchActions", "yellowActions"):
            match = re.search(rf"(?ms)^function {name}\([^\n]*\)\{{.*?^\}}", html)
            self.assertIsNotNone(match, f"report function {name} was not found")
            function_sources.append(match.group(0))

        js = "\n".join(
            [
                *function_sources,
                "globalThis.render = {delBlock, greenBatchActions, yellowActions};",
            ]
        )
        scenarios = [
            {
                "config": None,
                "expected": {"trash": False, "hard": False},
                "name": "static report",
            },
            {
                "config": {"actionsEnabled": False, "hardDeleteEnabled": False},
                "expected": {"trash": False, "hard": False},
                "name": "default read-only server",
            },
            {
                "config": {"actionsEnabled": True, "hardDeleteEnabled": False},
                "expected": {"trash": True, "hard": False},
                "name": "explicit reversible actions",
            },
            {
                "config": {"actionsEnabled": True, "hardDeleteEnabled": True},
                "expected": {"trash": True, "hard": True},
                "name": "separately enabled hard delete",
            },
        ]
        for scenario in scenarios:
            with self.subTest(scenario=scenario["name"]):
                setup = (
                    "const DELETE = "
                    + json.dumps(scenario["config"])
                    + "; const FM = 'Finder'; const b64 = () => 'encoded'; "
                    + "const esc = value => String(value);\n"
                    + js
                    + "\nconst item = {trash_paths: ['/Users/test/cache']}; "
                    + "const output = [render.delBlock(item), "
                    + "render.greenBatchActions([item]), render.yellowActions(item)].join('\\n'); "
                    + "process.stdout.write(output);"
                )
                result = subprocess.run(
                    [node, "-e", setup], capture_output=True, text=True, check=True
                )
                rendered = result.stdout
                self.assertEqual(
                    'class="del-btn trash"' in rendered,
                    scenario["expected"]["trash"],
                )
                self.assertEqual(
                    'class="del-btn danger"' in rendered,
                    scenario["expected"]["hard"],
                )


if __name__ == "__main__":
    unittest.main()
