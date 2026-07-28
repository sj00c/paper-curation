import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import sync_zotero  # noqa: E402


class SyncZoteroSecurityTests(unittest.TestCase):
    def test_slug_path_is_confined_to_papers_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(
                sync_zotero._safe_slug_dir(root, "001_safe"),
                root.resolve() / "001_safe",
            )
            for slug in ("", ".", "..", "../outside", "nested/outside", "nested\\outside", "bad\x00slug"):
                with self.subTest(slug=slug), self.assertRaises(RuntimeError):
                    sync_zotero._safe_slug_dir(root, slug)

    def test_symlink_slug_is_rejected_without_touching_target(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            target = Path(outside) / "sentinel"
            target.write_text("keep", encoding="utf-8")
            (root / "linked").symlink_to(Path(outside), target_is_directory=True)
            with self.assertRaises(RuntimeError):
                sync_zotero._safe_slug_dir(root, "linked")
            self.assertEqual(target.read_text(encoding="utf-8"), "keep")

    def test_force_delete_bypass_is_rejected_before_lookup(self):
        with self.assertRaisesRegex(ValueError, "unsupported"):
            sync_zotero._run_sync("any-topic", force_delete=True)

    def test_atomic_index_write_preserves_original_on_replace_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            index = root / "_papers_index.json"
            index.write_text('[{"slug":"old"}]\n', encoding="utf-8")
            with patch.object(sync_zotero.os, "replace", side_effect=OSError("synthetic crash")):
                with self.assertRaisesRegex(OSError, "synthetic crash"):
                    sync_zotero._atomic_write_json(index, [{"slug": "new"}])
            self.assertEqual(index.read_text(encoding="utf-8"), '[{"slug":"old"}]\n')
            self.assertEqual(list(root.glob(".*.tmp")), [])

    def test_atomic_index_write_rejects_symlink_destination(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            target = Path(outside) / "index.json"
            target.write_text("sentinel", encoding="utf-8")
            link = root / "_papers_index.json"
            link.symlink_to(target)
            with self.assertRaisesRegex(RuntimeError, "symlink"):
                sync_zotero._atomic_write_json(link, [])
            self.assertEqual(target.read_text(encoding="utf-8"), "sentinel")


if __name__ == "__main__":
    unittest.main()
