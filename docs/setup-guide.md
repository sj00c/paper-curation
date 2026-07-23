# Paper Curation — Setup Guide

Paper Curation 파이프라인의 설치 및 설정 가이드입니다.

## 사전 준비

시작하기 전에 Git, Node.js 18+, `conda`, Zotero API key, PDF가 들어 있는 Zotero 컬렉션, Google API key를 준비합니다. Claude 인증은 준비된 Claude Code OAuth 또는 Anthropic Console API key 중 하나면 됩니다. setup의 기본값 `auto`가 감지하며 특정 방식을 강제하지 않습니다. Java와 PaperBanana는 선택 기능이며 없으면 fallback 또는 기능 생략으로 처리합니다.

## 현재 체크아웃의 단일 하네스

현재 저장소의 Node 하네스는 내부/팀 milestone의 단일 진입점이며 외부 npm 패키지를 사용하지 않습니다. 스킬 설치는 Python 환경보다 먼저 독립적으로 실행됩니다. 공개 GitHub/npm release, 공개 scanner/license 정리, canonical upstream embedding merge는 연기되어 있으며 public-readiness를 주장하지 않습니다.

```bash
cd paper-curation

# 1) checkout 경로가 기록된 managed skill bundle 설치
node ./bin/paper-curation.mjs skill install

이 명령은 Claude Code의 `~/.claude/skills`, Codex의 `~/.codex/skills`, GJC의 `~/.gjc/agent/skills`를 모두 설치 대상으로 사용합니다. 대상별 unmanaged skill 충돌은 보존하고 건너뜁니다.

# 2) 비밀값을 shell history가 아닌 .env에 저장
cp .env.example .env
open -e .env                    # Linux: ${EDITOR:-vi} .env
```

```dotenv
ZOTERO_API_KEY=발급받은_Zotero_키
GEMINI_API_KEY=발급받은_Google_키
```

```bash
# 3) 현재 사용자 설정 생성
node ./bin/paper-curation.mjs setup --fresh-config

# 4) 인증·Zotero·Google·런타임 진단
node ./bin/paper-curation.mjs doctor --network --anthropic-smoke

# 5) setup이 출력한 alias 하나로 scratch smoke
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode smoke --source zotero --smoke-limit 1 --strict-pdf --no-deploy

# 6) 로컬 curate
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --no-deploy
```

`config.json`과 `.env`는 Git에서 제외되므로 다른 fork·worktree·사용자의 잔재일 수 있습니다. setup은 기존 config를 자동 신뢰하지 않습니다. 현재 사용자 것임을 검증한 경우에만 `setup --reuse-config`를 사용합니다. 새 설정은 Zotero 컬렉션을 하나 이상 선택받아 각 collection에 topic alias를 생성하며, alias는 임의의 Zotero 주제 프로필일 수 있습니다. fresh config는 secret-free이고 credential은 `.env` 또는 process env에서만 읽습니다.

Console API key를 강제할 때만 `.env`에 `ANTHROPIC_API_KEY`를 추가하고 다음을 실행합니다.

```bash
node ./bin/paper-curation.mjs setup --fresh-config --auth api-key
```

OAuth를 강제할 때만 `--auth oauth`를 사용합니다. `auto`는 준비된 OAuth/API key를 감지하지만 OAuth 토큰이나 API key를 config에 저장하지 않습니다. setup은 PaperBanana 같은 선택 저장소를 자동 clone하지 않습니다.

### 첫 프로덕션 실행 전 확인

smoke·진단·로컬 curate는 항상 `PAPER_CURATION_NO_DEPLOY=1`과 `--no-deploy`를 함께 사용합니다. 이 보호가 없는 production curate는 Cloudflare 자격증명이 설정되어 있으면 자동 publish할 수 있습니다. 배포는 사용자가 명시적으로 요청했을 때만 실행합니다.

```bash
node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode deploy
```

### Immutable release 이후

현재 첫 실행 문서는 checkout-local Node 하네스만 사용합니다. 내부 immutable tag/SHA 공지 이후에만 릴리스 노트의 고정 ref를 사용합니다. 공개 GitHub/npm 배포는 연기되어 있으며, ref 없는 GitHub NPX를 첫 설치 경로로 사용하지 않습니다.

## 수동 conda py312 fallback

<details>
<summary>NPX 없이 Python CLI로 직접 설치하기</summary>

### 1. 기존 checkout과 Dependencies

```bash
# 이미 받은 maintainer/fork/PR checkout 루트에서 실행합니다.
cd paper-curation
conda create -n py312 -c conda-forge python=3.12 pip -y
conda activate py312
pip install -r requirements.txt
```

### 2. Setup

```bash
# 실제 Zotero/Google 키는 shell history 대신 .env에 저장합니다.
cp .env.example .env
open -e .env
claude auth login
PYTHONUTF8=1 python pipeline/setup.py --anthropic-auth oauth --no-run

# API 키 과금 대안:
# 편집기로 .env에 ANTHROPIC_API_KEY를 추가한 뒤 실행합니다.
PYTHONUTF8=1 python pipeline/setup.py --anthropic-auth api-key --no-run
```

`setup.py`가 인터랙티브 설정 마법사를 실행하여 config.json 생성, Zotero 연결 테스트, SKILL.md 생성 및 설치를 수행합니다. 직접 실행할 때는 `--no-run`으로 비용이 드는 첫 파이프라인을 건너뜁니다. NPX에서 첫 실행까지 이어서 돌릴 때만 `--run-first`를 명시하세요.

스킬 설치를 건너뛰려면 `--no-install` 옵션을 사용하세요.

### config.json 직접 편집

설정 마법사 대신 직접 편집할 수도 있습니다:

```json
{
  "zotero": {
    "email": "your_email@example.com",
    "collections": {
      "my_topic": "My Zotero Collection Name"
    },
    "pdf_dir": "/path/to/your/zotero/pdfs"
  },
  "unpaywall_email": "your_email@example.com",
  "anthropic_auth": {
    "mode": "oauth"
  },
  "search_keywords": {
    "my_topic": {
      "primary": ["machine learning biology", "protein language model"],
      "secondary": ["single cell RNA", "drug target prediction"]
    }
  },
  "paperbanana_dir": "/path/to/paperbanana"
}
```

| Field | Description |
|-------|-------------|
| `anthropic_auth.mode` | 선택한 인증 방식(`auto`/`oauth`/`api-key`)의 비밀 없는 기록입니다. 토큰과 API key는 저장하지 않고 `claude auth login`, env-only `CLAUDE_CODE_OAUTH_TOKEN`, 또는 `.env`/process env의 `ANTHROPIC_API_KEY`를 사용합니다. |
| `email` | 이메일 (Zotero 및 Unpaywall용) |
| `collections` | Topic alias → Zotero 컬렉션 이름 매핑. 예: `my_topic`은 이후 `--topic my_topic`으로 쓰는 로컬 별칭입니다. Collection key는 Zotero API를 통해 자동 변환됩니다. |
| `pdf_dir` | Zotero PDF가 저장된 로컬 경로 |
| `search_keywords` | 토픽별 Core-1 검색 키워드 (`{topic: {primary: [...], secondary: [...]}}`). `primary` 매칭 0.5점, `secondary` 0.2점. 토픽은 저장소 예제가 아니라 현재 사용자가 선택한 Zotero collection alias입니다. fresh checkout에는 originality 평가 기본값이 내장되어 별도 trigger JSON이 필요 없습니다. (선택) |
| `paperbanana_dir` | [PaperBanana](https://github.com/dwzhu-pku/PaperBanana) clone 경로 (선택) |

### 환경변수 (선택)

API key와 경로 일부는 `.env` 또는 process env로 공급합니다. topic alias → Zotero 컬렉션 매핑 등 비밀이 아닌 설정만 `config.json`에 필요합니다. setup은 credential 값을 config에 저장하지 않습니다:

| 환경변수 | 용도 |
|----------|------|
| `ZOTERO_API_KEY` | Zotero API key |
| `ZOTERO_USER_ID` | Zotero user ID |
| `ZOTERO_DIR` | Zotero PDF 저장 경로 |
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code OAuth env-only token (`claude setup-token`). setup이 저장하지 않음 |
| `ANTHROPIC_API_KEY` | Anthropic Console API key (`--auth api-key`일 때만). OAuth 운영 셸에서는 우발 공존 방지 |
| `ANTHROPIC_AUTH_TOKEN` | Claude CLI gateway/bearer credential이며 구독 OAuth 토큰이 아닙니다. OAuth 모드에서는 unset |
| `GOOGLE_API_KEY` / `GEMINI_API_KEY` | Google AI key (검색 임베딩 `gemini-embedding-001`·Figure 검증·TTS — 필수) |
| `OPENAI_API_KEY` | OpenAI key (선택) |
| `RESEND_API_KEY` | Resend key (배포된 Audio Overview 이메일에만 필요, wrangler secret 으로도 등록) |
| `GITHUB_REPO` | GitHub repo (owner/repo) |
| `GITHUB_BRANCH` | Git branch (기본: master) |
| `PAGES_BASE_URL` | GitHub Pages base URL |

</details>

## 사용법

### Checkout-local Node CLI

메인 파이프라인. `--` 뒤 인자는 `pipeline/run_full.py`로 전달됩니다:

```bash
node ./bin/paper-curation.mjs doctor --network --anthropic-smoke
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode smoke --source zotero --smoke-limit 1 --strict-pdf --no-deploy
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --no-deploy
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source web --days 7 --max-papers 20 --no-deploy
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode reclassify --no-deploy
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode retime --images all --no-deploy
```
`--max-papers`는 `--source web`의 검색/등록 후보 수만 제한합니다. Zotero에 이미 있는 논문 review, 분류, timeline, index 같은 post-processing의 cap이 아닙니다. smoke/검증/repair-only/local 예시는 배포 억제를 반드시 함께 사용해야 합니다. 배포 억제 없는 production `curate`/`rebuild`/`reclassify`/`retime`은 Cloudflare 자격증명/설정이 있으면 자동 publish될 수 있습니다. 검색 인덱스/임베딩 cache metadata가 `pipeline/lib/search_index_metadata.py` 계약과 맞지 않으면 혼합하거나 자동 rebuild하지 않습니다(never auto-rebuilt). 명시적인 audit/migration/rebuild를 실행합니다.

Claude Code 스킬(`/paper-curation`)도 계속 사용할 수 있지만, 온보딩과 운영 문서의 표준 진입점은 checkout-local Node 하네스입니다.

### `/paper-curation-workflow`

파이프라인 워크플로우 다이어그램을 생성합니다.

```
/paper-curation-workflow                  # 5 candidates (기본)
/paper-curation-workflow --candidates=10  # 10 candidates
```

트리거: "workflow 만들어줘"

## Pipeline Scripts

단일 진입점은 `run_full.py` (3축 오케스트레이터)이고, 아래 개별 스크립트는 디버깅·복구용입니다. 모든 스크립트는 `pipeline/config_loader.py`를 통해 `config.json`을 읽습니다. 하드코딩된 인증 정보는 없습니다.

| Script | Purpose |
|--------|---------|
| `pipeline/config_loader.py` | 공유 설정: Zotero API key, User ID (자동), collection keys (자동) |
| `pipeline/sync_zotero.py` | Zotero에서 삭제/제목 변경 동기화 |
| `pipeline/run_update_force.py` | 배치 리뷰 생성 (PDF → 텍스트 → Figure → 리뷰) |
| `pipeline/build_papers_index.py` | 마스터 인덱스 재구축 |
| `pipeline/classify_papers.py` | 다중 카테고리 + 서브 카테고리 분류 |
| `pipeline/build_category_summaries.py` | 카테고리별 한국어 설명 생성 |
| `pipeline/generate_timelines.py` | Bottom-up 타임라인 생성 (Opus + PaperBanana) |
| `pipeline/review_to_html.py` | review.md → index.html 변환 |
| `pipeline/build_topic_index.py` | Topic 인덱스 페이지 생성 |
| `pipeline/prepare_deploy.py` | PNG→WebP 변환 + Cloudflare + gh-pages 배포 |

## PaperBanana (타임라인 생성용, 선택)

타임라인 이미지 생성에는 PaperBanana 계열 선택 dependency가 필요할 수 있습니다. 없어도 파이프라인은 정상 동작하며, 타임라인 이미지 생성만 건너뜁니다.

<details>
<summary>PaperBanana 설치 방법</summary>

PaperBanana 계열 선택 dependency는 각 프로젝트가 지원하는 immutable release tag/commit checkout을 사용하세요. 기본 브랜치를 그대로 clone하는 명령은 재현 가능한 설치가 아니므로 제공하지 않습니다. 준비한 뒤 PaperBanana 의존성을 설치합니다.

```bash
cd /path/to/paperbanana
pip install -r requirements.txt
```

`config.json`에 경로를 추가하세요:

```json
{
  "paperbanana_dir": "/path/to/paperbanana"
}
```

의존성 체인:
```
pipeline/generate_timelines.py
  → optional PaperBanana-compatible checkout (diagram generation)
```

</details>

## config.json 작동 원리

```
config.json
  ├── zotero.api_key     → 모든 Zotero API 호출
  ├── zotero.email       → Zotero 계정 식별
  ├── zotero.collections → Topic alias → Collection name
  │     ↓ (자동 변환)
  │   Zotero API: name → collection key
  │   Zotero API: api_key → user ID
  └── unpaywall_email    → Open Access PDF 조회
```

Collection key나 User ID는 직접 입력할 필요 없이 Zotero API를 통해 자동으로 조회됩니다. TLS 검증은 기본으로 켜져 있으며, 기업 프록시에서는 신뢰 CA를 설치하거나 `SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE`를 지정하세요. 임시 비보안 우회는 명명된 opt-out `PAPER_CURATION_INSECURE_TLS=1` 또는 `network.allow_insecure_tls`+`network.insecure_tls_reason`이 있을 때만 허용됩니다.

## 설치 확인 & 문제 해결

### 설치 확인 (verify)

긴 파이프라인 전에 인증·Python·패키지·Zotero 연결을 한 번에 확인하세요:

```bash
node ./bin/paper-curation.mjs doctor --network --anthropic-smoke
```

실행 계획만 확인하려면 deploy suppression을 명시합니다:

```bash
PAPER_CURATION_NO_DEPLOY=1 node ./bin/paper-curation.mjs run -- --topic <configured-topic> --mode curate --source zotero --dry-run --no-deploy
```

### 문제 해결 (Troubleshooting)

| 증상 / 에러 메시지 | 원인 | 해결 |
|---|---|---|
| `op_CALL_KW: pop from empty list` (numba 트레이스백) | `py312` env 밖에서 분류가 실행됨 | `conda activate py312` 후 재실행 |
| `ModuleNotFoundError: umap` / `hdbscan` / `sentence_transformers` | 의존성 누락 | env 활성화 후 `pip install -r requirements.txt` (umap-learn·hdbscan·sentence-transformers 포함) |
| Figure 품질이 낮음 / 표·구조가 깨짐 | Java 미설치로 PyMuPDF fallback | `brew install --cask temurin` (macOS) 후 재실행 |
| SPECTER2 / arXiv 다운로드가 멈춤 (한국 망) | huggingface LFS·arXiv 차단 | [operations.md "Korean network workarounds"](operations.md#korean-network-workarounds) 의 S3 미러 명령 사용 |
| `[COLLECTION_ERROR]` | Zotero 컬렉션 이름 오타 | 출력의 사용 가능한 컬렉션 목록에서 올바른 이름 선택 후 재실행 |
| 검색 인덱스가 빈 임베딩으로 빌드됨 | `GOOGLE_API_KEY` 미설정 | 편집기로 `.env`에 `GOOGLE_API_KEY`를 추가한 뒤 재실행 — 검색 임베딩은 Google `gemini-embedding-001` 사용 (OpenAI 키는 더 이상 필수 아님) |
| OAuth structured output 버전 오류 | Claude Code < 2.1.205 | `claude update` 후 `claude --version` 확인 |
| `Claude Code OAuth가 준비되지 않았습니다` | 구독 로그인이 없거나 만료됨 | `claude auth login` 또는 `claude setup-token` 후 `CLAUDE_CODE_OAUTH_TOKEN` 설정 |
