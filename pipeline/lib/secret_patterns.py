"""Credential shapes and JS key-slot stripping — one table, every scanner.

이 모듈이 존재하는 이유는 하나다: **strip 하는 쪽과 검사하는 쪽이 서로 다른
정규식을 들고 있으면 안전망이 그물보다 성겨진다.** 실제로 그랬다 —
`prepare_deploy` 의 strip 은 `sk-` 로 시작하는 값만 지웠는데 leak 검사는
`sk-ant-` / `sk-proj-` 만 찾았다. 그 사이에 낀 레거시 OpenAI 키
(`sk-` + 48 alnum) 는 **양쪽 모두**를 통과한다.

두 가지 원칙:

1. **Strip 은 값이 아니라 슬롯 이름으로 한다** (`strip_key_slots`).
   "키처럼 생겼으면 지운다" 는 fail-open 이다. 새 provider, 사내 게이트웨이,
   Azure(32 hex, 접두사 없음) 를 만나면 조용히 통과시킨다. 반대로
   "`_ANTHROPIC_KEY` 슬롯에 든 문자열 리터럴은 무엇이든 지운다" 는
   fail-closed 다. 지울 게 없으면 no-op 이고, 있으면 반드시 지운다.

2. **검사는 strip 의 상위집합이다** (`PATTERNS`). strip 이 놓친 게 있으면
   검사가 잡아야 의미가 있다. 그래서 여기엔 슬롯에 들어가지 않는 형태
   (AWS·GitHub·Google OAuth) 까지 넣는다.

OAuth 구독 자격증명(`CLAUDE_CODE_OAUTH_TOKEN`)은 애초에 어떤 생성기도 읽지
않는다 (`anthropic_auth` 가 `claude -p` 서브프로세스로만 쓴다). 그래도
`sk-ant-oat01-...` 형태가 `ANTHROPIC` 패턴에 잡히도록 해 둔다 — 누가
실수로 그 값을 API key 슬롯에 넣어도 배포 직전에 멈춘다.

의존성 없음(`re` 만). git pre-push 훅에서도 import 하므로 그래야 한다.
"""
from __future__ import annotations

import json
import re

# ── 자격증명 형태 ────────────────────────────────────────────────────────
# 문자 클래스는 일부러 좁게 잡는다. 논문 제목("Task-Oriented", "Risk-based")
# 에서 나오는 `sk-...` 오탐을 피하려면 레거시 OpenAI 는 하이픈/언더스코어를
# 허용하지 않는 48 alnum 이어야 한다. 실제 코퍼스 17,021 파일로 검증했다.
_SPECS: tuple[tuple[str, str], ...] = (
    # sk-ant-api03-… (API key) / sk-ant-oat01-… (구독 OAuth 토큰)
    ("Anthropic key or OAuth token", r"sk-ant-[A-Za-z0-9_-]{20,}"),
    ("OpenAI project key", r"sk-proj-[A-Za-z0-9_-]{20,}"),
    # 레거시 OpenAI: sk- + 48 alnum. strip 은 잡지만 예전 leak 검사는 놓쳤다.
    ("OpenAI legacy key", r"sk-[A-Za-z0-9]{48}"),
    ("Google API key", r"AIza[0-9A-Za-z_-]{35}"),
    # Google AI Studio 의 신형 키 형식. **이 감사에서 실제로 잡힌 구멍이다** —
    # 로컬 생성물 3,273개 페이지에 이 형식 키가 구워져 있었는데, 예전 stripper
    # (`_GEMINI_KEY = "AIza…"` 만 매치) 도 예전 leak 검사도 둘 다 통과시켰다.
    # 다음 배포에서 그대로 Cloudflare 로 올라갈 상태였다.
    ("Google API key (AQ)", r"AQ\.[A-Za-z0-9_-]{20,}"),
    ("Google OAuth token", r"ya29\.[A-Za-z0-9_-]{20,}"),
    ("AWS access key", r"AKIA[0-9A-Z]{16}"),
    ("GitHub token", r"gh[pousr]_[A-Za-z0-9]{20,}"),
)

PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (name, re.compile(rx)) for name, rx in _SPECS
)
BYTE_PATTERNS: tuple[tuple[str, re.Pattern[bytes]], ...] = tuple(
    (name, re.compile(rx.encode("ascii"))) for name, rx in _SPECS
)

# ── 생성 HTML 이 자격증명을 담을 수 있는 JS 슬롯 ─────────────────────────
# 여기에 이름을 올리는 순간 배포 strip 과 leak 검사가 동시에 따라온다.
# 새 슬롯을 추가하면서 이 튜플을 잊으면 테스트가 실패한다.
KEY_SLOTS: tuple[str, ...] = (
    "_ANTHROPIC_KEY",
    "_OPENAI_KEY",
    "_GEMINI_KEY",
    "_LLM_KEY",
)

# `window._GEMINI_KEY = "…"` 와 `let _ANTHROPIC_KEY = "…"` 를 모두 받는다.
# 예전 strip 은 Gemini 만 `window.` 를 허용해, `window._OPENAI_KEY = "sk-…"`
# 같은 조합이 생기면 통과시켰다.
_SLOT_RE = {
    slot: re.compile(
        r'(?P<decl>(?:const|let|var)\s+|window\.)?'
        + re.escape(slot)
        + r'\s*=\s*"(?P<val>(?:[^"\\]|\\.)*)"'
    )
    for slot in KEY_SLOTS
}

_LOCAL_EMAILS_RE = re.compile(r'window\._LOCAL_EMAILS\s*=\s*\[[^\]]*\]')
_LOCAL_EMAILS_LEAK_RE = re.compile(r'window\._LOCAL_EMAILS\s*=\s*\[\s*"[^"]+')


def strip_key_slots(text: str) -> tuple[str, int]:
    """모든 키 슬롯의 문자열 리터럴을 ``""`` 로 비운다.

    값의 모양을 보지 않는다. 이미 빈 슬롯은 건드리지 않으므로 idempotent 다.
    반환: (새 텍스트, 비운 슬롯 수).
    """
    stripped = 0
    out = text
    for slot, rx in _SLOT_RE.items():
        def _sub(m: re.Match[str], _slot: str = slot) -> str:
            nonlocal stripped
            if not m.group("val"):
                return m.group(0)
            stripped += 1
            return (m.group("decl") or "") + _slot + ' = ""'

        out = rx.sub(_sub, out)
    return out, stripped


def strip_local_emails(text: str) -> tuple[str, int]:
    """``window._LOCAL_EMAILS`` 배열을 비운다. 반환: (새 텍스트, 비운 횟수)."""
    out, n = _LOCAL_EMAILS_RE.subn('window._LOCAL_EMAILS = []', text)
    return out, n


_EMPTY_SLOT_RE = {
    slot: re.compile(
        r'(?P<decl>(?:const|let|var)\s+|window\.)?' + re.escape(slot) + r'\s*=\s*""'
    )
    for slot in KEY_SLOTS
}


def reinject_key_slot(text: str, slot: str, value: str) -> tuple[str, int]:
    """비어 있는 ``slot`` 에 ``value`` 를 되꽂는다 (로컬 복원 전용).

    strip 과 **같은 슬롯 표·같은 선언 형태**를 쓴다. 예전엔 strip 이
    `window.` 를 받고 re-inject 는 안 받는 비대칭이 있어, 한 번 strip 된
    슬롯이 로컬에서 영영 복원되지 않을 수 있었다. 값이 비면 no-op.
    """
    if not value or slot not in _EMPTY_SLOT_RE:
        return text, 0
    lit = json.dumps(value)
    return _EMPTY_SLOT_RE[slot].subn(
        lambda m: (m.group("decl") or "") + slot + " = " + lit, text
    )


def find_secrets(text: str) -> list[tuple[str, str]]:
    """(패턴 이름, 매치 문자열) 목록. 비어 있으면 깨끗하다."""
    return [(name, m) for name, rx in PATTERNS for m in rx.findall(text)]


def find_local_emails(text: str) -> bool:
    """``_LOCAL_EMAILS`` 에 주소가 남아 있으면 True."""
    return bool(_LOCAL_EMAILS_LEAK_RE.search(text))


def redact(value: str) -> str:
    """로그용 축약. 원문을 절대 그대로 찍지 않는다."""
    if len(value) <= 12:
        return value[:4] + "…"
    return value[:8] + "…" + value[-4:]
