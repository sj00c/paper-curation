---
title: "1031_The_Chaperone_Effect_in_Scientific_Publishing"
authors:
  - "Vedran Sekara"
  - "Pierre Deville"
  - "Sebastian E. Ahnert"
  - "Albert-László Barabási"
  - "Roberta Sinatra"
date: "2018.12"
doi: "10.1073/pnas.1800471115"
arxiv: ""
score: 4.0
essence: "과학 논문 출판에서 경험 많은 과학자(선임저자)가 특정 저널에 이전 경험이 있을 때 더 높은 출판 성공률을 보이는 '샤페론 효과(chaperone effect)'를 정량적으로 분석한 연구이다."
tags:
  - "cat/Open_Access_Publication_Analytics"
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Computational_Bibliometric_Analysis"
  - "sub/Polymer_Science_Publication_Analytics"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Sekara et al._2018_The chaperone effect in scientific publishing.pdf"
---

# The chaperone effect in scientific publishing

> **저자**: Vedran Sekara, Pierre Deville, Sebastian E. Ahnert, Albert-László Barabási, Roberta Sinatra, Sune Lehmann | **날짜**: 2018-12-11 | **DOI**: [10.1073/pnas.1800471115](https://doi.org/10.1073/pnas.1800471115)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Probability of being listed as PI in Nature given previous publication history. a, Terminology of authors. The l*

과학 논문 출판에서 경험 많은 과학자(선임저자)가 특정 저널에 이전 경험이 있을 때 더 높은 출판 성공률을 보이는 '샤페론 효과(chaperone effect)'를 정량적으로 분석한 연구이다.

## Motivation

- **Known**: 과학은 계층화된 구조를 가지며, 성공한 멘토와 상호작용하는 젊은 과학자들이 경력에서 더 높은 성취를 이룬다는 것이 알려져 있다. 또한 저자 순서는 각 과학자의 역할을 나타내는 중요한 신호이다.
- **Gap**: 과학 출판에서 멘토십 과정의 구체적인 역할, 특히 특정 저널에서의 출판 경험이 선임저자 지위 획득에 미치는 정량적 영향에 대한 이해가 부족하다.
- **Why**: 특정 저널에서의 경험이 고영향력 논문 출판 가능성에 미치는 영향을 이해하는 것은 과학자 경력 발전 경로와 과학적 우수성 전승 메커니즘을 밝히는 데 중요하다.
- **Approach**: 1960-2012년 사이에 발표된 386개 과학 저널의 610만 편 논문을 분석하여, 선임저자(PI: Principal Investigator)를 신규(new), 샤페론(chaperoned), 기성(established) 세 범주로 분류하고, 저널별·분야별로 샤페론 효과의 크기를 비교한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Probability of being listed as PI in Nature given previous publication history. a, Terminology of authors. The l*

- **저널별 샤페론 효과의 이질성**: 의학 및 생물 과학에서 샤페론 효과가 강하게 나타나며, 자연 과학에서는 더 약하다는 것을 증명했다.
- **고영향력 저널의 진입 장벽**: Nature, Science 등 다분야 고영향력 저널에서는 이전 출판 경험 없이 선임저자로 출판할 확률이 크게 감소하는 추세가 확인되었다.
- **샤페론 효과의 성과**: 샤페론 또는 기성 선임저자의 논문이 신규 선임저자의 논문보다 높은 평균 영향력(impact)을 가진다는 것을 정량화했다.
- **시간별 변화 추적**: Nature의 신규 선임저자 비율이 시간 경과에 따라 유의미하게 감소하여, 고영향력 저널의 진입 장벽이 증가하고 있음을 보여주었다.

## How


- 6.1백만 개의 논문 데이터셋 구성 (1960-2012년, 5개 분야, 386개 저널 포함)
- 저자명 동일성 확인(name disambiguation) 및 데이터 정제 수행
- 선임저자를 마지막 저자 위치 기준으로 분류 (각 저널별 선임저자 정의 기반)
- 각 저널에서 연도별 신규/샤페론/기성 선임저자 비율 계산
- 과학 분야(수학, 물리, 화학, 생물, 의학)별 샤페론 효과 비교
- 논문 영향력(citation impact) 분석으로 샤페론 효과의 실질적 성과 검증
- 알파벳순 귀무 모델(alphabetical null model) 구성으로 통계적 유의성 확인

## Originality

- 저자 순서 데이터를 활용하여 '샤페론 효과'라는 새로운 개념을 정량적으로 정의하고 측정한 점", '대규모 다중 저널 데이터셋(610만 편)을 통해 과학 전반에 걸친 패턴을 체계적으로 분석한 첫 시도
- 저널, 분야, 시간 축을 동시에 고려한 다차원적 분석으로 과학 출판 메커니즘의 복잡성을 포착
- 과학적 우수성 전승과 경력 발전 경로에 대한 정량적 실증 증거 제시

## Limitation & Further Study

- 마지막 저자가 항상 선임저자(PI)를 나타낸다는 가정이 모든 저널과 분야에 일관되게 적용되지 않을 수 있다.
- 저자명 동일성 확인 과정에서의 오류가 분석 결과에 영향을 미칠 수 있다.
- 인용수(citation impact)가 논문의 진정한 질(quality)을 완벽히 대표하지 못할 수 있다.
- 샤페론 효과가 저널 정책, 편집자의 선택 편향, 또는 다른 사회문화적 요인에 의해 강화될 수 있는 점을 충분히 논의하지 않았다.
- **후속 연구**: 특정 분야에서 샤페론 효과가 강한 이유에 대한 심층 질적 분석 필요, 멘토십의 구체적 메커니즘과 지식 이전 과정의 추적, 저널 정책 및 편집 관행이 샤페론 효과에 미치는 영향 조사

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 과학 출판의 숨겨진 메커니즘인 '샤페론 효과'를 대규모 데이터로 처음 정량화한 중요한 연구로, 과학자 경력 발전과 학문적 우수성 전승에 대한 새로운 통찰을 제공한다. 결과의 명확성과 실증적 증거가 강력하며, 과학정책 및 학문 공동체의 개선에 실질적 기여할 수 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1008_Reinforcing_Prestige_Journal_Citation_Biases_in_Astronomy/review]] — 저널 명성 기반 인용 편향이 개별 연구자 수준에서 나타나는 샤페론 효과의 거시적 맥락을 제공한다.
- ⚖️ 반론/비판: [[papers/941_Big_Names_or_Big_Ideas_Do_Peer-Review_Panels_Select_the_Best/review]] — 동료 심사에서 빅네임 효과가 샤페론 효과와 유사한 메커니즘으로 작동하는지 비교 분석이 필요하다.
- 🏛 기반 연구: [[papers/956_Early_career_setback_and_future_achievement_in_professional/review]] — 초기 경력 좌절이 샤페론 없는 연구자들의 출판 성공률에 미치는 장기적 영향을 보여준다.
- 🔗 후속 연구: [[papers/1032_The_Diversity-Innovation_Paradox_in_Science/review]] — 출판 성공에서의 샤페론 효과와 소수집단의 혁신 과소평가가 모두 과학계의 구조적 불평등을 드러낸다.
- 🏛 기반 연구: [[papers/1026_Systematic_Inequality_and_Hierarchy_in_Faculty_Hiring_Networ/review]] — 학술 채용 네트워크의 위계와 출판에서의 샤페론 효과가 모두 과학계 내 체계적 불평등의 메커니즘을 설명한다.
- ⚖️ 반론/비판: [[papers/981_Making_gender_diversity_work_for_scientific_discovery_and_in/review]] — 샤페론 효과의 긍정적 측면과 성별 다양성이 과학 발견에 미치는 영향을 균형적으로 비교할 수 있다.
- 🏛 기반 연구: [[papers/1046_The_structure_of_scientific_collaboration_networks/review]] — 과학 협력 네트워크의 구조적 이해가 샤페론 효과의 사회적 네트워크 메커니즘을 설명하는 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1008_Reinforcing_Prestige_Journal_Citation_Biases_in_Astronomy/review]] — 샤페론 효과가 개별 연구자 수준에서 나타나는 저널 출판 편향을 보여주는 미시적 관점을 제공한다.
- 🔗 후속 연구: [[papers/1032_The_Diversity-Innovation_Paradox_in_Science/review]] — 출판에서의 샤페론 효과와 함께 소수집단의 혁신 기여 과소평가가 과학계 불평등의 다면적 양상을 보여준다.
- 🧪 응용 사례: [[papers/1123_The_misalignment_of_incentives_in_academic_publishing_and_im/review]] — 과학 출판에서의 후견인 효과가 인센티브 왜곡에 미치는 구체적 사례다.
- 🏛 기반 연구: [[papers/1142_Beyond_Retractions_Forensic_Scientometrics_Techniques_to_Ide/review]] — 학술 출판에서 동료 검토의 영향과 한계를 이해하여 부정행위 탐지 맥락을 제공한다.
