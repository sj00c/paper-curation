"""PyMuPDF implementation of the Core text extraction port."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from paper_curation.domain.papers import ArtifactRef, Paper
from paper_curation.integrations.persistence.filesystem import (
    _PaperPaths,
    _artifact,
    _checked_artifact,
    _write_bytes,
)


@dataclass(frozen=True, slots=True)
class PyMuPDFTextExtractor:
    """Extract meaningful UTF-8 text from the selected PDF into paper staging."""

    workspace_root: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "workspace_root", Path(self.workspace_root))

    def extract(self, paper: Paper, source: ArtifactRef) -> ArtifactRef:
        paths = _PaperPaths(self.workspace_root)
        pdf_path = _checked_artifact(paths, paper, source)

        try:
            import fitz
        except ImportError as exc:  # pragma: no cover - environment configuration failure
            raise RuntimeError("PyMuPDF is required for PDF text extraction") from exc

        try:
            with fitz.open(pdf_path) as document:
                text = "\n".join(page.get_text("text") for page in document)
        except Exception as exc:
            raise ValueError("selected PDF could not be read") from exc
        if not _meaningful(text):
            raise ValueError("selected PDF contains no meaningful text")

        staged = paths.staged_output(paper, "text.txt")
        _write_bytes(staged, text.encode("utf-8"))
        return _artifact("text", paths.output(paper, "text.txt"), staged)


def _meaningful(text: str) -> bool:
    return any(character.isalnum() for character in text)
