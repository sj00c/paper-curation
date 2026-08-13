# Operations Manual

Paper Curation은 로컬 실행이 기본입니다. 공개 배포, 이메일, 원격 DB 동기화는 각각 별도의 명시적 설정과 명령이 있어야 동작합니다.

## 기본 점검

```bash
paper-curation inspect
paper-curation doctor
```

`inspect`는 저장소, Python 3.12, Claude 인증, Zotero 로컬 DB, 설정된 토픽과 publication mode를 읽기 전용으로 확인합니다. `doctor --network`만 외부 연결을 점검합니다.

## 로컬 운영

```bash
TOPIC=my-topic

# 실행 계획만 확인
PYTHONUTF8=1 python pipeline/run_full.py --topic "$TOPIC" --mode curate --source zotero --dry-run

# Zotero의 신규·누락 논문 처리
PYTHONUTF8=1 python pipeline/run_full.py --topic "$TOPIC" --mode curate --source zotero

# 웹 검색부터 신규 논문 처리
PYTHONUTF8=1 python pipeline/run_full.py --topic "$TOPIC" --mode curate --source web --days 7

# 로컬 대시보드
PYTHONUTF8=1 python pipeline/serve_local.py --topic "$TOPIC"
```

생성 결과는 `docs/{topic}/index.html`, 논문 리뷰는 `docs/papers/{slug}/`에 저장됩니다.

## 분류

기본 분류는 저장된 SPECTER2/UMAP/HDBSCAN 번들을 사용합니다.

```bash
PYTHONUTF8=1 python pipeline/run_full.py --topic "$TOPIC" --mode reclassify
```

Zotero 하위 컬렉션을 카테고리로 사용할 수도 있습니다.

```bash
PYTHONUTF8=1 python pipeline/run_full.py --topic "$TOPIC" --mode reclassify \
  --classify-source zotero --unclassified skip
```

`--unclassified include`는 이름이 `Unclassified`, `99 Unclassified`, `미분류`인 폴더를 카테고리로 포함합니다. 여러 하위 컬렉션에 속한 논문은 `all_categories`에 모두 기록됩니다.

## 이미지와 타임라인

```bash
# 변경된 카테고리만
PYTHONUTF8=1 python pipeline/run_full.py --topic "$TOPIC" --mode retime --images changed

# 전체 재생성
PYTHONUTF8=1 python pipeline/run_full.py --topic "$TOPIC" --mode retime --images all
```

Google API Key와 PaperBanana가 없으면 관련 이미지 기능만 비활성으로 남습니다.

## 검색 인덱스와 검색

```bash
PYTHONUTF8=1 python pipeline/build_search_index.py --topic "$TOPIC"
python pipeline/query_search_index.py --topic "$TOPIC" --query "your research question" --json
```

Google API Key가 없으면 lexical BM25 검색만 사용합니다. Dense 인덱스에는 `gemini-embedding-001`의 768차원 `RETRIEVAL_DOCUMENT` 벡터를 L2 정규화한 뒤 int8로 저장합니다.

## 검증과 복구

```bash
PYTHONUTF8=1 python pipeline/validate_papers.py --topic "$TOPIC" --strict
PYTHONUTF8=1 python pipeline/run_full.py --topic "$TOPIC" --mode audit
```

다음 명령은 데이터를 지우거나 원격 Zotero를 변경할 수 있으므로 먼저 dry-run 결과를 검토해야 합니다.

```bash
# PDF↔review 오매칭 산출물 제거
PYTHONUTF8=1 python pipeline/fix_matching.py --topic "$TOPIC" --execute

# Zotero 중복 삭제
PYTHONUTF8=1 python pipeline/dedup_zotero.py --topic "$TOPIC" --execute
```

예상하지 못한 사용자 변경은 stash·reset·삭제하지 않습니다.

## Bibliography DB

로컬 기본 DB는 `.cache/bibliography.sqlite3`입니다.

```bash
PYTHONUTF8=1 python pipeline/build_bibliography_db.py --all
PYTHONUTF8=1 python pipeline/check_bibliography_db.py --strict
PYTHONUTF8=1 python pipeline/query_bibliography.py --institution "Cambridge" --sort date
```

완료 이메일은 `notifications.completion_email` 또는 `BIBLIOGRAPHY_COMPLETION_EMAIL`을 설정하고 해당 실행에 `--notify`를 지정한 경우에만 발송됩니다.

## 공개 배포

공개 배포는 `config.json`에 다음처럼 명시해야 합니다.

```json
{
  "publication": {
    "mode": "public",
    "base_url": "https://papers.example.org"
  }
}
```

Cloudflare 자격증명과 Worker secrets도 별도로 설정합니다.

```bash
export CLOUDFLARE_API_TOKEN=...
export CLOUDFLARE_ACCOUNT_ID=...
npx wrangler secret put GOOGLE_API_KEY
PYTHONUTF8=1 python pipeline/run_full.py --topic "$TOPIC" --mode deploy
```

저장소의 `wrangler.toml`에는 소유자별 custom domain route가 없습니다. 배포자는 자신의 Wrangler 설정에 route를 추가해야 합니다. 배포 명령은 source branch를 자동 commit하거나 push하지 않습니다.

`docs/.assetsignore`에는 로컬 전용 토픽과 업로드 금지 자산을 설치별로 추가합니다. 현재 public deploy에서 `--topics` 부분 업로드는 지원하지 않으며, 전체 `docs/` 업로드 범위를 오해하지 않도록 명시적으로 거부합니다.

## 환경 경계

- 지원 인터프리터: Python 3.12
- Claude 인증: Claude Code OAuth 또는 `ANTHROPIC_API_KEY`
- Zotero API Key: 메타데이터·첨부 접근에 필수
- Google API Key: dense 검색, Figure 검증, 타임라인 이미지, TTS에 선택
- OpenAI API Key: 선택한 backend 기능에만 사용
- `PAPER_CURATION_CA_BUNDLE`: 사설 CA가 필요한 환경에서만 지정하며 TLS 검증을 끄지 않습니다.
