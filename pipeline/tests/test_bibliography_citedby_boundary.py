"""Contract tests for provider-neutral bibliography and cited-by boundaries."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from contextlib import contextmanager
import hashlib
import unittest

from paper_curation.application.bibliography import IngestBibliographySidecars
from paper_curation.application.citedby import AnalyzeCitedBy, CitingSourceError
from paper_curation.domain.bibliography import BibliographyRecord, BibliographyValidationError


class FakeRepository:
    def __init__(self, *, fail_key: str = "") -> None:
        self.committed: list[BibliographyRecord] = []
        self.fail_key = fail_key
        self.rollbacks = 0

    @contextmanager
    def transaction(self):
        pending: list[BibliographyRecord] = []

        class Transaction:
            def upsert(_, bibliography) -> None:
                if bibliography.record.key == self.fail_key:
                    raise RuntimeError("storage failed")
                pending.append(bibliography)

        try:
            yield Transaction()
        except Exception:
            self.rollbacks += 1
            raise
        else:
            self.committed.extend(pending)


def _sidecar(key: str, text: str, *, title: str = "A General Paper") -> dict[str, object]:
    return {
        "schema": "bibliography-sidecar-1",
        "zotero": {"key": key, "title": title, "DOI": "https://doi.org/10.1/ABC"},
        "authors": [{"display_name": "Ada Example"}],
        "affiliations": [{"name": "Example University", "country": "Korea"}],
        "text_md_sha256": hashlib.sha256(text.encode()).hexdigest(),
    }


class SidecarIngestionTests(unittest.TestCase):
    def test_ingests_sidecar_without_zotero_or_database_global(self) -> None:
        repository = FakeRepository()
        result = IngestBibliographySidecars(repository).ingest(
            [_sidecar("ZOTERO1", "review text")],
            text_by_zotero_key={"ZOTERO1": "review text"},
        )
        self.assertEqual(result.bibliographies[0].record.doi, "10.1/abc")
        self.assertEqual(repository.committed, list(result.bibliographies))
        self.assertEqual(
            result.bibliographies[0].record.institutions[0].name,
            "Example University",
        )

    def test_rejects_stale_hash_before_opening_transaction(self) -> None:
        repository = FakeRepository()
        with self.assertRaisesRegex(BibliographyValidationError, "stale sidecar"):
            IngestBibliographySidecars(repository).ingest(
                [_sidecar("ZOTERO1", "captured")],
                text_by_zotero_key={"ZOTERO1": "changed"},
            )
        self.assertEqual(repository.committed, [])
        self.assertEqual(repository.rollbacks, 0)

    def test_transaction_rolls_back_all_records_on_storage_failure(self) -> None:
        repository = FakeRepository(fail_key="ZOTERO2")
        use_case = IngestBibliographySidecars(repository)
        with self.assertRaisesRegex(RuntimeError, "storage failed"):
            use_case.ingest(
                [_sidecar("ZOTERO1", "first"), _sidecar("ZOTERO2", "second")],
                text_by_zotero_key={"ZOTERO1": "first", "ZOTERO2": "second"},
            )
        self.assertEqual(repository.committed, [])
        self.assertEqual(repository.rollbacks, 1)


class FakeSource:
    name = "catalog"

    def __init__(self, papers: Iterable[Mapping[str, object]], error: Exception | None = None) -> None:
        self._papers = tuple(papers)
        self._error = error
        self.calls = 0

    def fetch(self, target: BibliographyRecord) -> Iterable[Mapping[str, object]]:
        self.calls += 1
        if self._error is not None:
            raise self._error
        return self._papers


class FakeAnalyzer:
    def __init__(self) -> None:
        self.topics: list[str] = []

    def analyze(self, topic: str, target: BibliographyRecord, citing_papers):
        self.topics.append(topic)
        return {"count": len(citing_papers)}


class CitedByBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.target = BibliographyRecord(key="target", title="Target")

    def test_deduplicates_strong_ids_without_title_bridging_and_retains_provenance(self) -> None:
        source = FakeSource([
            {"title": "A Citing Paper", "doi": "10.10/ONE", "url": "https://one"},
            {"title": "A   Citing Paper", "arxiv_id": "arXiv:1234.5678", "url": "https://two"},
            {"title": "Other title", "doi": "10.10/one", "url": "https://three"},
        ])
        result = AnalyzeCitedBy(source, FakeAnalyzer()).analyze(self.target, topic="marine biology")
        self.assertEqual(len(result.citing_papers), 2)
        by_doi = next(paper for paper in result.citing_papers if paper.doi)
        by_arxiv = next(paper for paper in result.citing_papers if paper.arxiv_id)
        self.assertEqual(by_doi.doi, "10.10/one")
        self.assertEqual(
            [e.locator for e in by_doi.evidence],
            ["https://one", "https://three"],
        )
        self.assertEqual(by_arxiv.arxiv_id, "1234.5678")
        self.assertEqual([e.locator for e in by_arxiv.evidence], ["https://two"])

    def test_selected_provider_failure_is_not_replaced(self) -> None:
        source = FakeSource([], RuntimeError("catalog unavailable"))
        analyzer = FakeAnalyzer()
        with self.assertRaisesRegex(CitingSourceError, "catalog failed"):
            AnalyzeCitedBy(source, analyzer).analyze(self.target, topic="any topic")
        self.assertEqual(source.calls, 1)
        self.assertEqual(analyzer.topics, [])

    def test_accepts_an_arbitrary_topic(self) -> None:
        analyzer = FakeAnalyzer()
        result = AnalyzeCitedBy(FakeSource([]), analyzer).analyze(
            self.target, topic="고대 해양 무척추동물 화석",
        )
        self.assertEqual(result.topic, "고대 해양 무척추동물 화석")
        self.assertEqual(analyzer.topics, ["고대 해양 무척추동물 화석"])


if __name__ == "__main__":
    unittest.main()
