"""Focused tests for resumable Zotero metadata fetching."""

import io
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import config_loader  # noqa: E402

with (
    patch.object(config_loader, "get_zotero_api_key", return_value="test-key"),
    patch.object(config_loader, "get_zotero_user_id", return_value="123"),
    patch.object(config_loader, "get_zotero_dir", return_value="/tmp/paper-curation-cache-test"),
    patch.object(config_loader, "get_collections", return_value={}),
):
    import run_update_force as update  # noqa: E402
cache_path_for = getattr(update, "_zotero_items_cache_path")


class ZoteroMetadataCacheTests(unittest.TestCase):
    def test_fresh_cache_avoids_network_fetch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            payload = {
                "collection_key": "COLLKEY",
                "fetched_at": time.time(),
                "items": [{"key": "ITEM1", "title": "Cached paper"}],
            }
            cache_path = Path(temp_dir) / "zotero_items_COLLKEY.json"
            cache_path.write_text(json.dumps(payload), encoding="utf-8")
            with (
                patch.object(update, "_ZOTERO_ITEMS_CACHE_DIR", temp_dir),
                patch.object(
                    update.urllib.request,
                    "urlopen",
                    side_effect=AssertionError("network should not be used"),
                ),
            ):
                items = update.fetch_zotero_items("COLLKEY")

        self.assertEqual(items, payload["items"])

    def test_network_fetch_is_saved_for_resume(self):
        response = io.BytesIO(json.dumps([
            {"data": {"key": "ITEM1", "title": "Fetched paper", "itemType": "journalArticle"}},
        ]).encode("utf-8"))
        with tempfile.TemporaryDirectory() as temp_dir:
            with (
                patch.object(update, "_ZOTERO_ITEMS_CACHE_DIR", temp_dir),
                patch.object(update.urllib.request, "urlopen", return_value=response),
            ):
                items = update.fetch_zotero_items("COLLKEY")
                cache_path = Path(cache_path_for("COLLKEY"))
                saved = json.loads(cache_path.read_text(encoding="utf-8"))

        self.assertEqual(items, [{"key": "ITEM1", "title": "Fetched paper", "itemType": "journalArticle"}])
        self.assertEqual(saved["collection_key"], "COLLKEY")
        self.assertEqual(saved["items"], items)


if __name__ == "__main__":
    unittest.main()
