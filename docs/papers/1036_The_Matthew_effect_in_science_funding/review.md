---
title: "1036_The_Matthew_effect_in_science_funding"
authors:
  - "Thijs Bol"
  - "Mathijs de Vaan"
  - "Arnout van de Rijt"
date: "2018"
doi: "10.1073/pnas.1719557115"
arxiv: ""
score: 4.5
essence: "본 연구는 네덜란드 과학 펀딩 데이터를 분석하여 초기 펀딩 성공이 이후 펀딩 획득 확률을 2.5배 이상 증가시키는 Matthew effect를 실증적으로 검증했다. 흥미롭게도 이러한 펀딩 격차는 부분적으로 초기 실패자들의 재신청 포기에 의해 발생하는 '참여 메커니즘'에 의해 주도된다."
tags:
  - "cat/Academic_Impact_and_Mobility"
  - "cat/AI-Assisted_Scientific_Discovery"
  - "cat/Science_Policy_and_Research_Dynamics"
  - "sub/Scholar_Mobility_Patterns"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bol et al._2018_The Matthew effect in science funding.pdf"
---

# The Matthew effect in science funding

> **저자**: Thijs Bol, Mathijs de Vaan, Arnout van de Rijt | **날짜**: 2018 | **DOI**: [10.1073/pnas.1719557115](https://doi.org/10.1073/pnas.1719557115)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

본 연구는 네덜란드 과학 펀딩 데이터를 분석하여 초기 펀딩 성공이 이후 펀딩 획득 확률을 2.5배 이상 증가시키는 Matthew effect를 실증적으로 검증했다. 흥미롭게도 이러한 펀딩 격차는 부분적으로 초기 실패자들의 재신청 포기에 의해 발생하는 '참여 메커니즘'에 의해 주도된다.

## Motivation

- **Known**: 학계에서는 오랫동안 초기 성공이 누적적 우위(cumulative advantage)를 통해 향후 성공을 증가시키는 'Matthew effect'가 존재한다고 알려져 왔다. 다만 기존 연구는 관찰 데이터의 혼재 변수(confounding variables) 문제로 인해 인과관계를 확실히 입증하지 못했다.
- **Gap**: 과학 펀딩에서의 Matthew effect에 대한 체계적이고 인과적 증거가 부족했으며, 이 효과를 주도하는 구체적인 메커니즘(상태 효과 vs 참여 효과)이 명확히 규명되지 않았다.
- **Why**: 초기 커리어 단계의 펀딩은 과학자의 장기 경력 선택에 결정적 영향을 미치며, Matthew effect가 과학 메리토크래시를 훼손할 수 있기 때문에 이를 규명하는 것은 공정한 학문 생태계 구축에 필수적이다.
- **Approach**: 네덜란드 과학진흥재단(NWO)의 혁신펀딩제도 데이터를 이용하여 regression discontinuity design(RDD)을 적용했다. 펀딩 임계점(threshold) 근처의 신청자들을 비교함으로써 '거의 무작위'에 가까운 펀딩 성패를 자연실험으로 활용했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **Matthew effect 실증화**: 초기 경력 펀딩(Veni) 승자가 8년 후 중기 경력 펀딩(Vidi) 획득 확률이 낙선자 대비 2.5배 이상 높으며, 누적 펀딩액에서 €180,000 이상의 격차 발생
- **업적 기반이 아닌 지위 효과**: 초기 펀딩 승자의 향상된 성공률이 그로 인한 연구 업적(publications, citations, H-index)의 증가로 설명되지 않으며, 펀딩 자체가 자산으로 작용함을 시사
- **참여 메커니즘 규명**: 펀딩 격차의 일부가 초기 낙선자들의 재신청 의욕 저하 및 자발적 참여 감소로 인해 발생하는 행동학적 메커니즘임을 최초 입증
- **견고한 효과 크기**: 성별(여성/남성) 및 학문분야 전반에서 일관되게 관찰되는 효과로 높은 외적 타당성 확보

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- 데이터: 네덜란드 NWO의 Innovation Research Incentives Scheme에서 2000년 이후 총 €2.4억 규모 펀딩의 심사점수 및 펀딩 결정 전수 데이터 (3,660명 신청자)
- 방법: Regression discontinuity design을 통해 임계점 전후 신청자들의 예측 불가능한 펀딩 성패를 자연실험으로 활용
- 종속변수: (1) 중기 경력 펀딩 획득 확률, (2) 중기 경력 펀딩 신청 여부, (3) 누적 펀딩액 및 과학 성과 지표(출판수, 인용수, H-index)
- 독립변수: 초기 경력 펀딩 임계점 대비 신청자의 상대적 순위(±6/±5 ~ ±1/±2)
- 통제: 심사위원회 내 표준화 점수(within-committee z-score) 등을 통해 제안서 품질 차이 제어

## Originality

- **인과추론 혁신**: 기존 관찰 연구의 선택편향(selection bias) 문제를 회피하기 위해 hard threshold 정책을 활용한 RDD 설계로 '거의 무작위' 배치 달성", "**새로운 메커니즘 규명**: 상태 기반 Matthew effect가 아닌 행동학적 '참여 메커니즘'을 최초로 실증적으로 증명", '**시스템 수준 분석**: 개별 논문이 아닌 체계적 펀딩 배분 데이터 분석으로 학술 불평등의 구조적 근원 규명
- **종단 추적**: 8년 이상의 장기 추적으로 누적 이점의 동적 변화 포착

## Limitation & Further Study

- **지역 특수성**: 네덜란드 단일 펀딩 프로그램 데이터로, 다른 국가 및 펀딩 기관의 보편성 미확인
- **메커니즘의 부분적 설명**: 참여 감소가 전체 펀딩 격차의 일부만 설명하며, 나머지는 심사자의 지위 편향(status bias) 등 다른 메커니즘 존재 가능성
- **성공 기준의 한계**: 펀딩 획득만 측정되며, 펀딩 미획득자의 대체 경로(국제 펀딩, 산업 진출 등) 미추적
- **후속 연구**: (1) 다국가 다기관 비교연구로 구조적 보편성 검증, (2) 심사자 피드백 분석을 통한 지위 편향 메커니즘 규명, (3) 멘토링 등 개입 효과 검증

## Evaluation

- Novelty: 5/5
- Technical Soundness: 4/5
- Significance: 5/5
- Clarity: 4/5
- Overall: 4.5/5

**총평**: 본 연구는 인과추론 방법론과 풍부한 행정 데이터를 결합하여 학계의 오랜 이론을 실증적으로 검증하고, 특히 행동학적 '참여 메커니즘'이라는 새로운 설명 경로를 제시함으로써 과학 불평등 연구에 중요한 기여를 한다. 다만 단일 국가 데이터의 한계와 메커니즘의 부분적 설명력 수준은 추후 연구로 보완 필요하다.

## Related Papers

- 🔗 후속 연구: [[papers/956_Early_career_setback_and_future_achievement_in_professional/review]] — 초기 펀딩 실패가 미래 경력에 미치는 영향을 분석하여 Matthew effect의 시간적 차원을 확장한다.
- 🧪 응용 사례: [[papers/1026_Systematic_Inequality_and_Hierarchy_in_Faculty_Hiring_Networ/review]] — 학계 채용에서 나타나는 체계적 불평등 현상이 펀딩 격차와 어떻게 연결되는지 보여준다.
- 🔗 후속 연구: [[papers/996_Partisan_disparities_in_the_funding_of_science_in_the_United/review]] — 과학 펀딩에서의 Matthew effect가 정치적 성향에 따른 차별적 지원으로까지 확장되어 나타나는 양상을 보여줍니다.
- ⚖️ 반론/비판: [[papers/1121_Superstar_Extinctionsupsup/review]] — 슈퍼스타 과학자의 사망이 오히려 후속 연구자들에게 기회를 제공한다는 관점에서 Matthew effect의 지속성에 대해 다른 시각을 제시합니다.
- 🔄 다른 접근: [[papers/1012_Rethink_Funding_by_Putting_the_Lottery_First/review]] — 추첨 기반 펀딩 시스템은 Matthew effect로 인한 편향된 자금배분을 완화할 수 있는 혁신적 대안을 제시합니다.
- 🏛 기반 연구: [[papers/964_Funding_the_Frontier_Visualizing_the_Broad_Impact_of_Science/review]] — 과학 펀딩의 광범위한 영향을 시각화하는 연구는 Matthew effect가 어떻게 전체 과학 생태계에 파급효과를 미치는지 이해하는 기반이 됩니다.
- 🏛 기반 연구: [[papers/1007_Redefining_Academic_Performance_The_Development_of_the_NK_Co/review]] — 과학 펀딩에서의 Matthew 효과가 학술 성과 평가 지표 개발 시 고려해야 할 구조적 불평등을 보여준다.
- 🏛 기반 연구: [[papers/1026_Systematic_Inequality_and_Hierarchy_in_Faculty_Hiring_Networ/review]] — 학계의 체계적 불평등과 명성 기반 계층 구조가 과학 펀딩에서 Matthew effect가 발생하는 구조적 배경을 제공합니다.
- ⚖️ 반론/비판: [[papers/1111_A_Strategic_Guide_to_White_Space_Analysis_for_Pharmaceutical/review]] — 매튜 효과로 인한 불균등한 자금 배분 문제를 백색공간 분석으로 완화할 수 있는 대안 제시
- 🔄 다른 접근: [[papers/1069_Breaking_the_gatekeepers_how_AI_will_revolutionize_scientifi/review]] — 과학 펀딩의 권력 구조 문제를 다루지만, 마태 효과의 누적적 불이익보다는 AI를 통한 혁신적 해결 방안에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/996_Partisan_disparities_in_the_funding_of_science_in_the_United/review]] — 과학 펀딩에서의 마태 효과와 정당별 펀딩 격차가 과학 투자의 불평등 구조를 다각도로 조명한다.
- 🏛 기반 연구: [[papers/941_Big_Names_or_Big_Ideas_Do_Peer-Review_Panels_Select_the_Best/review]] — 과학 기금 배분에서 Matthew 효과가 동료평가 점수와 실제 성과 간 관계에 미치는 영향을 이해하는 배경을 제공합니다.
- 🏛 기반 연구: [[papers/964_Funding_the_Frontier_Visualizing_the_Broad_Impact_of_Science/review]] — 과학 펀딩에서의 매튜 효과에 대한 이론적 이해를 제공하여 펀딩 영향 분석의 배경을 마련한다.
- 🔗 후속 연구: [[papers/966_Global_citation_inequality_is_on_the_rise/review]] — 과학 펀딩에서 마태 효과가 글로벌 인용 불평등 증가의 구조적 원인 중 하나로서 불평등 심화 메커니즘을 설명한다.
- 🏛 기반 연구: [[papers/983_Mapping_Research_Funding_and_Outputs_at_the_Topic_Level_in_t/review]] — 과학 펀딩에서의 매튜 효과에 대한 이론적 이해를 제공하여 펀딩-성과 관계의 복잡성을 파악할 수 있다.
