"""
Unified topic index builder for paper-curation.
Reads reviews from papers/ central repo, generates {topic}/index.html.

Usage: PYTHONUTF8=1 python build_topic_index.py <configured-topic>
  e.g. PYTHONUTF8=1 python build_topic_index.py my_topic
"""
import json, os, re, sys
from html import escape
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST).strftime("%Y-%m-%d")

from collections import OrderedDict
from config_loader import PAPERS_DIR as _PAPERS_DIR, DOCS_DIR, get_topic_dir, get_zotero_api_key, get_zotero_user_id, get_topic_profile
from lib.categories import category_slug
from lib.search_index_metadata import (
    CACHE_FORMAT_VERSION,
    CHUNK_HASH_BASIS,
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
    EMBEDDING_PROVIDER,
    EMBEDDING_QUANTIZATION,
    EMBEDDING_SIDECAR_FILE,
    EMBEDDING_TASK_TYPE,
    INDEX_SCHEMA_VERSION,
    PROVENANCE_STATUS,
    REBUILD_GUIDANCE,
    SIDECAR_FORMAT_VERSION,
)
PAPERS_DIR = str(_PAPERS_DIR)

def get_topic():
    if len(sys.argv) > 1 and sys.argv[1].strip():
        return sys.argv[1].strip()
    raise SystemExit("Usage: PYTHONUTF8=1 python build_topic_index.py <topic>")


def _run_topic_index(topic=None, cross=None):
    """Build {topic}/index.html (cards + Deep Research UI).

    Phase 5 refactor: module-level code was wrapped into this
    function so the script is importable without side-effects.
    Pass ``topic`` explicitly; CLI execution reads ``sys.argv[1]``.
    """
    TOPIC = topic.strip() if isinstance(topic, str) else topic
    if TOPIC is None:
        TOPIC = get_topic()
    if not TOPIC:
        raise ValueError("topic must be a non-empty string")
    TOPIC_DIR = str(get_topic_dir(TOPIC))

    topic_profile = get_topic_profile(TOPIC)
    topic_label = topic_profile.get("label") or topic_profile.get("collection_name") or TOPIC
    theme = {
        "gradient": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
        "accent": "#3B82F6", "accent_dark": "#2563EB", "accent_light": "#60A5FA",
        "title": topic_label,
        "subtitle_prefix": topic_label,
    }
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
        meta_html = " | ".join(meta_parts)
        badges = []
        for label, key in [("Novelty", "novelty"), ("Technical Soundness", "technical_soundness"),
                            ("Significance", "significance"), ("Clarity", "clarity")]:
            val = paper.get(key)
            if val is not None: badges.append(f'<span class="score-badge">{label}: {val}</span>')
        if score and score > 0: badges.append(f'<span class="score-badge">Overall: {int(score)}</span>')
        badges_html = " ".join(badges)
        fig_html = ""
        if paper["has_fig"]:
            cap = paper.get("fig_caption", "")
            cap_html = f'<p class="fig-caption">{esc(cap)}</p>' if cap else ""
            fig_html = (
                '\n          <div class="paper-fig">'
                f'<img data-src="{esc(paper["fig_src"])}" alt="Figure" class="lazy">'
                f'{cap_html}</div>'
            )
        essence_html = ""
        if paper["essence"]:
            essence_html = (
                '\n          <div class="section">'
                '\n            <div class="section-label">Essence</div>'
                f'\n            <p>{esc(paper["essence"])}</p>'
                '\n          </div>'
            )
        eval_html = ""
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
        link_href = f"../papers/{esc(paper['dir'])}/index.html"
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
        if not text: return ""
        paras = [p.strip() for p in text.split("\n\n") if p.strip()]
        return "\n    ".join(f"<p>{esc(p)}</p>" for p in paras)


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
            '  <h2 class="insights-header" data-dashboard-action="toggle-insights" role="button" tabindex="0">'
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
                    f'\n  <div class="sub-header" data-dashboard-action="toggle-sub" data-target="{sc_id}" role="button" tabindex="0">'
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
            f'      <div class="topic-header" data-dashboard-action="toggle-topic" data-target="{topic_id}" role="button" tabindex="0">\n'
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
            '  <div class="timeline-media">'
            '<img class="timeline-image" src="research_timeline.png" alt="Research Timeline">'
            '</div>\n'
        )
        if exec_html:
            research_tl_html += f'  <div class="timeline-summary">\n    {exec_html}\n  </div>\n'
        if os.path.exists(os.path.join(TOPIC_DIR, "network.html")):
            research_tl_html += '  <div class="timeline-network-link"><a href="network.html" target="_blank" rel="noopener noreferrer">&#x1F517; Interactive Paper Network &rarr;</a></div>\n'
        research_tl_html += '</div>\n\n\n'

    # JSON embedded in a non-executable script is parsed via textContent. Escape
    # HTML-significant characters and JavaScript line separators defensively.
    bootstrap_json = json.dumps(
        {
            "schema": 1,
            "topic_alias": TOPIC,
            "audio_capability": {"schema": "AudioCapabilityV1", "state": "UNAVAILABLE"},
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
    bootstrap_json = (bootstrap_json.replace("<", "\\u003c").replace(">", "\\u003e")
                       .replace("&", "\\u0026").replace("\u2028", "\\u2028")
                       .replace("\u2029", "\\u2029"))

    HTML = (
        '<!DOCTYPE html>\n'
        '<html lang="ko">\n'
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">\n'
        f'<title>{esc(theme["title"])} &#8212; Paper Curation</title>\n'
        '<link rel="stylesheet" href="../public/paper-curation-local.css">\n'
        '</head>\n'
        f'<body class="{"dashboard-cross" if cross else "dashboard-local"}">\n'
        '<div class="container">\n'
        '  <div class="hero">\n'
        f'    <h1>{esc(theme["title"])} &#8212; Paper Curation</h1>\n'
        '    <div class="stats">\n'
        f'      <div class="stat"><div class="stat-num">{unique_papers}</div><div class="stat-label">\ub9ac\ubdf0 \uc644\ub8cc</div></div>\n'
        f'      <div class="stat"><div class="stat-num">{num_cats}</div><div class="stat-label">MECE \uce74\ud14c\uace0\ub9ac</div></div>\n'
        f'      <div class="stat"><div class="stat-num">{TODAY}</div><div class="stat-label">\ud050\ub808\uc774\uc158 \uc77c\uc790</div></div>\n'
        '    </div>\n'
        # Atom \ud53c\ub4dc \ub9c1\ud06c \u2014 hero(\ub2e4\ud06c \uadf8\ub77c\ub514\uc5b8\ud2b8) \uc704\ub77c \ud770\uc0c9+opacity \ub85c \uc774\uc9c8\uac10 \uc5c6\uac8c
        '    <div class="hero-feed-link"><a href="feed.xml" title="Atom 피드 구독 (RSS)">&#x1F4E1; RSS</a></div>\n'
        '  </div>\n\n\n'
        + research_tl_html
        + render_insights_section()
        + '  <div class="search-box">\n'
        '    <div class="search-row">\n'
        '      <input type="text" id="search-input" placeholder="Search papers by title, DOI, keyword...">\n'
        '      <div class="local-action-controls">\n'
        '        <button class="deep-btn" id="deep-normal" type="button">Normal</button>\n'
        '        <button class="deep-btn" id="deep-deeper" type="button">Deeper</button>\n'
        '        <button class="deep-btn" id="deep-audio" type="button" hidden disabled aria-disabled="true">Audio</button>\n'
        '      </div>\n'
        '    </div>\n'
        '    <div class="search-hint" id="search-hint">Enter title, DOI, author name, or keyword to filter</div>\n'
        '    <div class="search-count" id="search-count"></div>\n'
        '    <div class="deep-status" id="deep-status" role="status" aria-live="polite"></div>\n'
        '  </div>\n\n'
        + '  <div class="sort-bar">\n'
        '    <button class="sort-btn" data-dashboard-action="sort" data-sort-key="date" data-sort-dir="asc">\ucd9c\ud310\uc77c &#x25B2;</button>\n'
        '    <button class="sort-btn" data-dashboard-action="sort" data-sort-key="date" data-sort-dir="desc">\ucd9c\ud310\uc77c &#x25BC;</button>\n'
        '    <button class="sort-btn" data-dashboard-action="sort" data-sort-key="score" data-sort-dir="asc">\ud3c9\uc810 &#x25B2;</button>\n'
        '    <button class="sort-btn" data-dashboard-action="sort" data-sort-key="score" data-sort-dir="desc">\ud3c9\uc810 &#x25BC;</button>\n'
        '  </div>\n\n'
        '  <div id="cards">\n\n'
        + "\n\n".join(topic_groups_parts) + "\n\n"
        + '  </div>\n'
        '  <div class="credit">\n'
        f'    Generated by Claude Code &middot; {esc(theme["title"])} Paper Curation &middot; {TODAY}\n'
        '  </div>\n\n'
        '</div>\n\n'
        '<div id="lightbox" class="lightbox"><img id="lightbox-img" alt=""></div>\n\n'
        f'<script id="dashboard-bootstrap" type="application/json">{bootstrap_json}</script>\n'
        '<script src="../public/paper-curation-local.js" defer></script>\n'
        + '<footer class="dashboard-footer">'
        'Developed by Jehyun Lee, KIST AIX Strategy Department | jehyun.lee@gmail.com'
        '</footer>\n\n'
        '</body>\n</html>'
    )

    out_path = os.path.join(TOPIC_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(HTML)
    print(f"Written: {out_path} ({len(HTML):,} chars)")


    # Operator convenience: write docs/_zotero_keys.json (slug -> Zotero
    # itemKey). The Deep Research References list checks this on page load
    # and, if present, adds a one-click 'Open PDF' button next to each
    # reference. The button uses 'zotero://open-pdf/library/items/<KEY>'
    # which the Zotero desktop app handles directly. Git-ignored, so the
    # Cloudflare deployment never sees it.
    try:
        import urllib.request as _urllib_request
        import time as _time
        _api_key = get_zotero_api_key()
        _user_id = get_zotero_user_id()
        # The map is shared across all topics + git-ignored (localhost only).
        # Re-paginating the whole Zotero library on every topic build only risks
        # an API hang for no benefit, so reuse a recent (<24h) file. Force a
        # refresh by deleting docs/_zotero_keys.json; skip entirely with
        # SKIP_ZOTERO_KEYS=1.
        _zk_existing = Path(DOCS_DIR) / "_zotero_keys.json"
        _zm_existing = Path(DOCS_DIR) / "_zotero_meta.json"
        _zk_fresh = (_zk_existing.exists() and _zm_existing.exists()
                     and (_time.time() - _zk_existing.stat().st_mtime) < 86400)
        if os.environ.get("SKIP_ZOTERO_KEYS") or _zk_fresh:
            print(f"Zotero keys: reusing existing {_zk_existing} (fresh; skip re-fetch)")
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
