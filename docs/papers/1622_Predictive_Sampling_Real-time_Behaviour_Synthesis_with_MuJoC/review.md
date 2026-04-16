---
title: "1622_Predictive_Sampling_Real-time_Behaviour_Synthesis_with_MuJoC"
authors:
  - "Taylor Howell"
  - "Nimrod Gileadi"
  - "Saran Tunyasuvunakool"
  - "Kevin Zakka"
  - "Tom Erez"
date: "2022.12"
doi: ""
arxiv: ""
score: 4.0
essence: "MuJoCo 물리 엔진 기반의 실시간 예측 제어 프레임워크 MJPC를 소개하고, 간단한 샘플링 기반 알고리즘인 Predictive Sampling이 기존의 더 복잡한 알고리즘들과 경쟁력 있음을 보여준다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Terrain_Foothold_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Howell et al._2022_Predictive Sampling Real-time Behaviour Synthesis with MuJoCo.pdf"
---

# Predictive Sampling: Real-time Behaviour Synthesis with MuJoCo

> **저자**: Taylor Howell, Nimrod Gileadi, Saran Tunyasuvunakool, Kevin Zakka, Tom Erez, Yuval Tassa | **날짜**: 2022-12-01 | **URL**: [https://arxiv.org/abs/2212.00541](https://arxiv.org/abs/2212.00541)

---

## Essence

![Figure 3](figures/fig3.webp)

*Figure 3 | Graphical User Interface. The left tab includes modules for Tasks and the Agent. In the*

MuJoCo 물리 엔진 기반의 실시간 예측 제어 프레임워크 MJPC를 소개하고, 간단한 샘플링 기반 알고리즘인 Predictive Sampling이 기존의 더 복잡한 알고리즘들과 경쟁력 있음을 보여준다.

## Motivation

- **Known**: 고전적 모델 기반 제어와 최근의 학습 기반 강화학습 방법들이 로봇 제어에서 각각의 장단점을 가지고 있으며, shooting methods를 통한 trajectory optimization이 실시간 동작 생성에 효과적이다.
- **Gap**: 모델 기반 최적화는 구현이 어렵고 접근성이 낮으며, 로봇 연구자들이 예측 제어를 쉽게 활용할 수 있는 실용적인 도구와 인터페이스가 부족하다.
- **Why**: 실시간 피드백을 통한 대화형 시뮬레이션은 로봇 연구 속도를 가속화하고, 모델 기반 방법의 접근성을 높여 학습 기반 방법과의 결합 가능성을 열 수 있다.
- **Approach**: MuJoCo 기반의 오픈소스 대화형 프레임워크를 개발하여 iLQG, Gradient Descent, Predictive Sampling 세 가지 shooting-based planner를 구현하고, 비동기 시뮬레이션과 GUI를 통해 접근성을 높인다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4 | Behaviours generated with MuJoCo MPC. Time progresses left to right.*

- **MJPC 프레임워크 공개**: 모델 기반 예측 제어를 위한 완전한 오픈소스 소프트웨어 프레임워크로 github.com/deepmind/mujoco_mpc에서 이용 가능
- **Predictive Sampling 알고리즘**: 단순하고 이해하기 쉬운 zero-order 샘플링 기반 알고리즘이 iLQG와 같은 고차 알고리즘과 경쟁력 있는 성능을 보임
- **실시간 대화형 제어**: 비동기 시뮬레이션 슬로우다운을 통해 저사양 기계에서도 실시간 동작 생성 가능
- **접근성 향상**: 직관적인 GUI와 간단한 코드로 복잡한 로봇 작업 설계 및 최적화 가능
- **연구 생산성 증대**: 즉각적인 피드백을 통해 매개변수 조정 시 연구자의 인지 성능 향상

## How

![Figure 2](figures/fig2.webp)

*Figure 2 | Time-indexed spline representation of*

- shooting methods 기반의 trajectory optimization으로 제어 신호만을 결정 변수로 사용하여 물리적으로 가능한 궤적만 고려
- 세 가지 planner 구현: derivative-based iLQG (2차), Gradient Descent (1차), derivative-free Predictive Sampling (0차)
- warmstarting을 활용하여 이전 계획 단계의 결과를 새로운 상태 기반 최적화의 초기값으로 사용
- composable하고 risk-aware한 목적 함수를 통해 다양한 로봇 작업 지정
- C++ 구현과 멀티스레딩을 통해 parallel rollouts 처리
- 비동기 agent-planner 구조로 시뮬레이션 속도와 계획 최적화를 독립적으로 조절
- time-indexed spline representation으로 제어 신호 재매개변수화

## Originality

- Predictive Sampling: 의도적으로 기초적인 baseline으로 설계했음에도 불구하고 기존 알고리즘과 경쟁력 있는 성능을 보이는 흥미로운 발견
- 예측 제어 문맥에서 샘플링 기반 최적화가 경쟁력 있는 이유에 대한 분석 제시
- 대화형 시뮬레이션의 중요성 강조: 단순한 '부가 기능'이 아닌 고급 로봇 연구의 필수요소로 재정의", '모델 기반 최적화의 민주화라는 새로운 관점 도입

## Limitation & Further Study

- 알고리즘적 혁신 부재: 논문에서 명시적으로 새로운 알고리즘 발전을 제시하지 않으며, 주로 기존 방법들의 구현과 통합에 중점
- Predictive Sampling의 이론적 분석 부족: 왜 단순한 샘플링이 잘 작동하는지에 대한 엄밀한 이론적 근거 제시 부족
- 제한된 실험 평가: 발췌된 본문에서 정량적 벤치마크 결과나 광범위한 실험 비교 보이지 않음
- 확장성 논의 부재: 더 복잡한 고차원 문제나 장시간 horizon에서의 성능 특성에 대한 논의 부족
- 후속 연구 방향: 학습 기반 방법과의 결합 방안, value function approximation과의 통합, 비선형 제약 조건 처리 등에 대한 심화 연구 필요

## Evaluation

- Novelty: 3/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 새로운 알고리즘적 기여보다는 실용적이고 접근 가능한 도구의 개발과 제공에 중점을 두며, 예측 제어의 대중화와 연구 생산성 향상이라는 중요한 목표를 달성한다. Predictive Sampling의 실험적 경쟁력은 흥미로우나 이론적 분석이 보완되면 더욱 강력한 기여가 될 것이다.

## Related Papers

- 🔄 다른 접근: [[papers/1636_Reference-Free_Sampling-Based_Model_Predictive_Control/review]] — 두 논문 모두 sampling-based MPC를 사용하지만, Predictive Sampling은 간단한 샘플링을, Reference-Free는 spline 파라미터화를 통한 최적화를 제안함
- 🔗 후속 연구: [[papers/1938_Full-Order_Sampling-Based_MPC_for_Torque-Level_Locomotion_Co/review]] — Full-Order Sampling-Based MPC의 토크 수준 제어가 MJPC의 실시간 예측 제어 프레임워크를 더욱 정밀하게 확장함
- 🏛 기반 연구: [[papers/1855_Cost-Matching_Model_Predictive_Control_for_Efficient_Reinfor/review]] — Cost-Matching Model Predictive Control의 효율적 강화학습 방법론이 MJPC의 실시간 행동 합성의 기초가 됨
- 🔄 다른 접근: [[papers/1636_Reference-Free_Sampling-Based_Model_Predictive_Control/review]] — Reference-Free MPC는 spline 파라미터화 기반을, Predictive Sampling은 간단한 샘플링 기반 MPC를 통해 실시간 제어를 다르게 구현함
- 🔄 다른 접근: [[papers/1846_ComFree-Sim_A_GPU-Parallelized_Analytical_Contact_Physics_En/review]] — 실시간 행동 합성을 위한 다른 접근법으로 물리 엔진 최적화를 제시합니다.
- 🔄 다른 접근: [[papers/1883_DoublyAware_Dual_Planning_and_Policy_Awareness_for_Temporal/review]] — predictive sampling 기반 실시간 행동 합성이 TD-MPC 프레임워크와 다른 접근으로 humanoid control의 샘플 효율성을 개선한다.
- 🔄 다른 접근: [[papers/1938_Full-Order_Sampling-Based_MPC_for_Torque-Level_Locomotion_Co/review]] — 둘 다 sampling-based 실시간 제어를 다루지만 DIAL-MPC는 diffusion 기반이고 Predictive Sampling은 MuJoCo 기반이다.
- 🏛 기반 연구: [[papers/2145_TD-GRPC_Temporal_Difference_Learning_with_Group_Relative_Pol/review]] — Predictive Sampling의 실시간 행동 합성 기법이 TD-GRPC의 TD-MPC 프레임워크에서 off-policy 학습의 불안정성 해결에 방법론적 기반을 제공한다.
