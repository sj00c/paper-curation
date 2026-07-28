"""Fail-closed local delivery gate: commit only executor-owned paths.

Delivery ends at a local commit on the branch that is already checked out.
There is no remote, no publish, and no history rewrite in this module: every
Git invocation is funnelled through :func:`_run_git`, which accepts a small
allow-list of read/stage/commit subcommands and rejects everything else.

The gate is a sequence of explicit, independently callable steps:

1. :func:`inventory_worktree`   - lstat + digest every pending worktree change
2. :func:`resolve_ownership`    - normalise the executor-touched (``owned``) set
3. :func:`record_final_gate`    - pin branch, HEAD and per-owned-path digests
4. :func:`verify_no_drift`      - re-lstat/re-digest owned paths, branch, HEAD
5. :func:`check_deny_list`      - refuse generated artifacts, ``docs/**``, ``.gjc``
6. :func:`stage_owned`          - ``git add --`` with exact owned pathspecs
7. :func:`scan_staged_patch`    - credential scan of the staged patch
8. :func:`assert_staged_subset` - staged set must be a subset of ``owned``
9. :func:`commit_owned`         - one local commit

Non-owned worktree changes are deliberately *not* a hard stop.  Concurrent user
work is routine; the only assertion made about it is that it never reaches the
index (step 8).
"""

from __future__ import annotations

import fnmatch
import hashlib
import importlib.util
import os
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

SCANNER_PATH = Path(__file__).resolve().parents[1] / "scripts" / "scan-secrets.py"

# Only these Git subcommands may ever run.  Anything outside the allow-list is
# refused before a process is spawned, so the gate cannot reach a remote.
ALLOWED_SUBCOMMANDS = frozenset({"status", "rev-parse", "diff", "add", "commit"})

# Named explicitly so the refusal reason is precise and so tests can enumerate
# the network / history-rewriting surface that this module must never touch.
FORBIDDEN_SUBCOMMANDS = frozenset({
    "push", "pull", "fetch", "clone", "remote", "submodule", "request-pull",
    "send-email", "format-patch", "bundle", "archive", "daemon", "credential",
    "am", "apply", "cherry-pick", "revert", "rebase", "merge", "reset",
    "restore", "checkout", "switch", "branch", "tag", "worktree", "stash",
    "clean", "gc", "prune", "filter-branch", "update-ref", "symbolic-ref",
    "config", "notes", "replace", "reflog",
})

# Options that would widen the staged set, rewrite history, bypass hooks, or
# stage partial hunks.  Only arguments before the ``--`` separator are checked;
# everything after it is an exact pathspec validated by ownership resolution.
FORBIDDEN_ARGUMENTS = frozenset({
    "-p", "--patch", "-i", "--interactive", "-f", "--force", "--force-with-lease",
    "--amend", "--no-verify", "-n", "--dry-run", "-a", "--all", "-A", "-u",
    "--update", "--allow-empty", "--allow-empty-message", "-c", "-C", "--exec-path",
})

DENIED_EXACT = frozenset({
    ".gjc",
    ".env",
    "config.json",
    "pipeline/_update_force.log",
    "pipeline/_update_force_checkpoint.json",
})
DENIED_TOP_DIRECTORIES = frozenset({
    "docs", ".gjc", ".git", "artifacts", "pdf_cache", "papers", "node_modules",
    ".venv", "venv", ".pytest_cache", ".mypy_cache",
})
DENIED_COMPONENTS = frozenset({
    "__pycache__", ".git", ".gjc", ".obsidian", ".claude", ".omc", ".DS_Store",
})
DENIED_DIRECTORY_PREFIXES = (
    "pipeline/_img_timelines/",
    "pipeline/_img_workflows/",
)
DENIED_NAME_PATTERNS = (
    "_regen_*.py",
    "*_keys.json",
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.pem",
    "*.key",
    ".env.*",
)
# ``.env.example`` is a tracked, secret-free template and stays deliverable.
DENY_PATTERN_EXCEPTIONS = frozenset({".env.example"})

_PATHSPEC_MAGIC = ("*", "?", "[", "]", ":", "\\", "\n", "\r", "\0")


class DeliveryError(RuntimeError):
    """Base class for every refusal raised by the local delivery gate."""


class RepositoryError(DeliveryError):
    """The delivery target is not a usable Git worktree root."""


class OwnershipError(DeliveryError):
    """The declared owned set is malformed or does not match the worktree."""


class OwnedPathDriftError(DeliveryError):
    """An owned path changed between the final gate and staging."""


class BranchDriftError(DeliveryError):
    """The checked-out branch changed between the final gate and staging."""


class HeadDriftError(DeliveryError):
    """HEAD moved between the final gate and staging."""


class DetachedHeadError(DeliveryError):
    """Delivery requires a named branch; HEAD is detached."""


class DenyListError(DeliveryError):
    """An owned path is a generated artifact, under docs/, or under .gjc."""


class SecretScanError(DeliveryError):
    """The staged patch could not be proven free of credential-like content."""


class StagedScopeError(DeliveryError):
    """The staged set is not a subset of the owned set."""


class ForbiddenGitCommandError(DeliveryError):
    """A Git subcommand or option outside the delivery allow-list was attempted."""


class GitCommandError(DeliveryError):
    """An allowed Git command failed."""


@dataclass(frozen=True)
class PathState:
    """lstat identity plus a content digest for one worktree path."""

    path: str
    exists: bool
    mode: int
    size: int
    mtime_ns: int
    inode: int
    device: int
    digest: str | None


@dataclass(frozen=True)
class InventoryEntry:
    index_status: str
    worktree_status: str
    state: PathState

    @property
    def untracked(self) -> bool:
        return self.index_status == "?" and self.worktree_status == "?"


@dataclass(frozen=True)
class Inventory:
    """Pre-execution snapshot of every tracked-modified and untracked path."""

    root: Path
    entries: Mapping[str, InventoryEntry]

    def paths(self) -> tuple[str, ...]:
        return tuple(sorted(self.entries))


@dataclass(frozen=True)
class FinalGate:
    """Branch, HEAD and per-owned-path digests pinned at final-gate pass."""

    root: Path
    branch: str
    head: str
    owned: tuple[str, ...]
    states: Mapping[str, PathState]


@dataclass(frozen=True)
class DeliveryReceipt:
    branch: str
    base_head: str
    commit: str
    owned: tuple[str, ...]
    staged: tuple[str, ...]


def _reject_forbidden(args: Sequence[str]) -> str:
    """Validate an argv tail before any process is spawned."""
    if not args:
        raise ForbiddenGitCommandError("a git invocation requires a subcommand")
    if not all(isinstance(arg, str) for arg in args):
        raise ForbiddenGitCommandError("git arguments must be strings")
    subcommand = args[0]
    if subcommand.startswith("-"):
        raise ForbiddenGitCommandError("git global options are not accepted by the delivery gate")
    if subcommand in FORBIDDEN_SUBCOMMANDS:
        raise ForbiddenGitCommandError(f"git {subcommand} is forbidden by the local delivery gate")
    if subcommand not in ALLOWED_SUBCOMMANDS:
        raise ForbiddenGitCommandError(f"git {subcommand} is outside the local delivery allow-list")
    options = list(args[1:])
    if "--" in options:
        options = options[:options.index("--")]
    for option in options:
        head = option.split("=", 1)[0]
        if head in FORBIDDEN_ARGUMENTS:
            raise ForbiddenGitCommandError(f"git {subcommand} {head} is forbidden by the local delivery gate")
    return subcommand


def _run_git(args: Sequence[str], *, root: Path, input_data: bytes | None = None) -> bytes:
    """The single Git seam of this module.

    Every Git invocation in the delivery gate passes through here, so a spy that
    wraps this one function observes the complete argv history of a run.
    """
    _reject_forbidden(args)
    completed = subprocess.run(
        ["git", "--no-pager", *args],
        cwd=str(root),
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={**os.environ, "LC_ALL": "C", "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0"},
    )
    if completed.returncode:
        detail = completed.stderr.decode("utf-8", "replace").strip().splitlines()
        raise GitCommandError(f"git {args[0]} failed: {detail[-1] if detail else 'no diagnostic'}")
    return completed.stdout


def _git_text(args: Sequence[str], *, root: Path) -> str:
    return _run_git(args, root=root).decode("utf-8", "surrogateescape")


def _require_relative_path(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise OwnershipError("an owned path must be a non-empty string")
    if value.startswith("/") or value.startswith("-"):
        raise OwnershipError(f"owned path must be repository-relative: {value!r}")
    if any(token in value for token in _PATHSPEC_MAGIC):
        raise OwnershipError(f"owned path must not contain pathspec magic: {value!r}")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise OwnershipError(f"owned path must not contain traversal or empty components: {value!r}")
    return value


def _capture_state(root: Path, relative: str) -> PathState:
    target = root / relative
    try:
        info = os.lstat(target)
    except OSError:
        return PathState(relative, False, 0, 0, 0, 0, 0, None)
    if stat.S_ISLNK(info.st_mode):
        payload = b"symlink\0" + os.readlink(target).encode("utf-8", "surrogateescape")
        digest = hashlib.sha256(payload).hexdigest()
    elif stat.S_ISREG(info.st_mode):
        hasher = hashlib.sha256()
        with open(target, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                hasher.update(chunk)
        digest = hasher.hexdigest()
    else:
        raise OwnershipError(f"owned path is not a regular file or symlink: {relative}")
    return PathState(
        relative,
        True,
        info.st_mode,
        info.st_size,
        info.st_mtime_ns,
        info.st_ino,
        info.st_dev,
        digest,
    )


def _require_worktree_root(root: Path) -> Path:
    resolved = Path(root).resolve()
    if not resolved.is_dir():
        raise RepositoryError(f"delivery root is not a directory: {resolved}")
    try:
        toplevel = _git_text(["rev-parse", "--show-toplevel"], root=resolved).strip()
    except GitCommandError as error:
        raise RepositoryError(f"delivery root is not a git worktree: {resolved}") from error
    if not toplevel or Path(toplevel).resolve() != resolved:
        raise RepositoryError(f"delivery root is not the worktree root: {resolved}")
    return resolved


def current_branch(root: Path) -> str:
    branch = _git_text(["rev-parse", "--abbrev-ref", "HEAD"], root=root).strip()
    if not branch or branch == "HEAD":
        raise DetachedHeadError("HEAD is detached; local delivery requires a named branch")
    return branch


def head_commit(root: Path) -> str:
    head = _git_text(["rev-parse", "HEAD"], root=root).strip()
    if not head:
        raise RepositoryError("HEAD does not resolve to a commit")
    return head


def inventory_worktree(root: Path) -> Inventory:
    """Step 1: lstat + digest every tracked-modified and untracked path."""
    resolved = _require_worktree_root(root)
    raw = _git_text(
        ["status", "--porcelain=v1", "-z", "--untracked-files=all", "--no-renames"],
        root=resolved,
    )
    entries: dict[str, InventoryEntry] = {}
    for record in raw.split("\0"):
        if len(record) < 4:
            continue
        index_status, worktree_status, relative = record[0], record[1], record[3:]
        if not relative:
            continue
        entries[relative] = InventoryEntry(index_status, worktree_status, _capture_state(resolved, relative))
    return Inventory(resolved, entries)


def resolve_ownership(inventory: Inventory, owned: Iterable[str]) -> tuple[str, ...]:
    """Step 2: normalise the executor-touched set against the inventory."""
    resolved: list[str] = []
    for raw in owned:
        relative = _require_relative_path(raw)
        if relative not in inventory.entries:
            raise OwnershipError(f"owned path is not a pending worktree change: {relative}")
        if relative not in resolved:
            resolved.append(relative)
    if not resolved:
        raise OwnershipError("local delivery requires at least one owned path")
    return tuple(sorted(resolved))


def record_final_gate(inventory: Inventory, owned: Sequence[str]) -> FinalGate:
    """Step 3: pin branch, HEAD and a content digest per owned path."""
    root = inventory.root
    branch = current_branch(root)
    head = head_commit(root)
    states = {path: _capture_state(root, path) for path in owned}
    for path, state in states.items():
        if not state.exists:
            raise OwnershipError(f"owned path disappeared before the final gate: {path}")
    return FinalGate(root, branch, head, tuple(owned), states)


def verify_no_drift(gate: FinalGate) -> None:
    """Step 4: re-lstat/re-digest owned paths and re-read branch and HEAD."""
    for path, recorded in gate.states.items():
        current = _capture_state(gate.root, path)
        if current != recorded:
            raise OwnedPathDriftError(f"owned path changed after the final gate: {path}")
    branch = current_branch(gate.root)
    if branch != gate.branch:
        raise BranchDriftError(f"branch drifted from {gate.branch!r} to {branch!r} after the final gate")
    head = head_commit(gate.root)
    if head != gate.head:
        raise HeadDriftError(f"HEAD drifted from {gate.head} to {head} after the final gate")


def denied_reason(relative: str) -> str | None:
    """Return why a path is undeliverable, or ``None`` when it is allowed."""
    path = _require_relative_path(relative)
    if path in DENIED_EXACT:
        return f"{path} is on the delivery deny-list"
    parts = path.split("/")
    if parts[0] in DENIED_TOP_DIRECTORIES:
        return f"{parts[0]}/ is on the delivery deny-list"
    for component in parts:
        if component in DENIED_COMPONENTS:
            return f"{component} is on the delivery deny-list"
    for prefix in DENIED_DIRECTORY_PREFIXES:
        if path.startswith(prefix):
            return f"{prefix} is on the delivery deny-list"
    name = parts[-1]
    if name not in DENY_PATTERN_EXCEPTIONS:
        for pattern in DENIED_NAME_PATTERNS:
            if fnmatch.fnmatch(name, pattern):
                return f"{name} matches the generated-artifact deny pattern {pattern}"
    return None


def check_deny_list(paths: Iterable[str]) -> None:
    """Step 5: refuse generated artifacts, ``docs/**`` and ``.gjc``."""
    for path in paths:
        reason = denied_reason(path)
        if reason is not None:
            raise DenyListError(reason)


def stage_owned(gate: FinalGate) -> None:
    """Step 6: stage exactly the owned pathspecs; never a partial hunk."""
    _run_git(["add", "--", *gate.owned], root=gate.root)


def _load_scanner():
    if not SCANNER_PATH.is_file():
        raise SecretScanError(f"secret scanner is unavailable at {SCANNER_PATH}")
    spec = importlib.util.spec_from_file_location("paper_curation_scan_secrets", SCANNER_PATH)
    if spec is None or spec.loader is None:
        raise SecretScanError("secret scanner could not be loaded")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as error:  # noqa: BLE001 - a scanner that cannot load is a hard stop
        raise SecretScanError("secret scanner could not be loaded") from error
    if not callable(getattr(module, "contains_credential", None)):
        raise SecretScanError("secret scanner does not expose contains_credential")
    return module


def staged_patch(root: Path) -> bytes:
    return _run_git(["diff", "--cached", "--binary", "--no-color", "--no-renames"], root=root)


def scan_staged_patch(root: Path) -> None:
    """Step 7: hard credential gate over the staged patch.

    ``git diff --check`` only reports whitespace defects, so it cannot stand in
    for this scan.  The staged patch bytes are handed to the credential patterns
    owned by ``scripts/scan-secrets.py``.
    """
    scanner = _load_scanner()
    if scanner.contains_credential(staged_patch(root)):
        raise SecretScanError("staged patch contains credential-like content")


def staged_paths(root: Path) -> tuple[str, ...]:
    raw = _git_text(["diff", "--cached", "--name-only", "-z", "--no-renames"], root=root)
    return tuple(sorted(path for path in raw.split("\0") if path))


def assert_staged_subset(gate: FinalGate) -> tuple[str, ...]:
    """Step 8: the staged set must be a subset of the owned set.

    Non-owned worktree changes are not inspected here.  Routine concurrent user
    work is only a failure when it reaches the index.
    """
    staged = staged_paths(gate.root)
    extra = sorted(set(staged) - set(gate.owned))
    if extra:
        raise StagedScopeError(f"staged paths outside the owned set: {', '.join(extra)}")
    return staged


def commit_owned(gate: FinalGate, message: str) -> str:
    """Step 9: one local commit on the pinned branch."""
    if not isinstance(message, str) or not message.strip():
        raise DeliveryError("a delivery commit requires a non-empty message")
    _run_git(["commit", "-m", message], root=gate.root)
    return head_commit(gate.root)


def deliver(root: Path, owned: Iterable[str], message: str) -> DeliveryReceipt:
    """Run the full gate and end at one local commit on the current branch.

    A refusal raised after :func:`stage_owned` leaves the owned paths staged:
    ``git reset`` is a forbidden subcommand here, so unwinding the index is the
    operator's call.  No commit is created on any refusal path.
    """
    inventory = inventory_worktree(root)
    resolved = resolve_ownership(inventory, owned)
    gate = record_final_gate(inventory, resolved)
    verify_no_drift(gate)
    check_deny_list(gate.owned)
    stage_owned(gate)
    scan_staged_patch(gate.root)
    staged = assert_staged_subset(gate)
    commit = commit_owned(gate, message)
    return DeliveryReceipt(gate.branch, gate.head, commit, gate.owned, staged)
