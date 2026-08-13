"""
Unified topic index builder for paper-curation.
Reads reviews from papers/ central repo, generates {topic}/index.html.

Usage: PYTHONUTF8=1 python build_topic_index.py <topic>
  e.g. PYTHONUTF8=1 python build_topic_index.py my-topic
       PYTHONUTF8=1 python build_topic_index.py another-topic
"""
import json, os, re, sys
from html import escape
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from paper_curation.rendering import load_text_asset
from paper_curation.rendering.models import paper_href
from paper_curation.rendering.topic_page.view_model import build_topic_page_view_model

KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST).strftime("%Y-%m-%d")

from collections import OrderedDict
from config_loader import (
    PAPERS_DIR as _PAPERS_DIR, DOCS_DIR, get_operator_attribution,
    get_public_base_url, get_topic_dir, get_topic_profile,
    get_zotero_api_key, get_zotero_user_id,
)
from lib.categories import category_slug
from lib.audio_overview import (
    get_audio_css as _audio_css,
    audio_modal_html as _audio_modal,
    audio_script_block as _audio_script,
)
PAPERS_DIR = str(_PAPERS_DIR)

from lib import license_util as _lic


def _is_deploy_topic(topic):
    """True unless the topic is excluded from Cloudflare via docs/.assetsignore."""
    docs = os.path.dirname(PAPERS_DIR)
    try:
        for raw in open(os.path.join(docs, ".assetsignore"), encoding="utf-8"):
            s = raw.strip().rstrip("/")
            if s and not s.startswith("#") and "/" not in s and s == topic:
                return False
    except Exception:
        pass
    return True

def get_topic():
    from config_loader import resolve_topic
    return resolve_topic(sys.argv[1] if len(sys.argv) > 1 else "",
                         script="build_topic_index")


def _run_topic_index(topic=None, cross=None):
    """Build {topic}/index.html (cards + Deep Research UI).

    Phase 5 refactor: module-level code was wrapped into this
    function so the script is importable without side-effects.
    Pass ``topic`` explicitly; falls back to ``sys.argv[1]``.
    """
    TOPIC = topic if topic is not None else get_topic()
    TOPIC_DIR = str(get_topic_dir(TOPIC))

    # Theme colors per topic (title from config.json Zotero collection name)
    from config_loader import load_config
    _collections_raw = load_config().get("zotero", {}).get("collections", {})

    _default_theme = {
        "gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
        "accent": "#3B82F6", "accent_dark": "#2563EB", "accent_light": "#60A5FA",
    }
    profile = get_topic_profile(TOPIC)
    theme = dict(_default_theme)
    for key in ("gradient", "accent", "accent_dark", "accent_light"):
        if profile.get(key):
            theme[key] = str(profile[key])
    _collection_name = _collections_raw.get(TOPIC, TOPIC)
    theme["title"] = str(profile.get("title") or _collection_name)
    theme["subtitle_prefix"] = str(
        profile.get("subtitle_prefix") or theme["title"])
    if cross:
        theme = {
            "gradient": "linear-gradient(135deg, #1a0d2a 0%, #3a1a5c 50%, #6b21a8 100%)",
            "accent": "#8B3FD6", "accent_dark": "#6B21A8", "accent_light": "#B57BF0",
        }
        theme["title"] = cross.get("title", "통합 Deep Research")
        theme["subtitle_prefix"] = theme["title"]

    # Load data
    with open(os.path.join(PAPERS_DIR, "_papers_index.json"), encoding="utf-8") as f:
        papers_index = json.load(f)

    cls_path = os.path.join(TOPIC_DIR, "_new_classification.json")
    narr_path = os.path.join(TOPIC_DIR, "_timeline_narrative.json")

    if os.path.exists(cls_path):
        with open(cls_path, encoding="utf-8") as f:
            cls_data = json.load(f)
        categories = cls_data.get("categories", [])
        assignments = cls_data.get("assignments", [])
    else:
        # Fallback: extract categories from classifications[TOPIC] in _papers_index.json
        _cat_names = set()
        for p in papers_index:
            cls = p.get("classifications", {}).get(TOPIC, {})
            for c in cls.get("all_categories", []):
                _cat_names.add(c)
            if cls.get("primary_category"):
                _cat_names.add(cls["primary_category"])
        categories = [{"name": c} for c in sorted(_cat_names)] if _cat_names else []
        assignments = []

    if os.path.exists(narr_path):
        with open(narr_path, encoding="utf-8") as f:
            narrative = json.load(f)
        category_analyses = narrative.get("category_analyses", {})
        executive_summary = narrative.get("executive_summary_ko", "")
    else:
        category_analyses = {}
        executive_summary = ""

    # Load insights
    insights_path = os.path.join(TOPIC_DIR, "_insights.json")
    if os.path.exists(insights_path):
        with open(insights_path, encoding="utf-8") as f:
            insights_data = json.load(f)
    else:
        insights_data = {}

    # Merge _category_summaries.json (has description + papers per category)
    cat_sum_path = os.path.join(TOPIC_DIR, "_category_summaries.json")
    if os.path.exists(cat_sum_path):
        with open(cat_sum_path, encoding="utf-8") as f:
            cat_summaries = json.load(f)
        for cs in cat_summaries:
            cat_name_cs = cs.get("category", "")
            if cat_name_cs not in category_analyses:
                category_analyses[cat_name_cs] = {}
            if cs.get("description"):
                category_analyses[cat_name_cs]["description"] = cs["description"]
            if cs.get("description_ko"):
                category_analyses[cat_name_cs]["description_ko"] = cs["description_ko"]
            if cs.get("sub_themes_ko"):
                category_analyses[cat_name_cs]["sub_themes_ko"] = cs["sub_themes_ko"]
            if cs.get("papers"):
                category_analyses[cat_name_cs]["papers"] = cs["papers"]
            # sub_themes from _category_summaries.json always wins (has description_ko)
            if cs.get("sub_themes"):
                category_analyses[cat_name_cs]["sub_themes"] = cs["sub_themes"]

    # Filter papers for this topic
    if cross:
        topic_papers = []
    else:
        topic_papers = [p for p in papers_index if TOPIC in p.get("topics", [])]
    slug_to_index = {p["slug"]: p for p in topic_papers}

    # Assignment slug → category mapping (multi-class)
    # Priority: 1) classifications[TOPIC] in papers_index, 2) _new_classification.json assignments
    slug_to_cat = {}       # slug → primary_category (str)
    slug_to_all_cats = {}  # slug → all_categories (list)

    # From _new_classification.json (legacy, lower priority)
    for a in assignments:
        slug_to_cat[a["slug"]] = a.get("primary_category", "Other")
        slug_to_all_cats[a["slug"]] = a.get("all_categories", [a.get("primary_category", "Other")])

    # From classifications[TOPIC] in papers_index (higher priority, overrides)
    for p in topic_papers:
        cls = p.get("classifications", {}).get(TOPIC, {})
        if cls.get("primary_category"):
            slug_to_cat[p["slug"]] = cls["primary_category"]
            slug_to_all_cats[p["slug"]] = cls.get("all_categories", [cls["primary_category"]])

    # Available paper directories in papers/
    actual_dirs = sorted(
        d for d in os.listdir(PAPERS_DIR)
        if os.path.isdir(os.path.join(PAPERS_DIR, d)) and len(d) >= 3 and d[:3].isdigit()
    )

    def find_dir_for_slug(slug):
        if slug in actual_dirs:
            return slug
        for d in actual_dirs:
            if d.startswith(slug[:35]):
                return d
        num = slug.split("_")[0] if "_" in slug else slug[:4]
        candidates = [d for d in actual_dirs if d.startswith(num + "_")]
        if len(candidates) == 1:
            return candidates[0]
        return None

    def parse_review_md(slug):
        dir_name = find_dir_for_slug(slug)
        if not dir_name:
            return {}, None
        md_path = os.path.join(PAPERS_DIR, dir_name, "review.md")
        if not os.path.exists(md_path):
            return {}, dir_name
        with open(md_path, encoding="utf-8") as f:
            text = f.read()
        result = {}
        m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
        if m: result["title"] = m.group(1).strip()
        hm = re.search(r"^>\s*\*\*저자\*\*:\s*(.+)", text, re.MULTILINE)
        if hm:
            hl = hm.group(1)
            result["authors"] = hl.split("|")[0].strip()
            dm = re.search(r"\*\*날짜\*\*:\s*([^\|]+)", hl)
            if dm: result["date"] = dm.group(1).strip()
            jm = re.search(r"\*\*Journal\*\*:\s*([^\|]+)", hl)
            if jm: result["journal"] = jm.group(1).strip()
            doi_m = re.search(r"\*\*DOI\*\*:\s*([^\|]+)", hl)
            if doi_m: result["doi"] = doi_m.group(1).strip()
            ax_m = re.search(r"\*\*arXiv\*\*:\s*([^\|]+)", hl)
            if ax_m: result["arxiv"] = ax_m.group(1).strip()
        em = re.search(r"## (?:Essence|한줄 요약)[^\n]*\s*\n+([\s\S]+?)(?=\n## |\Z)", text)
        if em: result["essence"] = em.group(1).strip()
        # Parse scores from table format OR list format
        for label, key in [("Novelty", "novelty"), ("Technical Soundness", "technical_soundness"),
                            ("Significance", "significance"), ("Clarity", "clarity"), ("Overall", "overall_score")]:
            # Table: | Label | X/5 |
            sm = re.search(rf"\|\s*{label}\s*\|\s*(\d+(?:\.\d+)?)\s*/\s*5\s*\|", text)
            if not sm:
                # List: - Label: X/5
                sm = re.search(rf"-\s*{label}\s*:\s*(\d+(?:\.\d+)?)\s*/\s*5", text)
            if sm:
                val = float(sm.group(1))
                if key == "overall_score":
                    result[key] = val
                else:
                    result[key] = int(val)
        vm = re.search(r"\*\*총평\*\*:\s*([\s\S]+?)(?=\n##|\Z)", text)
        if vm: result["verdict"] = vm.group(1).strip()
        return result, dir_name

    from lib.dateutil import normalize_date

    # Build category → papers mapping
    cat_order = [c["name"] for c in categories] if categories else ["Other"]
    cat_papers = defaultdict(list)
    unmatched = []

    for p_idx in topic_papers:
        slug = p_idx["slug"]
        p_cls = p_idx.get("classifications", {}).get(TOPIC, {})
        all_cats = slug_to_all_cats.get(slug, p_cls.get("all_categories", [p_cls.get("primary_category", "Other")]))
        if not all_cats:
            all_cats = [slug_to_cat.get(slug, "Other")]
        review, dir_name = parse_review_md(slug)
        if dir_name is None:
            unmatched.append(slug)
            continue
        title = review.get("title") or p_idx.get("title", slug)
        authors = review.get("authors", "")
        raw_date = review.get("date") or str(p_idx.get("date", ""))
        date_fmt = normalize_date(raw_date)
        journal = review.get("journal", "")
        doi = review.get("doi") or p_idx.get("doi", "")
        arxiv = review.get("arxiv", "")
        essence = review.get("essence") or p_idx.get("essence", "")
        overall_score = review.get("overall_score") or p_idx.get("score") or 0
        has_fig = (os.path.exists(os.path.join(PAPERS_DIR, dir_name, "figures", "fig1.webp"))
                   or os.path.exists(os.path.join(PAPERS_DIR, dir_name, "figures", "fig1.png")))
        # Extract fig1 caption from pdffigures2 JSON or review.md
        fig_caption = ""
        pf2_dir = os.path.join(PAPERS_DIR, dir_name, "figures", "pdffigures2")
        pf2_json = None
        if os.path.isdir(pf2_dir):
            pf2_jsons = [f for f in os.listdir(pf2_dir) if f.endswith(".json")]
            if pf2_jsons:
                pf2_json = os.path.join(pf2_dir, pf2_jsons[0])
        if pf2_json and pf2_json.endswith(".json"):
            try:
                with open(pf2_json, "r", encoding="utf-8") as _f:
                    figs_meta = json.load(_f)
                if figs_meta and isinstance(figs_meta, list):
                    fig_caption = figs_meta[0].get("caption", "")
            except Exception as e:
                print(f"WARNING: pdffigures2 parse failed for {dir_name}: {e}")
        if not fig_caption:
            # Fallback: extract from review.md (line after ![Figure 1])
            md_path = os.path.join(PAPERS_DIR, dir_name, "review.md")
            if os.path.exists(md_path):
                with open(md_path, "r", encoding="utf-8") as _f:
                    md_text = _f.read()
                cap_m = re.search(r'!\[.*?\]\(figures/fig1.*?\)\s*\n+\*(.+?)\*', md_text)
                if cap_m:
                    fig_caption = cap_m.group(1).strip()
        paper_data = {
            "dir": dir_name, "slug": slug, "title": title, "authors": authors,
            "date": date_fmt, "journal": journal, "doi": doi, "arxiv": arxiv,
            "essence": essence, "overall_score": float(overall_score) if overall_score else 0,
            "novelty": review.get("novelty"), "technical_soundness": review.get("technical_soundness"),
            "significance": review.get("significance"), "clarity": review.get("clarity"),
            "verdict": review.get("verdict", ""),
            "has_fig": has_fig,
            "fig_src": (f"../papers/{dir_name}/figures/fig1.webp" if os.path.exists(os.path.join(PAPERS_DIR, dir_name, "figures", "fig1.webp"))
                        else f"../papers/{dir_name}/figures/fig1.png") if has_fig else None,
            "fig_caption": fig_caption,
            "license": p_idx.get("license", ""),
        }
        # Multi-class: add to ALL matching categories, with per-category sub_category
        sub_categories_map = p_cls.get("sub_categories", {})
        for cat in all_cats:
            if cat in cat_order or cat == "Other":
                card = dict(paper_data)
                card["sub_category"] = sub_categories_map.get(cat, p_cls.get("sub_category", "General") if cat == p_cls.get("primary_category") else "General")
                cat_papers[cat].append(card)

    if unmatched:
        print(f"WARNING unmatched: {unmatched}")
    # Enforce the package renderer boundary on the actual production cards.
    build_topic_page_view_model(
        TOPIC,
        (
            {**card, "category": category}
            for category, cards in cat_papers.items()
            for card in cards
        ),
        ({"name": category} for category in cat_order),
    )
    for cat in cat_papers:
        cat_papers[cat].sort(key=lambda p: p["overall_score"], reverse=True)
    total_cards = sum(len(v) for v in cat_papers.values())
    unique_papers = len(topic_papers)
    if cross:
        unique_papers = cross.get("paper_count", unique_papers)
    print(f"Total papers for {TOPIC}: {unique_papers} unique ({total_cards} cards with multi-class)")
    for cn in cat_order:
        print(f"  {cn}: {len(cat_papers.get(cn, []))}")

    # --- HTML Rendering ---

    def esc(s):
        return escape(str(s)) if s else ""

    operator_attribution = esc(get_operator_attribution())
    operator_attribution = (
        f"<br>{operator_attribution}"
        if operator_attribution else ""
    )

    def make_doi_link(doi, arxiv):
        if doi:
            # Skip invalid/empty values
            if doi in ('N/A', '[', ''):
                pass  # fall through to arxiv
            # Parse markdown link: [text](url)
            elif doi.startswith('['):
                md_m = re.match(r'\[([^\]]*)\]\((https?://[^)]+)\)', doi)
                if md_m:
                    text, url = md_m.group(1), md_m.group(2)
                    label = text if text else url
                    return f'<a href="{esc(url)}" target="_blank">{esc(label)}</a>'
            elif doi.startswith("http"):
                return f'<a href="{esc(doi)}" target="_blank">{esc(doi)}</a>'
            elif re.match(r'10\.\d{4,}/', doi):
                return f'<a href="https://doi.org/{esc(doi)}" target="_blank">{esc(doi)}</a>'
            else:
                return esc(doi)
        if arxiv:
            aid = arxiv.strip()
            if aid.startswith("http"):
                arxiv_id = aid.rsplit('/', 1)[-1]
                return f'<a href="{esc(aid)}" target="_blank">arXiv:{esc(arxiv_id)}</a>'
            return f'<a href="https://arxiv.org/abs/{esc(aid)}" target="_blank">arXiv:{esc(aid)}</a>'
        return ""

    # 게이팅은 배포 사본(PC_PUBLIC_BUILD=1)에서만 — 로컬 렌더는 항상 full
    _is_deploy = _is_deploy_topic(topic) and os.environ.get("PC_PUBLIC_BUILD") == "1"
    _fig_strict = os.environ.get("PC_FIGURE_POLICY", "") == "strict"
    _nd_suppress = os.environ.get("PC_ND_POLICY", "suppress") != "show"
    def render_paper_card(paper, num, cat_slug):
        score = paper["overall_score"]
        score_disp = f"{int(score)}/5" if score and score > 0 else "N/A"
        score_val = score if score else 0
        meta_parts = []
        if paper["authors"]: meta_parts.append(f'<strong>\uc800\uc790</strong>: {esc(paper["authors"])}')
        if paper["date"]: meta_parts.append(f'<strong>\ub0a0\uc9dc</strong>: {esc(paper["date"])}')
        if paper["journal"]: meta_parts.append(f'<strong>Journal</strong>: {esc(paper["journal"])}')
        dl = make_doi_link(paper["doi"], paper["arxiv"])
        if dl: meta_parts.append(f'<strong>DOI</strong>: {dl}')
        _cls = _lic.normalize(paper.get("license", ""))
        meta_parts.append(f'<strong>License</strong>: {esc(_lic.label(_cls))}')
        meta_html = " | ".join(meta_parts)
        badges = []
        for label, key in [("Novelty", "novelty"), ("Technical Soundness", "technical_soundness"),
                            ("Significance", "significance"), ("Clarity", "clarity")]:
            val = paper.get(key)
            if val is not None: badges.append(f'<span class="score-badge">{label}: {val}</span>')
        if score and score > 0: badges.append(f'<span class="score-badge">Overall: {int(score)}</span>')
        badges_html = " ".join(badges)
        _nd_public = _is_deploy and _lic.is_nd(_cls) and _nd_suppress
        fig_html = ""
        if paper["has_fig"]:
            cap = paper.get("fig_caption", "")
            cap_html = f'<p class="fig-caption">{esc(cap)}</p>' if cap else ""
            if _is_deploy and not _lic.figure_public_ok(_cls, strict=_fig_strict):
                fig_html = (
                    '\n          <div class="paper-fig">'
                    '<div class="fig-gated" style="padding:0.8rem;color:#999;font-size:0.8rem;">'
                    '&#128274; 원문 도표는 라이선스상 재현하지 않습니다</div>'
                    f'{cap_html}</div>'
                )
            else:
                fig_html = (
                    '\n          <div class="paper-fig">'
                    f'<img data-src="{esc(paper["fig_src"])}" alt="Figure" class="lazy">'
                    f'{cap_html}</div>'
                )
        essence_html = ""
        eval_html = ""
        if _nd_public:
            essence_html = (
                '\n          <div class="section">'
                '\n            <p style="color:#8a2a20;font-size:0.85rem;">'
                '&#128274; 변경금지(ND) 라이선스 — 2차적 저작물(AI 리뷰)의 공개가 제한됩니다. 원문을 확인하세요.</p>'
                '\n          </div>'
            )
        else:
            if paper["essence"]:
                essence_html = (
                    '\n          <div class="section">'
                    '\n            <div class="section-label">Essence</div>'
                    f'\n            <p>{esc(paper["essence"])}</p>'
                    '\n          </div>'
                )
            if badges or paper["verdict"]:
                inner = ""
                if badges_html: inner += f'<div class="scores">{badges_html}</div>\n            '
                if paper["verdict"]: inner += f'<p class="verdict">{esc(paper["verdict"])}</p>'
                eval_html = (
                    '\n          <div class="section">'
                    '\n            <div class="section-label">Evaluation</div>'
                    f'\n            {inner}'
                    '\n          </div>'
                )
        # Link to ../papers/{slug}/index.html
        link_href = paper_href(paper["dir"]).href
        return (
            f'        <div class="paper-card" data-date="{esc(paper["date"])}"'
            f' data-score="{score_val}" data-topic="{esc(cat_slug)}">\n'
            f'          <div class="paper-header">\n'
            f'            <span class="paper-num">#{num}</span>\n'
            f'            <span class="paper-date">{esc(paper["date"])}</span>\n'
            f'            <span class="paper-score">{score_disp}</span>\n'
            f'          </div>\n'
            f'          <h3><a href="{link_href}">{esc(paper["title"])}</a></h3>\n'
            f'          <p class="meta">{meta_html}</p>'
            f'{fig_html}{essence_html}{eval_html}\n'
            f'        </div>'
        )

    def _match_papers_to_subtheme(st_name, st_desc, papers):
        """Match papers to a sub-theme by keyword overlap in title."""
        keywords = set((st_name + " " + st_desc).lower().split())
        scored = []
        for p in papers:
            title_words = set(p.get("title", "").lower().split())
            overlap = len(keywords & title_words)
            if overlap >= 2:
                scored.append((overlap, p))
        scored.sort(key=lambda x: (-x[0], -x[1].get("score", 0)))
        return [s[1] for s in scored[:4]]  # max 4 papers per sub-theme


    def validate_description(text, cat_name, sub_name=""):
        """카테고리/sub-category 설명 품질 검증."""
        issues = []
        label = f"{cat_name}/{sub_name}" if sub_name else cat_name

        if not text or len(text) < 50:
            issues.append(f"{label}: 설명 누락 또는 너무 짧음 ({len(text or '')}자)")
        elif len(text) < 150:
            issues.append(f"{label}: 설명 부실 ({len(text)}자, 최소 150자 권장)")

        if text:
            # [NNN] 리터럴 체크
            if "[NNN]" in text:
                issues.append(f"{label}: [NNN] 리터럴 남아있음")
            # 논문 제목 인라인 체크 (영문 20자 이상 따옴표)
            quoted = re.findall(r"['\"][A-Z][^'\"]{20,}['\"]", text)
            if quoted:
                issues.append(f"{label}: 논문 제목 인라인 ({quoted[0][:40]}...)")
            # 한국어 비율 체크
            korean = len(re.findall(r'[\uac00-\ud7af]', text))
            if korean < len(text) * 0.3:
                issues.append(f"{label}: 한국어 비율 낮음 ({korean}/{len(text)})")
            # 마침표 종료
            if text.strip() and text.strip()[-1] not in ".다":
                issues.append(f"{label}: 마침표로 끝나지 않음 ('{text.strip()[-5:]}')")

        return issues


    def render_category_narrative(cat_name):
        ca = category_analyses.get(cat_name, {})
        if not ca: return ""
        overview = ca.get("description", "")
        sub_themes = ca.get("sub_themes", [])
        cat_papers = ca.get("papers", [])
        html_parts = []

        # Build slug number → paper info lookup. Prefer the CURRENT topic's
        # papers so a collision number (same slug number reused across
        # ingestion batches / merged repos) resolves to the paper that belongs
        # to THIS topic; fall back to the global map for numbers absent here.
        num_to_paper = {}
        for p in papers_index:                       # global fallback (legacy last-wins)
            slug = p.get("slug", "")
            title = p.get("title", "")
            num = slug.split("_")[0] if "_" in slug else slug[:3]
            num_to_paper[num] = (slug, title)
        for p in topic_papers:                        # topic-scoped overrides win
            slug = p.get("slug", "")
            title = p.get("title", "")
            num = slug.split("_")[0] if "_" in slug else slug[:3]
            num_to_paper[num] = (slug, title)
        # Category-primary override (highest precedence): resolves a SAME-topic
        # collision number to the paper whose PRIMARY category is the one being
        # rendered — the overview text of this category describes that paper.
        for p in topic_papers:
            cls = p.get("classifications", {}).get(TOPIC, {})
            pc = cls.get("primary_category") or slug_to_cat.get(p.get("slug", ""))
            if pc == cat_name:
                slug = p.get("slug", "")
                title = p.get("title", "")
                num = slug.split("_")[0] if "_" in slug else slug[:3]
                num_to_paper[num] = (slug, title)

        def _refs_to_links(text_html):
            """Convert [NNN] markers to <a> links."""
            def _repl(m):
                num = m.group(1)
                if num in num_to_paper:
                    slug, title = num_to_paper[num]
                    return f'<a href="../papers/{esc(slug)}/index.html" title="{esc(title)}">[{num}]</a>'
                # Try zero-padded: "87" → "087", "9" → "009"
                padded = num.zfill(3)
                if padded in num_to_paper:
                    slug, title = num_to_paper[padded]
                    return f'<a href="../papers/{esc(slug)}/index.html" title="{esc(title)}">[{num}]</a>'
                return m.group(0)
            return re.sub(r'\[(\d+)\]', _repl, text_html)

        # Category Overview (한글 우선)
        overview_ko = ca.get("description_ko", "")
        if overview_ko:
            overview_html = _refs_to_links(esc(overview_ko))
            html_parts.append(f'<h4>Category Overview</h4>\n<p>{overview_html}</p>')
        elif overview:
            html_parts.append(f'<h4>Category Overview</h4>\n<p>{esc(overview)}</p>')

        # Sub-category bullets — description_ko directly from sub_themes
        if sub_themes:
            html_parts.append('<ul class="subcategory-list">')
            for st in sub_themes:
                name = st.get("name", "")
                desc = st.get("description_ko", "") or st.get("description", "")
                if not name or not desc:
                    continue
                # Convert [NNN] markers to hyperlinks
                desc_html = _refs_to_links(esc(desc))
                html_parts.append(
                    f'<li><strong>{esc(name)}</strong>: {desc_html}</li>'
                )
            html_parts.append('</ul>')

        return "\n".join(html_parts)

    def render_exec_summary(text):
        if not text:
            return ""
        paras = [p.strip() for p in text.split("\n\n") if p.strip()]

        def _render_para(paragraph):
            safe = esc(paragraph)
            return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe)

        return "\n    ".join(f"<p>{_render_para(p)}</p>" for p in paras)

    # CSS with theme
    accent = theme["accent"]
    accent_dark = theme["accent_dark"]
    accent_light = theme["accent_light"]
    gradient = theme["gradient"]

    CSS = f"""* {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'KoPub Dotum', 'KoPubDotumMedium', -apple-system, 'Noto Sans KR', sans-serif; background: #f0f2f5; color: #333; line-height: 1.6; }}
    .container {{ max-width: 960px; margin: 0 auto; padding: 2rem 1.5rem; }}
    .hero {{ background: {gradient}; color: white; padding: 3rem 2rem; border-radius: 16px; margin-bottom: 2rem; }}
    .hero h1 {{ font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem; }}
    .hero .subtitle {{ opacity: 0.85; font-size: 1rem; }}
    .hero .stats {{ margin-top: 1rem; display: flex; gap: 2rem; }}
    .hero .stat {{ text-align: center; }}
    .hero .stat-num {{ font-size: 2rem; font-weight: 700; color: {accent_light}; }}
    .hero .stat-label {{ font-size: 0.8rem; opacity: 0.7; }}
    .paper-card {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-left: 4px solid {accent}; transition: transform 0.15s, box-shadow 0.15s; }}
    .paper-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }}
    .paper-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }}
    .paper-num {{ font-size: 0.85rem; color: #888; font-weight: 600; }}
    .paper-score {{ background: {accent}; color: white; padding: 0.2rem 0.7rem; border-radius: 20px; font-weight: 700; font-size: 0.9rem; }}
    .paper-card h3 {{ font-size: 1.05rem; color: #1a1a2e; margin-bottom: 0.3rem; }}
    .paper-card h3 a {{ color: #1a1a2e; text-decoration: none; }}
    .paper-card h3 a:hover {{ color: {accent}; }}
    .meta {{ font-size: 0.8rem; color: #888; margin-bottom: 0.8rem; }}
    .section {{ margin-top: 0.8rem; }}
    .section-label {{ font-weight: 700; font-size: 0.85rem; color: {accent}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem; border-bottom: 1px solid #e8edf3; padding-bottom: 0.2rem; }}
    .section p {{ font-size: 0.92rem; color: #444; }}
    .scores {{ display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.4rem; }}
    .score-badge {{ background: #e8edf3; color: {accent_dark}; padding: 0.15rem 0.6rem; border-radius: 12px; font-size: 0.78rem; font-weight: 600; }}
    .verdict {{ font-style: normal; color: #444; font-size: 0.9rem; }}
    .paper-fig {{ margin: 0.8rem 0; text-align: center; }}
    .paper-fig img {{ max-width: min(100%, 600px); border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }}
    .paper-fig .fig-caption {{ font-size: 0.78rem; color: #888; margin-top: 0.3rem; font-style: italic; line-height: 1.4; }}
    .excluded {{ background: #fff3cd; border-radius: 12px; padding: 1.2rem; margin-top: 1.5rem; }}
    .excluded h3 {{ color: #856404; font-size: 1rem; margin-bottom: 0.5rem; }}
    .excluded li {{ font-size: 0.85rem; color: #856404; margin: 0.3rem 0; }}
    .credit {{ text-align: center; font-size: 0.8rem; color: #aaa; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e0e0e0; }}
    .sort-bar {{ display: flex; gap: 0.5rem; margin-bottom: 1.2rem; flex-wrap: wrap; }}
    .sort-btn {{ background: white; border: 1px solid {accent}; color: {accent}; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; cursor: pointer; font-weight: 600; }}
    .sort-btn:hover, .sort-btn.active {{ background: {accent}; color: white; }}
    .timeline-section {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
    .timeline-section h2 {{ color: {accent_dark}; font-size: 1.1rem; margin-bottom: 1rem; }}
    .timeline-summary {{ font-size: 0.9rem; color: #444; line-height: 1.6; }}
    .timeline-summary p {{ margin: 0.5rem 0; }}
    .topic-group {{ margin-bottom: 1rem; }}
    .topic-header {{ background: #f5f5f5; border-radius: 12px; padding: 0.8rem 1.2rem; cursor: pointer; display: flex; align-items: center; gap: 0.8rem; border-left: 4px solid #999; user-select: none; transition: background 0.15s; }}
    .topic-header:hover {{ background: #ebebeb; }}
    .topic-name {{ font-weight: 700; font-size: 1rem; flex: 1; color: #444; }}
    .topic-count {{ font-size: 0.8rem; color: #888; background: #e0e0e0; padding: 0.15rem 0.5rem; border-radius: 10px; }}
    .topic-toggle {{ font-size: 0.8rem; color: #999; transition: transform 0.2s; }}
    .topic-body {{ padding: 0.5rem 0 0 0; }}
    .topic-body.collapsed {{ display: none; }}
    .category-timeline {{ margin: 0.5rem 0 1rem; text-align: center; }}
    .category-timeline img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
    .category-summary {{ background: white; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.06); font-size: 0.9rem; line-height: 1.7; color: #444; }}
    .sub-group {{ margin: 0.5rem 0; }}
    .sub-header {{ background: #fafafa; border-radius: 8px; padding: 0.5rem 1rem; cursor: pointer; display: flex; align-items: center; gap: 0.6rem; border-left: 3px solid {accent_light}; user-select: none; transition: background 0.15s; }}
    .sub-header:hover {{ background: #f0f0f0; }}
    .sub-name {{ font-weight: 600; font-size: 0.9rem; flex: 1; color: #555; }}
    .sub-count {{ font-size: 0.75rem; color: #999; background: #e8e8e8; padding: 0.1rem 0.4rem; border-radius: 8px; }}
    .sub-toggle {{ font-size: 0.7rem; color: #bbb; transition: transform 0.2s; }}
    .sub-body {{ padding: 0 0 0 0.5rem; }}
    .sub-body.collapsed {{ display: none; }}
    .category-summary p {{ margin: 0.6rem 0; }}
    .category-summary h4 {{ font-size: 0.95rem; color: {accent_dark}; margin: 0 0 0.4rem; }}
    .category-summary .subcategory-list {{ margin: 0.6rem 0 0.2rem 1.2rem; padding: 0; }}
    .category-summary .subcategory-list li {{ margin: 0.5rem 0; line-height: 1.6; }}
    .category-summary a {{ color: #2563EB; text-decoration: none; font-weight: 500; }}
    .category-summary a:hover {{ text-decoration: underline; }}
    .paper-date {{ font-size: 0.75rem; color: #999; }}
    img.lazy {{ opacity: 0; transition: opacity 0.3s; }}
    img.lazy.loaded {{ opacity: 1; }}
    .search-box {{ background: white; border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 1.2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
    .search-box input {{ width: 100%; padding: 0.6rem 1rem; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 0.95rem; font-family: inherit; outline: none; transition: border-color 0.2s; }}
    .search-box input:focus {{ border-color: {accent}; }}
    .search-box .search-hint {{ font-size: 0.75rem; color: #aaa; margin-top: 0.3rem; }}
    .search-box .search-count {{ font-size: 0.8rem; color: {accent}; font-weight: 600; margin-top: 0.3rem; display: none; }}
    .lightbox {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 9999; cursor: zoom-out; align-items: center; justify-content: center; }}
    .lightbox.active {{ display: flex; }}
    .lightbox img {{ max-width: 95%; max-height: 95%; object-fit: contain; border-radius: 8px; }}
    .paper-fig img, .category-timeline img, .timeline-section img {{ cursor: zoom-in; }}
    .insights-section {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
    .insights-section h2 {{ color: {accent_dark}; font-size: 1.1rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}
    .insights-header {{ cursor: pointer; user-select: none; margin-bottom: 0 !important; }}
    .insights-header.open {{ margin-bottom: 1rem !important; }}
    .insights-body.collapsed {{ display: none; }}
    .insights-section .insight-count {{ font-size: 0.8rem; color: #888; font-weight: 400; }}
    .insight-card {{ border-left: 4px solid #999; border-radius: 0 8px 8px 0; padding: 1rem 1.2rem; margin-bottom: 0.8rem; background: #fafafa; }}
    .insight-card.convergence {{ border-left-color: #7C3AED; background: #FAF5FF; }}
    .insight-card.gap {{ border-left-color: #F59E0B; background: #FFFBEB; }}
    .insight-card.emerging {{ border-left-color: #10B981; background: #F0FDF4; }}
    .insight-card.declining {{ border-left-color: #9CA3AF; background: #F9FAFB; }}
    .insight-type {{ font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem; }}
    .convergence .insight-type {{ color: #7C3AED; }}
    .gap .insight-type {{ color: #D97706; }}
    .emerging .insight-type {{ color: #059669; }}
    .declining .insight-type {{ color: #6B7280; }}
    .insight-title {{ font-size: 1rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.4rem; }}
    .insight-desc {{ font-size: 0.9rem; color: #444; line-height: 1.6; margin-bottom: 0.5rem; }}
    .insight-meta {{ font-size: 0.8rem; color: #888; display: flex; flex-wrap: wrap; gap: 0.8rem; }}
    .insight-meta .cats {{ color: {accent}; }}
    .insight-meta .evidence a {{ color: #2563EB; text-decoration: none; font-weight: 500; }}
    .insight-meta .evidence a:hover {{ text-decoration: underline; }}
    .insight-policy {{ font-size: 0.85rem; color: #4B5563; margin-top: 0.4rem; padding: 0.4rem 0.6rem; background: rgba(0,0,0,0.03); border-radius: 4px; }}
    .cat-insight {{ background: #f8f9fa; border-radius: 8px; padding: 0.8rem 1rem; margin-top: 0.8rem; font-size: 0.88rem; line-height: 1.6; }}
    .cat-insight .ci-label {{ font-weight: 600; color: {accent_dark}; margin-right: 0.3rem; }}
    .cat-insight .ci-gap {{ color: #D97706; }}
    .cat-insight .ci-policy {{ color: #4B5563; }}
    /* ============ Deep Research ============ */
    .search-row {{ display: flex; gap: 0.5rem; align-items: stretch; }}
    .search-row input {{ flex: 1; }}
    .mode-toggle {{ display: flex; gap: 0; border: 2px solid #e0e0e0; border-radius: 8px; overflow: hidden; flex-shrink: 0; }}
    .mode-btn {{ background: white; border: none; padding: 0.5rem 0.9rem; font-size: 0.85rem; cursor: pointer; color: #888; transition: all 0.15s; font-family: inherit; }}
    .mode-btn.active {{ background: {accent}; color: white; }}
    .mode-btn:hover:not(.active) {{ background: #f5f5f5; color: {accent_dark}; }}
    .deep-panel {{ margin-top: 1rem; background: #fcfcfd; border: 1px solid #e5e5e5; border-radius: 10px; overflow: hidden; }}
    .deep-header {{ display: flex; align-items: center; gap: 0.8rem; padding: 0.7rem 1.1rem; background: linear-gradient(135deg, {accent}12, transparent); border-bottom: 1px solid #eee; flex-wrap: wrap; }}
    .deep-header h3 {{ font-size: 0.95rem; color: {accent_dark}; margin: 0; flex-shrink: 0; font-weight: 700; }}
    .deep-model {{ padding: 0.35rem 0.55rem; border: 1px solid #ddd; border-radius: 6px; font-size: 0.78rem; background: white; cursor: pointer; font-family: inherit; color: #444; }}
    .deep-actions {{ margin-left: auto; display: flex; gap: 0.35rem; flex-wrap: wrap; }}
    .deep-btn {{ background: white; border: 1px solid #ddd; border-radius: 6px; padding: 0.32rem 0.7rem; font-size: 0.76rem; cursor: pointer; color: #555; transition: all 0.15s; font-family: inherit; }}
    .deep-btn:hover:not(:disabled) {{ background: {accent}; color: white; border-color: {accent}; }}
    .deep-btn:disabled {{ opacity: 0.4; cursor: not-allowed; }}
    .deep-stop-btn {{ background: #fef3f2; border-color: #f0c2bd; color: #b33a3a; font-weight: 700; }}
    .deep-stop-btn:hover:not(:disabled) {{ background: #b33a3a; color: white; border-color: #b33a3a; }}
    .deep-status {{ padding: 0.55rem 1.1rem; font-size: 0.82rem; color: #555; background: #f7f9fb; border-bottom: 1px solid #eee; display: none; }}
    .deep-status.active {{ display: block; }}
    .deep-status.error {{ color: #b33a3a; background: #fef3f2; border-bottom-color: #fadcd9; }}
    .deep-plan {{ padding: 0.6rem 1.1rem; background: #f9fafb; border-bottom: 1px solid #eee; display: none; }}
    .deep-plan.active {{ display: block; }}
    .deep-plan-title {{ font-size: 0.78rem; font-weight: 700; color: {accent_dark}; margin-bottom: 0.35rem; }}
    .deep-sec-title {{ margin-top: 0.7rem; padding-top: 0.5rem; border-top: 1px dashed #e2e2e2; }}
    .deep-plan-list {{ margin: 0 0 0 1.3rem; font-size: 0.8rem; color: #555; line-height: 1.6; }}
    .deep-plan-list li {{ margin: 0.15rem 0; }}
    .deep-plan-list li .rstat {{ color: #aaa; font-size: 0.73rem; margin-left: 0.45rem; }}
    .deep-plan-list li.done .rstat {{ color: {accent}; font-weight: 600; }}
    .deep-plan-list li.deep-sec-hdr {{ list-style: none; margin: 0.5rem 0 0.2rem -0.7rem; font-weight: 700; color: {accent_dark}; font-size: 0.76rem; }}
    .deep-deeper-lbl {{ display: inline-flex; align-items: center; gap: 0.3rem; font-size: 0.78rem; color: #444; cursor: pointer; user-select: none; white-space: nowrap; }}
    .deep-deeper-lbl input {{ cursor: pointer; }}
    .deep-deeper-note {{ font-size: 0.72rem; color: {accent}; font-weight: 600; }}
    .deep-body {{ padding: 1.2rem 1.5rem; display: none; }}
    .deep-body.active {{ display: block; }}
    .deep-answer {{ font-size: 0.94rem; line-height: 1.75; color: #262626; }}
    .deep-answer p {{ margin: 0.75rem 0; }}
    .deep-answer h1, .deep-answer h2, .deep-answer h3 {{ color: {accent_dark}; margin: 1.1rem 0 0.45rem; line-height: 1.3; }}
    .deep-answer h1 {{ font-size: 1.2rem; }}
    .deep-answer h2 {{ font-size: 1.05rem; }}
    .deep-answer h3 {{ font-size: 0.96rem; }}
    .deep-answer ul, .deep-answer ol {{ margin: 0.5rem 0 0.5rem 1.5rem; }}
    .deep-answer li {{ margin: 0.25rem 0; }}
    .deep-answer strong {{ color: #1a1a1a; }}
    .deep-answer a.ref {{ display: inline-block; color: {accent}; text-decoration: none; font-weight: 700; font-size: 0.72rem; padding: 0 0.32rem; border-radius: 3px; background: {accent}1a; margin: 0 0.12rem; vertical-align: super; line-height: 1.2; }}
    .deep-answer a.ref:hover {{ background: {accent}; color: white; }}
    .deep-answer figure {{ margin: 1rem 0; max-width: 100%; }}
    .deep-answer img {{ width: 100%; height: auto; display: block; margin: 1rem 0; padding: 0.5rem; background: #fafafa; border: 1px solid #eee; border-radius: 6px; box-sizing: border-box; cursor: zoom-in; }}
    .deep-answer figure img {{ margin: 0; }}
    .deep-answer figure figcaption {{ font-size: 0.78rem; color: #666; text-align: center; margin-top: 0.45rem; font-style: italic; }}
    .deep-answer p img {{ margin: 0.5rem 0; }}
    .deep-answer code {{ background: #f2f2f4; padding: 0.1rem 0.35rem; border-radius: 3px; font-size: 0.86em; font-family: ui-monospace, monospace; }}
    .deep-answer pre {{ background: #f6f8fa; padding: 0.7rem 0.9rem; border-radius: 6px; overflow-x: auto; }}
    .deep-refs {{ margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #eee; }}
    .deep-refs h4 {{ font-size: 0.88rem; color: {accent_dark}; margin-bottom: 0.55rem; }}
    .deep-refs ol {{ margin-left: 1.2rem; font-size: 0.82rem; color: #555; }}
    .deep-refs li {{ margin: 0.3rem 0; line-height: 1.55; }}
    .deep-refs a {{ color: {accent}; text-decoration: none; }}
    .deep-refs a:hover {{ text-decoration: underline; }}
    .deep-figures {{ margin-top: 1.4rem; padding-top: 1rem; border-top: 1px solid #eee; }}
    .deep-figures h4 {{ font-size: 0.88rem; color: {accent_dark}; margin-bottom: 0.6rem; }}
    .deep-figures-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 0.7rem; }}
    .deep-fig-item {{ background: #fafafa; border: 1px solid #eee; border-radius: 6px; overflow: hidden; }}
    .deep-fig-item a {{ text-decoration: none; color: inherit; display: block; }}
    .deep-fig-item img {{ width: 100%; height: 115px; object-fit: cover; cursor: zoom-in; display: block; }}
    .deep-fig-item .fig-cap {{ padding: 0.35rem 0.6rem; font-size: 0.7rem; color: #666; line-height: 1.35; }}"""

    # Audio Overview styles (shared lib). accent_bg ≈ accent at ~10% alpha.
    CSS = CSS + "\n" + _audio_css(accent, accent_dark, accent + "1a")
    if cross:
        CSS += (
            "\n/* cross-topic 통합 콘솔 (로컬 전용) */\n"
            ".sort-bar{display:none!important;}\n"
            ".mode-toggle{display:none!important;}\n"
            '.hero a[href="feed.xml"]{display:none!important;}\n'
            ".hero .stat:nth-child(2){display:none!important;}\n"
            ".cross-dir{background:#fff;border:1px solid #eee;border-radius:12px;padding:1.2rem 1.4rem;margin:0.5rem 0 0;}\n"
            ".cross-dir h2{font-size:1.05rem;margin-bottom:0.5rem;color:#6B21A8;}\n"
            ".cross-dir p{font-size:0.92rem;color:#444;line-height:1.7;}\n"
            ".cross-topics{display:flex;flex-wrap:wrap;gap:0.6rem;margin-top:0.9rem;}\n"
            "a.cross-topic{display:inline-flex;gap:0.45rem;align-items:center;padding:0.5rem 0.95rem;border:1px solid #e5e5e5;border-radius:999px;text-decoration:none;color:#333;font-size:0.9rem;}\n"
            "a.cross-topic:hover{background:#faf5ff;border-color:#B57BF0;}\n"
            "a.cross-topic strong{color:#6B21A8;}\n"
        )

    # Credentials are runtime-only BYOK values held in memory for one page load.
    JS = ("let _ANTHROPIC_KEY = '';\n"
          "let _OPENAI_KEY = '';\n"
          "let _LLM_KEY = '';\n"
          + ("window._PC_CROSS = " + ("true" if cross else "false") + ";\n")
          + load_text_asset())

    def render_insights_section():
        """_insights.json에서 cross-category insights 렌더링."""
        cross = insights_data.get("cross_category", [])
        if not cross:
            return ""

        # Build slug number → paper info lookup (topic-first; see _refs_to_links)
        num_to_paper = {}
        for p in papers_index:                       # global fallback
            slug = p.get("slug", "")
            title = p.get("title", "")
            num = slug.split("_")[0] if "_" in slug else slug[:3]
            num_to_paper[num] = (slug, title)
        for p in topic_papers:                        # topic-scoped overrides win
            slug = p.get("slug", "")
            title = p.get("title", "")
            num = slug.split("_")[0] if "_" in slug else slug[:3]
            num_to_paper[num] = (slug, title)

        type_labels = {
            "convergence": "융합",
            "gap": "연구 갭",
            "emerging": "신흥 트렌드",
            "declining": "감소 추세",
        }

        cards = []
        for ins in cross:
            itype = ins.get("type", "gap")
            label = type_labels.get(itype, itype)
            title = escape(ins.get("title", ""))
            desc = escape(ins.get("description", ""))
            cats = ins.get("categories", [])
            evidence = ins.get("evidence", [])
            policy = ins.get("policy_implication", "")

            cats_html = " · ".join(escape(c) for c in cats)
            ev_links = []
            for num in evidence:
                matched = num_to_paper.get(num) or num_to_paper.get(str(num).zfill(3))
                if matched:
                    slug, ptitle = matched
                    ev_links.append(
                        f'<a href="../papers/{escape(slug)}/index.html" title="{escape(ptitle)}">[{num}]</a>'
                    )
                else:
                    ev_links.append(f"[{num}]")
            ev_html = " ".join(ev_links)

            policy_html = ""
            if policy:
                policy_html = f'\n      <div class="insight-policy">&#x1F3DB; {escape(policy)}</div>'

            cards.append(
                f'    <div class="insight-card {itype}">\n'
                f'      <div class="insight-type">{label}</div>\n'
                f'      <div class="insight-title">{title}</div>\n'
                f'      <div class="insight-desc">{desc}</div>\n'
                f'      <div class="insight-meta">\n'
                f'        <span class="cats">{cats_html}</span>\n'
                f'        <span class="evidence">{ev_html}</span>\n'
                f'      </div>{policy_html}\n'
                f'    </div>'
            )

        # Collapsed by default — only the header shows; click to expand.
        return (
            '<div class="insights-section">\n'
            '  <h2 class="insights-header" onclick="toggleInsights()">'
            '<span class="topic-toggle" id="toggle-insights-body">&#x25B6;</span>'
            f' Research Insights <span class="insight-count">{len(cross)} findings</span></h2>\n'
            '  <div class="insights-body collapsed" id="insights-body">\n'
            + "\n".join(cards) + "\n"
            + '  </div>\n'
            + '</div>\n\n'
        )


    def render_category_insight(cat_name):
        """per_category insight를 카테고리 summary에 삽입할 HTML 반환."""
        per_cat = insights_data.get("per_category", {}).get(cat_name, {})
        if not per_cat:
            return ""
        parts = []
        kf = per_cat.get("key_finding", "")
        gap = per_cat.get("gap", "")
        pi = per_cat.get("policy_implication", "")
        if kf:
            parts.append(f'<span class="ci-label">&#x1F4CC; 핵심:</span> {escape(kf)}')
        if gap:
            parts.append(f'<span class="ci-label ci-gap">&#x26A0; 갭:</span> {escape(gap)}')
        if pi:
            parts.append(f'<span class="ci-label ci-policy">&#x1F3DB; 정책:</span> {escape(pi)}')
        if not parts:
            return ""
        return '<div class="cat-insight">' + "<br>".join(parts) + '</div>'


    # Build topic groups
    topic_groups_parts = []
    global_num = 1
    for cat_idx, cat_name in enumerate(cat_order):
        papers = cat_papers.get(cat_name, [])
        if not papers:
            continue
        topic_id = f"topic-{cat_idx}"
        cat_slug = category_slug(cat_name)
        narr_html = render_category_narrative(cat_name)

        # Category timeline image (in topic dir)
        cat_tl_file = f"category_timeline_{cat_slug}.png"
        cat_tl_exists = os.path.exists(os.path.join(TOPIC_DIR, cat_tl_file))
        cat_tl_html = ""
        if cat_tl_exists:
            cat_tl_html = (
                f'\n<div class="category-timeline">'
                f'<img data-src="{cat_tl_file}" alt="{esc(cat_name)} Timeline" class="lazy">'
                f'</div>'
            )

        cat_insight_html = render_category_insight(cat_name)
        summary_block = ""
        if narr_html or cat_tl_html or cat_insight_html:
            summary_block = f'\n<div class="category-summary">{cat_tl_html}{narr_html}{cat_insight_html}</div>'

        # Group papers by sub_category (if >30 papers in category)
        if len(papers) > 30:
            sub_groups = OrderedDict()
            for paper in papers:
                sc = paper.get("sub_category", "General")
                if sc not in sub_groups:
                    sub_groups[sc] = []
                sub_groups[sc].append(paper)

            # Merge small sub-categories (<3 papers) into "Others"
            small = [k for k, v in sub_groups.items() if len(v) < 3 and k != "Others"]
            if small:
                others = sub_groups.pop("Others", [])
                for k in small:
                    others.extend(sub_groups.pop(k))
                if others:
                    sub_groups["Others"] = others

            cards_html = ""
            for sc_idx, (sc_name, sc_papers) in enumerate(sub_groups.items()):
                sc_id = f"{topic_id}-sub-{sc_idx}"
                sc_cards = []
                for paper in sc_papers:
                    sc_cards.append(render_paper_card(paper, global_num, cat_slug))
                    global_num += 1
                cards_html += (
                    f'\n<div class="sub-group">'
                    f'\n  <div class="sub-header" onclick="toggleSub(\'{sc_id}\')">'
                    f'\n    <span class="sub-name">{esc(sc_name)}</span>'
                    f'\n    <span class="sub-count">{len(sc_papers)}</span>'
                    f'\n    <span class="sub-toggle" id="toggle-{sc_id}">&#x25B6;</span>'
                    f'\n  </div>'
                    f'\n  <div class="sub-body collapsed" id="{sc_id}">'
                    + "\n".join(sc_cards)
                    + '\n  </div>'
                    + '\n</div>'
                )
        else:
            cards_html = ""
            for paper in papers:
                cards_html += render_paper_card(paper, global_num, cat_slug)
                global_num += 1

        group = (
            f'<div class="topic-group" data-topic="{esc(cat_name)}">\n'
            f'      <div class="topic-header" onclick="toggleTopic(\'{topic_id}\')">\n'
            f'        <span class="topic-name">{esc(cat_name)}</span>\n'
            f'        <span class="topic-count">{len(papers)}\ud3b8</span>\n'
            f'        <span class="topic-toggle" id="toggle-{topic_id}">&#x25B6;</span>\n'
            f'      </div>\n'
            f'      <div class="topic-body collapsed" id="{topic_id}">{summary_block}\n'
            + cards_html + "\n"
            + '      </div>\n'
            + '    </div>'
        )
        topic_groups_parts.append(group)

    exec_html = render_exec_summary(executive_summary)
    num_cats = len([c for c in cat_order if cat_papers.get(c)])
    if cross:
        _tlinks = "".join(
            f'<a class="cross-topic" href="../{esc(t["slug"])}/index.html">'
            f'{esc(t.get("title", t["slug"]))} <strong>{int(t.get("papers", 0))}</strong></a>'
            for t in cross.get("topics", [])
        )
        topic_groups_parts = [
            '<div class="cross-dir">'
            '<h2>🧠 통합 Deep Research — 모든 토픽을 하나의 코퍼스로</h2>'
            f'<p>{unique_papers}편의 리뷰를 토픽 경계 없이 검색합니다. 위 검색창에서 '
            '<strong>🧠 Deep</strong> 을 누르고 질문하세요 — 연결 그래프를 넘나드는 '
            '<strong>Deeper</strong> 확장도 지원합니다. <em>(로컬 전용)</em></p>'
            '<div class="cross-topics">' + _tlinks + '</div>'
            '</div>'
        ]

    # Determine date range
    dates = [p.get("date", "") for cat in cat_papers.values() for p in cat]
    dates = [d for d in dates if d]
    date_range = f"{min(dates)} ~ {max(dates)}" if dates else ""

    # Research timeline
    has_research_tl = os.path.exists(os.path.join(TOPIC_DIR, "research_timeline.png"))
    research_tl_html = ""
    if has_research_tl:
        research_tl_html = (
            '<div class="timeline-section">\n'
            '  <h2>Research Timeline</h2>\n'
            '  <div style="text-align:center;margin:1rem 0">'
            '<img src="research_timeline.png" alt="Research Timeline"'
            ' style="max-width:100%;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1)">'
            '</div>\n'
        )
        if exec_html:
            research_tl_html += f'  <div class="timeline-summary">\n    {exec_html}\n  </div>\n'
        if os.path.exists(os.path.join(TOPIC_DIR, "network.html")):
            research_tl_html += f'  <div style="text-align:right;margin-top:0.8rem"><a href="network.html" target="_blank" rel="noopener noreferrer" style="color:{accent};font-weight:600;text-decoration:none;font-size:0.9rem">&#x1F517; Interactive Paper Network &rarr;</a></div>\n'
        research_tl_html += '</div>\n\n\n'

    # Deep Research Audio Overview: context provider built live from the answer.
    _AUDIO_PROVIDER_JS = (
        "window._audioContextProvider = function() {\n"
        "  return {\n"
        "    title: (DEEP.currentQuery || 'deep-research'),\n"
        "    review: '[질문]\\n' + (DEEP.currentQuery || '') + '\\n\\n[답변]\\n' + (DEEP.currentAnswer || ''),\n"
        "    connections: (DEEP.currentRefs || []).map(function(r) { return {title: r.title, relation: '인용', reason: ''}; })\n"
        "  };\n"
        "};"
    )

    public_base_url = get_public_base_url()
    og_meta = ""
    if public_base_url:
        topic_url = f"{public_base_url}/{TOPIC}/"
        og_meta = (
            f'<meta property="og:url" content="{esc(topic_url)}">\n'
            f'<meta property="og:image" content="{esc(topic_url)}research_timeline.png">\n'
        )

    HTML = (
        '<!DOCTYPE html>\n'
        '<html lang="ko">\n'
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
        f'<title>{esc(theme["title"])} &#8212; Paper Curation</title>\n'
        # OG 소셜 카드 — 토픽 링크 공유 시 타임라인 이미지가 카드로 뜬다
        # (research_timeline.png 는 배포 시 prepare_deploy 가 .webp 로 재작성).
        '<meta property="og:type" content="website">\n'
        '<meta property="og:site_name" content="Paper Curation">\n'
        f'<meta property="og:title" content="{esc(theme["title"])} — Paper Curation">\n'
        '<meta property="og:description" content="AI 논문 큐레이션 — 구조화 리뷰 · 연결 그래프 · 타임라인 · Deep Research">\n'
        f'{og_meta}'
        '<meta name="twitter:card" content="summary_large_image">\n'
        # Atom 피드 autodiscovery — RSS 리더가 feed.xml 을 자동 인식 (build_rss.py 생성)
        f'<link rel="alternate" type="application/atom+xml" title="{esc(theme["title"])} — Paper Curation" href="feed.xml">\n'
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/font-kopub/1.0/kopubdotum.css" integrity="sha384-a+6QFBwEmWYo4LaR7Ti/cfkRL9OEt6L85DKw3wkYLYxj+jlH56ipE4IdHWZ9+lOF" crossorigin="anonymous">\n'
        '<script>window.MathJax={tex:{inlineMath:[[\'$\',\'$\'],[\'\\\\(\',\'\\\\)\']],displayMath:[[\'$$\',\'$$\'],[\'\\\\[\',\'\\\\]\']]}};</script>\n'
        '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js" integrity="sha384-Wuix6BuhrWbjDBs24bXrjf4ZQ5aFeFWBuKkFekO2t8xFU0iNaLQfp2K6/1Nxveei" crossorigin="anonymous" async></script>\n'
        '<script src="https://cdn.jsdelivr.net/npm/marked@15.0.12/marked.min.js" integrity="sha384-948ahk4ZmxYVYOc+rxN1H2gM1EJ2Duhp7uHtZ4WSLkV4Vtx5MUqnV+l7u9B+jFv+" crossorigin="anonymous"></script>\n'
        f'<style>\n{CSS}\n</style>\n'
        '</head>\n'
        '<body>\n'
        '<div class="container">\n'
        '  <div class="hero">\n'
        f'    <h1>{esc(theme["title"])} &#8212; Paper Curation</h1>\n'
        '    <div class="ai-notice" style="margin:0.7rem 0 0.3rem;padding:0.55rem 0.9rem;background:#fff8e1;border:1px solid #ffe0a3;border-radius:8px;font-size:0.82rem;color:#7a5b00;line-height:1.55;">'
        '&#9888;&#65039; 이 사이트의 리뷰&middot;요약&middot;타임라인&middot;Deep Research 답변은 <strong>생성형 AI</strong>가 자동 생성한 결과물입니다. '
        '게재 논문은 arXiv&middot;OpenReview 등 공개 프리프린트이며, 원문 저작권은 <strong>원저작자</strong>에게 있습니다.'
        '</div>\n'
        '    <div class="stats">\n'
        f'      <div class="stat"><div class="stat-num">{unique_papers}</div><div class="stat-label">\ub9ac\ubdf0 \uc644\ub8cc</div></div>\n'
        f'      <div class="stat"><div class="stat-num">{num_cats}</div><div class="stat-label">MECE \uce74\ud14c\uace0\ub9ac</div></div>\n'
        f'      <div class="stat"><div class="stat-num">{TODAY}</div><div class="stat-label">\ud050\ub808\uc774\uc158 \uc77c\uc790</div></div>\n'
        '    </div>\n'
        # Atom \ud53c\ub4dc \ub9c1\ud06c \u2014 hero(\ub2e4\ud06c \uadf8\ub77c\ub514\uc5b8\ud2b8) \uc704\ub77c \ud770\uc0c9+opacity \ub85c \uc774\uc9c8\uac10 \uc5c6\uac8c
        '    <div style="margin-top:1rem;text-align:right"><a href="feed.xml" title="Atom \ud53c\ub4dc \uad6c\ub3c5 (RSS)" style="color:white;opacity:0.75;text-decoration:none;font-size:0.85rem;font-weight:600">&#x1F4E1; RSS</a></div>\n'
        '  </div>\n\n\n'
        + research_tl_html
        + render_insights_section()
        + '  <div class="search-box">\n'
        '    <div class="search-row">\n'
        '      <input type="text" id="search-input" placeholder="Search papers by title, DOI, keyword...">\n'
        '      <div class="mode-toggle">\n'
        '        <button class="mode-btn active" id="mode-classic" title="Substring search">Classic</button>\n'
        '        <button class="mode-btn" id="mode-deep" title="Deep Research (uses your API keys)">&#x1F9E0; Deep</button>\n'
        '      </div>\n'
        '    </div>\n'
        '    <div class="search-hint" id="search-hint">Enter title, DOI, author name, or keyword to filter</div>\n'
        '    <div class="search-count" id="search-count"></div>\n'
        '    <div id="deep-panel" class="deep-panel" style="display:none">\n'
        '      <div class="deep-header">\n'
        '        <h3>Deep Research</h3>\n'
        '        <select id="deep-length" class="deep-model" title="답변 분량">\n'
        '          <option value="short" selected>Short</option>\n'
        '          <option value="medium">Medium (2x)</option>\n'
        '          <option value="long">Long (5x)</option>\n'
        '        </select>\n'
        '        <select id="deep-model" class="deep-model" title="모델 등급. 키에 따라 Anthropic Sonnet/Opus, OpenAI GPT-4.1/GPT-5.5, Google Gemini 3.1 Flash-Lite/3.5 Flash 로 자동 매핑">\n'
        '          <option value="fast">Fast (cheap)</option>\n'
        '          <option value="smart">Smart (best)</option>\n'
        '        </select>\n'
        '        <label class="deep-deeper-lbl" title="체크 시: 답변 생성에 웹 검색을 허용합니다 — 관련 뉴스·빅테크 블로그·코퍼스 밖 최신 논문 참조. Anthropic/Gemini 키에서 동작 (OpenAI 키는 미지원). 검색 호출 비용이 소액 추가됩니다. 기본 OFF = 코퍼스 발췌만 사용.">\n'
        '          <input type="checkbox" id="deep-websearch"> &#x1F310; web\n'
        '        </label>\n'
        '        <label class="deep-deeper-lbl" title="체크 시: 핵심 논문의 연결 그래프(후속·반론·기반·응용)를 따라 확장하고, 단락별 에이전트가 작성한 뒤 오케스트레이터가 취합합니다. 분량 Long·최상위 모델이 자동 적용 (LLM 호출·시간·비용 증가).">\n'
        '          <input type="checkbox" id="deep-deeper"> Deeper\n'
        '        </label>\n'
        '        <span class="deep-deeper-note" id="deep-deeper-note"></span>\n'
        '        <button class="deep-btn deep-stop-btn" id="deep-stop" style="display:none" title="생성 중인 답변을 즉시 중단">&#x23F9;&#xFE0F; 중단</button>\n'
        '        <button class="deep-btn" id="deep-rerun" disabled title="현재 질의를 선택한 모델·분량으로 다시 실행">&#x21BB; 재시작</button>\n'
        '        <div class="deep-actions">\n'
        '          <button class="deep-btn" id="deep-copy" disabled title="Copy markdown">&#x1F4CB; Copy</button>\n'
        '          <button class="deep-btn" id="deep-download" disabled title="Download .md">&#x2B07; MARKDOWN</button>\n'
        '          <button class="deep-btn" id="deep-download-html" disabled title="Download .html">&#x2B07; HTML</button>\n'
        '          <button class="deep-btn" id="deep-newtab" disabled title="Open in new tab">&#x1F517; New tab</button>\n'
        '          <button class="deep-btn" id="deep-obsidian" disabled title="Save answer + your notes to Obsidian">&#x1F4DD; Obsidian</button>\n'
        '          <button class="deep-btn" id="deep-audio" disabled title="이 답변을 팟캐스트형 오디오로 생성 (Gemini · 키는 브라우저에만 저장)" onclick="openAudioModal()">&#x1F3A7; Audio</button>\n'
        '          <button class="deep-btn" id="deep-close" title="Close">&#x2715;</button>\n'
        '        </div>\n'
        '      </div>\n'
        '      <div class="deep-status" id="deep-status"></div>\n'
        '      <div class="deep-plan" id="deep-plan" style="display:none">\n'
        '        <div class="deep-plan-title">&#x1F5FA;&#xFE0F; Research plan</div>\n'
        '        <ol class="deep-plan-list" id="deep-plan-list"></ol>\n'
        '      </div>\n'
        '      <div class="deep-body" id="deep-body">\n'
        '        <div class="deep-answer" id="deep-answer"></div>\n'
        '        <div class="deep-refs" id="deep-refs" style="display:none">\n'
        '          <h4>References</h4>\n'
        '          <ol id="deep-refs-list"></ol>\n'
        '        </div>\n'
        '        <div class="deep-figures" id="deep-figures" style="display:none">\n'
        '          <h4>Related Figures</h4>\n'
        '          <div class="deep-figures-grid" id="deep-figures-grid"></div>\n'
        '        </div>\n'
        '      </div>\n'
        '    </div>\n'
        '  </div>\n\n'
        + '  <div class="sort-bar">\n'
        '    <button class="sort-btn" onclick="sortCards(\'date\',\'asc\')">\ucd9c\ud310\uc77c &#x25B2;</button>\n'
        '    <button class="sort-btn" onclick="sortCards(\'date\',\'desc\')">\ucd9c\ud310\uc77c &#x25BC;</button>\n'
        '    <button class="sort-btn" onclick="sortCards(\'score\',\'asc\')">\ud3c9\uc810 &#x25B2;</button>\n'
        '    <button class="sort-btn" onclick="sortCards(\'score\',\'desc\')">\ud3c9\uc810 &#x25BC;</button>\n'
        '  </div>\n\n'
        '  <div id="cards">\n\n'
        + "\n\n".join(topic_groups_parts) + "\n\n"
        + '  </div>\n'
        '  <div class="credit">\n'
        f'    Generated by Claude Code &middot; {esc(theme["title"])} Paper Curation &middot; {TODAY}\n'
        '  </div>\n\n'
        '</div>\n\n'
        '<div id="lightbox" class="lightbox"><img id="lightbox-img" alt=""></div>\n\n'
        f'<script>\n{JS}\n</script>\n\n'
        + _audio_modal("이 Deep Research 답변을 팟캐스트형 오디오로 생성합니다. (Gemini · 키는 브라우저에만 저장 · 완성본은 이메일로도 전송)") + "\n"
        + _audio_script("", mode="deep", provider_js=_AUDIO_PROVIDER_JS) + "\n"
        + '<footer style="text-align:center;padding:2rem 0 1rem;color:#999;font-size:0.85rem;border-top:1px solid #eee;margin-top:3rem;">'
        '게재 논문은 arXiv&middot;OpenReview 등 공개 프리프린트이며 저작권은 원저작자에게 귀속됩니다 &middot; 리뷰&middot;요약&middot;Deep Research 답변은 생성형 AI가 생성한 결과물입니다'
        + operator_attribution
        + '</footer>\n\n'
        '</body>\n</html>'
    )

    out_path = os.path.join(TOPIC_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(HTML)
    print(f"Written: {out_path} ({len(HTML):,} chars)")


    # Operator convenience: refresh docs/_zotero_keys.json (slug -> Zotero
    # itemKey). The Deep Research References list checks this on page load
    # and, if present, adds a one-click 'Open PDF' button next to each
    # reference. The button uses 'zotero://open-pdf/library/items/<KEY>'
    # which the Zotero desktop app handles directly. Git-ignored, so the
    # Cloudflare deployment never sees it.
    # Ordinary rendering is local-only and network-free: existing caches remain
    # available to the page, but Zotero credentials are never resolved unless
    # an operator explicitly asks to refresh them.
    _refresh_zotero_cache = (
        bool(os.environ.get("PAPER_CURATION_REFRESH_ZOTERO_CACHE"))
        and not bool(os.environ.get("SKIP_ZOTERO_KEYS"))
    )
    try:
        import urllib.request as _urllib_request
        _api_key = get_zotero_api_key() if _refresh_zotero_cache else ""
        _user_id = get_zotero_user_id() if _refresh_zotero_cache else ""
        # The map is shared across all topics + git-ignored (localhost only).
        # Re-paginating the whole Zotero library is opt-in. Existing caches are
        # consumed as-is; set PAPER_CURATION_REFRESH_ZOTERO_CACHE=1 to refresh.
        _zk_existing = Path(DOCS_DIR) / "_zotero_keys.json"
        _zm_existing = Path(DOCS_DIR) / "_zotero_meta.json"
        if not _refresh_zotero_cache:
            print(f"Zotero keys: using existing {_zk_existing} (refresh not requested)")
        elif _api_key and _user_id:
            _items = []
            _start = 0
            _limit = 100
            while True:
                _url = f"https://api.zotero.org/users/{_user_id}/items/top?format=json&limit={_limit}&start={_start}"
                _req = _urllib_request.Request(_url, headers={
                    "Zotero-API-Key": _api_key,
                    "User-Agent": "Mozilla/5.0",
                })
                with _urllib_request.urlopen(_req, timeout=30) as _resp:
                    _batch = json.load(_resp)
                if not _batch:
                    break
                _items.extend(_batch)
                if len(_batch) < _limit:
                    break
                _start += _limit

            def _norm_title(t):
                return re.sub(r"\s+", " ", t.lower().strip()) if t else ""

            def _norm_arxiv(s):
                m = re.search(r"(\d{4}\.\d{4,5})", s or "")
                return m.group(1) if m else ""

            # Index Zotero items by title AND DOI AND arXiv-id. The 'Open PDF'
            # button must reflect "this paper has a PDF", not "its title happens
            # to match" — exact-title matching silently dropped papers whose
            # stored title differs (truncation, punctuation, version suffix) even
            # when a PDF exists. DOI/arXiv give a robust ID-first fallback.
            _title_to_key, _doi_to_key, _arxiv_to_key = {}, {}, {}
            _zmeta = {}  # normalized-title -> {url, doi} for build_search_index
            for _it in _items:
                _d2 = _it.get("data", {})
                _zt = re.sub(r"[^a-z0-9]", "", (_d2.get("title", "") or "").lower())
                if _zt:
                    _zmeta.setdefault(_zt, {"url": (_d2.get("url") or "").strip(),
                                            "doi": (_d2.get("DOI") or "").strip()})
                _k = _it.get("key", "")
                if not _k:
                    continue
                if _d2.get("title"):
                    _title_to_key.setdefault(_norm_title(_d2["title"]), _k)
                _doi = (_d2.get("DOI", "") or "").lower().strip()
                if _doi:
                    _doi_to_key.setdefault(_doi, _k)
                _ax = _norm_arxiv((_d2.get("url", "") or "") + " "
                                  + (_d2.get("extra", "") or "") + " "
                                  + (_d2.get("archiveID", "") or ""))
                if _ax:
                    _arxiv_to_key.setdefault(_ax, _k)

            # Fetch attachment items so we can map parent -> PDF attachment
            # key. zotero://open-pdf requires the *attachment* key, not the
            # parent item key, to open the PDF directly.
            print("  Fetching Zotero attachments for PDF key mapping...")
            _attach_items = []
            _start = 0
            while True:
                _url = f"https://api.zotero.org/users/{_user_id}/items?itemType=attachment&format=json&limit={_limit}&start={_start}"
                _req = _urllib_request.Request(_url, headers={
                    "Zotero-API-Key": _api_key,
                    "User-Agent": "Mozilla/5.0",
                })
                with _urllib_request.urlopen(_req, timeout=30) as _resp:
                    _batch = json.load(_resp)
                if not _batch:
                    break
                _attach_items.extend(_batch)
                if len(_batch) < _limit:
                    break
                _start += _limit

            # Build parent_key -> first PDF attachment_key map
            _parent_to_pdf = {}
            for _att in _attach_items:
                _d = _att.get("data", {})
                _parent = _d.get("parentItem", "")
                _ct = _d.get("contentType", "") or ""
                _att_key = _att.get("key", "")
                if _parent and _att_key and "pdf" in _ct.lower() and _parent not in _parent_to_pdf:
                    _parent_to_pdf[_parent] = _att_key
            print(f"  {len(_parent_to_pdf)} PDF attachments found")

            _slug_to_key = {}
            _papers_index = Path(_PAPERS_DIR) / "_papers_index.json"
            if _papers_index.exists():
                with open(_papers_index, "r", encoding="utf-8") as _pf:
                    for _p in json.load(_pf):
                        _s = _p.get("slug", "")
                        if not _s:
                            continue
                        # Resolve the Zotero parent item: title first (preserves
                        # all existing matches), then DOI, then arXiv-id — so a
                        # title mismatch no longer hides a paper that has a PDF.
                        _parent_key = _title_to_key.get(_norm_title(_p.get("title", "")))
                        if not _parent_key:
                            _doi = (_p.get("doi", "") or "").lower().strip()
                            _parent_key = _doi_to_key.get(_doi) if _doi else None
                        if not _parent_key:
                            _ax = _norm_arxiv((_p.get("arxiv_id", "") or "") + " "
                                              + (_p.get("url", "") or "") + " " + _s)
                            _parent_key = _arxiv_to_key.get(_ax) if _ax else None
                        if _parent_key:
                            # Use PDF attachment key if available, fall back
                            # to parent key (which at least selects the item)
                            _slug_to_key[_s] = _parent_to_pdf.get(_parent_key, _parent_key)
            if _slug_to_key:
                _zk_path = Path(DOCS_DIR) / "_zotero_keys.json"
                _zk_path.write_text(json.dumps(_slug_to_key), encoding="utf-8")
                print(f"Zotero keys: {_zk_path} ({len(_slug_to_key)} matched, for localhost dev, git-ignored)")
            # Title -> {url, doi} map so build_search_index can give non-DOI
            # papers a real external URL (Zotero `url`). Local-only, git-ignored.
            _zm_path = Path(DOCS_DIR) / "_zotero_meta.json"
            _zm_path.write_text(json.dumps(_zmeta, ensure_ascii=False), encoding="utf-8")
            print(f"Zotero meta: {_zm_path} ({len(_zmeta)} titles, url/doi enrichment, git-ignored)")
    except Exception as _e:
        print(f"Zotero keys skipped: {_e}")

    # Verify no old-style paths
    old_paths = re.findall(r'(?:href|src)="(\d{3}_[^"]*)"', HTML)
    if old_paths:
        print(f"WARNING: {len(old_paths)} old-style paths found (should use ../papers/ prefix):")
        for p in old_paths[:5]:
            print(f"  {p}")
    else:
        print("OK: All paths use ../papers/ prefix")

    # Validate category/sub-category descriptions
    print("\n=== Description Quality Check ===")
    all_issues = []
    for ca_name, ca_data in category_analyses.items():
        # Validate overview
        overview = ca_data.get("description_ko", "")
        all_issues.extend(validate_description(overview, ca_name))
        # Validate sub-theme descriptions
        raw_stko = ca_data.get("sub_themes_ko", [])
        if isinstance(raw_stko, list):
            for st in raw_stko:
                if isinstance(st, dict):
                    all_issues.extend(validate_description(
                        st.get("description_ko", ""), ca_name, st.get("name", "")))
        elif isinstance(raw_stko, dict):
            for k, v in raw_stko.items():
                all_issues.extend(validate_description(v, ca_name, k))

    if all_issues:
        print(f"WARNING: {len(all_issues)} issues found:")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("OK: All descriptions pass quality check")


if __name__ == "__main__":
    from _env_guard import force_py312
    force_py312()
    _run_topic_index()
