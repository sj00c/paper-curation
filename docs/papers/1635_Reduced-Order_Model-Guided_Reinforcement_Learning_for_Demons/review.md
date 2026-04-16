---
title: "1635_Reduced-Order_Model-Guided_Reinforcement_Learning_for_Demons"
authors:
  - "Shuai Liu"
  - "Meng Cheng Lau"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "ROM-GRL은 모션캡처 데이터 없이 4-DOF reduced-order model로 생성한 gait template을 이용해 full-body humanoid 정책을 학습하는 2단계 강화학습 프레임워크이다. Adversarial discriminator를 통해 ROM의 5-dimensional gait feature 분포를 따르도록 유도하여 자연스러운 보행을 실현한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liu and Lau_2025_Reduced-Order Model-Guided Reinforcement Learning for Demonstration-Free Humanoid Locomotion.pdf"
---

# Reduced-Order Model-Guided Reinforcement Learning for Demonstration-Free Humanoid Locomotion

> **저자**: Shuai Liu, Meng Cheng Lau | **날짜**: 2025-09-23 | **URL**: [https://arxiv.org/abs/2509.19023](https://arxiv.org/abs/2509.19023)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of the ROM-GRL framework. In Stage 1, a 4-DOF ROM policy is trained in Box2D: the policy*

ROM-GRL은 모션캡처 데이터 없이 4-DOF reduced-order model로 생성한 gait template을 이용해 full-body humanoid 정책을 학습하는 2단계 강화학습 프레임워크이다. Adversarial discriminator를 통해 ROM의 5-dimensional gait feature 분포를 따르도록 유도하여 자연스러운 보행을 실현한다.

## Motivation

- **Known**: 순수 보상 기반 RL은 자세한 보상 설계가 필요하고 부자연스러운 움직임이 발생할 수 있으며, motion capture 기반 모방학습은 mocap 데이터 의존성이 높지만 높은 사실성을 달성한다.
- **Gap**: 모션캡처 데이터 없이도 자연스럽고 안정적인 humanoid 보행을 생성하는 방법이 부족하며, 복잡한 보상 설계 없이 demonstration-free 학습을 달성하기 어렵다.
- **Why**: Humanoid 로봇의 실제 배포에서 mocap 데이터 수집이 어렵고 비용이 높으며, 보상 설계의 불확실성을 줄이면서도 자연스러운 보행 동작을 얻는 것이 중요하다.
- **Approach**: 2단계 프레임워크로 먼저 경량 ROM을 PPO로 학습하여 에너지 효율적인 gait template을 생성하고, 이를 Soft Actor-Critic과 adversarial discriminator를 통해 full-body 정책으로 증류한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3 visualizes pelvis and foot trajectories for the ROM-GRL policy (blue) and the pure-reward baseline (orange),*

- **Demonstration-free learning**: 모션캡처 데이터나 elaborate reward shaping 없이 자연스러운 보행 학습
- **다중 속도 검증**: 1 m/s와 4 m/s에서 안정적이고 대칭적인 gait 생성
- **낮은 추적 오류**: 순수 보상 기반 baseline보다 상당히 낮은 tracking error 달성
- **패러다임 통합**: 보상 중심 및 모방 기반 방법 간의 간격을 좁혀 versatile humanoid 행동 실현

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Schematic of the planar ROM used to generate reference walking trajectories. The ROM consists of a central*

- Stage 1: 4-DOF planar ROM에 PPO 적용하여 compact gait template 생성
- Stage 2: ROM의 궤적으로부터 5-dimensional gait feature (pelvis/foot 궤적 등) 추출
- Soft Actor-Critic에 adversarial discriminator 통합하여 학생 정책의 feature 분포를 teacher의 분포에 맞춤
- Hierarchical decomposition으로 high-level gait planning과 low-level control 분리
- Physics simulation 기반 fully differentiable training pipeline 활용

## Originality

- ROM을 motion capture의 대체재로 활용하는 창의적 접근으로 demonstration-free 학습과 자연스러운 동작을 동시에 달성
- Adversarial discriminator를 통한 gait feature 분포 매칭으로 imitation learning 원칙을 mocap 없이 구현
- 경량 teacher 모델의 guidance를 고차원 정책으로 증류하는 novel distillation 스킴
- 보상 설계와 모방 학습의 장점을 결합한 하이브리드 패러다임 제시

## Limitation & Further Study

- 4-DOF ROM의 단순화로 인해 복잡한 동적 움직임(예: 점프, 회전)의 적용 가능성 미평가
- 1 m/s와 4 m/s의 제한된 속도 범위에서만 검증되어 광범위한 속도 적응성 불명확
- 5-dimensional gait feature로 제한된 제약이 모든 보행 특성을 충분히 포착하는지 미검증
- 실제 로봇에 대한 sim-to-real transfer 성능 미평가
- ROM의 동역학 모델이 실제 humanoid와 완벽히 일치하지 않을 경우의 영향 분석 부재
- 후속연구: 더 높은 DOF의 ROM, 다양한 보행 스타일 또는 동작으로 확장, 실물 로봇 실험, domain randomization을 통한 robustness 증대

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ROM-GRL은 reduced-order model을 creative하게 활용해 motion capture 의존성을 제거하면서 자연스럽고 안정적인 humanoid 보행을 달성하는 novel 프레임워크이다. 보상 설계와 모방 학습 간 간격을 효과적으로 줄였으나, 제한된 속도 범위와 실제 로봇 검증 부재가 일반화 가능성의 의문을 남긴다.

## Related Papers

- 🔄 다른 접근: [[papers/1940_Gait-Conditioned_Reinforcement_Learning_with_Multi-Phase_Cur/review]] — ROM-GRL은 reduced-order model 기반 2단계 학습을, Gait-Conditioned RL은 다중 위상 커리큘럼을 통해 보행 학습을 다르게 접근함
- 🏛 기반 연구: [[papers/1777_A_Gait_Driven_Reinforcement_Learning_Framework_for_Humanoid/review]] — A Gait Driven Reinforcement Learning Framework의 보행 주도 강화학습이 ROM-GRL의 gait template 기반 학습의 이론적 기초를 제공함
- 🔄 다른 접근: [[papers/1660_RuN_Residual_Policy_for_Natural_Humanoid_Locomotion/review]] — ROM-GRL과 RuN 모두 자연스러운 휴머노이드 보행을 위한 decoupled learning을 사용하지만 전자는 ROM 기반, 후자는 motion generator 기반이다
- 🏛 기반 연구: [[papers/1801_AMP_Adversarial_Motion_Priors_for_Stylized_Physics-Based_Cha/review]] — ROM-GRL의 adversarial discriminator가 AMP의 adversarial motion prior 방법론을 reduced-order model에 적용한 것이다
- 🔗 후속 연구: [[papers/2109_Natural_Humanoid_Robot_Locomotion_with_Generative_Motion_Pri/review]] — ROM-GRL의 4-DOF reduced model이 Natural Humanoid Locomotion의 generative motion prior와 결합되어 더 효율적인 gait 학습을 실현할 수 있다
- 🔄 다른 접근: [[papers/1944_General_Humanoid_Whole-Body_Control_via_Pretraining_and_Fast/review]] — Demonstration-free learning을 pretraining 기반 접근법으로 해결한 대조적 연구
- 🔄 다른 접근: [[papers/1660_RuN_Residual_Policy_for_Natural_Humanoid_Locomotion/review]] — RuN과 ROM-GRL 모두 자연스러운 휴머노이드 보행을 위한 decoupled learning을 사용하지만 전자는 motion generator 기반, 후자는 ROM 기반이다
- 🧪 응용 사례: [[papers/1816_Benchmarking_Humanoid_Imitation_Learning_with_Motion_Difficu/review]] — motion difficulty 평가 방법론이 reduced-order model 기반 demonstration learning에 실제 적용되어 학습 효율성을 향상시킨다.
