"""Canonical, source-neutral paper and curation evidence models."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Paper:
    """A bibliographic record identified within one source scope."""

    source_id: str
    scope_id: str
    record_id: str
    title: str
    authors: tuple[str, ...] = ()
    abstract: str = ""
    doi: str = ""
    published: str = ""
    url: str = ""
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.scope_id.strip() or not self.record_id.strip():
            raise ValueError("source ID, scope ID, and record ID are required")
        if not self.title.strip():
            raise ValueError("paper title is required")
        object.__setattr__(self, "authors", tuple(self.authors))
        object.__setattr__(self, "tags", tuple(self.tags))


@dataclass(frozen=True, slots=True)
class Attachment:
    """Source-neutral attachment metadata; access is handled by an adapter."""

    source_id: str
    scope_id: str
    record_id: str
    attachment_id: str
    filename: str
    media_type: str = "application/pdf"
    checksum: str = ""

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.source_id,
                self.scope_id,
                self.record_id,
                self.attachment_id,
                self.filename,
            )
        ):
            raise ValueError("source, scope, record, attachment IDs, and filename are required")


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    """Stable reference to an input or generated artifact, without its contents."""

    name: str
    path: str
    fingerprint: str

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.path.strip() or not self.fingerprint.strip():
            raise ValueError("artifact name, path, and fingerprint are required")


def paper_identity_fingerprint(source_id: str, scope_id: str, record_id: str) -> str:
    """Return a collision-free fingerprint for one source-neutral paper identity."""
    encoded = json.dumps(
        [source_id, scope_id, record_id],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"identity-sha256:{hashlib.sha256(encoded).hexdigest()}"


@dataclass(frozen=True, slots=True)
class StageEvidence:
    """Artifact evidence and optional provider provenance for one Core stage."""

    stage: str
    artifacts: tuple[ArtifactRef, ...] = field(default_factory=tuple)
    fingerprint: str = ""
    provider_id: str = ""
    input_id: str = ""
    model_id: str = ""

    def __post_init__(self) -> None:
        if not self.stage.strip() or not self.fingerprint.strip():
            raise ValueError("stage and fingerprint are required")
        object.__setattr__(self, "artifacts", tuple(self.artifacts))
