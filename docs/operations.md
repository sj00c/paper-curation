# Paper-Curation Operations Manual

Detailed recipes, concurrency tuning, and recovery flows for the
paper-curation pipeline. The trigger-side dispatcher lives in
`SKILL.md` — this file is the operator's reference.

## Pipeline overview

Single orchestrator: `pipeline/run_full.py` (3 axes — `--mode`,
`--source`, `--images`). Individual scripts under `pipeline/*.py` are
also importable as functions from `pipeline.api`:

```python
from pipeline.api import (
    search, register, sync, dedup_zotero,
    curate, classify, topic_model, category_summary, insights,
    timeline, network, search_index, topic_index, review_to_html,
    deploy, validate, audit_matching, fix_matching, cleanup,
)
```

## Modes (run_full.py)

| Mode | Default `--source` | Default `--images` | Purpose |
|------|--------------------|---------------------|---------|
| `curate` | `zotero` | `skip` | Pick up new papers; reuse existing reviews |
| `rebuild` | `zotero` | `all` | Regenerate everything (destructive — review.md/figures wiped) |
| `reclassify` | (none) | `changed` | Re-run topic_modeling + classify only |
| `retime` | (none) | `all` | Regenerate timeline narrative + images |
| `deploy` | (none) | `skip` | wrangler deploy + gh-pages sync + master push |
| `audit` | — | — | Standalone: PDF↔review mismatch audit |
| `fix-matching` | — | — | Standalone: delete artifacts for audit-flagged slugs |
| `dedup` | — | — | Standalone: Zotero collection dedup |
| `validate` | — | — | Standalone: post-build validation gate |

`--source web` adds search + register + sync as a preflight to `curate`.

## Common Commands

```bash
# Weekly run — web search + Zotero register + new-paper review
PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode curate --source web --days 7

# Local-only update (Zotero already has new papers)
PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode curate --source zotero

# Force-rebuild specific slugs (recovery)
PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode rebuild --slugs 088,1093 --strict-pdf

# Reclassify only (no LLM, HDBSCAN approximate_predict)
PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode reclassify

# Timeline narrative + images
PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode retime --images all

# Deploy
PYTHONUTF8=1 python pipeline/run_full.py --topic humanoid --mode deploy

# Dry-run (no execution)
PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode curate --source web --dry-run
```

## Safety flags

- `--strict-pdf` — block fuzzy PDF matching; ID (Zotero/DOI/arXiv) only
- `--slugs A,B,C` — restrict to specific slug prefixes
- `--dry-run` — print plan, no execution
- `--skip-dedup` / `--dedup-execute` — control Zotero dedup preflight
- `--yes` — bypass `--mode rebuild` confirmation gate

## Concurrency (Anthropic Tier 4 default)

`run_full.py --concurrency` and `run_update_force.py --concurrency`
control per-paper review parallelism. Default 16 (Tier 4). Lower
tiers should drop:

| Tier | Recommended |
|------|-------------|
| Free / 1 | 2–4 |
| 2 | 6–8 |
| 3 | 10–12 |
| **4** | **16–20** |

Phase 2 added per-category parallelism for the post-review phase:
- `CAT_SUMMARY_PARALLEL` (default 8) — Haiku per-category summaries
- `TIMELINE_NARRATIVE_PARALLEL` (default 8) — Opus per-category narratives
- `TIMELINE_IMAGE_PARALLEL` (default 4) — PaperBanana per-category images
- `EXTRACT_INSIGHTS_PARALLEL` (default 4) — Sonnet per-category paper_connections

Wall-clock for finalize phase: ~25 min → ~6 min at Tier 4.

## Python environment

Standard: conda env `py314` (Python 3.14). Required pip packages:

```bash
conda create -n py314 -c conda-forge python=3.14 pip -y
conda activate py314
pip install anthropic openai google-genai pymupdf Pillow requests pyzotero \
            opendataloader-pdf \
            numpy scikit-learn joblib pyyaml \
            umap-learn hdbscan sentence-transformers
brew install --cask temurin   # Java for opendataloader-pdf
```

Windows fallback (Smart App Control blocks numba/llvmlite):
spin up a separate `py312` env for `topic_modeling.py` and
`classify_papers.py` only — see CLAUDE.md "Windows fallback".

## Korean network workarounds

- **HuggingFace LFS blocked**: download SPECTER2 via AWS S3 mirror to
  `.cache/base/`, then `topic_modeling.py` auto-detects:

  ```bash
  mkdir -p .cache && cd .cache
  curl -L -o specter2_0.tar.gz \
       "https://ai2-s2-research-public.s3.amazonaws.com/specter2_0/specter2_0.tar.gz"
  tar -xzf specter2_0.tar.gz
  ```

- **arXiv chronic 429**: `search_papers.py --skip-arxiv` (OpenAlex + S2 only)
- **OpenDataLoader fallback**: PyMuPDF takes over silently; install
  Temurin Java to get pdffigures2 structure

## Schema v1 frontmatter (Phase 3)

Every `docs/papers/{slug}/review.md` carries YAML frontmatter
populated by `inject_frontmatter.py`. Readers prefer frontmatter over
body-regex parsing when `schema_version: v1` is present.

```yaml
---
title: "<full paper title>"
authors: ["First Last", ...]
date: "2021-07-15"
doi: "..."
primary_topic: ai4s
primary_category: "..."
all_categories: [...]
sub_categories: {"Category": "Sub-category", ...}
sub_category: "..."
scores:
  novelty: 5
  technical: 5
  significance: 5
  clarity: 4
  overall: 5
score: 5
essence: "..."
tags: [paper, ai4s, "ai4s/category-slug/sub-slug", ...]
schema_version: v1
---
```

Migration script: `pipeline/migrate_to_toolschema.py`. Originals are
preserved at `docs/papers/.legacy/{slug}_v0.md`. Re-running the
migration is idempotent (existing backups are kept).

## LLM tool-use + cache

Phase 3 migrated `write_review` and `extract_insights.cross_category`
to Anthropic tool-use schemas. Responses are forced into the schema
shape; the SDK retries on mismatch. Post-hoc fixers
(`fix_python_list_literals`, `fix_figure_paths`, `fix_evaluation_format`,
`validate_review_format`) are no longer invoked.

Each tool-use call is wrapped in `api._llm.cached_call` keyed on
`sha256(prompt || model || schema_version)`. Cache layout:

```
docs/papers/{slug}/.llm_cache/{hash}.json     # per-paper (write_review)
docs/{topic}/.llm_cache/{hash}.json           # per-topic (insights)
```

A re-run of `--mode rebuild` on an unchanged paper costs zero LLM
calls. Pass `force=True` to `cached_call` to bypass.

## Figure pre-validator (Phase 4)

`api.extract.pre_validate_figure(png_path)` runs before each Gemini
figure validation call. Heuristics: file size, dimensions, grayscale
variance. Skips ~30% of Gemini calls on obviously-invalid crops while
deferring borderline cases to the LLM.

## Deploy architecture

- **Cloudflare Workers (Static Assets)**: full content at
  `paper-curation.jehyun-lee.workers.dev`. `prepare_deploy.py` runs
  `npx wrangler deploy` using `CLOUDFLARE_API_TOKEN`/`CF_API_TOKEN` +
  `CLOUDFLARE_ACCOUNT_ID`. `docs/.assetsignore` excludes ai4s/scisci
  (local-only) and caches.
- **GitHub `gh-pages`**: redirect stubs only — one
  `{topic}/index.html` per deployable topic that meta-refreshes to
  the Cloudflare URL.
- **GitHub `master`**: code + `config.example.json` + `wrangler.toml`
  + `docs/.assetsignore`. Topic content (`docs/papers/`,
  `docs/humanoid/`, etc.) is `.gitignore`'d.

`pipeline/prepare_deploy.py` orchestrates everything: PNG→WebP, API-key
strip-then-restore, Cloudflare upload, gh-pages stub sync, Cloudflare
200 OK polling, master commit.

## Recovery flows

```bash
# Audit PDF↔review mismatches
PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode audit

# Delete artifacts for high-confidence mismatches
PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode fix-matching --yes

# Re-review cleaned slugs
PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode rebuild --slugs <list> --strict-pdf

# Validate
PYTHONUTF8=1 python pipeline/run_full.py --topic ai4s --mode validate --yes  # --yes → --strict
```

## Topic configuration

Each topic ↔ Zotero collection is in `config.json`:

```json
{
  "zotero": {
    "collections": {
      "ai4s": "WKEZLEE8",
      "scisci": "3KVIDDKH",
      "humanoid": "...",
      "physical-ai": "..."
    }
  }
}
```

`docs/.assetsignore` controls which topics ship to Cloudflare.

## See also

- `CLAUDE.md` — codebase-wide Claude Code guidance
- `SKILL.md` — the user-facing skill dispatcher (this trigger entry)
- `pipeline/api/__init__.py` — programmatic API (25 functions)
- `pipeline/api/_llm.py` — caching helpers for LLM calls
- `pipeline/api/extract.py` — figure pre-validation heuristics
