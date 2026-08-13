"""Hybrid retrieval application service."""

from __future__ import annotations

from collections.abc import Sequence
import math
from typing import Protocol, runtime_checkable

from paper_curation.domain.retrieval import (
    DenseRetrievalError,
    Hit,
    IndexMetadata,
    Query,
    RetrievalError,
    RetrievalValidationError,
)
@runtime_checkable
class IndexCatalog(Protocol):
    def get(self, topic: str) -> IndexMetadata: ...


@runtime_checkable
class LexicalRetriever(Protocol):
    def search(self, index: IndexMetadata, query: Query, limit: int) -> Sequence[Hit]: ...


@runtime_checkable
class DenseRetriever(Protocol):
    def embed(self, query: Query) -> Sequence[float]: ...
    def search(
        self, index: IndexMetadata, vector: Sequence[float], limit: int
    ) -> Sequence[Hit]: ...


@runtime_checkable
class Reranker(Protocol):
    def rerank(self, query: Query, hits: Sequence[Hit], limit: int) -> Sequence[Hit]: ...


RRF_K = 60


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[str]], *, k: int = RRF_K
) -> dict[str, float]:
    """Fuse zero-based identity rankings used by browser and CLI retrieval."""
    if k <= 0:
        raise RetrievalValidationError("RRF k must be positive")
    scores: dict[str, float] = {}
    for ranking in rankings:
        seen: set[str] = set()
        for rank, identity in enumerate(ranking):
            if not identity or identity in seen:
                raise RetrievalValidationError(
                    "RRF rankings require unique non-empty identities"
                )
            seen.add(identity)
            scores[identity] = scores.get(identity, 0.0) + 1 / (k + rank)
    return scores


class RetrievalUseCase:
    """Fuse injected lexical and optional dense retrieval with deterministic RRF."""

    def __init__(
        self,
        indexes: IndexCatalog,
        lexical: LexicalRetriever,
        dense: DenseRetriever | None = None,
        reranker: Reranker | None = None,
    ) -> None:
        self._indexes = indexes
        self._lexical = lexical
        self._dense = dense
        self._reranker = reranker

    def search(self, topic: str, query: Query) -> tuple[Hit, ...]:
        """Retrieve citeable chunks for ``topic`` without provider substitution.

        A missing dense provider is an explicit BM25/lexical-only mode. A
        configured dense provider that fails is an error, not a fallback.
        """
        if not isinstance(topic, str) or not topic.strip():
            raise RetrievalValidationError("topic must be a non-empty string")
        try:
            index = self._indexes.get(topic)
        except Exception:
            raise RetrievalError("index catalog failed") from None
        if not isinstance(index, IndexMetadata):
            raise RetrievalValidationError("index catalog returned invalid metadata")
        if index.topic != topic:
            raise RetrievalValidationError("index topic does not match requested topic")

        lexical_hits = self._search_lexical(index, query)
        ranked_sources: list[tuple[str, tuple[Hit, ...]]] = [("lexical", lexical_hits)]
        if self._dense is not None:
            vector = self._embed_dense(query, index)
            ranked_sources.append(("dense", self._search_dense(index, vector, query)))

        fused = self._fuse(index, ranked_sources)
        if self._reranker is not None and fused:
            fused = self._rerank(query, index, fused)
        return tuple(
            Hit(
                chunk_id=hit.chunk_id,
                slug=hit.slug,
                section=hit.section,
                score=hit.score,
                rank=position,
                provenance=hit.provenance,
            )
            for position, hit in enumerate(fused[:query.limit], start=1)
        )

    def _search_lexical(self, index: IndexMetadata, query: Query) -> tuple[Hit, ...]:
        try:
            hits = self._lexical.search(index, query, query.candidate_limit)
        except Exception:
            raise RetrievalError("lexical retrieval provider failed") from None
        return self._validate_hits(index, hits, "lexical")

    def _embed_dense(self, query: Query, index: IndexMetadata) -> tuple[float, ...]:
        assert self._dense is not None
        try:
            raw_vector = self._dense.embed(query)
        except Exception:
            raise DenseRetrievalError("dense embedding provider failed") from None
        if isinstance(raw_vector, (str, bytes)):
            raise DenseRetrievalError("dense embedding provider returned an invalid vector")
        try:
            vector = tuple(float(value) for value in raw_vector)
        except (TypeError, ValueError):
            raise DenseRetrievalError("dense embedding provider returned an invalid vector") from None
        if len(vector) != index.dimension:
            raise DenseRetrievalError("dense embedding dimension does not match index")
        if not vector or not all(math.isfinite(value) for value in vector):
            raise DenseRetrievalError("dense embedding provider returned an invalid vector")
        if math.fsum(value * value for value in vector) == 0:
            raise DenseRetrievalError("dense embedding provider returned a zero vector")
        return vector

    def _search_dense(
        self, index: IndexMetadata, vector: tuple[float, ...], query: Query
    ) -> tuple[Hit, ...]:
        assert self._dense is not None
        try:
            hits = self._dense.search(index, vector, query.candidate_limit)
        except Exception:
            raise DenseRetrievalError("dense retrieval provider failed") from None
        return self._validate_hits(index, hits, "dense")

    @staticmethod
    def _validate_hits(index: IndexMetadata, hits: Sequence[Hit], source: str) -> tuple[Hit, ...]:
        if isinstance(hits, (str, bytes)) or not isinstance(hits, Sequence):
            raise RetrievalValidationError(f"{source} retrieval provider must return a sequence of hits")
        chunks = {chunk.chunk_id: chunk for chunk in index.chunks}
        seen: set[str] = set()
        validated: list[Hit] = []
        for hit in hits:
            if not isinstance(hit, Hit):
                raise RetrievalValidationError(f"{source} retrieval provider returned a non-hit")
            chunk = chunks.get(hit.chunk_id)
            if chunk is None:
                raise RetrievalValidationError(f"{source} retrieval provider returned an unknown chunk identity")
            if hit.chunk_id in seen:
                raise RetrievalValidationError(f"{source} retrieval provider returned a duplicate chunk identity")
            if hit.slug != chunk.slug or hit.section != chunk.section:
                raise RetrievalValidationError(f"{source} retrieval provider returned mismatched citation metadata")
            seen.add(hit.chunk_id)
            validated.append(hit)
        return tuple(validated)

    @staticmethod
    def _fuse(index: IndexMetadata, sources: Sequence[tuple[str, tuple[Hit, ...]]]) -> tuple[Hit, ...]:
        scores: dict[str, float] = {}
        provenance: dict[str, list[str]] = {}
        rankings: list[tuple[str, ...]] = []
        for source, hits in sources:
            # Provider rank fields are not trusted as stable ordering: stable score
            # ordering plus chunk identity keeps equal-score fusion reproducible.
            ordered = sorted(hits, key=lambda hit: (-hit.score, hit.chunk_id))
            rankings.append(tuple(hit.chunk_id for hit in ordered))
            for hit in ordered:
                provenance.setdefault(hit.chunk_id, []).append(source)
        scores.update(reciprocal_rank_fusion(rankings))
        chunks = {chunk.chunk_id: chunk for chunk in index.chunks}
        ordered_ids = sorted(scores, key=lambda chunk_id: (-scores[chunk_id], chunk_id))
        return tuple(
            Hit(
                chunk_id=chunk_id,
                slug=chunks[chunk_id].slug,
                section=chunks[chunk_id].section,
                score=scores[chunk_id],
                rank=position,
                provenance=tuple(provenance[chunk_id]),  # type: ignore[arg-type]
            )
            for position, chunk_id in enumerate(ordered_ids, start=1)
        )

    def _rerank(self, query: Query, index: IndexMetadata, fused: tuple[Hit, ...]) -> tuple[Hit, ...]:
        assert self._reranker is not None
        try:
            reranked = self._reranker.rerank(query, fused, query.candidate_limit)
        except Exception:
            raise RetrievalError("reranking provider failed") from None
        validated = self._validate_hits(index, reranked, "reranker")
        rrf_scores = {hit.chunk_id: hit.score for hit in fused}
        source_provenance = {hit.chunk_id: hit.provenance for hit in fused}
        if any(hit.chunk_id not in rrf_scores for hit in validated):
            raise RetrievalValidationError("reranking provider returned a non-fused chunk identity")
        return tuple(
            Hit(
                chunk_id=hit.chunk_id,
                slug=hit.slug,
                section=hit.section,
                score=rrf_scores[hit.chunk_id],
                rank=hit.rank,
                provenance=source_provenance[hit.chunk_id] + ("reranker",),
            )
            for hit in sorted(validated, key=lambda hit: (hit.rank, hit.chunk_id))
        )
