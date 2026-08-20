"""Contract tests for the explicit, secret-safe setup use case."""

from __future__ import annotations

import os
from pathlib import Path
import stat
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from paper_curation.application.setup import SetupUseCase, plan_setup
from paper_curation.config.loader import load_config
from paper_curation.config.models import AppConfig
from paper_curation.integrations.persistence.configuration import FilesystemConfigWriter


def config_for(workspace: Path, secret: str = "never-print-this-secret") -> AppConfig:
    return AppConfig.from_mapping({
        "workspace": {"root": str(workspace)},
        "source": {
            "provider": "zotero",
            "transport": "zotero-storage",
            "collections": {"demo": "Demo Collection"},
            "sqlite_path": "",
        },
        "core": {"review": {"provider": "claude-code-oauth", "model": "configured-model", "local_endpoint": ""}},
        "features": {"dense_search": {"enabled": False, "provider": ""}},
        "credentials": {
            "zotero_api_key": secret,
            "anthropic_api_key": "",
            "google_api_key": "",
            "gemini_api_key": "",
            "openai_api_key": "",
        },
        "search_keywords": {"demo": {"primary": ["demo"], "secondary": []}},
        "topic_profiles": {"demo": {"title": "Demo"}},
        "publication": {"mode": "local", "base_url": ""},
        "operator": {"name": "", "organization": "", "email": ""},
        "notifications": {"completion_email": ""},
    })


class _UnexpectedWriter:
    def write(self, plan):  # type: ignore[no-untyped-def]
        raise AssertionError("preview must not write")


class SetupUseCaseTests(unittest.TestCase):
    def test_preview_does_not_write_and_hides_credentials(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            secret = "never-print-this-secret"
            plan = SetupUseCase(_UnexpectedWriter()).preview(config_for(root / "work", secret), root / "config.json")
            self.assertFalse((root / "config.json").exists())
            self.assertFalse((root / "work").exists())
            self.assertNotIn(secret, repr(plan))

    def test_first_setup_writes_private_loadable_config_and_workspace(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "work"
            target = root / "config" / "config.json"
            result = SetupUseCase(FilesystemConfigWriter()).execute(
                plan_setup(config_for(workspace), target)
            )
            self.assertEqual(result.target_path, target)
            self.assertIsNone(result.backup_path)
            self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
            self.assertEqual(load_config(target), config_for(workspace))
            for directory in (workspace, workspace / "papers", workspace / ".cache"):
                self.assertTrue(directory.is_dir())

    def test_existing_config_requires_explicit_replace(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "config.json"
            original = b"original configuration"
            target.write_bytes(original)
            with self.assertRaises(FileExistsError):
                SetupUseCase(FilesystemConfigWriter()).execute(plan_setup(config_for(root / "work"), target))
            self.assertEqual(target.read_bytes(), original)

    def test_replace_creates_private_exact_backup(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "config.json"
            original = b"original configuration\n"
            target.write_bytes(original)
            result = SetupUseCase(FilesystemConfigWriter()).execute(
                plan_setup(config_for(root / "work"), target, replace=True)
            )
            backup = root / "config.json.pre-setup.bak"
            self.assertEqual(result.backup_path, backup)
            self.assertEqual(backup.read_bytes(), original)
            self.assertEqual(stat.S_IMODE(backup.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)

    def test_atomic_replace_failure_preserves_original(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "config.json"
            original = b"original configuration\n"
            target.write_bytes(original)
            with patch("paper_curation.integrations.persistence.configuration.os.replace", side_effect=OSError("blocked")):
                with self.assertRaises(OSError):
                    SetupUseCase(FilesystemConfigWriter()).execute(
                        plan_setup(config_for(root / "work"), target, replace=True)
                    )
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual((root / "config.json.pre-setup.bak").read_bytes(), original)

    def test_results_never_reveal_credentials(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            secret = "never-print-this-secret"
            result = SetupUseCase(FilesystemConfigWriter()).execute(
                plan_setup(config_for(root / "work", secret), root / "config.json")
            )
            self.assertNotIn(secret, repr(result))


if __name__ == "__main__":
    unittest.main()
