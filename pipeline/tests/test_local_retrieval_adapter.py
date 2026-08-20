"""Contracts for the read-only committed-Core lexical retrieval adapter."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from paper_curation.domain.retrieval import Query, RetrievalError
from paper_curation.retrieval.local import LocalIndexCatalog, local_lexical_retrieval_use_case


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _paper(root: Path, *, source: str, scope: str, record: str, text: str) -> Path:
    key = lambda value: hashlib.sha256(value.encode()).hexdigest()
    directory = root / "papers" / key(source) / key(scope) / key(record)
    directory.mkdir(parents=True)
    text_path = directory / "text.txt"
    text_path.write_text(text, encoding="utf-8")
    receipt = {
        "schema_version": 1,
        "paper": {"source_id": source, "scope_id": scope, "record_id": record},
        "stages": [{"stage": "extract_text", "fingerprint": _digest(text_path), "artifacts": [{
            "name": "text", "path": str(text_path), "fingerprint": _digest(text_path),
        }]}],
    }
    (directory / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    return directory


def test_local_catalog_ranks_unicode_sections_stably_and_cites(tmp_path: Path) -> None:
    _paper(tmp_path, source="source", scope="scope", record="beta", text="# Method\ncafé 바나나 바나나\n\n# Result\napple")
    _paper(tmp_path, source="source", scope="scope", record="alpha", text="# Method\n바나나 café")
    use_case = local_lexical_retrieval_use_case(tmp_path, "configured-topic", "source", "scope")

    first = use_case.search("configured-topic", Query("CAFÉ 바나나"))
    second = use_case.search("configured-topic", Query("café 바나나"))

    assert [(hit.slug, hit.section, hit.provenance) for hit in first] == [
        ("beta", "Method", ("lexical",)), ("alpha", "Method", ("lexical",))
    ]
    assert [hit.chunk_id for hit in first] == [hit.chunk_id for hit in second]
    assert all(len(hit.chunk_id) == 64 for hit in first)


def test_catalog_rejects_bad_receipts_and_does_not_leak_or_write(tmp_path: Path) -> None:
    valid = _paper(tmp_path, source="source", scope="scope", record="valid", text="local finding")
    _paper(tmp_path, source="source", scope="other", record="foreign", text="local finding")
    before = {path: path.stat().st_mtime_ns for path in tmp_path.rglob("*")}
    catalog = LocalIndexCatalog(tmp_path, "topic", "source", "scope")
    assert [chunk.slug for chunk in catalog.get("topic").chunks] == ["valid"]
    assert before == {path: path.stat().st_mtime_ns for path in tmp_path.rglob("*")}

    receipt = valid / "receipt.json"
    payload = json.loads(receipt.read_text())
    payload["stages"][0]["artifacts"][0]["path"] = "../../secret.txt"
    receipt.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(RetrievalError):
        catalog.get("topic")
