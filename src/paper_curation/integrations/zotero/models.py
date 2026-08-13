"""Immutable Zotero records mapped to canonical domain models."""

from __future__ import annotations

from dataclasses import dataclass, field

from paper_curation.domain.papers import Attachment, Paper


@dataclass(frozen=True, slots=True)
class ZoteroPaperRecord:
    """The Zotero fields required to construct a canonical :class:`Paper`."""

    key: str
    collection_key: str
    title: str
    creators: tuple[str, ...] = field(default_factory=tuple)
    abstract_note: str = ""
    doi: str = ""
    date: str = ""
    url: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "creators", tuple(self.creators))
        object.__setattr__(self, "tags", tuple(self.tags))

    def to_paper(self) -> Paper:
        return Paper(
            key=self.key,
            title=self.title,
            collection_key=self.collection_key,
            authors=self.creators,
            abstract=self.abstract_note,
            doi=self.doi,
            published=self.date,
            url=self.url,
            tags=self.tags,
        )


@dataclass(frozen=True, slots=True)
class ZoteroAttachmentRecord:
    """Attachment metadata from Zotero, excluding local paths and credentials."""

    key: str
    parent_key: str
    filename: str
    content_type: str = "application/pdf"
    checksum: str = ""

    def to_attachment(self) -> Attachment:
        return Attachment(
            key=self.key,
            paper_key=self.parent_key,
            filename=self.filename,
            media_type=self.content_type,
            checksum=self.checksum,
        )
