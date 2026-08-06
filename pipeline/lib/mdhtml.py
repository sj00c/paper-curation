"""마크다운 → HTML 최소 변환기 (순수 텍스트 헬퍼).

`agent_lecture_digest` 안에 있던 것을 여기로 꺼냈다. 그 모듈은 최상단에서
`generate_audio` → `google.genai` 를 import 하기 때문에, 마크다운 한 줄을
렌더하려는 쪽까지 Gemini SDK 를 요구하게 된다. 실제로 citedby 리포트가 그
때문에 타임라인 narrative 를 렌더하지 못하고 `##`·`**` 를 글자 그대로
노출했다 (import 실패를 except 로 삼켜 조용히 품질만 떨어뜨렸다).

여기에는 `re` / `html` 외의 의존성이 없다. 선택 SDK 가 하나도 안 깔린
환경에서도 import 된다.
"""

from __future__ import annotations

import html as H
import re

_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def md_to_html(md: str) -> str:
    """`#{1,3}` 헤딩 · `**굵게**` · `[텍스트](링크)` 만 처리하는 좁은 변환기."""
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)          # 이미지 마크업 제거
    out, para = [], []

    def flush():
        if not para:
            return
        t = H.escape("\n".join(para)).replace("\n", "<br>")
        t = _LINK_RE.sub(lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>', t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        out.append(f"<p>{t}</p>")
        para.clear()

    for line in md.split("\n"):
        s = line.strip()
        if not s:
            flush(); continue
        m = re.match(r"(#{1,3})\s+(.*)", s)
        if m:
            flush()
            lvl = "h2" if len(m.group(1)) <= 2 else "h3"
            out.append(f"<{lvl}>{H.escape(m.group(2))}</{lvl}>")
        else:
            para.append(line)
    flush()
    return "\n".join(out)
