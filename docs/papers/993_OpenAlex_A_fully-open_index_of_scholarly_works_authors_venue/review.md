---
title: "993_OpenAlex_A_fully-open_index_of_scholarly_works_authors_venue"
authors:
  - "Jason Priem"
  - "Heather Piwowar"
  - "Richard Orr"
date: "2022"
doi: ""
arxiv: ""
score: 4.0
essence: "Microsoft Academic Graph 종료에 따라 학술 메타데이터의 완전 개방형(오픈 데이터, API, 소스코드) 대체 시스템으로 OpenAlex를 개발하였으며, 209M개 논문, 213M명 저자, 124K개 학술지 등 5개 엔티티 타입으로 구성된 학술 지식 그래프(Scientific Knowledge Graph)를 제공한다."
tags:
  - "cat/Open_Access_Publication_Analytics"
  - "cat/AI-Assisted_Scientific_Discovery"
  - "cat/Academic_Impact_and_Mobility"
  - "sub/Polymer_Science_Publication_Analytics"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Priem et al._2022_OpenAlex A fully-open index of scholarly works, authors, venues, institutions, and concepts.pdf"
---

# OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts

> **저자**: Jason Priem, Heather Piwowar, Richard Orr | **날짜**: 2022 | **URL**: [https://arxiv.org/abs/2205.01833](https://arxiv.org/abs/2205.01833)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Sketch of the OpenAlex graph data model.*

Microsoft Academic Graph 종료에 따라 학술 메타데이터의 완전 개방형(오픈 데이터, API, 소스코드) 대체 시스템으로 OpenAlex를 개발하였으며, 209M개 논문, 213M명 저자, 124K개 학술지 등 5개 엔티티 타입으로 구성된 학술 지식 그래프(Scientific Knowledge Graph)를 제공한다.

## Motivation

- **Known**: Microsoft Academic Graph (MAG)가 학술 메타데이터의 주요 무료 자원이었으나 2022년 1월 서비스 종료되었고, 기존의 OpenCitations, Semantic Scholar 등 부분 개방형 SKG들이 존재했다.
- **Gap**: MAG 종료로 인한 학술 메타데이터 접근성 공백이 발생했으며, 기존 시스템들이 완전한 개방성(데이터, API, 코드)을 동시에 제공하지 못하고 있었다.
- **Why**: 완전 개방형 학술 메타데이터는 연구 평가의 투명성 향상, 학술 자원의 민주적 접근, 오픈 사이언스 인프라 구축에 필수적이다.
- **Approach**: MAG를 기반으로 하면서도 완전 개방형 구조를 채택하여, Crossref, PubMed, arXiv 등 다양한 소스에서 데이터를 수집하고, 규칙 기반 및 머신러닝 기반 알고리즘으로 엔티티 파싱, 정규화, 중복 제거를 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Sketch of the OpenAlex graph data model.*

- **완전 개방형 인프라 구축**: 100% 오픈 데이터, 제한 없는 REST API, 오픈 소스 코드로 제공하며 Open Scholarly Infrastructure 원칙 준수
- **대규모 학술 지식 그래프 구성**: 209M개 works, 213M명 authors, 124K개 venues, 109K개 institutions, 65K개 concepts를 포함한 종합 메타데이터 데이터베이스
- **다중 식별자 지원**: 각 엔티티 타입별 표준 ID(DOI, ORCID, ISSN-L, ROR, Wikidata) 할당으로 상호운용성 극대화
- **정교한 엔티티 매칭**: 저자 명확화(disambiguation), 기관 파싱, 문서 버전 추적 등을 위한 머신러닝 알고리즘 개발

## How


- Crossref, PubMed, arXiv, 기관 저장소 등 다양한 소스에서 구조화/비구조화 메타데이터 수집
- 규칙 기반 및 머신러닝 2단계 알고리즘으로 기관 소속 문자열 추출 및 정규화
- MAG에서 학습된 분류기로 논문 제목과 초록으로부터 개념 자동 할당 (85% 적용률)
- 지문(fingerprinting) 알고리즘으로 preprint, VoR 등 다중 버전 문서 매칭 및 식별
- 영구적 OpenAlex ID를 웹 기반 URL로 제공하여 HTML/JSON 양식 접근 지원

## Originality

- MAG 종료 후 완전한 오픈 기반의 첫 번째 상용급 학술 지식 그래프 제공
- 기존 SKG들과 달리 데이터, API, 소스코드 모두 100% 개방하는 차별화된 모델
- 다양한 소스의 이질적 메타데이터를 통합하는 포괄적 엔티티 매칭 파이프라인
- Wikidata 기반 계층적 개념 구조로 표준화된 의미론적 표현

## Limitation & Further Study

- **엔티티 정확성 미검증**: 저자 및 기관 파싱/정규화 정확도가 미흡하며 고위험 평가 맥락에서의 신뢰성 부족
- **메타데이터 누락**: 자금 출처(funding sources), 교신저자(corresponding authors) 정보 미포함
- **비교 연구 부재**: 타 도구와의 정확성/완전성 비교 검증 필요
- **초기 단계의 제한**: 프로젝트 초창기로 데이터 품질 개선 및 대규모 검증 작업 필요
- **후속 연구**: 엔티티 정확도 개선, 결측 메타데이터 추가, 대규모 정확성 벤치마킹, 신뢰도 평가 체계 수립

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: OpenAlex는 MAG 종료로 인한 학술 인프라 공백을 메우면서 완전 개방형 모델을 제시한 중요한 프로젝트로, 규모와 개방성 측면에서 획기적이나 초기 단계로 엔티티 정확도 및 데이터 완전성 개선이 시급하다.

## Related Papers

- 🔄 다른 접근: [[papers/1015_S2ORC_The_Semantic_Scholar_Open_Research_Corpus/review]] — 학술 메타데이터 제공을 위한 또 다른 대규모 오픈 연구 코퍼스로서 OpenAlex와 상호 보완적인 역할을 한다.
- 🔗 후속 연구: [[papers/1023_SciSciNet_A_large-scale_open_data_lake_for_the_science_of_sc/review]] — OpenAlex 데이터를 활용하여 과학계량학 연구를 위한 더 포괄적인 오픈 데이터 레이크를 구축한다.
- 🏛 기반 연구: [[papers/1115_Google_Scholar_Microsoft_Academic_Scopus_Dimensions_Web_of_S/review]] — 학술 데이터베이스들 간의 비교 분석을 통해 OpenAlex 개발의 필요성과 방향성을 제시한다.
- 🧪 응용 사례: [[papers/1044_The_State_of_OA_A_Large-Scale_Analysis_of_the_Prevalence_and/review]] — OpenAlex 데이터를 활용하여 오픈 액세스 출판의 현황과 영향을 대규모로 분석할 수 있는 기반을 제공한다.
- 🏛 기반 연구: [[papers/1042_The_Scholarly_Knowledge_Ecosystem_Challenges_and_Opportuniti/review]] — 학술 지식 생태계의 오픈 인프라 구축을 위한 핵심 데이터 기반을 제공한다.
- ⚖️ 반론/비판: [[papers/1038_The_Oligopoly_of_Academic_Publishers_in_the_Digital_Era/review]] — 기존 상업적 학술 출판 독점 구조에 대한 완전 개방형 대안 시스템을 제시한다.
- 🔗 후속 연구: [[papers/1081_Science_Citation_IndexA_New_Dimension_in_Indexing_This_uniqu/review]] — 전통적인 인용 색인의 개념을 확장하여 다차원적이고 개방적인 학술 지식 그래프로 발전시켰다.
- 🔄 다른 접근: [[papers/1015_S2ORC_The_Semantic_Scholar_Open_Research_Corpus/review]] — OpenAlex와 S2ORC가 서로 다른 접근으로 대규모 학술 데이터베이스를 구축하여 상호 보완적 역할을 한다.
- 🔗 후속 연구: [[papers/1023_SciSciNet_A_large-scale_open_data_lake_for_the_science_of_sc/review]] — 학술 색인의 완전 개방화가 과학의 과학 연구를 위한 포괄적 데이터 레이크로 확장됩니다.
- 🔄 다른 접근: [[papers/1115_Google_Scholar_Microsoft_Academic_Scopus_Dimensions_Web_of_S/review]] — OpenAlex의 완전 오픈 인덱스가 기존 상업적 인용 데이터베이스들의 접근성 한계를 해결하는 대안을 제시한다.
- 🏛 기반 연구: [[papers/992_OpenAlex_in_focus_Metadata_quality_of_publication_type_and_l/review]] — OpenAlex의 전체 시스템을 소개한 기초 연구로, 메타데이터 품질 평가의 대상이 되는 시스템에 대한 근본적 이해를 제공합니다.
- 🏛 기반 연구: [[papers/1227_Exploring_Open_Access_Research_Trends_in_the_Indian_Council/review]] — OpenAlex 색인의 전반적 구조와 기능이 인도 농업연구회의소 개방접근 분석의 데이터 기반을 제공합니다.
