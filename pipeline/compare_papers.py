"""Multi-paper comparison generator (paper-curio "Comparison" command).

Given 2+ reviewed papers, builds a Korean comparative analysis (관점/방법론/
originality/결과/한계) via one Anthropic call over their review.md contents,
then emits a self-contained HTML page (review-page theme + Audio Overview
widget + .md download button) plus the comparison markdown itself.

Output lives under docs/papers/_comparisons/<NNN_vs_NNN...>/ — local-only
(docs/.assetsignore) and deterministic, so re-running the same paper set
refreshes the same directory.

Usage:
  PYTHONUTF8=1 python pipeline/compare_papers.py --slugs 9121,9122
  (slug tokens may be bare NNN numbers or full slugs; 2-6 papers)

The paper-curio bridge imports run_compare() directly; the CLI prints a final
single-line JSON ({ok, html, md, dir, title}) so callers can lastJson() it.
"""

import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import review_to_html as RH  # noqa: E402  (THEMES, css, md renderer, audio wiring)

PAPERS = RH.PAPERS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(PAPERS)))
COMPARE_DIR = os.path.join(PAPERS, "_comparisons")
COMPARE_MODEL = os.environ.get("COMPARE_MODEL", "claude-sonnet-5")
MAX_PAPERS = 6

# review.md 섹션 중 비교 프롬프트에 넣는 것 (Related Papers 등은 제외)
_SECTIONS = ["Essence", "Motivation", "Achievement", "How", "Originality",
             "Limitation & Further Study", "Evaluation"]

# 고정 비교 축 — 프롬프트와 스키마 설명에 함께 명시
_AXES = ["문제 설정과 관점", "방법론", "Originality", "결과와 성과", "한계와 리스크",
         "연구 지형 (같이 보면 좋은 논문)"]

# 연결 관계의 한글 라벨 (review 페이지와 동일)
_REL_LABELS = {
    "alternative": "다른 접근",
    "extension": "후속 연구",
    "foundation": "기반 연구",
    "counterpoint": "반론/비판",
    "application": "응용 사례",
}


def log(msg):
    print(msg, flush=True)


# ── paper loading ────────────────────────────────────────────────────────────

def _load_index():
    with open(os.path.join(PAPERS, "_papers_index.json"), encoding="utf-8") as f:
        return json.load(f)


def resolve_slugs(tokens, index):
    """Resolve bare NNN numbers or full slugs to canonical index slugs."""
    by_slug = {p["slug"]: p for p in index}
    resolved = []
    for tok in tokens:
        tok = tok.strip()
        if not tok:
            continue
        if tok in by_slug:
            resolved.append(tok)
            continue
        pref = [s for s in by_slug if s.split("_", 1)[0] == tok]
        if len(pref) != 1:
            raise SystemExit(f"slug '{tok}' resolves to {len(pref)} papers — "
                             f"use the full slug")
        resolved.append(pref[0])
    return resolved


def _parse_sections(md):
    """review.md → {section_name: text} (frontmatter stripped)."""
    body = re.sub(r"\A---\n[\s\S]*?\n---\n", "", md)
    parts = re.split(r"\n## +", "\n" + body)
    out = {}
    for p in parts[1:]:
        name, _, text = p.partition("\n")
        out[name.strip()] = text.strip()
    return out


def load_paper(slug, index, slug_titles, all_conns):
    entry = next((p for p in index if p["slug"] == slug), None)
    if entry is None:
        raise SystemExit(f"'{slug}' not in _papers_index.json")
    md_path = os.path.join(PAPERS, slug, "review.md")
    if not os.path.exists(md_path):
        raise SystemExit(f"{slug}: review.md 없음 — 먼저 리뷰를 생성하세요")
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    # 같이 보면 좋은 논문 (bidirectional connections view, top 8)
    conns = []
    for c in (all_conns.get(slug) or [])[:8]:
        cslug = c.get("slug", "")
        conns.append({
            "slug": cslug,
            "title": slug_titles.get(cslug, cslug),
            "relation": _REL_LABELS.get(c.get("relation", ""), c.get("relation", "")),
            "reason": c.get("reason", ""),
        })
    return {
        "slug": slug,
        "num": slug.split("_", 1)[0],
        "title": entry.get("title") or slug,
        "authors": entry.get("authors") or [],
        "date": str(entry.get("date") or ""),
        "doi": entry.get("doi") or "",
        "topic": entry.get("primary_topic") or "",
        "category": (entry.get("classifications", {})
                     .get(entry.get("primary_topic", ""), {})
                     .get("primary_category", "")),
        "sections": _parse_sections(md),
        "connections": conns,
    }


# ── LLM comparison ───────────────────────────────────────────────────────────

_TOOL = {
    "name": "emit_comparison",
    "description": "논문 비교 분석 결과를 구조화해 반환",
    "input_schema": {
        "type": "object",
        "properties": {
            "overview_ko": {"type": "string", "description":
                            "논문들의 관계와 비교 구도 총평 (한국어 3-5문장, 전문용어는 영어)"},
            "axes": {"type": "array", "items": {
                "type": "object",
                "properties": {
                    "axis_ko": {"type": "string", "description": f"비교 축 이름 — 반드시 이 5개를 순서대로: {', '.join(_AXES)}"},
                    "entries": {"type": "array", "items": {
                        "type": "object",
                        "properties": {
                            "slug": {"type": "string"},
                            "summary_ko": {"type": "string", "description": "이 축에서 이 논문의 입장/내용 (2-4문장)"},
                        },
                        "required": ["slug", "summary_ko"],
                    }},
                    "synthesis_ko": {"type": "string", "description":
                                     "이 축에서 논문들을 맞대어 본 분석 — 공통점/차이/우열/상보성 (2-4문장)"},
                },
                "required": ["axis_ko", "entries", "synthesis_ko"],
            }},
            "quick_table": {"type": "array", "items": {
                "type": "object",
                "properties": {
                    "axis_ko": {"type": "string"},
                    "cells": {"type": "array", "items": {"type": "string"},
                              "description": "논문 순서대로, 각 논문을 한 줄(≤60자)로"},
                },
                "required": ["axis_ko", "cells"],
            }},
            "reading_guide_ko": {"type": "string", "description":
                                 "독자 유형별로 어떤 논문을 어떤 순서로 읽을지 추천 (3-5문장)"},
            "diagram_spec_en": {
                "type": "object",
                "description": "비교 다이어그램용 짧은 영어 문구 — 이미지에 렌더링되므로 반드시 영어",
                "properties": {
                    "labels": {"type": "array", "items": {"type": "string"},
                               "description": "논문 순서대로, 각 논문의 짧은 영어 레이블 (≤6 words)"},
                    "rows": {"type": "array", "items": {
                        "type": "object",
                        "properties": {
                            "axis_en": {"type": "string", "description": "axis label in English (≤4 words)"},
                            "cells": {"type": "array", "items": {"type": "string"},
                                      "description": "논문 순서대로, 이 축에서 각 논문의 핵심 (≤8 words, English)"},
                        },
                        "required": ["axis_en", "cells"],
                    }},
                    "common_en": {"type": "string",
                                  "description": "shared ground of the papers (≤12 words, English)"},
                },
                "required": ["labels", "rows", "common_en"],
            },
        },
        "required": ["overview_ko", "axes", "quick_table", "reading_guide_ko",
                     "diagram_spec_en"],
    },
}


def _section_text(p, name):
    """Section text for the prompt. Evaluation 은 점수 표(| 로 시작하는 행)를
    걷어내고 총평 서술만 남긴다 — 점수 비교는 하지 않는다."""
    text = p["sections"].get(name, "")
    if name == "Evaluation":
        text = "\n".join(ln for ln in text.splitlines()
                         if not ln.lstrip().startswith("|"))
    return text.strip()[:2000]


def _build_prompt(papers):
    blocks = []
    for i, p in enumerate(papers, 1):
        sec_txt = "\n".join(
            f"### {name}\n{_section_text(p, name)}"
            for name in _SECTIONS if p["sections"].get(name))
        authors = ", ".join(p["authors"][:6])
        conn_txt = "\n".join(
            f"- {c['title']} ({c['relation']}): {c['reason'][:150]}"
            for c in p["connections"]) or "- (없음)"
        blocks.append(f"[P{i}] slug={p['slug']}\n제목: {p['title']}\n"
                      f"저자: {authors}\n연도: {p['date']}\n분류: {p['category']}\n"
                      f"{sec_txt}\n### 같이 보면 좋은 논문\n{conn_txt}")
    papers_txt = "\n\n---\n\n".join(blocks)
    return (
        f"다음 {len(papers)}편의 논문 리뷰를 매끄럽게 비교 분석하라.\n\n"
        f"{papers_txt}\n\n"
        "지침:\n"
        "- 최상위 필드 5개(overview_ko, axes, quick_table, reading_guide_ko, "
        "diagram_spec_en)를 하나도 빠뜨리지 말고 모두 채울 것 — overview_ko 를 "
        "가장 먼저 작성하라\n"
        f"- axes 는 정확히 이 6축을 이 순서로: {', '.join(_AXES)}\n"
        "- 각 축의 entries 에는 모든 논문을 slug 로 포함\n"
        "- '연구 지형 (같이 보면 좋은 논문)' 축에서는 각 논문의 주변 논문 목록이 "
        "그리는 연구 지형을 비교 — 공유하는 이웃, 서로 다른 계보와 응용 방향\n"
        "- quick_table 은 같은 6축, cells 는 논문 순서(P1, P2, ...)대로 한 줄 요약\n"
        "- 한국어 서술, 전문용어·모델명은 영어 유지. 근거 없는 우열 판정 금지 — "
        "리뷰에 있는 내용만 사용\n"
        "- 점수(숫자 평점)는 언급·비교하지 말 것\n"
        "- 서로 다른 관점(문제를 보는 시각), originality 의 결, 결과의 성격 차이를 "
        "드러내는 데 집중\n"
        "- diagram_spec_en 은 비교 다이어그램에 그대로 렌더링된다 — 짧고 명확한 "
        "영어 문구만 사용 (rows 는 앞의 5축 요약, 연구 지형 축은 제외)\n"
        "- axes 의 각 원소는 반드시 {\"axis_ko\": ..., \"entries\": "
        "[{\"slug\": ..., \"summary_ko\": ...}], \"synthesis_ko\": ...} 형태의 "
        "객체, quick_table 의 각 원소는 {\"axis_ko\": ..., \"cells\": [...]} 객체"
    )


def _valid_comp(out):
    """Tool input 이 렌더링 가능한 구조인지 검증. 문제면 사유 문자열 반환."""
    for k in _TOOL["input_schema"]["required"]:
        if k not in out:
            return f"missing key: {k}"
    axes = out.get("axes")
    if not isinstance(axes, list) or not axes:
        return "axes is not a non-empty list"
    for ax in axes:
        if not isinstance(ax, dict) or not ax.get("axis_ko") \
                or not isinstance(ax.get("entries"), list):
            return f"malformed axis: {str(ax)[:120]}"
        for e in ax["entries"]:
            if not isinstance(e, dict) or "slug" not in e or "summary_ko" not in e:
                return f"malformed entry: {str(e)[:120]}"
    for row in out.get("quick_table", []):
        if not isinstance(row, dict) or not isinstance(row.get("cells"), list):
            return f"malformed quick_table row: {str(row)[:120]}"
    spec = out.get("diagram_spec_en")
    if not isinstance(spec, dict) or not isinstance(spec.get("labels"), list) \
            or not isinstance(spec.get("rows"), list):
        return f"malformed diagram_spec_en: {str(spec)[:120]}"
    return ""


def compare_llm(papers):
    from anthropic import Anthropic
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        try:
            with open(os.path.join(ROOT, "config.json"), encoding="utf-8") as f:
                key = json.load(f).get("anthropic_api_key")
        except Exception:
            pass
    if not key:
        raise SystemExit("ANTHROPIC_API_KEY 없음")
    client = Anthropic(api_key=key, timeout=300.0, max_retries=4)
    base_prompt = _build_prompt(papers)
    required = ", ".join(_TOOL["input_schema"]["required"])
    extra = ""
    last_err = ""
    for attempt in range(1, 4):
        # adaptive-thinking 모델은 thinking 토큰이 max_tokens 에 포함되므로
        # 여유 있게 잡아야 tool input 이 잘리지 않는다.
        resp = client.messages.create(
            model=COMPARE_MODEL,
            max_tokens=24000,
            tools=[_TOOL],
            tool_choice={"type": "tool", "name": "emit_comparison"},
            messages=[{"role": "user", "content": base_prompt + extra}],
        )
        block = next((b for b in resp.content if b.type == "tool_use"), None)
        out = block.input if block is not None else {}
        problem = _valid_comp(out) if isinstance(out, dict) else "input not a dict"
        if not problem:
            return out
        got = sorted(out.keys()) if isinstance(out, dict) else []
        last_err = f"stop_reason={resp.stop_reason}, {problem}, got={got}"
        log(f"  attempt {attempt}: invalid tool input ({last_err}) — retrying")
        # 필드 누락이 확률적으로 발생하므로, 무엇이 잘못됐는지 명시해 교정한다.
        extra = (f"\n\n[재시도 지시] 직전 응답은 무효였다 — 문제: {problem}. "
                 f"emit_comparison 의 required 최상위 필드({required})를 하나도 "
                 f"빠뜨리지 말고 전부 채워 완전한 객체를 다시 제출하라. "
                 f"overview_ko 를 가장 먼저 작성하라.")
    raise SystemExit(f"비교 생성 실패: {last_err}")


# ── markdown / html emit ─────────────────────────────────────────────────────

def _comp_title(papers):
    """Plain-text title: [비교] '제목1' vs '제목2'"""
    joined = " vs ".join(f"'{p['title'][:60]}'" for p in papers)
    return f"[비교] {joined}"


def _comp_title_html(papers):
    """h1 markup — '[비교]' 와 'vs' 는 회색으로."""
    parts = [f"&#39;{RH.esc(p['title'][:60])}&#39;" for p in papers]
    joined = ' <span class="cmp-gray">vs</span> '.join(parts)
    return f'<span class="cmp-gray">[비교]</span> {joined}'


def generate_comparison_image(papers, comp, out_dir):
    """PaperBanana 로 두(N) 논문 비교 다이어그램 생성 → comparison.png.

    실패해도 페이지 생성은 계속한다 (이미지 없이). COMPARE_IMAGE=0 으로 스킵.
    """
    if os.environ.get("COMPARE_IMAGE", "1") == "0":
        log("  diagram: skipped (COMPARE_IMAGE=0)")
        return False
    spec = comp.get("diagram_spec_en") or {}
    labels = spec.get("labels") or [p["title"][:40] for p in papers]
    rows = spec.get("rows") or []
    common = spec.get("common_en", "")
    row_lines = "\n".join(
        f"- {r.get('axis_en', '')}: " + " | ".join(r.get("cells", []))
        for r in rows)
    method = (
        f"# Side-by-side comparison of {len(papers)} research papers\n\n"
        f"A clean {len(papers)}-column versus-style comparison diagram.\n\n"
        f"Columns (one per paper, left to right): "
        + " / ".join(f'"{l}"' for l in labels) + "\n\n"
        f"Comparison rows (axis: one cell per column, left to right):\n{row_lines}\n\n"
        f"Bottom strip spanning all columns — shared ground: {common}\n\n"
        "Design: distinct accent color per column, axis labels on the left "
        "margin, short phrases only (no sentences), generous whitespace, "
        "no watermark, no extra text beyond the given phrases."
    )
    caption = ("Visual comparison of " + " vs ".join(labels)
               + " across problem framing, method, originality, results, and limitations.")
    try:
        from lib.paperbanana import generate_diagram
        import time as _t
        t0 = _t.time()
        log("  diagram: generating via PaperBanana...")
        png = generate_diagram(method, caption, aspect_ratio="16:9",
                               critic_rounds=2,
                               output_path=os.path.join(out_dir, "comparison.png"))
        if png:
            log(f"  diagram: OK ({len(png)//1024}KB, {int(_t.time() - t0)}s)")
            return True
        log("  diagram: generation returned None — page continues without image")
    except Exception as e:
        log(f"  diagram: failed ({e}) — page continues without image")
    return False


def build_markdown(papers, comp, has_image=False):
    lines = [f"# {_comp_title(papers)}", ""]
    if has_image:
        lines += ["![비교 다이어그램](comparison.png)", ""]
    for i, p in enumerate(papers, 1):
        doi = f" · DOI: {p['doi']}" if p["doi"] else ""
        lines.append(f"- **[P{i}] {p['title']}** ({p['date']}){doi}")
        for c in p["connections"]:
            lines.append(f"  - 같이 보면 좋은 논문 · {c['relation']}: {c['title']}")
    lines += ["", "## 총평", "", comp["overview_ko"], "", "## 한눈 비교", ""]
    header = "| 비교 축 | " + " | ".join(f"P{i}" for i in range(1, len(papers) + 1)) + " |"
    lines += [header, "|" + "---|" * (len(papers) + 1)]
    for row in comp.get("quick_table", []):
        cells = [c.replace("|", "/") for c in row.get("cells", [])]
        lines.append(f"| {row.get('axis_ko', '')} | " + " | ".join(cells) + " |")
    slug_to_label = {p["slug"]: f"P{i} · {p['title'][:50]}"
                     for i, p in enumerate(papers, 1)}
    for ax in comp.get("axes", []):
        lines += ["", f"## {ax.get('axis_ko', '')}", ""]
        for e in ax.get("entries", []):
            label = slug_to_label.get(e.get("slug", ""), e.get("slug", ""))
            lines += [f"**{label}**", "", e.get("summary_ko", ""), ""]
        lines += ["> " + ax.get("synthesis_ko", ""), ""]
    lines += ["## 읽기 가이드", "", comp.get("reading_guide_ko", ""), ""]
    return "\n".join(lines)


def _paper_card(p, i):
    authors = ", ".join(p["authors"][:4]) + (" 외" if len(p["authors"]) > 4 else "")
    doi_html = (f' · <a href="https://doi.org/{RH.esc(p["doi"])}" target="_blank">DOI</a>'
                if p["doi"] else "")
    review_href = f"../../{p['slug']}/index.html"
    conn_items = "".join(
        f'<li><span class="rel">{RH.esc(c["relation"])}</span>'
        f'<a href="../../{c["slug"]}/index.html">{RH.esc(c["title"][:70])}</a></li>'
        for c in p["connections"])
    conn_html = (f'<div class="cmp-conn-head">같이 보면 좋은 논문</div>'
                 f'<ul class="cmp-conn">{conn_items}</ul>') if conn_items else ""
    return (f'<div class="cmp-card"><div class="cmp-card-num">P{i}</div>'
            f'<div class="cmp-card-title"><a href="{review_href}">{RH.esc(p["title"])}</a></div>'
            f'<div class="cmp-card-meta">{RH.esc(authors)} ({RH.esc(p["date"])})'
            f'{doi_html}<br>{RH.esc(p["category"])}</div>'
            f'{conn_html}</div>')


_CMP_CSS = """
.cmp-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin: 1.2rem 0; }
.cmp-card { border: 1px solid #e0e0e8; border-radius: 10px; padding: 1rem; background: #fff; }
.cmp-card-num { font-weight: 700; color: ACCENT; font-size: 0.85rem; margin-bottom: 0.3rem; }
.cmp-card-title { font-weight: 600; line-height: 1.4; margin-bottom: 0.4rem; }
.cmp-card-title a { color: #1a1a2e; text-decoration: none; }
.cmp-card-title a:hover { color: ACCENT; }
.cmp-card-meta { font-size: 0.82rem; color: #666; margin-bottom: 0.5rem; }
.cmp-gray { color: #999; font-weight: 600; }
.cmp-hero { margin: 1.2rem 0; }
.cmp-hero img { width: 100%; border: 1px solid #e0e0e8; border-radius: 10px; }
.cmp-conn-head { font-size: 0.78rem; font-weight: 700; color: #888; margin-top: 0.6rem; border-top: 1px solid #eee; padding-top: 0.5rem; }
.cmp-conn { list-style: none; padding: 0; margin: 0.3rem 0 0; }
.cmp-conn li { font-size: 0.78rem; margin: 0.2rem 0; color: #555; line-height: 1.4; }
.cmp-conn a { color: #1a1a2e; text-decoration: none; }
.cmp-conn a:hover { color: ACCENT; text-decoration: underline; }
.cmp-conn .rel { color: ACCENT; font-weight: 600; margin-right: 0.35rem; }
.cmp-synthesis { border-left: 4px solid ACCENT; background: ACCENT_BG; padding: 0.7rem 1rem; border-radius: 0 8px 8px 0; margin: 0.8rem 0 1.4rem; }
.dl-bar { margin: 0.6rem 0 1.4rem; }
.dl-btn { background: ACCENT; color: #fff; border: none; border-radius: 8px; padding: 0.5rem 1rem; font-size: 0.88rem; cursor: pointer; font-family: inherit; }
.dl-btn:hover { background: ACCENT_DARK; }
"""


def build_html(papers, comp, md_text, theme, name, image_b64=None):
    title = _comp_title(papers)
    # 이미지는 base64 인라인 — .html 다운로드 시에도 페이지가 자기완결이 되도록.
    hero = (f'<div class="cmp-hero"><img src="data:image/png;base64,{image_b64}" '
            'alt="비교 다이어그램"></div>') if image_b64 else ""
    cards = '<div class="cmp-cards">' + "".join(
        _paper_card(p, i) for i, p in enumerate(papers, 1)) + "</div>"

    n = len(papers)
    thead = ("<tr><th>비교 축</th>" +
             "".join(f"<th>P{i}</th>" for i in range(1, n + 1)) + "</tr>")
    trows = "".join(
        "<tr><td><strong>{}</strong></td>{}</tr>".format(
            RH.esc(r.get("axis_ko", "")),
            "".join(f"<td>{RH.esc(c)}</td>" for c in r.get("cells", [])))
        for r in comp.get("quick_table", []))
    table = f"<table><thead>{thead}</thead><tbody>{trows}</tbody></table>"

    slug_to_label = {p["slug"]: f"P{i} · {p['title'][:50]}"
                     for i, p in enumerate(papers, 1)}
    ax_html = []
    for ax in comp.get("axes", []):
        parts = [f"<h2>{RH.esc(ax.get('axis_ko', ''))}</h2>"]
        for e in ax.get("entries", []):
            label = slug_to_label.get(e.get("slug", ""), e.get("slug", ""))
            parts.append(f"<p><strong>{RH.esc(label)}</strong></p>")
            parts.append(RH.md_section_to_html(e.get("summary_ko", "")))
        parts.append(f'<div class="cmp-synthesis">'
                     f'{RH.md_section_to_html(ax.get("synthesis_ko", ""))}</div>')
        ax_html.append('<div class="section">' + "".join(parts) + "</div>")

    # .md 다운로드: 마크다운 원문을 JS 문자열로 내장 (</ 는 태그 조기 종료 방지)
    md_js = json.dumps(md_text, ensure_ascii=False).replace("</", "<\\/")
    name_js = json.dumps(name)
    dl_js = ("function _dl(blob, fname) { "
             "var a = document.createElement('a'); "
             "a.href = URL.createObjectURL(blob); "
             "a.download = fname; a.click(); "
             "URL.revokeObjectURL(a.href); } "
             "function downloadCmpMd() { "
             "_dl(new Blob([window._CMP_MD], {type: 'text/markdown'}), "
             "window._CMP_NAME + '.md'); } "
             "function downloadCmpHtml() { "
             "var h = '<!DOCTYPE html>' + document.documentElement.outerHTML; "
             "_dl(new Blob([h], {type: 'text/html'}), "
             "window._CMP_NAME + '.html'); }")

    css = (RH.get_css(theme) + "\n" + RH.get_audio_css(theme) + "\n" +
           _CMP_CSS.replace("ACCENT_DARK", theme["accent_dark"])
                   .replace("ACCENT_BG", theme["accent_bg"])
                   .replace("ACCENT", theme["accent"]))
    audio_ctx = {"title": title, "review": md_text, "connections": []}

    body = f"""<div class="container">
<h1>{_comp_title_html(papers)}</h1>
<div class="dl-bar">
<button class="dl-btn" onclick="downloadCmpMd()">.md 다운로드</button>
<button class="dl-btn" onclick="downloadCmpHtml()">.html 다운로드</button>
</div>
{RH.audio_bar_html()}
{hero}
{cards}
<div class="section"><h2>총평</h2>{RH.md_section_to_html(comp["overview_ko"])}</div>
<div class="section"><h2>한눈 비교</h2>{table}</div>
{"".join(ax_html)}
<div class="section"><h2>읽기 가이드</h2>{RH.md_section_to_html(comp.get("reading_guide_ko", ""))}</div>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{RH.esc(title)}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/font-kopub/1.0/kopubdotum.css">
<style>
{css}
</style>
</head>
<body>
{body}
{RH.audio_modal_html()}
<script>
window._CMP_MD = {md_js};
window._CMP_NAME = {name_js};
{dl_js}
</script>
{RH.audio_script_block(audio_ctx)}
<footer style="text-align:center;padding:2rem 0 1rem;color:#999;font-size:0.85rem;border-top:1px solid #eee;margin-top:3rem;">
Developed by Jehyun Lee, KIST AIX Strategy Department | jehyun.lee@gmail.com
</footer>
</body>
</html>"""


# ── entrypoint ───────────────────────────────────────────────────────────────

def run_compare(slug_tokens):
    index = _load_index()
    slugs = resolve_slugs(slug_tokens, index)
    if not 2 <= len(slugs) <= MAX_PAPERS:
        raise SystemExit(f"논문 2~{MAX_PAPERS}편을 지정하세요 (현재 {len(slugs)})")
    slug_titles = {p["slug"]: (p.get("title") or p["slug"]) for p in index}
    all_conns = RH._load_connections()
    papers = [load_paper(s, index, slug_titles, all_conns) for s in slugs]
    log(f"Comparing {len(papers)} papers via {COMPARE_MODEL}:")
    for p in papers:
        log(f"  - {p['slug']} ({len(p['connections'])} connections)")

    name = "_vs_".join(p["num"] for p in papers)
    out_dir = os.path.join(COMPARE_DIR, name)
    os.makedirs(out_dir, exist_ok=True)

    comp = compare_llm(papers)
    has_image = generate_comparison_image(papers, comp, out_dir)
    image_b64 = None
    if has_image:
        import base64
        with open(os.path.join(out_dir, "comparison.png"), "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("ascii")
    md_text = build_markdown(papers, comp, has_image=has_image)
    theme = RH.THEMES.get(papers[0]["topic"], RH.THEMES["ai4s"])
    html = build_html(papers, comp, md_text, theme, name, image_b64=image_b64)
    md_path = os.path.join(out_dir, "comparison.md")
    html_path = os.path.join(out_dir, "index.html")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    log(f"Wrote {html_path}")
    return {"ok": True, "html": html_path, "md": md_path, "dir": out_dir,
            "title": _comp_title(papers)}


def main():
    ap = argparse.ArgumentParser(description="Multi-paper comparison generator")
    ap.add_argument("--slugs", required=True,
                    help="comma-separated slugs or NNN numbers (2-6 papers)")
    args = ap.parse_args()
    result = run_compare([t for t in args.slugs.split(",") if t.strip()])
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    from _env_guard import force_py312
    force_py312()
    main()
