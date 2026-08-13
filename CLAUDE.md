# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This repository curates papers from a configured Zotero collection into structured reviews,
HTML pages, topic views, and optional search indexes. All local data, credentials, collection
names, storage locations, hosting targets, and notification recipients belong in local
configuration; do not add them to repository documentation or tracked files.

`docs/papers/` is the source of generated paper content. A topic view under `docs/<topic>/`
contains its generated index, classifications, narratives, network data, and optional search
artifacts. Generated corpus content is intentionally ignored by Git.

## Local setup and configuration

Start by reading `config.example.json`, then create an untracked `config.json` with the Zotero
collection, local PDF directory, and only the optional integrations required by this install.
Credentials must be supplied through local configuration or the environment, never committed.

`pipeline/setup.py` is an interactive local configuration helper. It may create local
configuration and install a local Claude skill at `~/.claude/skills/paper-curation/`, but it
does **not** run a curation build, deploy content, publish a branch, or send notifications.
Review the generated configuration before running any pipeline command.

```bash
python pipeline/setup.py --no-install
```

A normal local dependency setup is deliberately separate from curation:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Architecture

| Component | Responsibility |
|---|---|
| `pipeline/run_full.py` | Orchestrates selected local pipeline modes and validates incompatible options. |
| Zotero integration | Retrieves configured collection metadata and attachments. |
| `run_update_force.py` | Extracts text and figures, creates reviews, and renders paper HTML. |
| `build_papers_index.py` | Rebuilds the paper metadata index atomically. |
| `topic_modeling.py` / `classify_papers.py` | Creates or applies topic classifications. Zotero hierarchy classification is also supported. |
| `build_topic_index.py` | Produces the topic index, navigation, and search UI. |
| `build_search_index.py` | Builds the optional hybrid retrieval index. |
| `validate_papers.py` | Checks generated-content integrity; `--strict` fails on violations. |
| `prepare_deploy.py` | Prepares a configured deployment target; it is never part of local setup. |

The retrieval UI combines lexical and dense retrieval when a search index is available. Query
embeddings may be served by a configured worker endpoint or `pipeline/serve_local.py`; readers
need not receive provider credentials. Optional answer-generation credentials are BYOK.

Cross-category insights choose one configured backend candidate. A failure is not retried on a
different provider: **대체 금지**. Missing optional credentials disable the dependent feature;
they do not enable a substitute provider.

## Routine local commands

All commands below act on the explicit `<topic>` supplied by the operator. Start with a dry run
when the source may alter external state.

```bash
# Inspect the planned curation work without writing content.
PYTHONUTF8=1 python pipeline/run_full.py --topic <topic> --mode curate --source web --dry-run

# Curate from the configured local/Zotero source.
PYTHONUTF8=1 python pipeline/run_full.py --topic <topic> --mode curate --source zotero

# Rebuild generated views for an existing topic.
PYTHONUTF8=1 python pipeline/run_full.py --topic <topic> --mode rebuild

# Validate generated output.
PYTHONUTF8=1 python pipeline/validate_papers.py --topic <topic> --strict

# Query an existing local search index without rebuilding it.
python pipeline/query_search_index.py --topic <topic> --query "example research question" --mode hybrid --json
```

## Classification and bibliography

The default classifier uses stored embedding and clustering artifacts. With
`--classify-source zotero`, child collections in the configured Zotero collection become
categories; `--unclassified` controls whether an explicitly named unclassified collection is
included. These modes write the same downstream classification schema.

`pipeline/build_bibliography_db.py` builds the local bibliographic database from paper metadata
and sidecars. It records bibliographic fields and normalized affiliation evidence. Keep one
writer per local database; use the provided lock and validation tools rather than sharing a live
SQLite file through a sync service. Affiliation evidence is retained with its source so reports
can distinguish publisher metadata, resolved records, and PDF-derived inference.

```bash
PYTHONUTF8=1 python pipeline/build_bibliography_db.py --topic <topic>
PYTHONUTF8=1 python pipeline/check_bibliography_db.py --strict
python pipeline/report_field_leaders.py --topic <topic> --top 20
```

## Explicit recovery and destructive operations

Recovery commands are not onboarding steps. Run their dry-run form first, inspect the report,
and use an execute flag only when the operator has confirmed the affected scope.

```bash
# Audit only; does not remove artifacts.
PYTHONUTF8=1 python pipeline/audit_matching.py --topic <topic>

# Backs up and removes flagged generated review artifacts after audit.
PYTHONUTF8=1 python pipeline/fix_matching.py --topic <topic> --execute

# DESTRUCTIVE: removes duplicate Zotero items after a dry-run review.
PYTHONUTF8=1 python pipeline/dedup_zotero.py --topic <topic> --execute

# DESTRUCTIVE: deletes stale generated files after previewing the cleanup plan.
PYTHONUTF8=1 python pipeline/cleanup.py --execute
```

## Publication and notifications

Building locally does not publish anything. Deployment requires an explicitly configured hosting
target and the credentials accepted by that target. Invoke the deploy mode only after reviewing
the generated output and target configuration:

```bash
# EXTERNAL SIDE EFFECT: publish only to the configured target.
PYTHONUTF8=1 python pipeline/run_full.py --topic <topic> --mode deploy
```

Notifications are opt-in local configuration. Do not infer recipients, domains, repository
branches, remote machines, or credentials from this repository.

## Engineering rules

- Keep `AGENTS.md` and `CLAUDE.md` identical after their distinct headers.
- Treat `config.json`, caches, generated corpus output, and credentials as local state.
- Preserve the canonical `review.md` → `index.html` rendering flow; do not hand-edit generated
  HTML when the source review or renderer should be fixed.
- Use explicit topics and inspect dry-run output before operations that create, change, publish,
  or delete data.
- Keep API behavior documented as implemented; do not promise automatic fallback, build,
  deployment, or notification behavior.
