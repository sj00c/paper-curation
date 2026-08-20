"""Contract tests for the one-time strict local config migration."""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import stat
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from paper_curation.application.migrate import (
    execute_config_migration,
    load_config_migration,
    plan_config_migration,
)
from paper_curation.cli import main
from paper_curation.config.models import AppConfig
from paper_curation.errors import ConfigError


class ConfigMigrationTests(unittest.TestCase):
    def old_config(self) -> dict[str, object]:
        return {
            "zotero": {
                "api_key": "never-print-this-secret",
                "collections": {"example_topic": "Example Collection"},
            },
            "anthropic_auth": {"mode": "oauth"},
        }

    def test_preview_lists_deterministic_paths_and_never_secrets(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "config.json"
            path.write_text(json.dumps(self.old_config()), encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["migrate", "--config", str(path)]), 0)
            self.assertEqual(
                output.getvalue().splitlines(),
                [
                    "workspace.root", "source.provider", "source.transport", "source.collections",
                    "source.sqlite_path", "core.review.provider", "core.review.model", "core.review.local_endpoint",
                    "features", "credentials", "search_keywords", "topic_profiles", "publication",
                    "operator", "notifications",
                ],
            )
            self.assertNotIn("never-print-this-secret", output.getvalue())
            self.assertNotIn("claude-sonnet-5", output.getvalue())
            self.assertFalse((path.parent / "config.json.pre-migration.bak").exists())

    def test_execute_creates_exact_backup_and_loadable_atomic_result(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "config.json"
            original = (
                b'{\n  "zotero": {"collections": {"example_topic": "Example Collection"}},\n'
                b'  "anthropic_auth": {"mode": "oauth"}\n}\n'
            )
            path.write_bytes(original)
            self.assertEqual(main(["migrate", "--config", str(path), "--execute"]), 0)
            backup = path.parent / "config.json.pre-migration.bak"
            self.assertEqual(backup.read_bytes(), original)
            self.assertEqual(stat.S_IMODE(backup.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            migrated = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(AppConfig.from_mapping(migrated).core.review.provider, "claude-code-oauth")
            self.assertEqual(AppConfig.from_mapping(migrated).core.review.model, "claude-sonnet-5")

    def test_atomic_failure_leaves_original_and_backup(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "config.json"
            original = json.dumps(self.old_config()).encode()
            path.write_bytes(original)
            plan = load_config_migration(path)
            with patch("paper_curation.application.migrate.os.replace", side_effect=OSError("blocked")):
                with self.assertRaises(ConfigError):
                    execute_config_migration(path, plan)
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual((path.parent / "config.json.pre-migration.bak").read_bytes(), original)

    def test_idempotent_plan_has_no_changes(self) -> None:
        migrated = plan_config_migration(self.old_config())
        again = plan_config_migration(migrated.config)
        self.assertEqual(again.changed_paths, ())

    def test_execute_no_change_does_not_create_a_backup(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "config.json"
            migrated = plan_config_migration(self.old_config())
            path.write_text(json.dumps(migrated.config), encoding="utf-8")
            execute_config_migration(path, plan_config_migration(migrated.config))
            self.assertFalse((path.parent / "config.json.pre-migration.bak").exists())

    def test_explicit_cloudflare_publication_is_migrated_and_loadable(self) -> None:
        config = self.old_config()
        config["zotero"] = {
            "collections": {"example_topic": "Example Collection"},
            "sqlite_path": "/Users/example/Zotero/zotero.sqlite",
            "pdf_dir": "/Users/example/Zotero/storage",
        }
        config["publication"] = {
            "base_url": "https://example.invalid/papers",
            "provider": "cloudflare",
            "config_path": "deploy/wrangler.toml",
        }
        plan = plan_config_migration(config)
        self.assertEqual(plan.config["source"]["transport"], "local-sqlite")
        self.assertEqual(plan.config["source"]["sqlite_path"], "/Users/example/Zotero/zotero.sqlite")
        self.assertEqual(
            plan.config["publication"],
            {
                "mode": "public",
                "base_url": "https://example.invalid/papers",
                "provider": "cloudflare",
                "config_path": "deploy/wrangler.toml",
            },
        )
        self.assertEqual(AppConfig.from_mapping(plan.config).publication.provider, "cloudflare")
        self.assertIn("zotero.pdf_dir", plan.changed_paths)

    def test_url_only_publication_remains_local_without_inferred_deploy(self) -> None:
        config = self.old_config()
        config["github"] = {"pages_base_url": "https://example.invalid/papers"}
        plan = plan_config_migration(config)
        self.assertEqual(
            plan.config["publication"],
            {
                "mode": "local",
                "base_url": "https://example.invalid/papers",
                "provider": "",
                "config_path": "",
            },
        )
        self.assertEqual(plan.reported_paths, ("github.pages_base_url",))
        self.assertEqual(AppConfig.from_mapping(plan.config).publication.mode, "local")

    def test_explicit_local_publication_remains_local_and_idempotent(self) -> None:
        config = self.old_config()
        config["publication"] = {"mode": "local", "base_url": "https://example.invalid/papers"}
        plan = plan_config_migration(config)
        self.assertEqual(plan.config["publication"]["mode"], "local")
        self.assertEqual(plan.config["publication"]["provider"], "")
        self.assertEqual(plan.config["publication"]["config_path"], "")
        self.assertEqual(plan_config_migration(plan.config).changed_paths, ())

    def test_unsupported_publication_target_is_reported_without_public_action(self) -> None:
        config = self.old_config()
        config["publication"] = {
            "base_url": "https://example.invalid/papers",
            "provider": "github-pages",
            "config_path": "deploy.yml",
        }
        plan = plan_config_migration(config)
        self.assertEqual(plan.config["publication"]["mode"], "local")
        self.assertEqual(
            plan.reported_paths,
            ("publication.base_url", "publication.provider", "publication.config_path"),
        )

    def test_cloudflare_publication_rejects_path_traversal(self) -> None:
        config = self.old_config()
        config["publication"] = {
            "base_url": "https://example.invalid/papers",
            "target": "cloudflare",
            "config_path": "../wrangler.toml",
        }
        with self.assertRaisesRegex(ValueError, "workspace-relative"):
            plan_config_migration(config)

    def test_unsupported_values_are_reported_and_not_copied(self) -> None:
        config = self.old_config()
        config["topic_profiles"] = {"example_topic": {"title": "Example", "accent": "#123"}}
        config["unrelated"] = {"token": "must-not-survive"}
        plan = plan_config_migration(config)
        self.assertEqual(plan.reported_paths, ("topic_profiles.example_topic.accent", "unrelated"))
        self.assertNotIn("unrelated", plan.config)
        self.assertEqual(plan.config["topic_profiles"]["example_topic"], {"title": "Example"})

    def test_missing_review_selection_is_a_clear_secret_safe_error(self) -> None:
        config = self.old_config()
        del config["anthropic_auth"]
        config["anthropic_api_key"] = "secret"
        plan = plan_config_migration(config)
        self.assertEqual(plan.config["core"]["review"]["provider"], "anthropic-api")
        self.assertEqual(plan.config["core"]["review"]["model"], "claude-sonnet-5")
        del config["anthropic_api_key"]
        with self.assertRaisesRegex(ValueError, "core.review.provider cannot be migrated"):
            plan_config_migration(config)

    def test_anthropic_model_is_preserved_without_previewing_its_value(self) -> None:
        config = self.old_config()
        del config["anthropic_auth"]
        config["anthropic_api_key"] = "never-print-this-api-secret"
        config["anthropic_model"] = "private-selected-model"
        plan = plan_config_migration(config)
        self.assertEqual(plan.config["core"]["review"]["provider"], "anthropic-api")
        self.assertEqual(plan.config["core"]["review"]["model"], "private-selected-model")
        self.assertIn("core.review.model", plan.changed_paths)
        self.assertNotIn("anthropic_model", plan.reported_paths)

    def test_local_model_requires_and_preserves_an_explicit_model(self) -> None:
        config = self.old_config()
        del config["anthropic_auth"]
        config["local_model"] = {
            "base_url": "http://localhost:11434/v1",
            "model": "qwen2.5:7b-instruct",
        }
        plan = plan_config_migration(config)
        self.assertEqual(plan.config["core"]["review"], {
            "provider": "local-model",
            "model": "qwen2.5:7b-instruct",
            "local_endpoint": "http://localhost:11434/v1",
        })
        del config["local_model"]["model"]
        with self.assertRaisesRegex(
            ValueError,
            r"core\.review\.model cannot be migrated; set local_model\.model",
        ):
            plan_config_migration(config)

    def test_invalid_explicit_anthropic_model_has_a_path_only_error(self) -> None:
        config = self.old_config()
        config["anthropic_model"] = {"value": "do-not-print-this-model"}
        with self.assertRaisesRegex(
            ValueError,
            r"core\.review\.model cannot be migrated; set anthropic_model",
        ) as raised:
            plan_config_migration(config)
        self.assertNotIn("do-not-print-this-model", str(raised.exception))

    def test_backup_collision_refuses_replacement(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "config.json"
            path.write_text(json.dumps(self.old_config()), encoding="utf-8")
            backup = path.parent / "config.json.pre-migration.bak"
            backup.write_bytes(b"existing backup")
            before = path.read_bytes()
            with self.assertRaises(ConfigError):
                execute_config_migration(path, load_config_migration(path))
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(backup.read_bytes(), b"existing backup")


if __name__ == "__main__":
    unittest.main()
