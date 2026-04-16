---
title: "2105_MoRE_Mixture_of_Residual_Experts_for_Humanoid_Lifelike_Gaits"
authors:
  - "Dewei Wang"
  - "Xinmiao Wang"
  - "Xinzhe Liu"
  - "Jiyuan Shi"
  - "Yingnan Zhao"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "휴머노이드 로봇이 복잡한 지형을 인간다운 보행으로 횡단하기 위해 Mixture of Residual Experts (MoRE)와 다중 판별자를 활용한 2단계 RL 학습 프레임워크를 제안한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Terrain_Foothold_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2025_MoRE Mixture of Residual Experts for Humanoid Lifelike Gaits Learning on Complex Terrains.pdf"
---

# MoRE: Mixture of Residual Experts for Humanoid Lifelike Gaits Learning on Complex Terrains

> **저자**: Dewei Wang, Xinmiao Wang, Xinzhe Liu, Jiyuan Shi, Yingnan Zhao, Chenjia Bai, Xuelong Li | **날짜**: 2025-06-10 | **URL**: [https://arxiv.org/abs/2506.08840](https://arxiv.org/abs/2506.08840)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2.*

휴머노이드 로봇이 복잡한 지형을 인간다운 보행으로 횡단하기 위해 Mixture of Residual Experts (MoRE)와 다중 판별자를 활용한 2단계 RL 학습 프레임워크를 제안한다.

## Motivation

- **Known**: 휴머노이드 로봇은 RL 기반 접근법으로 강건한 보행 능력을 보이며, motion-tracking이나 AMP를 통해 인간다운 행동을 학습할 수 있다.
- **Gap**: 기존 motion-tracking 및 AMP 기반 방법들은 주로 평탄 지형에만 적합하고 proprioception만 사용하여 exteroception을 활용한 복잡 지형 횡단과 다중 보행 패턴의 원활한 전환을 동시에 달성하기 어렵다.
- **Why**: 휴머노이드 로봇이 실제 환경의 다양한 지형을 인간다운 자연스러운 보행으로 안정적으로 이동할 수 있다면 인간과 유사한 작업 수행 능력을 크게 향상시킬 수 있다.
- **Approach**: 2단계 훈련 파이프라인으로 첫 단계에서 깊이 카메라를 이용해 복잡 지형 횡단 정책을 학습하고, 두 번째 단계에서 MoE 기반 residual 모듈과 다중 판별자를 통해 인간 동작 prior를 활용하여 다중 보행 패턴을 학습한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Our framework leverages a two-stage training pipeline and the mixture*

- **2단계 패러다임**: 단일 정책으로 여러 보행을 습득하면서 복잡 지형에서 강건한 보행을 동시에 달성
- **Residual Experts 아키텍처**: MoE 기반 latent residual 전문가들을 학습하여 다중 판별자로부터의 인간 동작 prior를 효과적으로 통합
- **맞춤형 보행 보상**: 기준 동작과 보조 행동 제약을 동시에 학습하는 gait-specific 보상 설계로 정밀한 보행 제어 달성
- **실제 배포 검증**: Unitree G1 휴머노이드 로봇에서 walk, run, crouch-walking, high-knees 등 다중 인간다운 보행 패턴 간 원활한 전환 실현

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- Stage 1: depth camera 입력을 활용하여 elevation map을 구성하고 proprioception과 함께 사용하여 기본 locomotion 정책을 PPO로 훈련
- Stage 2: 훈련된 기본 정책의 마지막 hidden layer에 latent residual을 추가하는 MoRE 모듈 부착
- MoRE 모듈은 gating network를 통해 다중 expert outputs의 가중 조합을 생성하여 gait command 기반 보행 선택 실현
- 다중 판별자는 각각 서로 다른 참고 동작에 대해 훈련되며 gait command에 따라 선택되어 보행 의존적 보상 제공
- gait-specific 보상 함수로 base height 조정 등 세밀한 행동 제어를 통해 보행 다양성 강화

## Originality

- 기존 AMP 방법들이 단일 참고 동작만 사용하는 반면, 다중 판별자를 통해 여러 보행 패턴을 동시에 학습하는 구조 제안
- proprioception과 exteroception을 통합하면서 동시에 인간다운 보행을 달성하는 최초의 방법
- MoE 기반 residual 모듈로 gradient conflict를 제거하고 학습 가속화
- 2단계 훈련 파이프라임을 통해 기존 강건한 locomotion 정책을 효과적으로 재사용하면서 새로운 보행 학습

## Limitation & Further Study

- 현재 방법은 시뮬레이션 기반 훈련에 크게 의존하고 있어 sim-to-real 갭에 대한 상세 분석 부족
- MoE 기반 아키텍처의 computational overhead와 inference latency에 대한 정량적 분석 미흡
- 후속 연구: 더 다양한 극단적 지형(돌, 물 등)에 대한 일반화 능력 검증 필요
- 후속 연구: real-time gait 전환 시 에너지 효율성 및 안정성 분석 필요
- 후속 연구: 다른 휴머노이드 로봇 플랫폼으로의 일반화 가능성 탐색

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 복잡 지형 횡단과 인간다운 다중 보행 학습을 동시에 달성하는 통합적 프레임워크를 제시하며, MoE 기반 residual 접근법과 다중 판별자 활용으로 방법론적 독창성을 보인다. 실제 로봇 배포 검증과 함께 기술적으로 견고하고 실무적 중요성이 높은 연구이다.

## Related Papers

- 🔄 다른 접근: [[papers/2110_No_More_Marching_Learning_Humanoid_Locomotion_for_Short-Rang/review]] — 둘 다 휴머노이드의 효율적인 이동을 다루지만, MoRE는 복잡한 지형에서의 인간다운 보행에, No More Marching은 단거리 목표 도달에 집중한다.
- 🏛 기반 연구: [[papers/1656_Robust_and_Versatile_Bipedal_Jumping_Control_through_Reinfor/review]] — Robust and Versatile Bipedal Jumping의 강화학습 기반 보행 제어 기법이 MoRE의 다중 전문가 시스템 설계에 이론적 기초를 제공한다.
- 🔗 후속 연구: [[papers/1978_Hiking_in_the_Wild_A_Scalable_Perceptive_Parkour_Framework_f/review]] — Hiking in the Wild의 지각 기반 파쿠르 프레임워크를 복잡한 지형에서 더욱 자연스러운 인간다운 보행으로 확장한 연구이다.
- 🔄 다른 접근: [[papers/1660_RuN_Residual_Policy_for_Natural_Humanoid_Locomotion/review]] — 둘 다 natural humanoid locomotion이지만 MoRE는 복잡한 지형 횡단에, RuN은 일반적인 자연스러운 보행에 중점을 둔다
- 🏛 기반 연구: [[papers/1695_StyleLoco_Generative_Adversarial_Distillation_for_Natural_Hu/review]] — StyleLoco의 GAD 기반 자연스러운 보행 생성이 MoRE의 다중 판별자 학습 프레임워크에 방법론적 기반을 제공했다
- 🏛 기반 연구: [[papers/1924_FARM_Frame-Accelerated_Augmentation_and_Residual_Mixture-of-/review]] — FARM의 residual mixture-of-experts 구조가 MoRE의 잔차 전문가 혼합을 통한 인간다운 보행 학습의 기술적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1792_Adversarial_Locomotion_and_Motion_Imitation_for_Humanoid_Pol/review]] — 복잡한 지형에서의 인간다운 보행을 위한 다른 접근법으로, adversarial learning과 mixture of experts의 차이를 비교할 수 있다.
- 🔄 다른 접근: [[papers/1924_FARM_Frame-Accelerated_Augmentation_and_Residual_Mixture-of-/review]] — 둘 다 다양한 동작 유형 처리를 위해 mixture-of-experts를 사용하지만 적용 영역이 다르다.
- 🔄 다른 접근: [[papers/2110_No_More_Marching_Learning_Humanoid_Locomotion_for_Short-Rang/review]] — 둘 다 휴머노이드의 효율적 이동을 다루지만, No More Marching은 단거리 목표 도달 최적화에, MoRE는 복잡 지형의 자연스러운 보행에 초점을 둔다.
