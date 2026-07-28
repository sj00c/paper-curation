import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pipeline import query_search_index as search
from pipeline.lib import search_index_metadata as meta


class QuerySearchIndexTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name) / "docs"
        self.root.mkdir()
        self.topic = self.root / "topic"
        self.topic.mkdir()

    def tearDown(self):
        self.tempdir.cleanup()

    def write_index(self, *, canonical=True, sidecar=True, sidecar_size=None):
        chunks = [
            {"slug": "one", "section": "abstract", "text": "alpha beta", "citation": "C1", "figures": ["f1"], "notes": "n1", "parent_id": "p1", "source_id": "s1", "chunk_id": "c1"},
            {"slug": "two", "section": "results", "text": "beta gamma", "citation": "C2"},
        ]
        index = {
            "count": len(chunks), "chunks": chunks,
            "papers": [{"slug": "two", "notes": "paper note", "parent": "paper parent"}],
        }
        if canonical:
            index.update(meta.current_index_metadata())
        else:
            index.update({"model": meta.EMBEDDING_MODEL, "dim": meta.EMBEDDING_DIMENSION, "quant": meta.EMBEDDING_QUANTIZATION})
        (self.topic / "_search_index.json").write_text(json.dumps(index), encoding="utf-8")
        if sidecar:
            payload = bytearray(meta.EMBEDDING_DIMENSION * len(chunks) if sidecar_size is None else sidecar_size)
            payload[0] = 127
            payload[meta.EMBEDDING_DIMENSION + 1] = 127
            (self.topic / meta.EMBEDDING_SIDECAR_FILE).write_bytes(payload)

    def vector(self):
        return [1.0] + [0.0] * (meta.EMBEDDING_DIMENSION - 1)

    def test_lexical_only_preserves_chunk_and_paper_fields(self):
        self.write_index()
        result = search.search_index(self.root, "topic", "alpha", top_k=1, candidate_k=2)
        self.assertEqual(result["mode"], "lexical_bm25")
        self.assertEqual(result["dense_status"]["reason"], "query_vector not provided")
        self.assertEqual(result["results"][0]["citation"], "C1")
        self.assertEqual(result["results"][0]["figures"], ["f1"])
        self.assertEqual(result["results"][0]["notes"], "n1")
        self.assertEqual(result["results"][0]["parent_id"], "p1")
        self.assertEqual(result["results"][0]["source_id"], "s1")
        self.assertEqual(result["results"][0]["chunk_id"], "c1")

    def test_valid_hybrid_uses_rrf_k_60_and_is_deterministic(self):
        self.write_index()
        first = search.search_index(self.root, "topic", "alpha", top_k=2, candidate_k=2, query_vector=self.vector())
        second = search.search_index(self.root, "topic", "alpha", top_k=2, candidate_k=2, query_vector=self.vector())
        self.assertEqual(first, second)
        self.assertEqual(first["mode"], "hybrid_rrf")
        self.assertEqual(first["rrf_k"], 60)
        self.assertTrue(first["dense_status"]["enabled"])
        self.assertAlmostEqual(first["results"][0]["score"], 2 / 61)

    def test_invalid_or_legacy_metadata_downgrades_without_rebuild(self):
        self.write_index()
        payload = json.loads((self.topic / "_search_index.json").read_text())
        payload["embedding_model"] = "wrong"
        (self.topic / "_search_index.json").write_text(json.dumps(payload))
        result = search.search_index(self.root, "topic", "alpha", top_k=1, candidate_k=2, query_vector=self.vector())
        self.assertEqual(result["mode"], "lexical_bm25")
        self.assertIn("metadata invalid", result["dense_status"]["reason"])
        self.write_index(canonical=False)
        result = search.search_index(self.root, "topic", "alpha", top_k=1, candidate_k=2, query_vector=self.vector())
        self.assertIn("legacy", result["dense_status"]["reason"])

    def test_bounds_traversal_and_symlinks_are_refused(self):
        self.write_index()
        for top_k, candidate_k in ((0, 1), (2, 1), (1, 101)):
            with self.assertRaises(search.SearchRequestError):
                search.search_index(self.root, "topic", "alpha", top_k=top_k, candidate_k=candidate_k)
        with self.assertRaises(search.SearchRequestError):
            search.search_index(self.root, "../topic", "alpha")
        target = self.root / "real.json"
        target.write_text("{}")
        (self.topic / "_search_index.json").unlink()
        os.symlink(target, self.topic / "_search_index.json")
        with self.assertRaises(search.SearchRequestError):
            search.search_index(self.root, "topic", "alpha")

    def test_search_is_read_only_and_never_invokes_provider(self):
        self.write_index()
        before = {path.name: path.read_bytes() for path in self.topic.iterdir()}
        with patch("urllib.request.urlopen", side_effect=AssertionError("network must not run")):
            result = search.search_index(self.root, "topic", "alpha", top_k=1, candidate_k=2)
        after = {path.name: path.read_bytes() for path in self.topic.iterdir()}
        self.assertEqual(before, after)
        self.assertEqual(result["results"][0]["slug"], "one")


if __name__ == "__main__":
    unittest.main()
