"""Zotero boundary contracts.

Concrete adapters own authentication, HTTP, and local Zotero access.  This module deliberately
contains only structural contracts so importing it cannot perform provider work.
"""

from __future__ import annotations

from typing import Protocol

from paper_curation.domain.papers import Attachment, Paper


class ZoteroReader(Protocol):
    """Read-only Zotero operations used by curation."""

    def list_collection(self, collection_key: str) -> tuple[Paper, ...]: ...

    def list_attachments(self, paper_key: str) -> tuple[Attachment, ...]: ...


class ZoteroMutator(Protocol):
    """Explicit, opt-in Zotero mutations."""

    def mark_curated(self, paper_key: str) -> None: ...


class ZoteroGateway(ZoteroReader, ZoteroMutator, Protocol):
    """Complete adapter contract; reads never imply a mutation."""
