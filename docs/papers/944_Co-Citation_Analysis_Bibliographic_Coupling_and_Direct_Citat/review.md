---
title: "944_Co-Citation_Analysis_Bibliographic_Coupling_and_Direct_Citat"
authors:
  - "Kevin W. Boyack"
  - "Richard Klavans"
date: "2010.12"
doi: "10.1002/asi.21419"
arxiv: ""
score: 4.0
essence: "대규모 생의학 문헌(2004-2008, 215만 개 논문)을 이용하여 공인용분석(co-citation analysis), 서지적 결합(bibliographic coupling), 직접 인용(direct citation), 그리고 하이브리드 접근법의 4가지 유사성 기반 방법이 연구 최전선을 얼마나 정확하게 표현하는지 비교 평가했다."
tags:
  - "cat/Open_Access_Publication_Analytics"
  - "cat/Computational_Bibliometric_Analysis"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/Polymer_Science_Publication_Analytics"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Boyack and Klavans_2010_Co‐citation analysis, bibliographic coupling, and direct citation Which citation approach represent.pdf"
---

# Co‐citation analysis, bibliographic coupling, and direct citation: Which citation approach represents the research front most accurately?

> **저자**: Kevin W. Boyack, Richard Klavans | **날짜**: 12/2010 | **DOI**: [10.1002/asi.21419](https://doi.org/10.1002/asi.21419)

---

## Essence


대규모 생의학 문헌(2004-2008, 215만 개 논문)을 이용하여 공인용분석(co-citation analysis), 서지적 결합(bibliographic coupling), 직접 인용(direct citation), 그리고 하이브리드 접근법의 4가지 유사성 기반 방법이 연구 최전선을 얼마나 정확하게 표현하는지 비교 평가했다.

## Motivation

- **Known**: 공인용분석과 서지적 결합은 과학 지도화의 오래된 기법이며, 여러 선행연구에서 다양한 방법론들의 정확성을 비교한 바 있으나 결과가 일관되지 않았다.
- **Gap**: 대규모 코퍼스에서 citation-based 접근법들의 정확성을 체계적으로 비교한 연구가 부족하며, 특히 실제 포트폴리오 분석 응용에 적합한 정확도 측정 지표가 필요하다.
- **Why**: 과학 지도화는 연구 기획 및 평가, 자금 배분 등 실제 의사결정에 사용되므로, 어떤 citation 접근법이 가장 정확한 클러스터링을 제공하는지 파악하는 것이 중요하다.
- **Approach**: 2.15백만 개 논문의 대규모 생의학 문헌 코퍼스에 대해 4가지 유사성 접근법을 적용하고, Jensen-Shannon 발산을 이용한 텍스트 응집도(textual coherence)와 MEDLINE의 연구비-논문 연계 데이터 기반 집중도(concentration measure) 두 가지 정확성 지표로 평가했다.

## Achievement


- **세 가지 순수 citation 기반 방법의 정확성 순위 규명**: 서지적 결합이 공인용분석을 약간 상회하며, 직접 인용이 가장 낮은 정확성을 보였다
- **하이브리드 접근법의 우수성 입증**: citation-text 하이브리드 방법(서지적 결합 기반)이 순수 서지적 결합 결과를 모든 지표에서 개선했다
- **대규모 코퍼스에서 높은 클러스터링 성공률**: 4가지 접근법 모두 92% 이상의 논문을 성공적으로 클러스터링했다
- **새로운 정확도 측정 지표 개발**: 연구비 연계 데이터 기반의 포트폴리오 분석 친화적 평가 지표를 제시했다

## How


- 2004-2008년 생의학 문헌 2,153,769개 논문의 대규모 코퍼스 구축
- 4가지 citation 유사성 접근법(co-citation, bibliographic coupling, direct citation, hybrid) 구현 및 적용
- Jensen-Shannon 발산을 이용한 클러스터 내 텍스트 응집도(within-cluster textual coherence) 계산
- MEDLINE 연구비 인정(acknowledgment) 정보로부터 grant-to-article 연계 추출 및 클러스터 집중도 측정
- 두 가지 정확성 지표를 이용한 방법론 간 비교 분석

## Originality

- 대규모 코퍼스(215만 개 논문)를 대상으로 한 첫 종합적 citation 방법 비교 연구
- 연구비 연계 데이터를 활용한 참신한 정확도 측정 지표 개발로 포트폴리오 분석과의 직접적 연계 제시
- citation 접근법의 이론적 차이를 시각화(Figure 1)하여 각 방법의 장단점을 명확하게 설명
- 직접 인용(direct citation) 방법의 정확성에 대한 첫 대규모 실증 평가

## Limitation & Further Study

- 분석 대상이 생의학 분야로 제한되어 다른 학문 분야에의 일반화 가능성 미지수
- 한국어 및 비영문 문헌 미포함으로 인한 국제 대표성 한계
- 논문 발행 후 인용 누적에 시간이 필요하므로 최신 논문의 정확한 클러스터링이 어려울 수 있음
- 후속연구로서 텍스트 기반 방법론과의 비교, 다른 학문 분야 적용, 시간 경과에 따른 안정성 검증이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 대규모 코퍼스와 새로운 정확도 지표를 활용하여 citation 기반 science mapping 방법론의 상대적 성능을 처음으로 체계적으로 평가한 중요한 연구로, 생의학 분야의 포트폴리오 분석 등 실제 응용에 직접 활용 가능한 신뢰성 높은 결과를 제시했다.

## Related Papers

- 🏛 기반 연구: [[papers/1018_Science_Mapping_and_Science_Maps/review]] — 과학 매핑의 기본 원리와 방법론에 대한 종합적 이해를 제공하여 인용 분석 방법들의 맥락을 파악할 수 있다.
- 🔗 후속 연구: [[papers/1004_Quantifying_spatialtemporal_citation_diffusion_of_individual/review]] — 인용 기반 유사성 분석을 공간-시간적 인용 확산 패턴 분석으로 확장하여 더 동적인 관점을 제공한다.
- 🔄 다른 접근: [[papers/989_Modeling_Changing_Scientific_Concepts_with_Complex_Networks/review]] — 복잡 네트워크를 활용하여 과학 개념의 변화를 모델링하는 다른 접근법을 제시한다.
- 🧪 응용 사례: [[papers/1024_Software_survey_VOSviewer_a_computer_program_for_bibliometri/review]] — 서지계량학 방법론을 실제 분석에 적용하기 위한 도구적 접근을 제시한다
- 🔗 후속 연구: [[papers/977_Introducing_multiverse_analysis_to_bibliometrics_The_case_of/review]] — 서지계량학 분석에서 방법론적 다양성의 중요성을 멀티버스 분석으로 확장한다
- 🏛 기반 연구: [[papers/1071_Data_measurement_and_empirical_methods_in_the_science_of_sci/review]] — 과학학 분야의 데이터와 실증 방법론에 대한 포괄적 기초를 제공한다
- 🔄 다른 접근: [[papers/985_Mapping_scientific_communities_at_scale/review]] — 대규모 과학 공동체 매핑을 위한 링크 필터링 방법론이 기존 유사성 기반 방법들의 확장성 문제에 새로운 해결책을 제시한다.
- 🏛 기반 연구: [[papers/1009_Relative_Citation_Ratio_A_New_Metric_That_Uses_Citation_Rate/review]] — 공동인용 분석 방법론을 활용하여 학문 분야를 정의하고 인용 영향력을 정규화하는 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1024_Software_survey_VOSviewer_a_computer_program_for_bibliometri/review]] — 동시인용 분석과 서지결합이 VOSviewer의 핵심 클러스터링 알고리즘의 이론적 토대를 구성한다.
- 🏛 기반 연구: [[papers/1081_Science_Citation_IndexA_New_Dimension_in_Indexing_This_uniqu/review]] — 동시인용분석과 서지결합 등 현대 인용분석 기법의 이론적 토대를 제공한다.
- 🔗 후속 연구: [[papers/1053_Visualizing_the_context_of_citations_referencing_papers_publ/review]] — 전통적 동시인용 분석을 인용 맥락의 키워드 동시출현으로 확장한 혁신적 접근법을 보여준다.
- 🏛 기반 연구: [[papers/1073_MOLIERE_Automatic_Biomedical_Hypothesis_Generation_System/review]] — 문헌 간 인용 관계 분석 방법론이 자동 가설 생성 시스템의 기반 이론을 제공한다.
- 🔗 후속 연구: [[papers/990_Networks_of_Scientific_Papers/review]] — 동시인용, 서지결합, 직접인용 분석이 초기 인용 네트워크 연구를 정교화한 방법론으로 발전시킨다.
- 🔄 다른 접근: [[papers/985_Mapping_scientific_communities_at_scale/review]] — 링크 필터링 기반 과학 공동체 매핑이 기존 유사성 기반 서지계량학 방법들의 확장성 문제에 새로운 해결책을 제시한다.
- 🏛 기반 연구: [[papers/1144_Bibliometric_analysis_of_publications_titled_culinary_arts_s/review]] — 요리 예술 분야의 co-citation과 bibliographic coupling 분석의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1146_BIBLIOMETRIC_ANALYSIS_ON_PARENTING_STYLES_AND_ADOLESCENTS_HA/review]] — 부모 양육과 청소년 행복 연구의 co-citation과 co-word 분석 방법론의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1154_Contributions_of_accreditation_organizations_in_health_servi/review]] — 보건의료 인증 연구의 co-citation과 co-authorship 분석 방법론의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/926_A_bibliometric_analysis_of_bouldering_and_climbing_research/review]] — 서지계량학의 핵심 분석 방법들이 특정 분야 연구 동향 파악의 이론적 토대를 제공한다
- 🏛 기반 연구: [[papers/984_Mapping_Scholarly_Impact_Citation_Analysis_of_Commerce_Docto/review]] — 동시인용분석과 서지결합의 기본 방법론을 다룬 기초 연구로, 인용 네트워크 분석에 필요한 이론적 토대를 제공합니다.
