# 운영 계약

## 명령 경계

| 목적 | 정식 명령 | 계약 |
|---|---|---|
| topic 확인 | `node ./bin/paper-curation.mjs topic` | setup이 생성한 alias만 사용 |
| bounded scratch | `PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 node ./bin/paper-curation.mjs run -- --topic <alias> --mode smoke --source zotero --smoke-limit 1 --strict-pdf --no-deploy` | read-only, bounded, Zotero write/register/delete 없음 |
| 일반 로컬 curate | `PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 node ./bin/paper-curation.mjs run -- --topic <alias> --mode curate --source zotero --no-deploy` | deploy와 vector rebuild suppressor가 항상 필요 |
| 대시보드 | `node ./bin/paper-curation.mjs serve --topic <alias> [--port N]` | 정확히 `127.0.0.1` loopback |
| product deployment preview | `node ./bin/paper-curation.mjs deploy --topic <alias> --dry-run` | 정확한 topic scope만 표시하며 실제 배포는 fail-closed로 거부 |

일반 `run`은 deploy를 승인하거나 실행하지 않으며 `run --mode deploy`는 지원되지 않습니다. PR로 소스 변경을 전달하는 것은 product deployment와 다릅니다.

## localhost action protocol

생성 dashboard에는 secret이 없고 browser-direct credential/provider 호출이 없습니다. localhost server는 exact provider/model/work/maxima/cost plan을 만들 수 있지만, 이 checkout에는 trusted worker adapter가 없으므로 bootstrap에서 `DISPATCH_UNAVAILABLE`을 선언하고 Normal/Deeper/Audio action을 disabled 상태로 유지합니다.

1. 브라우저가 exact-loopback bootstrap capability를 받는다.
2. 서버가 action auth와 scope-bound plan을 만들 수 있다.
3. plan은 provider, model, work, maxima, cost(`PRICE_UNAVAILABLE`)를 preview한다.
4. 현재 checkout의 start는 approval을 소비하기 전에 HTTP 503 `DISPATCH_UNAVAILABLE`로 fail-closed한다.

입력 digest, provider, model, work, maxima 또는 cost가 변하면 plan scope가 달라집니다. approval 만료·재사용·scope 변화는 fail-closed입니다. auth도 action별입니다: `auto`는 OAuth-only이고 API-key fallback이 없으며, API key는 명시적 `api-key` action에서만 사용합니다.

## Retrieval

질의는 기존 corpus snapshot에 대한 read-only retrieval입니다. BM25와 dense 후보를 RRF로 융합하고 candidate K=60을 사용합니다. dense가 이용 불가하면 lexical-only로 downgrade합니다. 질의는 index rebuild, provider fallback, 웹 검색, Zotero registration을 시작하지 않습니다.

## Audio Overview

Audio capability는 Gemini-only입니다. Gemini auth가 없으면 hidden/disabled non-error 상태이며 zero provider calls, probes, 또는 fallback입니다. Gemini auth가 있더라도 이 checkout은 trusted worker adapter가 없어 action capability를 disabled 상태로 유지합니다. Audio plan은 requested duration, exact script/TTS models, work, maxima, `PRICE_UNAVAILABLE`을 포함하며, duration은 근사 목표이고 실제 playable output의 hard maximum은 3,600 seconds입니다.

## Zotero onboarding과 비기능 범위

setup은 Zotero collections를 자동 선택하지 않습니다. 사용자가 collection을 고르고 각 선택에 alias를 부여합니다. scratch 작업은 bounded read-only입니다. 제품은 telemetry를 전송하지 않으며 개인 데이터/개인 메모 수집, lecture processing, scheduling을 제공하지 않습니다.

## 배포 운영

이 checkout의 dedicated `deploy` surface는 `--dry-run` preview만 지원합니다. 신뢰할 수 있는 deployment approval issuer/executor가 없으므로 실제 배포는 fail-closed로 거부됩니다. 일반 smoke, curate, verify, repair 명령은 deploy/vector-rebuild suppressor를 계속 유지합니다. 이 문서는 provider 호출, 실제 배포, 또는 비용 발생 검증을 실행했다는 기록이 아닙니다.
