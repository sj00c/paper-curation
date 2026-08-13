---
name: paper-curation
description: "로컬 논문 큐레이션을 공식 paper-curation CLI로 설정·점검·생성·검색·검증·복구·명시적 배포한다."
---

# Paper Curation

## Official interface

설치된 `paper-curation` CLI만 기본 경로로 사용한다. `pipeline/run_full.py`는 기존 자동화 및 고급 장애 재현용 호환성 래퍼이며 새 작업의 진입점이 아니다.

| 요청 | 명령 |
|---|---|
| 설정 | `paper-curation setup` |
| 상태 점검 | `paper-curation inspect` |
| 연결 진단 | `paper-curation doctor --network` |
| 전체 재생성 | `paper-curation build --topic my-topic` |
| 증분 갱신 | `paper-curation update --topic my-topic` |
| 로컬 열람 | `paper-curation serve --topic my-topic` |
| 검색 | `paper-curation query --topic my-topic --query "..."` |
| 검증 | `paper-curation validate --topic my-topic` |
| 복구 미리보기 | `paper-curation repair --topic my-topic` |
| 복구 실행 | `paper-curation repair --topic my-topic --execute` |
| 공개 배포 | `paper-curation deploy --topic my-topic` |

## Side-effect rules

- `inspect`와 기본 `doctor`는 읽기 전용이다. 네트워크 진단은 `doctor --network`에서만 한다.
- `repair`는 미리보기 후에만 `--execute`로 변경한다.
- `build`와 `update`는 배포·알림을 하지 않는다. 공개는 명시적 `deploy`와 로컬 publication 설정이 모두 필요하다.
- 구성 변경은 먼저 미리보기하고 검토 뒤 실행한다.

```bash
paper-curation migrate --config config.json
paper-curation migrate --config config.json --execute
```

마이그레이션은 알려진 이전 로컬 데이터 경로와 공개 URL 값을 보존한다. 자격증명과 로컬 경로는 사용자에게 묻거나 로컬 설정에서만 사용하며, 브라우저 키를 저장·URL 전달·정적 출력에 포함하지 않는다.

## Legacy troubleshooting

기존 호출을 재현해야 할 때만 사용한다:

```bash
python pipeline/run_full.py --topic my-topic --mode curate --source zotero
```
