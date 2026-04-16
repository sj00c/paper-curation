---
title: "1009_Relative_Citation_Ratio_A_New_Metric_That_Uses_Citation_Rate"
authors:
  - "B. Ian Hutchins"
  - "Xin Yuan"
  - "James M. Anderson"
  - "George M. Santangelo"
date: "2016"
doi: "10.1371/journal.pbio.1002541"
arxiv: ""
score: 4.0
essence: "논문은 공동인용 네트워크(co-citation network)를 활용하여 학문 분야를 정규화한 상대인용비율(RCR: Relative Citation Ratio)이라는 새로운 논문 영향력 측정 지표를 제안한다. 기존의 저널임팩트팩터(JIF)와 h-지수의 한계를 극복하기 위해 개별 논문 수준에서 인용 영향력을 측정할 수 있는 방법론을 제시한다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Hutchins et al._2016_Relative Citation Ratio A New Metric That Uses Citation Rates to Measure Influence at the Article L.pdf"
---

# Relative Citation Ratio: A New Metric That Uses Citation Rates to Measure Influence at the Article Level

> **저자**: B. Ian Hutchins, Xin Yuan, James M. Anderson, George M. Santangelo | **날짜**: 2016 | **DOI**: [10.1371/journal.pbio.1002541](https://doi.org/10.1371/journal.pbio.1002541)

---

## Essence

![Figure 3](figures/fig3.webp)

*Fig 3. Algorithm for calculating the Relative Citation Ratio (RCR). (A) Article citation rate (ACR) is calculated as the*

논문은 공동인용 네트워크(co-citation network)를 활용하여 학문 분야를 정규화한 상대인용비율(RCR: Relative Citation Ratio)이라는 새로운 논문 영향력 측정 지표를 제안한다. 기존의 저널임팩트팩터(JIF)와 h-지수의 한계를 극복하기 위해 개별 논문 수준에서 인용 영향력을 측정할 수 있는 방법론을 제시한다.

## Motivation

- **Known**: 학술지 출판 및 인용 계량학(bibliometrics)은 연구 영향력 평가에 광범위하게 사용되고 있으나, 저널임팩트팩터와 h-지수 등 기존 지표들의 심각한 한계가 인정되고 있다. 이들 지표는 분야 간 편향, 게재 위치에 따른 왜곡, 협력 과학의 저평가 등의 문제를 가지고 있다.
- **Gap**: 기존 인용 정규화 방법들(journal-level normalization, citation percentiles, source normalization 등)은 이론적 이해는 높이지만 광범위한 채택이 이루어지지 않고 있다. 실무적으로 투명하고 자유롭게 접근 가능하며, 동료 비교 그룹을 기준으로 해석 가능한 통합적 벤치마킹 기능을 갖춘 지표가 부재하다.
- **Why**: 연구비 지원 기관과 채용 위원회는 수천 개의 경쟁 지원자 중에서 과학적 성공 가능성을 판단해야 하며, 신뢰성 있는 데이터 기반의 정규화된 지표는 암묵적 편향 완화와 다학제 연구 평가에 필수적이다.
- **Approach**: 각 논문의 공동인용 네트워크(함께 인용되는 논문들)를 활용하여 해당 분야의 기대 인용율(ECR: Expected Citation Rate)을 산출하고, 실제 인용율(ACR: Article Citation Rate)을 이로 정규화하는 방식으로 RCR을 계산한다. 특정 동료 비교 그룹에 대한 벤치마킹 기능을 포함한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig 4. RCRs correspond with expert reviewer scores. (A–C) Bubble plots of reviewer scores versus RCR for three different*

- **공동인용 네트워크 기반 분야 정규화**: 논문이 함께 인용되는 다른 논문들의 네트워크를 분석하여 학문 분야를 정확하게 식별하고, 해당 분야의 인용 행동을 반영한 정규화를 수행
- **개별 논문 수준의 측정**: 저널단위가 아닌 논문 수준에서 영향력을 평가함으로써 같은 저널 내 논문들 간의 큰 인용 차이를 포착
- **동료 비교 그룹 벤치마킹**: 교육 중심 기관, 개발도상국 등 동일한 맥락의 연구기관/국가 간 공정한 비교를 가능하게 하는 통합적 벤치마킹 기능 구현
- **전문가 의견과의 상관성 검증**: 88,835개 논문(2003-2010년 발표) 분석을 통해 RCR 값이 생의학 분야 주제 전문가 평가와 강한 상관관계를 보임을 입증
- **공개적 웹 도구 제공**: PubMed 논문의 RCR을 계산하고 관련 지표에 접근할 수 있는 무료 iCite 웹 도구(https://icite.od.nih.gov) 개발 및 공개

## How

![Figure 3](figures/fig3.webp)

*Fig 3. Algorithm for calculating the Relative Citation Ratio (RCR). (A) Article citation rate (ACR) is calculated as the*

- 각 논문의 참고문헌 목록에서 공동인용 관계를 분석하여 해당 논문이 속한 주제 영역을 정의하는 공동인용 네트워크 구축
- 같은 네트워크에 속한 논문들의 인용 분포를 분석하여 기대 인용율(ECR) 산출
- 발표 이후 경과 시간을 고려한 시간 정규화(예: citations per year) 적용
- 실제 인용율(ACR)을 기대 인용율(ECR)로 나누어 RCR 계산 (RCR = ACR / ECR)
- 선택 가능한 동료 비교 그룹(peer comparison group)을 설정하여 상대적 성과 평가
- 전문가 평가(NIH 동료 심사 점수) 데이터와의 상관성 분석을 통한 타당성 검증
- 정량적 방법론(회귀분석, 분위수 회귀)을 활용한 통계적 검증

## Originality

- 공동인용 네트워크를 인용 정규화의 기준으로 사용하는 혁신적 접근: 기존의 저널 카테고리나 주제 분류 시스템이 아닌, 실제 인용 행동 데이터를 기반으로 한 동적 분야 정의
- Relative Citation Rate'라는 동명의 기존 방법과 구별되는 새로운 방법론: 공동인용 네트워크의 위상적(topological) 특성을 활용한 독창적 계산 방식", '벤치마킹 기능의 혁신: 동료 비교 그룹의 성과에 대한 상대적 위치를 제시함으로써 맥락적 해석을 가능하게 한 첫 인용 기반 지표
- 텍스트 유사성이 아닌 인용 네트워크 구조를 기반으로 한 주제 정의: TF-IDF 등 전통적 텍스트 마이닝보다 정확한 학문적 근접성 파악

## Limitation & Further Study

- **PubMed 기반 데이터의 제한**: 생의학 분야에 최적화되어 있으며, 다른 학문분야(인문학, 사회과학 등)로의 적용 시 인용 행동의 차이로 인한 문제 가능성
- **초기 논문의 편향**: 출판 초기 인용이 많은 논문은 높은 RCR을 보이는 경향이 있어, 최근 발표 논문의 평가에 부정적 편향 존재 가능
- **공동인용 네트워크의 불완성**: 매우 새로운 논문이나 매우 전문화된 논문의 경우 공동인용 네트워크가 충분하지 않을 수 있음
- **자기인용(self-citation)의 처리**: 논문에서 언급되지 않았으며, 저자들의 자기인용이 RCR에 미치는 영향 분석 필요
- **후속 연구 방향**: (1) 다른 학문분야(물리학, 화학, 사회과학 등)에서의 RCR 타당성 검증, (2) 공동인용 네트워크 크기와 RCR 안정성 간의 관계 분석, (3) 자기인용 및 특정 인용 편향에 대한 민감도 분석, (4) 시간의 흐름에 따른 RCR의 변동성 연구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 공동인용 네트워크라는 혁신적 개념을 활용하여 분야 정규화와 벤치마킹을 동시에 해결하는 새로운 인용 지표를 제시함으로써, 오랫동안 문제시되어온 저널임팩트팩터의 오용을 실질적으로 극복할 수 있는 대안을 제공한다. 전문가 의견과의 강한 상관성 검증과 공개 웹 도구 제공을 통해 학술계의 광범위한 채택 가능성을 높였다.

## Related Papers

- 🔄 다른 접근: [[papers/1007_Redefining_Academic_Performance_The_Development_of_the_NK_Co/review]] — 논문 수준의 RCR과 연구자 수준의 NK 지수가 서로 다른 관점에서 학술 성과를 측정한다.
- 🏛 기반 연구: [[papers/944_Co-Citation_Analysis_Bibliographic_Coupling_and_Direct_Citat/review]] — 공동인용 분석 방법론을 활용하여 학문 분야를 정의하고 인용 영향력을 정규화하는 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1047_Theory_and_Practice_of_the_g-index/review]] — 기존의 g-지수 등 인용 기반 지표를 발전시켜 분야별 정규화를 통한 더 정확한 영향력 측정을 가능하게 한다.
- 🔄 다른 접근: [[papers/933_An_index_to_quantify_an_individuals_scientific_research_outp/review]] — h-index의 학문 분야별 편향을 해결하기 위해 공동인용 네트워크 기반의 정규화된 대안 지표를 제시합니다.
- ⚖️ 반론/비판: [[papers/1122_The_disruption_index_suffers_from_citation_inflation_Re-anal/review]] — 새로운 인용 지표의 유용성을 주장하는 반면, 기존 파괴성 지수가 인용 인플레이션으로 왜곡된다는 비판적 관점을 제시합니다.
- 🔗 후속 연구: [[papers/1001_Public_Profile_Matters_A_Scalable_Integrated_Approach_to_Rec/review]] — 인용 추천 시스템에서 상대인용비율과 같은 정규화된 지표를 활용하여 더 정확한 추천 성능을 달성할 수 있다.
- 🔄 다른 접근: [[papers/1007_Redefining_Academic_Performance_The_Development_of_the_NK_Co/review]] — 개별 논문 수준의 RCR 지표와 연구자 수준의 NK 지수가 상호 보완적으로 학술 성과를 평가할 수 있다.
- 🔗 후속 연구: [[papers/1047_Theory_and_Practice_of_the_g-index/review]] — 상대 인용 비율이라는 새로운 지표가 g-지수와 함께 인용 기반 영향력 측정의 다양한 접근법을 보여준다.
- 🔄 다른 접근: [[papers/1049_Universality_of_citation_distributions_Toward_an_objective_m/review]] — 학문분야 간 인용 차이를 보정하는 방법을 다루지만, 상대적 인용 비율보다는 보편적 곡선으로의 수렴에 초점을 맞춘다.
- 🔄 다른 접근: [[papers/1056_Where_Do_Your_Citations_Come_From_Citation-Constellation_A_F/review]] — RCR이 상대적 인용비를 통한 영향력 측정과 달리, 인용 네트워크의 사회구조적 경로를 분석하는 보완적 접근법을 제시한다.
- 🔄 다른 접근: [[papers/933_An_index_to_quantify_an_individuals_scientific_research_outp/review]] — h-index가 학문 분야별 차이를 반영하지 못하는 문제를 해결하기 위해 공동인용 네트워크 기반의 정규화된 인용 지표를 제안합니다.
- 🏛 기반 연구: [[papers/937_Authorship_titles_and_open_access_as_drivers_of_citation_per/review]] — 상대적 인용 비율 지표가 정형외과 논문의 인용 성과 동인 분석에 보다 정확한 비교 기준을 제공합니다.
- 🔄 다른 접근: [[papers/943_Citation_Analysis_as_a_Tool_in_Journal_Evaluation/review]] — 저널 영향도 평가를 전통적 인용 분석과 상대적 인용 비율이라는 다른 지표로 각각 측정
- 🔗 후속 연구: [[papers/1210_Scilit_with_the_Integrated_Impact_Indicator_Assessment/review]] — 상대인용비율(RCR) 개념을 확장하여 학제간 저널 평가에 특화된 지표로 발전시켰습니다.
- 🏛 기반 연구: [[papers/1167_Enabling_transparent_research_evaluation_A_method_for_histor/review]] — NIH의 RCR 지표 개발과 역사적 데이터 추출의 이론적 기반을 제공한다.
