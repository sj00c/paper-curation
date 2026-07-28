# Paper Curation

Zotero 컬렉션의 논문을 **로컬에서** 검토하고 탐색하는 도구입니다. 생성된 대시보드는 secret-free이며, 브라우저가 API 키·OAuth 토큰·provider endpoint에 직접 연결하지 않습니다.

English: [README.en.md](README.en.md)

## 시작하기

Zotero API key, PDF가 든 컬렉션, 그리고 필요한 작업에 맞는 인증을 준비합니다. setup은 컬렉션을 수동으로 선택하게 하고 선택마다 topic alias를 만듭니다. alias는 `config.json`의 `zotero.collections`에 있는 값만 사용합니다.

```bash
node ./bin/paper-curation.mjs skill install
node ./bin/paper-curation.mjs setup --fresh-config
node ./bin/paper-curation.mjs doctor --network

# 제한된 read-only scratch smoke: 항상 두 suppressor를 함께 사용
PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 node ./bin/paper-curation.mjs run -- \
  --topic <alias> --mode smoke --source zotero --smoke-limit 1 --strict-pdf --no-deploy

# 일반 로컬 curate: 항상 두 suppressor를 함께 사용
PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 node ./bin/paper-curation.mjs run -- \
  --topic <alias> --mode curate --source zotero --no-deploy

# 정확한 loopback 서버
node ./bin/paper-curation.mjs serve --topic <alias> [--port N]
```

`.env` 또는 process environment로 credential을 공급합니다. fresh `config.json`과 생성 대시보드에는 secret을 쓰지 않습니다. `setup --reuse-config`는 기존 설정과 Zotero 계정이 현재 사용자 것임을 확인한 뒤에만 사용합니다.

## 인증·작업 승인

인증은 작업마다 서버가 판정합니다. `--auth auto`는 준비된 **OAuth만** 선택하며 API key로 fallback하지 않습니다. API key는 `--auth api-key`를 명시한 해당 작업에서만 사용합니다. `--auth oauth`는 OAuth만 요구합니다. credential은 config, dashboard, browser storage에 저장하거나 노출하지 않습니다.

대시보드는 localhost server에서 exact provider/model/work/maxima/cost plan을 만들 수 있지만, 이 checkout에는 trusted worker adapter가 없으므로 bootstrap이 `DISPATCH_UNAVAILABLE`을 선언하고 action 버튼을 disabled 상태로 유지합니다. start 요청도 approval을 소비하기 전에 HTTP 503으로 fail-closed합니다.

## 검색과 Audio

검색은 기존 snapshot을 읽기만 하는 BM25+dense hybrid retrieval이며 RRF의 후보 K는 60입니다. dense가 없거나 사용할 수 없으면 lexical 검색으로 downgrade하며, 이 요청이 index를 rebuild하거나 외부 검색·Zotero 등록을 시작하지는 않습니다.

Audio Overview는 선택 기능입니다. Gemini 인증이 없으면 UI는 숨김/disabled의 비오류 상태가 되고 Gemini 호출, probe, 다른 provider fallback을 전혀 하지 않습니다. Gemini 인증이 있어도 trusted worker adapter가 없는 현재 checkout에서는 action capability가 disabled입니다. Audio plan은 Gemini 전용 exact models와 근사 요청 길이, 3,600초 hard actual maximum을 결속합니다.

## Zotero와 범위

Zotero onboarding은 수동 collection 선택과 명시된 alias에서 시작합니다. scratch smoke는 bounded·read-only이며 Zotero 항목을 등록·수정·삭제하지 않습니다. 이 제품은 telemetry를 보내지 않고, 개인 메모/개인 데이터 수집, 강의 처리, 일정 관리 기능을 제공하지 않습니다.

## 배포와 소스 전달

일반 `run` 명령은 product deployment를 승인하거나 실행하지 않습니다. `run --mode deploy`는 지원되지 않습니다. 이 checkout에는 신뢰할 수 있는 deployment approval issuer/executor가 없으므로 실제 배포는 fail-closed로 거부되며, 다음 명령은 정확한 topic scope를 미리 보는 dry-run만 제공합니다.

```bash
node ./bin/paper-curation.mjs deploy --topic <alias> --dry-run
```

소스 변경의 GitHub PR 전달은 코드 리뷰용 소스 delivery이며 product deployment와 별개입니다. 이 문서는 live provider, deployment 또는 비용 발생 테스트를 실행했다는 주장을 하지 않습니다.

자세한 내용: [설정 안내](docs/setup-guide.md), [운영](docs/operations.md), [아키텍처](docs/architecture.md).
