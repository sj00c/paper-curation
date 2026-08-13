"""Provider-neutral cited-by analysis use case."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Protocol

from paper_curation.domain.bibliography import (
    BibliographyRecord,
    BibliographyValidationError,
    CitedByResult,
    CitingPaper,
    SourceEvidence,
)


class CitingSource(Protocol):
    """The selected provider of papers citing a target record."""

    @property
    def name(self) -> str:
        """Stable provenance label for this provider."""

    def fetch(self, target: BibliographyRecord) -> Iterable[Mapping[str, object]]:
        """Return citing-paper metadata or raise the provider failure unchanged."""


class CitedByAnalyzer(Protocol):
    """Application-specific analysis over provider-neutral citing papers."""

    def analyze(
        self,
        topic: str,
        target: BibliographyRecord,
        citing_papers: tuple[CitingPaper, ...],
    ) -> object:
        """Analyze papers for any caller-supplied topic."""


class CitingSourceError(RuntimeError):
    """The selected citing source failed without exposing provider details."""


def _text(value: object, path: str, *, required: bool = False) -> str:
    if value is None and not required:
        return ""
    if not isinstance(value, str):
        raise BibliographyValidationError(f"{path} must be text")
    result = value.strip()
    if required and not result:
        raise BibliographyValidationError(f"{path} must not be empty")
    return result


def _candidate(value: Mapping[str, object], source_name: str) -> CitingPaper:
    grade = _text(value.get("evidence_grade"), "citing.evidence_grade") or "secondary"
    locator = _text(value.get("url", value.get("locator")), "citing.locator")
    return CitingPaper(
        title=_text(value.get("title"), "citing.title", required=True),
        doi=_text(value.get("doi", value.get("DOI")), "citing.doi"),
        arxiv_id=_text(value.get("arxiv_id", value.get("arxiv")), "citing.arxiv_id"),
        evidence=(SourceEvidence(source_name, grade, locator),),  # type: ignore[arg-type]
    )


def _merge_evidence(*groups: tuple[SourceEvidence, ...]) -> tuple[SourceEvidence, ...]:
    retained: list[SourceEvidence] = []
    for evidence in groups:
        for item in evidence:
            if item not in retained:
                retained.append(item)
    return tuple(retained)


def deduplicate_citing_papers(papers: Iterable[CitingPaper]) -> tuple[CitingPaper, ...]:
    """Merge papers connected by DOI, arXiv ID, or normalized title identity."""
    groups: list[list[CitingPaper]] = []
    group_keys: list[set[str]] = []
    for paper in papers:
        matches = [index for index, keys in enumerate(group_keys) if keys & paper.identity_keys]
        if not matches:
            groups.append([paper])
            group_keys.append(set(paper.identity_keys))
            continue

        first = matches[0]
        groups[first].append(paper)
        group_keys[first].update(paper.identity_keys)
        # A paper can bridge previously separate DOI/arXiv/title groups.
        for index in reversed(matches[1:]):
            groups[first].extend(groups[index])
            group_keys[first].update(group_keys[index])
            del groups[index]
            del group_keys[index]

    deduplicated: list[CitingPaper] = []
    for group in groups:
        preferred = next((paper for paper in group if paper.doi), group[0])
        arxiv_id = preferred.arxiv_id or next((paper.arxiv_id for paper in group if paper.arxiv_id), "")
        deduplicated.append(CitingPaper(
            title=preferred.title,
            doi=preferred.doi,
            arxiv_id=arxiv_id,
            evidence=_merge_evidence(*(paper.evidence for paper in group)),
        ))
    return tuple(deduplicated)


class AnalyzeCitedBy:
    """Fetch once from the selected source, deduplicate, then analyze the result."""

    def __init__(self, source: CitingSource, analyzer: CitedByAnalyzer) -> None:
        self._source = source
        self._analyzer = analyzer

    def analyze(self, target: BibliographyRecord, *, topic: str) -> CitedByResult:
        source_name = _text(self._source.name, "citing source name", required=True)
        normalized_topic = _text(topic, "topic", required=True)
        # Deliberately no retry or secondary-provider path: the caller selected this source.
        try:
            raw_papers = tuple(self._source.fetch(target))
        except Exception:
            raise CitingSourceError(f"citing source {source_name} failed") from None
        candidates = tuple(_candidate(value, source_name) for value in raw_papers)
        papers = deduplicate_citing_papers(candidates)
        analysis = self._analyzer.analyze(normalized_topic, target, papers)
        return CitedByResult(target, normalized_topic, source_name, papers, analysis)
