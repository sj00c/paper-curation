"""Filesystem adapter for local build, validation, and repair use cases."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import shutil
import stat
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

from paper_curation.application.workspace_ops import (
    BuildWorkspaceResult,
    RepairWorkspaceResult,
    ValidateWorkspaceResult,
    WorkspaceEntry,
    WorkspaceIssue,
    WorkspaceRepairAction,
)
from paper_curation.domain.papers import paper_identity_fingerprint


_PAPERS = "papers"
_RECEIPT = "receipt.json"
_PAGE = "index.html"
_STAGING = ".staging"
_SITE = "site"
_QUARANTINE = ".quarantine"
_GENERATED_NAMES = frozenset({_RECEIPT, _PAGE, "review.md", "sidecar.json", "text.txt"})
_CHUNK_SIZE = 1024 * 1024
_CORE_STAGES = (
    "identify",
    "materialize_source",
    "extract_text",
    "generate_review",
    "write_sidecar",
    "render_page",
)
_STAGE_ARTIFACTS = {
    "identify": (),
    "materialize_source": ("source-pdf", "source.pdf"),
    "extract_text": ("text", "text.txt"),
    "generate_review": ("review.md", "review.md"),
    "write_sidecar": ("sidecar", "sidecar.json"),
    "render_page": ("page", _PAGE),
}
_SITE_BACKUP = re.compile(rf"^\.{re.escape(_SITE)}\.[0-9a-f]{{32}}\.backup$")


@dataclass(frozen=True, slots=True)
class FilesystemWorkspaceOps:
    """Operate only on locally committed Core output below one workspace root."""

    workspace_root: Path
    _unsafe_input_root: bool = field(init=False, repr=False)

    def __post_init__(self) -> None:
        supplied = Path(self.workspace_root).expanduser().absolute()
        object.__setattr__(
            self,
            "_unsafe_input_root",
            any(candidate.is_symlink() for candidate in (supplied, *supplied.parents)),
        )
        object.__setattr__(self, "workspace_root", supplied.resolve())

    def build(self) -> BuildWorkspaceResult:
        _assert_safe_workspace(self.workspace_root, self._unsafe_input_root)
        _recover_site_backups(self.workspace_root)
        validation = self.validate()
        if validation.issues:
            raise ValueError("cannot build site from invalid committed Core records")
        entries = tuple(self._entries())
        site = self.workspace_root / _SITE
        staged = self.workspace_root / f".{_SITE}.{uuid.uuid4().hex}.staging"
        try:
            staged.mkdir(parents=True)
            for entry in entries:
                if _validate_record(self.workspace_root, entry.page_path.parent):
                    raise ValueError("committed Core record changed during build")
                relative = entry.page_path.relative_to(self.workspace_root / _PAPERS)
                _atomic_write(staged / _PAPERS / relative, _read_regular(entry.page_path))
            _atomic_write(staged / _PAGE, _site_html(entries).encode("utf-8"))
            _assert_safe_workspace(self.workspace_root, self._unsafe_input_root)
            for entry in entries:
                if _validate_record(self.workspace_root, entry.page_path.parent):
                    raise ValueError("committed Core record changed before promotion")
            _replace_directory(staged, site)
        finally:
            if staged.exists():
                shutil.rmtree(staged, ignore_errors=True)
        return BuildWorkspaceResult(site / _PAGE, entries)

    def validate(self) -> ValidateWorkspaceResult:
        issues: list[WorkspaceIssue] = []
        issues.extend(_workspace_safety_issues(self.workspace_root, self._unsafe_input_root))
        if issues:
            return ValidateWorkspaceResult(tuple(issues))
        records, discovery_issues = _discover_records(self.workspace_root / _PAPERS)
        issues.extend(discovery_issues)
        for record in records:
            issues.extend(_validate_record(self.workspace_root, record))
        return ValidateWorkspaceResult(tuple(sorted(issues, key=lambda issue: (str(issue.path), issue.message))))

    def repair(self, *, execute: bool) -> RepairWorkspaceResult:
        _assert_safe_workspace(self.workspace_root, self._unsafe_input_root)
        actions = self._repair_actions()
        if execute:
            for action in actions:
                self._execute(action)
        return RepairWorkspaceResult(tuple(actions), execute)

    def _entries(self) -> list[WorkspaceEntry]:
        entries: list[WorkspaceEntry] = []
        for record in self._record_directories():
            receipt = _load_receipt(record / _RECEIPT)
            assert receipt is not None  # validate() establishes this before build().
            paper = receipt["paper"]
            page = record / _PAGE
            entries.append(WorkspaceEntry(_label(paper), page))
        return sorted(entries, key=lambda entry: (entry.label, str(entry.page_path)))

    def _record_directories(self) -> list[Path]:
        records, _ = _discover_records(self.workspace_root / _PAPERS)
        return records

    def _repair_actions(self) -> list[WorkspaceRepairAction]:
        actions: list[WorkspaceRepairAction] = []
        records, discovery_issues = _discover_records(
            self.workspace_root / _PAPERS
        )
        if discovery_issues:
            raise ValueError("workspace paper tree contains unsafe entries")
        staging = self.workspace_root / _STAGING
        if _is_directory(staging):
            for path in sorted(staging.iterdir()):
                if path.is_symlink() or not _contained(path, staging) or not _is_directory(path):
                    raise ValueError("workspace staging contains an unsafe entry")
                actions.append(WorkspaceRepairAction(path, "remove-staging", "abandoned staging directory"))
        for record in records:
            if _validate_record(self.workspace_root, record):
                actions.append(WorkspaceRepairAction(record, "quarantine-record", "invalid generated record"))
        return actions

    def _execute(self, action: WorkspaceRepairAction) -> None:
        if action.action == "remove-staging":
            staging = self.workspace_root / _STAGING
            if not _contained(action.path, staging) or not _is_directory(action.path):
                raise ValueError("staging repair target changed before execution")
            _assert_safe_workspace(self.workspace_root)
            shutil.rmtree(action.path)
            return
        if action.action == "quarantine-record":
            papers = self.workspace_root / _PAPERS
            if not _contained(action.path, papers) or not _is_directory(action.path):
                raise ValueError("quarantine target changed before execution")
            if not any(record == action.path for record in self._record_directories()):
                raise ValueError("quarantine target is no longer a generated record")
            if not _validate_record(self.workspace_root, action.path):
                raise ValueError("quarantine action is stale because the record is valid")
            destination = self.workspace_root / _QUARANTINE / uuid.uuid4().hex / action.path.relative_to(papers)
            _assert_safe_workspace(self.workspace_root)
            destination.parent.mkdir(parents=True, exist_ok=True)
            _assert_safe_workspace(self.workspace_root)
            os.replace(action.path, destination)
            return
        raise ValueError(f"unsupported repair action: {action.action}")


def _validate_record(root: Path, record: Path) -> list[WorkspaceIssue]:
    receipt_path = record / _RECEIPT
    if not _is_directory(record) or _has_symlink_ancestor(record, root.parent):
        return [WorkspaceIssue(record, "record directory is missing or unsafe")]
    receipt = _load_receipt(receipt_path)
    if receipt is None:
        return [WorkspaceIssue(record, "receipt is missing or malformed")]
    issues: list[WorkspaceIssue] = []
    paper = receipt.get("paper")
    if not isinstance(paper, dict) or any(not isinstance(paper.get(key), str) or not paper[key].strip() for key in ("source_id", "scope_id", "record_id")):
        issues.append(WorkspaceIssue(receipt_path, "receipt paper identity is malformed"))
    elif record != _record_path(root, paper):
        issues.append(WorkspaceIssue(receipt_path, "receipt paper identity does not match record path"))
    stages = receipt.get("stages")
    if not isinstance(stages, list) or not stages:
        issues.append(WorkspaceIssue(receipt_path, "receipt stages are missing or malformed"))
        return issues
    if tuple(stage.get("stage") if isinstance(stage, dict) else None for stage in stages) != _CORE_STAGES:
        issues.append(WorkspaceIssue(receipt_path, "receipt Core stages are incomplete or out of order"))
        return issues
    page_valid = False
    for stage in stages:
        if not isinstance(stage, dict):
            issues.append(WorkspaceIssue(receipt_path, "receipt stage is malformed"))
            continue
        stage_name = stage.get("stage")
        if stage_name not in _STAGE_ARTIFACTS:
            issues.append(WorkspaceIssue(receipt_path, "receipt stage is malformed"))
            continue
        artifacts = stage.get("artifacts")
        if not isinstance(artifacts, list):
            issues.append(WorkspaceIssue(receipt_path, "receipt artifacts are missing or malformed"))
            continue
        expected = _STAGE_ARTIFACTS[stage_name]
        if not expected:
            expected_identity = (
                paper_identity_fingerprint(
                    paper["source_id"], paper["scope_id"], paper["record_id"]
                )
                if not issues and isinstance(paper, dict)
                else None
            )
            if artifacts or stage.get("fingerprint") != expected_identity:
                issues.append(WorkspaceIssue(receipt_path, "receipt identify stage is malformed"))
            continue
        if len(artifacts) != 1:
            issues.append(WorkspaceIssue(receipt_path, "receipt stage has duplicate or missing artifacts"))
            continue
        if stage_name == "materialize_source" and (
            not isinstance(stage.get("input_id"), str) or not stage["input_id"].strip()
        ):
            issues.append(WorkspaceIssue(receipt_path, "receipt source stage input_id is missing"))
            continue
        if stage_name == "generate_review" and (
            not isinstance(stage.get("provider_id"), str)
            or not stage["provider_id"].strip()
            or not isinstance(stage.get("model_id"), str)
            or not stage["model_id"].strip()
        ):
            issues.append(
                WorkspaceIssue(
                    receipt_path,
                    "receipt review provider or model provenance is missing",
                )
            )
            continue
        fingerprints: list[str] = []
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                issues.append(WorkspaceIssue(receipt_path, "receipt artifact is malformed"))
                continue
            name, raw_path, fingerprint = artifact.get("name"), artifact.get("path"), artifact.get("fingerprint")
            if not all(isinstance(value, str) and value for value in (name, raw_path, fingerprint)):
                issues.append(WorkspaceIssue(receipt_path, "receipt artifact is malformed"))
                continue
            artifact_path = _artifact_path(root, raw_path)
            expected_path = record / expected[1]
            if name != expected[0] or artifact_path != expected_path:
                issues.append(WorkspaceIssue(receipt_path, "receipt artifact is not the exact record-local output"))
                continue
            if not _is_regular_file(artifact_path):
                issues.append(WorkspaceIssue(artifact_path, "receipt artifact is missing"))
                continue
            if not _fingerprint_matches(artifact_path, fingerprint):
                issues.append(WorkspaceIssue(artifact_path, "receipt artifact fingerprint does not match"))
                continue
            fingerprints.append(fingerprint)
            if stage_name == "render_page":
                page_valid = True
        declared = stage.get("fingerprint")
        if not isinstance(declared, str) or declared != "|".join(fingerprints):
            issues.append(WorkspaceIssue(receipt_path, "receipt stage fingerprint does not match artifacts"))
    page = record / _PAGE
    if not page_valid or not _is_regular_file(page):
        issues.append(WorkspaceIssue(page, "committed page is missing from receipt"))
    return issues


def _load_receipt(path: Path) -> dict[str, object] | None:
    try:
        value = json.loads(_read_regular(path).decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        return None
    return value


def _artifact_path(root: Path, raw_path: str) -> Path | None:
    candidate = Path(raw_path).expanduser()
    if not candidate.is_absolute() and ".." in candidate.parts:
        return None
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    if _has_symlink_ancestor(candidate, root.parent):
        return None
    return candidate


def _fingerprint_matches(path: Path, fingerprint: str) -> bool:
    if fingerprint.startswith("sha256:"):
        fingerprint = fingerprint.removeprefix("sha256:")
    if len(fingerprint) != 64 or any(character not in "0123456789abcdef" for character in fingerprint.lower()):
        return False
    digest = hashlib.sha256()
    try:
        with _open_regular(path) as artifact:
            for chunk in iter(lambda: artifact.read(_CHUNK_SIZE), b""):
                digest.update(chunk)
    except OSError:
        return False
    return digest.hexdigest() == fingerprint.lower()


def _label(paper: dict[str, object]) -> str:
    return " / ".join(str(paper[key]) for key in ("source_id", "scope_id", "record_id"))


def _record_path(root: Path, paper: dict[str, object]) -> Path:
    path = root / _PAPERS
    for key in ("source_id", "scope_id", "record_id"):
        path /= hashlib.sha256(str(paper[key]).encode("utf-8")).hexdigest()
    return path


def _discover_records(papers: Path) -> tuple[list[Path], list[WorkspaceIssue]]:
    records: list[Path] = []
    issues: list[WorkspaceIssue] = []
    if not papers.exists():
        return records, issues
    if not _is_directory(papers):
        return records, [WorkspaceIssue(papers, "papers root is unsafe")]

    def visit(directory: Path, depth: int) -> None:
        for child in sorted(directory.iterdir()):
            if child.is_symlink():
                issues.append(WorkspaceIssue(child, "paper tree contains a symlink"))
                continue
            if not _is_directory(child) or not re.fullmatch(r"[0-9a-f]{64}", child.name):
                issues.append(
                    WorkspaceIssue(child, "paper tree has an unexpected entry")
                )
                continue
            next_depth = depth + 1
            if next_depth == 3:
                records.append(child)
            else:
                visit(child, next_depth)

    visit(papers, 0)
    return sorted(records), issues


def _contained(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return not _has_symlink_ancestor(path, parent.parent)


def _site_html(entries: tuple[WorkspaceEntry, ...]) -> str:
    links = "\n".join(
        f'<li><a href="{html.escape(_site_href(entry.page_path), quote=True)}">{html.escape(entry.label, quote=True)}</a></li>'
        for entry in entries
    )
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Paper curation</title></head>
<body><main><h1>Paper curation</h1><ul>
%s
</ul></main></body></html>
""" % links


def _site_href(page: Path) -> str:
    return _PAPERS + "/" + quote(page.relative_to(page.parents[3]).as_posix(), safe="/")


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("xb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _replace_directory(staged: Path, destination: Path) -> None:
    backup = destination.with_name(f".{destination.name}.{uuid.uuid4().hex}.backup")
    moved_previous = False
    try:
        if destination.exists():
            if destination.is_symlink():
                raise ValueError("site destination is a symlink")
            os.replace(destination, backup)
            moved_previous = True
        os.replace(staged, destination)
    except Exception:
        if moved_previous and backup.exists() and not destination.exists():
            os.replace(backup, destination)
        raise
    if backup.exists():
        shutil.rmtree(backup, ignore_errors=True)


def _has_symlink_ancestor(path: Path, stop_before: Path | None = None) -> bool:
    current = path
    while True:
        if current.is_symlink():
            return True
        if stop_before is None or current == stop_before:
            return False
        if current.parent == current:
            return False
        current = current.parent


def _is_directory(path: Path) -> bool:
    return path.is_dir() and not path.is_symlink()


def _is_regular_file(path: Path) -> bool:
    try:
        return path.is_file() and not path.is_symlink()
    except OSError:
        return False


def _open_regular(path: Path):
    if not _is_regular_file(path):
        raise OSError("unsafe artifact path")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        mode = os.fstat(descriptor).st_mode
        if not stat.S_ISREG(mode):
            raise OSError("artifact is not a regular file")
        return os.fdopen(descriptor, "rb")
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise


def _read_regular(path: Path) -> bytes:
    with _open_regular(path) as source:
        return source.read()


def _workspace_safety_issues(root: Path, unsafe_input_root: bool = False) -> list[WorkspaceIssue]:
    unsafe = [
        path
        for path in (root, root / _PAPERS, root / _STAGING, root / _QUARANTINE, root / _SITE)
        if _has_symlink_ancestor(path, root.parent)
        or (path.exists() and not _is_directory(path))
    ]
    if unsafe_input_root:
        unsafe.append(root)
    return [WorkspaceIssue(path, "workspace path is a symlink or has a symlinked ancestor") for path in unsafe]


def _assert_safe_workspace(root: Path, unsafe_input_root: bool = False) -> None:
    if _workspace_safety_issues(root, unsafe_input_root):
        raise ValueError("workspace path is a symlink or has a symlinked ancestor")


def _recover_site_backups(root: Path) -> None:
    site = root / _SITE
    backups = [
        candidate
        for candidate in root.glob(f".{_SITE}.*.backup")
        if _SITE_BACKUP.fullmatch(candidate.name) and _is_directory(candidate)
    ]
    if not backups:
        return
    if not site.exists():
        os.replace(sorted(backups)[-1], site)
        backups = [candidate for candidate in backups if candidate.exists()]
    for backup in backups:
        if _is_directory(backup):
            shutil.rmtree(backup)
