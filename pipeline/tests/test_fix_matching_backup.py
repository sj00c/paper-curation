import tempfile
import unittest
import sys
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE))
import fix_matching  # noqa: E402


class FixMatchingBackupTests(unittest.TestCase):
    def test_execute_copies_every_artifact_before_removal(self):
        with tempfile.TemporaryDirectory() as tmp:
            papers = Path(tmp) / "papers"
            slug = "001_example"
            source = papers / slug
            (source / "figures").mkdir(parents=True)
            (source / "review.md").write_text("review", encoding="utf-8")
            (source / "text.md").write_text("text", encoding="utf-8")
            (source / "index.html").write_text("html", encoding="utf-8")
            (source / "figures" / "figure.webp").write_bytes(b"figure")
            backup = Path(tmp) / "recovery"

            with patch.object(fix_matching, "PAPERS_DIR", papers):
                removed = fix_matching.delete_slug_artifacts(
                    slug, dry_run=False, backup_root=backup)

            self.assertEqual(len(removed), 4)
            self.assertFalse((source / "review.md").exists())
            self.assertEqual(
                (backup / slug / "review.md").read_text(encoding="utf-8"),
                "review",
            )
            self.assertEqual(
                (backup / slug / "figures" / "figure.webp").read_bytes(),
                b"figure",
            )

    def test_execute_requires_a_backup_destination(self):
        with self.assertRaises(ValueError):
            fix_matching.delete_slug_artifacts("001_example", dry_run=False)


if __name__ == "__main__":
    unittest.main()
