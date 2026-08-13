"""Domain models for provider-neutral search retrieval."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal


Provenance = Literal["lexical", "dense", "reranker"]


class RetrievalError(RuntimeError):
    """A retrieval operation could not be completed safely."""


class RetrievalValidationError(RetrievalError, ValueError):
    """A retrieval boundary input or provider result violates its contract."""


class DenseRetrievalError(RetrievalError):
    """An installed dense provider failed; callers must not silently substitute it."""


@dataclass(frozen=True, slots=True)
class Chunk:
    """A citeable unit in a conceptual search index."""

    chunk_id: str
    slug: str
    section: str
    text: str

    def __post_init__(self) -> None:
        for field_name in ("chunk_id", "slug", "section"):
            if not isinstance(getattr(self, field_name), str) or not getattr(self, field_name).strip():
                raise RetrievalValidationError(f"chunk {field_name} must be a non-empty string")
        if not isinstance(self.text, str) or not self.text.strip():
            raise RetrievalValidationError("chunk text must be a non-empty string")


@dataclass(frozen=True, slots=True)
class Query:
    """A topic-neutral request for ranked search results."""

    text: str
    limit: int = 10
    candidate_limit: int = 100

    def __post_init__(self) -> None:
        if not isinstance(self.text, str) or not self.text.strip():
            raise RetrievalValidationError("query text must be a non-empty string")
        for field_name in ("limit", "candidate_limit"):
            value = getattr(self, field_name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise RetrievalValidationError(f"query {field_name} must be a positive integer")
        if self.candidate_limit < self.limit:
            raise RetrievalValidationError("query candidate_limit must be at least limit")


@dataclass(frozen=True, slots=True)
class Hit:
    """A scored citeable chunk returned by a retrieval provider or use case."""

    chunk_id: str
    slug: str
    section: str
    score: float
    rank: int
    provenance: tuple[Provenance, ...]

    def __post_init__(self) -> None:
        for field_name in ("chunk_id", "slug", "section"):
            if not isinstance(getattr(self, field_name), str) or not getattr(self, field_name).strip():
                raise RetrievalValidationError(f"hit {field_name} must be a non-empty string")
        if not isinstance(self.score, (int, float)) or isinstance(self.score, bool) or not math.isfinite(self.score):
            raise RetrievalValidationError("hit score must be finite")
        if not isinstance(self.rank, int) or isinstance(self.rank, bool) or self.rank < 1:
            raise RetrievalValidationError("hit rank must be a positive integer")
        if not isinstance(self.provenance, tuple) or not self.provenance or any(
            source not in {"lexical", "dense", "reranker"} for source in self.provenance
        ):
            raise RetrievalValidationError("hit provenance must contain known retrieval sources")


@dataclass(frozen=True, slots=True)
class IndexMetadata:
    """Metadata and stable identities for one prebuilt conceptual search index.

    ``model``, ``dimension``, ``quantization``, and ``embedding_file`` map to
    the existing search-index artifact's model, dim, quant, and emb_file fields.
    """

    topic: str
    dimension: int
    chunks: tuple[Chunk, ...]
    model: str | None = None
    quantization: str | None = None
    embedding_file: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.topic, str) or not self.topic.strip():
            raise RetrievalValidationError("index topic must be a non-empty string")
        if not isinstance(self.dimension, int) or isinstance(self.dimension, bool) or self.dimension < 1:
            raise RetrievalValidationError("index dimension must be a positive integer")
        if not isinstance(self.chunks, tuple):
            raise RetrievalValidationError("index chunks must be an immutable tuple")
        if any(not isinstance(chunk, Chunk) for chunk in self.chunks):
            raise RetrievalValidationError("index chunks must contain only chunks")
        if len({chunk.chunk_id for chunk in self.chunks}) != len(self.chunks):
            raise RetrievalValidationError("index chunk identities must be unique")
        if self.model is not None and (not isinstance(self.model, str) or not self.model.strip()):
            raise RetrievalValidationError("index model must be a non-empty string or None")
        for field_name in ("quantization", "embedding_file"):
            value = getattr(self, field_name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise RetrievalValidationError(f"index {field_name} must be a non-empty string or None")

    @property
    def count(self) -> int:
        """The existing artifact's ``count`` field."""
        return len(self.chunks)

    @property
    def dim(self) -> int:
        """The existing artifact's ``dim`` field."""
        return self.dimension

    @property
    def quant(self) -> str | None:
        """The existing artifact's ``quant`` field."""
        return self.quantization

    @property
    def emb_file(self) -> str | None:
        """The existing artifact's ``emb_file`` field."""
        return self.embedding_file
