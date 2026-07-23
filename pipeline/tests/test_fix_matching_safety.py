"""Safety contracts for mismatch recovery output and dry-run behavior."""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import fix_matching  # noqa: E402


class FixMatchingSafetyTests(unittest.TestCase):
    def test_dry_run_writes_no_backup_and_prints_safe_followup(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            papers = root / "papers"
            slug = "001_Test_Paper"
            (papers / slug).mkdir(parents=True)
            review = papers / slug / "review.md"
            review.write_text("keep me", encoding="utf-8")
            topic_dir = root / "topic"
            output = io.StringIO()

            with (
                patch.object(fix_matching, "PAPERS_DIR", papers),
                patch.object(
                    fix_matching,
                    "load_index",
                    return_value=[{"slug": slug, "topics": ["ai4s"]}],
                ),
                patch.object(fix_matching, "get_topic_dir", return_value=topic_dir),
                redirect_stdout(output),
            ):
                result = fix_matching._run_fix_matching(
                    "ai4s", slugs="001", execute=False
                )

            self.assertIsNone(result["backup_path"])
            self.assertFalse(topic_dir.exists())
            self.assertTrue(review.exists())
            text = output.getvalue()
            self.assertIn("Backup list    : not written (dry-run)", text)
            self.assertIn("PAPER_CURATION_NO_DEPLOY=1", text)
            self.assertIn("--mode rebuild", text)
            self.assertIn("--no-deploy --yes", text)


if __name__ == "__main__":
    unittest.main()
