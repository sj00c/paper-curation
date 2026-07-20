"""Focused tests for first-run doctor artifact reporting."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import doctor as doctor_module  # noqa: E402


class DoctorFirstRunTests(unittest.TestCase):
    def test_missing_topic_directory_is_warning_before_first_run(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            reporter = doctor_module.Reporter()
            with (
                patch.object(doctor_module, "DOCS_DIR", root / "docs"),
                patch.object(
                    doctor_module,
                    "PAPERS_INDEX",
                    root / "docs" / "papers" / "_papers_index.json",
                ),
            ):
                doctor_module.check_topic(
                    reporter,
                    "ai4s",
                    {"zotero": {"collections": {"ai4s": "AI for Science"}}},
                    None,
                )

        self.assertEqual(reporter.fails, 0)
        self.assertEqual(reporter.warns, 1)

    def test_missing_topic_directory_fails_after_index_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            papers_index = root / "docs" / "papers" / "_papers_index.json"
            papers_index.parent.mkdir(parents=True)
            papers_index.write_text("[]", encoding="utf-8")
            reporter = doctor_module.Reporter()
            with (
                patch.object(doctor_module, "DOCS_DIR", root / "docs"),
                patch.object(doctor_module, "PAPERS_INDEX", papers_index),
            ):
                doctor_module.check_topic(
                    reporter,
                    "ai4s",
                    {"zotero": {"collections": {"ai4s": "AI for Science"}}},
                    [],
                )

        self.assertEqual(reporter.fails, 1)
        self.assertEqual(reporter.warns, 0)


if __name__ == "__main__":
    unittest.main()
