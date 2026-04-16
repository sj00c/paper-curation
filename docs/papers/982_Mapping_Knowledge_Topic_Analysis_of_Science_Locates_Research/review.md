---
title: "982_Mapping_Knowledge_Topic_Analysis_of_Science_Locates_Research"
authors:
  - "Radim Hladik"
  - "Yann Renisio"
date: "2024.02"
doi: "10.31235/osf.io/94jd5"
arxiv: ""
score: 4.0
essence: "과학 출판물의 의미론적 네트워크와 주제 모델링을 기반으로 연구자들의 인식론적 위치를 규명하는 새로운 좌표계를 제시한다. 주제 구성과 기하학적 데이터 분석을 결합하여 개별 연구자를 학문 지형 내에 위치시킨다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Hladik and Renisio_2024_Mapping Knowledge Topic Analysis of Science Locates Researchers in Disciplinary Landscape.pdf"
---

# Mapping Knowledge: Topic Analysis of Science Locates Researchers in Disciplinary Landscape

> **저자**: Radim Hladik, Yann Renisio | **날짜**: 2024-02-22 | **DOI**: [10.31235/osf.io/94jd5](https://doi.org/10.31235/osf.io/94jd5)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Cloud of topics in the knowledge space. Scores of topics on principal*

과학 출판물의 의미론적 네트워크와 주제 모델링을 기반으로 연구자들의 인식론적 위치를 규명하는 새로운 좌표계를 제시한다. 주제 구성과 기하학적 데이터 분석을 결합하여 개별 연구자를 학문 지형 내에 위치시킨다.

## Motivation

- **Known**: 과학지도 제작은 인용 네트워크나 공저 관계를 통해 지식 구조를 시각화해왔으나, 전통적 학문 분류와 실증적 접근의 괴리가 존재한다. 부르디외의 장 이론은 위치의 공간과 입장 표취의 공간 간 상동성을 강조하지만 실증적 방법론이 부족했다.
- **Gap**: scientometrics와 sociology 전통의 양분된 과학지도 제작 방식을 통합하고, 지식(knowledge)과 지식생산자(knowledge-producers) 간 갭을 해결할 통합 프레임워크가 필요하다. 연구자의 입장 표취(position-takings)를 기하학적으로 분석할 방법론이 부재했다.
- **Why**: 과학 자원 배분, 학제간 협력 기회, 그리고 연구 분야의 시간적 변화를 이해하려면 지식과 생산자를 동시에 분석해야 한다. 이는 과학정책 수립과 평가 제도 개선에 직결된다.
- **Approach**: 주제 모델링(Topic Modeling), 구성적 데이터 분석(Compositional Data Analysis, CoDa), 기하학적 데이터 분석(Geometric Data Analysis, GDA)을 결합하여 출판물 텍스트(제목, 초록, 키워드)로부터 의미론적 관계와 학문 분류 원리를 동시에 분석한다. 체코 국가 R&D 데이터베이스의 1,039,577개 출판물을 대상으로 실증 분석을 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Clustering of disciplinary topic portfolios. Hierarchical clustering with*

- **계층적 군집화**: 전통적 학문 분류와 실증적 하향식 주제 모델이 높은 일치도를 보여 모델의 신뢰성을 입증했다.
- **주성분분석 기반 3축 구조 발견**: 문화-자연(Culture-Nature), 생명-비생명(Life-Non-life), 연구대상-연구방법(Materials-Methods)의 3가지 인식론적 축이 과학 지식공간을 주로 구조화한다.
- **개별 연구자 위치 특정**: 연구자의 주제 포트폴리오를 통해 3개 연속 척도의 인식론적 좌표에 관계적으로 위치시킬 수 있다.
- **외적 타당성 검증**: 출판 형식, 성별, 기관 소속, 펀딩 출처 등 비텍스트 변수와의 관계가 일관된 패턴을 보여 방법론의 견고성을 입증했다.

## How


- 체코 R&D 정보시스템으로부터 2000-2021년 118,560명 저자의 1,039,577개 출판물 데이터 수집
- 출판물 제목, 초록, 키워드로부터 문서-용어 행렬(document-term matrix) 구성
- 잠재 디리클레 할당(LDA) 기반 주제 모델링으로 의미론적으로 일관된 주제 집합 추출
- 주제 구성을 비율 데이터로 변환하여 구성적 데이터 분석(CoDa) 적용
- 기하학적 데이터 분석(GDA)을 통해 주제 공간을 시각화하고 연구자 위치 도출
- 주성분분석(PCA)으로 지식공간 구조화 축 식별
- 학문 분류, 연구자 특성 등과의 연관성 분석으로 외적 타당성 검증

## Originality

- Bourdieu 장 이론의 두 공간(위치 공간과 입장 표취 공간)을 실제로 통합 분석한 최초의 연구로, 학문 분류와 텍스트 분석의 동시적 결합을 제시했다.
- 주제 모델링에 구성적 데이터 분석과 기하학적 데이터 분석을 결합한 혁신적 방법론으로, 개별 연구자를 인식론적 좌표에 위치시키는 새로운 접근을 개발했다.
- 과학지도의 scientometric 전통(인용, 공저 기반)과 sociological 전통(사회적 위치)의 오랜 분리를 극복하는 통합 프레임워크를 제시했다.
- 대규모 전국 데이터베이스의 체계적 활용으로 과학 분야 전체의 구조를 경험적으로 규명하는 새로운 가능성을 보여주었다.

## Limitation & Further Study

- **언어 의존성**: 체코어 출판물 기반 분석으로 영어 과학커뮤니티와의 비교 가능성이 제한되며, 다국어 과학 지형 반영 부족
- **인용 정보 미포함**: 텍스트 기반만 사용하여 인용 네트워크가 제공하는 시간적 영향도와 학파 형성 정보를 활용하지 못함
- **학제간 교류 분석 부족**: 개별 축(Culture-Nature 등)은 식별되었으나 축 간 상호작용과 경계 영역의 상세 분석이 필요
- **후속연구**: (1) 다국가 비교를 통한 국가별 학문 구조 차이 규명, (2) 시계열 분석으로 주제 공간의 동적 변화 추적, (3) 성별·기관별 세부 그룹의 이동 궤적 연구, (4) 인용 네트워크와의 통합 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Bourdieu 이론을 실증적으로 구현하면서 과학지도 제작의 methodological 전통을 통합하는 중요한 기여다. 방법론의 견고성과 정책 적용 가능성이 높으나, 국가 특수성과 언어 의존성의 한계를 극복하기 위한 확장 연구가 필요하다.

## Related Papers

- 🏛 기반 연구: [[papers/985_Mapping_scientific_communities_at_scale/review]] — 대규모 과학 공동체 매핑의 기초 방법론으로, 연구자의 인식론적 위치 규명에 필요한 네트워크 분석 토대를 제공합니다.
- 🔄 다른 접근: [[papers/1050_Unsupervised_embedding_of_trajectories_captures_the_latent_s/review]] — 궤적의 비지도학습 임베딩으로 잠재 구조를 포착하는 연구로, 주제 모델링과 다른 접근법으로 연구자 위치를 파악하는 대안적 방법입니다.
- 🏛 기반 연구: [[papers/1076_Predicting_research_trends_with_semantic_and_neural_networks/review]] — 의미 및 신경 네트워크를 활용한 연구 트렌드 예측 방법론을 주제 분석 기반 연구자 위치 매핑에 적용할 수 있다.
- 🔗 후속 연구: [[papers/986_Mapping_the_changing_structure_of_science_through_diachronic/review]] — 과학 구조의 시간적 변화 매핑을 개별 연구자의 인식론적 위치 매핑으로 확장하여 미시적 관점을 제공한다.
- 🏛 기반 연구: [[papers/969_Hierarchical_Classification_of_Research_Fields_in_the_Web_of/review]] — 계층적 연구 분야 분류 시스템이 연구자의 인식론적 위치 좌표계 개발의 기본 토대를 제공한다.
- 🏛 기반 연구: [[papers/929_A_network_approach_to_topic_models/review]] — 주제 모델에 대한 네트워크 접근법이 연구자 위치 매핑의 방법론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1018_Science_Mapping_and_Science_Maps/review]] — 주제 수준 분석이 과학 지도의 지식 구조 표현에서 핵심적 방법론적 토대를 제공한다.
- 🧪 응용 사례: [[papers/986_Mapping_the_changing_structure_of_science_through_diachronic/review]] — 과학 지식 매핑과 주제 분석 방법론이 학술지 임베딩을 통한 과학 구조 변화 추적에 구체적 분석 도구를 제공한다.
- 🔄 다른 접근: [[papers/949_Comparative_science_mapping_a_novel_conceptual_structure_ana/review]] — 과학 매핑에서 주제 분석과 메타데이터 기반 개념 구조 분석이 서로 다른 접근법을 제시합니다.
- 🧪 응용 사례: [[papers/969_Hierarchical_Classification_of_Research_Fields_in_the_Web_of/review]] — 계층적 분류 시스템이 연구자의 인식론적 위치를 규명하는 좌표계 개발에 직접 활용될 수 있다.
- 🏛 기반 연구: [[papers/1133_A_bibliometric_and_visualized_analysis_of_choriocapillaris_f/review]] — 주제 수준 과학 지식 배치가 특정 의학 분야의 신흥 트렌드 파악에 방법론적 토대를 제공한다.
