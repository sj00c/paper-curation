import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PIPELINE = Path(__file__).resolve().parents[1]
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

import prepare_deploy  # noqa: E402


class PrepareDeployScopeTests(unittest.TestCase):
    def test_unrequested_topic_directory_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs = Path(temp_dir)
            for topic in ("robotics-lab", "historical-local"):
                topic_dir = docs / topic
                topic_dir.mkdir()
                (topic_dir / "index.html").write_text("ok", encoding="utf-8")
            (docs / ".assetsignore").write_text("", encoding="utf-8")

            with patch.object(prepare_deploy, "DOCS_DIR", docs):
                with self.assertRaisesRegex(SystemExit, "historical-local"):
                    prepare_deploy._assert_requested_topic_scope(["robotics-lab"])

    def test_assetsignore_exclusion_makes_requested_scope_explicit(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            docs = Path(temp_dir)
            for topic in ("robotics-lab", "historical-local"):
                topic_dir = docs / topic
                topic_dir.mkdir()
                (topic_dir / "index.html").write_text("ok", encoding="utf-8")
            (docs / ".assetsignore").write_text("historical-local/\n", encoding="utf-8")

            with patch.object(prepare_deploy, "DOCS_DIR", docs):
                self.assertEqual(
                    prepare_deploy._assert_requested_topic_scope(["robotics-lab"]),
                    ["robotics-lab"],
                )


if __name__ == "__main__":
    unittest.main()
