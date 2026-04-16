---
title: "937_Authorship_titles_and_open_access_as_drivers_of_citation_per"
authors:
  - "Filippo Migliorini"
  - "Raju Vaishya"
  - "Fabrizio Rivera"
  - "Jörg Eschweiler"
  - "Philipp Kobbe"
date: "2026.03"
doi: "10.1186/s10195-026-00911-z"
arxiv: ""
score: 4.0
essence: "정형외과 논문 97,806개를 분석하여 저자 수, 제목 특성, 개방접근(OA) 출판이 인용 성과에 미치는 영향을 규명한 scientometric 연구"
tags:
  - "cat/Open_Access_Publication_Analytics"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Academic_Impact_and_Mobility"
  - "sub/Polymer_Science_Publication_Analytics"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Migliorini et al._2026_Authorship, titles and open access as drivers of citation performance in orthopaedics a scientometr.pdf"
---

# Authorship, titles and open access as drivers of citation performance in orthopaedics: a scientometric analysis

> **저자**: Filippo Migliorini, Raju Vaishya, Fabrizio Rivera, Jörg Eschweiler, Philipp Kobbe, Marcel Betsch, Francesco Oliva, Nicola Maffulli | **날짜**: 2026-03-20 | **DOI**: [10.1186/s10195-026-00911-z](https://doi.org/10.1186/s10195-026-00911-z)

---

## Essence


정형외과 논문 97,806개를 분석하여 저자 수, 제목 특성, 개방접근(OA) 출판이 인용 성과에 미치는 영향을 규명한 scientometric 연구

## Motivation

- **Known**: 다중 저자 논문과 개방접근 논문이 더 많은 인용을 받는다고 알려져 있으나, 정형외과 분야에서 제목 구조와 결합된 영향은 체계적으로 규명되지 않았음
- **Gap**: 정형외과 분야에서 저자 수, 제목 특성, OA 상태가 인용 성과에 미치는 복합적 영향을 대규모로 분석한 연구가 부족함
- **Why**: 연구자들이 윤리적 기준을 유지하면서 자신의 연구 영향력을 최대화할 수 있는 실증적 근거를 제공하고, 정형외과 출판 전략 수립에 기여할 수 있음
- **Approach**: 2010-2020년 Scopus 데이터베이스에서 정형외과 논문을 검색하여 다중선형회귀분석(multiple linear regression)으로 저자 수, 제목 특성(길이, 문장부호), OA 상태와 연간 정규화 인용률(citations/year)의 관계를 분석

## Achievement


- **저자 수와 인용 성과의 양의 상관**: 저자 1명 추가당 연 0.108건의 인용 증가 (β=0.108, p<0.001)
- **개방접근의 인용 이점**: OA 논문이 비-OA 논문 대비 연 0.175건 높은 인용률 달성 (p=0.001)
- **제목 특성의 차등적 영향**: 콜론(+0.314건/년), 대시(+0.187건/년)는 인용 증가, 물음표(-0.476건/년)와 전체 대문자(-0.71건/년)는 인용 감소
- **연구 설계별 인용 순위**: 네트워크 메타분석(6.64건/년) > 체계적 리뷰(5.66) > 메타분석(5.08) > 무작위 대조 시험(3.90) > 관찰 연구(2.40) > 증례 보고(0.77)
- **제목 길이의 이중 효과**: 문자 수는 양의 상관(β=0.023, p<0.001)이나 단어 수는 음의 상관(β=-0.183, p<0.001)

## How


- Scopus 데이터베이스에서 'orthopaedic' 키워드로 2010-2020년 논문 검색 (97,806개 논문 확보)", 'Python 3.11 및 Pandas 라이브러리를 사용하여 CSV 파일 처리 및 데이터 정제
- 종속변수로 '연간 인용률(citations_per_year)' 계산: 총 인용 수 ÷ 발표 이후 연수", '독립변수 표준화: 저자 수(연속형), OA 상태(이진형), 제목 특성(길이, 문장부호, 형식), 연구 설계 유형
- statsmodels 라이브러리로 OLS(Ordinary Least Squares) 다중선형회귀분석 수행
- 그룹별 비교 통계검정(comparative statistical testing)으로 제목 스타일 및 연구 설계 간 차이 평가
- 탐색적 모델링(exploratory modelling)으로 최고 인용률을 예측하는 저자 수와 제목 특성의 조합 식별

## Originality

- 정형외과 분야에 특화된 대규모 단일 학제(field-specific) 분석으로, 기존의 학제 간 또는 소규모 연구의 한계 극복
- 저자 수, 제목 특성, OA 상태의 **복합적 영향**을 동시에 분석한 통합 접근법
- 제목의 문자 수와 단어 수가 상반된 효과를 갖는다는 **새로운 발견**으로 제목 구성의 이중성 규명
- 연구 설계별 인용 성과의 명확한 위계 구조를 정량화하여 메타-분석류 논문의 인용 우위를 실증
- 정규화된 인용률(per-year normalization) 사용으로 출판 시간에 따른 편향 제거

## Limitation & Further Study

- Scopus만 사용하여 Web of Science, PubMed 등 다른 데이터베이스의 인용 패턴 미반영 가능
- 인용 수가 연구 질(research quality)과 완벽히 일치하지 않으며, 자기인용(self-citation) 제외 미실행
- 2010-2020년 데이터로 시간 경과에 따른 저자 수, OA 출판 정책의 변화 반영 제한
- 제목 특성(문장부호, 형식)의 인과관계는 규명되지 않았으며, 교란 변수(confounding variables) 미제어 가능성
- 후속 연구: (1) 자기인용 제외 후 재분석, (2) 다학제 데이터베이스 통합 비교, (3) 질적 내용 분석과 결합, (4) 저자 학파(school), 기관의 영향 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 정형외과 분야의 출판 특성과 인용 성과의 관계를 대규모 실증 데이터로 명확히 규명한 실용적이고 신뢰할 수 있는 연구로, 저자들이 윤리를 훼손하지 않으면서 학술 영향력을 최적화할 수 있는 증거 기반 지침을 제시함.

## Related Papers

- 🔗 후속 연구: [[papers/1226_Evaluating_Open_Access_Advantages_for_Citations_and_Altmetri/review]] — 개방접근의 인용 성과 영향을 정형외과 분야의 저자 수, 제목 특성과 결합한 구체적 분석으로 확장합니다.
- 🏛 기반 연구: [[papers/946_Collective_Credit_Allocation_in_Science/review]] — 과학에서의 집단적 크레딧 할당 이론이 정형외과 논문의 저자 수와 인용 성과 관계를 설명하는 기반이 됩니다.
- 🔗 후속 연구: [[papers/940_Bibliometrics_Global_Gender_Disparities_in_Science/review]] — 과학 출판에서 저자십과 관련된 성별 격차 문제를 정형외과 분야의 구체적 사례로 확장 분석한다.
- 🏛 기반 연구: [[papers/1034_The_Increasing_Dominance_of_Teams_in_Production_of_Knowledge/review]] — 팀 기반 지식 생산에서 저자 수가 연구 성과에 미치는 영향의 이론적 배경을 제공한다.
- 🔄 다른 접근: [[papers/1047_Theory_and_Practice_of_the_g-index/review]] — 인용 성과 측정을 위한 다른 지표인 g-index를 통해 저자십 효과를 평가할 수 있다.
- 🏛 기반 연구: [[papers/1009_Relative_Citation_Ratio_A_New_Metric_That_Uses_Citation_Rate/review]] — 상대적 인용 비율 지표가 정형외과 논문의 인용 성과 동인 분석에 보다 정확한 비교 기준을 제공합니다.
- 🔗 후속 연구: [[papers/1059_Women_are_credited_less_in_science_than_men/review]] — 저자 수와 인용 성과 관계 분석이 과학에서 여성의 신용 인정 부족 문제와 연결되어 성별 영향 분석으로 확장됩니다.
- 🔗 후속 연구: [[papers/1008_Reinforcing_Prestige_Journal_Citation_Biases_in_Astronomy/review]] — 저자 정보, 제목, 오픈액세스가 인용에 미치는 영향 분석은 저널 명성 편향 외에도 논문 인용에 영향을 주는 다른 요인들을 포괄적으로 다룹니다.
- 🔗 후속 연구: [[papers/1044_The_State_of_OA_A_Large-Scale_Analysis_of_the_Prevalence_and/review]] — 저자 신분, 제목, 오픈 액세스가 인용 성과에 미치는 복합적 영향을 분석한다.
- 🏛 기반 연구: [[papers/932_An_empirical_analysis_of_open_access_citation_advantages_in/review]] — 개방접근과 인용 성과 관계에 대한 일반적 분석이 특정 분야 연구의 기초를 제공한다
- 🔗 후속 연구: [[papers/954_Do_novel_papers_attract_more_social_attention/review]] — 오픈 액세스와 제목이 인용에 미치는 영향을 분석한 연구로, 소셜 미디어 주목도와 인용도 관계를 확장 연구할 수 있습니다.
- 🔗 후속 연구: [[papers/1226_Evaluating_Open_Access_Advantages_for_Citations_and_Altmetri/review]] — 저자십과 제목이 인용에 미치는 영향을 OA 이점 분석에 확장 적용한 연구입니다.
- 🔗 후속 연구: [[papers/1227_Exploring_Open_Access_Research_Trends_in_the_Indian_Council/review]] — 개방접근 출판 패턴 분석을 저자 속성과 인용 성과 측면에서 확장한 연구이다
