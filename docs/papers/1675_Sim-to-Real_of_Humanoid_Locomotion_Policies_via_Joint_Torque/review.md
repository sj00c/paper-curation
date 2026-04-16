---
title: "1675_Sim-to-Real_of_Humanoid_Locomotion_Policies_via_Joint_Torque"
authors:
  - "Junhyeok Rui Cha"
  - "Woohyun Cha"
  - "Jaeyong Shin"
  - "Donghyeon Kim"
  - "Jaeheung Park"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 기존 domain randomization의 한계를 극복하기 위해 상태 의존적인 joint torque space perturbation을 주입하여 humanoid 로봇의 sim-to-real 전이를 개선하는 방법을 제안한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Cha et al._2025_Sim-to-Real of Humanoid Locomotion Policies via Joint Torque Space Perturbation Injection.pdf"
---

# Sim-to-Real of Humanoid Locomotion Policies via Joint Torque Space Perturbation Injection

> **저자**: Junhyeok Rui Cha, Woohyun Cha, Jaeyong Shin, Donghyeon Kim, Jaeheung Park | **날짜**: 2025-04-09 | **URL**: [https://arxiv.org/abs/2504.06585](https://arxiv.org/abs/2504.06585)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the training framework: The dynamics*

본 논문은 기존 domain randomization의 한계를 극복하기 위해 상태 의존적인 joint torque space perturbation을 주입하여 humanoid 로봇의 sim-to-real 전이를 개선하는 방법을 제안한다.

## Motivation

- **Known**: Domain randomization(DR)은 시뮬레이션과 현실 사이의 reality gap을 줄이기 위해 널리 사용되고 있으나, 시뮬레이터가 노출하는 유한한 매개변수 집합과 그 영향의 수식화 방식에 의해 근본적으로 제약된다.
- **Gap**: 기존 DR 방식은 고정된 매개변수 세트만 무작위화할 수 있어 비선형 actuator 동역학이나 contact compliance 같은 복잡한 현실 갭을 포착하지 못한다. RFI는 존재하지만 상태 의존성이 없어 표현력이 제한적이다.
- **Why**: Humanoid 로봇 제어는 고차원 시스템이면서 bipedal 불안정성으로 인해 까다로우며, 충분한 현실성을 갖춘 제어 정책 개발이 산업 및 연구에 중요하다.
- **Approach**: Neural network을 이용한 상태 의존적 perturbation generator를 제안하여 joint torque 입력 단계에서 동적 불확실성을 시뮬레이션하고, Denoising World Model Learning(DWL)과 Raibert 기반 궤적 생성을 결합한 훈련 프레임워크를 구축한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Snapshots of training, sim-to-sim transfer, and sim-to-real transfer. This work proposes a novel sim-to-real met*

- **상태 의존적 joint torque perturbation 방법**: 기존 parametric randomization보다 표현력이 높은 neural network 기반 perturbation으로 비선형 actuator 거동과 contact compliance 같은 복잡한 동역학 불일치를 시뮬레이션
- **Full-sized humanoid TOCABI에서 검증**: 확장된 무작위화 범위, 미학습 지면 마찰, 거친 지형, 수정된 동역학에 대해 우수한 강건성을 보이며 zero-shot sim-to-real 전이 달성
- **Motion capture 없는 훈련 프레임워크**: GRU 기반 encoder가 privileged observation 재구성을 통해 robust latent representation을 학습하고, online Raibert 기반 궤적 생성이 velocity-adaptive reference를 제공하여 adversarial training 없이 자연스러운 humanoid gait 생성

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the training framework: The dynamics*

- Joint torque 입력 단계에 상태 의존적 perturbation을 추가: δ_τ(s) = f_θ(s)로 표현되는 neural network 기반 perturbation function 도입
- Perturbation function의 가중치를 각 에피소드 시작 시 무작위로 샘플링하여 다양한 동역학 환경 생성
- DWL을 통한 latent representation 학습: privileged information(예: 실제 지표면 특성)을 reconstruction 과제로 활용하여 policy가 robust한 representation 획득
- Raibert 휴리스틱을 이용한 velocity-adaptive reference trajectory 생성으로 reward shaping 간소화
- Training 중 확장된 domain randomization 범위와 perturbation 주입으로 policy의 일반화 능력 강화

## Originality

- Domain randomization의 효과를 joint torque space perturbation으로 재해석하고, 이를 neural network으로 확장하여 기존 parametric randomization의 표현력 한계를 극복
- 상태 의존적 perturbation을 통해 복잡한 비선형 동역학을 직접 시뮬레이션하는 새로운 sim-to-real 패러다임 제시
- DWL과 Raibert 기반 휴리스틱의 조합으로 motion capture 데이터 없이도 자연스러운 humanoid locomotion 학습

## Limitation & Further Study

- Perturbation function의 neural network 아키텍처 선택(크기, 깊이 등)이 성능에 미치는 영향에 대한 상세한 분석 부족
- 제시된 방법이 TOCABI 하나의 humanoid 로봇에서만 검증되어 다른 로봇 플랫폼(quadruped 등)으로의 일반화 가능성 불명확
- Real-world 배포 시 추가 fine-tuning의 필요성 여부와 required data quantity에 대한 논의 부재
- Perturbation의 통계적 특성(예: 분포, 크기)이 policy 성능에 미치는 영향에 대한 ablation study 제한적
- 후속 연구로는 다양한 로봇 형태에 대한 확장, 적응형 perturbation intensity 조정 메커니즘, 그리고 실시간 online adaptation 기법 개발이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 domain randomization의 근본적 한계를 creative하게 해결하고 full-sized humanoid 로봇에서 실증적 검증을 통해 sim-to-real 전이 분야에 유의미한 기여를 한다. 다만 방법의 일반화 가능성과 실제 배포 시나리오에서의 추가 고려사항에 대한 더 깊은 분석이 있으면 완성도가 높아질 수 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1664_Sampling-Based_System_Identification_with_Active_Exploration/review]] — sim-to-real을 joint torque perturbation vs sampling-based parameter identification으로 다르게 접근합니다.
- 🔗 후속 연구: [[papers/1657_Robust_Humanoid_Walking_on_Compliant_and_Uneven_Terrain_with/review]] — 개선된 sim-to-real 전이가 복잡한 지형에서의 robust walking으로 적용됩니다.
- 🔄 다른 접근: [[papers/1664_Sampling-Based_System_Identification_with_Active_Exploration/review]] — sim-to-real gap을 physics parameter identification vs joint torque perturbation으로 다르게 해결합니다.
- 🏛 기반 연구: [[papers/1657_Robust_Humanoid_Walking_on_Compliant_and_Uneven_Terrain_with/review]] — domain randomization의 한계를 극복한 sim-to-real 방법이 복잡 지형 보행에 필수적입니다.
- 🔄 다른 접근: [[papers/1877_DiffCoTune_Differentiable_Co-Tuning_for_Cross-domain_Robot_C/review]] — 조인트 토크 매칭을 통한 다른 시뮬레이션-현실 학습 방식을 제시합니다.
- 🧪 응용 사례: [[papers/2048_Learning_Bipedal_Locomotion_on_Gear-Driven_Humanoid_Robot_Us/review]] — 발목 IMU 기반 프레임워크가 관절 토크를 통한 sim-to-real 학습에 실제 적용될 수 있다.
- 🔄 다른 접근: [[papers/2107_MOSAIC_Bridging_the_Sim-to-Real_Gap_in_Generalist_Humanoid_M/review]] — Sim-to-real 전이에서 범용 동작 추적과 관절 토크 기반의 다른 접근법을 비교하여 각각의 장단점을 분석할 수 있다.
- 🏛 기반 연구: [[papers/2155_Towards_bridging_the_gap_Systematic_sim-to-real_transfer_for/review]] — Sim-to-Real of Humanoid Locomotion의 관절 토크 기반 전이 기법이 PMSM 에너지 모델을 통한 체계적 전이의 기반 방법론을 제공합니다.
- 🔗 후속 연구: [[papers/2151_Toward_Reliable_Sim-to-Real_Predictability_for_MoE-based_Rob/review]] — joint torque 기반 sim-to-real 접근법에 MoE와 RoboGauge 평가를 통합하면 더 신뢰할 수 있는 전이 성능 예측 가능
