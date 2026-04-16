---
title: "1228_OpenRad_a_Curated_Repository_of_Open-access_AI_models_for_Ra"
authors:
  - "Konstantinos Vrettos"
  - "Galini Papadaki"
  - "E. Brilakis"
  - "Matthaios Triantafyllou"
  - "D. Leventis"
date: "2026"
doi: "N/A"
arxiv: ""
score: 4.0
essence: "OpenRad는 방사선학 분야의 개방형 AI 모델을 위한 큐레이션된 저장소로, 5,239개의 논문을 검색하여 1,694개의 개방형 코드/모델을 보유한 표준화된 리소스이다. 이 저장소는 RSNA AI Roadmap 온톨로지를 따르며 모델 발견성, 재현성, 임상 적용을 촉진한다."
tags:
  - "cat/Open_Access_Publication_Analytics"
  - "cat/Academic_Impact_and_Mobility"
  - "sub/Polymer_Science_Publication_Analytics"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/OpenRad a Curated Repository of Open-access AI models for Radiology.pdf"
---

# OpenRad: a Curated Repository of Open-access AI models for Radiology

> **저자**: Konstantinos Vrettos, Galini Papadaki, E. Brilakis, Matthaios Triantafyllou, D. Leventis, Despina Staraki, Maria Mavroforou, E. Tzanis, Konstantina Giouroukou, Michail E. Klontzas | **날짜**: 2026 | **DOI**: N/A

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig.1 Flowchart of the article selection process*

OpenRad는 방사선학 분야의 개방형 AI 모델을 위한 큐레이션된 저장소로, 5,239개의 논문을 검색하여 1,694개의 개방형 코드/모델을 보유한 표준화된 리소스이다. 이 저장소는 RSNA AI Roadmap 온톨로지를 따르며 모델 발견성, 재현성, 임상 적용을 촉진한다.

## Motivation

- **Known**: 방사선학 AI 연구는 급속히 증가했지만 모델들이 다양한 플랫폼에 산재되어 있어 발견성과 재현성이 저해되고 있다. RSNA AI Roadmap은 표준화된 온톨로지를 제안했으나 기존 저장소들은 핸드픽된 소수 모델만 포함하고 재현 가능한 개방형 코드가 부족하다.
- **Gap**: 기존 저장소들은 개방형 코드를 동반하지 않은 모델을 포함하거나 제한된 수의 모델만 제공하여, 연구자들이 새로운 모델을 개발하거나 임상 워크플로우를 개선하는 데 실질적으로 도움이 되지 않는다.
- **Why**: 개방형, 큐레이션된, 표준화된 중앙 저장소는 모든 이미징 모달리티와 방사선학 전문 분야에 걸친 AI 모델의 발견, 재현성 보장, 임상 번역을 촉진하여 방사선학 커뮤니티의 연구 효율성과 임상 적용을 크게 향상시킬 수 있다.
- **Approach**: PubMed, arXiv, Scopus에서 5,239개 논문을 검색한 후, gpt-oss:120b LLM을 사용하여 RSNA JSON 스키마 기반 모델 레코드를 자동 추출하고 10명의 전문가가 수동으로 검증했다. GitHub 저장소 분석을 통해 학습된 가중치와 대화형 구현의 가용성을 추가로 평가했다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig.2: (A): OpenRad Interface. (B) Live, interactive statistics based on the entire model*

- **1,694개 개방형 모델 큐레이션**: 모든 이미징 모달리티(CT, MRI, X-Ray, US)와 방사선학 전문 분야를 포함하는 전문가 검증 모델 컬렉션 구축
- **표준화된 메타데이터**: RSNA AI Roadmap의 RadLex 온톨로지를 따르는 일관성 있고 상호운용 가능한 모델 레코드
- **자동 추출 안정성**: Levenshtein ratio > 90%의 높은 안정성으로 구조화된 필드 추출, 78.5%의 편집이 경미한 수준
- **포괄적 메타데이터**: 표준 RSNA 필드에 추가로 데이터셋 세부사항, 검증 전략, 사전학습 가중치/대화형 구현 가용성 정보 포함
- **웹 인터페이스 및 커뮤니티 기능**: 키워드 검색, 모달리티/전문분야/사용사례/검증상태/데모 가용성 필터링, 실시간 통계, 커뮤니티 모델 제출 포탈
- **AI 연구 동향 분석**: CNN과 transformer가 우세 아키텍처이며, MRI가 가장 많이 사용되는 모달리티(뇌신경방사선학 621개 모델), 중국과 미국이 주요 연구국임을 파악

## How

![Figure 1](figures/fig1.webp)

*Fig.1 Flowchart of the article selection process*

- PubMed, arXiv, Scopus 데이터베이스를 사용하여 5,239개 레코드 수집
- DOI 기반 중복 제거(985개) 및 방사선학 AI 모델에 포함되지 않은 논문 제외(1,832개)
- 개방형 코드/모델이 없는 논문(704개) 및 데이터셋만 제공하는 논문(24개) 제외
- gpt-oss:120b LLM과 Python 'instructor' 라이브러리를 사용한 구조화된 프롬프트로 자동 추출", '전체 텍스트 PDF 또는 초록을 LLM에 입력하여 RSNA JSON 스키마 필드 자동 채우기
- 225개 논문의 무작위 샘플에 대해 difflib.SequenceMatcher, Levenshtein ratio, Jaccard similarity로 LLM 출력 안정성 평가
- 10명의 전문가 검토자(PhD 3명, MSc 6명, 조교수 1명)가 모든 생성된 레코드를 수동 검증
- 경미한 편집(오타, 불완전한 메트릭)과 주요 편집(누락된 필드, 손상된 링크) 구분
- GitHub URL 자동 쿼리로 사전학습된 가중치와 대화형 구현 가용성 식별
- 저자 소속 파싱으로 ISO-3 국가 코드 매핑 및 지리공간 분석 수행
- Seaborn, Matplotlib, Plotly로 모델 아키텍처, 검증 전략, 지역별 분포 시각화
- WordCloud를 사용한 보고된 모델 제한사항의 정성적 분석

## Originality

- **대규모 자동화 + 수동 검증 하이브리드**: gpt-oss:120b를 사용한 자동 추출과 전문가 10명의 수동 검증을 결합하여 대규모 모델 기록화의 확장성과 신뢰성 동시 달성
- **재현 가능성 중심 필터링**: 개방형 코드/모델을 동반하지 않은 논문을 명시적으로 제외하여 실제 사용 가능한 모델만 포함하는 차별화된 저장소 구축
- **GitHub 저장소 메타데이터 추가 분석**: 논문 메타데이터 외에 자동화된 GitHub 쿼리로 사전학습 가중치와 대화형 구현 가용성을 추가적으로 평가
- **표준화 + 커뮤니티 확장성**: RSNA AI Roadmap 온톨로지를 따르면서도 커뮤니티 모델 제출 포탈로 지속적인 갱신 가능
- **포괄적 통계 대시보드**: 모달리티별, 전문분야별, 국가별 분포 등 개방형 AI 연구의 현황을 실시간으로 제공

## Limitation & Further Study

- **LLM 환각 위험**: gpt-oss:120b의 자동 추출 결과가 항상 정확하지 않아 10명의 수동 검증 필요하며, 논문이 대규모로 추가될 경우 검증 병목 가능
- **개방형 모델 편향**: 개방형 코드/모델을 공개하지 않은 고성능 연구들이 제외되어 저장소가 전체 방사선학 AI 랜드스케이프의 완전한 반영이 아님
- **메타데이터 완성도**: 78.5%만 경미한 편집이었지만, 일부 논문들은 보고된 필드가 불완전할 수 있으며 표준화 정도가 일정하지 않을 가능성
- **시간적 한계**: 논문 발표에서 저장소 등재까지의 시간 지연이 발생할 수 있으며, 빠르게 진화하는 방사선학 AI 분야에서 저장소 신선도 유지 필요
- **후속연구 방향**: (1) LLM 검증 자동화로 수동 검증 비용 감소, (2) 개인 및 기관 GitHub 저장소 자동 크롤링으로 발견성 향상, (3) 모델 성능 메타분석 도구 개발, (4) 임상 실제 데이터셋으로의 모델 이전 가능성 평가 연구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: OpenRad는 방사선학 AI 모델의 발견성, 재현성, 임상 번역을 촉진하기 위해 LLM 자동화와 전문가 검증을 효과적으로 결합한 포괄적인 큐레이션 저장소이다. 개방형 코드 중심 필터링과 표준화된 메타데이터는 실무적 가치가 높으나, 개방형 모델 편향과 지속적 검증 비용은 향후 개선이 필요한 부분이다.

## Related Papers

- 🔄 다른 접근: [[papers/1075_Open_Catalyst_2020_OC20_Dataset_and_Community_Challenges/review]] — 오픈 카탈리스트와 OpenRad 모두 특정 분야를 위한 개방형 AI 모델 저장소를 서로 다른 접근법으로 구축합니다.
- 🏛 기반 연구: [[papers/1072_Embracing_Foundation_Models_for_Advancing_Scientific_Discove/review]] — 과학 발견을 위한 기초 모델 수용 이론이 방사선학 AI 모델 저장소 설계의 이론적 배경을 제공합니다.
- 🔄 다른 접근: [[papers/1015_S2ORC_The_Semantic_Scholar_Open_Research_Corpus/review]] — OpenRad와 S2ORC 모두 대규모 과학 데이터를 체계적으로 수집하고 표준화하여 연구 커뮤니티에 제공하는 오픈 사이언스 인프라 구축 프로젝트다.
- 🏛 기반 연구: [[papers/1134_A_scientometrics_survey_of_machine_learning_and_neural_netwo/review]] — 사이버보안 분야의 기계학습 응용에 대한 scientometric 조사가 의료 AI 모델의 보안성과 신뢰성 평가에 필수적인 방법론적 통찰을 제공한다.
- 🔗 후속 연구: [[papers/1109_A_comprehensive_large-scale_biomedical_knowledge_graph_for_A/review]] — 의료 AI 분야의 지식 그래프를 방사선학 특화 AI 모델로 확장한 접근이다
- 🏛 기반 연구: [[papers/930_A_Survey_on_Knowledge_Organization_Systems_of_Research_Field/review]] — 연구 분야 지식 조직 체계에 대한 포괄적 분석이 특화 분야 저장소 구축의 기반을 제공한다
