"""Canonical, provider-neutral paper and generated-artifact models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Paper:
    """A bibliographic item identified by its stable provider key."""

    key: str
    title: str
    collection_key: str
    authors: tuple[str, ...] = ()
    abstract: str = ""
    doi: str = ""
    published: str = ""
    url: str = ""
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("paper key is required")
        if not self.title.strip():
            raise ValueError("paper title is required")
        if not self.collection_key.strip():
            raise ValueError("collection key is required")
        object.__setattr__(self, "authors", tuple(self.authors))
        object.__setattr__(self, "tags", tuple(self.tags))


@dataclass(frozen=True, slots=True)
class Attachment:
    """Provider-neutral attachment metadata; access is handled by an adapter."""

    key: str
    paper_key: str
    filename: str
    media_type: str = "application/pdf"
    checksum: str = ""

    def __post_init__(self) -> None:
        if not self.key.strip() or not self.paper_key.strip() or not self.filename.strip():
            raise ValueError("attachment key, paper key, and filename are required")


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    """Stable reference to a generated artifact, without retaining its contents."""

    name: str
    path: str
    fingerprint: str

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.path.strip() or not self.fingerprint.strip():
            raise ValueError("artifact name, path, and fingerprint are required")


@dataclass(frozen=True, slots=True)
class StageEvidence:
    """Artifact evidence produced by one curation stage."""

    stage: str
    artifacts: tuple[ArtifactRef, ...] = field(default_factory=tuple)
    fingerprint: str = ""

    def __post_init__(self) -> None:
        if not self.stage.strip() or not self.fingerprint.strip():
            raise ValueError("stage and fingerprint are required")
        object.__setattr__(self, "artifacts", tuple(self.artifacts))
