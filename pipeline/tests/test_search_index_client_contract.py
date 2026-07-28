import json
import tempfile
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIPELINE = ROOT / "pipeline"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))

from pipeline.lib import search_index_metadata as metadata  # noqa: E402
from pipeline import query_search_index  # noqa: E402
from pipeline import serve_local  # noqa: E402


class SearchIndexClientContractTests(unittest.TestCase):
    def test_current_metadata_keeps_document_and_query_tasks_distinct(self):
        current = metadata.current_index_metadata()
        self.assertEqual(current[metadata.KEY_EMBEDDING_TASK_TYPE], "RETRIEVAL_DOCUMENT")
        self.assertEqual(serve_local.QUERY_TASK_TYPE, "RETRIEVAL_QUERY")
        self.assertEqual(serve_local.EMBED_DIM, current[metadata.KEY_EMBEDDING_DIMENSION])

    def test_generated_local_dashboard_has_no_browser_embedding_or_provider_path(self):
        builder = (PIPELINE / "build_topic_index.py").read_text(encoding="utf-8")
        runtime = (ROOT / "docs/public/paper-curation-local.js").read_text(encoding="utf-8")
        combined = (builder + runtime).lower()
        self.assertNotIn("/api/embed", combined)
        self.assertNotIn("generativelanguage.googleapis.com", combined)
        self.assertNotIn("localstorage", combined)
        self.assertIn("/api/action/plan", runtime)

    def test_local_server_does_not_expose_legacy_embedding_effect(self):
        self.assertFalse(hasattr(serve_local, "gemini_embed"))
        source = Path(serve_local.__file__).read_text(encoding="utf-8")
        self.assertNotIn("embedContent", source)
        self.assertNotIn('path == "/api/embed"', source)

    def test_metadata_mismatch_downgrades_to_lexical_without_provider(self):
        payload = {
            "chunks": [{"id": "c1", "text": "safe lexical evidence", "parent_id": "p1"}],
            "embedding_provider": "other",
        }
        with tempfile.TemporaryDirectory() as directory:
            topic = Path(directory) / "safe-topic"
            topic.mkdir()
            (topic / "_search_index.json").write_text(
                json.dumps(payload), encoding="utf-8"
            )
            result = query_search_index.search_index(
                directory,
                "safe-topic",
                "lexical",
                top_k=1,
                candidate_k=1,
                query_vector=[1.0] * metadata.EMBEDDING_DIMENSION,
            )
        self.assertEqual(result["mode"], "lexical_bm25")
        self.assertFalse(result["dense_status"]["enabled"])
        self.assertTrue(result["dense_status"]["reason"])
        self.assertEqual(result["results"][0]["id"], "c1")

    def test_known_safe_legacy_validation_remains_fail_closed(self):
        mixed = {
            **metadata.current_index_metadata(),
            "model": metadata.EMBEDDING_MODEL,
            "dim": metadata.EMBEDDING_DIMENSION,
        }
        result = metadata.validate_known_safe_legacy_index(mixed)
        self.assertFalse(result.ok)
        self.assertTrue(result.errors)


if __name__ == "__main__":
    unittest.main()
