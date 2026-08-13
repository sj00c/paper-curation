# Contributing

## Upstream integration

Start from a generic fork's `main` and create a temporary integration branch. Keep the branch narrowly scoped and remove it after the integration decision.

Classify changes before proposing them upstream:

- **Upstream candidates:** generic algorithms, domain/application contracts, reusable adapters, configuration extension points, rendering resources, and synthetic fixtures.
- **Operator-specific artifacts:** corpus data, generated pages, credentials, local paths, public URLs, deployment settings, machine assumptions, and topic/person-specific rules. Keep these local; do not submit or auto-merge them.

Run the contract gate and the full gate required by the repository before requesting integration. Generated corpus is never auto-merged, even when a gate passes; it requires a separate operator review.

## Design rules

Do not use topic-, person-, or machine-named branches. Do not encode installation-specific behavior in generic code. Add or extend an adapter or configuration extension point instead. Keep dependencies directed inward: domain code must not depend on the CLI, integrations, or rendering.

Changes to adapters, configuration, or contracts require synthetic fixture tests that cover normal behavior, invalid input, and the intended side-effect boundary. Do not use private corpus data, secrets, or live production services as fixtures.

## User interface

The official interface is the installed `paper-curation` CLI: `setup`, `inspect`, `doctor`, `build`, `update`, `serve`, `query`, `validate`, `repair`, and `deploy`. Preserve the declarative side-effect policy: inspection is read-only, repair requires explicit execution, and deployment is separate from build/update. `pipeline/run_full.py` remains only as a compatibility wrapper for existing callers.
