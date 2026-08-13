#!/usr/bin/env python3
"""Scan git objects that a push would introduce for credential material.

Unlike patch/diff scanners, this reads raw commit/tag/blob objects through
`git cat-file --batch`. Therefore merge-resolution content, `-diff` paths,
binary/NUL blobs, and annotated-tag messages are all inspected.

Input (default): pre-push ref lines on stdin:
    <local-ref> <local-oid> <remote-ref> <remote-oid>
Every non-deletion local tip is enumerated with `rev-list --objects <oid>`.
This deliberately includes objects reachable from an existing remote: a remote
ref is not evidence that the local history was already scanned. With no stdin,
all objects reachable from HEAD are scanned. `--all` scans only the current
HEAD snapshot; `--history` scans every object from every ref.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import re
import subprocess
import sys
import threading
from collections.abc import Iterable

# 이 훅은 **자기완결적이어야 한다.** `.git/hooks/pre-push` 가 부르는 유일한
# 파일이고, `scripts/` 만 떼어 배치되는 경우가 실제로 있다 (테스트 픽스처가
# 바로 그 형태다). 따라서 `pipeline/` 을 import 하지 않는다 — import 하면
# 훅이 ModuleNotFoundError 로 죽고, 그건 fail-closed 처럼 보이지만 실제로는
# "훅이 고장 났으니 끄자" 로 이어진다.
#
# 대신 표를 복제하되 **표류는 테스트로 막는다**:
# `pipeline/tests/test_deploy_secret_surface.py` 가 이 표와
# `pipeline/lib/secret_patterns.PATTERNS` 의 동일성을 강제한다. 한쪽만
# 고치면 CI 가 깨진다.
ZERO_RE = re.compile(r"^0+$")
RAW_PATTERNS = (
    # sk-ant-api03-… (API key) / sk-ant-oat01-… (구독 OAuth 토큰)
    ("Anthropic key or OAuth token", re.compile(rb"sk-ant-[A-Za-z0-9_-]{20,}")),
    ("OpenAI project key", re.compile(rb"sk-proj-[A-Za-z0-9_-]{20,}")),
    # 레거시 OpenAI: sk- + 48 alnum. 예전 표는 이걸 통째로 놓쳤다.
    ("OpenAI legacy key", re.compile(rb"sk-[A-Za-z0-9]{48}")),
    ("Google API key", re.compile(rb"AIza[0-9A-Za-z_-]{35}")),
    # Google AI Studio 신형 키. 배포 감사에서 실제로 잡힌 형식이다.
    ("Google API key (AQ)", re.compile(rb"AQ\.[A-Za-z0-9_-]{20,}")),
    ("Google OAuth token", re.compile(rb"ya29\.[A-Za-z0-9_-]{20,}")),
    ("AWS access key", re.compile(rb"AKIA[0-9A-Z]{16}")),
    ("GitHub token", re.compile(rb"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("Zotero API key", re.compile(
        rb"""(?:ZOTERO_API_KEY|Zotero-API-Key)\s*["']?\s*[,=:]\s*["']?[A-Za-z0-9]{24}(?![A-Za-z0-9])"""
    )),
)
BASE64_TOKEN = re.compile(rb"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{24,}={0,2}(?![A-Za-z0-9+/=])")
WHITESPACE = re.compile(rb"\s+")


def git(*args: str, input_data: bytes | None = None) -> bytes:
    proc = subprocess.run(
        ["git", *args], input=input_data, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace").strip())
    return proc.stdout


def rev_objects(args: list[str]) -> set[str]:
    out = git("rev-list", "--objects", "--no-object-names", *args)
    return {line.decode("ascii") for line in out.splitlines() if line}


def pushed_objects(lines: Iterable[str]) -> set[str]:
    objects: set[str] = set()
    refs_seen = 0
    for line in lines:
        fields = line.split()
        if len(fields) != 4:
            continue
        _local_ref, local_oid, _remote_ref, _remote_oid = fields
        refs_seen += 1
        if ZERO_RE.fullmatch(local_oid):  # deletion
            continue
        objects.update(rev_objects([local_oid]))
    if refs_seen == 0:
        objects.update(rev_objects(["HEAD"]))
    return objects


def snapshot_objects() -> set[str]:
    # Snapshot mode: inspect the complete current tree independent of diff attrs
    # or binary status, plus HEAD and annotated-tag objects/messages.
    objects = {git("rev-parse", "HEAD").decode().strip()}
    out = git("ls-tree", "-r", "-z", "--format=%(objectname)", "HEAD")
    objects.update(x.decode("ascii") for x in out.split(b"\0") if x)
    tags = git("for-each-ref", "--format=%(objectname)", "refs/tags")
    objects.update(x.decode("ascii") for x in tags.splitlines() if x)
    return objects


def history_objects() -> set[str]:
    """All objects reachable from any local or remote ref."""
    return rev_objects(["--all"])


def findings(data: bytes) -> set[str]:
    found = {name for name, pattern in RAW_PATTERNS if pattern.search(data)}

    # Catch keys split across whitespace/newlines without changing the object.
    compact = WHITESPACE.sub(b"", data)
    found.update(name + " (whitespace-split)"
                 for name, pattern in RAW_PATTERNS if pattern.search(compact))

    # Catch a key stored as a single standard-base64 token. Decode only
    # plausible tokens; malformed candidates are ignored.
    for token in BASE64_TOKEN.findall(data):
        try:
            decoded = base64.b64decode(token, validate=True)
        except (binascii.Error, ValueError):
            continue
        found.update(name + " (base64)"
                     for name, pattern in RAW_PATTERNS if pattern.search(decoded))
    return found


def scan_objects(oids: set[str]) -> list[tuple[str, str, set[str]]]:
    if not oids:
        return []
    proc = subprocess.Popen(
        ["git", "cat-file", "--batch"], stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None and proc.stdout is not None
    ordered = sorted(oids)

    # Feed stdin concurrently while consuming stdout. Writing every OID first
    # can deadlock once cat-file fills its stdout pipe.
    def feed() -> None:
        try:
            proc.stdin.write("".join(f"{oid}\n" for oid in ordered).encode("ascii"))
            proc.stdin.close()
        except BrokenPipeError:
            pass

    writer = threading.Thread(target=feed, daemon=True)
    writer.start()

    hits: list[tuple[str, str, set[str]]] = []
    for _expected in ordered:
        header = proc.stdout.readline().decode("ascii", "replace").strip().split()
        if len(header) < 3 or header[1] == "missing":
            continue
        oid, obj_type, size_s = header[:3]
        size = int(size_s)
        data = proc.stdout.read(size)
        proc.stdout.read(1)  # batch separator newline
        matched = findings(data)
        if matched:
            hits.append((oid, obj_type, matched))
    writer.join()
    rc = proc.wait()
    if rc:
        err = (proc.stderr.read() if proc.stderr else b"").decode("utf-8", "replace")
        raise RuntimeError(err.strip() or f"git cat-file exited {rc}")
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan raw pushed git objects for secrets")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--all", action="store_true",
                       help="scan the current HEAD snapshot and annotated-tag objects")
    modes.add_argument("--history", action="store_true",
                       help="scan all objects reachable from every ref")
    args = parser.parse_args()
    try:
        if args.history:
            oids = history_objects()
        elif args.all:
            oids = snapshot_objects()
        else:
            oids = pushed_objects(sys.stdin)
        hits = scan_objects(oids)
    except Exception as exc:
        print(f"[secret-scan] ERROR: {exc}", file=sys.stderr)
        return 2  # scanner failures block the push (fail closed)

    if hits:
        print("[secret-scan] credential material found — refusing operation", file=sys.stderr)
        for oid, obj_type, names in hits[:20]:
            print(f"  {oid[:12]} {obj_type}: {', '.join(sorted(names))}", file=sys.stderr)
        print("Remove the secret from git history and rotate it before retrying.", file=sys.stderr)
        return 1
    print(f"[secret-scan] ✓ scanned {len(oids)} raw git objects; no credentials")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
