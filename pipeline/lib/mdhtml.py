"""마크다운 → HTML 최소 변환기 (순수 텍스트 헬퍼).

Provider SDK를 요구하는 생성기와 분리하여, 마크다운 한 줄을 렌더하려는 쪽이
선택 의존성을 함께 import하지 않도록 한다.

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
