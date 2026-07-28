# 설정 안내

## 경계와 준비물

이 도구는 로컬 loopback 서버와 명시한 Zotero topic alias로 동작합니다. Node.js와 Zotero API key, PDF가 있는 Zotero 컬렉션, 그리고 필요한 action의 인증을 준비합니다. credential은 `.env` 또는 process environment에만 두고 shell history, `config.json`, 생성 HTML에 넣지 않습니다.

```dotenv
ZOTERO_API_KEY=your_zotero_key
# Gemini Audio를 실제로 사용할 때만 Gemini credential을 설정합니다.
GEMINI_API_KEY=your_gemini_key
```

## 수동 onboarding

```bash
node ./bin/paper-curation.mjs skill install
node ./bin/paper-curation.mjs setup --fresh-config
node ./bin/paper-curation.mjs topic
```

setup은 사용자에게 Zotero collection을 수동 선택하게 하고 선택별 alias를 생성합니다. alias는 문서 예제나 기본값으로 정하지 않으며 `config.json`의 `zotero.collections`에서 확인합니다. fresh config는 secret-free입니다. 기존 ignored config를 자동 신뢰하지 않으므로, 현재 사용자와 Zotero account의 설정임을 확인한 경우에만 `--reuse-config`를 사용합니다.

`--auth auto`는 준비된 OAuth만 선택합니다. API key가 있더라도 `auto`가 API key로 fallback하지 않습니다. API key 사용은 해당 action에서 `--auth api-key`를 명시할 때만 가능하며 `--auth oauth`는 OAuth만 요구합니다.

## 진단과 안전한 로컬 실행

```bash
node ./bin/paper-curation.mjs doctor --network

# bounded, read-only scratch 작업
PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 node ./bin/paper-curation.mjs run -- \
  --topic <alias> --mode smoke --source zotero --smoke-limit 1 --strict-pdf --no-deploy

# 일반 로컬 작업
PAPER_CURATION_NO_DEPLOY=1 PAPER_CURATION_NO_VECTOR_REBUILD=1 node ./bin/paper-curation.mjs run -- \
  --topic <alias> --mode curate --source zotero --no-deploy
```

모든 일반 `run` 명령에는 `PAPER_CURATION_NO_DEPLOY=1`, `PAPER_CURATION_NO_VECTOR_REBUILD=1`, `--no-deploy`를 함께 사용합니다. scratch smoke는 제한된 read-only 작업이며 Zotero에 register/write/delete하지 않습니다. `run --mode deploy`는 거부됩니다.

## 대시보드 서버

```bash
node ./bin/paper-curation.mjs serve --topic <alias> [--port N]
```

서버는 정확히 `127.0.0.1`에서만 제공됩니다. 생성 대시보드는 secret-free이고 browser-direct provider 호출을 하지 않습니다. 서버는 exact provider/model/work/maxima/cost plan을 만들 수 있지만 trusted worker adapter가 없으므로 bootstrap에서 `DISPATCH_UNAVAILABLE`을 선언하고 action을 disabled 상태로 유지합니다. start도 approval을 소비하기 전에 HTTP 503으로 거부됩니다.

## 선택 Audio Overview

Audio는 Gemini 전용의 선택 기능입니다. Gemini auth가 없으면 disabled/hidden의 비오류 상태가 되며 provider call, capability probe, fallback을 실행하지 않습니다. Gemini auth가 있어도 trusted worker adapter가 없는 현재 checkout에서는 action capability가 disabled입니다. plan은 요청 duration을 근사 목표로, 실제 재생 길이는 3,600초를 hard maximum으로 결속합니다.

## 배포

product deployment는 일반 실행이나 이 안내의 smoke/curate에 포함되지 않습니다. 이 checkout에는 신뢰할 수 있는 deployment approval issuer/executor가 없으므로 실제 배포는 fail-closed로 거부되며, 다음 명령은 정확한 topic scope의 dry-run preview만 제공합니다.

```bash
node ./bin/paper-curation.mjs deploy --topic <alias> --dry-run
```

GitHub PR은 source change delivery/review이지 product deployment가 아닙니다. 이 안내는 live provider, deployment, 또는 비용 발생 테스트가 수행되었다고 주장하지 않습니다.
