"""Persistence boundary for canonical bibliography records."""

from __future__ import annotations

from paper_curation.application.bibliography import (
    BibliographyRepository,
    BibliographyTransaction,
)

__all__ = ["BibliographyRepository", "BibliographyTransaction"]
