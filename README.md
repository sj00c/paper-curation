# Paper Curation

Paper Curation은 Zotero 컬렉션의 논문을 로컬에서 검토하고 정적 페이지로 만들며 검색하는 설치형 도구입니다. 공식 인터페이스는 Python 패키지의 `paper-curation` CLI입니다. 이 포크는 한 번의 업스트림 인테이크 이후 현재 제품의 소스 오브 트루스이며, 업스트림과 지속 동기화하지 않습니다.

## 설치와 엄격한 설정

```bash
git clone <fork-url>
cd paper-curation
conda env create -f environment.yml
conda activate py312
```

`environment.yml`은 Docker 설정이 아닌 로컬 Conda 환경입니다. Zotero, 인증 상태, PDF, 설정, 캐시와 생성물은 모두 워크스테이션에 남습니다.

설정 입력은 엄격한 JSON 스키마여야 합니다. 지원하지 않는 키, 잘못된 타입, 모순된 전송·제공자 설정은 거부됩니다. `config.example.json`을 출발점으로 삼되, 설치별 값은 추적하지 않는 별도 입력 파일에 둡니다. 먼저 미리보기하고 검토한 뒤에만 설정과 작업공간을 만드십시오.

```bash
paper-curation setup --input strict-input-config.json --config config.json
paper-curation setup --input strict-input-config.json --config config.json --execute
```

기존 대상 설정을 교체하는 경우에만 `--replace`를 실행 명령에 추가합니다. 이미 있는 이전 설정의 스키마 변경은 별도 마이그레이션으로 먼저 미리보기한 뒤 적용합니다.

```bash
paper-curation migrate --config config.json
paper-curation migrate --config config.json --execute
```

마이그레이션은 인식하는 이전 로컬 데이터 경로와 공개 URL을 보존하고, 표현할 수 없는 값은 보고합니다.

## 로컬 작업 흐름

작업공간 루트 아래의 `papers/`, `.cache/`, `.staging/`, `site/`는 모두 설치 로컬 상태입니다. 코퍼스나 생성 결과는 저장소에서 추적하지 않습니다.

`source.transport`은 둘 중 하나를 명시합니다. `local-sqlite`는 로컬 Zotero SQLite 라이브러리 경로를 요구하고, `zotero-storage`는 그 경로 없이 Zotero Storage를 사용합니다. `source.collections`의 별칭을 `--topic`에 전달합니다.

Core 검토에는 정확히 하나의 `core.review.provider`와 `core.review.model`이 반드시 명시됩니다. 선택한 조합이 실패하면 Core가 실패하며 다른 제공자나 모델로 대체되지 않습니다. 활성화한 enhancement는 설치된 어댑터가 있을 때만 허용됩니다. 자격증명이 존재한다는 사실만으로 enhancement나 제공자가 자동 활성화되지는 않습니다.

일상적인 순서는 다음과 같습니다.

```bash
paper-curation inspect --config config.json
paper-curation doctor --config config.json
paper-curation build --config config.json
paper-curation validate --config config.json
paper-curation serve --config config.json
```

`inspect`와 기본 `doctor`는 읽기 전용이며, `doctor --config config.json --network`만 구성된 외부 연결을 점검합니다. `build` 뒤에는 `validate`를 통과한 뒤 `serve`로 로컬 사이트를 제공합니다. `serve --config config.json --dry-run`, `--host`, `--port`, `--public-bind`는 제공 계획과 바인딩을 명시적으로 제어합니다.

## 검토, 검색, 복구, 공개 배포

`update`는 구성된 컬렉션에서 Core를 실행합니다. 성공한 Core는 완전한 검토, 페이지, 영수증을 함께 남기며 부분 결과는 성공으로 취급하지 않습니다. 먼저 선택과 비용을 검토합니다. `--paper`는 반복할 수 있고, `--attachment RECORD_ID=ATTACHMENT`는 선택한 각 논문의 자동 PDF 선택을 재정의합니다.

```bash
paper-curation update --config config.json --topic <topic-alias> --dry-run
paper-curation update --config config.json --topic <topic-alias> --paper <record-id> --attachment <record-id>=<attachment-id>
paper-curation query --config config.json --topic <topic-alias> --query "research question" --limit 10
paper-curation repair --config config.json
paper-curation repair --config config.json --execute
```

`query`는 완료되고 검증된 Core 결과를 읽는 제공자 없는 로컬 어휘(lexical) 검색입니다. `repair`는 기본적으로 복구 조치를 미리보기만 하며 `--execute`에서만 씁니다.

공개 배포는 Cloudflare로 명시적으로 구성한 경우에만 별도 실행합니다. `build`나 `update`는 배포하지 않습니다.

```bash
paper-curation deploy --config config.json
paper-curation deploy --config config.json --execute
```

첫 명령은 배포 미리보기이고, 실행에는 공개 Cloudflare 구성과 필요한 로컬 인증이 필요합니다. 인증 정보와 배포 대상은 문서, 정적 출력, 저장소에 넣지 않습니다.

## 호환성

`pipeline/run_full.py`는 기존 실행 파일 경로를 위한 얇은 이름 호환 wrapper이며 공식 CLI와 같은 인자만 받습니다. 별도 업무 로직이나 과거 mode/flag는 소유하지 않습니다.

제품 요구사항은 [PRD](docs/PRD.md), 규범 공학 계약은 [SPEC](docs/SPEC.md), 다음 세션 인계는 [HANDOFF](docs/HANDOFF.md)를 참조하세요. 운영 세부사항은 [operations](docs/operations.md), 구조 설명은 [architecture](docs/architecture.md), 초기 설정은 [setup guide](docs/setup-guide.md)에 있습니다.
