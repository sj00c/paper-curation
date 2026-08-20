"""Synthetic contracts for application-level bibliography intake and link parsing."""

from __future__ import annotations

from contextlib import contextmanager
import unittest

from paper_curation.application.affiliation_links import (
    infer_marker_alphabet,
    parse_author_markers,
    parse_marker_affiliations,
    resolve_affiliation_links,
)
from paper_curation.application.bibliography import (
    BibliographyCandidate,
    IngestBibliographySidecars,
    merge_bibliography_candidates,
)
from paper_curation.domain.author_identity import Author
from paper_curation.domain.bibliography import (
    BibliographyRecord,
    BibliographyField,
    BibliographyValidationError,
    FieldEvidence,
    Institution,
    SourceEvidence,
)


class Repository:
    def __init__(self) -> None:
        self.upserts: list[BibliographyRecord] = []

    @contextmanager
    def transaction(self):
        class Transaction:
            def upsert(_, bibliography) -> None:
                self.upserts.append(bibliography)
        yield Transaction()


class AffiliationLinkTests(unittest.TestCase):
    def test_document_scoped_symbols_digit_runs_and_wrapped_byline(self) -> None:
        document = """Ada Example¹, Bob Example2\n1 Example University\n2 Other University"""
        alphabet = infer_marker_alphabet(document)
        self.assertEqual(alphabet, ("1", "2"))
        markers = parse_author_markers(document, (Author("Ada Example"), Author("Bob Example")), alphabet)
        self.assertEqual(markers, {0: ("1",), 1: ("2",)})
        self.assertEqual(parse_marker_affiliations(document, alphabet)["1"], ("Example University",))
        self.assertNotIn("*", alphabet)

    def test_ties_and_many_to_many_stay_unresolved(self) -> None:
        authors = (Author("Ada Example"), Author("Bob Example"))
        institutions = (Institution("Example University"), Institution("Example Institute"))
        self.assertEqual(resolve_affiliation_links(authors, institutions), ())
        self.assertEqual(resolve_affiliation_links(authors, institutions, named_affiliations={0: ("Example",)}), ())

    def test_explicit_named_shared_and_singleton_resolution(self) -> None:
        authors = (Author("Ada Example"), Author("Bob Example"))
        institutions = (Institution("Example University"), Institution("Other University"))
        explicit = resolve_affiliation_links(
            authors, institutions, author_markers={0: ("1",)}, marker_affiliations={"1": "Example University"},
        )
        self.assertEqual([(link.author_index, link.institution_index) for link in explicit], [(0, 0)])
        shared = resolve_affiliation_links(authors, institutions, shared_affiliations=("Other University",))
        self.assertEqual([(link.author_index, link.institution_index) for link in shared], [(0, 1), (1, 1)])
        singleton = resolve_affiliation_links(authors, (institutions[0],))
        self.assertEqual([(link.author_index, link.institution_index) for link in singleton], [(0, 0), (1, 0)])

    def test_unicode_name_boundaries_and_marker_declarations_are_conservative(self) -> None:
        self.assertEqual(
            parse_author_markers("Ali¹, Li²", (Author("Li"),), ("1", "2")),
            {0: ("2",)},
        )
        document = "1 Πανεπιστήμιο\n2 Университет\n3 大学"
        alphabet = infer_marker_alphabet(document)
        self.assertEqual(alphabet, ("1", "2", "3"))
        declarations = parse_marker_affiliations("1 Example University\n1 Other University", ("1",))
        self.assertEqual(declarations, {"1": ("Example University", "Other University")})
        authors = (Author("Ada Example"),)
        institutions = (Institution("Example University"), Institution("Other University"))
        self.assertEqual(
            resolve_affiliation_links(
                authors, institutions, author_markers={0: ("1",)}, marker_affiliations=declarations,
            ),
            (),
        )
        consistent = parse_marker_affiliations("1 Example University\n1 Example University", ("1",))
        self.assertEqual(
            [(link.author_index, link.institution_index) for link in resolve_affiliation_links(
                authors, institutions, author_markers={0: ("1",)}, marker_affiliations=consistent,
            )],
            [(0, 0)],
        )

    def test_named_affiliations_union_every_explicit_match(self) -> None:
        authors = (Author("Ada Example"),)
        institutions = (Institution("Example University"), Institution("Other University"))
        links = resolve_affiliation_links(
            authors,
            institutions,
            named_affiliations={0: ("Example University", "Other University")},
        )
        self.assertEqual([(link.author_index, link.institution_index) for link in links], [(0, 0), (0, 1)])


class BibliographyMergeTests(unittest.TestCase):
    def _record(self, **values: object) -> BibliographyRecord:
        return BibliographyRecord(key="one", title=values.pop("title", "A Paper"), **values)

    def test_priority_gap_fill_and_equal_assertion_evidence_union(self) -> None:
        high = BibliographyCandidate(
            self._record(doi="10.1/a", evidence=(SourceEvidence("high", "primary"),)), 10,
        )
        low = BibliographyCandidate(
            self._record(
                doi="10.1/a", publication_title="Journal",
                evidence=(SourceEvidence("low", "secondary"),),
            ), 1,
        )
        merged = merge_bibliography_candidates((low, high))
        self.assertEqual(merged.record.publication_title, "Journal")
        doi_assertion = next(item for item in merged.field_evidence if item.field.name == "doi")
        self.assertEqual(len(doi_assertion.evidence), 2)

    def test_lower_priority_strong_identifier_conflicts_still_block(self) -> None:
        top_missing = BibliographyCandidate(self._record(), 10)
        doi_conflict = BibliographyCandidate(self._record(doi="10.1/a"), 2)
        other_doi = BibliographyCandidate(self._record(doi="10.1/b"), 1)
        with self.assertRaisesRegex(BibliographyValidationError, "DOI identity conflict"):
            merge_bibliography_candidates((top_missing, doi_conflict, other_doi))
        with self.assertRaisesRegex(BibliographyValidationError, "arXiv identity conflict"):
            merge_bibliography_candidates((
                top_missing,
                BibliographyCandidate(self._record(arxiv_id="arXiv:1234.5678"), 2),
                BibliographyCandidate(self._record(arxiv_id="arXiv:9999.9999"), 1),
            ))
        with self.assertRaisesRegex(BibliographyValidationError, "DOI identity conflict"):
            merge_bibliography_candidates((
                BibliographyCandidate(
                    self._record(),
                    2,
                    (FieldEvidence(BibliographyField("doi", "10.1/a")),),
                ),
                BibliographyCandidate(
                    self._record(),
                    1,
                    (FieldEvidence(BibliographyField("doi", "10.1/b")),),
                ),
            ))

    def test_author_cardinality_order_and_ambiguity_block(self) -> None:
        ada = (Author("Ada Example"),)
        bob = (Author("Bob Example"),)
        first = BibliographyCandidate(self._record(authors=ada), 2)
        for other, reason in (
            (BibliographyCandidate(self._record(authors=(Author("Ada Example"), Author("Bob Example"))), 1), "conflict"),
            (BibliographyCandidate(self._record(authors=bob), 1), "unresolved"),
            (BibliographyCandidate(self._record(), 3), "unresolved"),
        ):
            with self.assertRaisesRegex(BibliographyValidationError, f"author identity {reason}"):
                merge_bibliography_candidates((first, other))

    def test_descriptive_conflicts_retain_all_evidence_and_equal_priority_is_order_independent(self) -> None:
        left = BibliographyCandidate(
            self._record(publication_title="Journal A", evidence=(SourceEvidence("a", "primary"),)), 5,
        )
        right = BibliographyCandidate(
            self._record(publication_title="Journal B", evidence=(SourceEvidence("b", "secondary"),)), 1,
        )
        merged = merge_bibliography_candidates((left, right))
        self.assertEqual(merged.record.publication_title, "Journal A")
        conflict = next(item for item in merged.conflicts if item.field_name == "publication_title")
        self.assertEqual({item.field.value for item in conflict.assertions}, {"Journal A", "Journal B"})
        self.assertEqual({e.source for item in conflict.assertions for e in item.evidence}, {"a", "b"})
        repository = Repository()
        ingested = IngestBibliographySidecars(repository).ingest_candidates((left, right))
        self.assertEqual(ingested.bibliographies[0].conflicts, merged.conflicts)
        self.assertEqual(repository.upserts[0].field_evidence, merged.field_evidence)
        tied_left = BibliographyCandidate(self._record(publication_title="Journal A"), 5)
        tied_right = BibliographyCandidate(self._record(publication_title="Journal B"), 5)
        self.assertEqual(
            merge_bibliography_candidates((tied_left, tied_right)).record.publication_title,
            merge_bibliography_candidates((tied_right, tied_left)).record.publication_title,
        )
        self.assertEqual(merge_bibliography_candidates((tied_left, tied_right)).record.publication_title, "")

    def test_title_or_doi_conflict_blocks_every_upsert_and_success_is_idempotent(self) -> None:
        repository = Repository()
        use_case = IngestBibliographySidecars(repository)
        first = BibliographyCandidate(self._record(doi="10.1/a"), 2)
        conflict = BibliographyCandidate(self._record(doi="10.1/b"), 1)
        with self.assertRaisesRegex(BibliographyValidationError, "DOI identity conflict"):
            use_case.ingest_candidates((first, conflict))
        self.assertEqual(repository.upserts, [])
        result = use_case.ingest_candidates((first,))
        use_case.ingest_candidates((first,))
        self.assertEqual(result.bibliographies[0], repository.upserts[0])
        self.assertEqual(len(repository.upserts), 2)
        with self.assertRaisesRegex(BibliographyValidationError, "title identity conflict"):
            merge_bibliography_candidates((first, BibliographyCandidate(self._record(title="Different"), 1)))

    def test_strict_author_contract(self) -> None:
        import hashlib
        text = "review text"
        sidecar = {
            "schema": "bibliography-sidecar-1",
            "zotero": {"key": "one", "title": "A Paper"},
            "authors": ["Ada Example"],
            "text_md_sha256": hashlib.sha256(text.encode()).hexdigest(),
        }
        with self.assertRaisesRegex(BibliographyValidationError, "authors\\[0\\] must be a mapping"):
            IngestBibliographySidecars(Repository()).ingest([sidecar], text_by_zotero_key={"one": text})


if __name__ == "__main__":
    unittest.main()
