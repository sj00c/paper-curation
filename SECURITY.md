# Security Policy

## Reporting

Report a suspected vulnerability privately through the repository host's security-advisory channel. Never include keys, tokens, private paper text, generated corpus, or personal data in a public report.

## Local-first boundaries

- `config.json`, `.env`, credential caches, databases, PDF caches, generated corpus data, and deployment values are local and untracked.
- Setup is configuration-only; inspection and default doctor are read-only.
- Build and update do not deploy, notify, repair remote data, or synchronize remote bibliography data implicitly.
- Repair previews changes by default and requires `--execute`; public deployment requires the separate `deploy` command and an explicit configured destination.
- Configuration migration is previewed before explicit execution. It preserves recognized legacy local paths and public URL values and reports unsupported values.

## Credential and browser handling

- Static rendered output must not contain owner API keys or notification recipients.
- Browser BYOK credentials are memory-only for one page load. They are not persisted in Web Storage or included in URLs.
- Browser requests may use same-origin server routes; server credentials remain at that configured boundary.
- TLS certificate and hostname verification remain enabled. Private CAs use `PAPER_CURATION_CA_BUNDLE`.
- `scripts/scan-secrets.py` scans current Git objects and reachable history; rotate any credential ever committed.

Install the optional hook and scan manually:

```bash
bash scripts/install-hooks.sh
python scripts/scan-secrets.py --all
python scripts/scan-secrets.py --history
```

A clean current snapshot does not make historical exposure safe; revoke and rotate exposed credentials.
