# Paper Curation

로컬 Zotero 코퍼스를 검토·렌더링·검색하는 설치형 도구입니다. 공식 진입점은 Python 패키지가 제공하는 `paper-curation` CLI입니다. 기존 로컬 데이터, 설정의 경로와 공개 URL은 설정 마이그레이션이 보존합니다.

## 설치와 일상 작업

```bash
python -m pip install .
python -m pip install -r requirements.txt
paper-curation setup
paper-curation inspect
paper-curation doctor --network
paper-curation update --topic <topic>
paper-curation serve --topic <topic>
```

`setup`은 로컬 `config.json`만 만들거나 갱신합니다. `inspect`와 기본 `doctor`는 읽기 전용이며, `doctor --network`만 외부 연결을 확인합니다. 전체 생성은 `build --topic <topic>`, 증분 수집·생성은 `update --topic <topic>`입니다. 검색·검증·복구·공개 배포는 각각 다음처럼 명시합니다.

```bash
paper-curation query --topic <topic> --query "research question"
paper-curation validate --topic <topic>
paper-curation repair --topic <topic>          # preview
paper-curation repair --topic <topic> --execute # writes changes
paper-curation deploy --topic <topic>
```

배포는 `build`나 `update`에 포함되지 않는 별도 공개 작업입니다. 로컬 생성은 기본적으로 외부에 게시하거나 알림을 보내지 않습니다.

## 구성과 보안

`config.json`, `.env`, PDF 캐시, 데이터베이스, 생성 코퍼스는 설치자 로컬 상태이며 추적하지 않습니다. 선택 통합의 자격증명이 없으면 해당 기능만 비활성화됩니다. 브라우저의 BYOK 키는 한 페이지의 메모리에만 두며 Web Storage나 URL에 저장하지 않습니다. 소유자 키는 정적 결과물에 넣지 않습니다.

구성 스키마가 바뀌면 먼저 미리보기를 실행하고, 결과를 검토한 뒤에만 적용합니다.

```bash
paper-curation migrate --config config.json
paper-curation migrate --config config.json --execute
```

마이그레이션은 알려진 이전 로컬 데이터 경로와 공개 URL 값을 보존하고, 새 스키마에 표현할 수 없는 값은 보고합니다.

## 호환성

`pipeline/run_full.py`는 기존 자동화용 호환성 래퍼로 남아 있습니다. 새 문서·자동화는 공식 CLI를 사용합니다. 고급 레거시 플래그를 조사하거나 장애를 재현할 때만 다음을 사용합니다.

```bash
python pipeline/run_full.py --topic <topic> --mode curate --source zotero
```

운영 세부사항은 [operations](docs/operations.md), 모듈 경계는 [architecture](docs/architecture.md), 기여 절차는 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.
