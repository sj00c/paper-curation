import base64
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch
from pathlib import Path

from pipeline import build_search_index
from pipeline.lib import search_index_metadata as meta
from pipeline import build_cross_index
from pipeline import doctor as doctor_module
from pipeline import api as pipeline_api


_EMB = base64.b64encode(bytes([7]) * meta.EMBEDDING_DIMENSION).decode("ascii")

APPROVED_CANONICAL_KEYS = {
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
}
SHORTENED_VERSIONED_KEYS = {
    "schema_version",
    "provider",
    "task_type",
    "provenance_status",
}
LEGACY_PREVERSION_KEYS = {
    "model",
    "dim",
    "quant",
}


class SearchIndexMetadataTests(unittest.TestCase):
    def test_current_index_metadata_uses_exact_canonical_contract_keys(self):
        metadata = meta.current_index_metadata()
        payload = {
            **metadata,
            "count": 1,
            "papers": {},
            "chunks": [{"text": "hello", "text_sha": "sha"}],
        }
        result = meta.validate_index_metadata(payload)
        self.assertTrue(result.ok)
        self.assertFalse(result.is_legacy)
        self.assertEqual(set(metadata) - {"emb_file"}, APPROVED_CANONICAL_KEYS)
        self.assertFalse((SHORTENED_VERSIONED_KEYS | LEGACY_PREVERSION_KEYS).intersection(metadata))

    def test_current_cache_metadata_uses_exact_canonical_contract_keys(self):
        metadata = meta.current_cache_metadata()
        payload = {**metadata, "count": 1, "emb": {"sha": _EMB}}
        result = meta.validate_cache_metadata(payload)
        self.assertTrue(result.ok)
        self.assertFalse(result.is_legacy)
        self.assertEqual(
            set(metadata),
            APPROVED_CANONICAL_KEYS - {"index_schema_version", "sidecar_format_version"},
        )
        self.assertFalse((SHORTENED_VERSIONED_KEYS | LEGACY_PREVERSION_KEYS).intersection(metadata))

    def test_index_mismatches_are_operator_facing_and_do_not_rebuild(self):
        base = meta.current_index_metadata()
        cases = {
            "index_schema_version": 999,
            "embedding_provider": "other",
            "embedding_model": "other-model",
            "embedding_task_type": "RETRIEVAL_QUERY",
            "embedding_dimension": 3072,
            "embedding_quantization": "float32",
            "chunk_hash_basis": "sha256(text)",
            "sidecar_format_version": 999,
            "source_provenance_approval_status": "remote",
        }
        for key, value in cases.items():
            with self.subTest(key=key):
                payload = {**base, key: value}
                result = meta.validate_index_metadata(payload)
                self.assertFalse(result.ok)
                message = "; ".join(result.errors)
                self.assertIn(key, message)
                self.assertIn("Rebuild the local search index", message)
                self.assertIn("never rebuilds automatically", message)

    def test_cache_mismatches_are_rejected(self):
        base = meta.current_cache_metadata()
        cases = {
            "cache_format_version": 999,
            "embedding_provider": "other",
            "embedding_model": "other-model",
            "embedding_task_type": "RETRIEVAL_QUERY",
            "embedding_dimension": 3072,
            "embedding_quantization": "float32",
            "chunk_hash_basis": "sha256(text)",
            "source_provenance_approval_status": "remote",
        }
        for key, value in cases.items():
            with self.subTest(key=key):
                result = meta.validate_cache_metadata({**base, key: value, "emb": {}})
                self.assertFalse(result.ok)
                self.assertIn(key, "; ".join(result.errors))

    def test_known_safe_preversion_index_and_cache_are_only_compatibility_accepted(self):
        legacy_index = {
            "model": meta.EMBEDDING_MODEL,
            "dim": meta.EMBEDDING_DIMENSION,
            "quant": meta.EMBEDDING_QUANTIZATION,
            "emb_file": meta.EMBEDDING_SIDECAR_FILE,
            "chunks": [{"text": "legacy", "text_sha": "sha", "emb": _EMB}],
        }
        legacy_cache = {
            "model": meta.EMBEDDING_MODEL,
            "count": 1,
            "emb": {"sha": _EMB},
        }

        index_result = meta.validate_index_metadata(legacy_index)
        cache_result = meta.validate_cache_metadata(legacy_cache)

        normalized_index = meta.canonicalize_index_metadata(legacy_index)
        normalized_cache = meta.canonicalize_cache_metadata(legacy_cache)

        self.assertTrue(index_result.ok)
        self.assertTrue(index_result.is_legacy)
        self.assertEqual(normalized_index["embedding_model"], meta.EMBEDDING_MODEL)
        self.assertEqual(normalized_index["embedding_dimension"], meta.EMBEDDING_DIMENSION)
        self.assertEqual(normalized_index["embedding_quantization"], meta.EMBEDDING_QUANTIZATION)
        self.assertFalse(SHORTENED_VERSIONED_KEYS.intersection(normalized_index))
        self.assertFalse(meta.validate_index_metadata(legacy_index, allow_legacy=False).ok)
        self.assertTrue(cache_result.ok)
        self.assertTrue(cache_result.is_legacy)
        self.assertEqual(normalized_cache["embedding_model"], meta.EMBEDDING_MODEL)
        self.assertFalse(SHORTENED_VERSIONED_KEYS.intersection(normalized_cache))
        self.assertFalse(meta.validate_cache_metadata(legacy_cache, allow_legacy=False).ok)

    def test_shortened_versioned_index_and_cache_contracts_are_rejected(self):
        versioned_index = {
            "schema_version": meta.INDEX_SCHEMA_VERSION,
            "provider": meta.EMBEDDING_PROVIDER,
            "model": meta.EMBEDDING_MODEL,
            "task_type": meta.EMBEDDING_TASK_TYPE,
            "dim": meta.EMBEDDING_DIMENSION,
            "quant": meta.EMBEDDING_QUANTIZATION,
            "chunk_hash_basis": meta.CHUNK_HASH_BASIS,
            "sidecar_format_version": meta.SIDECAR_FORMAT_VERSION,
            "cache_format_version": meta.CACHE_FORMAT_VERSION,
            "provenance_status": meta.PROVENANCE_STATUS,
            "emb_file": meta.EMBEDDING_SIDECAR_FILE,
            "chunks": [],
        }
        versioned_cache = {
            "cache_format_version": meta.CACHE_FORMAT_VERSION,
            "provider": meta.EMBEDDING_PROVIDER,
            "model": meta.EMBEDDING_MODEL,
            "task_type": meta.EMBEDDING_TASK_TYPE,
            "dim": meta.EMBEDDING_DIMENSION,
            "quant": meta.EMBEDDING_QUANTIZATION,
            "chunk_hash_basis": meta.CHUNK_HASH_BASIS,
            "provenance_status": meta.PROVENANCE_STATUS,
            "count": 0,
            "emb": {},
        }

        for payload, validator in (
            (versioned_index, meta.validate_index_metadata),
            (versioned_cache, meta.validate_cache_metadata),
        ):
            result = validator(payload)
            self.assertFalse(result.ok)
            message = "; ".join(result.errors)
            self.assertIn("shortened versioned metadata is not known-safe legacy", message)
            self.assertIn("Rebuild the local search index", message)
            self.assertEqual(meta.canonicalize_index_metadata(payload).get("provider"), meta.EMBEDDING_PROVIDER)

    def test_partial_canonical_and_mixed_metadata_fail_closed_not_legacy_safe(self):
        cases = [
            (
                "partial canonical",
                {"embedding_provider": meta.EMBEDDING_PROVIDER},
                "partial canonical metadata is not known-safe legacy",
            ),
            (
                "mixed canonical and legacy",
                {"embedding_provider": meta.EMBEDDING_PROVIDER, "model": meta.EMBEDDING_MODEL},
                "mixed canonical and legacy metadata is not known-safe legacy",
            ),
            (
                "partial legacy shared-only",
                {"chunk_hash_basis": meta.CHUNK_HASH_BASIS},
                "partial canonical metadata is not known-safe legacy",
            ),
        ]
        for label, payload, legacy_error in cases:
            with self.subTest(label):
                self.assertFalse(meta.validate_index_metadata(payload).ok)
                index_legacy = meta.validate_known_safe_legacy_index(payload)
                cache_legacy = meta.validate_known_safe_legacy_cache(payload)
                self.assertFalse(index_legacy.ok)
                self.assertTrue(index_legacy.is_legacy)
                self.assertIn(legacy_error, "; ".join(index_legacy.errors))
                self.assertFalse(meta.validate_cache_metadata(payload).ok)
                self.assertFalse(cache_legacy.ok)
                self.assertTrue(cache_legacy.is_legacy)
                self.assertIn(legacy_error, "; ".join(cache_legacy.errors))

    def test_complete_canonical_with_legacy_short_keys_rejected_before_success(self):
        index_payload = {
            **meta.current_index_metadata(),
            "provider": meta.EMBEDDING_PROVIDER,
            "model": meta.EMBEDDING_MODEL,
            "count": 0,
            "papers": {},
            "chunks": [],
        }
        cache_payload = {
            **meta.current_cache_metadata(),
            "provider": meta.EMBEDDING_PROVIDER,
            "model": meta.EMBEDDING_MODEL,
            "count": 0,
            "emb": {},
        }

        index_result = meta.validate_index_metadata(index_payload)
        cache_result = meta.validate_cache_metadata(cache_payload)

        self.assertFalse(index_result.ok)
        self.assertIn("shortened versioned metadata is not known-safe legacy", "; ".join(index_result.errors))
        self.assertFalse(cache_result.ok)
        self.assertIn("shortened versioned metadata is not known-safe legacy", "; ".join(cache_result.errors))

    def test_shortened_versioned_cache_is_not_canonicalized_into_acceptance(self):
        payload = {
            "provider": meta.EMBEDDING_PROVIDER,
            "model": meta.EMBEDDING_MODEL,
            "task_type": meta.EMBEDDING_TASK_TYPE,
            "dim": meta.EMBEDDING_DIMENSION,
            "quant": meta.EMBEDDING_QUANTIZATION,
            "chunk_hash_basis": meta.CHUNK_HASH_BASIS,
            "provenance_status": meta.PROVENANCE_STATUS,
            "count": 0,
            "emb": {},
        }

        result = meta.validate_cache_metadata(payload)

        self.assertFalse(result.ok)
        self.assertIn("shortened versioned metadata is not known-safe legacy", "; ".join(result.errors))

    def test_load_embedding_cache_skips_incompatible_index_and_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            topic_dir = Path(tmp)
            text = "hello"
            sha = build_search_index._chunk_sha(meta.EMBEDDING_MODEL, text)
            (topic_dir / "_search_index.json").write_text(
                json.dumps({
                    **meta.current_index_metadata(),
                    "embedding_provider": "other",
                    "count": 1,
                    "papers": {},
                    "chunks": [{"text": text, "text_sha": sha, "emb": _EMB}],
                }),
                encoding="utf-8",
            )
            (topic_dir / build_search_index.EMBED_CACHE_NAME).write_text(
                json.dumps({**meta.current_cache_metadata(), "cache_format_version": 999, "emb": {sha: _EMB}}),
                encoding="utf-8",
            )

            self.assertEqual(build_search_index.load_embedding_cache(topic_dir, meta.EMBEDDING_MODEL), {})

    def test_load_embedding_cache_accepts_current_and_legacy_local_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            topic_dir = Path(tmp)
            text = "hello"
            current_sha = build_search_index._chunk_sha(meta.EMBEDDING_MODEL, text)
            legacy_text = "legacy"
            legacy_sha = build_search_index._chunk_sha(meta.EMBEDDING_MODEL, legacy_text)
            (topic_dir / meta.EMBEDDING_SIDECAR_FILE).write_bytes(bytes([7]) * meta.EMBEDDING_DIMENSION)
            (topic_dir / "_search_index.json").write_text(
                json.dumps({
                    "model": meta.EMBEDDING_MODEL,
                    "dim": meta.EMBEDDING_DIMENSION,
                    "quant": meta.EMBEDDING_QUANTIZATION,
                    "emb_file": meta.EMBEDDING_SIDECAR_FILE,
                    "chunks": [{"text": legacy_text, "text_sha": legacy_sha}],
                }),
                encoding="utf-8",
            )
            (topic_dir / build_search_index.EMBED_CACHE_NAME).write_text(
                json.dumps({**meta.current_cache_metadata(), "count": 1, "emb": {current_sha: _EMB}}),
                encoding="utf-8",
            )

            cache = build_search_index.load_embedding_cache(topic_dir, meta.EMBEDDING_MODEL)
            self.assertEqual(cache[current_sha], _EMB)
            self.assertEqual(cache[legacy_sha], _EMB)

    def _write_topic_index(self, root, topic, payload=None, sidecar_size=None):
        topic_dir = root / topic
        topic_dir.mkdir(parents=True)
        chunks = [{"slug": "paper", "text": "hello", "text_sha": "sha"}]
        index = {
            **meta.current_index_metadata(),
            "count": len(chunks),
            "papers": {"paper": {"title": "Paper"}},
            "chunks": chunks,
        }
        if payload:
            index.update(payload)
        topic_dir.joinpath("_search_index.json").write_text(json.dumps(index), encoding="utf-8")
        size = meta.EMBEDDING_DIMENSION * len(chunks) if sidecar_size is None else sidecar_size
        topic_dir.joinpath(meta.EMBEDDING_SIDECAR_FILE).write_bytes(bytes([1]) * size)
        return topic_dir

    def test_cross_merge_refuses_metadata_mismatch_before_reading_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write_topic_index(docs, "good")
            self._write_topic_index(docs, "bad", {"embedding_provider": "other"}, sidecar_size=0)
            with patch.object(build_cross_index, "DOCS_DIR", docs):
                with self.assertRaises(SystemExit) as caught:
                    build_cross_index.merge_indexes(["good", "bad"])
            message = str(caught.exception)
            self.assertIn("embedding_provider", message)
            self.assertIn("Rebuild the local search index", message)
            self.assertIn("never rebuilds automatically", message)
            self.assertNotIn("sidecar length", message)

    def test_cross_merge_refuses_sidecar_length_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write_topic_index(docs, "bad", sidecar_size=meta.EMBEDDING_DIMENSION - 1)
            with patch.object(build_cross_index, "DOCS_DIR", docs):
                with self.assertRaises(SystemExit) as caught:
                    build_cross_index.merge_indexes(["bad"])
            self.assertIn("embedding sidecar length mismatch", str(caught.exception))
            self.assertIn("never rebuilds automatically", str(caught.exception))

    def test_doctor_validates_search_index_read_only_and_never_builds(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            self._write_topic_index(docs, "ai4s", {"embedding_provider": "other"})
            (docs / "ai4s" / "index.html").write_text("", encoding="utf-8")
            (docs / "ai4s" / "_new_classification.json").write_text("{}", encoding="utf-8")
            reporter = doctor_module.Reporter()
            fake_builder = MagicMock()
            with (
                patch.object(doctor_module, "DOCS_DIR", docs),
                patch.object(doctor_module, "PAPERS_INDEX", docs / "papers" / "_papers_index.json"),
                patch.dict("sys.modules", {"build_search_index": fake_builder}),
            ):
                doctor_module.check_topic(
                    reporter,
                    "ai4s",
                    {"zotero": {"collections": {"ai4s": "AI for Science"}}},
                    [],
                )
            fake_builder.assert_not_called()
            self.assertGreaterEqual(reporter.fails, 1)

    def test_doctor_secret_source_warning_redacts_values_and_reports_tls(self):
        reporter = doctor_module.Reporter()
        secret = "sk-ant-secret-not-for-output"
        output = io.StringIO()
        status = type("Status", (), {
            "mode": "api-key",
            "source": "env:ANTHROPIC_API_KEY",
            "ready": True,
            "detail": "API key configured",
        })()
        with (
            patch.object(doctor_module, "auth_status", return_value=status),
            patch.dict(doctor_module.os.environ, {"ANTHROPIC_API_KEY": secret}, clear=True),
            redirect_stdout(output),
        ):
            doctor_module.check_api_keys(
                reporter,
                {"anthropic_api_key": "legacy-secret", "google_api_key": "google-secret"},
                anthropic_smoke=False,
            )
        text = output.getvalue()
        self.assertIn("env:ANTHROPIC_API_KEY", text)
        self.assertIn("config:anthropic_api_key", text)
        self.assertIn("TLS verification", text)
        self.assertNotIn(secret, text)
        self.assertNotIn("legacy-secret", text)
        self.assertNotIn("google-secret", text)

    def test_api_search_defaults_match_cli_and_validate_topic(self):
        runner = MagicMock(return_value={"ok": True})
        fake_module = MagicMock()
        fake_module._run_search = runner

        with patch.dict("sys.modules", {"search_papers": fake_module}):
            result = pipeline_api.search(" ai4s ")

        self.assertEqual(result, {"ok": True})
        runner.assert_called_once_with(
            topic="ai4s",
            days=7,
            max_papers=100,
            threshold=0.3,
            skip_arxiv=False,
            since=None,
            until=None,
        )

        runner.reset_mock()
        with patch.dict("sys.modules", {"search_papers": fake_module}):
            pipeline_api.search(
                "scisci",
                days=14,
                max_papers=12,
                threshold=0.9,
                skip_arxiv=True,
                since="2026-01-01",
                until="2026-01-31",
            )
        runner.assert_called_once_with(
            topic="scisci",
            days=14,
            max_papers=12,
            threshold=0.9,
            skip_arxiv=True,
            since="2026-01-01",
            until="2026-01-31",
        )

        runner.reset_mock()
        with patch.dict("sys.modules", {"search_papers": fake_module}):
            with self.assertRaises(ValueError):
                pipeline_api.search("   ")
        runner.assert_not_called()

    def test_api_search_index_is_explicit_boundary_and_model_aligned(self):
        runner = MagicMock(return_value={"ok": True})
        fake_module = MagicMock()
        fake_module._run_search_index = runner
        with patch.dict("sys.modules", {"build_search_index": fake_module}):
            result = pipeline_api.search_index("ai4s", dry_run=True)
        self.assertEqual(result, {"ok": True})
        runner.assert_called_once_with(
            topic="ai4s",
            model=meta.EMBEDDING_MODEL,
            limit=None,
            dry_run=True,
        )
        with self.assertRaises(ValueError):
            pipeline_api.search_index("ai4s", model="text-embedding-3-small", dry_run=True)


if __name__ == "__main__":
    unittest.main()
