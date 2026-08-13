"""Network-free contracts for the provider-neutral retrieval boundary."""

from __future__ import annotations

import unittest

from paper_curation.application.retrieve import RRF_K, RetrievalUseCase
from paper_curation.domain.retrieval import (
    Chunk,
    DenseRetrievalError,
    Hit,
    IndexMetadata,
    Query,
)


class Catalog:
    def __init__(self, index: IndexMetadata) -> None:
        self.index = index

    def get(self, topic: str) -> IndexMetadata:
        return self.index


class Lexical:
    def __init__(self, hits: tuple[Hit, ...]) -> None:
        self.hits = hits
        self.calls = 0

    def search(self, index: IndexMetadata, query: Query, limit: int) -> tuple[Hit, ...]:
        self.calls += 1
        return self.hits


class Dense:
    def __init__(self, vector: tuple[float, ...], hits: tuple[Hit, ...]) -> None:
        self.vector = vector
        self.hits = hits
        self.calls = 0

    def embed(self, query: Query) -> tuple[float, ...]:
        self.calls += 1
        return self.vector

    def search(self, index: IndexMetadata, vector: tuple[float, ...], limit: int) -> tuple[Hit, ...]:
        self.calls += 1
        return self.hits


def _index(topic: str = "any-topic") -> IndexMetadata:
    return IndexMetadata(
        topic=topic,
        dimension=2,
        model="test-model",
        quantization="int8-l2norm",
        embedding_file="_search_index_emb.bin",
        chunks=(
            Chunk("a:How", "a", "How", "alpha method"),
            Chunk("b:Achievement", "b", "Achievement", "beta result"),
        ),
    )


def _hit(chunk_id: str, slug: str, section: str, score: float) -> Hit:
    return Hit(chunk_id, slug, section, score, 1, ("lexical",))


class RetrievalBoundaryTests(unittest.TestCase):
    def test_lexical_only_is_available_without_dense_provider(self) -> None:
        index = _index()
        lexical = Lexical((_hit("a:How", "a", "How", 2.0),))
        result = RetrievalUseCase(Catalog(index), lexical).search("any-topic", Query("alpha"))
        self.assertEqual([(hit.slug, hit.section, hit.provenance) for hit in result], [("a", "How", ("lexical",))])
        self.assertAlmostEqual(result[0].score, 1 / RRF_K)

    def test_hybrid_rrf_fuses_lexical_and_dense_ranks(self) -> None:
        index = _index()
        lexical = Lexical((
            _hit("a:How", "a", "How", 2.0),
            _hit("b:Achievement", "b", "Achievement", 1.0),
        ))
        dense = Dense((1.0, 0.0), (
            _hit("b:Achievement", "b", "Achievement", 2.0),
            _hit("a:How", "a", "How", 1.0),
        ))
        result = RetrievalUseCase(Catalog(index), lexical, dense).search("any-topic", Query("question"))
        self.assertEqual([hit.chunk_id for hit in result], ["a:How", "b:Achievement"])
        self.assertAlmostEqual(result[0].score, 1 / RRF_K + 1 / (RRF_K + 1))
        self.assertEqual(result[0].provenance, ("lexical", "dense"))
        self.assertEqual(dense.calls, 2)

    def test_equal_scores_are_stable_by_chunk_identity(self) -> None:
        index = _index()
        lexical = Lexical((
            _hit("b:Achievement", "b", "Achievement", 1.0),
            _hit("a:How", "a", "How", 1.0),
        ))
        result = RetrievalUseCase(Catalog(index), lexical).search("any-topic", Query("tie"))
        self.assertEqual([hit.chunk_id for hit in result], ["a:How", "b:Achievement"])

    def test_malformed_dense_vector_fails_instead_of_falling_back(self) -> None:
        index = _index()
        lexical = Lexical((_hit("a:How", "a", "How", 1.0),))
        dense = Dense((1.0,), ())
        with self.assertRaises(DenseRetrievalError):
            RetrievalUseCase(Catalog(index), lexical, dense).search("any-topic", Query("alpha"))
        self.assertEqual(lexical.calls, 1)

    def test_arbitrary_topic_is_not_hard_coded(self) -> None:
        index = _index("면역-설계-2026")
        lexical = Lexical((_hit("a:How", "a", "How", 1.0),))
        result = RetrievalUseCase(Catalog(index), lexical).search("면역-설계-2026", Query("어떤 주제도 검색"))
        self.assertEqual(result[0].slug, "a")


if __name__ == "__main__":
    unittest.main()
