---
title: "1688_Spectral_Normalization_for_Lipschitz-Constrained_Policies_on"
authors:
  - "Jaeyong Shin"
  - "Woohyun Cha"
  - "Donghyeon Kim"
  - "Junhyeok Cha"
  - "Jaeheung Park"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 인간형 로봇의 보행 학습에서 Spectral Normalization (SN)을 사용하여 Lipschitz 연속성을 효율적으로 강제하고, 기존의 gradient penalty 기반 방법보다 GPU 메모리 오버헤드를 줄이면서도 유사한 성능을 달성한다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Parallel_Robot_Training"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shin et al._2025_Spectral Normalization for Lipschitz-Constrained Policies on Learning Humanoid Locomotion.pdf"
---

# Spectral Normalization for Lipschitz-Constrained Policies on Learning Humanoid Locomotion

> **저자**: Jaeyong Shin, Woohyun Cha, Donghyeon Kim, Junhyeok Cha, Jaeheung Park | **날짜**: 2025-04-11 | **URL**: [https://arxiv.org/abs/2504.08246](https://arxiv.org/abs/2504.08246)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

본 논문은 인간형 로봇의 보행 학습에서 Spectral Normalization (SN)을 사용하여 Lipschitz 연속성을 효율적으로 강제하고, 기존의 gradient penalty 기반 방법보다 GPU 메모리 오버헤드를 줄이면서도 유사한 성능을 달성한다.

## Motivation

- **Known**: 강화학습으로 학습된 로봇 제어 정책은 시뮬레이션에서 뛰어난 성능을 보이지만, 실제 로봇의 유한한 actuator 대역폭 등 현실적 제약을 반영하지 않아 sim-to-real 전이에 실패한다. 기존에는 regularization reward나 gradient penalty 기반 Lipschitz-Constrained Policy (LCP)로 이를 완화했다.
- **Gap**: Gradient penalty 기반 LCP는 효과적이지만 정책 gradient 계산으로 인한 GPU 메모리 오버헤드가 크며, 대규모 병렬 시뮬레이션 환경에서 훈련 속도를 제한한다.
- **Why**: 로봇의 실제 배포 시 고주파 토크 변화는 진동과 불안정성을 야기하므로, 효율적인 대역폭 제한 방법은 실제 로봇 제어의 실용성을 크게 향상시킨다.
- **Approach**: Spectral Normalization을 정책 네트워크의 가중치 행렬에 적용하여 가중치의 최대 singular value로 정규화함으로써, 명시적인 gradient 계산 없이 Lipschitz 상수를 제약한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **메모리 효율성**: SN은 gradient penalty 기반 방법 대비 GPU 메모리 사용량을 크게 감소시켜 더 효율적인 병렬 훈련을 가능하게 함
- **성능 동등성**: 시뮬레이션과 실제 인간형 로봇 플랫폼 모두에서 SN은 GP-LCP와 유사한 제어 안정성을 달성
- **Sim-to-real 전이 개선**: 실제 actuator 대역폭 및 제어 제약을 고려하여 현실적인 정책 학습을 도모

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. Comparison between a standard actor network and an actor network*

- Lipschitz 연속성: 함수 f에 대해 ‖f(x) − f(y)‖ ≤ L‖x − y‖를 만족하는 Lipschitz 상수 L이 존재하도록 제약
- Spectral Normalization 적용: 각 가중치 행렬 W_l을 최대 singular value σ(W_l)로 정규화하여 W_l / σ(W_l) 형태로 변환
- 네트워크 아키텍처: 표준 actor 네트워크에 SN을 적용하여 고주파 동작 변화를 억제
- 훈련: Actor-Critic 기반 강화학습 프레임워크에서 SN 정규화된 정책으로 학습 진행

## Originality

- GAN의 discriminator 안정화를 위해 개발된 Spectral Normalization을 로봇 보행 정책의 Lipschitz 제약에 처음 적용
- Gradient penalty 기반 방법의 대체재로서 SN의 효율성을 체계적으로 실증하고, 메모리-성능 트레이드오프 분석 제공
- 시뮬레이션과 실제 로봇 모두에서 검증하여 실용적 가치 증명

## Limitation & Further Study

- Spectral Normalization의 singular value 계산 비용과 수렴 특성에 대한 이론적 분석 부족
- 다양한 로봇 형태(쌍족, 사족 등)와 복잡한 지형에서의 일반화 성능 검증 필요
- SN의 spectral norm 제약이 정책의 표현력을 제한할 가능성에 대한 상세 분석 필요
- 실제 로봇 실험이 하나의 인간형 플랫폼에만 제한되어 있어, 더 다양한 하드웨어에서의 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 Spectral Normalization이라는 기존 기법을 로봇 정책 학습의 대역폭 제약 문제에 창의적으로 적용하여, 계산 효율성과 성능을 모두 달성한 실용적인 솔루션을 제시한다. 시뮬레이션과 실제 로봇 양쪽에서의 검증으로 신뢰성을 높였으며, sim-to-real 전이 문제 해결에 중요한 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1710_The_invariant_extended_Kalman_filter_as_a_stable_observer/review]] — Spectral Normalization의 Lipschitz 연속성 보장이 IEKF의 안정성 분석에서 요구되는 수학적 조건과 이론적으로 연관된다.
- 🔄 다른 접근: [[papers/1759_Whole-Body_Model-Predictive_Control_of_Legged_Robots_with_Mu/review]] — SN 기반 메모리 효율적 학습과 MuJoCo 기반 실시간 MPC는 모두 계산 효율성을 추구하는 상호 보완적 제어 접근법이다.
- 🔄 다른 접근: [[papers/2062_Learning_Smooth_Humanoid_Locomotion_through_Lipschitz-Constr/review]] — 두 논문 모두 Lipschitz 제약을 통한 부드러운 휴머노이드 보행을 다루지만, spectral normalization과 일반적인 제약이라는 다른 구현 방법을 사용한다.
- 🏛 기반 연구: [[papers/1926_FastTD3_Simple_Fast_and_Capable_Reinforcement_Learning_for_H/review]] — 빠르고 효율적인 강화학습 방법의 기초를 제공한다.
- 🔗 후속 연구: [[papers/2108_Multi-task_Deep_Reinforcement_Learning_with_PopArt/review]] — 다중 작업 deep RL을 Lipschitz 제약으로 확장하여 더 안정적인 학습을 달성한다.
- 🏛 기반 연구: [[papers/1696_Success_in_Humanoid_Reinforcement_Learning_under_Partial_Obs/review]] — 부분 관찰 환경에서의 안정적 학습 기법을 Lipschitz 연속성 관점에서 보완하여 메모리 효율성과 성능을 동시에 개선했다.
- 🔄 다른 접근: [[papers/1881_Distillation-PPO_A_Novel_Two-Stage_Reinforcement_Learning_Fr/review]] — 휴머노이드 학습의 안정성을 위해 서로 다른 아키텍처(Spectral Normalization vs 2단계 강화학습)를 통해 효율적인 정책 학습을 추구한다.
- 🏛 기반 연구: [[papers/1696_Success_in_Humanoid_Reinforcement_Learning_under_Partial_Obs/review]] — Lipschitz 연속성을 통한 안정적 학습 기법을 부분 관찰 환경으로 확장하여 고정 길이 과거 관찰 시퀀스를 활용한 안정적 정책 학습을 구현했다.
- 🧪 응용 사례: [[papers/1710_The_invariant_extended_Kalman_filter_as_a_stable_observer/review]] — IEKF의 안정성 분석에 필요한 Lie group 상의 조건들이 Spectral Normalization의 Lipschitz 제약과 수학적으로 연관되어 상호 보완한다.
- 🏛 기반 연구: [[papers/1629_Quantum_deep_reinforcement_learning_for_humanoid_robot_navig/review]] — Spectral Normalization의 Lipschitz 제약 정책이 quantum deep RL에서 안정적인 학습과 수렴성 보장의 이론적 기초를 제공함
- 🏛 기반 연구: [[papers/1843_CMR_Contractive_Mapping_Embeddings_for_Robust_Humanoid_Locom/review]] — Lipschitz 제약 정책을 위한 spectral normalization이 CMR에서 disturbance attenuation을 위한 Lipschitz regularization의 구현 기반을 제공한다
- 🔗 후속 연구: [[papers/1854_Coordinated_Humanoid_Robot_Locomotion_with_Symmetry_Equivari/review]] — 립시츠 제약 정책이 대칭 등변 제어의 안정성을 보장합니다.
- 🔗 후속 연구: [[papers/2033_Keep_on_Going_Learning_Robust_Humanoid_Motion_Skills_via_Sel/review]] — Keep on Going의 선택적 적대적 강화가 Spectral Normalization의 Lipschitz 제약 정책과 결합되어 더 안정적인 견고성 달성
- 🏛 기반 연구: [[papers/2062_Learning_Smooth_Humanoid_Locomotion_through_Lipschitz-Constr/review]] — Lipschitz 제약을 통한 정책 안정화의 이론적 기반과 구현 방법을 제공한다.
- 🔄 다른 접근: [[papers/2133_PDF-HR_Pose_Distance_Fields_for_Humanoid_Robots/review]] — 포즈 거리 필드 대신 Lipschitz 제약을 통해 정책의 안정성과 타당성을 보장하는 다른 수학적 접근법이다.
