"""Synthetic contracts for pure bibliography-domain intake algorithms."""

from __future__ import annotations

import unittest

from paper_curation.domain.affiliations import (
    affiliation_score,
    affiliations_contradict,
    canonical_affiliation,
    match_affiliation,
)
from paper_curation.domain.author_identity import Author, canonical_author_name, decide_author_identity
from paper_curation.domain.bibliography import (
    AuthorInstitutionLink,
    BibliographyField,
    BibliographyRecord,
    BibliographyValidationError,
    CitingPaper,
    FieldEvidence,
    Institution,
    MergedBibliography,
    SourceEvidence,
    canonical_title,
    canonical_doi,
    merge_field_evidence,
    stable_evidence_union,
)


class AuthorIdentityTests(unittest.TestCase):
    def test_unicode_display_is_preserved_and_comparison_is_unicode_preserving(self) -> None:
        author = Author("  José  García  ")
        self.assertEqual(author.display_name, "José  García")
        self.assertEqual(author.identity_key, "josé garcía")
        self.assertNotEqual(canonical_author_name("José García"), canonical_author_name("Jose Garcia"))
        self.assertEqual(canonical_author_name("王 小明"), "王 小明")

    def test_name_expansion_is_ambiguous_without_shared_orcid(self) -> None:
        self.assertEqual(decide_author_identity(Author("García, J."), Author("J. García")), "same")
        self.assertEqual(decide_author_identity(Author("J Smith"), Author("John Smith")), "unresolved")
        self.assertEqual(decide_author_identity(Author("Jean-Luc Picard"), Author("Jean Luc Picard")), "unresolved")

    def test_orcid_conflicts_fail_closed(self) -> None:
        known = Author("Ada Lovelace", "0000-0002-1825-0097")
        same = Author("A. Lovelace", "https://orcid.org/0000-0002-1825-0097")
        conflict = Author("Ada Lovelace", "0000-0001-5109-3700")
        self.assertEqual(decide_author_identity(known, same), "same")
        self.assertEqual(decide_author_identity(known, conflict), "conflict")

    def test_shared_compatible_orcid_overrides_name_expansion(self) -> None:
        self.assertEqual(
            decide_author_identity(
                Author("J Smith", "0000-0002-1825-0097"),
                Author("John Smith", "0000-0002-1825-0097"),
            ),
            "same",
        )


class AffiliationTests(unittest.TestCase):
    def test_data_free_normalization_scores_and_tie_safe_matching(self) -> None:
        self.assertEqual(canonical_affiliation("Université de Paris"), "université de paris")
        self.assertEqual(affiliation_score("Example University", "Example University"), 1.0)
        candidates = (Institution("Example University"), Institution("Example Institute"))
        self.assertIs(match_affiliation("Example University", candidates), candidates[0])
        self.assertIsNone(match_affiliation("Example", candidates, minimum_score=0.1))

    def test_explicit_identifiers_and_countries_can_contradict(self) -> None:
        self.assertTrue(affiliations_contradict(Institution("A", country="KR"), Institution("A", country="US")))
        self.assertTrue(affiliations_contradict(Institution("A", ror_id="01"), Institution("A", ror_id="02")))
        self.assertFalse(affiliations_contradict(Institution("A"), Institution("B")))

    def test_match_requires_discriminative_institution_agreement(self) -> None:
        self.assertIsNone(match_affiliation("Department", (Institution("Department of Physics"),)))
        institution = Institution("Seoul National University")
        self.assertIsNone(
            match_affiliation("Department of Mathematics, Seoul National University", (institution,)),
        )
        self.assertIsNone(
            match_affiliation(
                "Alpha Beta Department",
                (Institution("Alpha Beta University"), Institution("Alpha Beta Institute")),
            )
        )
        self.assertIsNone(
            match_affiliation(
                "Department of Mathematics, University of Cambridge",
                (
                    Institution("Department of Biology, University of Cambridge"),
                    Institution("Department of Physics, University of Cambridge"),
                ),
            )
        )
        self.assertIsNone(
            match_affiliation(
                "Department of Electrical and Computer Engineering, Example University",
                (
                    Institution(
                        "Department of Electrical and Computer Science, Example University"
                    ),
                ),
            )
        )


class BibliographyIntakeTests(unittest.TestCase):
    def test_rejects_doi_templates_and_preserves_canonical_doi(self) -> None:
        self.assertEqual(canonical_doi("https://doi.org/10.1000/ABC"), "10.1000/abc")
        for placeholder in ("10.xxxx/example", "10.1234/your-doi", "10.1234/{identifier}"):
            with self.assertRaises(BibliographyValidationError):
                canonical_doi(placeholder)

    def test_link_indices_are_bounded_by_the_record(self) -> None:
        record = BibliographyRecord(
            key="paper", title="Paper", authors=(Author("Ada Lovelace"),), institutions=(Institution("Example University"),),
        )
        MergedBibliography(record, author_institution_links=(AuthorInstitutionLink(0, 0),))
        with self.assertRaises(BibliographyValidationError):
            MergedBibliography(record, author_institution_links=(AuthorInstitutionLink(1, 0),))
        with self.assertRaises(BibliographyValidationError):
            MergedBibliography(record, author_institution_links=(AuthorInstitutionLink(0, 1),))

    def test_evidence_union_is_exact_and_stable(self) -> None:
        first = SourceEvidence("source-a", "primary", "one")
        second = SourceEvidence("source-b", "secondary", "two")
        self.assertEqual(stable_evidence_union((first, second), (first,)), (first, second))
        assertion = BibliographyField("title", "Paper")
        merged = merge_field_evidence(
            FieldEvidence(assertion, (first,)),
            FieldEvidence(assertion, (second,)),
        )
        self.assertEqual(merged, (FieldEvidence(assertion, (first, second)),))

    def test_titles_are_nfc_normalized_for_identity_keys(self) -> None:
        title = "Cafe\u0301"
        self.assertEqual(canonical_title(title), canonical_title("Café"))
        self.assertEqual(
            CitingPaper(title).identity_keys,
            frozenset({"title:café"}),
        )

    def test_identified_records_do_not_use_title_identity(self) -> None:
        first = CitingPaper("Shared title", doi="10.1000/first")
        second = CitingPaper("Shared title", doi="10.1000/second")
        self.assertTrue(first.identity_keys.isdisjoint(second.identity_keys))
        record = BibliographyRecord(key="first", title="Shared title", doi="10.1000/first")
        self.assertEqual(record.identity_keys, frozenset({"doi:10.1000/first"}))

    def test_citing_paper_evidence_is_frozen_and_deduplicated(self) -> None:
        evidence = SourceEvidence("source-a", "primary", "one")
        citing = CitingPaper("Paper", evidence=(evidence, evidence))
        self.assertEqual(citing.evidence, (evidence,))


if __name__ == "__main__":
    unittest.main()
