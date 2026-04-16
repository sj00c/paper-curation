---
title: "1040_The_Price-Pareto_growth_model_of_networks_with_community_str"
authors:
  - "Łukasz Brzozowski"
  - "Marek Gagolewski"
  - "Grzegorz Siudem"
  - "Barbara Żogała-Siudem"
date: "2026.02"
doi: "10.48550/arXiv.2510.13392"
arxiv: ""
score: 4.0
essence: "커뮤니티 구조를 가진 네트워크의 도수 수열(degree sequence)을 모델링하기 위해 Price 모델을 확장한 Price-Pareto 성장 모델을 제안한다. 각 커뮤니티별로 이질적인 인용 역학을 포착할 수 있는 분석적 틀을 제공한다."
tags:
  - "cat/Science_Policy_and_Research_Dynamics"
  - "cat/Academic_Impact_and_Mobility"
  - "sub/Gender_Citation_Imbalance"
  - "topic/scisci"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Brzozowski et al._2026_The Price-Pareto growth model of networks with community structure.pdf"
---

# The Price-Pareto growth model of networks with community structure

> **저자**: Łukasz Brzozowski, Marek Gagolewski, Grzegorz Siudem, Barbara Żogała-Siudem | **날짜**: 2026-02-23 | **DOI**: [10.48550/arXiv.2510.13392](https://doi.org/10.48550/arXiv.2510.13392)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Example model-predicted node in-degree sequences for communities in a graph with 𝑁= 30,000 nodes and*

커뮤니티 구조를 가진 네트워크의 도수 수열(degree sequence)을 모델링하기 위해 Price 모델을 확장한 Price-Pareto 성장 모델을 제안한다. 각 커뮤니티별로 이질적인 인용 역학을 포착할 수 있는 분석적 틀을 제공한다.

## Motivation

- **Known**: Price의 누적 이득(cumulative advantage) 모델과 Barabási-Albert 모델은 우선 결합(preferential attachment)을 통해 멱법칙 분포를 설명했으나, 균질성을 가정하여 다양한 과학 분야의 이질적인 인용 문화를 포착하지 못한다.
- **Gap**: 기존 인용 네트워크 모델은 전역적 균질성을 가정하거나 (BA, Price, 3DSI), 커뮤니티 구조를 포함하면서도 해석 불가능한 복잡한 블랙박스 모델(GNN, GVA)이 되는 문제가 있다. 커뮤니티 구조를 가진 네트워크의 동적 성장을 분석적으로 모델링할 수 있는 도구가 부족하다.
- **Why**: 과학 분야마다 다른 성장률과 인용 문화를 가지므로, 다양한 학문 영역의 특성을 반영하는 이질적(heterogeneous) 네트워크 모델이 필수적이다. 이는 실제 인용 네트워크의 구조를 정확하게 이해하고 예측하는 데 중요하다.
- **Approach**: 3DSI 모델을 커뮤니티 구조로 확장하여, 각 커뮤니티별로 우연적(accidental) 인용과 선호적(preferential) 인용을 구분하여 모델링한다. 도출된 모수 추정자를 통해 실제 인용 네트워크에 적합시킬 수 있다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Complementary cumulative distribution functions of the observed and modelled in-degree sequences in the seven*

- **커뮤니티 구조 기반 분석 틀**: 각 클러스터의 인용 수를 기술하는 분석 공식 도출
- **지니 지수 계산**: 각 커뮤니티 내 도수 분포의 불평등을 정량화하는 방법 제시
- **Pareto 타입 II 분포 수렴 증명**: 각 커뮤니티의 인용 수 분포가 파레토 분포로 수렴함을 이론적으로 증명
- **모수 추정자 개발**: 실제 인용 네트워크에 모델을 적합할 수 있는 통계적 추정 방법 도출
- **이질적 역학 포착**: 서로 다른 과학 분야의 뚜렷한 성장 비율과 인용 문화를 모델링 가능

## How


- 3DSI 모델의 확장: 우연적 인용(random) 성분과 선호적 인식(preferential) 성분의 혼합
- 각 커뮤니티에 독립적 모수 할당: 커뮤니티별 생산성(productivity), 총 영향력(impact), 행운도(luck) 설정
- 점근 분석: 대규모 네트워크에서 도수 분포의 극한 거동 분석
- Gini 지수 공식 유도: 분포 불평등을 정량적으로 측정
- 실데이터 적합: 도출된 모수 추정자를 이용한 최대우도 추정(MLE) 또는 모멘트 방법 적용

## Originality

- 선호적 결합과 커뮤니티 구조를 동시에 다루는 첫 분석적 모델: 기존 연구는 둘 중 하나만 처리
- 커뮤니티별 이질적 모수 도입: 균질성 가정을 완화하여 현실적 네트워크 표현
- 폐쇄형 분석 공식 제공: 블랙박스 신경망 모델과 달리 해석 가능한 수학적 결과 제시
- Pareto 분포 수렴성 증명: 개별 커뮤니티 수준에서의 이론적 보장 제공

## Limitation & Further Study

- 커뮤니티 사전 정의 필요: 외생적으로 주어지거나 알고리즘으로 발견된 커뮤니티 필요 (커뮤니티 검출 능력 부재)
- 연결 편향성(assortative) 가정: 같은 커뮤니티 내 인용이 높다는 가정이 모든 네트워크에 성립하지 않을 수 있음
- 시간 역학의 제한: 논문의 나이에 따른 관심도 감쇠(attention decay)를 완전히 명시하지 않음
- 후속 연구 방향: (1) 동적 커뮤니티 구조 변화 모델링, (2) 커뮤니티 간 인용 흐름 명시적 포함, (3) 신경망과의 하이브리드 접근

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 인용 네트워크의 커뮤니티 구조와 성장 역학을 동시에 포착하는 첫 분석적 모델을 제시하며, 폐쇄형 수학적 결과와 실용적 적합 능력을 모두 제공한다. 과학계량학과 네트워크 과학 분야에 중요한 기여로 평가된다.

## Related Papers

- 🏛 기반 연구: [[papers/960_Evolution_of_the_social_network_of_scientific_collaborations/review]] — 과학자 협력 네트워크의 우선적 부착 관찰이 Price-Pareto 모델의 커뮤니티별 이질적 인용 역학 설계에 실증적 근거를 제공한다.
- 🏛 기반 연구: [[papers/957_Emergence_of_Scaling_in_Random_Networks/review]] — 무작위 네트워크에서 스케일링 출현 현상이 Price-Pareto 모델의 수학적 토대를 제공한다.
- 🧪 응용 사례: [[papers/990_Networks_of_Scientific_Papers/review]] — 과학 논문의 서지학적 네트워크 패턴이 Price-Pareto 모델의 실제 적용 사례를 보여준다.
- 🏛 기반 연구: [[papers/1049_Universality_of_citation_distributions_Toward_an_objective_m/review]] — 인용 분포의 보편성 연구가 커뮤니티별 이질적 인용 역학을 모델링하는 Price-Pareto 모델의 이론적 근거를 제공한다.
- 🔗 후속 연구: [[papers/948_Community_Detection_in_Graphs/review]] — 커뮤니티 탐지 방법론을 기반으로 하여, 발견된 커뮤니티 구조에서 인용 네트워크의 성장 과정을 수학적으로 모델링한다.
- 🔄 다른 접근: [[papers/1046_The_structure_of_scientific_collaboration_networks/review]] — 과학 협력 네트워크의 구조적 특성을 분석하되, 정적 구조보다는 동적 성장 과정에서의 커뮤니티별 차별화된 메커니즘에 초점을 맞춘다.
- 🧪 응용 사례: [[papers/1049_Universality_of_citation_distributions_Toward_an_objective_m/review]] — 인용 분포의 보편성이 커뮤니티별로 다른 인용 역학을 모델링하는 Price-Pareto 모델에 적용된다.
- 🔗 후속 연구: [[papers/947_Collective_dynamics_of_small-world_networks/review]] — Price-Pareto 성장 모델은 small-world 네트워크 이론을 기반으로 커뮤니티 구조를 가진 네트워크의 진화를 설명합니다.
- 🔄 다른 접근: [[papers/948_Community_Detection_in_Graphs/review]] — 커뮤니티 구조를 가진 네트워크의 성장 모델을 통해 커뮤니티 검출과 다른 관점에서 네트워크 구조를 분석한다.
- 🔗 후속 연구: [[papers/957_Emergence_of_Scaling_in_Random_Networks/review]] — 스케일-프리 네트워크 모델을 커뮤니티 구조를 포함한 더 복잡한 네트워크로 발전시킨다
- 🔗 후속 연구: [[papers/960_Evolution_of_the_social_network_of_scientific_collaborations/review]] — Price-Pareto 모델이 커뮤니티 구조를 가진 네트워크에서 preferential attachment의 이질적 역학을 더 정교하게 모델링한다.
