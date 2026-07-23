"""
Programmatic API for the paper-curation pipeline.

Existing CLI entrypoints (search_papers.py, register_zotero.py, ...) remain
fully functional; this package exposes their core work as importable
functions so callers can compose them without subprocess overhead.

Public functions are re-exported here so the typical usage is::

    from pipeline.api import search, register, classify, timeline, deploy

    search(topic="my-topic", days=7)
    register(topic="my-topic")
    classify(topic="my-topic")
    timeline(topic="my-topic")
    deploy(topic="my-topic", push=True)

Module-level imports are lazy (done inside each wrapper) so that
importing :mod:`pipeline.api` is cheap and side-effect free.

Phase 1 design: each ``_run_X(...)`` lives inside the original CLI script
and is the single shared body between the CLI ``main()`` and the public
API. Phase 2/3 will add caching, tool-use schemas, and threaded
parallelism inside these ``_run_X`` functions without touching call
sites.
"""

from pathlib import Path
import sys


_PIPELINE = Path(__file__).resolve().parent.parent
if str(_PIPELINE) not in sys.path:
    sys.path.insert(0, str(_PIPELINE))


def _require_topic(topic):
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("topic must be a non-empty string")
    return topic.strip()


# --------------------------------------------------------------------------- #
# Search / Zotero registration / sync
# --------------------------------------------------------------------------- #

def search(topic, *, days=7, max_papers=100, threshold=0.3,
           skip_arxiv=False, since=None, until=None):
    """Run multi-source paper search (arXiv + Semantic Scholar + OpenAlex).

    Returns the result dict that ``search_papers.py`` would have saved to
    ``docs/{topic}/_search_results.json``.
    """
    from search_papers import _run_search
    return _run_search(topic=_require_topic(topic), days=days, max_papers=max_papers,
                       threshold=threshold, skip_arxiv=skip_arxiv,
                       since=since, until=until)


def register(topic, *, input_path=None, dry_run=False):
    """Register search results to Zotero + download PDFs."""
    from register_zotero import _run_register
    return _run_register(topic=_require_topic(topic), input_path=input_path, dry_run=dry_run)


def register_fix_pdfs(topic, *, dry_run=False):
    """Retry PDF downloads for items in the Zotero collection missing PDFs."""
    from register_zotero import _run_fix_pdfs
    return _run_fix_pdfs(topic=_require_topic(topic), dry_run=dry_run)


def register_fix_metadata(topic, *, dry_run=False, limit=None):
    """Backfill thin metadata on existing Zotero items."""
    from register_zotero import _run_fix_metadata
    return _run_fix_metadata(topic=_require_topic(topic), dry_run=dry_run, limit=limit)


def sync(topic, *, dry_run=False):
    """Sync Zotero deletions/renames back into _papers_index.json."""
    from sync_zotero import _run_sync
    return _run_sync(topic=_require_topic(topic), dry_run=dry_run)


def dedup_zotero(topic, *, execute=False):
    """Detect (and optionally remove) Zotero duplicates."""
    from dedup_zotero import _run_dedup
    return _run_dedup(topic=_require_topic(topic), execute=execute)


# --------------------------------------------------------------------------- #
# PDF/text/figure extraction + review writing
# --------------------------------------------------------------------------- #

def extract_text(pdf_path, slug_dir):
    """Extract text.md from a PDF into ``slug_dir``."""
    from run_update_force import extract_text as _impl
    return _impl(pdf_path, slug_dir)


def extract_figures(pdf_path, slug_dir):
    """Render Figures from a PDF into ``slug_dir/figures/``."""
    from run_update_force import extract_figures as _impl
    return _impl(pdf_path, slug_dir)


def write_review(item, slug_dir, figures):
    """Generate review.md for a single paper (Phase 3 will switch this to
    Anthropic tool-use schemas)."""
    from run_update_force import write_review as _impl
    return _impl(item, slug_dir, figures)


def curate(topic, *, mode="curate", concurrency=16, slugs="",
           strict_pdf=False, timeline=False, also_reclassify=False,
           skip_dedup=False, dedup_execute=False, dry_run=False):
    """End-to-end curation batch (PDF → review → classify → timeline → deploy).

    This is the programmatic equivalent of ``run_update_force.py``.
    """
    from run_update_force import _run_curate
    return _run_curate(topic=_require_topic(topic), mode=mode, concurrency=concurrency,
                       slugs=slugs, strict_pdf=strict_pdf, timeline=timeline,
                       also_reclassify=also_reclassify,
                       skip_dedup=skip_dedup, dedup_execute=dedup_execute,
                       dry_run=dry_run)


# --------------------------------------------------------------------------- #
# Master index / topic modelling / classification
# --------------------------------------------------------------------------- #

def build_papers_index(topic):
    """Rebuild docs/papers/_papers_index.json from review.md files."""
    from build_papers_index import _run_build_index
    return _run_build_index(topic=_require_topic(topic))


def topic_model(topic, *, skip_connections=False, skip_classification=False,
                min_cats=8, max_cats=12):
    """Run UMAP + HDBSCAN clustering and persist the bundle."""
    from topic_modeling import _run_topic_model
    return _run_topic_model(topic=_require_topic(topic), skip_connections=skip_connections,
                            skip_classification=skip_classification,
                            min_cats=min_cats, max_cats=max_cats)


def classify(topic, *, slugs=None, dry_run=False):
    """Assign primary/all_categories using the persisted HDBSCAN bundle.

    `slugs` may be a list of slug-prefixes or a comma-separated string.
    """
    from classify_papers import _run_classify
    return _run_classify(topic=_require_topic(topic), slugs=slugs, dry_run=dry_run)


# --------------------------------------------------------------------------- #
# Narrative generation (Haiku/Sonnet/Opus)
# --------------------------------------------------------------------------- #

def category_summary(topic, *, regen_ko=False, categories=None):
    """Build _category_summaries.json (Korean descriptions + sub-themes).

    `categories` is an optional list of category names to selectively regenerate.
    """
    from build_category_summaries import _run_category_summary
    return _run_category_summary(topic=_require_topic(topic), regen_ko=regen_ko,
                                 categories=categories)


def insights(topic, *, insights_only=False, connections_only=False, categories=None):
    """Extract cross-category insights + paper_connections."""
    from extract_insights import _run_insights
    return _run_insights(topic=_require_topic(topic), insights_only=insights_only,
                         connections_only=connections_only,
                         categories=categories)


def timeline(topic, *, main_only=False, category_only=False,
             narrative_only=False, images_only=False, candidates=3,
             categories=None):
    """Generate timeline narrative + PaperBanana images."""
    from generate_timelines import _run_timeline
    return _run_timeline(topic=_require_topic(topic), main_only=main_only,
                         category_only=category_only,
                         narrative_only=narrative_only,
                         images_only=images_only, candidates=candidates,
                         categories=categories)


# --------------------------------------------------------------------------- #
# HTML / network / search index / deploy
# --------------------------------------------------------------------------- #

def network(topic):
    """Build D3.js force-directed network HTML for a topic."""
    from generate_network import _run_network
    return _run_network(topic=_require_topic(topic))


def search_index(topic, *, model=None, limit=None, dry_run=False):
    """Explicit build boundary for Deep Research RAG index creation."""
    try:
        from pipeline.lib.search_index_metadata import EMBEDDING_MODEL, REBUILD_GUIDANCE
    except ModuleNotFoundError:
        from lib.search_index_metadata import EMBEDDING_MODEL, REBUILD_GUIDANCE
    selected_model = model or EMBEDDING_MODEL
    if selected_model != EMBEDDING_MODEL:
        raise ValueError(
            f"search_index model must be {EMBEDDING_MODEL!r}, got {selected_model!r}. {REBUILD_GUIDANCE}"
        )
    from build_search_index import _run_search_index
    return _run_search_index(topic=_require_topic(topic), model=selected_model, limit=limit,
                             dry_run=dry_run)


def topic_index(topic):
    """Render docs/{topic}/index.html (cards + Deep Research UI)."""
    from build_topic_index import _run_topic_index
    return _run_topic_index(topic=_require_topic(topic))


def review_to_html(*, slug=None, slugs=None, all_papers=False):
    """Convert review.md → index.html (for one slug, a range, or all)."""
    from review_to_html import _run_review_to_html
    return _run_review_to_html(slug=slug, slugs=slugs, all_papers=all_papers)


def deploy(topic, *, push=False, quality=90, dry_run=False):
    """PNG→WebP + Cloudflare wrangler deploy + gh-pages stub sync."""
    from prepare_deploy import _run_deploy
    return _run_deploy(topic=_require_topic(topic), push=push, quality=quality, dry_run=dry_run)


# --------------------------------------------------------------------------- #
# Validation / audit / recovery / cleanup
# --------------------------------------------------------------------------- #

def validate(topic, *, strict=False, fix=False):
    """Run the validation gate (figure refs, classification schema, etc.)."""
    from validate_papers import _run_validate
    return _run_validate(topic=_require_topic(topic), strict=strict, fix=fix)


def audit_matching(topic):
    """PDF↔review mismatch audit."""
    from audit_matching import _run_audit
    return _run_audit(topic=_require_topic(topic))


def fix_matching(topic, *, slugs=None, execute=False):
    """Recovery: delete artifacts for audit-flagged slugs so they get re-reviewed."""
    from fix_matching import _run_fix_matching
    return _run_fix_matching(topic=_require_topic(topic), slugs=slugs, execute=execute)


def cleanup(*, execute=False, purge_text=False):
    """Remove stale files (old timelines, caches) + prune narrative JSONs."""
    from cleanup import _run_cleanup
    return _run_cleanup(execute=execute, purge_text=purge_text)


__all__ = [
    # search / zotero
    "search", "register", "register_fix_pdfs", "register_fix_metadata",
    "sync", "dedup_zotero",
    # extract / review
    "extract_text", "extract_figures", "write_review", "curate",
    # index / topic / classify
    "build_papers_index", "topic_model", "classify",
    # narrative
    "category_summary", "insights", "timeline",
    # html / network / search index / deploy
    "network", "search_index", "topic_index", "review_to_html", "deploy",
    # validate / audit / cleanup
    "validate", "audit_matching", "fix_matching", "cleanup",
]
