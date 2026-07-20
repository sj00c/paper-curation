"""Focused setup-gate tests for OAuth/API-key onboarding."""

import os
import sys
import unittest
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import setup as setup_cli  # noqa: E402


class SetupAuthTests(unittest.TestCase):
    def test_core_key_gate_excludes_anthropic_and_resend(self):
        self.assertEqual(
            [spec["env"] for spec in setup_cli.REQUIRED_KEYS],
            ["ZOTERO_API_KEY", "GOOGLE_API_KEY"],
        )

    def test_google_env_alias_is_accepted(self):
        google_spec = next(
            spec for spec in setup_cli.REQUIRED_KEYS
            if spec["env"] == "GOOGLE_API_KEY"
        )
        with patch.dict(
            os.environ,
            {"GOOGLE_API_KEY": "", "GEMINI_API_KEY": "gemini-key"},
            clear=False,
        ):
            value, source = setup_cli._key_value({}, google_spec)
        self.assertEqual((value, source), ("gemini-key", "env"))

    def test_dotenv_loader_preserves_shell_precedence_and_ignores_blanks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "PC_TEST_DOTENV_VALUE=from-file\n"
                "PC_TEST_SHELL_VALUE=from-file\n"
                "PC_TEST_BLANK=\n",
                encoding="utf-8",
            )
            with patch.dict(
                os.environ,
                {"PC_TEST_SHELL_VALUE": "from-shell"},
                clear=False,
            ):
                loaded = setup_cli._load_dotenv(env_path)
                self.assertEqual(os.environ["PC_TEST_DOTENV_VALUE"], "from-file")
                self.assertEqual(os.environ["PC_TEST_SHELL_VALUE"], "from-shell")
                self.assertNotIn("PC_TEST_BLANK", os.environ)

        self.assertEqual(loaded, ["PC_TEST_DOTENV_VALUE"])

    def test_step_config_uses_key_and_creates_pdf_cache(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_path = root / "config.json"
            with (
                patch.object(setup_cli, "REPO", root),
                patch.object(setup_cli, "CONFIG_PATH", config_path),
                patch.dict(
                    os.environ,
                    {
                        "ZOTERO_API_KEY": "zotero-secret",
                        "ZOTERO_COLLECTION_NAME": "Trial Papers",
                        "ZOTERO_TOPIC_ALIAS": "trial",
                        "ZOTERO_DIR": "",
                        "ZOTERO_EMAIL": "",
                        "UNPAYWALL_EMAIL": "",
                        "PAPERBANANA_DIR": "",
                        "GITHUB_REPO": "",
                    },
                    clear=False,
                ),
                patch("builtins.input", side_effect=AssertionError("unexpected prompt")),
            ):
                cfg = setup_cli.step_config()

            self.assertTrue(config_path.is_file())
            self.assertEqual(cfg["zotero"]["api_key"], "zotero-secret")
            self.assertEqual(cfg["zotero"]["collections"], {"trial": "Trial Papers"})
            self.assertEqual(cfg["zotero"]["pdf_dir"], str((root / "pdf_cache").resolve()))
            self.assertTrue((root / "pdf_cache").is_dir())

    def test_step_config_rejects_empty_zotero_key_before_network(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with (
                patch.object(setup_cli, "REPO", root),
                patch.object(setup_cli, "CONFIG_PATH", root / "config.json"),
                patch.dict(os.environ, {"ZOTERO_API_KEY": ""}, clear=False),
                patch("builtins.input", return_value=""),
                patch.object(
                    setup_cli,
                    "_select_zotero_collection",
                    side_effect=AssertionError("network lookup should not run"),
                ),
            ):
                with self.assertRaises(SystemExit):
                    setup_cli.step_config()

    def test_collection_is_selected_from_zotero_api_results(self):
        with (
            patch.dict(
                os.environ,
                {"ZOTERO_COLLECTION_NAME": "", "ZOTERO_TOPIC_ALIAS": ""},
                clear=False,
            ),
            patch.object(
                setup_cli,
                "_fetch_zotero_collections",
                return_value=("123", [("Robotics", "AAA"), ("Physical AI", "BBB")]),
            ),
            patch("builtins.input", return_value="2"),
        ):
            name, alias = setup_cli._select_zotero_collection("zotero-key")

        self.assertEqual((name, alias), ("Physical AI", "physical-ai"))

    def test_oauth_persists_only_non_secret_mode(self):
        cfg = {"anthropic_api_key": "old-metered-key"}
        status = SimpleNamespace(
            ready=True,
            mode="oauth",
            source="saved:/login",
            detail="claude.ai, max",
        )
        with (
            patch.object(setup_cli, "_anthropic_status", return_value=status),
            patch.object(setup_cli, "claude_version", return_value=(2, 1, 205)),
        ):
            dirty = setup_cli._ensure_anthropic_auth(cfg, "oauth")

        self.assertTrue(dirty)
        self.assertEqual(cfg["anthropic_auth"], {"mode": "oauth"})
        self.assertNotIn("claude_code_oauth_token", cfg)

    def test_api_key_mode_keeps_existing_compatible_field(self):
        cfg = {"anthropic_api_key": "configured-key", "anthropic_auth": {"mode": "oauth"}}
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": ""}, clear=False):
            dirty = setup_cli._ensure_anthropic_auth(cfg, "api-key")

        self.assertTrue(dirty)
        self.assertEqual(cfg["anthropic_api_key"], "configured-key")
        self.assertNotIn("anthropic_auth", cfg)

    def test_oauth_rejects_old_claude_code(self):
        cfg = {}
        status = SimpleNamespace(ready=True, mode="oauth", source="saved:/login", detail="max")
        with (
            patch.object(setup_cli, "_anthropic_status", return_value=status),
            patch.object(setup_cli, "claude_version", return_value=(2, 1, 201)),
        ):
            with self.assertRaises(SystemExit):
                setup_cli._ensure_anthropic_auth(cfg, "oauth")


if __name__ == "__main__":
    unittest.main()
