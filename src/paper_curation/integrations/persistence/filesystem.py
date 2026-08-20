"""Local filesystem implementations of the Core persistence ports."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from paper_curation.domain.papers import (
    ArtifactRef,
    Paper,
    StageEvidence,
    paper_identity_fingerprint,
)


_SOURCE_NAME = "source.pdf"
_TEXT_NAME = "text.txt"
_REVIEW_NAME = "review.md"
_SIDECAR_NAME = "sidecar.json"
_PAGE_NAME = "index.html"
_RECEIPT_NAME = "receipt.json"
_CORE_ARTIFACTS = (
    ("identify", None, None),
    ("materialize_source", "source-pdf", _SOURCE_NAME),
    ("extract_text", "text", _TEXT_NAME),
    ("generate_review", "review.md", _REVIEW_NAME),
    ("write_sidecar", "sidecar", _SIDECAR_NAME),
    ("render_page", "page", _PAGE_NAME),
)


@dataclass(frozen=True, slots=True)
class _PaperPaths:
    root: Path

    def __post_init__(self) -> None:
        root = Path(self.root).expanduser()
        if not root.is_absolute():
            root = Path.cwd() / root
        object.__setattr__(self, "root", root)
        self._check_workspace()

    def _check_workspace(self) -> None:
        if any(candidate.is_symlink() for candidate in (self.root, *self.root.parents)):
            raise ValueError("workspace ownership boundary contains a symlink")
        for path in (self.root, self.root / "papers", self.root / ".staging"):
            if path.is_symlink():
                raise ValueError("workspace ownership boundary contains a symlink")
            if path.exists() and not path.is_dir():
                raise ValueError("workspace ownership boundary is not a directory")

    def _check_owned_path(self, path: Path) -> None:
        self._check_workspace()
        try:
            relative = path.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("path escapes the workspace") from exc
        current = self.root
        for part in relative.parts:
            current /= part
            if current.is_symlink():
                raise ValueError("workspace ownership boundary contains a symlink")
        try:
            path.resolve(strict=False).relative_to(self.root.resolve(strict=False))
        except ValueError as exc:
            raise ValueError("path escapes the workspace") from exc

    def check_staged_write(self, path: Path) -> None:
        try:
            path.relative_to(self.root / ".staging")
        except ValueError as exc:
            raise ValueError("write is outside paper staging") from exc
        self._check_owned_path(path)

    def check_canonical_write(self, path: Path) -> None:
        try:
            path.relative_to(self.root / "papers")
        except ValueError as exc:
            raise ValueError("write is outside paper output") from exc
        self._check_owned_path(path)

    def canonical(self, paper: Paper) -> Path:
        return self.root / "papers" / _paper_key(paper)

    def staging(self, paper: Paper) -> Path:
        return self.root / ".staging" / _paper_key(paper)

    def output(self, paper: Paper, name: str) -> Path:
        return self.canonical(paper) / name

    def staged_output(self, paper: Paper, name: str) -> Path:
        return self.staging(paper) / name

    def staged_for(self, paper: Paper, path: Path) -> Path:
        """Resolve an output ref to its staged file before receipt promotion."""
        canonical = self.canonical(paper)
        try:
            relative = path.resolve(strict=False).relative_to(canonical)
        except ValueError:
            return path
        return self.staging(paper) / relative


def _safe_id(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty identifier")
    candidate = Path(value)
    if (
        value in {".", ".."}
        or candidate.is_absolute()
        or len(candidate.parts) != 1
        or "/" in value
        or "\\" in value
        or "\x00" in value
    ):
        raise ValueError(f"{label} must not contain a path")
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _paper_key(paper: Paper) -> Path:
    return Path(
        _safe_id(paper.source_id, "source_id"),
        _safe_id(paper.scope_id, "scope_id"),
        _safe_id(paper.record_id, "record_id"),
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as artifact:
        for chunk in iter(lambda: artifact.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _staging_paths(path: Path) -> _PaperPaths | None:
    absolute = path.expanduser()
    if not absolute.is_absolute():
        absolute = Path.cwd() / absolute
    for parent in (absolute.parent, *absolute.parents):
        if parent.name == ".staging":
            paths = _PaperPaths(parent.parent)
            paths.check_staged_write(absolute)
            return paths
    return None


def _write_bytes(path: Path, content: bytes) -> None:
    paths = _staging_paths(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if paths:
        paths.check_staged_write(path)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        if paths:
            paths.check_staged_write(temporary)
        with temporary.open("xb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        if paths:
            paths.check_staged_write(path)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _copy_file(path: Path, source: Path) -> None:
    paths = _staging_paths(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if paths:
        paths.check_staged_write(path)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        if paths:
            paths.check_staged_write(temporary)
        with source.open("rb") as input_file, temporary.open("xb") as output:
            shutil.copyfileobj(input_file, output, length=1024 * 1024)
            output.flush()
            os.fsync(output.fileno())
        if paths:
            paths.check_staged_write(path)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _artifact(name: str, logical_path: Path, actual_path: Path) -> ArtifactRef:
    return ArtifactRef(name, str(logical_path), _sha256(actual_path))


def _fingerprint_matches(path: Path, fingerprint: str) -> bool:
    digest = _sha256(path)
    return fingerprint in {digest, f"sha256:{digest}"}


def _checked_artifact(paths: _PaperPaths, paper: Paper, artifact: ArtifactRef) -> Path:
    path = Path(artifact.path).expanduser()
    if not path.is_absolute():
        if ".." in path.parts:
            raise ValueError("artifact path escapes the workspace")
        path = paths.root / path
    expected = paths.output(paper, _artifact_filename(artifact.name))
    staged = paths.staged_output(paper, _artifact_filename(artifact.name))
    if path == expected:
        paths.check_canonical_write(expected)
        paths.check_staged_write(staged)
        if staged.is_file() and _fingerprint_matches(staged, artifact.fingerprint):
            return staged
        if not paths.staging(paper).exists() and expected.is_file() and _fingerprint_matches(
            expected, artifact.fingerprint
        ):
            _copy_file(staged, expected)
            return staged
        raise ValueError(f"artifact fingerprint is invalid: {artifact.name}")
    raise ValueError(f"artifact fingerprint is invalid: {artifact.name}")


def _artifact_filename(name: str) -> str:
    for _, artifact_name, filename in _CORE_ARTIFACTS:
        if artifact_name == name:
            assert filename is not None
            return filename
    raise ValueError(f"artifact name is invalid: {name}")


def _paper_payload(paper: Paper) -> dict[str, Any]:
    return {
        "source_id": paper.source_id,
        "scope_id": paper.scope_id,
        "record_id": paper.record_id,
        "title": paper.title,
        "authors": list(paper.authors),
        "abstract": paper.abstract,
        "doi": paper.doi,
        "published": paper.published,
        "url": paper.url,
        "tags": list(paper.tags),
    }


@dataclass(frozen=True, slots=True)
class FilesystemStagedAttachment:
    """Copy one exact materialized PDF into the atomic paper staging area."""

    workspace_root: Path
    delegate: Any

    def materialize(self, paper: Paper, attachment: Any) -> ArtifactRef:
        generated = self.delegate.materialize(paper, attachment)
        raw_source = Path(generated.path).expanduser()
        if raw_source.is_symlink() or any(
            parent.is_symlink() for parent in raw_source.parents
        ):
            raise ValueError("materialized source is not a regular file")
        source = raw_source.resolve(strict=True)
        if not source.is_file():
            raise ValueError("materialized source is not a regular file")
        if not _fingerprint_matches(source, generated.fingerprint):
            raise ValueError("materialized source fingerprint is invalid")
        paths = _PaperPaths(self.workspace_root)
        staged = paths.staged_output(paper, _SOURCE_NAME)
        _copy_file(staged, source)
        if not _fingerprint_matches(staged, generated.fingerprint):
            raise ValueError("materialized source changed while staging")
        return _artifact("source-pdf", paths.output(paper, _SOURCE_NAME), staged)


@dataclass(frozen=True, slots=True)
class FilesystemSidecar:
    """Write provenance-only sidecars into a paper's staging directory."""

    workspace_root: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "workspace_root", Path(self.workspace_root))

    def write(
        self,
        paper: Paper,
        text: ArtifactRef,
        review: ArtifactRef,
        review_provider_id: str,
        review_model_id: str,
    ) -> ArtifactRef:
        if not review_provider_id.strip():
            raise ValueError("review provider ID is required")
        if not review_model_id.strip():
            raise ValueError("review model ID is required")
        paths = _PaperPaths(self.workspace_root)
        _checked_artifact(paths, paper, text)
        _checked_artifact(paths, paper, review)
        payload = {
            "schema_version": 1,
            "paper": _paper_payload(paper),
            "text_sha256": text.fingerprint,
            "review_sha256": review.fingerprint,
            "review_provider_id": review_provider_id,
            "review_model_id": review_model_id,
        }
        staged = paths.staged_output(paper, _SIDECAR_NAME)
        _write_bytes(
            staged,
            (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )
        return _artifact("sidecar", paths.output(paper, _SIDECAR_NAME), staged)


@dataclass(frozen=True, slots=True)
class FilesystemStagedReview:
    """Stage and verify a provider review before the Core receipt promotes it."""

    workspace_root: Path
    provider: Any

    def __post_init__(self) -> None:
        object.__setattr__(self, "workspace_root", Path(self.workspace_root))

    def write(self, paper: Paper, text: ArtifactRef) -> ArtifactRef:
        paths = _PaperPaths(self.workspace_root)
        text_path = _checked_artifact(paths, paper, text)
        provider_text = ArtifactRef(text.name, str(text_path), text.fingerprint)
        generated = self.provider.write(paper, provider_text)
        raw_generated = Path(generated.path).expanduser()
        owned_root = paths.root / ".review-provider"
        paths._check_owned_path(owned_root)
        if not raw_generated.is_absolute() or ".." in raw_generated.parts:
            raise ValueError("provider review artifact path is invalid")
        resolved_owned_root = owned_root.resolve(strict=True)
        try:
            raw_generated.resolve(strict=True).relative_to(resolved_owned_root)
        except ValueError as exc:
            raise ValueError("provider review artifact is outside its owned root") from exc
        paths._check_owned_path(raw_generated)
        if raw_generated.is_symlink():
            raise ValueError("provider review artifact must not be a symlink")
        generated_path = raw_generated.resolve(strict=True)
        if not generated_path.is_file() or not _fingerprint_matches(
            generated_path, generated.fingerprint
        ):
            raise ValueError("provider review artifact fingerprint is invalid")
        staged = paths.staged_output(paper, _REVIEW_NAME)
        _copy_file(staged, generated_path)
        if not _fingerprint_matches(staged, generated.fingerprint):
            raise ValueError("provider review changed while staging")
        return _artifact("review.md", paths.output(paper, _REVIEW_NAME), staged)


@dataclass(frozen=True, slots=True)
class FilesystemPage:
    """Render a self-contained, escaped local HTML page from Core outputs."""

    workspace_root: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "workspace_root", Path(self.workspace_root))

    def render(self, paper: Paper, review: ArtifactRef, sidecar: ArtifactRef) -> ArtifactRef:
        paths = _PaperPaths(self.workspace_root)
        review_path = _checked_artifact(paths, paper, review)
        sidecar_path = _checked_artifact(paths, paper, sidecar)
        try:
            review_markdown = review_path.read_text(encoding="utf-8")
            metadata = json.loads(sidecar_path.read_text(encoding="utf-8"))
            metadata_paper = metadata["paper"]
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
            raise ValueError("sidecar or review is not loadable") from exc
        if not review_markdown.strip():
            raise ValueError("review is empty")
        if not isinstance(metadata_paper, dict):
            raise ValueError("sidecar paper metadata is invalid")
        page = _render_page(metadata_paper, review_markdown)
        staged = paths.staged_output(paper, _PAGE_NAME)
        _write_bytes(staged, page.encode("utf-8"))
        return _artifact("page", paths.output(paper, _PAGE_NAME), staged)


@dataclass(frozen=True, slots=True)
class FilesystemReceipt:
    """Verify Core artifacts and atomically promote one staged paper directory."""

    workspace_root: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "workspace_root", Path(self.workspace_root))

    def commit(self, paper: Paper, evidence: tuple[StageEvidence, ...]) -> ArtifactRef:
        paths = _PaperPaths(self.workspace_root)
        self._validate_evidence(paths, paper, evidence, allow_complete_canonical=True)
        self._seed_complete_resumed_staging(paths, paper, evidence)
        self._validate_evidence(paths, paper, evidence)
        self._validate_staging_tree(paths, paper, include_receipt=False)
        receipt = {
            "schema_version": 1,
            "paper": {
                "source_id": paper.source_id,
                "scope_id": paper.scope_id,
                "record_id": paper.record_id,
            },
            "stages": [_receipt_stage(stage) for stage in evidence],
        }
        staged_receipt = paths.staged_output(paper, _RECEIPT_NAME)
        _write_bytes(
            staged_receipt,
            (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )
        self._validate_staging_tree(paths, paper, include_receipt=True)
        self._promote(paths, paper)
        canonical_receipt = paths.output(paper, _RECEIPT_NAME)
        return _artifact("receipt", canonical_receipt, canonical_receipt)

    @staticmethod
    def _validate_evidence(
        paths: _PaperPaths,
        paper: Paper,
        evidence: tuple[StageEvidence, ...],
        *,
        allow_complete_canonical: bool = False,
    ) -> None:
        if len(evidence) != len(_CORE_ARTIFACTS):
            raise ValueError("receipt requires complete Core evidence")
        for stage, (expected_stage, expected_name, expected_file) in zip(
            evidence, _CORE_ARTIFACTS, strict=True
        ):
            if stage.stage != expected_stage:
                raise ValueError("receipt Core stage is invalid")
            if expected_stage == "materialize_source" and not stage.input_id.strip():
                raise ValueError("receipt source input identity is required")
            if expected_stage == "generate_review" and (
                not stage.provider_id.strip() or not stage.model_id.strip()
            ):
                raise ValueError("receipt review provider and model are required")
            if expected_name is None:
                expected = paper_identity_fingerprint(
                    paper.source_id, paper.scope_id, paper.record_id
                )
                if stage.artifacts or stage.fingerprint != expected:
                    raise ValueError("receipt identity evidence is invalid")
                continue
            if len(stage.artifacts) != 1:
                raise ValueError("receipt artifact count is invalid")
            artifact = stage.artifacts[0]
            expected_path = paths.output(paper, expected_file)
            if (
                artifact.name != expected_name
                or Path(artifact.path) != expected_path
                or stage.fingerprint != artifact.fingerprint
            ):
                raise ValueError("receipt artifact contract is invalid")
            staged = paths.staged_output(paper, expected_file)
            paths.check_staged_write(staged)
            valid_staged = (
                staged.is_file()
                and not staged.is_symlink()
                and _fingerprint_matches(staged, artifact.fingerprint)
            )
            valid_canonical = (
                allow_complete_canonical
                and not paths.staging(paper).exists()
                and expected_path.is_file()
                and not expected_path.is_symlink()
                and _fingerprint_matches(expected_path, artifact.fingerprint)
            )
            if not valid_staged and not valid_canonical:
                raise ValueError(f"artifact fingerprint is invalid: {artifact.name}")

    @staticmethod
    def _seed_complete_resumed_staging(
        paths: _PaperPaths, paper: Paper, evidence: tuple[StageEvidence, ...]
    ) -> None:
        staged = paths.staging(paper)
        if staged.exists():
            return
        for stage, (_, expected_name, expected_file) in zip(evidence, _CORE_ARTIFACTS, strict=True):
            if expected_name is None:
                continue
            artifact = stage.artifacts[0]
            canonical = paths.output(paper, expected_file)
            if not canonical.is_file() or canonical.is_symlink() or not _fingerprint_matches(
                canonical, artifact.fingerprint
            ):
                raise ValueError(f"resumed artifact fingerprint is invalid: {artifact.name}")
            _copy_file(paths.staged_output(paper, expected_file), canonical)

    @staticmethod
    def _validate_staging_tree(paths: _PaperPaths, paper: Paper, *, include_receipt: bool) -> None:
        staged = paths.staging(paper)
        paths.check_staged_write(staged)
        if not staged.is_dir() or staged.is_symlink():
            raise ValueError("paper staging directory is missing")
        expected = {filename for _, _, filename in _CORE_ARTIFACTS if filename}
        if include_receipt:
            expected.add(_RECEIPT_NAME)
        files: set[str] = set()
        for parent, directories, names in os.walk(staged, followlinks=False):
            parent_path = Path(parent)
            for directory in directories:
                if (parent_path / directory).is_symlink():
                    raise ValueError("paper staging contains a symlink")
            for name in names:
                candidate = parent_path / name
                if candidate.is_symlink() or not candidate.is_file():
                    raise ValueError("paper staging contains an invalid entry")
                files.add(str(candidate.relative_to(staged)))
        if files != expected:
            raise ValueError("paper staging tree is incomplete")

    @staticmethod
    def _promote(paths: _PaperPaths, paper: Paper) -> None:
        staged = paths.staging(paper)
        canonical = paths.canonical(paper)
        paths.check_staged_write(staged)
        paths.check_canonical_write(canonical)
        if not staged.is_dir() or staged.is_symlink():
            raise ValueError("paper staging directory is missing")
        canonical.parent.mkdir(parents=True, exist_ok=True)
        paths.check_canonical_write(canonical)
        backup = canonical.with_name(f".{canonical.name}.{uuid.uuid4().hex}.backup")
        moved_previous = False
        try:
            if canonical.exists():
                paths.check_canonical_write(canonical)
                os.replace(canonical, backup)
                moved_previous = True
            paths.check_staged_write(staged)
            paths.check_canonical_write(canonical)
            os.replace(staged, canonical)
        except Exception:
            if moved_previous and backup.exists() and not canonical.exists():
                paths.check_canonical_write(canonical)
                os.replace(backup, canonical)
            raise
        if backup.exists():
            shutil.rmtree(backup, ignore_errors=True)


@dataclass(frozen=True, slots=True)
class FilesystemEvidenceVerifier:
    """Recompute each artifact digest for resumable Core evidence."""

    workspace_root: Path

    def valid(self, paper: Paper, evidence: tuple[StageEvidence, ...]) -> bool:
        try:
            paths = _PaperPaths(self.workspace_root)
            for stage in evidence:
                if stage.stage == "identify":
                    if (
                        stage.artifacts
                        or stage.fingerprint
                        != paper_identity_fingerprint(
                            paper.source_id, paper.scope_id, paper.record_id
                        )
                    ):
                        return False
                    continue
                if len(stage.artifacts) != 1:
                    return False
                artifact = stage.artifacts[0]
                if stage.stage == "commit_receipt":
                    expected_name, filename = "receipt", _RECEIPT_NAME
                else:
                    expected_name = next(
                        (
                            name
                            for name_stage, name, _ in _CORE_ARTIFACTS
                            if name_stage == stage.stage
                        ),
                        None,
                    )
                    filename = next(
                        (
                            file
                            for name_stage, _, file in _CORE_ARTIFACTS
                            if name_stage == stage.stage
                        ),
                        None,
                    )
                if (
                    expected_name is None
                    or filename is None
                    or artifact.name != expected_name
                    or stage.fingerprint != artifact.fingerprint
                ):
                    return False
                path = Path(artifact.path).expanduser()
                expected = paths.output(paper, filename)
                if path != expected:
                    return False
                try:
                    paths.check_canonical_write(expected)
                    staged = paths.staged_output(paper, filename)
                    paths.check_staged_write(staged)
                except (OSError, ValueError):
                    return False
                if not any(
                    candidate.is_file() and _fingerprint_matches(candidate, artifact.fingerprint)
                    for candidate in (expected, staged)
                ):
                    return False
            if evidence and evidence[-1].stage == "commit_receipt":
                receipt_path = Path(evidence[-1].artifacts[0].path)
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                if receipt.get("paper") != {
                    "source_id": paper.source_id,
                    "scope_id": paper.scope_id,
                    "record_id": paper.record_id,
                } or receipt.get("stages") != [
                    _receipt_stage(stage) for stage in evidence[:-1]
                ]:
                    return False
            return True
        except (OSError, ValueError):
            return False


def _receipt_stage(stage: StageEvidence) -> dict[str, Any]:
    return {
        "stage": stage.stage,
        "fingerprint": stage.fingerprint,
        "provider_id": stage.provider_id,
        "input_id": stage.input_id,
        "model_id": stage.model_id,
        "artifacts": [
            {"name": artifact.name, "path": artifact.path, "fingerprint": artifact.fingerprint}
            for artifact in stage.artifacts
        ],
    }


def _render_page(metadata: dict[str, Any], review_markdown: str) -> str:
    title = _as_text(metadata.get("title"))
    authors = metadata.get("authors", [])
    if not isinstance(authors, list):
        authors = []
    author_line = ", ".join(_as_text(author) for author in authors if _as_text(author))
    abstract = _as_text(metadata.get("abstract"))
    review_html = _markdown_as_safe_html(review_markdown)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>{html.escape(title, quote=True)}</title>
<style>
body {{ font-family: system-ui, sans-serif; line-height: 1.55; color: #18212f; max-width: 880px; margin: 2rem auto; padding: 0 1rem; }}
article {{ border: 1px solid #d8dee8; border-radius: .5rem; padding: 1.5rem; }}
h1 {{ margin-top: 0; }} .authors {{ color: #4b5563; }} .abstract {{ background: #f5f7fa; padding: 1rem; border-radius: .25rem; }}
.review {{ white-space: pre-wrap; overflow-wrap: anywhere; }}
</style>
</head>
<body><article>
<h1>{html.escape(title, quote=True)}</h1>
<p class=\"authors\">{html.escape(author_line, quote=True)}</p>
<section class=\"abstract\"><h2>Abstract</h2><p>{html.escape(abstract, quote=True)}</p></section>
<section><h2>Review</h2><div class=\"review\">{review_html}</div></section>
</article></body>
</html>
"""


def _as_text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _markdown_as_safe_html(markdown: str) -> str:
    """Keep markdown readable without trusting it as HTML."""
    escaped = html.escape(markdown, quote=True)
    escaped = re.sub(r"(?m)^### (.+)$", r"<h4>\1</h4>", escaped)
    escaped = re.sub(r"(?m)^## (.+)$", r"<h3>\1</h3>", escaped)
    escaped = re.sub(r"(?m)^# (.+)$", r"<h2>\1</h2>", escaped)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return escaped
