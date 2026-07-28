#!/usr/bin/env python3
"""Read-only local retrieval over a topic ``_search_index.json``.

This module deliberately never embeds queries, rebuilds an index, or writes cache
files.  Callers may provide a locally-produced query vector; otherwise retrieval
is lexical BM25 only.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence
PIPELINE_DIR = Path(__file__).resolve().parent
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

from lib.search_index_metadata import (
    EMBEDDING_DIMENSION,
    EMBEDDING_SIDECAR_FILE,
    KEY_SOURCE_PROVENANCE_APPROVAL_STATUS,
    validate_index_metadata,
)

RRF_K = 60
MAX_CANDIDATES = 100
_INDEX_NAME = "_search_index.json"
_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


class SearchRequestError(ValueError):
    """Raised for invalid or unsafe local retrieval requests."""


def _tokens(value: str) -> list[str]:
    return _TOKEN_RE.findall(value.lower())


def _safe_topic_dir(topic_root: str | os.PathLike[str], topic: str) -> Path:
    if not isinstance(topic, str) or not topic or topic in {".", ".."}:
        raise SearchRequestError("topic must be a non-empty single path component")
    if Path(topic).name != topic or "/" in topic or "\\" in topic:
        raise SearchRequestError("topic traversal is not allowed")
    root = Path(topic_root)
    try:
        root_stat = root.lstat()
    except OSError as exc:
        raise SearchRequestError(f"topic root is unavailable: {exc}") from exc
    if os.path.islink(root):
        raise SearchRequestError("topic root symlink traversal is not allowed")
    if not root_stat:
        raise SearchRequestError("topic root is unavailable")
    topic_dir = root / topic
    try:
        topic_stat = topic_dir.lstat()
    except OSError as exc:
        raise SearchRequestError(f"topic is unavailable: {exc}") from exc
    if os.path.islink(topic_dir) or not topic_stat:
        raise SearchRequestError("topic symlink traversal is not allowed")
    if not topic_dir.is_dir():
        raise SearchRequestError("topic is not a directory")
    return topic_dir


def _read_regular_json(path: Path) -> Mapping[str, Any]:
    try:
        if os.path.islink(path) or not path.is_file():
            raise SearchRequestError(f"{path.name} must be a regular non-symlink file")
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
    except json.JSONDecodeError as exc:
        raise SearchRequestError(f"{path.name} is not valid JSON: {exc.msg}") from exc
    except OSError as exc:
        raise SearchRequestError(f"cannot read {path.name}: {exc}") from exc
    if not isinstance(value, Mapping):
        raise SearchRequestError(f"{path.name} must contain an object")
    return value


def _validate_bounds(top_k: int, candidate_k: int) -> None:
    if isinstance(top_k, bool) or isinstance(candidate_k, bool):
        raise SearchRequestError("top_k and candidate_k must be integers")
    if not isinstance(top_k, int) or not isinstance(candidate_k, int):
        raise SearchRequestError("top_k and candidate_k must be integers")
    if not 1 <= top_k <= candidate_k <= MAX_CANDIDATES:
        raise SearchRequestError("require 1 <= top_k <= candidate_k <= 100")


def _normalized_vector(vector: Sequence[object]) -> list[float]:
    if isinstance(vector, (str, bytes)) or len(vector) != EMBEDDING_DIMENSION:
        raise SearchRequestError(f"query_vector must contain exactly {EMBEDDING_DIMENSION} values")
    out: list[float] = []
    for value in vector:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise SearchRequestError("query_vector values must be finite numbers")
        out.append(float(value))
    norm = math.sqrt(sum(value * value for value in out))
    if not math.isfinite(norm) or norm == 0:
        raise SearchRequestError("query_vector must have a finite non-zero norm")
    return [value / norm for value in out]


def _bm25(chunks: Sequence[Mapping[str, Any]], query: str) -> list[tuple[int, float]]:
    query_terms = _tokens(query)
    if not query_terms:
        return [(index, 0.0) for index in range(len(chunks))]
    documents = [_tokens(str(chunk.get("text", ""))) for chunk in chunks]
    count = len(documents)
    average_length = sum(map(len, documents)) / count if count else 0.0
    document_frequency = Counter(term for document in documents for term in set(document))
    query_frequency = Counter(query_terms)
    scores: list[tuple[int, float]] = []
    for index, document in enumerate(documents):
        frequencies = Counter(document)
        score = 0.0
        for term, qf in query_frequency.items():
            frequency = frequencies[term]
            if not frequency:
                continue
            idf = math.log(1.0 + (count - document_frequency[term] + 0.5) / (document_frequency[term] + 0.5))
            denominator = frequency + 1.2 * (1.0 - 0.75 + 0.75 * len(document) / (average_length or 1.0))
            score += qf * idf * frequency * 2.2 / denominator
        scores.append((index, score))
    return sorted(scores, key=lambda item: (-item[1], item[0]))


def _dense_vectors(topic_dir: Path, index: Mapping[str, Any], chunk_count: int) -> tuple[list[memoryview] | None, str | None]:
    validation = validate_index_metadata(index)
    if not validation.ok:
        return None, "index metadata invalid: " + "; ".join(validation.errors)
    if validation.is_legacy:
        return None, "legacy index metadata is unbound; dense retrieval disabled"
    if index.get("emb_file") != EMBEDDING_SIDECAR_FILE:
        return None, "canonical embedding sidecar is not declared"
    sidecar = topic_dir / EMBEDDING_SIDECAR_FILE
    try:
        if os.path.islink(sidecar) or not sidecar.is_file():
            return None, "embedding sidecar is missing or symlinked"
        payload = sidecar.read_bytes()
    except OSError as exc:
        return None, f"embedding sidecar is unreadable: {exc}"
    expected_size = chunk_count * EMBEDDING_DIMENSION
    if len(payload) != expected_size:
        return None, f"embedding sidecar length mismatch: expected {expected_size}, got {len(payload)}"
    signed = memoryview(payload).cast("b")
    return [signed[offset:offset + EMBEDDING_DIMENSION] for offset in range(0, len(signed), EMBEDDING_DIMENSION)], None


def _cosine_scores(vectors: Sequence[memoryview], query: Sequence[float]) -> list[tuple[int, float]]:
    scores: list[tuple[int, float]] = []
    for index, vector in enumerate(vectors):
        dot = sum(component * weight for component, weight in zip(vector, query))
        norm = math.sqrt(sum(component * component for component in vector))
        scores.append((index, dot / norm if norm else 0.0))
    return sorted(scores, key=lambda item: (-item[1], item[0]))


def search_index(
    topic_root: str | os.PathLike[str],
    topic: str,
    query: str,
    *,
    top_k: int = 10,
    candidate_k: int = 50,
    query_vector: Sequence[object] | None = None,
) -> dict[str, Any]:
    """Search one local topic index without changing the filesystem or network state."""
    _validate_bounds(top_k, candidate_k)
    if not isinstance(query, str) or not query.strip():
        raise SearchRequestError("query must be a non-empty string")
    normalized_query = _normalized_vector(query_vector) if query_vector is not None else None
    topic_dir = _safe_topic_dir(topic_root, topic)
    index = _read_regular_json(topic_dir / _INDEX_NAME)
    raw_chunks = index.get("chunks")
    if not isinstance(raw_chunks, list) or not all(isinstance(chunk, Mapping) for chunk in raw_chunks):
        raise SearchRequestError("index chunks must be an array of objects")
    chunks = list(raw_chunks)
    lexical = _bm25(chunks, query)[:candidate_k]
    dense_status: dict[str, Any] = {
        "enabled": False,
        "reason": "query_vector not provided",
        "metadata_provenance_status": index.get(KEY_SOURCE_PROVENANCE_APPROVAL_STATUS),
    }
    dense: list[tuple[int, float]] = []
    if normalized_query is not None:
        vectors, reason = _dense_vectors(topic_dir, index, len(chunks))
        if vectors is None:
            dense_status["reason"] = reason
        else:
            dense = _cosine_scores(vectors, normalized_query)[:candidate_k]
            dense_status.update(enabled=True, reason=None)
    if dense:
        ranks: dict[int, float] = {}
        for rank, (chunk_index, _) in enumerate(lexical, start=1):
            ranks[chunk_index] = ranks.get(chunk_index, 0.0) + 1.0 / (RRF_K + rank)
        for rank, (chunk_index, _) in enumerate(dense, start=1):
            ranks[chunk_index] = ranks.get(chunk_index, 0.0) + 1.0 / (RRF_K + rank)
        ordered = sorted(ranks, key=lambda chunk_index: (-ranks[chunk_index], chunk_index))[:top_k]
        scores = {chunk_index: ranks[chunk_index] for chunk_index in ordered}
        mode = "hybrid_rrf"
    else:
        ordered = [chunk_index for chunk_index, _ in lexical[:top_k]]
        scores = dict(lexical[:top_k])
        mode = "lexical_bm25"
    papers = index.get("papers")
    papers_by_slug = {paper.get("slug"): paper for paper in papers if isinstance(paper, Mapping) and paper.get("slug") is not None} if isinstance(papers, list) else {}
    results: list[dict[str, Any]] = []
    for rank, chunk_index in enumerate(ordered, start=1):
        record = dict(chunks[chunk_index])
        paper = papers_by_slug.get(record.get("slug"))
        if paper:
            for key in ("citation", "citations", "figures", "figure", "notes", "note", "parent_id", "parent", "source", "source_id", "chunk_id"):
                if key not in record and key in paper:
                    record[key] = paper[key]
        record["rank"] = rank
        record["score"] = scores[chunk_index]
        results.append(record)
    return {
        "topic": topic,
        "query": query,
        "mode": mode,
        "rrf_k": RRF_K if mode == "hybrid_rrf" else None,
        "dense_status": dense_status,
        "results": results,
    }


# A descriptive alias for callers that use the module name as the API name.
query_search_index = search_index


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only local topic search")
    parser.add_argument("--topic-root", required=True, help="directory containing topic directories")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--candidate-k", type=int, default=50)
    parser.add_argument("--query-vector", help="JSON array of locally supplied vector values")
    args = parser.parse_args(argv)
    try:
        vector = json.loads(args.query_vector) if args.query_vector is not None else None
        result = search_index(args.topic_root, args.topic, args.query, top_k=args.top_k, candidate_k=args.candidate_k, query_vector=vector)
    except (SearchRequestError, json.JSONDecodeError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, sort_keys=True, separators=(",", ":")), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
