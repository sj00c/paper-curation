"""Contracts for the real system probe adapter used by doctor."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from paper_curation.config.models import AppConfig
from paper_curation.integrations.diagnostics import SystemDiagnosticsProbes


def config_for(*, sqlite_path: str = "/workspace/source.sqlite") -> AppConfig:
    return AppConfig.from_mapping({
        "workspace": {"root": "~/workspace"},
        "source": {
            "provider": "zotero",
            "transport": "local-sqlite",
            "sqlite_path": sqlite_path,
            "collections": {"scope": "Collection"},
        },
        "core": {"review": {"provider": "anthropic-api", "model": "configured-model"}},
        "features": {},
        "credentials": {},
        "search_keywords": {},
        "topic_profiles": {},
        "publication": {"mode": "local", "base_url": ""},
    })


class RecordingFilesystem:
    """Record probed paths so tilde expansion is observable without touching HOME."""

    def __init__(self) -> None:
        self.probed: list[Path] = []

    def exists(self, location) -> bool:
        self.probed.append(Path(location))
        return True

    def access(self, location, mode) -> bool:
        self.probed.append(Path(location))
        return True


class WorkspaceProbeExpansionTest(unittest.TestCase):
    def test_workspace_probes_expand_tilde_before_checking(self) -> None:
        filesystem = RecordingFilesystem()
        probes = SystemDiagnosticsProbes(
            config=config_for(),
            environment={},
            path_exists=filesystem.exists,
            path_access=filesystem.access,
        )

        readable = probes.workspace_readable("~/workspace")
        writable = probes.workspace_writable("~/workspace")

        self.assertTrue(readable.ready)
        self.assertTrue(writable.ready)
        expanded = Path("~/workspace").expanduser()
        self.assertEqual(filesystem.probed, [expanded] * 4)
        for probed in filesystem.probed:
            self.assertNotIn("~", str(probed))

    def test_local_sqlite_source_probe_expands_tilde(self) -> None:
        filesystem = RecordingFilesystem()
        probes = SystemDiagnosticsProbes(
            config=config_for(sqlite_path="~/library/zotero.sqlite"),
            environment={},
            path_exists=filesystem.exists,
            path_access=filesystem.access,
        )

        result = probes.source_ready("local-sqlite", network=False)

        self.assertTrue(result.ready)
        self.assertEqual(filesystem.probed, [Path("~/library/zotero.sqlite").expanduser()])


if __name__ == "__main__":
    unittest.main()
