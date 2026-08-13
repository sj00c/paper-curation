# CLAUDE.md

This file guides coding agents. All content after this header must match its counterpart.

## Product contract

The installable `src/paper_curation` package and its `paper-curation` CLI are the official interface. Use `setup`, `migrate`, `inspect`, `doctor`, `build`, `update`, `serve`, `query`, `validate`, `repair`, and `deploy`. `pipeline/run_full.py` is a compatibility wrapper for existing automation and advanced troubleshooting, not the primary entry point.

## Architecture

Dependencies point inward: CLI and orchestration call application use cases; application owns domain contracts; integrations, retrieval, bibliography, rendering, and config implement those contracts. Domain code has no CLI, network, filesystem, or rendering dependency. Rendering uses packaged static resources. Keep side effects declarative: plan them in application/orchestration and perform them only in integration adapters.

Configured provider candidates are **대체 금지**: choose one configured
provider and surface its failure rather than silently substituting another.

## Operations and security

All configuration, credentials, caches, databases, generated corpus data, local paths, and deployment URLs are installation-local and untracked. Never add them to repository files. `inspect` and normal `doctor` are read-only. `repair` previews by default and requires `--execute` to write. Build/update never deploy; deployment is an explicit configured public action. Browser BYOK values are page-memory only and never enter Web Storage, URLs, or static output.

Preview configuration migration before execution:

```bash
paper-curation migrate --config config.json
paper-curation migrate --config config.json --execute
```

Migration preserves recognized legacy local data paths and public URL values and reports unsupported values.

## Contributor integration contract

Work from a generic fork's `main`, then create a temporary integration branch. Classify each change before integration: generic algorithms, contracts, adapters, and synthetic fixtures may go upstream; operator-specific corpus, credentials, local paths, deployment settings, generated output, and person/topic/machine artifacts may not. Run contract and full gates before proposing integration. Never auto-merge generated corpus; review it separately as local operator output.

Do not create topic-, person-, or machine-named branches. Extend adapters or configuration extension points instead of embedding installation behavior. Add synthetic fixture tests for new adapters, configuration behavior, and contracts. Keep `AGENTS.md` and `CLAUDE.md` byte-identical after their headers.
