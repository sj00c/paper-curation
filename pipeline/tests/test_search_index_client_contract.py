import json
import unittest
from unittest import mock
from pathlib import Path

from pipeline.lib import search_index_metadata as meta


ROOT = Path(__file__).resolve().parents[2]
BUILD_TOPIC_INDEX = ROOT / "pipeline" / "build_topic_index.py"
WORKER_INDEX = ROOT / "worker" / "index.js"
from pipeline import serve_local

APPROVED_CANONICAL_KEYS = [
    "index_schema_version",
    "embedding_provider",
    "embedding_model",
    "embedding_task_type",
    "embedding_dimension",
    "embedding_quantization",
    "chunk_hash_basis",
    "sidecar_format_version",
    "cache_format_version",
    "source_provenance_approval_status",
]
LEGACY_SHORT_RESPONSE_KEYS = {"provider", "model", "task_type", "dim"}


class SearchIndexClientContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build_src = BUILD_TOPIC_INDEX.read_text(encoding="utf-8")
        cls.worker_src = WORKER_INDEX.read_text(encoding="utf-8")

    def test_generated_client_renders_authoritative_current_metadata(self):
        src = self.build_src
        for name in [
            "INDEX_SCHEMA_VERSION",
            "EMBEDDING_PROVIDER",
            "EMBEDDING_MODEL",
            "EMBEDDING_TASK_TYPE",
            "EMBEDDING_DIMENSION",
            "EMBEDDING_QUANTIZATION",
            "CHUNK_HASH_BASIS",
            "SIDECAR_FORMAT_VERSION",
            "CACHE_FORMAT_VERSION",
            "PROVENANCE_STATUS",
            "EMBEDDING_SIDECAR_FILE",
            "REBUILD_GUIDANCE",
        ]:
            self.assertIn(name, src)
        self.assertIn("window._DEEP_INDEX_TASK_TYPE", src)
        self.assertIn("deepValidateIndexMetadata", src)
        for key in APPROVED_CANONICAL_KEYS:
            self.assertIn(key, src)
        self.assertIn("index_schema_version: DEEP_INDEX_SCHEMA_VERSION", src)
        self.assertIn("embedding_provider: DEEP_EMBED_PROVIDER", src)
        self.assertIn("embedding_task_type: DEEP_INDEX_TASK_TYPE", src)
        self.assertIn("cache_format_version: DEEP_CACHE_FORMAT_VERSION", src)
        self.assertNotIn("\n        provider: DEEP_EMBED_PROVIDER", src)
        self.assertNotIn("\n        task_type: DEEP_INDEX_TASK_TYPE", src)

    def test_known_safe_legacy_is_readable_only_for_matching_old_fields(self):
        src = self.build_src
        worker = self.worker_src
        for haystack in (src, worker):
            self.assertIn("mixed canonical and legacy metadata is not known-safe legacy", haystack)
            self.assertIn("partial canonical metadata is not known-safe legacy", haystack)
            self.assertIn("partial versioned metadata is not known-safe legacy", haystack)
            self.assertIn("shortened versioned metadata is not known-safe legacy", haystack)
        self.assertIn("deepValidateKnownSafeLegacyIndex", src)
        self.assertIn("index.model !== DEEP_EMBED_MODEL", src)
        self.assertIn("index.dim !== DEEP_EMBED_DIM", src)
        self.assertIn("index.quant !== DEEP_EMBED_QUANT", src)


    def test_generated_client_rejects_mixed_shape_before_normalizing_for_worker(self):
        src = self.build_src
        self.assertIn("deepContractShapeError(index, expected)", src)
        self.assertIn("const validation = deepValidateIndexMetadata(index);", src)
        self.assertIn("const source = validation.ok ? (validation.normalized || index || {}) : {};", src)
        shape_check = src.index("const shapeError = deepContractShapeError(index, expected);")
        self.assertLess(shape_check, src.index("for (const k in expected)", shape_check))
        self.assertLess(
            src.index("const validation = deepValidateIndexMetadata(index);"),
            src.index("const source = validation.ok ? (validation.normalized || index || {}) : {};"),
        )

    def test_worker_direct_embed_request_rejects_mixed_shape_before_embedding(self):
        worker = self.worker_src
        self.assertIn("contractShapeError(payload, expected)", worker)
        self.assertIn("mixed canonical and legacy metadata is not known-safe legacy", worker)
        shape_check = worker.index("const shapeError = contractShapeError(payload, expected);")
        self.assertLess(shape_check, worker.index("for (const key of Object.keys(expected))", shape_check))
        self.assertLess(
            worker.index("validateIndexMetadata(body && body.index_metadata)"),
            worker.index("fetch(apiUrl"),
        )
    def test_mismatch_disables_dense_and_keeps_bm25_fallback(self):
        src = self.build_src
        self.assertIn("deepDisableDense('Search index metadata is incompatible:", src)
        self.assertIn("BM25 only", src)
        self.assertIn("buildBM25(DEEP.index)", src)
        self.assertIn("const useDense = deepDenseAvailable() && queryVec", src)
        self.assertIn("let sc = 0;", src)

    def test_sidecar_version_and_byte_length_mismatch_disable_dense(self):
        src = self.build_src
        self.assertIn("sidecar_format_version", src)
        self.assertIn("DEEP_SIDECAR_FORMAT_VERSION", src)
        self.assertIn("Embedding sidecar byte length expected", src)
        self.assertIn("deepDisableDense(e && e.message || e)", src)

    def test_no_automatic_index_build_call_from_consumers(self):
        combined = self.build_src + "\n" + self.worker_src
        self.assertNotIn("build_search_index(", combined)
        self.assertNotIn("buildSearchIndex(", combined)
        self.assertIn("validation never rebuilds automatically", combined)

    def test_query_and_document_tasks_are_distinct_and_aligned(self):
        src = self.build_src
        worker = self.worker_src
        self.assertEqual(meta.EMBEDDING_TASK_TYPE, "RETRIEVAL_DOCUMENT")
        self.assertIn('json.dumps("RETRIEVAL_QUERY")', src)
        self.assertIn("DEEP_INDEX_TASK_TYPE", src)
        self.assertIn("DEEP_QUERY_TASK_TYPE", src)
        self.assertIn("data.embedding_task_type !== DEEP_QUERY_TASK_TYPE", src)
        self.assertIn('const INDEX_TASK_TYPE = "RETRIEVAL_DOCUMENT";', worker)
        self.assertIn('const QUERY_TASK_TYPE = "RETRIEVAL_QUERY";', worker)
        self.assertIn("taskType: QUERY_TASK_TYPE", worker)
        self.assertIn("embedding_task_type: QUERY_TASK_TYPE", worker)
        self.assertIn("embedding_provider: EMBED_PROVIDER", worker)
        self.assertIn("embedding_model: EMBED_MODEL", worker)
        self.assertIn("embedding_dimension: EMBED_DIM", worker)
        self.assertNotIn("\n    provider: EMBED_PROVIDER", worker)
        self.assertNotIn("\n    model: EMBED_MODEL", worker)
        self.assertNotIn("\n    task_type: QUERY_TASK_TYPE", worker)
        self.assertNotIn("\n    dim: EMBED_DIM", worker)
        self.assertEqual(serve_local.EMBED_PROVIDER, meta.EMBEDDING_PROVIDER)
        self.assertEqual(serve_local.GEMINI_MODEL, meta.EMBEDDING_MODEL)
        self.assertEqual(serve_local.QUERY_TASK_TYPE, "RETRIEVAL_QUERY")
        self.assertEqual(serve_local.EMBED_DIM, meta.EMBEDDING_DIMENSION)

    def test_worker_constants_match_python_metadata_contract(self):
        worker = self.worker_src
        expected_literals = {
            "INDEX_SCHEMA_VERSION": meta.INDEX_SCHEMA_VERSION,
            "EMBED_PROVIDER": meta.EMBEDDING_PROVIDER,
            "EMBED_MODEL": meta.EMBEDDING_MODEL,
            "INDEX_TASK_TYPE": meta.EMBEDDING_TASK_TYPE,
            "EMBED_DIM": meta.EMBEDDING_DIMENSION,
            "EMBED_QUANT": meta.EMBEDDING_QUANTIZATION,
            "CHUNK_HASH_BASIS": meta.CHUNK_HASH_BASIS,
            "SIDECAR_FORMAT_VERSION": meta.SIDECAR_FORMAT_VERSION,
            "CACHE_FORMAT_VERSION": meta.CACHE_FORMAT_VERSION,
            "PROVENANCE_STATUS": meta.PROVENANCE_STATUS,
            "EMBED_SIDECAR_FILE": meta.EMBEDDING_SIDECAR_FILE,
        }
        for name, value in expected_literals.items():
            literal = json.dumps(value) if isinstance(value, str) else repr(value)
            self.assertIn(f"const {name} = {literal};", worker)

    def test_worker_rejects_incompatible_document_metadata_before_embedding(self):
        worker = self.worker_src
        self.assertIn("validateIndexMetadata(body && body.index_metadata)", worker)
        self.assertIn("Incompatible document index metadata", worker)
        self.assertIn("409", worker)
        self.assertLess(
            worker.index("validateIndexMetadata(body && body.index_metadata)"),
            worker.index("fetch(apiUrl"),
        )
        self.assertIn("x-goog-api-key", worker)
        self.assertNotIn("GOOGLE_API_KEY, detail", worker)

    def test_local_embed_handler_returns_worker_aligned_query_metadata_without_network(self):
        handler = serve_local.LocalHandler.__new__(serve_local.LocalHandler)
        sent = {}

        def send_json(code, obj):
            sent["code"] = code
            sent["obj"] = obj

        handler._read_body = lambda: json.dumps({
            "text": "loopback query",
            "index_metadata": meta.current_index_metadata(),
        }).encode("utf-8")
        handler._send_json = send_json

        vector = [1.0] + [0.0] * (meta.EMBEDDING_DIMENSION - 1)
        with mock.patch.object(serve_local, "resolve_google_key", return_value="test-google-key"), \
             mock.patch.object(serve_local, "gemini_embed", return_value=vector) as embed:
            serve_local.LocalHandler._handle_embed(handler)

        self.assertEqual(sent["code"], 200)
        self.assertEqual(sent["obj"]["embedding"], vector)
        self.assertEqual(sent["obj"]["embedding_provider"], meta.EMBEDDING_PROVIDER)
        self.assertEqual(sent["obj"]["embedding_model"], meta.EMBEDDING_MODEL)
        self.assertEqual(sent["obj"]["embedding_task_type"], "RETRIEVAL_QUERY")
        self.assertEqual(sent["obj"]["embedding_dimension"], meta.EMBEDDING_DIMENSION)
        self.assertFalse(LEGACY_SHORT_RESPONSE_KEYS.intersection(sent["obj"]))
        self.assertEqual(len(sent["obj"]["embedding"]), meta.EMBEDDING_DIMENSION)
        embed.assert_called_once_with("loopback query", "test-google-key")

    def test_local_embed_handler_rejects_incompatible_document_metadata_before_embedding(self):
        handler = serve_local.LocalHandler.__new__(serve_local.LocalHandler)
        sent = {}

        def send_json(code, obj):
            sent["code"] = code
            sent["obj"] = obj

        bad_metadata = dict(meta.current_index_metadata())
        bad_metadata["embedding_dimension"] = meta.EMBEDDING_DIMENSION + 1
        handler._read_body = lambda: json.dumps({
            "text": "loopback query",
            "index_metadata": bad_metadata,
        }).encode("utf-8")
        handler._send_json = send_json

        with mock.patch.object(serve_local, "resolve_google_key", return_value="test-google-key"), \
             mock.patch.object(serve_local, "gemini_embed") as embed:
            serve_local.LocalHandler._handle_embed(handler)

        self.assertEqual(sent["code"], 409)
        self.assertEqual(sent["obj"]["error"], "Incompatible document index metadata")
        self.assertIn("embedding_dimension expected", sent["obj"]["detail"])
        embed.assert_not_called()

    def test_local_embed_handler_rejects_mixed_document_metadata_through_shared_validator(self):
        handler = serve_local.LocalHandler.__new__(serve_local.LocalHandler)
        sent = {}

        def send_json(code, obj):
            sent["code"] = code
            sent["obj"] = obj

        mixed_metadata = {
            **meta.current_index_metadata(),
            "provider": meta.EMBEDDING_PROVIDER,
        }
        handler._read_body = lambda: json.dumps({
            "text": "loopback query",
            "index_metadata": mixed_metadata,
        }).encode("utf-8")
        handler._send_json = send_json

        with mock.patch.object(serve_local, "resolve_google_key", return_value="test-google-key"), \
             mock.patch.object(serve_local, "gemini_embed") as embed:
            serve_local.LocalHandler._handle_embed(handler)

        self.assertEqual(sent["code"], 409)
        self.assertEqual(sent["obj"]["error"], "Incompatible document index metadata")
        self.assertIn("shortened versioned metadata is not known-safe legacy", sent["obj"]["detail"])
        embed.assert_not_called()

    def test_local_embed_handler_rejects_wrong_embedding_dimension(self):
        handler = serve_local.LocalHandler.__new__(serve_local.LocalHandler)
        sent = {}

        def send_json(code, obj):
            sent["code"] = code
            sent["obj"] = obj

        handler._read_body = lambda: json.dumps({
            "text": "loopback query",
            "index_metadata": meta.current_index_metadata(),
        }).encode("utf-8")
        handler._send_json = send_json

        with mock.patch.object(serve_local, "resolve_google_key", return_value="test-google-key"), \
             mock.patch.object(serve_local, "gemini_embed", return_value=[1.0]):
            serve_local.LocalHandler._handle_embed(handler)

        self.assertEqual(sent["code"], 502)
        self.assertIn("dimension mismatch", sent["obj"]["error"])


if __name__ == "__main__":
    unittest.main()
