#!/usr/bin/env python3
"""Fail-closed scanner for Git objects proposed by a pre-push update."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ZERO_OID = re.compile(r"^0+$")
OID = re.compile(r"^[0-9a-fA-F]{40}(?:[0-9a-fA-F]{24})?$")
REF = re.compile(r"^refs/[A-Za-z0-9._/+-]+$")
CREDENTIAL_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
    re.compile(rb"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(rb"\bAIza[0-9A-Za-z_-]{35}\b"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{36,255}\b"),
    re.compile(rb"\bxox[baprs]-[0-9A-Za-z-]{20,}\b"),
    re.compile(rb"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}\b"),
)


class ScanError(RuntimeError):
    """The scanner could not establish that the update is safe."""


def git(args: list[str], *, input_data: bytes | None = None) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise ScanError("Git could not read a proposed object")
    return completed.stdout


def valid_oid(value: str) -> bool:
    return bool(OID.fullmatch(value))


def validate_update(local_ref: str, local_oid: str, remote_ref: str, remote_oid: str) -> None:
    if not REF.fullmatch(local_ref) or not REF.fullmatch(remote_ref):
        raise ScanError("Update contains an unsupported ref name")
    if not valid_oid(local_oid) or not valid_oid(remote_oid):
        raise ScanError("Update contains an invalid object id")
    if len(local_oid) != len(remote_oid):
        raise ScanError("Update uses mixed object id formats")
    if ZERO_OID.fullmatch(local_oid):
        raise ScanError("Ref deletion is rejected by the security hook policy")


def existing_object(oid: str) -> bool:
    return bool(git(["rev-parse", "--verify", "--quiet", f"{oid}^{{object}}"]).strip())


def object_ids(local_oid: str, remote_oid: str) -> set[str]:
    """Return every object introduced by an update, plus its root object.

    A zero remote oid denotes a new ref, where all objects reachable from the
    local object must be inspected.  A non-zero base must exist locally: a
    shallow clone cannot prove which objects are being pushed, so it fails.
    """
    if not existing_object(local_oid):
        raise ScanError("Local object is unavailable")
    if not ZERO_OID.fullmatch(remote_oid) and not existing_object(remote_oid):
        raise ScanError("Remote base object is unavailable")

    revision = local_oid if ZERO_OID.fullmatch(remote_oid) else f"{remote_oid}..{local_oid}"
    output = git(["rev-list", "--objects", "--no-object-names", revision])
    ids = {local_oid.lower()}
    for line in output.splitlines():
        try:
            oid = line.decode("ascii")
        except UnicodeDecodeError as error:
            raise ScanError("Git returned an invalid object id") from error
        if not valid_oid(oid):
            raise ScanError("Git returned an invalid object id")
        ids.add(oid.lower())
    return ids


def raw_objects(oids: Iterable[str]) -> Iterable[bytes]:
    ordered_oids = sorted(oids)
    requested = "".join(f"{oid}\n" for oid in ordered_oids).encode("ascii")
    output = git(["cat-file", "--batch"], input_data=requested)
    cursor = 0
    for expected_oid in ordered_oids:
        newline = output.find(b"\n", cursor)
        if newline < 0:
            raise ScanError("Git returned an incomplete object")
        header = output[cursor:newline].split()
        cursor = newline + 1
        if len(header) != 3 or header[0].lower() != expected_oid.encode("ascii") or header[1] == b"missing":
            raise ScanError("Git could not read a proposed object")
        try:
            size = int(header[2])
        except ValueError as error:
            raise ScanError("Git returned an invalid object size") from error
        end = cursor + size
        if end >= len(output) or output[end:end + 1] != b"\n":
            raise ScanError("Git returned an incomplete object")
        yield output[cursor:end]
        cursor = end + 1
    if cursor != len(output):
        raise ScanError("Git returned unexpected object data")


def contains_credential(content: bytes) -> bool:
    return any(pattern.search(content) for pattern in CREDENTIAL_PATTERNS)


def scan(local_ref: str, local_oid: str, remote_ref: str, remote_oid: str) -> None:
    validate_update(local_ref, local_oid, remote_ref, remote_oid)
    for content in raw_objects(object_ids(local_oid, remote_oid)):
        if contains_credential(content):
            raise ScanError("Credential-like content detected")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a proposed Git update for credentials.")
    parser.add_argument("--update", nargs=4, metavar=("LOCAL_REF", "LOCAL_OID", "REMOTE_REF", "REMOTE_OID"))
    args = parser.parse_args()
    try:
        scan(*args.update)
    except Exception:
        print("security scanner: update rejected; credentials or scanner errors are not safe to push", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
