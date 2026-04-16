---
title: "1309_An_Real-Sim-Real_RSR_Loop_Framework_for_Generalizable_Roboti"
authors:
  - "Lu Shi"
  - "Yuxuan Xu"
  - "Shiyu Wang"
  - "Jinhao Huang"
  - "Wenhao Zhao"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 Real-Sim-Real (RSR) 루프 프레임워크를 제안하여 differentiable simulation을 활용해 시뮬레이션 파라미터를 반복적으로 개선하고 실제 세계 조건과 정렬시킴으로써 sim-to-real 갭을 해소한다. 정보 이론 기반의 비용 함수를 통해 다양하고 대표적인 실세계 데이터 수집을 유도하여 시뮬레이션 정제의 효율성을 극대화한다."
tags:
  - "cat/Robot_Policy_Learning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_AI_Architectures"
  - "sub/Robotic_Policy_Scaling"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shi et al._2025_An Real-Sim-Real (RSR) Loop Framework for Generalizable Robotic Policy Transfer with Differentiable.pdf"
---

# An Real-Sim-Real (RSR) Loop Framework for Generalizable Robotic Policy Transfer with Differentiable Simulation

> **저자**: Lu Shi, Yuxuan Xu, Shiyu Wang, Jinhao Huang, Wenhao Zhao, Yufei Jia, Zike Yan, Weibin Gu, Guyue Zhou | **날짜**: 2025-03-13 | **URL**: [https://arxiv.org/abs/2503.10118](https://arxiv.org/abs/2503.10118)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

본 논문은 Real-Sim-Real (RSR) 루프 프레임워크를 제안하여 differentiable simulation을 활용해 시뮬레이션 파라미터를 반복적으로 개선하고 실제 세계 조건과 정렬시킴으로써 sim-to-real 갭을 해소한다. 정보 이론 기반의 비용 함수를 통해 다양하고 대표적인 실세계 데이터 수집을 유도하여 시뮬레이션 정제의 효율성을 극대화한다.

## Motivation

- **Known**: Domain Randomization (DR)과 domain adaptation은 sim-to-real 갭 해소의 주요 기법이나, DR은 수동 선택이 필요하고 폐쇄형 루프 접근으로 실세계 데이터 피드백을 활용하지 못한다. Differentiable simulator를 이용한 파라미터 튜닝도 제안되었으나 실세계 데이터 편향과 일반화 문제가 남아있다.
- **Gap**: 기존 방법들은 실세계 데이터 수집 과정의 편향을 간과하며, 시각 정보만에 의존하거나 특정 로봇 유형에 제한된다. 정책이 중요한 영역을 균형있게 탐색하도록 유도하면서 시뮬레이션 튜닝을 위한 정보성 높은 데이터를 체계적으로 수집하는 방법이 부족하다.
- **Why**: 로봇 정책의 실제 배포에 있어 sim-to-real 갭 감소는 안전성과 효율성을 크게 향상시킨다. 정보 이론 기반 비용 함수로 데이터 수집 과정을 최적화하면 제한된 실세계 상호작용으로도 높은 성능을 달성할 수 있다.
- **Approach**: RSR 루프는 실세계에서 수집한 데이터로 시뮬레이션을 튜닝하고, 개선된 시뮬레이션에서 정책을 학습하며, 이를 다시 실세계에 배포하는 반복 과정을 수행한다. Information theory 기반의 informative cost function을 설계하여 PPO, SAC 등 기존 RL 알고리즘과 통합 가능하게 하고, MuJoCo MJX 플랫폼 위에 구현하여 다양한 로봇 시스템과의 호환성을 보장한다.

## Achievement


- **Informative Cost Function**: 정보 이론에 기반한 비용 함수가 실세계 데이터 수집의 편향을 최소화하고 각 데이터 포인트의 시뮬레이션 정제에 대한 기여도를 최대화함
- **알고리즘 통합성**: 제안된 비용 함수가 PPO, SAC 등 기존 RL 알고리즘과 seamlessly 통합되어 추가적인 구현 수정이 최소화됨
- **일반화 성능**: 로봇 조작 태스크에서 명시적·암시적 환경 불확실성 모두에 대해 높은 작업 성능과 일반화 가능성 달성
- **플랫폼 호환성**: MuJoCo MJX 플랫폼 기반 구현으로 다양한 로봇 시스템에 적용 가능한 확장성 확보

## How

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- Kernel Density Estimation (KDE)을 통해 실세계 데이터 분포를 추정하고 미탐색 영역 식별
- 정보 이론 메트릭(예: entropy reduction, mutual information)을 기반으로 시뮬레이션 튜닝에 최적화된 데이터 포인트의 정보성 정량화
- 비용 함수에 물리적 상태와 시각적 정보를 모두 포함하여 dynamic variables(속도, 가속도, 스러스트 등) 포착
- Differentiable simulator의 gradient 계산으로 실세계 데이터와 시뮬레이션 간 손실 함수 최소화
- 개선된 시뮬레이션 환경에서 RL 정책 학습 후 실세계 배포, 그리고 다시 실세계 데이터 수집으로 RSR 루프 반복

## Originality

- Information theory 기반의 informative cost function을 RL 알고리즘과 결합하여 능동적 데이터 수집 전략을 제시한 점이 기존 수동 parameter randomization과 차별화됨
- 물리적 상태와 시각적 정보를 동시에 고려하는 다중 모드 비용 함수 설계로 robust한 시뮬레이션 튜닝 가능
- RSR 루프를 통한 폐쇄형 피드백 구조로 실세계 데이터를 체계적으로 활용하는 반복 개선 프레임워크

## Limitation & Further Study

- 시각적 손실 함수 추가에 따른 계산 비용 증가와 성능 향상 간의 트레이드오프에 대한 분석이 충분하지 않음
- 다양한 로봇 플랫폼(팔, 이족보행로봇, 드론 등)에서의 일반화 가능성 검증이 제한적으로 제시됨
- 실세계 실험 규모가 제한적이어서 대규모 산업 응용의 현실성 평가 필요
- 후속 연구: 더 복잡한 동역학 및 다중 에이전트 시나리오로의 확장, 계산 효율성 최적화, 다양한 센서 모달리티 통합

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 information theory 기반의 informative cost function을 통해 sim-to-real 전이 문제를 체계적으로 해결하는 새로운 RSR 루프 프레임워크를 제시하며, differentiable simulation과 기존 RL 알고리즘의 통합으로 실무 적용 가능성이 높다. 다만 실세계 실험의 범위 확대와 계산 비용 분석이 추후 과제이다.

## Related Papers

- 🔄 다른 접근: [[papers/1297_A_Real-to-Sim-to-Real_Approach_to_Robotic_Manipulation_with/review]] — Real-to-Sim-to-Real 접근법의 다른 구현 방식을 제시한다.
- 🔗 후속 연구: [[papers/1527_Real2Render2Real_Scaling_Robot_Data_Without_Dynamics_Simulat/review]] — 동역학 시뮬레이션 없이 로봇 데이터를 스케일링하는 방법으로 RSR 루프를 확장한다.
- 🏛 기반 연구: [[papers/1572_Sim-to-Real_Reinforcement_Learning_for_Vision-Based_Dexterou/review]] — 시각 기반 정교한 조작을 위한 Sim-to-Real 강화학습의 기초 이론을 제공한다.
- 🏛 기반 연구: [[papers/1386_Evaluating_Real-World_Robot_Manipulation_Policies_in_Simulat/review]] — 시뮬레이션에서 실제 로봇 정책 평가에 대한 기초적인 방법론을 제공합니다.
- 🔄 다른 접근: [[papers/1293_A_Distributional_Treatment_of_Real2Sim2Real_for_Object-Centr/review]] — 둘 다 Real2Sim2Real 프레임워크를 제안하지만 RSR Loop은 differentiable simulation에, Distributional Treatment는 물리 파라미터 분포 추정에 중점을 둡니다.
- 🔗 후속 연구: [[papers/1368_DiWA_Diffusion_Policy_Adaptation_with_World_Models/review]] — DiWA의 world model을 활용한 diffusion policy adaptation 개념을 Real-Sim-Real loop에서 반복적인 시뮬레이션 개선으로 확장한 방법론입니다.
- 🏛 기반 연구: [[papers/1472_Mastering_Diverse_Domains_through_World_Models/review]] — Mastering Diverse Domains through World Models의 world model 활용 개념을 differentiable simulation 기반의 sim-to-real 갭 해소로 구체화한 연구입니다.
- 🏛 기반 연구: [[papers/1293_A_Distributional_Treatment_of_Real2Sim2Real_for_Object-Centr/review]] — 일반화 가능한 로봇 제어를 위한 RSR 루프 프레임워크가 Real2Sim2Real의 이론적 기반을 제공합니다.
