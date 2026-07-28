# 아키텍처

## 신뢰 경계

`node ./bin/paper-curation.mjs serve --topic <alias> [--port N]`는 정확히 `127.0.0.1` loopback에만 bind합니다. 생성된 HTML dashboard는 secret-free이며 API key, OAuth token, provider endpoint를 browser에 전달하거나 browser에서 직접 호출하지 않습니다. 이 checkout은 trusted worker adapter가 없어 bootstrap에서 `DISPATCH_UNAVAILABLE`을 선언하고 action 버튼을 disabled 상태로 유지합니다.

서버는 action마다 auth를 판정합니다. `auto`는 OAuth-only이며 API key를 fallback으로 사용하지 않습니다. API key는 명시적 `api-key` action에서만, OAuth는 `oauth` action에서만 허용합니다. credential은 config, dashboard, browser storage에 보관하지 않습니다.

## Action plan과 approval

각 action은 immutable scope를 가진 plan을 먼저 생성합니다. scope에는 입력/리소스 digest, ingress, action, provider와 model, work, maxima, external allowlist, cost가 포함됩니다. UI는 provider, model, work, maxima, 그리고 estimated 또는 unavailable cost를 preview합니다.

approval은 plan scope에만 묶인 single-use credential입니다. 60초 뒤 만료되며 input, provider, model, work, maxima, cost가 달라지면 fail-closed합니다. 현재 checkout의 start는 trusted worker adapter가 없어 approval을 redeem하기 전에 HTTP 503 `DISPATCH_UNAVAILABLE`을 반환합니다.

## Corpus와 retrieval

setup은 Zotero collection을 사용자가 수동 선택하도록 하고 선택마다 local topic alias를 생성합니다. alias는 `config.json`의 `zotero.collections`에서만 해석됩니다. fresh config는 secret-free이며 기존 config는 사용자가 소유를 확인했을 때만 reuse합니다.

scratch smoke는 bounded read-only Zotero 작업이다. Zotero item을 search/register/sync/write/delete하지 않습니다. corpus retrieval도 read-only입니다: BM25와 dense retrieval을 RRF로 합치며 candidate K=60을 사용합니다. dense path가 없거나 실패하면 lexical retrieval로 downgrade하고, 질의 자체가 index rebuild, external search 또는 Zotero registration을 유발하지 않습니다.

## Audio capability

Audio Overview capability는 Gemini-only입니다. Gemini credential이 없으면 UI는 hidden/disabled의 non-error 상태가 되며 Gemini request, provider probe, 또는 다른 provider fallback을 전혀 하지 않습니다. Gemini credential이 있어도 trusted worker adapter가 없는 현재 checkout에서는 action capability가 disabled입니다.

Audio plan은 Gemini provider/model, source digest, requested duration, speaker/language 등의 work, maxima, cost를 결속합니다. requested duration은 근사 목표이다. 실제 decoded/playable duration은 검증되어 3,600초보다 큰 결과를 거부합니다.

## CLI와 deployment 분리

일반 orchestration은 `run --` passthrough로 수행하되 ordinary command에는 `PAPER_CURATION_NO_DEPLOY=1`, `PAPER_CURATION_NO_VECTOR_REBUILD=1`, `--no-deploy`를 모두 붙입니다. `run --mode deploy`는 CLI가 거부합니다. product deployment는 일반 run의 결과나 approval으로 자동 실행되지 않습니다.

이 checkout이 제공하는 deployment 관련 CLI surface는 정확한 topic scope의 dry-run preview뿐입니다.

```bash
node ./bin/paper-curation.mjs deploy --topic <alias> --dry-run
```

이 checkout에는 신뢰할 수 있는 deployment approval issuer/executor가 없으므로 실제 배포는 fail-closed로 거부됩니다. GitHub PR은 소스 변경을 review/delivery하는 경로일 뿐 product deployment가 아닙니다.

## 명시적 비기능 범위

이 제품은 telemetry를 전송하지 않습니다. personal-data 또는 personal-note collection, lecture processing, scheduling 기능은 설계 범위 밖입니다. 이 문서는 live provider 실행, 실제 product deployment, 또는 비용 발생 테스트가 수행되었다고 주장하지 않습니다.

## Locked intent traceability

- `artifact:curation-core`: 임의의 configured topic alias에서 재현 가능한 local curation 산출물을 만든다.
- `artifact:retrieval`: metadata compatibility를 검증한 read-only BM25/dense RRF retrieval을 제공한다.
- `artifact:security-compliance`: TLS, secret scan, static-asset/license, provenance 경계를 fail-closed로 검증한다.
- `surface:cli`: install/setup/doctor/run/smoke/serve와 preview-only deploy를 checkout-local CLI로 제공한다.
- `surface:generated-site`: exact-loopback localhost dashboard를 정상 제공 surface로 사용한다.
- `surface:agent-skills`: Claude Code, Codex, GJC에 동일한 9개 managed skills를 생성한다.
- `integration:zotero`: 수동 선택한 Zotero collection과 configured alias만 입력 경계로 사용한다.
- `integration:upstream`: 전체 merge/rebase 대신 auditable selective reimplementation만 허용한다.
- `integration:providers`: env-first auth와 operation-scoped provider/model/work/maxima/cost approval을 요구한다.
- `constraint:no-deploy-default`: 일반 실행은 deploy/vector rebuild를 억제하고 product deploy는 unavailable로 거부한다.
- `constraint:secure-defaults`: insecure TLS, stale metadata, malformed authority는 우회 없이 거부한다.
- `constraint:domain-agnostic`: 특정 topic, corpus, 개인 운영 환경을 기본값으로 포함하지 않는다.
- `constraint:no-upstream-copy`: 검증되지 않은 upstream source/evaluation data를 복사하지 않는다.
