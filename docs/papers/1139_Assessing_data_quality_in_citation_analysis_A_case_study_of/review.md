---
title: "1139_Assessing_data_quality_in_citation_analysis_A_case_study_of"
authors:
  - "Guoyang Rong"
  - "Ying Chen"
  - "Thorsten Koch"
  - "Keisuke Honda"
date: "2026.03"
doi: "10.1016/j.joi.2026.101775"
arxiv: ""
score: 4.0
essence: "Web of Science와 Crossref 두 주요 인용 데이터 소스의 데이터 품질 차이를 분석하고, 통합 벤치마크 기반 GOLD 프레임워크를 개발하여 reference completeness와 key node inclusion을 체계적으로 평가한다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Rong et al._2026_Assessing data quality in citation analysis A case study of web of science and Crossref.pdf"
---

# Assessing data quality in citation analysis: A case study of web of science and Crossref

> **저자**: Guoyang Rong, Ying Chen, Thorsten Koch, Keisuke Honda | **날짜**: 03/2026 | **DOI**: [10.1016/j.joi.2026.101775](https://doi.org/10.1016/j.joi.2026.101775)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Framework of data quality assessment method.*

Web of Science와 Crossref 두 주요 인용 데이터 소스의 데이터 품질 차이를 분석하고, 통합 벤치마크 기반 GOLD 프레임워크를 개발하여 reference completeness와 key node inclusion을 체계적으로 평가한다.

## Motivation

- **Known**: 인용 분석은 데이터 품질에 크게 의존하며, 기존 연구들은 여러 데이터베이스의 coverage와 overlap을 비교했다. 하지만 citation network에서 key nodes와 그들의 인용 관계가 포함되었는지를 정량적으로 평가하는 방법은 부족하다.
- **Gap**: 기존 data quality assessment 방법들은 데이터 completeness를 진단하지만, 인용 네트워크의 영향력 있는 노드(key nodes)와 그들의 citation links 누락이 network metrics에 미치는 영향을 정량화하지 못한다. citation rank 변화에 따른 체계적인 분류 방법이 필요하다.
- **Why**: 부정확한 인용 데이터는 research evaluation 결과의 신뢰성과 비교가능성을 훼손하며, 특히 key nodes의 누락은 citation network 구조를 왜곡하여 편향된 network metrics를 생성한다.
- **Approach**: WoS와 Crossref를 통합하여 벤치마크 데이터셋을 구축하고, reference completeness와 key node inclusion 두 차원에서 target dataset을 평가한다. PageRank-inspired network metrics와 raw citation counts의 rank 변화를 비교하여 GOLD 프레임워크로 key node 누락 케이스를 분류한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2. Principle of ’GOLD’ framework.*

- **GOLD 프레임워크 개발**: raw citation count와 network metric rank의 변화 조합을 통해 key node 누락을 4가지 뚜렷한 케이스로 체계적으로 분류
- **다층적 평가**: dataset, publication, cluster 세 수준에서 publication coverage, reference completeness, key node inclusion을 평가할 수 있는 통합 방법론 제시
- **WoS와 Crossref 비교**: 두 데이터 소스 간 significant discrepancies 발견 및 이러한 차이가 citation analysis 결과에 미치는 영향 정량화
- **영향 받는 출판물 식별**: key node 누락으로 인해 영향을 받는 특정 출판물들을 체계적으로 식별

## How

![Figure 1](figures/fig1.webp)

*Fig. 1. Framework of data quality assessment method.*

- 두 데이터 소스(WoS, Crossref)를 통합하여 scale-matched benchmark dataset 구축
- Reference Coverage Rate (RCR)를 정의하여 reference completeness 측정
- 각 publication의 raw citation count와 PageRank-inspired metric 계산
- target dataset과 benchmark 간 rank 변화를 비교하여 4가지 GOLD 케이스 분류
- dataset, publication, cluster 레벨에서 통계적 분석 실시
- 시간별 연평균 인용 수 및 ASP (Average Statistic Parameter) 비교

## Originality

- 기존 data quality 평가 연구들과 달리, citation network의 key nodes 포함 여부를 정량적으로 측정하는 체계적 방법론 제시
- integration-based benchmark 방식을 활용하되, rank 변화 기반 GOLD 프레임워크로 노드 누락의 영향을 4가지 유형으로 구분
- PageRank-inspired metrics과 raw citation counts의 조합을 통해 network structural importance를 동시에 고려
- 다층적(dataset/publication/cluster) 평가 관점으로 data quality 문제의 영향 범위를 세분화

## Limitation & Further Study

- 벤치마크가 WoS와 Crossref 두 소스의 통합에만 한정되어, 30개 이상의 다른 인용 데이터 소스는 포함하지 못함
- 실제 최고 품질 벤치마크는 모든 인용 데이터 소스의 통합이어야 하지만, 현실적으로 달성 불가능한 상황에서 부분 벤치마크 사용
- GOLD 프레임워크의 4가지 케이스 분류 기준이 rank 변화에만 기반하므로, 다른 quality dimensions (예: metadata accuracy, 오류 유형)은 고려하지 못함
- 후속 연구: (1) 더 많은 데이터 소스를 포함한 다중 소스 통합 벤치마크 개발, (2) 도메인별 key node 정의 기준 정제, (3) metadata quality와 citation matching accuracy 평가 추가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 citation analysis의 data quality 평가에서 key node inclusion을 처음 체계적으로 정량화하는 GOLD 프레임워크를 제안하며, WoS와 Crossref의 구체적 비교를 통해 높은 실용성을 보여준다. 다만 벤치마크 구성의 한계와 평가 차원의 제한이 있어 향후 확장이 필요하다.

## Related Papers

- 🏛 기반 연구: [[papers/1115_Google_Scholar_Microsoft_Academic_Scopus_Dimensions_Web_of_S/review]] — Web of Science와 Crossref 외에 다른 주요 학술 데이터베이스들의 특성을 종합적으로 이해할 수 있다.
- 🧪 응용 사례: [[papers/1024_Software_survey_VOSviewer_a_computer_program_for_bibliometri/review]] — GOLD 프레임워크 개발에 VOSviewer 같은 bibliometric 도구의 적용 가능성을 탐색할 수 있다.
- 🔗 후속 연구: [[papers/1167_Enabling_transparent_research_evaluation_A_method_for_histor/review]] — 인용 데이터 품질 평가를 NIH RCR 데이터의 투명한 추출 방법과 연계하여 확장할 수 있다.
- 🔗 후속 연구: [[papers/992_OpenAlex_in_focus_Metadata_quality_of_publication_type_and_l/review]] — OpenAlex 메타데이터 품질 분석을 다른 주요 데이터베이스와의 체계적 비교로 발전시킨다
- 🧪 응용 사례: [[papers/1058_Why_Most_Published_Research_Findings_Are_False/review]] — 거짓 연구 결과 문제를 데이터 품질 관점에서 해결하는 실용적 접근법이다
- 🏛 기반 연구: [[papers/1071_Data_measurement_and_empirical_methods_in_the_science_of_sci/review]] — 과학의과학 분야의 데이터와 측정 방법론이 인용 분석 데이터 품질 평가의 이론적 토대를 제공하기 때문
- 🔗 후속 연구: [[papers/1115_Google_Scholar_Microsoft_Academic_Scopus_Dimensions_Web_of_S/review]] — 인용 데이터베이스 품질 평가 방법론을 다양한 데이터소스 비교로 확장한다
- 🔄 다른 접근: [[papers/992_OpenAlex_in_focus_Metadata_quality_of_publication_type_and_l/review]] — 인용 분석에서 데이터 품질을 평가한 연구로, OpenAlex 메타데이터와 다른 데이터베이스의 품질 평가 방법론을 제시하는 대안적 접근법입니다.
- 🔗 후속 연구: [[papers/1167_Enabling_transparent_research_evaluation_A_method_for_histor/review]] — NIH RCR 데이터의 투명한 추출을 인용 분석의 데이터 품질 평가와 연계하여 신뢰성을 높인다.
- 🔗 후속 연구: [[papers/1138_Arts_and_Humanities_Citation_Index_for_Research_Evaluation_i/review]] — 둘 다 주요 인용 데이터베이스의 데이터 품질 문제를 다루며 상호 보완적인 분석을 제공한다.
- 🔄 다른 접근: [[papers/1133_A_bibliometric_and_visualized_analysis_of_choriocapillaris_f/review]] — 인용 분석의 데이터 품질 평가가 맥락삭 연구의 bibliometric 분석에서 데이터 신뢰성 검증 방법을 제공한다.
