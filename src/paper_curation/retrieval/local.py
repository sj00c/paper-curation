"""Read-only local implementations of the retrieval ports.

The adapter deliberately consumes only promoted Core paper directories.  A
receipt is revalidated on every catalog read; it is not a cache builder.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from typing import Any
import unicodedata

from paper_curation.application.retrieve import RetrievalUseCase
from paper_curation.domain.retrieval import Chunk, Hit, IndexMetadata, Query, RetrievalValidationError


_SHA256 = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$")
_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_CHUNK_SIZE = 1_200


def _identifier_hash(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty identifier")
    if (
        value in {".", ".."}
        or "/" in value
        or "\\" in value
        or "\x00" in value
        or Path(value).is_absolute()
    ):
        raise ValueError(f"{label} must not contain a path")
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _matches_digest(value: object, digest: str) -> bool:
    return isinstance(value, str) and _SHA256.fullmatch(value) is not None and value.removeprefix("sha256:") == digest


def _tokens(text: str) -> tuple[str, ...]:
    """Return case-folded Unicode letter/number words without locale state."""
    normalized = unicodedata.normalize("NFKC", text).casefold()
    words: list[str] = []
    current: list[str] = []
    for character in normalized:
        category = unicodedata.category(character)
        if category[0] in {"L", "N"} or (category[0] == "M" and current):
            current.append(character)
        elif current:
            words.append("".join(current))
            current = []
    if current:
        words.append("".join(current))
    return tuple(words)


def _split_sections(text: str) -> tuple[tuple[str, str], ...]:
    """Split markdown-like text into bounded, named, deterministic fragments."""
    sections: list[tuple[str, list[str]]] = []
    name = "Text"
    lines: list[str] = []
    for line in text.splitlines():
        heading = _HEADING.match(line)
        if heading:
            if "".join(lines).strip():
                sections.append((name, lines))
            name = heading.group(2).strip()
            lines = []
        else:
            lines.append(line)
    if "".join(lines).strip():
        sections.append((name, lines))

    output: list[tuple[str, str]] = []
    for section, raw_lines in sections:
        paragraphs = [part.strip() for part in "\n".join(raw_lines).split("\n\n") if part.strip()]
        current = ""
        for paragraph in paragraphs:
            if current and len(current) + len(paragraph) + 2 > _CHUNK_SIZE:
                output.append((section, current))
                current = ""
            while len(paragraph) > _CHUNK_SIZE:
                boundary = paragraph.rfind(" ", 0, _CHUNK_SIZE + 1)
                boundary = boundary if boundary > 0 else _CHUNK_SIZE
                if current:
                    output.append((section, current))
                    current = ""
                output.append((section, paragraph[:boundary].strip()))
                paragraph = paragraph[boundary:].strip()
            current = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if current:
            output.append((section, current))
    return tuple(output)


class LocalIndexCatalog:
    """Load one configured source/scope from committed, verified Core outputs."""

    def __init__(self, workspace_root: Path | str, topic: str, source_id: str, scope_id: str) -> None:
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("topic must be a non-empty string")
        self._root = Path(workspace_root).expanduser().resolve()
        self._topic = topic
        self._source_id = source_id
        self._scope_id = scope_id
        self._source_hash = _identifier_hash(source_id, "source_id")
        self._scope_hash = _identifier_hash(scope_id, "scope_id")

    def get(self, topic: str) -> IndexMetadata:
        if topic != self._topic:
            raise RetrievalValidationError("requested topic is not configured for this catalog")
        scope = self._root / "papers" / self._source_hash / self._scope_hash
        if not scope.is_dir() or scope.is_symlink():
            return IndexMetadata(topic=self._topic, dimension=1, chunks=())
        chunks: list[Chunk] = []
        for paper_dir in sorted(scope.iterdir(), key=lambda path: path.name):
            if not paper_dir.is_dir() or paper_dir.is_symlink():
                continue
            chunks.extend(self._paper_chunks(paper_dir))
        return IndexMetadata(topic=self._topic, dimension=1, chunks=tuple(sorted(chunks, key=lambda chunk: chunk.chunk_id)))

    def _paper_chunks(self, paper_dir: Path) -> tuple[Chunk, ...]:
        receipt_path = paper_dir / "receipt.json"
        text_path = paper_dir / "text.txt"
        try:
            self._safe_file(receipt_path)
            self._safe_file(text_path)
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            record_id = self._verified_record(receipt, paper_dir, text_path)
            text = text_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError, KeyError):
            raise RetrievalValidationError("committed Core receipt is invalid") from None
        if not text.strip():
            raise RetrievalValidationError("committed Core receipt is invalid")
        chunks: list[Chunk] = []
        for ordinal, (section, content) in enumerate(_split_sections(text), start=1):
            identity = hashlib.sha256(
                f"{self._source_id}\n{self._scope_id}\n{record_id}\n{section}\n{ordinal}\n{content}".encode("utf-8")
            ).hexdigest()
            chunks.append(Chunk(identity, record_id, section, content))
        return tuple(chunks)

    def _verified_record(self, receipt: Any, paper_dir: Path, text_path: Path) -> str:
        if not isinstance(receipt, dict) or receipt.get("schema_version") != 1:
            raise ValueError("invalid receipt")
        paper = receipt.get("paper")
        if not isinstance(paper, dict):
            raise ValueError("invalid receipt")
        source_id, scope_id, record_id = (paper.get(key) for key in ("source_id", "scope_id", "record_id"))
        if source_id != self._source_id or scope_id != self._scope_id or not isinstance(record_id, str):
            raise ValueError("invalid receipt")
        if _identifier_hash(record_id, "record_id") != paper_dir.name:
            raise ValueError("invalid receipt")
        stages = receipt.get("stages")
        if not isinstance(stages, list):
            raise ValueError("invalid receipt")
        text_stages = [
            (stage, artifact)
            for stage in stages
            if isinstance(stage, dict) and stage.get("stage") == "extract_text"
            for artifact in (stage.get("artifacts"),)
            if isinstance(artifact, list)
            for artifact in artifact
            if isinstance(artifact, dict)
        ]
        if len(text_stages) != 1:
            raise ValueError("invalid receipt")
        stage, artifact = text_stages[0]
        if artifact.get("name") not in {"text", "text.txt"}:
            raise ValueError("invalid receipt")
        if stage.get("fingerprint") != artifact.get("fingerprint"):
            raise ValueError("invalid receipt")
        artifact_path = Path(str(artifact.get("path", ""))).expanduser()
        expected = text_path.resolve()
        resolved = (artifact_path if artifact_path.is_absolute() else self._root / artifact_path).resolve(strict=False)
        if resolved != expected or not _matches_digest(artifact.get("fingerprint"), _digest(text_path)):
            raise ValueError("invalid receipt")
        return record_id

    def _safe_file(self, path: Path) -> None:
        if not path.is_file() or path.is_symlink():
            raise ValueError("unsafe artifact")
        resolved = path.resolve(strict=True)
        if resolved != path or not resolved.is_relative_to(self._root):
            raise ValueError("unsafe artifact")


class LocalLexicalRetriever:
    """Deterministic provider-free Unicode lexical retriever."""

    def search(self, index: IndexMetadata, query: Query, limit: int) -> tuple[Hit, ...]:
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            raise RetrievalValidationError("retrieval limit must be a positive integer")
        query_terms = set(_tokens(query.text))
        if not query_terms:
            return ()
        scored: list[tuple[float, Chunk]] = []
        for chunk in index.chunks:
            counts = Counter(_tokens(chunk.text))
            matched = query_terms.intersection(counts)
            if matched:
                frequency = sum(counts[token] for token in matched)
                coverage = len(matched) / len(query_terms)
                scored.append((float(frequency) + coverage, chunk))
        scored.sort(key=lambda item: (-item[0], item[1].chunk_id))
        return tuple(
            Hit(chunk.chunk_id, chunk.slug, chunk.section, score, rank, ("lexical",))
            for rank, (score, chunk) in enumerate(scored[:limit], start=1)
        )


def local_lexical_retrieval_use_case(
    workspace_root: Path | str, topic: str, source_id: str, scope_id: str
) -> RetrievalUseCase:
    """Construct the official local lexical-only retrieval use case."""
    return RetrievalUseCase(LocalIndexCatalog(workspace_root, topic, source_id, scope_id), LocalLexicalRetriever())

