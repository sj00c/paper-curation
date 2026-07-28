# Paper Curation

A **local** tool for reviewing and exploring papers in Zotero collections. Generated dashboards are secret-free: the browser never connects directly to API keys, OAuth tokens, or provider endpoints.

Korean: [README.md](README.md)

## Quick start

Prepare a Zotero API key, a collection containing PDFs, and authentication for the action being requested. Setup asks the user to select collections manually and creates one topic alias per selection. Only aliases in `config.json` under `zotero.collections` are valid.

```bash
node ./bin/paper-curation.mjs skill install
node ./bin/paper-curation.mjs setup --fresh-config
node ./bin/paper-curation.mjs doctor --network

# Bounded, read-only scratch smoke: always use both suppressors
PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 node ./bin/paper-curation.mjs run -- \
  --topic <alias> --mode smoke --source zotero --smoke-limit 1 --strict-pdf --no-deploy

# Ordinary local curation: always use both suppressors
PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 node ./bin/paper-curation.mjs run -- \
  --topic <alias> --mode curate --source zotero --no-deploy

# Exact loopback server
node ./bin/paper-curation.mjs serve --topic <alias> [--port N]
```

Supply credentials through `.env` or the process environment. A fresh `config.json` and generated dashboard contain no secrets. Use `setup --reuse-config` only after confirming that the existing configuration and Zotero account belong to the current user.

## Authentication and action approval

The server resolves authentication per action. `--auth auto` selects a ready **OAuth** credential only; it never falls back to an API key. An API key is used only by the action explicitly requested with `--auth api-key`. `--auth oauth` requires OAuth. Credentials are not stored or exposed in configuration, dashboards, or browser storage.

The dashboard can produce an exact provider/model/work/maxima/cost plan through the localhost server, but this checkout has no trusted worker adapter. Bootstrap therefore declares `DISPATCH_UNAVAILABLE`, action controls remain disabled, and start fails with HTTP 503 before consuming approval.

## Retrieval and Audio

Retrieval is read-only over the existing snapshot: BM25+dense hybrid retrieval with RRF candidate K=60. If dense retrieval is unavailable, it downgrades to lexical retrieval. A query never rebuilds the index or initiates web search or Zotero registration.

Audio Overview is optional. Without Gemini authentication it is hidden/disabled as a non-error and makes zero Gemini calls, probes, or provider fallbacks. Even with Gemini authentication, the action capability remains disabled in this checkout because no trusted worker adapter is present. Audio plans bind the exact Gemini models, approximate requested duration, and a 3,600-second hard actual maximum.

## Zotero and product boundaries

Zotero onboarding begins with manual collection selection and an explicit alias. Scratch smoke is bounded and read-only: it does not register, modify, or delete Zotero items. The product has no telemetry, personal-note/personal-data collection, lecture processing, or scheduling feature.

## Deployment versus source delivery

Ordinary `run` commands neither authorize nor execute product deployment. `run --mode deploy` is unsupported. This checkout has no trusted deployment approval issuer or executor, so product deploy execution is unavailable and fails closed; the command below only previews an exact topic scope:

```bash
node ./bin/paper-curation.mjs deploy --topic <alias> --dry-run
```

A GitHub PR that delivers source changes is source delivery for review, not product deployment. This documentation does not claim that live-provider, deployment, or cost-incurring tests were run.

See [setup guide](docs/setup-guide.md), [operations](docs/operations.md), and [architecture](docs/architecture.md).
