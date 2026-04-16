---
title: "1678_SkillBlender_Towards_Versatile_Humanoid_Whole-Body_Loco-Mani"
authors:
  - "Yuxuan Kuang"
  - "Haoran Geng"
  - "Amine Elhafsi"
  - "Tan-Dzung Do"
  - "Pieter Abbeel"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "SkillBlender는 사전학습된 목표조건부 원시 기술들을 동적으로 혼합하여 휴머노이드 로봇이 복잡한 전신 조작-이동 작업을 최소한의 보상 엔지니어링으로 수행할 수 있게 하는 계층적 강화학습 프레임워크이다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Adaptive_Locomotion_Recovery"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kuang et al._2025_SkillBlender Towards Versatile Humanoid Whole-Body Loco-Manipulation via Skill Blending.pdf"
---

# SkillBlender: Towards Versatile Humanoid Whole-Body Loco-Manipulation via Skill Blending

> **저자**: Yuxuan Kuang, Haoran Geng, Amine Elhafsi, Tan-Dzung Do, Pieter Abbeel, Jitendra Malik, Marco Pavone, Yue Wang | **날짜**: 2025-06-11 | **URL**: [https://arxiv.org/abs/2506.09366](https://arxiv.org/abs/2506.09366)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of SkillBlender. We first pretrain goal-conditioned primitive expert skills that are*

SkillBlender는 사전학습된 목표조건부 원시 기술들을 동적으로 혼합하여 휴머노이드 로봇이 복잡한 전신 조작-이동 작업을 최소한의 보상 엔지니어링으로 수행할 수 있게 하는 계층적 강화학습 프레임워크이다.

## Motivation

- **Known**: 휴머노이드 로봇은 최적제어와 강화학습을 통해 전신 제어와 조작-이동에서 상당한 진전을 이루었으나, 각 작업마다 광범위한 작업별 보상 튜닝이 필요하여 확장성이 제한된다.
- **Gap**: 기존 강화학습 방법들은 방향, 보행, 접촉, 호기심 등 다양한 보상항을 균형있게 조정해야 하므로 일상적 시나리오의 다양한 작업에 확장하기 어렵다는 한계가 있다.
- **Why**: 휴머노이드 로봇의 일상적 배포를 위해서는 학습된 기본 능력들을 효율적으로 조합하여 다양한 작업을 자동으로 수행할 수 있는 확장 가능하고 다용도적인 시스템이 필수적이다.
- **Approach**: 인간의 운동 기술 발달에서 영감을 받아, 작업비특이적 원시 기술들을 먼저 사전학습한 후 고수준 제어기가 부분목표와 per-joint 가중치 벡터를 학습하여 이들 기술을 혼합하는 방식을 제안한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Qualitative comparison between different methods. Our SkillBlender not only achieves*

- **SkillBlender 프레임워크**: 목표조건부 원시 기술들을 동적으로 혼합하는 독특한 벡터화 가중치 메커니즘으로 더 유연하고 정확한 휴머노이드 행동을 생성
- **SkillBench 벤치마크**: 병렬화 가능하고 3개의 신체형태, 4개의 원시 기술, 8개의 도전적 과제를 포함하며 정확도와 실현가능성을 모두 측정하는 평가 메트릭 제공
- **최소한의 보상 엔지니어링**: 기존 방법의 다중 보상항 대신 작업당 1-2개의 보상항으로 강건하고 자연스러운 정책 학습 가능
- **광범위한 성능 향상**: 모든 기준선을 능가하며 보상 해킹을 자연스럽게 방지하여 다양한 일상적 조작-이동 작업에서 더 정확하고 실현가능한 움직임 실현

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of SkillBlender. We first pretrain goal-conditioned primitive expert skills that are*

- 사전학습 단계: 워킹, 리칭, 조작, 푸싱 등 4개의 목표조건부 원시 기술을 task-agnostic하게 학습
- 고수준 제어기: 부분목표 생성과 per-joint 가중치 벡터를 학습하여 원시 기술들을 동적으로 혼합
- 정확도 메트릭: 작업 완료 성공을 측정
- 실현가능성 메트릭: 인간다움과 자연스러움을 평가하여 보상 해킹 방지
- 평행 시뮬레이션: RL 학습 효율성 향상

## Originality

- 기존 HRL 방법과 달리 multiple reusable skills을 명시적으로 다루고, 특히 per-joint 벡터화 가중치를 통한 고유한 기술 혼합 전략 제시
- 인간의 운동 기술 발달 과정(기초 능력 먼저 습득 → 복합 작업 수행)에서 직접 영감을 받은 계층적 구조
- 정확도와 실현가능성을 동시에 평가하는 이중 차원의 평가 메트릭 도입으로 보상 해킹 문제 체계적 해결
- 3개 신체형태와 8개 다양한 과제를 지원하는 포괄적이고 병렬화된 벤치마크 제공

## Limitation & Further Study

- 시뮬레이션 기반 실험만 제시되어 실제 하드웨어 로봇에서의 검증이 필요
- 사전학습된 4개의 원시 기술으로 제한되어 있으며, 새로운 기술 추가 시 재학습 필요성 존재
- 평가 메트릭의 '실현가능성' 정의가 휴머노이드 특성에 얼마나 일반화되는지 검토 필요", '대규모 일상적 작업 다양성(수백 개 이상)에 대한 확장성 검증 부족
- 후속연구로 실제 로봇 배포, 다양한 신체형태 간 기술 전이 학습, 적응형 기술 추가 학습 메커니즘 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SkillBlender는 휴머노이드 로봇의 다용도적 조작-이동 능력 개발에 대한 우아하고 실용적인 해결책을 제시하며, 포괄적인 벤치마크와 함께 향후 휴머노이드 연구의 중요한 기초가 될 가능성이 높다.

## Related Papers

- 🔄 다른 접근: [[papers/2089_ManiSkill-HAB_A_Benchmark_for_Low-Level_Manipulation_in_Home/review]] — 두 논문 모두 계층적 학습을 통한 조작-이동 작업을 다루지만, 일반적인 스킬 혼합과 홈 환경 특화라는 다른 접근을 사용한다.
- 🏛 기반 연구: [[papers/1943_GBC_Generalized_Behavior-Cloning_Framework_for_Whole-Body_Hu/review]] — 일반적인 행동 클로닝 프레임워크를 통한 전신 휴머노이드 제어의 기초를 제공한다.
- 🔗 후속 연구: [[papers/2090_MASH_Cooperative-Heterogeneous_Multi-Agent_Reinforcement_Lea/review]] — 협력적 이종 다중 에이전트 학습을 원시 기술 혼합으로 확장하여 더 복잡한 조작-이동 작업을 수행한다.
- 🏛 기반 연구: [[papers/1674_Sim-to-Real_Learning_for_Humanoid_Box_Loco-Manipulation/review]] — 기본적인 loco-manipulation 기술들이 복잡한 전신 조작-이동 작업의 primitive skill 기반이 됩니다.
- 🔗 후속 연구: [[papers/2115_OKAMI_Teaching_Humanoid_Robots_Manipulation_Skills_through_S/review]] — primitive skill blending이 human demonstration을 통한 manipulation skill teaching으로 확장됩니다.
- 🔗 후속 연구: [[papers/1674_Sim-to-Real_Learning_for_Humanoid_Box_Loco-Manipulation/review]] — 박스 조작의 기본 loco-manipulation이 더 복잡한 전신 조작-이동 작업으로 발전됩니다.
- 🔗 후속 연구: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — ResMimic의 전신 loco-manipulation이 SkillBlender의 다양한 스킬 결합과 통합되어 더 versatile한 휴머노이드 제어를 실현할 수 있다
- 🔗 후속 연구: [[papers/1642_RGMP_Recurrent_Geometric-prior_Multimodal_Policy_for_General/review]] — RGMP의 87% 성공률 달성 경험이 SkillBlender의 다양한 whole-body skill 결합에서 성능 최적화 가이드라인을 제공할 수 있다
- 🔗 후속 연구: [[papers/1760_X-Loco_Towards_Generalist_Humanoid_Locomotion_Control_via_Sy/review]] — SkillBlender의 다재다능한 whole-body 제어가 X-Loco의 전문가 정책 통합 방식을 보완합니다.
- 🏛 기반 연구: [[papers/1896_EGM_Efficiently_Learning_General_Motion_Tracking_Policy_for/review]] — SkillBlender의 다양한 loco-manipulation 기술 블렌딩 방법론이 EGM의 일반화된 모션 추적 정책 학습을 위한 기반을 제공한다.
- 🏛 기반 연구: [[papers/1995_Humanoid_Hanoi_Investigating_Shared_Whole-Body_Control_for_S/review]] — SkillBlender의 versatile whole-body loco-manipulation 기법이 Humanoid Hanoi의 reusable skill 조합 방법론의 기초를 제공한다.
- 🏛 기반 연구: [[papers/2018_HYPERmotion_Learning_Hybrid_Behavior_Planning_for_Autonomous/review]] — 다재다능한 전신 로코-조작이 하이브리드 행동 계획의 기반 기술이다.
- 🔗 후속 연구: [[papers/2038_KungfuBot2_Learning_Versatile_Motion_Skills_for_Humanoid_Who/review]] — OMoE를 기반으로 한 다중 기술 학습을 loco-manipulation 통합 시스템으로 확장하여 더 포괄적인 휴머노이드 능력을 구현할 수 있다.
- 🔄 다른 접근: [[papers/2091_MaskedManipulator_Versatile_Whole-Body_Manipulation/review]] — 둘 다 versatile whole-body manipulation이지만 MaskedManipulator는 masked approach를, SkillBlender는 skill composition 방식을 사용한다
- 🔗 후속 연구: [[papers/2159_TrajBooster_Boosting_Humanoid_Whole-Body_Manipulation_via_Tr/review]] — SkillBlender의 versatile whole-body control에 TrajBooster의 궤적 전이 방법을 적용하면 더 다양한 manipulation skill 학습 가능
- 🔗 후속 연구: [[papers/2165_ULC_A_Unified_and_Fine-Grained_Controller_for_Humanoid_Loco-/review]] — SkillBlender의 versatile whole-body skills에 ULC의 residual action modeling을 적용하면 더 정밀한 loco-manipulation 제어 가능
- 🔄 다른 접근: [[papers/2153_Towards_Adaptive_Humanoid_Control_via_Multi-Behavior_Distill/review]] — 다중행동 증류는 여러 행동을 하나의 정책으로 통합하고 SkillBlender는 다양한 스킬을 조합하는 서로 다른 휴머노이드 제어 접근법입니다.
