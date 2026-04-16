---
title: "1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body"
authors:
  - "Siheng Zhao"
  - "Yanjie Ze"
  - "Yue Wang"
  - "C. Karen Liu"
  - "Pieter Abbeel"
date: "2025.10"
doi: "10.48550/arXiv.2510.05070"
arxiv: ""
score: 4.0
essence: "ResMimic는 일반 모션 추적(GMT) 정책을 기반으로 효율적인 잔차 정책(residual policy)을 학습하여 인간형 로봇의 정밀한 전신 이동-조작 능력을 실현하는 이단계 잔차학습 프레임워크이다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhao et al._2025_ResMimic From General Motion Tracking to Humanoid Whole-body Loco-Manipulation via Residual Learnin.pdf"
---

# ResMimic: From General Motion Tracking to Humanoid Whole-body Loco-Manipulation via Residual Learning

> **저자**: Siheng Zhao, Yanjie Ze, Yue Wang, C. Karen Liu, Pieter Abbeel, Guanya Shi, Rocky Duan | **날짜**: 2025-10-08 | **DOI**: [10.48550/arXiv.2510.05070](https://doi.org/10.48550/arXiv.2510.05070)

---

## Essence

![Figure 3](figures/fig3.webp)

*Fig. 3: Overview of ResMimic : (1) A general motion tracking policy is trained on large-scale human motion data to serve*

ResMimic는 일반 모션 추적(GMT) 정책을 기반으로 효율적인 잔차 정책(residual policy)을 학습하여 인간형 로봇의 정밀한 전신 이동-조작 능력을 실현하는 이단계 잔차학습 프레임워크이다.

## Motivation

- **Known**: 일반 모션 추적(GMT) 정책들은 대규모 인간 모션 데이터로 훈련되어 다양한 인간 동작을 재현할 수 있으나, 대상 객체에 대한 인식이 부족하여 조작 정밀도가 낮다.
- **Gap**: 기존 인간형 이동-조작 연구들은 모두 작업별 보상 설계에 의존하거나 단계별 제어로 제한되어 통합된 효율적 프레임워크가 없다.
- **Why**: 인간형 로봇의 전신 이동-조작 능력은 일상 서비스 및 창고 자동화 등 실제 응용에서 핵심이 되며, 기존 로봇(사족 또는 바퀴 매니퓰레이터)로는 달성할 수 없는 표현력을 제공한다.
- **Approach**: 대규모 인간 모션 데이터로 훈련한 GMT 정책을 견고한 기초로 사용하고, 이 위에 작업별 잔차 정책을 학습하여 객체 추적 및 상호작용 정밀도를 개선한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: We deploy ResMimic on a Unitree G1 humanoid to demonstrate diverse whole-body loco-manipulation capabilities.*

- **이단계 잔차학습 프레임워크**: 사전훈련된 GMT 정책과 작업별 정밀 잔차 정책의 결합으로 효율적이고 정확한 이동-조작을 실현
- **맞춤형 보상 설계**: point-cloud 기반 객체 추적 보상, 신체-객체 접촉 보상, curriculum 기반 가상 객체 제어기로 훈련 효율성 및 sim-to-real 전이 향상
- **광범위한 평가**: 시뮬레이션과 실제 Unitree G1 인간형 로봇에서 모션 추적, 객체 추적, 작업 성공률, 훈련 효율성, 견고성 및 일반화 측면의 실질적 개선 입증
- **연구 가속 자산 공개**: GPU 가속 시뮬레이션 인프라, sim-to-sim 평가 프로토타입, 모션 데이터 공개 예정

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Overview of ResMimic : (1) A general motion tracking policy is trained on large-scale human motion data to serve*

- Stage I: 대규모 인간-전용 모션 캡처 데이터로 GMT 정책(πGMT)을 훈련하여 인간형 전신 행동의 견고한 기초 확보
- Stage II: 훈련된 GMT 정책의 출력을 개선하는 작업별 잔차 정책(πRes)을 학습하여 로봇 상태(sr_t), 객체 상태(so_t), 참조 모션(ŝr_t), 객체 목표 상태(ŝo_t)를 조건으로 미세 조정
- 최종 행동은 a_t = agmt_t + Δares_t로 계산되어 기본 모션에 보정 신호를 더함
- Point-cloud 기반 객체 추적 보상으로 부드러운 최적화 달성
- Contact reward로 인간형-객체 상호작용의 정확성 명시적 유도
- Curriculum 기반 가상 객체 제어기로 초기 훈련 안정화

## Originality

- 기존 잔차학습이 손으로 설계한 정책이나 MPC를 개선하던 반면, 대규모 사전훈련된 GMT 정책을 기초로 하는 새로운 잔차학습 패러다임 제시
- 인간형 로봇 제어에서 기초 모델 사전훈련-미세조정 패러다임을 처음 체계적으로 탐구
- 전신 이동-조작에 특화된 point-cloud 기반 보상, contact 기반 보상, curriculum 제어기의 혁신적 설계
- 단순 조작을 넘어 4.5kg 무거운 하중 운반, 비규칙 형상 객체 다루기 등 다양한 전신 접촉을 포함한 복합 이동-조작 시연

## Limitation & Further Study

- GMT 정책의 사전훈련 데이터 규모 및 다양성에 의존적이므로, 훈련 데이터의 품질이 최종 성능을 제약할 수 있음
- 객체 추적 보상이 point-cloud 기반이어서 센서 노이즈나 폐색(occlusion) 상황에서의 강건성이 검증되지 않음
- 현재 평가는 Unitree G1 단일 플랫폼에서만 수행되어 다른 인간형 로봇 구조로의 일반화 미검증
- 후속 연구: 센서 노이즈 및 폐색에 대한 강건성 개선, 다양한 인간형 로봇 플랫폼으로의 확장, 더욱 복잡한 다중-객체 조작 시나리오로의 확대

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ResMimic는 대규모 사전훈련 GMT 정책과 효율적 잔차 정책의 결합으로 인간형 로봇의 정밀한 전신 이동-조작을 실현한 혁신적 프레임워크이며, 맞춤형 보상 설계와 광범위한 실증으로 인간형 로봇 제어 분야에 중요한 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1955_GMT_General_Motion_Tracking_for_Humanoid_Whole-Body_Control/review]] — GMT의 범용 모션 추적 기법이 ResMimic의 일반 모션 추적 정책 기반 잔차 학습의 핵심 기초를 제공함
- 🔗 후속 연구: [[papers/1820_BeyondMimic_From_Motion_Tracking_to_Versatile_Humanoid_Contr/review]] — BeyondMimic의 motion tracking을 넘어선 versatile control이 ResMimic의 GMT 기반 loco-manipulation을 더욱 발전시킬 수 있음
- 🔄 다른 접근: [[papers/1639_Residual_Off-Policy_RL_for_Finetuning_Behavior_Cloning_Polic/review]] — 두 논문 모두 residual learning을 사용하지만 ResMimic은 motion tracking 기반 loco-manipulation에, Residual Off-Policy는 BC 정책 개선에 집중한다
- 🔗 후속 연구: [[papers/1678_SkillBlender_Towards_Versatile_Humanoid_Whole-Body_Loco-Mani/review]] — ResMimic의 전신 loco-manipulation이 SkillBlender의 다양한 스킬 결합과 통합되어 더 versatile한 휴머노이드 제어를 실현할 수 있다
- 🔄 다른 접근: [[papers/1617_PILOT_A_Perceptive_Integrated_Low-level_Controller_for_Loco-/review]] — 통합 loco-manipulation을 single policy 대신 residual learning으로 해결
- 🔄 다른 접근: [[papers/1681_SMAP_Self-supervised_Motion_Adaptation_for_Physically_Plausi/review]] — 두 논문 모두 인간 모션을 휴머노이드 로봇으로 적응시키는 문제를 다루지만, 자기지도 학습과 일반적인 추적이라는 다른 방법을 사용한다.
- 🔄 다른 접근: [[papers/1685_SONIC_Supersizing_Motion_Tracking_for_Natural_Humanoid_Whole/review]] — 두 논문 모두 모션 추적을 다루지만, 대규모 모델과 일반적인 추적이라는 다른 규모의 접근을 사용한다.
- 🔄 다른 접근: [[papers/1639_Residual_Off-Policy_RL_for_Finetuning_Behavior_Cloning_Polic/review]] — 두 논문 모두 residual policy를 사용하지만 전자는 off-policy RL로 BC 개선에, 후자는 GMT 정책 기반 loco-manipulation에 집중한다
- 🔄 다른 접근: [[papers/1655_Robust_and_Generalized_Humanoid_Motion_Tracking/review]] — 두 논문 모두 인간 모션을 휴머노이드 로봇이 추적하는 문제를 다루지만, 다른 네트워크 아키텍처를 사용한다.
- 🔄 다른 접근: [[papers/1660_RuN_Residual_Policy_for_Natural_Humanoid_Locomotion/review]] — 인간 모션을 휴머노이드가 따라하는 문제에서 residual learning과 일반적인 추적 방법이라는 다른 접근을 사용한다.
- 🏛 기반 연구: [[papers/1694_SteadyTray_Learning_Object_Balancing_Tasks_in_Humanoid_Tray/review]] — 일반적인 모션 트래킹 기술을 트레이 운반이라는 특정 작업으로 확장하여 ReST-RL 아키텍처를 통한 계층적 제어를 실현했다.
- 🔗 후속 연구: [[papers/1612_PhysHMR_Learning_Humanoid_Control_Policies_from_Vision_for_P/review]] — PhysHMR의 통합 프레임워크가 ResMimic의 잔차 학습과 결합되어 더 정밀한 전신 제어를 실현할 수 있다
- 🔄 다른 접근: [[papers/1617_PILOT_A_Perceptive_Integrated_Low-level_Controller_for_Loco-/review]] — Loco-manipulation 통합 제어를 단일 policy 대신 residual policy 접근법으로 해결
- 🔗 후속 연구: [[papers/1751_Visual_Imitation_Enables_Contextual_Humanoid_Control/review]] — ResMimic의 일반적인 모션 추적이 VIDEOMIMIC의 4D 기하학 재구성 접근법을 보완합니다.
- 🔗 후속 연구: [[papers/1753_VisualMimic_Visual_Humanoid_Loco-Manipulation_via_Motion_Tra/review]] — 일반적 모션 트래킹에서 전신 제어로의 확장에서 visual과 residual 접근법이라는 보완적 방법론을 다룬다.
- 🔄 다른 접근: [[papers/1785_A_Whole-Body_Motion_Imitation_Framework_from_Human_Data_for/review]] — 동일한 whole-body motion tracking 목표를 ResNet 기반 geometric prior와 contact-aware MPC라는 다른 방법으로 달성한다
- 🔄 다른 접근: [[papers/1862_DeepMimic_Example-Guided_Deep_Reinforcement_Learning_of_Phys/review]] — whole-body motion tracking을 residual learning으로 접근하여 DeepMimic과 다른 관점의 해결책을 제시한다.
- 🔄 다른 접근: [[papers/1955_GMT_General_Motion_Tracking_for_Humanoid_Whole-Body_Control/review]] — 둘 다 일반적인 모션 추적을 다루지만 GMT는 Mixture-of-Experts를, ResMimic은 residual 기법을 사용한다.
- 🏛 기반 연구: [[papers/2021_Implicit_Kinodynamic_Motion_Retargeting_for_Human-to-humanoi/review]] — 일반적인 모션 추적 기법을 제공하여 IKMR의 기본 추적 메커니즘에 대한 이론적 기반을 마련한다.
- 🏛 기반 연구: [[papers/2088_Make_Tracking_Easy_Neural_Motion_Retargeting_for_Humanoid_Wh/review]] — 일반 동작 추적에서 휴머노이드 전신 제어로의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/2107_MOSAIC_Bridging_the_Sim-to-Real_Gap_in_Generalist_Humanoid_M/review]] — ResMimic의 residual learning 기법이 MOSAIC의 빠른 residual 적응 메커니즘 설계에 핵심 아이디어를 제공했다
