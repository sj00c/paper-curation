"""Contract tests for the explicit local config migration command."""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
import stat

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
                "collections": {"research": "Research Collection"},
            },
            "unrelated": {"preserve": ["this", "exactly"]},
        }

    def test_old_config_preview_is_typed_and_only_lists_paths(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "config.json"
            path.write_text(json.dumps(self.old_config()), encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(main(["migrate", "--config", str(path)]), 0)
            self.assertEqual(
                output.getvalue().splitlines(),
                [
                    "search_keywords.research",
                    "topic_profiles.research.title",
                    "publication.mode",
                    "publication.base_url",
                ],
            )
            self.assertNotIn("never-print-this-secret", output.getvalue())
            self.assertFalse((path.parent / "config.json.pre-migration.bak").exists())

    def test_execute_creates_exact_backup_and_loadable_atomic_result(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "config.json"
            original = b'{\n  "zotero": {"collections": {"research": "Research Collection"}}\n}\n'
            path.write_bytes(original)
            self.assertEqual(main(["migrate", "--config", str(path), "--execute"]), 0)
            backup = path.parent / "config.json.pre-migration.bak"
            self.assertEqual(backup.read_bytes(), original)
            self.assertEqual(stat.S_IMODE(backup.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertEqual(AppConfig.from_mapping(json.loads(path.read_text(encoding="utf-8"))).publication.mode, "local")

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

    def test_execute_hardens_a_read_only_source_config(self) -> None:
        with TemporaryDirectory() as temporary:
            path = Path(temporary) / "config.json"
            path.write_text(json.dumps(self.old_config()), encoding="utf-8")
            path.chmod(0o444)
            execute_config_migration(path, load_config_migration(path))
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    def test_existing_customizations_and_unknown_values_are_preserved(self) -> None:
        config = self.old_config()
        config.update(
            {
                "search_keywords": {"research": {"primary": ["custom"], "secondary": ["kept"], "extra": 1}},
                "topic_profiles": {"research": {"title": "Custom title", "accent": "#123"}},
                "publication": {"mode": "local", "base_url": "", "target": "keep"},
            }
        )
        planned = plan_config_migration(config)
        self.assertEqual(planned.config["search_keywords"], config["search_keywords"])
        self.assertEqual(planned.config["topic_profiles"], config["topic_profiles"])
        self.assertEqual(planned.config["unrelated"], config["unrelated"])

    def test_malformed_collections_are_rejected(self) -> None:
        with self.assertRaises((ConfigError, ValueError)):
            plan_config_migration({"zotero": {"collections": {"topic": 7}}})

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
