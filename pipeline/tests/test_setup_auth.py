"""Focused setup-gate tests for OAuth/API-key onboarding."""

import os
import io
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

    def test_step_config_writes_secret_free_topic_profile_and_creates_pdf_cache(self):
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
            self.assertNotIn("api_key", cfg["zotero"])
            self.assertEqual(cfg["zotero"]["collections"], {"trial": "Trial Papers"})
            self.assertEqual(cfg["topic_profiles"]["trial"]["label"], "Trial Papers")
            self.assertEqual(cfg["topic_profiles"]["trial"]["collection_name"], "Trial Papers")
            self.assertNotIn("collection_key", cfg["topic_profiles"]["trial"])
            self.assertNotIn("collection", cfg["topic_profiles"]["trial"])
            self.assertNotIn("collection_label", cfg["topic_profiles"]["trial"])
            self.assertEqual(cfg["topic_profiles"]["trial"]["search_keywords"]["primary"], ["Trial Papers"])
            self.assertEqual(cfg["paths"]["zotero_dir"], str((root / "pdf_cache").resolve()))
            self.assertEqual(cfg["anthropic_auth"], {"mode": "auto"})
            self.assertTrue((root / "pdf_cache").is_dir())
            self.assertNotIn("zotero-secret", config_path.read_text(encoding="utf-8"))

    def test_step_config_writes_canonical_collection_keys_from_api_selection(self):
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
                        "ZOTERO_COLLECTION_NAME": "",
                        "ZOTERO_TOPIC_ALIAS": "",
                        "ZOTERO_DIR": "",
                        "ZOTERO_EMAIL": "",
                        "UNPAYWALL_EMAIL": "",
                        "PAPERBANANA_DIR": "",
                        "GITHUB_REPO": "",
                    },
                    clear=False,
                ),
                patch.object(
                    setup_cli,
                    "_fetch_zotero_collections",
                    return_value=("123", [("Robotics", "AAA11111"), ("Physical AI", "BBB22222")]),
                ),
                patch("builtins.input", return_value="2"),
            ):
                cfg = setup_cli.step_config()

            self.assertEqual(cfg["zotero"]["collections"], {"physical-ai": "Physical AI"})
            self.assertEqual(
                cfg["topic_profiles"]["physical-ai"],
                {
                    "label": "Physical AI",
                    "collection_name": "Physical AI",
                    "collection_key": "BBB22222",
                    "search_keywords": {
                        "primary": ["Physical AI"],
                        "secondary": ["physical-ai"],
                    },
                },
            )
            contents = config_path.read_text(encoding="utf-8")
            self.assertNotIn("zotero-secret", contents)

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

    def test_multiple_collections_can_be_selected_without_hardcoded_topic(self):
        with (
            patch.dict(
                os.environ,
                {"ZOTERO_COLLECTION_NAME": "", "ZOTERO_TOPIC_ALIAS": ""},
                clear=False,
            ),
            patch.object(
                setup_cli,
                "_fetch_zotero_collections",
                return_value=(
                    "123",
                    [
                        ("Robotics", "AAA"),
                        ("Physical AI", "BBB"),
                        ("Life Sciences", "CCC"),
                    ],
                ),
            ),
            patch("builtins.input", return_value="2,3"),
        ):
            selected = setup_cli._select_zotero_collections("zotero-key")

        self.assertEqual(
            selected,
            {
                "physical-ai": {"label": "Physical AI", "name": "Physical AI", "key": "BBB"},
                "life-sciences": {"label": "Life Sciences", "name": "Life Sciences", "key": "CCC"},
            },
        )

    def test_existing_config_requires_explicit_noninteractive_choice(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config_path.write_text(
                '{"zotero":{"collections":{"stale":"Fork Residue"}}}',
                encoding="utf-8",
            )
            with (
                patch.object(setup_cli, "CONFIG_PATH", config_path),
                patch.object(setup_cli.sys.stdin, "isatty", return_value=False),
            ):
                with self.assertRaises(SystemExit) as raised:
                    setup_cli.step_config()

            self.assertEqual(raised.exception.code, 2)

    def test_existing_config_is_reused_only_when_explicit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config_path.write_text(
                '{"zotero":{"collections":{"mine":"My Papers"}}}',
                encoding="utf-8",
            )
            with patch.object(setup_cli, "CONFIG_PATH", config_path):
                cfg = setup_cli.step_config("reuse")

            self.assertEqual(cfg["zotero"]["collections"], {"mine": "My Papers"})

    def test_auto_auth_selects_api_key_without_rewriting_config_or_secret(self):
        cfg = {"anthropic_auth": {"mode": "auto"}}
        status = SimpleNamespace(
            ready=True,
            mode="api-key",
            source="env:ANTHROPIC_API_KEY",
            detail="auto selected API key",
        )
        with (
            patch.object(setup_cli, "_anthropic_status", return_value=status),
            patch.dict(os.environ, {"ANTHROPIC_API_KEY": "metered-secret"}, clear=False),
        ):
            dirty = setup_cli._ensure_anthropic_auth(cfg, "auto")

        self.assertFalse(dirty)
        self.assertEqual(cfg, {"anthropic_auth": {"mode": "auto"}})
        self.assertNotIn("anthropic_api_key", cfg)

    def test_auto_auth_selects_oauth_without_rewriting_config_or_secret(self):
        cfg = {"anthropic_auth": {"mode": "auto"}}
        status = SimpleNamespace(
            ready=True,
            mode="oauth",
            source="saved:/login",
            detail="auto selected saved OAuth",
        )
        with (
            patch.object(setup_cli, "_anthropic_status", return_value=status),
            patch.object(setup_cli, "claude_version", return_value=(2, 1, 205)),
        ):
            dirty = setup_cli._ensure_anthropic_auth(cfg, "auto")

        self.assertFalse(dirty)
        self.assertEqual(cfg, {"anthropic_auth": {"mode": "auto"}})
        self.assertNotIn("claude_code_oauth_token", cfg)

    def test_setup_printed_and_invoked_first_run_commands_are_no_deploy_and_no_rebuild_safe(self):
        cfg = {"zotero": {"collections": {"trial": "Trial Papers"}}}
        stdout = io.StringIO()
        with (
            patch.object(sys, "argv", ["setup.py"]),
            patch.object(sys, "stdout", stdout),
            patch.object(setup_cli, "_load_dotenv", return_value=[]),
            patch.object(setup_cli, "step_config", return_value=cfg),
            patch.object(setup_cli, "step_env_check"),
            patch.object(setup_cli, "step_zotero_test"),
            patch.object(setup_cli, "step_paperbanana", return_value=cfg),
            patch.object(setup_cli, "step_skill_md"),
            patch.object(setup_cli, "step_install"),
            patch.object(setup_cli, "_preflight_clustering_env", return_value=True),
            patch.object(setup_cli.subprocess, "run") as run_mock,
        ):
            setup_cli.main()

        emitted = [
            line.strip()
            for line in stdout.getvalue().splitlines()
            if "python pipeline/run_full.py" in line
        ]
        self.assertGreaterEqual(len(emitted), 3)
        for command in emitted:
            self.assertIn("PAPER_CURATION_NO_DEPLOY=1", command)
            self.assertIn("--no-deploy", command)

            if "--mode rebuild" not in command:
                self.assertIn("PAPER_CURATION_NO_VECTOR_REBUILD=1", command)
            else:
                self.assertNotIn("PAPER_CURATION_NO_VECTOR_REBUILD=1", command)
        invoked = run_mock.call_args.args[0]
        invoked_env = run_mock.call_args.kwargs["env"]
        self.assertIn("--no-deploy", invoked)
        self.assertEqual(invoked_env["PAPER_CURATION_NO_DEPLOY"], "1")
        self.assertEqual(invoked_env["PAPER_CURATION_NO_VECTOR_REBUILD"], "1")


    def test_legacy_config_credentials_emit_redacted_migration_warnings(self):
        cfg = {
            "zotero": {"api_key": "zotero-secret"},
            "google_api_key": "google-secret",
            "anthropic_api_key": "anthropic-secret",
            "resend_api_key": "resend-secret",
            "openai_api_key": "openai-secret",
        }
        stdout = io.StringIO()
        with (
            patch.object(sys, "stdout", stdout),
            patch.object(setup_cli, "_ensure_anthropic_auth", return_value=False),
            patch.dict(
                os.environ,
                {
                    "ZOTERO_API_KEY": "",
                    "GOOGLE_API_KEY": "",
                    "GEMINI_API_KEY": "",
                    "RESEND_API_KEY": "",
                    "OPENAI_API_KEY": "",
                },
                clear=False,
            ),
        ):
            setup_cli.step_env_check(cfg, "api-key")

        output = stdout.getvalue()
        for field_path, env_name in (
            ("zotero.api_key", "ZOTERO_API_KEY"),
            ("google_api_key", "GOOGLE_API_KEY"),
            ("resend_api_key", "RESEND_API_KEY"),
            ("openai_api_key", "OPENAI_API_KEY"),
        ):
            self.assertIn(field_path, output)
            self.assertIn(env_name, output)
        for secret in ("zotero-secret", "google-secret", "anthropic-secret", "resend-secret", "openai-secret"):
            self.assertNotIn(secret, output)

    def test_legacy_anthropic_config_warning_is_redacted(self):
        cfg = {"anthropic_api_key": "anthropic-secret"}
        stdout = io.StringIO()
        with (
            patch.object(sys, "stdout", stdout),
            patch.dict(os.environ, {"ANTHROPIC_API_KEY": ""}, clear=False),
        ):
            setup_cli._ensure_anthropic_auth(cfg, "api-key")

        output = stdout.getvalue()
        self.assertIn("anthropic_api_key", output)
        self.assertIn("ANTHROPIC_API_KEY", output)
        self.assertNotIn("anthropic-secret", output)
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
        self.assertEqual(cfg["anthropic_auth"], {"mode": "api-key"})

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
