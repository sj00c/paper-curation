---
title: "1629_Whom_to_Trust_Elective_Learning_for_Distributed_Gaussian_Pro"
authors:
  - "Zewen Yang"
  - "Xiaobing Dai"
  - "Akshat Dubey"
  - "Sandra Hirche"
  - "Georges Hattab"
date: "2024.02"
doi: ""
arxiv: ""
score: 4.0
essence: "Multi-agent 시스템에서 신뢰도 기반의 선택적 학습을 통해 Gaussian process regression의 분산 협력 학습을 개선하는 Pri-GP 알고리즘을 제안한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Robot_Policy_Learning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yang et al._2024_Whom to Trust Elective Learning for Distributed Gaussian Process Regression.pdf"
---

# Whom to Trust? Elective Learning for Distributed Gaussian Process Regression

> **저자**: Zewen Yang, Xiaobing Dai, Akshat Dubey, Sandra Hirche, Georges Hattab | **날짜**: 2024-02-05 | **URL**: [https://arxiv.org/abs/2402.03014](https://arxiv.org/abs/2402.03014)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Violin plots of prediction errors for different meth-*

Multi-agent 시스템에서 신뢰도 기반의 선택적 학습을 통해 Gaussian process regression의 분산 협력 학습을 개선하는 Pri-GP 알고리즘을 제안한다.

## Motivation

- **Known**: 분산 GP 기반 협력 학습은 모든 이웃 에이전트의 예측을 집계하여 개별 예측 정확도를 향상시킨다. 그러나 기존 방법들은 모든 이웃과의 강제적 정보 교환과 O(N²) 복잡도의 분산 계산이 필요하다.
- **Gap**: 기존 분산 GP 접근법은 에이전트가 협력자를 선택할 유연성이 없으며, 사전 지식이 잘못된 경우 잠재적으로 오도될 수 있는 예측도 집계한다. 또한 계산 오버헤드가 크고 안전-중요 시스템에 적합한 오차 보증이 부족하다.
- **Why**: Multi-agent 시스템의 robotic swarm navigation, underwater exploration, drone search and rescue 등 실제 응용에서 제한된 계산 자원과 안전성 요구사항이 존재하기 때문에, 효율적이고 신뢰할 수 있는 분산 학습이 중요하다.
- **Approach**: Prior 오차를 기반으로 이웃 에이전트의 신뢰도를 평가하여 선택적으로 예측을 요청하는 prior-aware elective distributed GP (Pri-GP)를 제안한다. 이는 분산 계산 없이 에이전트가 협력자를 동적으로 선택할 수 있게 한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Violin plots of prediction errors for different meth-*

- **계산 복잡도 감소**: 분산 계산으로 인한 O(N²) 복잡도를 제거하여 계산 오버헤드를 크게 줄인다.
- **예측 정확도 개선**: 특히 사전 지식이 잘못된 경우 오도될 수 있는 이웃의 예측을 제외함으로써 개별 예측 정확도를 향상시킨다.
- **오차 보증**: Pri-GP 프레임워크 내에서 예측 오차 상한을 제시하여 안전-중요 MAS 응용의 신뢰성을 보장한다.
- **유연한 협력**: 에이전트가 신뢰도에 기반하여 협력 이웃을 선택하는 유연성을 제공한다.

## How


- Prior 오차 메트릭 정의: 각 에이전트의 사전 지식 오차를 계산하여 이웃의 신뢰도 평가 기준으로 사용
- 선택적 예측 요청: 임계값을 기반으로 신뢰도 높은 이웃으로부터만 예측을 선택적으로 요청
- 분산 기반 가중치 제거: 분산 계산 대신 prior 오차에 기반한 간단한 가중치 방식 사용
- Bayesian 프레임워크: Gaussian process regression의 확률적 예측과 업데이트 능력 활용
- 오차 상한 도출: Assumption 1의 Lipschitz 연속성을 이용하여 이론적 오차 보증 제공

## Originality

- **Prior 오차 기반 신뢰도 평가**: 기존 분산 GP의 uniform 가중치나 분산 기반 방식과 달리, prior 오차를 직접 활용하는 새로운 메트릭 제안
- **선택적 협력 메커니즘**: 분산 협력 학습에서 에이전트의 자율적 협력자 선택 능력을 처음으로 도입
- **계산 효율성 개선**: 분산 계산의 O(N²) 복잡도를 제거하면서도 이론적 오차 보증 제공
- **일반화 가능성**: Prior 오차 메트릭이 다양한 머신러닝 방법론에 적용 가능한 광범위한 적용성 제시

## Limitation & Further Study

- **1차원 함수 제한**: 논문에서 스칼라 함수(d=1)만 다루며, 고차원 함수 확장은 Kronecker product 등의 기법이 필요
- **Lipschitz 연속성 가정**: Assumption 1의 Lipschitz 상수 L_f 추정이 실제 시스템에서 어려울 수 있음
- **동적 네트워크 구조**: 정적 그래프 G 기반으로 설계되어 동적으로 변하는 communication network에 대한 분석 부재
- **이질적 에이전트 미지원**: 모든 에이전트가 동일한 함수 f(x)를 학습하는 동질적 설정만 고려
- **후속 연구**: 고차원 함수 확장, 동적 네트워크 환경 적용, 이질적 MAS 설정 확장, 실제 시스템 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 논문은 분산 GP 학습에서 신뢰도 기반 선택적 협력을 통해 계산 효율성과 예측 정확도를 동시에 개선하는 실질적이고 창의적인 해결책을 제시한다. 이론적 오차 보증과 함께 안전-중요 응용의 신뢰성 요구를 충족하는 점이 특히 강점이다.

## Related Papers

- 🔄 다른 접근: [[papers/1401_GauDP_Reinventing_Multi-Agent_Collaboration_through_Gaussian/review]] — 둘 다 multi-agent 시스템에서 협력 학습을 다루지만 Pri-GP는 신뢰도 기반을, GauDP는 Gaussian 분포 기반 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1539_RoboFactory_Exploring_Embodied_Agent_Collaboration_with_Comp/review]] — RoboFactory의 embodied agent 협력을 신뢰도 기반 선택적 학습으로 확장하여 분산 환경에서의 효율성을 개선한다.
- 🏛 기반 연구: [[papers/1471_Masked_Visual_Pre-training_for_Motor_Control/review]] — 모터 제어를 위한 masked visual pre-training이 분산 Gaussian process regression의 시각적 특징 학습 기반을 제공한다.
- 🏛 기반 연구: [[papers/1564_Scaling_Proprioceptive-Visual_Learning_with_Heterogeneous_Pr/review]] — 이질적인 사전 훈련 모델을 활용한 고유감각-시각 학습이 분산 GP 회귀의 multi-modal 학습 기반을 제공한다.
- 🏛 기반 연구: [[papers/1306_All_Robots_in_One_A_New_Standard_and_Unified_Dataset_for_Ver/review]] — All Robots in One의 통합 데이터셋이 Pri-GP의 분산 로봇 학습을 위한 표준화된 기반을 제공한다.
- 🔗 후속 연구: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — Multimodal Fusion 서베이가 Pri-GP의 분산 학습을 멀티모달 퓨전 관점에서 확장하여 로봇 응용에 적용한다.
- 🏛 기반 연구: [[papers/1501_On_the_Vulnerability_of_LLMVLM-Controlled_Robotics/review]] — Multi-agent 시스템에서의 신뢰성과 보안 문제에 대한 기본 개념을 제공하여 분산 학습에서의 신뢰도 평가 방법론을 뒷받침한다.
- 🔄 다른 접근: [[papers/1440_Jailbreaking_LLM-Controlled_Robots/review]] — 둘 다 AI 시스템의 신뢰성 문제를 다루지만, 하나는 분산 협력에서의 신뢰도를, 다른 하나는 보안 취약점에 집중한다.
- 🔗 후속 연구: [[papers/1535_RoboArena_Distributed_Real-World_Evaluation_of_Generalist_Ro/review]] — Pri-GP의 분산 신뢰 기반 학습을 로봇 평가 환경으로 확장하여 다중 에이전트 로봇 시스템의 신뢰성 있는 협력을 가능하게 한다.
- 🔗 후속 연구: [[papers/1539_RoboFactory_Exploring_Embodied_Agent_Collaboration_with_Comp/review]] — 분산 Gaussian Process 학습의 trust 메커니즘이 RoboFactory의 다중 에이전트 협력을 더 신뢰성 있는 시스템으로 발전시킨다.
