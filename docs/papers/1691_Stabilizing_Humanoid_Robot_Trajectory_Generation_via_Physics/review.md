---
title: "1691_Stabilizing_Humanoid_Robot_Trajectory_Generation_via_Physics"
authors:
  - "Evelyn D'Elia"
  - "Paolo Maria Viceconte"
  - "Lorenzo Rapetti"
  - "Diego Ferigo"
  - "Giulio Romualdi"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "인간형 로봇의 궤적 생성에 물리 기반 학습과 제어 기반 보정을 결합하여 모방학습의 안정성을 향상시키는 방법을 제안한다. Physics-informed loss와 PI 제어기를 통해 물리 법칙 위반을 줄이고 실제 로봇에서의 안정성을 개선한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/D'Elia et al._2025_Stabilizing Humanoid Robot Trajectory Generation via Physics-Informed Learning and Control-Informed.pdf"
---

# Stabilizing Humanoid Robot Trajectory Generation via Physics-Informed Learning and Control-Informed Steering

> **저자**: Evelyn D'Elia, Paolo Maria Viceconte, Lorenzo Rapetti, Diego Ferigo, Giulio Romualdi, Giuseppe L'Erario, Raffaello Camoriano, Daniele Pucci | **날짜**: 2025-09-29 | **URL**: [https://arxiv.org/abs/2509.24697](https://arxiv.org/abs/2509.24697)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Our method used to execute various walking direc-*

인간형 로봇의 궤적 생성에 물리 기반 학습과 제어 기반 보정을 결합하여 모방학습의 안정성을 향상시키는 방법을 제안한다. Physics-informed loss와 PI 제어기를 통해 물리 법칙 위반을 줄이고 실제 로봇에서의 안정성을 개선한다.

## Motivation

- **Known**: 행동 복제(behavior cloning)를 이용한 인간형 로봇 궤적 생성은 인간다운 부드러운 움직임을 가능하게 하였으나, 제한된 데이터량으로 인해 물리 법칙을 위반하고 불안정한 궤적을 생성할 수 있다. Physics-informed machine learning(PIML)은 물리 제약을 학습에 인코딩하여 데이터 효율성을 개선하는 것으로 알려져 있다.
- **Gap**: 기존 PIML 기반 인간형 로봇 제어는 미분불가능한 리워드 함수를 사용하거나 인간다움이 부족하며, 학습 단계에서의 물리 제약 인코딩과 추론 단계에서의 드리프트 보정을 통합적으로 다루는 연구가 부족하다.
- **Why**: 인간형 로봇이 협력적 환경에서 안전하고 신뢰할 수 있게 작동하려면 물리적으로 타당한 궤적을 생성해야 하며, 동시에 인간다운 움직임을 유지해야 한다. 이는 실제 배포 환경에서의 안정성과 사용자 신뢰도를 결정한다.
- **Approach**: 두 가지 전략으로 구성된다: (1) 학습 단계에서 접촉 발의 속도를 0으로 유지하도록 하는 미분가능한 물리 기반 손실함수를 추가하고, (2) 추론 단계에서 네트워크 출력에 비례-적분(PI) 제어기를 직접 적용하여 드리프트를 최소화한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Comparison of the drift in base position (top) and*

- **Floating-base 로봇의 전체 운동학적 상태 학습**: 표준 데이터 적합 손실과 함께 kinematically feasible 접촉을 고려한 physics-informed loss를 제시하여, 네트워크가 접촉 발은 고정하고 유각 발만 이동하도록 학습하게 함
- **제어 기반 드리프트 감소**: 기본 제어 이론을 활용하여 사용자 입력과 네트워크 예측을 결합한 보정항을 도입, 궤적의 드리프트를 효과적으로 감소
- **실제 로봇 검증**: ergoCub 인간형 로봇에서 두 가지 제어 아키텍처로 실험하여 방법의 다중성(modularity)과 효과성을 입증, 궤적의 정확도와 물리 제약 준수를 상당히 개선

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overall humanoid locomotion architecture integrating*

- Supervised learning을 통해 이전 상태와 사용자 지정 방향 입력이 주어졌을 때 다음 상태의 전체 운동학적 상태를 예측하는 신경망 학습
- Physics-informed loss 함수 L(z; θ) = wF·LF(z; θ) + wB·LB(z; θ) + wD·LD(z; θ) 형태로 정의하여 미분가능한 물리 제약을 backpropagation 중에 반영
- Jacobian 행렬을 자동 미분(automatic differentiation)으로 계산하여 접촉 발의 속도 제약을 손실함수에 인코딩
- 추론 단계에서 PI 제어기 u_corrected = u_network + kP·e + kI·∫e를 적용하여 네트워크 출력의 체계적 오류를 실시간으로 보정
- Ablation study를 통해 각 구성 요소(physics-informed loss, PI 제어기)의 기여도 정량화
- ergoCub 로봇에서 다양한 보행 방향 실험 및 두 가지 서로 다른 제어 아키텍처와의 호환성 검증

## Originality

- PIML과 제어 이론을 결합한 모듈식 프레임워크로, 학습 단계와 추론 단계를 명확히 분리하여 각각 다른 안정화 전략을 적용
- Automatic differentiation을 활용하여 Jacobian 기반 접촉 속도 제약을 미분가능한 손실함수로 구현, 기존 non-differentiable 리워드 방식과 차별화
- 사용자 입력과 네트워크 예측을 PI 제어기로 블렌딩하는 방식은 경량이면서도 효과적인 추론 단계 보정 방법으로 실제 배포에 용이
- 행동 복제의 인간다움을 유지하면서 물리 타당성을 개선하는 명확한 목표 설정과 체계적 접근

## Limitation & Further Study

- **데이터 의존성**: 여전히 초기 행동 복제 모델의 품질에 의존하므로, 훈련 데이터의 다양성과 품질이 충분하지 않으면 성능 제한
- **물리 제약의 선택성**: 현재 접촉 발의 속도만을 제약하고 있으며, 다른 중요한 물리 법칙(예: 모멘텀 보존, 지면 반력 제약)은 미포함
- **제어기 튜닝**: PI 제어기의 이득(kP, kI) 값이 수동으로 조정되어야 하며, 로봇이나 환경 변화에 따른 자동 조정 메커니즘 부재
- **일반화 성능**: ergoCub 로봇에서만 검증되었으므로 다른 인간형 로봇이나 사족 로봇으로의 일반화 정도 미지수
- **계산 비용**: 실시간 Jacobian 계산과 자동 미분으로 인한 계산 오버헤드의 상세 분석 부족
- **후속 연구**: (1) 더 포괄적인 물리 제약을 손실함수에 포함하는 방법, (2) 적응형 PI 제어 이득 조정 기법, (3) 다양한 인간형 로봇 플랫폼으로의 확장, (4) 동적 환경(예: 장애물, 계단)에서의 성능 평가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 물리 기반 학습과 제어 이론을 효과적으로 결합하여 인간형 로봇 궤적 생성의 실제 안정성을 향상시키는 실질적이고 모듈식의 접근법을 제시한다. 특히 미분가능한 물리 제약 인코딩과 추론 단계의 PI 제어 보정은 구현이 간단하면서도 실증적 효과가 크며, 실제 로봇 검증으로 산업 적용 가능성을 보여준다.

## Related Papers

- 🔄 다른 접근: [[papers/1615_Physics-Based_Motion_Imitation_with_Adversarial_Differential/review]] — 두 논문 모두 물리 기반 모방 학습을 다루지만, 물리 정보 기반 안정화와 adversarial differential privacy라는 다른 접근을 사용한다.
- 🏛 기반 연구: [[papers/1862_DeepMimic_Example-Guided_Deep_Reinforcement_Learning_of_Phys/review]] — 예시 기반 깊은 강화학습의 물리 기반 캐릭터 제어 기초를 제공한다.
- 🔗 후속 연구: [[papers/2137_PhysDiff_Physics-Guided_Human_Motion_Diffusion_Model/review]] — 물리 기반 인간 모션 diffusion을 physics-informed learning으로 안정화하는 방향으로 발전시킨다.
- 🔄 다른 접근: [[papers/1684_SoftMimic_Learning_Compliant_Whole-body_Control_from_Example/review]] — 휴머노이드의 안정적 제어를 위해 서로 다른 접근(물리 기반 궤적 보정 vs 순응적 동작 생성)을 통해 물리 법칙과 안정성을 보장한다.
- 🔗 후속 연구: [[papers/1955_GMT_General_Motion_Tracking_for_Humanoid_Whole-Body_Control/review]] — 모션 트래킹의 기본 개념을 물리 기반 학습과 제어 기반 보정으로 확장하여 모방학습의 안정성을 크게 향상시켰다.
- 🔄 다른 접근: [[papers/1684_SoftMimic_Learning_Compliant_Whole-body_Control_from_Example/review]] — 휴머노이드의 안정적 제어를 위해 서로 다른 접근(순응적 동작 생성 vs 물리 기반 궤적 보정)을 통해 물리 법칙과 안정성을 보장한다.
- 🔗 후속 연구: [[papers/1858_cuRoboV2_Dynamics-Aware_Motion_Generation_with_Depth-Fused_D/review]] — physics-based trajectory stabilization과 dynamics-aware motion generation이 함께 안전하고 안정적인 로봇 운동 생성의 완전한 솔루션을 구성한다.
- 🏛 기반 연구: [[papers/2001_Humanoid_Robot_Acrobatics_Utilizing_Complete_Articulated_Rig/review]] — 물리학 기반 궤적 안정화 기술이 완전한 강체 역학 기반 아크로바틱 동작 제어의 핵심 토대가 된다.
- 🏛 기반 연구: [[papers/2049_Learning_Differentiable_Reachability_Maps_for_Optimization-b/review]] — 물리 유도 궤적 안정화가 최적화 기반 인간형 모션 생성의 기반이다.
- 🏛 기반 연구: [[papers/2133_PDF-HR_Pose_Distance_Fields_for_Humanoid_Robots/review]] — Physics-constrained trajectory generation이 PDF-HR의 pose distance field에서 로봇 포즈의 물리적 plausibility 평가의 기술적 기반을 제공합니다.
