"""Timeline images are optional, but partial image sets must stay consistent."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


PIPELINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE))

import validate_papers


class TimelineValidationTests(unittest.TestCase):
    def _topic(self, root: Path) -> None:
        (root / "_new_classification.json").write_text(
            json.dumps({
                "categories": [
                    {"name": "01 First Category"},
                    {"name": "02 Second Category"},
                ]
            }),
            encoding="utf-8",
        )

    def test_no_images_means_optional_image_feature_is_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            topic_dir = Path(temporary)
            self._topic(topic_dir)
            with patch.object(validate_papers, "get_topic_dir", return_value=topic_dir):
                self.assertEqual(validate_papers.check_timeline_mismatch("topic"), [])

    def test_partial_image_set_reports_missing_categories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            topic_dir = Path(temporary)
            self._topic(topic_dir)
            (topic_dir / "category_timeline_01_First_Category.png").write_bytes(b"png")
            with patch.object(validate_papers, "get_topic_dir", return_value=topic_dir):
                issues = validate_papers.check_timeline_mismatch("topic")
            self.assertEqual(
                issues,
                ["  [timeline] MISSING image for category slug: 02_Second_Category"],
            )


if __name__ == "__main__":
    unittest.main()
