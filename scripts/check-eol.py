#!/usr/bin/env python3
"""Preserve each tracked file's existing line-ending convention.

The repository contains both CRLF and LF files. ``.gitattributes`` prevents
Git conversion, while this command catches editors that rewrite line endings
and turn a focused change into a whole-file diff.

사용:
  python3 scripts/check-eol.py         # 검사만. 오염이 있으면 exit 1
  python3 scripts/check-eol.py --fix   # HEAD 의 줄바꿈으로 되돌림 (내용 변경은 보존)
"""

import subprocess
import sys
from pathlib import Path


def _run(args):
    return subprocess.run(args, capture_output=True, check=False)


def _eol_kind(data: bytes) -> str:
    """파일의 지배적 줄바꿈. 혼재면 'mixed'."""
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    if crlf and lf:
        return "mixed"
    if crlf:
        return "crlf"
    if lf:
        return "lf"
    return "none"


def _changed_files() -> list:
    """HEAD 와 다른 추적 파일 (워킹트리 + 인덱스)."""
    out = _run(["git", "diff", "HEAD", "--name-only"]).stdout.decode("utf-8", "replace")
    return [f for f in out.split("\n") if f.strip()]


def _is_binary(data: bytes) -> bool:
    return b"\x00" in data[:8000]


def inspect(fix: bool = False) -> int:
    repo = Path(_run(["git", "rev-parse", "--show-toplevel"])
                .stdout.decode().strip() or ".")
    offenders = []

    for rel in _changed_files():
        path = repo / rel
        if not path.is_file():
            continue

        head = _run(["git", "show", f"HEAD:{rel}"])
        if head.returncode != 0:
            continue                      # 신규 파일 — 기준이 없다
        old = head.stdout
        new = path.read_bytes()

        if _is_binary(old) or _is_binary(new):
            continue

        old_eol, new_eol = _eol_kind(old), _eol_kind(new)
        if old_eol == new_eol or old_eol == "none":
            continue

        # 줄바꿈을 통일해서 비교했을 때 같으면 = 내용은 그대로, 줄바꿈만 바뀐 것.
        # 다르면 내용도 함께 바뀐 것이므로, 줄바꿈은 원래대로 되돌리되 내용은 지킨다.
        same_content = old.replace(b"\r\n", b"\n") == new.replace(b"\r\n", b"\n")
        offenders.append((rel, old_eol, new_eol, same_content))

        if fix:
            body = new.replace(b"\r\n", b"\n")
            if old_eol == "crlf":
                body = body.replace(b"\n", b"\r\n")
            path.write_bytes(body)

    if not offenders:
        return 0

    verb = "복원함" if fix else "감지"
    print(f"[eol] 줄바꿈이 바뀐 파일 {len(offenders)}개 ({verb}):", file=sys.stderr)
    for rel, old_eol, new_eol, same in offenders:
        note = "줄바꿈만" if same else "내용도 함께 변경"
        print(f"  {rel}: {old_eol.upper()} → {new_eol.upper()}  ({note})", file=sys.stderr)

    if fix:
        print("[eol] 원래 줄바꿈으로 되돌렸습니다. git diff 로 확인하세요.", file=sys.stderr)
        return 0

    print("[eol] 되돌리려면: python3 scripts/check-eol.py --fix", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(inspect(fix="--fix" in sys.argv[1:]))
