---
name: paper-curation
description: "Compatibility router for the managed paper-curation skill bundle. Triggers: 논문 큐레이션, 최신 논문 찾아줘, Zotero 논문 리뷰해줘, paper curation, curate papers, paper-curation 설치, paper-curation 진단, paper-curation 배포."
---
<!-- paper-curation-managed-skill -->

# Paper Curation Router

This compatibility skill routes all work through the managed paper-curation skills installed from this checkout. Use the checkout-local Node CLI harness as the only orchestration boundary; do not reproduce pipeline phases in the agent, call internal Python scripts directly, depend on other skills outside this bundle, or assume a topic, credential mode, repository owner, deployment target, or fork state.

Checkout recorded when this router was installed:

```text
/Users/sj/dev/paper-curation
```

Resolve the checkout before every run:

1. Use the recorded path when it still contains `bin/paper-curation.mjs` and `pipeline/setup.py`.
2. Otherwise locate the user's current paper-curation checkout.
3. Run all commands from that checkout.

Managed skill ids installed by `node ./bin/paper-curation.mjs skill install`:

```text
paper-curation, paper-curation-router, paper-curation-setup, paper-curation-doctor, paper-curation-topic, paper-curation-search-register, paper-curation-curate-review, paper-curation-smoke, paper-curation-deploy
```

## Router policy

- For installation or first-use bootstrap, follow `paper-curation-setup`.
  Bootstrap command: `PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs setup --fresh-config`.
- For health checks, follow `paper-curation-doctor`.
  Use `PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs doctor --network`.
- For configured exact topic aliases, follow `paper-curation-topic`.
  Use `PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs topic`.
- For recent-paper search and Zotero registration, follow `paper-curation-search-register`.
- For local Zotero review or curation, follow `paper-curation-curate-review`.
- For bounded local verification, follow `paper-curation-smoke`.
- For localhost viewing, use `PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs serve --topic <topic>`.
- For product-deploy scope preview only, follow `paper-curation-deploy`.
  Its only command is `node ./bin/paper-curation.mjs deploy --topic <topic> --dry-run`; actual deployment is unavailable and fails closed.

The harness uses only Node.js built-ins. Python packages are pipeline runtime dependencies and are installed by `setup`, not prerequisites for installing or loading this skill.

Do not hardcode any example topic alias. Use only exact keys printed from `zotero.collections` by `PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs topic`.

Never expose `.env`, API keys, OAuth tokens, or credential-bearing command lines. For smoke, preview, repair, search/register, and ordinary local curation, keep `PAPER_CURATION_NO_DEPLOY=1`, `PAPER_CURATION_NO_VECTOR_REBUILD=1`, and `--no-deploy`. This checkout has no trusted deployment executor.

Before any provider action, show the provider, model, work, maxima, and cost; obtain fresh approval scoped to that operation. `auto` is OAuth-only. An API key is used only for an explicit approved action. Do not substitute a provider automatically. When Gemini Audio is unavailable, hide and disable it, make zero calls, and keep core curation safe.
