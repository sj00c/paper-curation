"""
papers/_papers_index.json 재생성.

모든 papers/{slug}/review.md를 파싱하여 마스터 인덱스를 생성한다.

Usage:
  PYTHONUTF8=1 python build_papers_index.py --topic <topic>  # topics 필드에 topic 할당
"""

import argparse
import json
import os
import re
import sys

from config_loader import PAPERS_DIR as _PAPERS_DIR, get_papers_index_path
PAPERS_DIR = str(_PAPERS_DIR)


from lib.dateutil import normalize_date as normalize_date_to_yyyymm


def _slug_has_figures(slug):
    fig_dir = os.path.join(PAPERS_DIR, slug, "figures")
    return os.path.isdir(fig_dir) and any(
        f.endswith((".png", ".webp")) for f in os.listdir(fig_dir)
    )


def _text_md_sha256(slug):
    text_path = os.path.join(PAPERS_DIR, slug, "text.md")
    if not os.path.exists(text_path):
        return ""
    try:
        import hashlib
        with open(text_path, "rb") as tf:
            return hashlib.sha256(tf.read()).hexdigest()[:16]
    except Exception:
        return ""


def parse_review(slug):
    """review.md에서 메타데이터와 평가 점수를 추출.

    Phase 3: prefer YAML frontmatter (schema v1) when present; fall back
    to legacy body-regex parsing for review.md files that have not been
    re-injected with the new schema yet.
    """
    review_path = os.path.join(PAPERS_DIR, slug, "review.md")
    if not os.path.exists(review_path):
        return None

    with open(review_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Try frontmatter first — single source of truth post-migration.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        from inject_frontmatter import parse_frontmatter
        fm, body = parse_frontmatter(content)
    except Exception:
        fm, body = {}, content

    if fm.get("schema_version") == "v1":
        scores_dict = fm.get("scores") or {}
        return {
            "title": fm.get("title") or slug,
            "authors": (fm.get("authors") or [])[:5],
            "date": normalize_date_to_yyyymm(str(fm.get("date") or "")),
            "doi": str(fm.get("doi") or ""),
            "essence": str(fm.get("essence") or "")[:500],
            "score": float(scores_dict.get("overall", fm.get("score", 0)) or 0),
            "has_pdf": os.path.exists(os.path.join(PAPERS_DIR, slug, "text.md")),
            "has_figures": _slug_has_figures(slug),
            "verdict": "",
            "text_md_sha256": _text_md_sha256(slug),
            "doi_verified": True,  # schema-validated → trusted
        }

    # ── Legacy body-regex path (pre-Phase 3 review.md without frontmatter) ──
    title_m = re.search(r'^#\s+(.+)', body, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else slug

    authors_m = re.search(r'\*\*저자\*\*:\s*([^|*\n]+?)(?:\s*\|)', body)
    authors = [a.strip() for a in authors_m.group(1).split(",") if a.strip()] if authors_m else []

    date_m = re.search(r'\*\*날짜\*\*:\s*(.+?)(?:\s*\||\s*$)', body, re.MULTILINE)
    date_raw = date_m.group(1).strip() if date_m else ""
    date = normalize_date_to_yyyymm(date_raw)

    doi_m = re.search(r'\*\*DOI\*\*:\s*\[?([^\]\s\)]+)', body)
    doi = doi_m.group(1).strip() if doi_m else ""

    essence = ""
    ess_m = re.search(r'## Essence\s*\n(.*?)(?=\n## |\Z)', body, re.DOTALL)
    if ess_m:
        lines = [l.strip() for l in ess_m.group(1).strip().split('\n')
                 if l.strip() and not l.strip().startswith('![') and not l.strip().startswith('*')]
        essence = " ".join(lines)[:300]

    scores = {}
    for label, key in [("Novelty", "novelty"), ("Technical Soundness", "tech"),
                        ("Significance", "sig"), ("Clarity", "clarity"), ("Overall", "overall")]:
        m = re.search(rf'{label}\D*(\d+(?:\.\d+)?)\s*/\s*5', body)
        if m:
            scores[key] = float(m.group(1))

    verdict_m = re.search(r'\*\*총평\*\*[:\s]*(.+?)(?:\n|$)', body)
    verdict = verdict_m.group(1).strip() if verdict_m else ""

    # Figures
    fig_dir = os.path.join(PAPERS_DIR, slug, "figures")
    has_figs = os.path.isdir(fig_dir) and any(f.endswith(('.png', '.webp')) for f in os.listdir(fig_dir))

    # Has PDF (text.md exists = had PDF) + integrity hash
    text_path = os.path.join(PAPERS_DIR, slug, "text.md")
    has_pdf = os.path.exists(text_path)
    text_md_sha256 = ""
    if has_pdf:
        try:
            import hashlib
            with open(text_path, "rb") as tf:
                text_md_sha256 = hashlib.sha256(tf.read()).hexdigest()[:16]
        except Exception:
            pass

    # DOI verification: does review.md mention index.doi anywhere?
    # (Cheap signal that review was generated from the right paper.)
    doi_verified = False
    if doi:
        norm_doi = doi.lower()
        for pref in ("https://doi.org/", "http://doi.org/", "doi:"):
            if norm_doi.startswith(pref):
                norm_doi = norm_doi[len(pref):]
        doi_verified = norm_doi[:30] in content.lower()

    return {
        "title": title,
        "authors": authors[:5],
        "date": date,
        "doi": doi,
        "essence": essence,
        "score": scores.get("overall", 0),
        "has_pdf": has_pdf,
        "has_figures": has_figs,
        "verdict": verdict,
        "text_md_sha256": text_md_sha256,
        "doi_verified": doi_verified,
    }


def _run_build_index(topic):
    """Programmatic entrypoint. Returns the generated index list."""
    index_path = os.path.join(PAPERS_DIR, "_papers_index.json")
    existing = {}
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            for p in json.load(f):
                existing[p["slug"]] = p

    index = []
    for slug in sorted(os.listdir(PAPERS_DIR)):
        slug_dir = os.path.join(PAPERS_DIR, slug)
        if not os.path.isdir(slug_dir) or not slug[0].isdigit():
            continue

        parsed = parse_review(slug)
        if not parsed:
            continue

        prev = existing.get(slug, {})

        # Migrate old flat fields → classifications[topic] structure
        # Only migrate into the topic that matches `topic` arg (prevents cross-contamination)
        classifications = prev.get("classifications", {})
        if not classifications and prev.get("primary_category"):
            primary_topic = prev.get("primary_topic", topic)
            classifications[primary_topic] = {
                "primary_category": prev.get("primary_category", ""),
                "all_categories": prev.get("all_categories", []),
                "sub_category": prev.get("sub_category", ""),
            }

        entry = {
            "slug": slug,
            "title": parsed["title"],
            "authors": parsed["authors"],
            "date": parsed["date"],
            "doi": parsed["doi"],
            "topics": prev.get("topics", [topic]),
            "primary_topic": prev.get("primary_topic", topic),
            "classifications": classifications,
            "score": parsed["score"],
            "essence": parsed["essence"],
            "has_pdf": parsed["has_pdf"],
            "has_figures": parsed["has_figures"],
            "review_date": prev.get("review_date", ""),
            "text_md_sha256": parsed.get("text_md_sha256", ""),
            "doi_verified": parsed.get("doi_verified", False),
            "zotero_item_key": prev.get("zotero_item_key", ""),
            "pdf_path": prev.get("pdf_path", ""),
        }
        index.append(entry)

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from lib.atomic_io import atomic_write_json
    atomic_write_json(index_path, index)

    with_scores = sum(1 for p in index if p["score"] > 0)
    with_cats = sum(1 for p in index if p.get("classifications"))
    print(f"Generated _papers_index.json: {len(index)} papers")
    print(f"  With scores: {with_scores}")
    print(f"  With category: {with_cats}")
    print(f"  With essence: {sum(1 for p in index if p['essence'])}")
    return index


def main():
    parser = argparse.ArgumentParser(description="Rebuild _papers_index.json")
    parser.add_argument("--topic", required=True, help="Topic to assign to papers")
    args = parser.parse_args()
    _run_build_index(topic=args.topic)


if __name__ == "__main__":
    from _env_guard import force_py312
    force_py312()
    main()
