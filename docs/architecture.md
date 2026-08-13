# Architecture

## Package direction

The installable `src/paper_curation` package is the product boundary. Dependencies flow inward:

`cli` and `orchestration` → `application` → `domain`; integrations, retrieval, bibliography, rendering, and configuration implement ports owned by the inner layers. The domain never imports the CLI, filesystem/network integrations, or rendering assets. `pipeline/` is retained for compatibility and operational adapters; `pipeline/run_full.py` is a compatibility wrapper, not the primary architecture.

## Responsibilities

| Layer | Responsibility |
|---|---|
| domain | Stable curation concepts, validation rules, and plans; no I/O. |
| application | Use cases for setup, inspection, build, update, validation, repair, and deployment planning. |
| integrations | Zotero, providers, local filesystem, network, and deployment adapters. |
| retrieval | Index construction and read-only query execution; queries do not rebuild an index. |
| bibliography | Local bibliography database, provenance, locking, and integrity checks. |
| rendering | Transforms reviewed data into static pages and packaged UI resources. |
| orchestration | Orders declared steps, reports plans/receipts, and executes adapters. |
| config | Parses, validates, previews, and explicitly applies local configuration migration. |
| cli | Maps the official `paper-curation` commands to application use cases. |

## Side-effect policy

Plans are declarative: a use case names required steps and their inputs before an adapter performs I/O. `inspect` and default `doctor` are read-only. `repair` previews by default and writes only with `--execute`. `build`, `update`, and `deploy` are distinct operations; deploy is explicit and public only when the local configuration selects a public destination. No command infers recipients, remote targets, credentials, or publication intent.

## Static resources and browser boundary

Rendering assets are package data, not ad-hoc copies from a caller working directory. Static output contains no owner credentials. Browser-supplied answer keys remain in memory for one page load and are not persisted in Web Storage or encoded in URLs. Same-origin services may use server-held credentials only behind their configured server boundary.

## Configuration evolution

Configuration migration is local and reversible at the operator boundary: preview first, inspect the report, then execute. It preserves recognized existing local-data locations and public URL values. Unknown or unrepresentable values are reported rather than silently discarded.

## Provider selection

Insights use the configured backend order in `EXTRACT_INSIGHTS_CC_BACKENDS`.
That order chooses one configured provider; it is **not a fallback chain**
(`대체 체인이 아니다`). A selected provider failure is surfaced instead of
substituting another provider.

## Official commands

`paper-curation setup`, `migrate`, `inspect`, `doctor`, `build`, `update`, `serve`, `query`, `validate`, `repair`, and `deploy` are the supported user interface. Advanced compatibility troubleshooting may invoke `pipeline/run_full.py`; it remains available for existing callers and is not claimed to be removed.
