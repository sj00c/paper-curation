# Paper Curation — Setup Guide

Paper Curation 파이프라인의 설치 및 설정 가이드입니다.

## 사전 준비

시작하기 전에 아래 항목을 준비하세요:
- Git, Node.js **18 이상**, `conda` 명령(Miniconda 또는 Miniforge) — NPX가 `py312` 환경과 Python 의존성을 설치합니다.

- [Claude Code](https://claude.ai/code) **2.1.205 이상** 설치
- Claude 인증 방식 선택
  - **구독 OAuth (권장)** — Claude Pro/Max/Team/Enterprise. `claude auth login`으로 로그인하거나 `claude setup-token`으로 받은 env-only `CLAUDE_CODE_OAUTH_TOKEN`을 사용합니다.
  - **Console API 키** — Anthropic Console metered API 과금. `ANTHROPIC_API_KEY`를 쓰고 NPX/setup에서 `--auth api-key`를 명시합니다.
- [Zotero API Key](https://www.zotero.org/settings/keys) 발급, Zotero 컬렉션 이름 확인, Zotero PDF 저장 경로 확인
- `GOOGLE_API_KEY` — 검색 임베딩 `gemini-embedding-001`·Figure 검증·TTS에 **필수**
- `OPENAI_API_KEY` — 선택
- `RESEND_API_KEY` — 배포된 Audio Overview 이메일에만 필요
- Java Runtime — `opendataloader-pdf` 가 Java CLI 래퍼. macOS: `brew install --cask temurin`. 없으면 PyMuPDF 로 자동 fallback (표/구조 추출 품질 ↓).

> OAuth 토큰은 setup이 저장하지 않습니다. `config.json`에는 `anthropic_auth.mode = "oauth"`만 저장할 수 있습니다. Claude CLI 자체는 API 키를 OAuth보다 우선할 수 있으므로 OAuth 운영 셸에서는 `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`을 unset하는 편이 안전합니다. 이 저장소는 OAuth로 선택된 Claude child 호출에서 두 API 자격증명을 제거하고, `auto` 모드에서는 OAuth token/login을 API 키보다 우선합니다.

## NPX 설치 (권장)

### 새 클론 + 온보딩

```bash
npx --yes github:jehyunlee/paper-curation init --auth oauth --dir paper-curation
```

### 이미 체크아웃한 저장소

```bash
npx . setup --auth oauth
```
> **중요:** `config.json`은 로컬 비밀 설정이라 Git에 포함되지 않으며 `clone`/`pull`로 생성되지 않습니다. 가장 쉬운 방법은 export 없이 setup을 실행하고 프롬프트에 Zotero API key를 붙여 넣는 것입니다.
>
> ```bash
> cd ~/dev/paper-curation
> npx . setup --auth oauth
> ```
>
> `export`는 선택사항이며 파일을 만들지 않습니다. 사용할 경우 같은 터미널에서 setup까지 실행합니다. setup은 Zotero API로 컬렉션을 조회해 번호 선택을 받고, topic alias와 `pdf_cache/`를 자동 생성합니다.

### 파일로 한 번에 입력 (`.env`, 권장)

터미널 export 대신 편집 가능한 템플릿을 복사할 수 있습니다:

```bash
cp .env.example .env
open -e .env                    # 또는 원하는 편집기로 .env 열기
npx . setup --auth oauth
```

`.env.example`에는 실제로 필요한 API key 두 개만 있습니다:

```dotenv
ZOTERO_API_KEY=
GEMINI_API_KEY=
```

Claude는 저장된 `claude auth login` 구독 세션을 사용하므로 `ANTHROPIC_API_KEY`는 필요하지 않습니다. `.env`는 Git에서 제외됩니다. setup은 컬렉션을 자동 조회하고 프로젝트의 `pdf_cache/`를 생성합니다. Zotero Storage에 동기화된 PDF는 실행 중 API로 자동 다운로드합니다. Zotero Storage에 없는 로컬 linked attachment만 사용할 때는 `.env`에 `ZOTERO_DIR=/linked/attachment/path`를 고급 override로 추가합니다.

### Anthropic Console API 키 과금 대안

```bash
export ANTHROPIC_API_KEY=your_key
npx . setup --auth api-key
```

NPX setup은 config.json 생성, Zotero 연결 테스트, PaperBanana 확인, SKILL.md 설치 안내를 수행합니다. 기본값으로는 비용이 드는 파이프라인을 자동 실행하지 않습니다. 첫 실행까지 이어서 돌릴 때만 `--run-first`를 명시하세요.
`npx . doctor --network`는 OAuth(`claude auth login`/`CLAUDE_CODE_OAUTH_TOKEN`) 또는 API 키(`ANTHROPIC_API_KEY`) 중 현재 선택한 Claude 인증과 Zotero/Google 연결을 진단합니다.

진단과 실행:

```bash
npx . doctor --network
npx . run -- --topic my_topic --mode curate --source zotero
```

## 수동 conda py312 fallback

<details>
<summary>NPX 없이 Python CLI로 직접 설치하기</summary>

### 1. Clone & Dependencies

```bash
git clone https://github.com/jehyunlee/paper-curation.git
cd paper-curation
conda create -n py312 -c conda-forge python=3.12 pip -y
conda activate py312
pip install -r requirements.txt
```

### 2. Setup

```bash
# OAuth: 저장된 로그인 또는 env-only 장기 토큰
claude auth login
# 장기 토큰이 필요하면 발급 후 출력된 토큰을 env에 설정
claude setup-token
export CLAUDE_CODE_OAUTH_TOKEN='발급된_토큰'

export GOOGLE_API_KEY=your_key
export ZOTERO_API_KEY=your_key
PYTHONUTF8=1 python pipeline/setup.py --anthropic-auth oauth --no-run

# API 키 대안
export ANTHROPIC_API_KEY=your_key
PYTHONUTF8=1 python pipeline/setup.py --anthropic-auth api-key --no-run
```

`setup.py`가 인터랙티브 설정 마법사를 실행하여 config.json 생성, Zotero 연결 테스트, SKILL.md 생성 및 설치를 수행합니다. 직접 실행할 때는 `--no-run`으로 비용이 드는 첫 파이프라인을 건너뜁니다. NPX에서 첫 실행까지 이어서 돌릴 때만 `--run-first`를 명시하세요.

스킬 설치를 건너뛰려면 `--no-install` 옵션을 사용하세요.

### config.json 직접 편집

설정 마법사 대신 직접 편집할 수도 있습니다:

```json
{
  "zotero": {
    "api_key": "your_zotero_api_key",
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
| `api_key` | Zotero API key ([Settings → Feeds/API](https://www.zotero.org/settings/keys)) |
| `anthropic_auth.mode` | OAuth 선택 기록용 `oauth`만 저장합니다. 토큰은 저장하지 않고 `claude auth login` 또는 env-only `CLAUDE_CODE_OAUTH_TOKEN`을 사용합니다. API-key 모드는 `--auth api-key`와 `ANTHROPIC_API_KEY` 또는 최상위 `anthropic_api_key`로 동작합니다. |
| `email` | 이메일 (Zotero 및 Unpaywall용) |
| `collections` | Topic alias → Zotero 컬렉션 이름 매핑. Collection key는 Zotero API를 통해 자동 변환됩니다. |
| `pdf_dir` | Zotero PDF가 저장된 로컬 경로 |
| `search_keywords` | 토픽별 Core-1 검색 키워드 (`{topic: {primary: [...], secondary: [...]}}`). `primary` 매칭 0.5점, `secondary` 0.2점. `ai4s`/`scisci` 는 빌트인 기본값이 있어 생략 가능하고, 그 외 신규 토픽은 여기에 추가합니다. (선택) |
| `paperbanana_dir` | [PaperBanana](https://github.com/dwzhu-pku/PaperBanana) clone 경로 (선택) |

### 환경변수 (선택)

API key와 경로 일부는 환경변수로 공급할 수 있습니다. 다만 topic alias → Zotero 컬렉션 매핑 등은 `config.json`에 필요합니다. setup을 실행하면 현재 셸의 필수 환경변수를 읽어 Git에서 제외된 로컬 `config.json`에 저장합니다:

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

### NPX CLI

메인 파이프라인. `--` 뒤 인자는 `pipeline/run_full.py`로 전달됩니다:

```bash
npx . doctor --network
npx . run -- --topic my_topic --mode curate --source zotero
npx . run -- --topic my_topic --mode curate --source web --days 7
npx . run -- --topic my_topic --mode reclassify
npx . run -- --topic my_topic --mode retime --images all
```

Claude Code 스킬(`/paper-curation`)도 계속 사용할 수 있지만, 온보딩과 운영 문서의 표준 진입점은 NPX입니다.

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

타임라인 생성에는 PaperBanana와 scisci 래퍼가 필요합니다. 없어도 파이프라인은 정상 동작하며, 타임라인 생성만 건너뜁니다.

<details>
<summary>PaperBanana 설치 방법</summary>

```bash
# 1. PaperBanana 클론
git clone https://github.com/dwzhu-pku/PaperBanana.git /path/to/paperbanana
cd /path/to/paperbanana
pip install -r requirements.txt

# 2. scisci 클론 (PaperBanana 래퍼)
git clone https://github.com/jehyunlee/scisci.git /path/to/scisci
```

`config.json`에 경로를 추가하세요:

```json
{
  "paperbanana_dir": "/path/to/paperbanana",
  "scisci_lib": "/path/to/scisci/scie"
}
```

의존성 체인:
```
pipeline/generate_timelines.py
  → scisci/scie/lib/paperbanana.py   (래퍼: 경로 관리, async 실행)
    → paperbanana/                    (7-agent pipeline: Retriever → Planner → Visualizer → Critic)
  → scisci/scie/lib/timeline.py      (LLM 내러티브 분석)
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

Collection key나 User ID는 직접 입력할 필요 없이 Zotero API를 통해 자동으로 조회됩니다.

## 설치 확인 & 문제 해결

### 설치 확인 (verify)

긴 파이프라인 전에 인증·Python·패키지·Zotero 연결을 한 번에 확인하세요:

```bash
npx . doctor --network
```

실행 계획만 확인하려면:

```bash
npx . run -- --topic my_topic --mode curate --source zotero --dry-run
```

### 문제 해결 (Troubleshooting)

| 증상 / 에러 메시지 | 원인 | 해결 |
|---|---|---|
| `op_CALL_KW: pop from empty list` (numba 트레이스백) | `py312` env 밖에서 분류가 실행됨 | `conda activate py312` 후 재실행 |
| `ModuleNotFoundError: umap` / `hdbscan` / `sentence_transformers` | 의존성 누락 | env 활성화 후 `pip install -r requirements.txt` (umap-learn·hdbscan·sentence-transformers 포함) |
| Figure 품질이 낮음 / 표·구조가 깨짐 | Java 미설치로 PyMuPDF fallback | `brew install --cask temurin` (macOS) 후 재실행 |
| SPECTER2 / arXiv 다운로드가 멈춤 (한국 망) | huggingface LFS·arXiv 차단 | [operations.md "Korean network workarounds"](operations.md#korean-network-workarounds) 의 S3 미러 명령 사용 |
| `[COLLECTION_ERROR]` | Zotero 컬렉션 이름 오타 | 출력의 사용 가능한 컬렉션 목록에서 올바른 이름 선택 후 재실행 |
| 검색 인덱스가 빈 임베딩으로 빌드됨 | `GOOGLE_API_KEY` 미설정 | `export GOOGLE_API_KEY=...` 후 재실행 — 검색 임베딩은 Google `gemini-embedding-001` 사용 (OpenAI 키는 더 이상 필수 아님) |
| OAuth structured output 버전 오류 | Claude Code < 2.1.205 | `claude update` 후 `claude --version` 확인 |
| `Claude Code OAuth가 준비되지 않았습니다` | 구독 로그인이 없거나 만료됨 | `claude auth login` 또는 `claude setup-token` 후 `CLAUDE_CODE_OAUTH_TOKEN` 설정 |
