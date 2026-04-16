---
title: "979_Large_teams_develop_and_small_teams_disrupt_science_and_tech"
authors:
  - "Lingfei Wu"
  - "Dashun Wang"
  - "James A. Evans"
date: "2019.02"
doi: "10.1038/s41586-019-0941-9"
arxiv: ""
score: 4.0
essence: "65백만 개 이상의 논문, 특허, 소프트웨어 제품 분석을 통해 소규모 팀은 과학기술을 혁신(disrupt)하고 대규모 팀은 기존 아이디어를 발전(develop)시킨다는 것을 입증했다."
tags:
  - "cat/AI-Assisted_Scientific_Discovery"
  - "cat/Academic_Impact_and_Mobility"
  - "cat/Open_Access_Publication_Analytics"
  - "sub/Scientific_Language_Model_Development"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wu et al._2019_Large teams develop and small teams disrupt science and technology.pdf"
---

# Large teams develop and small teams disrupt science and technology

> **저자**: Lingfei Wu, Dashun Wang, James A. Evans | **날짜**: 2019-02-21 | **DOI**: [10.1038/s41586-019-0941-9](https://doi.org/10.1038/s41586-019-0941-9)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2 | Small teams disrupt whereas large teams develop. a–c, For*

65백만 개 이상의 논문, 특허, 소프트웨어 제품 분석을 통해 소규모 팀은 과학기술을 혁신(disrupt)하고 대규모 팀은 기존 아이디어를 발전(develop)시킨다는 것을 입증했다.

## Motivation

- **Known**: 과학기술 분야에서 팀 규모의 증가 추세가 관찰되고 있으며, 이는 전문화, 통신기술 발전, 학제간 협력 필요성 때문으로 알려져 있다. 그러나 팀 규모가 지식발견과 기술혁신에 최적화되어 있는지는 증거 부족 상태이다.
- **Gap**: 대규모 팀이 더 많은 인용을 받는다는 것은 알려져 있으나, 단순 인용 수만으로는 혁신적 기여와 발전적 기여를 구분할 수 없다. 팀 규모와 과학기술의 혁신성(disruption) 간의 체계적 관계는 규명되지 않았다.
- **Why**: 과학기술 정책과 자금 배분이 대규모 팀 중심으로 편향되어 있는 현황에서, 소규모 팀의 혁신적 역할을 입증함으로써 다양한 팀 규모를 지원하는 균형잡힌 정책 수립의 근거를 제공한다.
- **Approach**: 세 가지 출처(Web of Science 논문, US 특허, GitHub 소프트웨어)에서 수집한 65백만 개 데이터에 대해 disruption 지수(-1~1)를 계산하여 팀 규모별 과학기술의 혁신성을 정량적으로 측정하고 비교 분석했다.

## Achievement


- **팀 규모와 혁신성의 역관계**: 팀이 1명에서 50명으로 증가할 때 논문, 특허, 소프트웨어의 disruption 점수가 각각 70, 30, 50 백분위수 감소
- **고임팩트 작업의 명확한 분화**: 상위 5% 인용 수준에서 솔로 저자는 고임팩트 논문 생산 확률이 10인 팀과 동등하나, 혁신적 논문 생산 확률은 72% 더 높음
- **시간과 분야에 걸친 일관성**: 1954-2014년 전 기간과 90% 학문 분야에서 팀 규모와 disruption의 음의 상관관계 일관되게 관찰
- **disruption 지수의 타당성 검증**: 노벨상 수상 논문이 상위 2% disruption 분포에 위치, BTW 모델 논문(혁신)은 상위 1%, Bose-Einstein 응축 논문(발전)은 하위 3%에 위치

## How

![Figure 1](figures/fig1.webp)

*Fig. 1 | Quantifying disruption. a, Simplified illustration of disruption.*

- Web of Science에서 42백만 논문(611백만 인용), USPTO에서 500만 특허(6500만 인용), GitHub에서 1600만 소프트웨어 프로젝트와 900만 포크 수집
- Citation displacement를 기반으로 한 disruption 지수 D = (p_i - p_j)/(n_i + n_j + n_k) 계산 (i: 해당 논문, j: 인용된 논문, k: 동시 인용 논문)
- 팀 규모별로 disruption 점수의 분포를 분석하고 백분위 변화 측정
- 고임팩트 작업(상위 5% 인용)에 대해 별도 분석 실행
- 시간 기간, 학문 분야, 논문 유형(이론/경험, 리뷰/원저)별 층화 분석 실행
- arXiv 매칭을 통해 논문의 그림 개수로 이론-경험 구분 후 통제 분석 실행

## Originality

- **disruption 지수의 새로운 적용**: 기존 특허 분석용 지수를 학술 논문, 특허, 소프트웨어에 걸쳐 대규모로 체계적 적용
- **세 도메인 통합 분석**: 65백만 개 규모의 이질적 데이터 소스를 동일한 개념으로 통합 분석하여 보편적 패턴 규명
- **개별 수준 분석**: 토픽과 연구 설계 통제 후에도 팀 크기 효과가 개인 수준에서 발생함을 입증 (사람들의 팀 이동 추적)
- **고임팩트 작업의 역설 발견**: 대규모 팀이 높은 임팩트 작업을 더 잘 생산하지만, 그것들이 오히려 덜 혁신적이라는 역설적 발견

## Limitation & Further Study

- **출판 및 인용 편향**: 소규모 팀의 혁신 작업이 즉시 인용되지 않고 미래에 평가될 가능성이 높아 현재 데이터로는 잠재적 혁신을 과소평가할 가능성
- **분야별 예외**: 컨퍼런스 중심의 컴퓨터 공학과 공학 분야에서 패턴이 약화되어 출판 문화에 따른 편향 존재
- **인과관계 미규명**: 팀 규모가 혁신성을 직접 결정하는지, 아니면 혁신적 사람들이 소규모 팀을 선택하는지는 미결정
- **GitHub 데이터 한계**: 2011-2014년 최근 4년만 포함하여 장기 추세 관찰 부족
- **후속 연구 필요**: 팀 조성(다양성, 위계), 기금 배분, 기관 구조 등 팀 성과에 영향미치는 다른 요인들에 대한 추가 조사 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 팀 규모와 혁신성 관계에 대한 과학적 증거를 대규모 데이터로 처음 체계적으로 제시한 중요한 연구이며, 과학정책 수립에 직접적 함의를 제공한다. 다만 인과관계 규명과 분야별 메커니즘에 대한 추가 연구가 필요하다.

## Related Papers

- 🔗 후속 연구: [[papers/1034_The_Increasing_Dominance_of_Teams_in_Production_of_Knowledge/review]] — 팀 크기와 지식 생산 간의 관계를 더 깊이 탐구하여 팀 규모가 과학적 혁신에 미치는 영향을 확장 분석한다.
- 🔄 다른 접근: [[papers/965_Gender-diverse_teams_produce_more_novel_and_higher-impact_sc/review]] — 팀 구성에서 규모 대신 성별 다양성이 혁신적 연구 성과에 미치는 영향을 다른 관점에서 조명한다.
- 🔗 후속 연구: [[papers/1010_Remote_collaboration_fuses_fewer_breakthrough_ideas/review]] — 원격 협업 환경에서도 소규모 팀의 혁신적 아이디어 융합 능력이 제한된다는 것을 보여주어 팀 규모 이론을 보완한다.
- 🏛 기반 연구: [[papers/995_Papers_and_patents_are_becoming_less_disruptive_over_time/review]] — 과학기술 분야에서 혁신성(disruptiveness)이 시간에 따라 감소하는 현상의 근본적 증거를 제공한다.
- 🏛 기반 연구: [[papers/1005_Quantifying_the_dynamics_of_failure_across_science_startups/review]] — 대규모 팀과 소규모 팀의 차별화된 역할은 실패와 성공의 동역학이 팀 구성에 따라 다르게 나타날 수 있음을 시사합니다.
- 🔗 후속 연구: [[papers/1010_Remote_collaboration_fuses_fewer_breakthrough_ideas/review]] — 대규모 팀과 소규모 팀의 차이에 더해 물리적 거리가 혁신성에 미치는 영향을 추가로 분석한다.
- 🔗 후속 연구: [[papers/1034_The_Increasing_Dominance_of_Teams_in_Production_of_Knowledge/review]] — 대규모 팀과 소규모 팀의 차별적 역할 분석은 팀 기반 지식 생산의 증가가 혁신의 성격에 미치는 영향을 더 자세히 규명합니다.
- 🧪 응용 사례: [[papers/1117_Human-Modeling_in_Sequential_Decision-Making_An_Analysis_thr/review]] — 대규모 팀과 소규모 팀의 혁신 방식 차이가 인간-AI 협력에서 팀 구성 전략에 실용적 시사점을 제공하기 때문
- 🏛 기반 연구: [[papers/1066_Accelerating_science_with_human-aware_artificial_intelligenc/review]] — 대규모 팀과 소규모 팀의 과학 발전 메커니즘 차이를 이해하여, 인간 중심 AI가 포착해야 할 과학적 발견의 사회적 역학을 제공한다.
- 🔗 후속 연구: [[papers/995_Papers_and_patents_are_becoming_less_disruptive_over_time/review]] — 대규모 팀과 소규모 팀의 혁신 패턴 차이가 혁신성 감소 현상의 팀 구성 요인을 설명한다.
- 🏛 기반 연구: [[papers/960_Evolution_of_the_social_network_of_scientific_collaborations/review]] — 협력 네트워크의 진화가 과학적 발견과 기술 혁신에 미치는 영향을 이해하는 기초를 제공한다.
- 🏛 기반 연구: [[papers/977_Introducing_multiverse_analysis_to_bibliometrics_The_case_of/review]] — 대규모 팀은 개발하고 소규모 팀은 파괴적 연구를 한다는 원본 연구로, 다중우주분석의 검증 대상이 되는 기초 연구입니다.
- 🏛 기반 연구: [[papers/1170_Evolution_of_Social_Work_Knowledge_Production_Over_35_Years/review]] — 사회복지 분야의 협력 증대와 팀 규모 변화를 과학기술에서 대규모 팀의 역할 이론으로 설명할 수 있다.
- 🏛 기반 연구: [[papers/1212_Shifts_in_Biotechnology_Research_Fronts_20002026_A_Bibliomet/review]] — 대형팀과 소규모팀의 과학기술 발전 역할이 생명공학 연구 전환의 배경을 설명합니다.
