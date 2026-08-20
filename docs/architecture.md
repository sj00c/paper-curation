# Architecture

This document explains the architecture. Normative engineering requirements
are owned by [SPEC.md](SPEC.md), product intent by [PRD.md](PRD.md), and current
execution state by [HANDOFF.md](HANDOFF.md). If wording conflicts, those
ownership boundaries take precedence.

## Product source and upstream intake

This fork is the product source of truth. It takes reusable generic material
from `jehyunlee/paper-curation@bab6b9e9` once during this reconstruction; it
does not continuously fetch, merge, rebase, or preserve compatibility with
upstream. Operator credentials, paths, source data, corpus data, receipts, and
generated pages remain installation-local and untracked.

## Package direction

The installable `src/paper_curation` package is the product boundary. Dependencies flow inward:

`cli` and the single composition root → `application` → `domain`.
Integrations, retrieval, bibliography, rendering, and configuration are outer
implementations of ports owned by the inner layers. The domain never imports
the CLI, filesystem, network, rendering, or provider SDK. Application code
never imports `pipeline`, provider SDKs, or concrete adapters. Only the
composition root assembles concrete adapters.

These are enforced source boundaries, not conventions: AST-based tests report
the importing module, line, and forbidden import. The tests inspect Python
imports rather than comments or arbitrary text, so explanatory prose cannot
cause a boundary failure. `pipeline/` is retained only for compatibility and
explicit operational adapters; `pipeline/run_full.py` is a compatibility
wrapper, not the primary architecture.

## Responsibilities

| Layer | Responsibility |
|---|---|
| domain | Stable curation concepts, validation rules, and plans; no I/O. |
| application | Use cases and port contracts for setup, inspection, Core execution, validation, repair, and deployment planning. |
| integrations | Zotero, providers, local filesystem, network, and deployment adapters. |
| retrieval | Index construction and read-only query execution; queries do not rebuild an index. |
| bibliography | Local bibliography database, provenance, locking, and integrity checks. |
| rendering | Transforms reviewed data into static pages and packaged UI resources. |
| orchestration | Orders declared steps, reports plans/receipts, and executes adapters. |
| config | Parses, validates, previews, and explicitly applies local configuration migration. |
| cli | Maps the official `paper-curation` commands to application use cases. |

## Side-effect policy

Plans are declarative: a use case names required steps and their inputs before an adapter performs I/O. `inspect` and default `doctor` are read-only. `repair` previews by default and writes only with `--execute`. `build`, `update`, and `deploy` are distinct operations; deploy is explicit and public only when the local configuration selects a public destination. No command infers recipients, remote targets, credentials, or publication intent.

## Mandatory Core

Every successful curation executes this complete sequence, in order:

1. **IDENTIFY**
2. **MATERIALIZE_SOURCE**
3. **EXTRACT_TEXT**
4. **GENERATE_REVIEW**
5. **WRITE_SIDECAR**
6. **RENDER_PAGE**
7. **COMMIT_RECEIPT**

The Core succeeds only when the source identity is unambiguous, the source and
extracted text validate, the review is complete, and the sidecar, page, and
receipt are loadable. A partial artifact is not a successful result and must
not replace an existing completed result.

## Domain and topic neutrality

Core identity is source-neutral: `source_id`, `scope_id`, `record_id`, and
`attachment_id`. The domain does not know Zotero; the v1 composition selects a
Zotero adapter. Topics, institutions, taxonomies, prompt style, and workspace
locations are installation configuration, never product-code defaults.
Neutrality tests use multiple synthetic topic aliases and temporary workspaces
through the same config, workspace, and rendering contract. They do not rely
only on a blacklist of historic topic names.

## Provider and capability selection

Core review is mandatory and has exactly one explicitly selected provider and
model.
Setup and doctor validate that provider's execution and credential
requirements, and the plan shows its cost classification before execution.
The selected provider failing fails Core; no other provider or model is
instantiated or substituted.

An optional capability requires both `enabled: true`, exactly one selected
provider, and an installed adapter. An enabled enhancement without that adapter
is rejected. Credentials are evidence that a selected provider may run, never
a selection or activation mechanism. Disabled capabilities perform no provider
construction or external call. An optional capability runs only after Core
success; its failure preserves the completed Core result and blocks only
dependents.

The legacy operator insights extension still reads
`EXTRACT_INSIGHTS_CC_BACKENDS` while it is being moved behind the capability
boundary. Its configured order selects one backend; **대체 체인이 아니다**.
Failure of that selected backend is surfaced rather than retried through
another provider.

## Static resources and browser boundary

Rendering assets are package data, not ad-hoc copies from a caller working directory. Static output contains no owner credentials. Browser-supplied answer keys remain in memory for one page load and are not persisted in Web Storage or encoded in URLs. Same-origin services may use server-held credentials only behind their configured server boundary.

## Configuration evolution

Configuration input is strict: unknown keys, invalid types, and invalid
cross-field combinations are rejected. Configuration migration is local and
reversible at the operator boundary: preview first, inspect the report, then
execute. It preserves recognized existing local-data locations and public URL
values. Unknown or unrepresentable values are reported rather than silently
discarded.

Each installation owns its workspace root and the local `papers/`, `.cache/`,
`.staging/`, and `site/` paths beneath it. Corpus data and generated output are
never tracked repository content.

## Official commands

`paper-curation setup`, `migrate`, `inspect`, `doctor`, `build`, `update`,
`serve`, `query`, `validate`, `repair`, and `deploy` are the supported user
interface. Deployment is only an explicit public Cloudflare operation:
`build` and `update` never deploy. `pipeline/run_full.py` is only a
filename-compatibility wrapper around the official CLI; it accepts the same
arguments and owns no historical mode or business logic.
