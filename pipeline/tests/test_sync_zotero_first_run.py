"""Regression test for syncing before the master index exists."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import sync_zotero as sync_module  # noqa: E402


class SyncZoteroFirstRunTests(unittest.TestCase):
    def test_missing_master_index_is_treated_as_empty_first_run(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            papers_dir = Path(temp_dir) / "docs" / "papers"
            with (
                patch.object(sync_module, "PAPERS_DIR", str(papers_dir)),
                patch.object(sync_module, "COLLECTIONS", {"ai4s": "COLLKEY"}),
                patch.object(sync_module, "fetch_zotero_items", return_value=[]),
            ):
                sync_module._run_sync("ai4s")

            self.assertTrue(papers_dir.is_dir())
            self.assertFalse((papers_dir / "_papers_index.json").exists())


if __name__ == "__main__":
    unittest.main()
