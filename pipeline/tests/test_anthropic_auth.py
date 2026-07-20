"""Focused tests for Anthropic API-key vs Claude Code OAuth selection.

No network or real model calls are made.
"""

import json
import os
import sys
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import anthropic_auth as auth  # noqa: E402


class AnthropicAuthTests(unittest.TestCase):
    def test_explicit_oauth_ignores_api_key_for_selection(self):
        with (
            patch.object(auth, "_config", return_value={"anthropic_auth": {"mode": "oauth"}}),
            patch.object(auth.shutil, "which", return_value="/usr/bin/claude"),
            patch.object(auth, "claude_version", return_value=(2, 1, 205)),
            patch.dict(
                os.environ,
                {"ANTHROPIC_API_KEY": "metered-key", "CLAUDE_CODE_OAUTH_TOKEN": "oauth-token"},
                clear=False,
            ),
        ):
            client = auth.create_anthropic_client()
        self.assertIsInstance(client, auth.ClaudeCodeClient)

    def test_auto_oauth_token_precedes_metered_api_key(self):
        with (
            patch.object(auth, "_config", return_value={}),
            patch.object(auth.shutil, "which", return_value="/usr/bin/claude"),
            patch.object(auth, "claude_version", return_value=(2, 1, 205)),
            patch.dict(
                os.environ,
                {
                    "ANTHROPIC_API_KEY": "metered-key",
                    "CLAUDE_CODE_OAUTH_TOKEN": "oauth-token",
                    "PAPER_CURATION_ANTHROPIC_AUTH": "auto",
                },
                clear=False,
            ),
        ):
            status = auth.auth_status()
            client = auth.create_anthropic_client()

        self.assertEqual((status.mode, status.source, status.ready), (
            "oauth", "env:CLAUDE_CODE_OAUTH_TOKEN", True,
        ))
        self.assertIsInstance(client, auth.ClaudeCodeClient)

    def test_auto_saved_oauth_precedes_configured_api_key(self):
        with (
            patch.object(auth, "_config", return_value={"anthropic_api_key": "metered-key"}),
            patch.object(auth, "_saved_oauth_status", return_value=(True, "claude.ai, firstParty")),
            patch.object(auth.shutil, "which", return_value="/usr/bin/claude"),
            patch.object(auth, "claude_version", return_value=(2, 1, 205)),
            patch.dict(
                os.environ,
                {"CLAUDE_CODE_OAUTH_TOKEN": "", "PAPER_CURATION_ANTHROPIC_AUTH": "auto"},
                clear=False,
            ),
        ):
            status = auth.auth_status()
            client = auth.create_anthropic_client()

        self.assertEqual(status.mode, "oauth")
        self.assertIsInstance(client, auth.ClaudeCodeClient)

    def test_saved_oauth_probe_removes_api_credentials(self):
        seen = {}

        def fake_run(_command, **kwargs):
            seen["env"] = kwargs["env"]
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps({
                    "loggedIn": True,
                    "authMethod": "claude.ai",
                    "apiProvider": "firstParty",
                }),
                stderr="",
            )

        with (
            patch.object(auth.shutil, "which", return_value="/usr/bin/claude"),
            patch.object(auth.subprocess, "run", side_effect=fake_run),
            patch.dict(
                os.environ,
                {"ANTHROPIC_API_KEY": "metered", "ANTHROPIC_AUTH_TOKEN": "bearer"},
                clear=False,
            ),
        ):
            ready, _detail = auth._saved_oauth_status()

        self.assertTrue(ready)
        self.assertNotIn("ANTHROPIC_API_KEY", seen["env"])
        self.assertNotIn("ANTHROPIC_AUTH_TOKEN", seen["env"])

    def test_explicit_sdk_key_is_an_api_billing_decision(self):
        sentinel = object()
        with (
            patch.object(auth, "configured_mode", return_value="oauth"),
            patch("anthropic.Anthropic", return_value=sentinel) as constructor,
        ):
            client = auth.create_anthropic_client(api_key="explicit-api-key")
        self.assertIs(client, sentinel)
        constructor.assert_called_once_with(
            api_key="explicit-api-key",
            timeout=180.0,
            max_retries=4,
        )

    def test_with_options_overrides_timeout_and_retries(self):
        client = auth.ClaudeCodeClient(timeout=180, max_retries=4)
        narrowed = client.with_options(timeout=90, max_retries=1)
        self.assertEqual((narrowed.timeout, narrowed.max_retries), (90.0, 1))

    def test_timeout_kills_claude_process_group(self):
        process = MagicMock(pid=4242, returncode=-9)
        process.communicate.side_effect = [
            auth.subprocess.TimeoutExpired(["claude"], 1),
            ("partial", "timed out"),
        ]

        with (
            patch.object(auth.subprocess, "Popen", return_value=process) as popen,
            patch.object(auth.os, "name", "posix"),
            patch.object(auth.os, "killpg") as killpg,
        ):
            with self.assertRaises(auth.subprocess.TimeoutExpired):
                auth._run_claude_process(
                    ["claude", "-p"],
                    input="prompt",
                    timeout=1,
                    cwd="/tmp",
                    env={},
                )

        self.assertTrue(popen.call_args.kwargs["start_new_session"])
        killpg.assert_called_once_with(4242, auth.signal.SIGKILL)
        self.assertEqual(process.communicate.call_count, 2)

    def test_watchdog_kills_when_communicate_does_not_time_out(self):
        released = threading.Event()
        process = MagicMock(pid=4242, returncode=-9)
        call_count = 0

        def communicate(**_kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                released.wait(1)
            return "", ""

        process.communicate.side_effect = communicate
        process.kill.side_effect = released.set
        started = time.monotonic()
        with (
            patch.object(auth.subprocess, "Popen", return_value=process),
            patch.object(auth.os, "name", "posix"),
            patch.object(auth.os, "killpg") as killpg,
        ):
            with self.assertRaises(auth.subprocess.TimeoutExpired):
                auth._run_claude_process(
                    ["claude", "-p"],
                    input="prompt",
                    timeout=0.05,
                    cwd="/tmp",
                    env={},
                )

        self.assertLess(time.monotonic() - started, 0.5)
        killpg.assert_called_once_with(4242, auth.signal.SIGKILL)
        process.kill.assert_called_once_with()

    def test_watchdog_enforces_wall_deadline_after_system_sleep(self):
        released = threading.Event()
        process = MagicMock(pid=4242, returncode=-9)
        fake_wall = [100.0]
        call_count = 0

        def communicate(**_kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                fake_wall[0] = 200.0
                released.wait(1)
            return "", ""

        process.communicate.side_effect = communicate
        process.kill.side_effect = released.set
        started = time.monotonic()
        with (
            patch.object(auth.subprocess, "Popen", return_value=process),
            patch.object(auth.os, "name", "posix"),
            patch.object(auth.os, "killpg") as killpg,
            patch.object(auth.time, "time", side_effect=lambda: fake_wall[0]),
        ):
            with self.assertRaises(auth.subprocess.TimeoutExpired):
                auth._run_claude_process(
                    ["claude", "-p"],
                    input="prompt",
                    timeout=10,
                    cwd="/tmp",
                    env={},
                )

        self.assertLess(time.monotonic() - started, 0.75)
        killpg.assert_called_once_with(4242, auth.signal.SIGKILL)
        process.kill.assert_called_once_with()

    def test_oauth_child_removes_higher_precedence_api_credentials(self):
        seen = {}

        def fake_run(command, **kwargs):
            seen["command"] = command
            seen["env"] = kwargs["env"]
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps({"type": "result", "is_error": False, "result": "OK"}),
                stderr="",
            )

        with (
            patch.object(auth.shutil, "which", return_value="/usr/bin/claude"),
            patch.object(auth, "_run_claude_process", side_effect=fake_run),
            patch.dict(
                os.environ,
                {"ANTHROPIC_API_KEY": "metered", "ANTHROPIC_AUTH_TOKEN": "bearer"},
                clear=False,
            ),
        ):
            client = auth.ClaudeCodeClient(max_retries=0)
            response = client.messages.create(
                model="haiku", max_tokens=10,
                messages=[{"role": "user", "content": "say OK"}],
            )

        self.assertEqual(response.content[0].text, "OK")
        self.assertNotIn("ANTHROPIC_API_KEY", seen["env"])
        self.assertNotIn("ANTHROPIC_AUTH_TOKEN", seen["env"])
        self.assertIn("--safe-mode", seen["command"])
        self.assertNotIn("--bare", seen["command"])

    def test_structured_output_maps_to_tool_use_block(self):
        schema = {
            "type": "object",
            "properties": {"answer": {"type": "string"}},
            "required": ["answer"],
        }
        payload = {
            "type": "result",
            "is_error": False,
            "result": "",
            "structured_output": {"answer": "yes"},
        }

        with (
            patch.object(auth.shutil, "which", return_value="/usr/bin/claude"),
            patch.object(auth, "claude_version", return_value=(2, 1, 205)),
            patch.object(
                auth,
                "_run_claude_process",
                return_value=SimpleNamespace(returncode=0, stdout=json.dumps(payload), stderr=""),
            ) as run,
        ):
            response = auth.ClaudeCodeClient(max_retries=0).messages.create(
                model="sonnet",
                max_tokens=100,
                tools=[{"name": "emit", "input_schema": schema}],
                tool_choice={"type": "tool", "name": "emit"},
                messages=[{"role": "user", "content": "answer"}],
            )

        block = response.content[0]
        self.assertEqual((block.type, block.name, block.input), ("tool_use", "emit", {"answer": "yes"}))
        command = run.call_args.args[0]
        self.assertIn("--json-schema", command)

    def test_structured_output_requires_supported_cli_version(self):
        with (
            patch.object(auth.shutil, "which", return_value="/usr/bin/claude"),
            patch.object(auth, "claude_version", return_value=(2, 1, 201)),
        ):
            with self.assertRaisesRegex(auth.AnthropicAuthError, "claude update"):
                auth.ClaudeCodeClient(max_retries=0).messages.create(
                    model="sonnet",
                    tools=[{"name": "emit", "input_schema": {"type": "object"}}],
                    messages=[{"role": "user", "content": "answer"}],
                )
    def test_vision_call_materializes_only_images_in_temporary_cwd(self):
        seen = {}

        def fake_run(command, **kwargs):
            cwd = Path(kwargs["cwd"])
            seen["cwd"] = cwd
            seen["command"] = command
            seen["prompt"] = kwargs["input"]
            image = cwd / "input-image-1.png"
            self.assertTrue(image.is_file())
            self.assertEqual(image.read_bytes(), b"image-bytes")
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps({
                    "type": "result",
                    "is_error": False,
                    "structured_output": {"best": 1},
                }),
                stderr="",
            )

        encoded = __import__("base64").b64encode(b"image-bytes").decode()
        with (
            patch.object(auth.shutil, "which", return_value="/usr/bin/claude"),
            patch.object(auth, "claude_version", return_value=(2, 1, 205)),
            patch.object(auth, "_run_claude_process", side_effect=fake_run),
        ):
            response = auth.ClaudeCodeClient(max_retries=0).messages.create(
                model="haiku",
                tools=[{
                    "name": "pick",
                    "input_schema": {
                        "type": "object",
                        "properties": {"best": {"type": "integer"}},
                        "required": ["best"],
                    },
                }],
                messages=[{
                    "role": "user",
                    "content": [{
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": encoded,
                        },
                    }],
                }],
            )

        self.assertEqual(response.content[0].input, {"best": 1})
        self.assertIn("Read", seen["command"])
        self.assertNotIn(encoded, seen["prompt"])
        self.assertFalse(seen["cwd"].exists())

    def test_base64_images_fail_closed(self):
        with self.assertRaises(auth.ClaudeCodeUnsupportedContent):
            auth._render_messages([
                {
                    "role": "user",
                    "content": [{"type": "image", "source": {"type": "base64", "data": "abc"}}],
                }
            ])

    def test_json_extraction_accepts_fenced_result(self):
        self.assertEqual(auth._extract_json('```json\n{"ok": true}\n```'), {"ok": True})


if __name__ == "__main__":
    unittest.main()
