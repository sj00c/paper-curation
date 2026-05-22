"""
Paper-Curation --local --update-force 배치 실행 스크립트.

사용법:
  PYTHONUTF8=1 python run_update_force.py --topic ai4s
  # --concurrency 기본값 16 (Anthropic Tier 4). Tier 1~3 은 4~12 로 낮춤.

기능:
  1. Zotero 컬렉션에서 전체 논문 fetch
  2. 기존 review.md, text.md, figures/ 삭제
  3. PDF 파싱 → text.md
  4. Figure 추출 + Gemini Flash 검증 (5라운드, 감쇠)
  5. review.md 작성 (Claude Haiku)
  6. index.html 변환 (review_to_html.py)
  7. 진행 상황을 checkpoint.json에 저장 (중단 후 재개 가능)

소요 시간 예상: 840편 × 병렬 4 = ~20시간
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Paths
from config_loader import (
    PAPERS_DIR as _PAPERS_DIR, PIPELINE_DIR, _ssl_ctx,
    get_zotero_api_key, get_zotero_user_id, get_collection_key, get_collections, get_zotero_dir,
    get_topic_dir,
)
from lib.categories import category_slug
PAPERS_DIR = str(_PAPERS_DIR)
PROJECT_ROOT = PIPELINE_DIR.parent


def _split_cats_by_image_presence(topic, cats):
    """Split categories by whether their timeline image exists.

    Returns (cats_with_image, cats_missing_image).
    Image path: docs/{topic}/category_timeline_{slug}.{png,webp}
    """
    topic_dir = get_topic_dir(topic)
    with_image = []
    missing = []
    for cat in cats:
        slug = category_slug(cat)
        has_image = any(
            os.path.exists(os.path.join(str(topic_dir), f"category_timeline_{slug}.{ext}"))
            for ext in ("png", "webp")
        )
        (with_image if has_image else missing).append(cat)
    return with_image, missing

# topic_modeling.py / classify_papers.py 는 UMAP + hdbscan + sentence-transformers
# 의존. macOS + Python 3.14 (conda env `py314`) 에서는 numba 0.65 / llvmlite 0.47
# 휠로 단일 환경에서 동작한다. 서브프로세스도 현재 인터프리터 (sys.executable) 를
# 그대로 사용하므로 활성화된 env 가 그대로 상속된다. 변수명은 호환을 위해 유지.
TOPIC_MODELING_PYTHON = sys.executable

ZOTERO_DIR = get_zotero_dir()

API_KEY = get_zotero_api_key()
USER_ID = get_zotero_user_id()
COLLECTIONS = get_collections()

# Checkpoint
CHECKPOINT_FILE = str(PIPELINE_DIR / "_update_force_checkpoint.json")


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "failed": [], "phase": "init"}


_cp_lock = threading.Lock()
_slug_to_zotero_key = {}


def save_checkpoint(cp):
    with _cp_lock:
        with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
            json.dump(cp, f, ensure_ascii=False, indent=2)


# ── Phase 1: Fetch Zotero ──

def fetch_zotero_items(collection_key):
    items = []
    start = 0
    while True:
        url = (f"https://api.zotero.org/users/{USER_ID}/collections/"
               f"{collection_key}/items/top?limit=100&start={start}&format=json&sort=title")
        req = urllib.request.Request(url, headers={"Zotero-API-Key": API_KEY})
        with urllib.request.urlopen(req, context=_ssl_ctx) as resp:
            batch = json.load(resp)
        if not batch:
            break
        for item in batch:
            d = item["data"]
            if d.get("itemType") in ("attachment", "note",
                                      "forumPost", "videoRecording"):
                continue
            items.append(d)
        start += 100
        if len(batch) < 100:
            break
    return items


# ── PDF match audit log (Phase 1a: diagnose 139-paper mismatch bug) ──
# Every find_pdf() call appends one JSON line to this file so we can
# retroactively audit which matches used the weak fuzzy fallback.
_AUDIT_LOG_PATH = None  # lazily initialised in _audit_append()


def _audit_append(record):
    """Append one JSONL record to the find_pdf audit log."""
    global _AUDIT_LOG_PATH
    try:
        if _AUDIT_LOG_PATH is None:
            logs_dir = os.path.join(os.path.dirname(__file__), "_logs")
            os.makedirs(logs_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            _AUDIT_LOG_PATH = os.path.join(logs_dir, f"find_pdf_audit_{ts}.jsonl")
        with open(_AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass  # audit log never breaks the pipeline


def _extract_arxiv_id_from_item(item):
    """Try to read an arXiv ID from a Zotero item's url/DOI/archiveID."""
    for field in ("url", "DOI", "archiveID", "extra"):
        val = item.get(field, "") or ""
        m = re.search(r"(\d{4}\.\d{4,5})", val)
        if m:
            return m.group(1)
    return None


# Global flag toggled by CLI. When True, fuzzy fallback is disabled entirely.
_STRICT_PDF = False


def find_pdf(item):
    """Find local PDF path for a Zotero item.

    Returns (path, method). `method` is one of:
      - zotero_children_abs     : Zotero child API returned an absolute path that exists
      - zotero_children_basename: Zotero child API path's basename found under ZOTERO_DIR
      - doi_filename            : DOI string appears in a PDF filename under ZOTERO_DIR
      - arxiv_filename          : arXiv ID appears in a PDF filename under ZOTERO_DIR
      - fuzzy                   : weak title-keyword match (LAST RESORT, logged)
      - no_match                : no candidate — caller skips the paper
    """
    key = item.get("key", "")
    title = item.get("title", "")

    # Priority 1: Zotero children API (authoritative attachment path)
    try:
        url = f"https://api.zotero.org/users/{USER_ID}/items/{key}/children?format=json"
        req = urllib.request.Request(url, headers={"Zotero-API-Key": API_KEY})
        with urllib.request.urlopen(req, timeout=10, context=_ssl_ctx) as resp:
            children = json.load(resp)
        for c in children:
            cd = c.get("data", {})
            if cd.get("itemType") != "attachment":
                continue
            if cd.get("contentType") not in ("application/pdf", ""):
                continue
            path = cd.get("path", "")
            if not path.lower().endswith(".pdf"):
                continue
            if os.path.exists(path):
                _audit_append({"key": key, "title": title[:80],
                               "method": "zotero_children_abs", "path": path})
                return path, "zotero_children_abs"
            fname = os.path.basename(path)
            alt = os.path.join(ZOTERO_DIR, fname)
            if os.path.exists(alt):
                _audit_append({"key": key, "title": title[:80],
                               "method": "zotero_children_basename", "path": alt})
                return alt, "zotero_children_basename"
    except Exception as e:
        _audit_append({"key": key, "title": title[:80],
                       "method": "children_api_error", "error": str(e)[:200]})

    # Priority 2: DOI in filename (reliable when present)
    doi = (item.get("DOI") or item.get("doi") or "").strip()
    if doi:
        doi_norm = re.sub(r"[^a-z0-9]", "", doi.lower())
        if len(doi_norm) >= 10:  # avoid accidental short-DOI collisions
            for fname in os.listdir(ZOTERO_DIR):
                if not fname.lower().endswith(".pdf"):
                    continue
                fname_norm = re.sub(r"[^a-z0-9]", "", fname.lower())
                if doi_norm in fname_norm:
                    matched = os.path.join(ZOTERO_DIR, fname)
                    _audit_append({"key": key, "title": title[:80],
                                   "method": "doi_filename", "path": matched,
                                   "doi": doi})
                    return matched, "doi_filename"

    # Priority 3: arXiv ID in filename
    arxiv_id = _extract_arxiv_id_from_item(item)
    if arxiv_id:
        for fname in os.listdir(ZOTERO_DIR):
            if not fname.lower().endswith(".pdf"):
                continue
            if arxiv_id in fname:
                matched = os.path.join(ZOTERO_DIR, fname)
                _audit_append({"key": key, "title": title[:80],
                               "method": "arxiv_filename", "path": matched,
                               "arxiv_id": arxiv_id})
                return matched, "arxiv_filename"

    # Priority 4 (optional): fuzzy title match — STRICTER than before.
    # The original 3-of-5 keyword rule caused the 139-paper mismatch bug.
    # We now require: (a) at least 5 significant keywords from the title,
    # (b) at least 5 of them appear in the filename (score >= 5), and
    # (c) coverage >= 80% of candidate keywords. Disabled entirely under
    # --strict-pdf.
    if _STRICT_PDF or not title:
        _audit_append({"key": key, "title": title[:80], "method": "no_match",
                       "reason": "strict_pdf" if _STRICT_PDF else "no_title"})
        return None, "no_match"

    title_words = re.sub(r"[^a-z0-9\s]", "", title.lower()).split()
    key_words = [w for w in title_words if len(w) > 3][:8]
    if len(key_words) < 5:
        _audit_append({"key": key, "title": title[:80], "method": "no_match",
                       "reason": "too_few_keywords", "keywords": key_words})
        return None, "no_match"

    best_match = None
    best_score = 0
    for fname in os.listdir(ZOTERO_DIR):
        if not fname.lower().endswith(".pdf"):
            continue
        fname_lower = fname.lower()
        score = sum(1 for w in key_words if w in fname_lower)
        if score > best_score:
            best_score = score
            best_match = fname

    coverage = best_score / max(1, len(key_words))
    if best_match and best_score >= 5 and coverage >= 0.8:
        matched = os.path.join(ZOTERO_DIR, best_match)
        _audit_append({"key": key, "title": title[:80], "method": "fuzzy",
                       "path": matched, "score": best_score,
                       "coverage": round(coverage, 2), "keywords": key_words,
                       "WARNING": "weak match — verify with audit_matching.py"})
        log(f"  WARN fuzzy PDF match for '{title[:60]}' "
            f"(score {best_score}/{len(key_words)}, cov {coverage:.0%})")
        return matched, "fuzzy"

    _audit_append({"key": key, "title": title[:80], "method": "no_match",
                   "reason": "fuzzy_below_threshold", "best_score": best_score,
                   "best_candidate": best_match, "keywords": key_words})
    return None, "no_match"


# ── Zotero ↔ text.md sanity check (zero-cost PDF integrity gate) ──

def _zotero_text_sanity(item, text_md_path, min_title_coverage=0.6):
    """Verify Zotero metadata (title/DOI/first author) appears in the extracted
    text. Catches the "Zotero attachment is wrong PDF" failure mode that even
    `--strict-pdf` cannot detect: find_pdf returned Zotero's linked file, but
    that file is the wrong paper.

    All signals are local regex/substring — no LLM call.

    Returns (passed: bool, reason: str).
    """
    if not os.path.exists(text_md_path):
        return True, "no_text_skip"  # text extraction failed; downstream already fails
    try:
        with open(text_md_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read(6000).lower()
    except Exception:
        return True, "read_error_skip"

    # 1. Title keyword coverage
    title_words = re.sub(r"[^a-z0-9\s]", " ", (item.get("title") or "").lower()).split()
    kw = [w for w in title_words if len(w) > 3][:6]
    title_hits = sum(1 for w in kw if w in text) if kw else 0
    title_ok = (not kw) or title_hits >= max(3, int(len(kw) * min_title_coverage))

    # 2. DOI exact (ignore non-alphanumeric)
    doi = re.sub(r"[^a-z0-9]", "", (item.get("DOI") or "").lower())
    text_norm = re.sub(r"[^a-z0-9]", "", text)
    doi_ok = True if len(doi) < 10 else (doi in text_norm)

    # 3. First author lastName
    creators = item.get("creators", []) or []
    last = ""
    for c in creators:
        last = (c.get("lastName") or "").lower()
        if last:
            break
    author_ok = True if len(last) < 3 else (last in text)

    # title + doi 둘 다 통과면 author 무관 (corporate author, 이미지 헤더 등
    # 저자명 추출 실패가 흔해서 단독 blocker로 쓰지 않음).
    if title_ok and doi_ok:
        return True, f"ok (title {title_hits}/{len(kw)} doi=T author={author_ok})"
    if title_ok and author_ok:
        return True, f"ok (title {title_hits}/{len(kw)} author=T doi={doi_ok})"
    return False, (f"title_hits={title_hits}/{len(kw)} "
                   f"doi_ok={doi_ok} author_ok={author_ok}")


# ── Phase 2: Extract text.md (OpenDataLoader → PyMuPDF fallback) ──

def extract_text(pdf_path, slug_dir):
    text_path = os.path.join(slug_dir, "text.md")

    # Strategy 1: OpenDataLoader (better table/formula/structure extraction)
    # NOTE: pip package is `opendataloader-pdf` but Python import name is
    # `opendataloader_pdf` (underscore). Earlier code used `opendataloader.pdf`
    # which silently ImportError'd and fell through to PyMuPDF every time.
    # Requires Java Runtime (e.g. `brew install --cask temurin`).
    try:
        import tempfile, re
        from opendataloader_pdf import convert as odl_convert
        with tempfile.TemporaryDirectory() as tmpdir:
            odl_convert(input_path=[pdf_path], output_dir=tmpdir,
                        format="markdown", quiet=True)
            md_files = [f for f in os.listdir(tmpdir) if f.endswith(".md")]
            if md_files:
                with open(os.path.join(tmpdir, md_files[0]), "r", encoding="utf-8") as f:
                    text = f.read()
                if text and len(text) > 100:
                    # OpenDataLoader exports its own image dump and embeds
                    # `![image N](relative/path.png)` lines pointing to a
                    # sibling dir that paper-curation never tracks (we use
                    # PyMuPDF for figures/). Collapse those refs into
                    # `[Figure N]` so the body flow survives but the broken
                    # paths don't pollute Claude review prompts.
                    text = re.sub(r'!\[image\s*(\d+)\]\([^)]*\)',
                                  r'[Figure \1]', text)
                    text = re.sub(r'\n{3,}', '\n\n', text)
                    with open(text_path, "w", encoding="utf-8") as f:
                        f.write(text)
                    return True
    except ImportError:
        pass  # OpenDataLoader not installed → fallback
    except Exception as e:
        log(f"  OpenDataLoader failed: {e}, falling back to PyMuPDF")

    # Strategy 2: PyMuPDF fallback
    try:
        import fitz
        doc = fitz.open(pdf_path)
        text = "\n".join(doc[p].get_text() for p in range(len(doc)))
        doc.close()
        if text and len(text) > 100:
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(text)
            return True
    except Exception as e:
        log(f"  text.md failed: {e}")
    return False


# ── Phase 3: Extract figures + Gemini validation ──

def extract_figures(pdf_path, slug_dir):
    fig_dir = os.path.join(slug_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    try:
        import fitz
    except ImportError:
        log("  PyMuPDF not available")
        return []

    doc = fitz.open(pdf_path)
    figures = []
    MARGIN = 30
    MAX_ROUNDS = 5

    # Gemini validation function
    def validate(img_path, caption):
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY", ""))
            with open(img_path, "rb") as f:
                img_bytes = f.read()
            prompt = (f"Evaluate cropping of this academic figure.\nCaption: {caption}\n"
                      f"Check: (1) content CLIPPED at edges? (2) EXCESS body text?\n"
                      f"JSON only: {{\"status\":\"ok\"|\"clipped\"|\"oversized\"|\"both\","
                      f"\"issues\":\"brief\",\"adjust_pt\":{{\"top\":0,\"bottom\":0,\"left\":0,\"right\":0}}}}\n"
                      f"adjust_pt: positive=expand, negative=shrink. PDF points.")
            resp = client.models.generate_content(
                model="gemini-3.1-pro-preview",
                contents=[types.Part.from_bytes(data=img_bytes, mime_type="image/png"), prompt])
            text = resp.text.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text)
        except Exception:
            return {"status": "ok", "adjust_pt": {}}

    for pn in range(min(30, len(doc))):
        page = doc[pn]
        pw, ph = page.rect.width, page.rect.height
        text_dict = page.get_text("dict")
        txt_blocks = [b for b in text_dict["blocks"] if b["type"] == 0]
        img_blocks = [b for b in text_dict["blocks"] if b["type"] == 1
                      and (b["bbox"][2] - b["bbox"][0]) > 50
                      and (b["bbox"][3] - b["bbox"][1]) > 50]

        for tb in txt_blocks:
            first_line = tb["lines"][0] if tb["lines"] else None
            if not first_line:
                continue
            lt = "".join(s["text"] for s in first_line["spans"])
            m = re.match(r"(Figure|Fig\.?)\s*(\d+)", lt)
            if not m:
                continue
            fig_num = int(m.group(2))
            if fig_num in [int(f["name"]) for f in figures]:
                continue
            if fig_num > 5:
                continue

            cap_top = tb["bbox"][1]
            cap_bottom = tb["bbox"][3]
            caption = lt.strip()[:120]

            # Full page start
            x0, y0 = 0, 0
            x1, y1 = pw, ph

            out = os.path.join(fig_dir, f"fig{fig_num}.png")

            for rnd in range(MAX_ROUNDS + 1):
                # Try rendering with decreasing resolution on error
                rendered = False
                for scale in [3, 2, 1]:
                    try:
                        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale),
                                              clip=fitz.Rect(x0, y0, x1, y1))
                        pix.save(out)
                        rendered = True
                        break
                    except Exception:
                        continue
                if not rendered:
                    break  # skip this figure entirely

                if rnd == MAX_ROUNDS:
                    break

                result = validate(out, caption)
                if result.get("status") == "ok":
                    break

                # Round 0: educated guess
                if rnd == 0 and result.get("status") in ("oversized", "both"):
                    cap_cx = (tb["bbox"][0] + tb["bbox"][2]) / 2
                    cap_w = tb["bbox"][2] - tb["bbox"][0]
                    if cap_w < pw * 0.6:
                        if cap_cx < pw * 0.45:
                            x1 = pw * 0.52
                        elif cap_cx > pw * 0.55:
                            x0 = pw * 0.48
                    y1 = min(ph, cap_bottom + 15)
                    y0 = max(0, 40)
                    continue

                damping = [1.0, 0.8, 0.6, 0.45, 0.35][min(rnd, 4)]
                adj = result.get("adjust_pt", {})
                y0 = max(0, y0 - adj.get("top", 0) * damping)
                y1 = min(ph, y1 + adj.get("bottom", 0) * damping)
                x0 = max(0, x0 - adj.get("left", 0) * damping)
                x1 = min(pw, x1 + adj.get("right", 0) * damping)

            # Fallback
            final_ratio = (x1 - x0) * (y1 - y0) / (pw * ph)
            if final_ratio < 0.15:
                for scale in [3, 2, 1]:
                    try:
                        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
                        pix.save(out)
                        break
                    except Exception:
                        continue

            figures.append({"name": str(fig_num), "page": pn, "caption": caption})

    doc.close()
    return figures


# ── Phase 4: Write review.md (Claude Haiku → JSON → Template) ──

REVIEW_TEMPLATE = """# {title}

> **저자**: {authors} | **날짜**: {date} | {ref_label}: {ref_link}

---

## Essence

{fig_essence}
{essence}

## Motivation

- **Known**: {known}
- **Gap**: {gap}
- **Why**: {why}
- **Approach**: {approach}

## Achievement

{fig_achievement}
{achievement}

## How

{fig_how}
{how}

## Originality

{originality}

## Limitation & Further Study

{limitation}

## Evaluation

- Novelty: {novelty}/5
- Technical Soundness: {tech}/5
- Significance: {significance}/5
- Clarity: {clarity}/5
- Overall: {overall}/5

**총평**: {verdict}
"""


def write_review(item, slug_dir, figures):
    text_path = os.path.join(slug_dir, "text.md")
    if not os.path.exists(text_path):
        return False

    with open(text_path, "r", encoding="utf-8") as f:
        paper_text = f.read()[:15000]

    title = item.get("title", "")
    authors = ", ".join(
        f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
        for c in item.get("creators", [])
    )
    date = item.get("date", "")
    doi = item.get("DOI", "")
    abstract = item.get("abstractNote", "")

    fig_refs = ""
    for fig in figures:
        fig_refs += f"\n- Fig {fig['name']}: {fig['caption'][:80]}"

    try:
        from anthropic import Anthropic
        client = Anthropic()

        prompt = f"""논문을 분석하고 JSON으로 리뷰 필드를 반환하세요.

제목: {title}
Abstract: {abstract}
본문 (발췌): {paper_text[:12000]}
Figure 목록:{fig_refs}

JSON 필드 (모두 한국어 서술. 단 Jargon — 기술 용어·모델명·데이터셋·알고리즘·수식·프레임워크·제품명 등 — 은 원문 그대로 유지하고 번역하지 말 것. 예: "diffusion model을 사용한다" (O), "확산 모델(diffusion model)을 사용한다" (X)):
{{
  "essence": "1-2문장 핵심 요약",
  "fig_essence": "Essence에 가장 관련된 Figure 번호 (예: 1). 없으면 0",
  "known": "알려진 것 1-2문장",
  "gap": "연구 갭 1-2문장",
  "why": "왜 중요한지 1-2문장",
  "approach": "접근법 1-2문장",
  "achievement": "성과 (마크다운 번호 목록, 각 항목 **굵은 제목**: 설명)",
  "fig_achievement": "Achievement에 관련된 Figure 번호. 없으면 0",
  "how": "방법론 (마크다운 bullet 목록)",
  "fig_how": "How에 관련된 Figure 번호. 없으면 0",
  "originality": "독창성 (마크다운 bullet 목록)",
  "limitation": "한계 + 후속연구 (마크다운 bullet 목록)",
  "novelty": 4, "tech": 3, "significance": 4, "clarity": 4, "overall": 4,
  "verdict": "총평 1-2문장"
}}

JSON만 출력. 코드 블록 없이."""

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text)

        # Build figure insertions
        def fig_block(fig_num_str):
            try:
                n = int(fig_num_str)
            except (ValueError, TypeError):
                return ""
            if n == 0:
                return ""
            fig = next((f for f in figures if int(f["name"]) == n), None)
            if not fig:
                return ""
            cap = fig.get("caption", f"Figure {n}")
            return f"![Figure {n}](figures/fig{n}.png)\n\n*{cap}*\n"

        # DOI vs URL
        url = item.get("url", "")
        if doi:
            ref_label = "**DOI**"
            ref_link = f"[{doi}](https://doi.org/{doi})"
        elif url:
            ref_label = "**URL**"
            ref_link = f"[{url}]({url})"
        else:
            ref_label = "**DOI**"
            ref_link = "N/A"

        review_text = REVIEW_TEMPLATE.format(
            title=title, authors=authors, date=date,
            ref_label=ref_label, ref_link=ref_link,
            essence=data.get("essence", ""),
            fig_essence=fig_block(data.get("fig_essence", 0)),
            known=data.get("known", ""),
            gap=data.get("gap", ""),
            why=data.get("why", ""),
            approach=data.get("approach", ""),
            achievement=data.get("achievement", ""),
            fig_achievement=fig_block(data.get("fig_achievement", 0)),
            how=data.get("how", ""),
            fig_how=fig_block(data.get("fig_how", 0)),
            originality=data.get("originality", ""),
            limitation=data.get("limitation", ""),
            novelty=data.get("novelty", 3),
            tech=data.get("tech", 3),
            significance=data.get("significance", 3),
            clarity=data.get("clarity", 3),
            overall=data.get("overall", 3),
            verdict=data.get("verdict", ""),
        )

        review_path = os.path.join(slug_dir, "review.md")
        with open(review_path, "w", encoding="utf-8") as f:
            f.write(review_text.strip() + "\n")
        return True

    except Exception as e:
        log(f"  review.md failed: {e}")
        return False


def fix_python_list_literals(slug_dir):
    """Post-process: convert Python list literals ['a','b'] to markdown bullets."""
    review_path = os.path.join(slug_dir, "review.md")
    if not os.path.exists(review_path):
        return
    with open(review_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "['" not in content and '["' not in content:
        return
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        s = line.strip()
        if (s.startswith("[") and s.endswith("]") and
                ("'" in s or '"' in s) and len(s) > 20):
            # Parse by splitting on quote-comma-quote patterns
            inner = s[1:-1]  # remove [ ]
            # Split on ', ' or ", " patterns between items
            items = re.split(r"'\s*,\s*'|'\s*,\s*\"|\"'\s*,\s*'|\"'\s*,\s*\"", inner)
            if len(items) > 1:
                for item in items:
                    clean = item.strip().strip("'\"")
                    if clean:
                        new_lines.append(f"- {clean}")
                continue
        new_lines.append(line)
    new_content = "\n".join(new_lines)
    if new_content != content:
        with open(review_path, "w", encoding="utf-8") as f:
            f.write(new_content)


def validate_review_format(slug_dir):
    """Post-process: review.md 포맷 검증 + 자동 수정."""
    review_path = os.path.join(slug_dir, "review.md")
    if not os.path.exists(review_path):
        return
    with open(review_path, "r", encoding="utf-8") as f:
        content = f.read()
    issues = []

    # 1. 필수 섹션 존재 확인
    required = ["## Essence", "## Motivation", "## Achievement", "## How",
                 "## Originality", "## Limitation", "## Evaluation"]
    for sec in required:
        if sec not in content:
            issues.append(f"Missing section: {sec}")

    # 2. Python 리스트 리터럴 잔류
    if re.search(r"^\['.{20,}", content, re.MULTILINE):
        issues.append("Python list literal remaining")

    # 3. Evaluation 테이블 형식 잔류
    if "## Evaluation" in content:
        eval_part = content.split("## Evaluation")[-1][:500]
        if "| " in eval_part and "---" in eval_part:
            issues.append("Evaluation in table format")

    # 4. 빈 DOI 링크
    if "[](https://doi.org/)" in content:
        issues.append("Empty DOI link")

    # 5. 제목이 파일명
    title_m = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if title_m and ".pdf" in title_m.group(1):
        issues.append(f"Title contains filename: {title_m.group(1)[:40]}")

    if issues:
        slug = os.path.basename(slug_dir)
        log(f"  FORMAT ISSUES in {slug}: {issues}")

    return issues


def fix_figure_paths(slug_dir):
    """Post-process: replace placeholder URLs and broken figure paths with actual figure files."""
    review_path = os.path.join(slug_dir, "review.md")
    if not os.path.exists(review_path):
        return
    with open(review_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Build map of available figures
    fig_dir = os.path.join(slug_dir, "figures")
    fig_map = {}
    if os.path.isdir(fig_dir):
        for fname in os.listdir(fig_dir):
            m = re.match(r"fig(\d+)\.(png|webp)", fname)
            if m:
                fig_map[int(m.group(1))] = f"figures/{fname}"

    if not fig_map:
        return

    changed = False

    # Replace any external image URL `![alt](http(s)://...)` with the matching
    # local figure. Picks figure number from alt text ("Figure 3", "Fig.2",
    # "그림 1"); falls back to sequential assignment from available figures.
    seq_state = {"next": min(fig_map.keys())}
    sorted_keys = sorted(fig_map.keys())
    ext_replaced = 0

    def replace_external_image(match):
        nonlocal ext_replaced
        alt = match.group(1)
        target = None
        num_m = re.search(r"(?:Figure|Fig\.?|그림)\s*(\d+)", alt, re.IGNORECASE)
        if num_m:
            n = int(num_m.group(1))
            if n in fig_map:
                target = fig_map[n]
        if target is None:
            for k in sorted_keys:
                if k >= seq_state["next"]:
                    target = fig_map[k]
                    seq_state["next"] = k + 1
                    break
        if target is None:
            return match.group(0)
        ext_replaced += 1
        return f"![{alt}]({target})"

    new_content = re.sub(
        r"!\[([^\]]*)\]\(https?://[^)]+\)",
        replace_external_image,
        content,
    )
    if new_content != content:
        content = new_content
        changed = True

    # Legacy placeholder pattern fallback (cases without `![alt](...)` syntax,
    # e.g. inline `<img src=...>` shipped by an older prompt template).
    def replace_placeholder(match):
        url = match.group(0)
        fig_m = re.search(r"Fig[+_ ](\d+)", url)
        if fig_m:
            num = int(fig_m.group(1))
            if num in fig_map:
                return fig_map[num]
        if 1 in fig_map:
            return fig_map[1]
        return url

    if "placeholder" in content:
        new_content = re.sub(r"https://via\.placeholder\.com/[^\)]+", replace_placeholder, content)
        if new_content != content:
            content = new_content
            changed = True

    # Fix broken relative paths (e.g., figures/fig1.png when only .webp exists)
    def fix_ext(match):
        path = match.group(1)
        fig_m = re.match(r"figures/fig(\d+)\.(png|webp)", path)
        if fig_m:
            num = int(fig_m.group(1))
            if num in fig_map and fig_map[num] != path:
                return f"({fig_map[num]})"
        return match.group(0)

    new_content = re.sub(r"\((figures/fig\d+\.(?:png|webp))\)", fix_ext, content)
    if new_content != content:
        content = new_content
        changed = True

    if changed:
        with open(review_path, "w", encoding="utf-8") as f:
            f.write(content)
        slug = os.path.basename(slug_dir)
        log(f"  {slug}: fixed figure paths")


def fix_evaluation_format(slug_dir):
    """Post-process: convert any remaining Evaluation tables to list format."""
    review_path = os.path.join(slug_dir, "review.md")
    if not os.path.exists(review_path):
        return
    with open(review_path, "r", encoding="utf-8") as f:
        content = f.read()
    # If Evaluation has table rows, convert
    if "## Evaluation" in content and "| " in content.split("## Evaluation")[-1][:500]:
        eval_section = content.split("## Evaluation")[-1]
        scores = {}
        for label in ["Novelty", "Technical Soundness", "Significance", "Clarity", "Overall"]:
            m = re.search(rf'{label}\D*(\d+(?:\.\d+)?)\s*/\s*5', eval_section)
            if m:
                scores[label] = m.group(1)
        verdict_m = re.search(r'\*\*총평\*\*[:\s]*(.+?)(?:\n|$)', eval_section)
        verdict = verdict_m.group(1).strip() if verdict_m else ""

        new_eval = "\n## Evaluation\n\n"
        for label in ["Novelty", "Technical Soundness", "Significance", "Clarity", "Overall"]:
            new_eval += f"- {label}: {scores.get(label, '3')}/5\n"
        if verdict:
            new_eval += f"\n**총평**: {verdict}\n"

        before_eval = content.split("## Evaluation")[0]
        content = before_eval + new_eval
        with open(review_path, "w", encoding="utf-8") as f:
            f.write(content)


# ── Phase 5: Convert to HTML ──

def convert_to_html(slug):
    try:
        # Import review_to_html from repo
        sys.path.insert(0, str(PIPELINE_DIR))
        from review_to_html import convert_review, detect_topic
        md_path = os.path.join(PAPERS_DIR, slug, "review.md")
        html_path = os.path.join(PAPERS_DIR, slug, "index.html")
        index_path = os.path.join(PAPERS_DIR, "_papers_index.json")
        if not os.path.exists(md_path):
            return False
        topic = detect_topic(slug, index_path)
        html = convert_review(md_path, topic, slug)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    except Exception as e:
        log(f"  html failed: {e}")
        return False


# ── Process single paper ──

def make_slug(item, existing_slugs):
    """Match item to existing slug or generate new one."""
    title = item.get("title", "Unknown")
    # Normalize for matching
    norm_title = re.sub(r"[^a-z0-9]", "", title.lower())[:40]

    # Match against existing slugs (skip number prefix)
    for s in existing_slugs:
        # Extract text part after NNN_
        parts = s.split("_", 1)
        if len(parts) < 2:
            continue
        slug_text = re.sub(r"[^a-z0-9]", "", parts[1].lower())[:40]
        if norm_title[:25] == slug_text[:25] and len(norm_title[:25]) > 10:
            return s

    # No match → new slug
    safe = "".join(c if c.isalnum() or c in " -_" else "" for c in title)[:60].strip()
    safe = safe.replace(" ", "_")
    # Find max slug number across all existing
    max_num = 0
    for d in existing_slugs:
        m = re.match(r"(\d+)_", d)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return f"{max_num + 1:03d}_{safe}"


def paper_has_other_topics(slug):
    """Check if paper belongs to topics other than the current one."""
    index_path = os.path.join(PAPERS_DIR, "_papers_index.json")
    if not os.path.exists(index_path):
        return False
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            papers = json.load(f)
        for p in papers:
            if p.get("slug") == slug:
                topics = p.get("topics", [])
                return len(topics) > 1
    except Exception:
        pass
    return False


MAX_RETRIES = 3


def _do_process(item, slug, slug_dir, pdf_path):
    """Single attempt: text.md → figures → review.md → index.html.
    Returns (status, reason) — status is 'ok' or 'fail'."""

    # Extract text
    log(f"  {slug}: extracting text...")
    extract_text(pdf_path, slug_dir)
    text_path = os.path.join(slug_dir, "text.md")
    if not os.path.exists(text_path) or os.path.getsize(text_path) < 100:
        return "fail", "text_extraction_failed"

    # Zotero ↔ text sanity check (zero-cost PDF integrity gate)
    ok, reason = _zotero_text_sanity(item, text_path)
    if not ok:
        log(f"  {slug}: SANITY FAIL ({reason}) — aborting review")
        return "fail", f"sanity_mismatch:{reason}"

    # Extract figures
    log(f"  {slug}: extracting figures...")
    figures = extract_figures(pdf_path, slug_dir)
    log(f"  {slug}: {len(figures)} figures extracted")

    # Write review
    log(f"  {slug}: writing review...")
    write_review(item, slug_dir, figures)
    review_path = os.path.join(slug_dir, "review.md")
    if not os.path.exists(review_path) or os.path.getsize(review_path) < 200:
        return "fail", "review_write_failed"

    # Post-process
    fix_python_list_literals(slug_dir)
    fix_evaluation_format(slug_dir)
    fix_figure_paths(slug_dir)
    validate_review_format(slug_dir)

    # Convert to HTML
    convert_to_html(slug)
    html_path = os.path.join(slug_dir, "index.html")
    if not os.path.exists(html_path) or os.path.getsize(html_path) < 200:
        return "fail", "html_conversion_failed"

    return "ok", ""


def process_paper(item, slug, cp):
    """Process a single paper with up to MAX_RETRIES auto-retries on failure."""
    if slug in cp["completed"]:
        return "skipped"

    slug_dir = os.path.join(PAPERS_DIR, slug)
    os.makedirs(slug_dir, exist_ok=True)

    # Clean existing files — but SKIP if paper belongs to other topics too
    if paper_has_other_topics(slug):
        log(f"  {slug}: belongs to multiple topics, skipping file deletion")
    else:
        for fname in ["review.md", "index.html", "text.md"]:
            fpath = os.path.join(slug_dir, fname)
            if os.path.exists(fpath):
                os.remove(fpath)
        fig_dir = os.path.join(slug_dir, "figures")
        if os.path.isdir(fig_dir):
            shutil.rmtree(fig_dir)

    # Find PDF
    pdf_path, match_method = find_pdf(item)
    if not pdf_path:
        log(f"  {slug}: no PDF found (method={match_method})")
        with _cp_lock:
            cp["failed"].append({"slug": slug, "reason": f"no_pdf:{match_method}"})
        save_checkpoint(cp)
        return "no_pdf"
    # Record Zotero item key → slug mapping for index persistence (Phase 1
    # PDF integrity field). Keyed across threads via _cp_lock for safety.
    with _cp_lock:
        _slug_to_zotero_key[slug] = item.get("key", "")
    if match_method == "fuzzy":
        log(f"  {slug}: PDF matched via FUZZY — review required")

    # Try up to MAX_RETRIES times
    last_reason = ""
    for attempt in range(1, MAX_RETRIES + 1):
        status, reason = _do_process(item, slug, slug_dir, pdf_path)
        if status == "ok":
            with _cp_lock:
                cp["completed"].append(slug)
            save_checkpoint(cp)
            if attempt > 1:
                log(f"  {slug}: succeeded on attempt {attempt}")
            return "ok"
        last_reason = reason
        log(f"  {slug}: attempt {attempt}/{MAX_RETRIES} failed ({reason})")
        if attempt < MAX_RETRIES:
            time.sleep(2)

    # All retries exhausted
    log(f"  {slug}: FAILED after {MAX_RETRIES} attempts ({last_reason})")
    with _cp_lock:
        cp["failed"].append({"slug": slug, "reason": last_reason})
    save_checkpoint(cp)
    return last_reason


# ── Main ──

# ── Phase 2: 3-axis mode mapping ─────────────────────────────────────────────
# MECE modes replace the 8-recipe legacy grid. Each --mode implies a specific
# combination of --resume/--skip-existing/--timeline/--category. When --mode
# is not used, the legacy flags behave exactly as before (backward compatible).
_MODE_LEGACY_MAP = {
    "curate":     {"resume": True,  "skip_existing": True,  "timeline": False, "category": False},
    "rebuild":    {"resume": False, "skip_existing": False, "timeline": False, "category": False},
    "reclassify": {"resume": True,  "skip_existing": True,  "timeline": False, "category": True},
    "retime":     {"resume": True,  "skip_existing": True,  "timeline": True,  "category": False},
}


def _apply_mode_mapping(args):
    """Translate --mode into legacy flag values.

    When args.mode is None (default), this is a no-op and existing callers keep
    working unchanged. When --mode is set, any conflicting legacy flag that was
    *explicitly* provided earns a DeprecationWarning, and the mode wins.
    """
    if args.mode is None:
        return  # legacy-only invocation, nothing to do

    target = _MODE_LEGACY_MAP[args.mode]
    # Detect explicit legacy flags that diverge from the mode's target
    overridden = []
    for field, expected in target.items():
        current = getattr(args, field)
        if current and not expected:
            overridden.append(f"--{field.replace('_', '-')}")
    if overridden:
        print(f"[deprecated] --mode {args.mode} overrides legacy flags: "
              f"{', '.join(overridden)} (these will be ignored)",
              file=sys.stderr)

    # Apply the mapping
    for field, value in target.items():
        setattr(args, field, value)
    print(f"[mode] {args.mode} → resume={args.resume}, skip_existing={args.skip_existing}, "
          f"timeline={args.timeline}, category={args.category}")


def main():
    parser = argparse.ArgumentParser(description="Paper-curation --update-force batch")
    parser.add_argument("--topic", default="ai4s", help="Topic: ai4s or scisci")
    parser.add_argument("--concurrency", type=int, default=16, help="Parallel workers (Tier 4 default; lower for Tier 1~3 — see README)")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip papers that already have review.md (for --update mode)")
    parser.add_argument("--limit", type=int, default=0, help="Limit papers (0=all)")
    parser.add_argument("--timeline", action="store_true",
                        help="Regenerate timeline images (with --resume: changed cats only, alone: all cats)")
    parser.add_argument("--category", action="store_true",
                        help="Re-run topic_modeling to reclassify all papers. Auto-enables --timeline for changed categories.")
    parser.add_argument("--strict-pdf", action="store_true",
                        help="Disable fuzzy PDF matching — skip papers without Zotero/DOI/arXiv link.")
    parser.add_argument("--slugs", default="",
                        help="Comma-separated slug prefixes (e.g. '088,1093'). Only these papers are (re)processed. "
                             "Implies force-rebuild of the listed slugs regardless of checkpoint.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print which papers would be processed and exit without writing.")
    parser.add_argument("--skip-dedup", action="store_true",
                        help="Skip the Zotero duplicate preflight (saves ~1-5 min; not recommended).")
    parser.add_argument("--dedup-execute", action="store_true",
                        help="Let the Zotero dedup preflight actually delete duplicates. "
                             "Default is dry-run (report only).")
    # ── Phase 2: 3-axis mode (new, MECE). When --mode is set, it overrides the
    # legacy flag combinations and emits DeprecationWarnings for any legacy
    # flags that were also specified. Omitting --mode keeps 100% legacy
    # behavior, so existing callers (incl. in-flight batches) are unaffected.
    parser.add_argument("--mode", choices=["curate", "rebuild", "reclassify", "retime"],
                        default=None,
                        help="New MECE mode selector. curate=new papers only (keeps existing reviews); "
                             "rebuild=regenerate all reviews; reclassify=re-run topic modeling on existing reviews; "
                             "retime=regenerate timeline narratives+images only. "
                             "When set, overrides --resume/--skip-existing/--timeline/--category combinations.")
    args = parser.parse_args()

    # Apply --mode → legacy flags mapping. Pure translation; no behavior change
    # when --mode is absent (args.mode is None → all legacy flags honored as-is).
    _apply_mode_mapping(args)

    # Propagate strict-pdf flag to find_pdf()
    global _STRICT_PDF
    _STRICT_PDF = args.strict_pdf
    if _STRICT_PDF:
        print("[strict-pdf] fuzzy PDF matching disabled — papers without authoritative PDF links will be skipped")

    # ── Rebuild safety: snapshot _papers_index.json so an accidental wipe
    # is reversible. Only triggered when --mode rebuild AND not --slugs (mass).
    if args.mode == "rebuild" and not args.slugs and not args.dry_run:
        idx_path = os.path.join(PAPERS_DIR, "_papers_index.json")
        if os.path.exists(idx_path):
            backup_path = os.path.join(PAPERS_DIR, "_papers_index.backup.json")
            try:
                shutil.copy2(idx_path, backup_path)
                print(f"[rebuild-safety] snapshot saved: {backup_path}")
            except Exception as _e:
                print(f"[rebuild-safety] snapshot FAILED: {_e}")

    # ── Preflight: Zotero dedup ────────────────────────────────────────────
    # Runs in ALL modes (full/local/update). Users may accidentally double-
    # register the same paper in Zotero via the UI or imports; running this
    # every time keeps the collection clean before we spend compute on reviews.
    # Default is dry-run → a report is written to {topic}/_dedup_zotero_report.json;
    # pass --dedup-execute once trust is built and you want auto-deletion.
    # `--slugs` and `--dry-run` modes skip the preflight because they are
    # targeted operations that should not touch the collection as a whole.
    if not args.skip_dedup and not args.slugs and not args.dry_run:
        dedup_script = os.path.join(os.path.dirname(__file__), "dedup_zotero.py")
        if os.path.exists(dedup_script):
            print(f"\n[preflight] Zotero dedup ({'EXECUTE' if args.dedup_execute else 'dry-run'}) for topic={args.topic}")
            dedup_cmd = [sys.executable, dedup_script, "--topic", args.topic]
            if args.dedup_execute:
                dedup_cmd.append("--execute")
            rc = subprocess.call(dedup_cmd)
            if rc != 0:
                print(f"[preflight] dedup exited {rc} — continuing anyway")

    collection_key = COLLECTIONS.get(args.topic, "")
    if not collection_key:
        print(f"Unknown topic: {args.topic}")
        return

    # Load checkpoint
    if args.resume:
        cp = load_checkpoint()
        # Clear failed list so they get retried
        prev_failed = len(cp.get("failed", []))
        cp["failed"] = []
        previously_completed = set(cp.get("completed", []))
        log(f"Resuming: {len(cp['completed'])} completed, {prev_failed} previously failed (will retry)")
    else:
        cp = {"completed": [], "failed": [], "phase": "init"}
        previously_completed = set()

    # Fetch items
    log(f"Fetching Zotero collection '{args.topic}' ({collection_key})...")
    items = fetch_zotero_items(collection_key)
    log(f"Total papers: {len(items)}")

    # Get existing slugs
    existing_slugs = sorted(d for d in os.listdir(PAPERS_DIR)
                            if os.path.isdir(os.path.join(PAPERS_DIR, d)) and d[0].isdigit())

    # Map items to slugs
    item_slug_pairs = []
    for item in items:
        slug = make_slug(item, existing_slugs)
        item_slug_pairs.append((item, slug))
        if slug not in existing_slugs:
            existing_slugs.append(slug)

    # --slugs filter: restrict processing to listed slug prefixes, and force-rebuild them
    if args.slugs:
        wanted_prefixes = [s.strip() for s in args.slugs.split(",") if s.strip()]
        before = len(item_slug_pairs)
        item_slug_pairs = [
            (it, slug) for (it, slug) in item_slug_pairs
            if any(slug.startswith(p) or slug == p for p in wanted_prefixes)
        ]
        log(f"--slugs: kept {len(item_slug_pairs)}/{before} papers matching {wanted_prefixes}")
        # Force rebuild: drop from checkpoint.completed so they are re-processed
        kept = {slug for _, slug in item_slug_pairs}
        cp["completed"] = [s for s in cp.get("completed", []) if s not in kept]
        save_checkpoint(cp)

    # Rebuild safety: preview PDF matching for first 5 papers so the
    # operator can spot fuzzy/wrong matches before the destructive run.
    if args.mode == "rebuild" and not args.slugs and not args.dry_run:
        print(f"\n[rebuild-preview] sampling 5 PDFs to verify matching before "
              f"processing {len(item_slug_pairs)} papers:")
        for it, slug in item_slug_pairs[:5]:
            try:
                _p, _m = find_pdf(it)
            except Exception as _e:
                _p, _m = None, f"err:{_e}"
            print(f"  {slug[:55]:55s} | method={_m} | path={_p or '(none)'}")
        print(f"[rebuild-preview] proceed if these look correct. "
              f"Ctrl-C now to abort.\n")

    if args.dry_run:
        print(f"[dry-run] would process {len(item_slug_pairs)} papers:")
        for _, slug in item_slug_pairs[:50]:
            print(f"  {slug}")
        if len(item_slug_pairs) > 50:
            print(f"  ... +{len(item_slug_pairs) - 50} more")
        return

    # Skip papers with existing review.md (--skip-existing or --resume).
    # When --slugs is used the listed papers must be force-rebuilt, so they
    # are intentionally excluded from this "already done" shortcut.
    forced_slugs = set()
    if args.slugs:
        forced_slugs = {slug for _, slug in item_slug_pairs}
    if args.skip_existing or args.resume:
        skipped = 0
        for item, slug in item_slug_pairs:
            if slug in forced_slugs:
                continue
            review_path = os.path.join(PAPERS_DIR, slug, "review.md")
            if os.path.exists(review_path) and os.path.getsize(review_path) >= 200:
                if slug not in cp["completed"]:
                    cp["completed"].append(slug)
                    skipped += 1
        save_checkpoint(cp)
        log(f"--skip-existing: {skipped} papers with existing review.md marked as completed")

    # Filter already completed
    remaining = [(item, slug) for item, slug in item_slug_pairs
                 if slug not in cp["completed"]]

    if args.limit > 0:
        remaining = remaining[:args.limit]

    log(f"To process: {len(remaining)} (completed: {len(cp['completed'])}, failed: {len(cp['failed'])})")
    log(f"Concurrency: {args.concurrency}")
    log(f"Estimated time: ~{len(remaining) * 5 / args.concurrency / 60:.1f} hours")

    # Process with thread pool
    start_time = time.time()
    done = 0

    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = {}
        for item, slug in remaining:
            future = executor.submit(process_paper, item, slug, cp)
            futures[future] = slug

        for future in as_completed(futures):
            slug = futures[future]
            try:
                result = future.result()
                done += 1
                elapsed = time.time() - start_time
                rate = elapsed / done if done else 0
                eta = rate * (len(remaining) - done) / 3600
                log(f"[{done}/{len(remaining)}] {slug}: {result} (ETA: {eta:.1f}h)")
            except Exception as e:
                log(f"[{done}/{len(remaining)}] {slug}: ERROR {e}")
                with _cp_lock:
                    cp["failed"].append({"slug": slug, "reason": str(e)})
                save_checkpoint(cp)

    elapsed_total = (time.time() - start_time) / 3600
    log(f"\nPass 1 done! {done} papers in {elapsed_total:.1f}h")
    log(f"Completed: {len(cp['completed'])}, Failed: {len(cp['failed'])}")

    # Note: per-paper auto-retry (MAX_RETRIES=3) is built into process_paper.
    # No separate retry pass needed.

    log(f"\nFinal: {len(cp['completed'])} completed, {len(cp['failed'])} failed")

    # ── Persist Zotero item key → slug mapping into _papers_index.json ──
    # build_papers_index will preserve `zotero_item_key` via prev.get(...).
    if _slug_to_zotero_key:
        try:
            from lib.atomic_io import atomic_write_json
            idx_path = os.path.join(PAPERS_DIR, "_papers_index.json")
            if os.path.exists(idx_path):
                with open(idx_path, "r", encoding="utf-8") as f:
                    _idx = json.load(f)
                _patched = 0
                for _e in _idx:
                    _k = _slug_to_zotero_key.get(_e.get("slug"))
                    if _k and _e.get("zotero_item_key") != _k:
                        _e["zotero_item_key"] = _k
                        _patched += 1
                if _patched:
                    atomic_write_json(idx_path, _idx)
                    log(f"  [zotero_item_key] persisted {_patched} mappings into _papers_index.json")
        except Exception as _e:
            log(f"  [zotero_item_key] persist failed: {_e}")

    # ── Post-processing: rebuild index, classify, insights, topic page ──
    if len(cp['completed']) > 0 or args.timeline or args.category:
        log("\n" + "=" * 60)
        log("POST-PROCESSING: index → classify → summaries → insights → HTML → topic index")
        log("=" * 60)

        topic = args.topic
        is_update = args.resume  # --resume implies update mode
        do_reclassify = args.category  # --category forces topic_modeling
        do_timeline_images = args.timeline or args.category  # --category auto-enables timeline

        # Identify newly processed slugs (for update mode)
        newly_completed = set(cp.get("completed", [])) - previously_completed

        def run_step(step_name, cmd, step_timeout=600):
            log(f"  [{step_name}] ...")
            try:
                result = subprocess.run(
                    cmd, cwd=str(PIPELINE_DIR.parent),
                    capture_output=True, text=True, timeout=step_timeout,
                    env={**os.environ, "PYTHONUTF8": "1"},
                )
                if result.returncode != 0:
                    log(f"  [{step_name}] FAILED (exit {result.returncode})")
                    # Dump full stderr + stdout to disk so the real traceback
                    # (often >200 chars) survives for diagnosis.
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_step = re.sub(r'[^A-Za-z0-9_-]+', '_', step_name)[:50]
                    dump_path = PIPELINE_DIR / "_logs" / f"step_failure_{safe_step}_{ts}.log"
                    try:
                        dump_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(dump_path, "w", encoding="utf-8") as f:
                            f.write(f"=== command ===\n")
                            f.write(" ".join(str(c) for c in cmd) + "\n")
                            f.write(f"\n=== exit code: {result.returncode} ===\n")
                            f.write(f"\n=== STDERR ({len(result.stderr or '')} chars) ===\n")
                            f.write(result.stderr or "(empty)\n")
                            f.write(f"\n=== STDOUT ({len(result.stdout or '')} chars) ===\n")
                            f.write(result.stdout or "(empty)\n")
                        log(f"    [diag] full output dumped: {dump_path}")
                    except Exception as _dump_e:
                        log(f"    [diag] dump failed: {_dump_e}")
                    # Console: last 30 lines of stderr (not first 200 chars) —
                    # tracebacks are most useful at the tail.
                    if result.stderr:
                        last = result.stderr.rstrip().splitlines()[-30:]
                        for ln in last:
                            log(f"    {ln}")
                else:
                    out_lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
                    if out_lines:
                        log(f"  [{step_name}] OK: {out_lines[-1][:100]}")
                    else:
                        log(f"  [{step_name}] OK")
            except subprocess.TimeoutExpired:
                log(f"  [{step_name}] TIMEOUT ({step_timeout}s)")
            except Exception as e:
                log(f"  [{step_name}] ERROR: {str(e)[:100]}")

        # Step 1: Always rebuild index
        run_step("build_papers_index",
                 ["python", "pipeline/build_papers_index.py", "--topic", topic])

        # Step 2: topic_modeling
        # --category: always run (reclassify all)
        # --resume without --category: skip (keep existing categories)
        # full mode: always run
        old_cats_by_slug = {}
        if do_reclassify:
            # Snapshot current classifications before reclassification
            try:
                idx_path = os.path.join(PAPERS_DIR, "_papers_index.json")
                with open(idx_path, "r", encoding="utf-8") as f:
                    idx = json.load(f)
                for p in idx:
                    cls = p.get("classifications", {}).get(topic, {})
                    old_cats_by_slug[p["slug"]] = set(cls.get("all_categories", []))
            except Exception:
                pass
            run_step("topic_modeling",
                     [TOPIC_MODELING_PYTHON, "pipeline/topic_modeling.py", "--topic", topic], 1200)
        elif is_update:
            run_step("topic_modeling (coords+connections)",
                     [TOPIC_MODELING_PYTHON, "pipeline/topic_modeling.py", "--topic", topic, "--skip-classification"], 1200)
        else:
            run_step("topic_modeling",
                     [TOPIC_MODELING_PYTHON, "pipeline/topic_modeling.py", "--topic", topic], 1200)

        # Step 3: classify (always — new papers only in update mode without --category)
        run_step("classify_papers",
                 [TOPIC_MODELING_PYTHON, "pipeline/classify_papers.py", "--topic", topic], 600)

        # Step 4: Determine changed categories
        changed_cats = []
        if do_reclassify:
            # Compare before/after classifications to find changed categories
            try:
                idx_path = os.path.join(PAPERS_DIR, "_papers_index.json")
                with open(idx_path, "r", encoding="utf-8") as f:
                    idx = json.load(f)
                cat_set = set()
                for p in idx:
                    if topic not in p.get("topics", []):
                        continue
                    slug = p["slug"]
                    cls = p.get("classifications", {}).get(topic, {})
                    new_cats = set(cls.get("all_categories", []))
                    old_cats = old_cats_by_slug.get(slug, set())
                    # Categories that gained or lost this paper
                    diff = new_cats.symmetric_difference(old_cats)
                    cat_set.update(diff)
                    cat_set.update(new_cats)  # also include current cats of moved papers
                changed_cats = sorted(cat_set) if cat_set else []
                if changed_cats:
                    log(f"  [changed_categories] {len(changed_cats)} categories changed after reclassification")
                    for c in changed_cats:
                        log(f"    - {c}")
                else:
                    log("  [changed_categories] No category changes detected — full regeneration")
            except Exception as e:
                log(f"  [changed_categories] ERROR comparing: {e} — full regeneration")
                changed_cats = []
        elif is_update and newly_completed:
            try:
                idx_path = os.path.join(PAPERS_DIR, "_papers_index.json")
                with open(idx_path, "r", encoding="utf-8") as f:
                    idx = json.load(f)
                cat_set = set()
                for p in idx:
                    if p.get("slug") in newly_completed:
                        cls = p.get("classifications", {}).get(topic, {})
                        for c in cls.get("all_categories", []):
                            cat_set.add(c)
                        pc = cls.get("primary_category", "")
                        if pc:
                            cat_set.add(pc)
                changed_cats = sorted(cat_set)
                log(f"  [changed_categories] {len(changed_cats)} categories affected by {len(newly_completed)} new papers")
                for c in changed_cats:
                    log(f"    - {c}")
            except Exception as e:
                log(f"  [changed_categories] ERROR reading index: {e}")
                changed_cats = []

        # Step 5-6: summaries, insights, timelines — scoped by changed categories
        if do_reclassify and changed_cats:
            # --category: full reclassification → rebuild ALL summaries/insights (old cats must be purged)
            # Only timelines are scoped to changed categories
            run_step("build_category_summaries",
                     ["python", "pipeline/build_category_summaries.py", "--topic", topic], 1200)
            run_step("extract_insights",
                     ["python", "pipeline/extract_insights.py", "--topic", topic], 1800)
            cats_arg = ["--categories"] + changed_cats
            run_step("generate_timelines",
                     ["python", "pipeline/generate_timelines.py", "--topic", topic] + cats_arg, 21600)
        elif do_reclassify:
            # --category but no diff detected: full regeneration
            run_step("build_category_summaries",
                     ["python", "pipeline/build_category_summaries.py", "--topic", topic], 1200)
            run_step("extract_insights",
                     ["python", "pipeline/extract_insights.py", "--topic", topic], 1800)
            run_step("generate_timelines",
                     ["python", "pipeline/generate_timelines.py", "--topic", topic], 21600)
        elif is_update:
            if changed_cats:
                cats_arg = ["--categories"] + changed_cats
                run_step("build_category_summaries",
                         ["python", "pipeline/build_category_summaries.py", "--topic", topic] + cats_arg, 1200)
                run_step("extract_insights",
                         ["python", "pipeline/extract_insights.py", "--topic", topic] + cats_arg, 1800)

                # Split by image presence:
                #   - cats_with_image: narrative-only (unless --timeline explicitly requested)
                #   - cats_missing_image: always full generation (new/renamed categories MUST get images)
                cats_with_image, cats_missing_image = _split_cats_by_image_presence(topic, changed_cats)
                if cats_missing_image:
                    log(f"  [generate_timelines] {len(cats_missing_image)} categories missing timeline image — will generate:")
                    for c in cats_missing_image:
                        log(f"    - {c}")
                if do_timeline_images:
                    # --timeline: full generation for all changed cats
                    run_step("generate_timelines",
                             ["python", "pipeline/generate_timelines.py", "--topic", topic] + cats_arg, 21600)
                else:
                    # Auto: narrative-only for cats with existing images
                    if cats_with_image:
                        run_step("generate_timelines (narrative)",
                                 ["python", "pipeline/generate_timelines.py", "--topic", topic,
                                  "--categories"] + cats_with_image + ["--narrative-only"], 21600)
                    # Auto: full generation for new/renamed cats without images
                    if cats_missing_image:
                        run_step("generate_timelines (images)",
                                 ["python", "pipeline/generate_timelines.py", "--topic", topic,
                                  "--categories"] + cats_missing_image, 21600)
            else:
                log("  [summaries/insights/timelines] SKIP (no new papers classified)")
        elif do_timeline_images:
            # --timeline alone (no --resume): full regeneration of all narratives + images
            run_step("build_category_summaries",
                     ["python", "pipeline/build_category_summaries.py", "--topic", topic], 1200)
            run_step("extract_insights",
                     ["python", "pipeline/extract_insights.py", "--topic", topic], 1800)
            run_step("generate_timelines",
                     ["python", "pipeline/generate_timelines.py", "--topic", topic], 21600)
        else:
            # Full mode (no --resume, no --timeline)
            run_step("build_category_summaries",
                     ["python", "pipeline/build_category_summaries.py", "--topic", topic], 1200)
            run_step("extract_insights",
                     ["python", "pipeline/extract_insights.py", "--topic", topic], 1800)
            run_step("generate_timelines",
                     ["python", "pipeline/generate_timelines.py", "--topic", topic], 21600)

        # Step 7-10: Always run (fast steps)
        run_step("inject_frontmatter",
                 ["python", "pipeline/inject_frontmatter.py", "--topic", topic], 600)
        run_step("generate_moc",
                 ["python", "pipeline/generate_moc.py", "--topic", topic], 600)
        run_step("generate_network",
                 ["python", "pipeline/generate_network.py", "--topic", topic], 600)

        # Verify UMAP coordinate coverage before deploy
        try:
            topic_dir = str(get_topic_dir(topic))
            umap_path = os.path.join(topic_dir, "_umap_coords.json")
            idx_path = os.path.join(PAPERS_DIR, "_papers_index.json")
            with open(idx_path, "r", encoding="utf-8") as f:
                all_idx = json.load(f)
            topic_slugs = {p["slug"] for p in all_idx if topic in p.get("topics", [])}
            umap_slugs = set()
            if os.path.exists(umap_path):
                with open(umap_path, "r", encoding="utf-8") as f:
                    umap_slugs = set(json.load(f).keys())
            missing = topic_slugs - umap_slugs
            if missing:
                log(f"\n  [verify_umap] {len(missing)} papers missing UMAP coordinates — re-running topic_modeling...")
                run_step("topic_modeling (umap fix)",
                         [TOPIC_MODELING_PYTHON, "pipeline/topic_modeling.py", "--topic", topic, "--skip-connections"], 1200)
                run_step("generate_network (rebuild)",
                         ["python", "pipeline/generate_network.py", "--topic", topic], 600)
            else:
                log(f"  [verify_umap] OK: all {len(topic_slugs)} papers have coordinates")
        except Exception as e:
            log(f"  [verify_umap] WARNING: verification failed ({str(e)[:100]})")

        run_step("review_to_html",
                 ["python", "pipeline/review_to_html.py", "--all"], 600)
        run_step("build_topic_index",
                 ["python", "pipeline/build_topic_index.py", topic], 600)

        # Deep Research search index (section-aware chunks + OpenAI embeddings).
        # Reads OPENAI_API_KEY from env or config.json; fails fast if missing.
        # Cleanup stale category narratives/timelines before building the
        # search index so Deep Research never surfaces renamed categories.
        # Always runs --execute because post-processing has just rewritten
        # the classifier output; any orphan entries are safe to remove.
        run_step("cleanup",
                 ["python", "pipeline/cleanup.py", "--execute"], 300)

        run_step("build_search_index",
                 ["python", "pipeline/build_search_index.py", "--topic", topic], 900)

        # Deploy via wrangler (Cloudflare Workers with Static Assets) +
        # idempotent gh-pages stub sync. Requires:
        #   CLOUDFLARE_API_TOKEN (or CF_API_TOKEN), CLOUDFLARE_ACCOUNT_ID.
        has_cf_token = bool(
            os.environ.get("CLOUDFLARE_API_TOKEN") or os.environ.get("CF_API_TOKEN")
        )
        has_account_id = bool(os.environ.get("CLOUDFLARE_ACCOUNT_ID"))
        if has_cf_token and has_account_id:
            log("\n  [prepare_deploy] Cloudflare env vars found, deploying...")
            try:
                result = subprocess.run(
                    ["python", "pipeline/prepare_deploy.py", "--topic", topic, "--push"],
                    cwd=str(PIPELINE_DIR.parent),
                    capture_output=True, text=True, timeout=1800,
                    env={**os.environ, "PYTHONUTF8": "1"},
                )
                if result.returncode == 0:
                    log(f"  [prepare_deploy] OK: wrangler deploy + gh-pages sync done")
                else:
                    log(f"  [prepare_deploy] FAILED (exit {result.returncode})")
                    if result.stderr:
                        log(f"    {result.stderr[:500]}")
            except Exception as e:
                log(f"  [prepare_deploy] ERROR: {str(e)[:100]}")
        else:
            missing = []
            if not has_cf_token:
                missing.append("CLOUDFLARE_API_TOKEN (or CF_API_TOKEN)")
            if not has_account_id:
                missing.append("CLOUDFLARE_ACCOUNT_ID")
            log(f"\n  [prepare_deploy] SKIP: missing env vars — {', '.join(missing)}")

        log("\nPost-processing complete!")


if __name__ == "__main__":
    main()
