---
title: "1974_Hierarchical_Vision-Language_Planning_for_Multi-Step_Humanoi"
authors:
  - "André Schakkal"
  - "Ben Zandonati"
  - "Zhutian Yang"
  - "Navid Azizan"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "인간형 로봇의 복잡한 다단계 조작 작업을 위해 저수준 RL 추적 제어기, 중수준 모방학습 기반 스킬 정책, 고수준 VLM 기반 계획 및 모니터링으로 구성된 3계층 계층적 프레임워크를 제시한다."
tags:
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Manipulation_Reasoning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Schakkal et al._2025_Hierarchical Vision-Language Planning for Multi-Step Humanoid Manipulation.pdf"
---

# Hierarchical Vision-Language Planning for Multi-Step Humanoid Manipulation

> **저자**: André Schakkal, Ben Zandonati, Zhutian Yang, Navid Azizan | **날짜**: 2025-06-28 | **URL**: [https://arxiv.org/abs/2506.22827](https://arxiv.org/abs/2506.22827)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the proposed hierarchical framework for autonomous multi-step humanoid manipulation. The system*

인간형 로봇의 복잡한 다단계 조작 작업을 위해 저수준 RL 추적 제어기, 중수준 모방학습 기반 스킬 정책, 고수준 VLM 기반 계획 및 모니터링으로 구성된 3계층 계층적 프레임워크를 제시한다.

## Motivation

- **Known**: 최근 RL과 IL 기술이 보행, 댄싱, 복싱 등 단일 스킬 실행을 가능하게 했으며, 저수준 RL 추적 제어와 중수준 모션 생성을 조합한 2계층 구조가 humanoid 제어에서 성공을 거두었다.
- **Gap**: 기존 humanoid 시스템은 자율적으로 다단계 작업에서 스킬을 선택하고 순서를 정하거나 실행을 검증할 수 있는 통합 고수준 모듈이 부족하여, 긴 시간 지평의 조작 작업에서 인간 개입이 필요하다.
- **Why**: 인간형 로봇의 실제 배포를 위해서는 산업 및 가정 환경에서 복잡한 다단계 조작 작업을 신뢰성 있게 수행할 수 있어야 하며, VLM을 활용한 자율적 스킬 순서화와 모니터링이 이를 가능하게 한다.
- **Approach**: VLM 기반 플래너가 텍스트 및 시각 입력으로부터 IL 스킬 시퀀스를 생성하고, VLM 기반 모니터가 실시간 시각 피드백으로 스킬 완료를 검증하는 고수준 계획 모듈을 2계층 humanoid 제어 스택 위에 추가한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Our hierarchical humanoid manipulation system autonomously executes a multi-step rearrangement task. The robot f*

- **3계층 계층적 제어 구조**: 저수준 RL 기반 tracking policy (PPO), 중수준 imitation learning 기반 skill policies, 고수준 VLM 기반 planning 및 monitoring을 통합
- **VLM 기반 자율 스킬 관리**: pretrained vision-language models를 활용하여 다단계 작업에서 실시간으로 스킬을 선택하고 완료 여부를 검증
- **실제 humanoid 로봇 검증**: Unitree G1 (29-DoF) 로봇으로 40번의 실제 시험에서 73% 성공률 달성
- **해석 가능한 계획**: VLM 기반 접근이 end-to-end 모델보다 높은 해석 가능성과 구조화된 스킬 분해를 제공

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the proposed hierarchical framework for autonomous multi-step humanoid manipulation. The system*

- **저수준 tracking policy**: 전신 모션 목표(root motion goal + expression goal)를 입력받아 joint commands를 생성하는 PPO 기반 RL 정책으로, 200 Hz 주기로 실행
- **중수준 IL 스킬 정책**: 인간 텔레오퍼레이션 데이터로부터 학습된 여러 skill policies가 egocentric visual observations와 proprioceptive states를 입력받아 target joint angles를 생성 (25 Hz)
- **고수준 VLM 플래너**: 저주파(1 Hz) VLM이 시각 및 텍스트 입력으로부터 스킬 시퀀스를 생성
- **VLM 모니터**: 고주파 VLM이 egocentric RGB 이미지 히스토리를 분석하여 현재 스킬의 완료 여부를 실시간으로 검증하고 스킬 전환 조율
- **인간 데이터 기반 학습**: human pose estimation으로 capture된 인간 자세 데이터를 로봇 morphology로 retargeting하여 IL 스킬 학습

## Originality

- **VLM 기반 모니터링 추가**: 기존 2계층 humanoid 구조에 skill completion verification을 위한 VLM 기반 실행 모니터를 새로운 계층으로 추가
- **계층적 planning 통합**: VLM 기반 planner가 IL 스킬 라이브러리와 직접 통합되어 자동 스킬 선택 및 순서화를 가능하게 함
- **실제 multi-step 작업 구현**: 기존 single-skill 시연을 넘어 obstacle pushing, object pickup, placement 등 여러 단계의 non-prehensile pick-and-place 작업 수행

## Limitation & Further Study

- **제한된 성공률**: 73% 성공률은 신뢰성 있는 자동화 배포에는 여전히 낮으며, 실패 사례 분석 및 오류 복구 전략이 미흡
- **단일 작업 검증**: 하나의 representative pick-and-place 작업으로만 검증되었으며, 다양한 작업 유형에 대한 일반화 능력 미실증
- **VLM 의존성**: pretrained VLM의 성능에 의존하므로, VLM의 오류가 시스템 전체 신뢰성을 제한
- **스킬 설계 비용**: IL 스킬 정책을 위해 각 작업마다 human teleoperation demonstrations 수집 필요
- **후속연구 방향**: (1) 오류 감지 및 복구 메커니즘 강화, (2) in-context learning을 통한 새로운 작업 적응성 개선, (3) 더 복잡한 다단계 작업으로 확대, (4) 다양한 humanoid 플랫폼으로의 전이 학습

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 humanoid 로봇의 자율적 다단계 조작을 위해 VLM 기반 계획 및 모니터링을 기존 2계층 제어에 추가하는 실용적인 접근을 제시하며, 실제 로봇 시험으로 기술적 가능성을 입증했다. 다만 73% 성공률과 단일 작업 검증은 추후 개선이 필요한 부분이다.

## Related Papers

- 🔄 다른 접근: [[papers/2018_HYPERmotion_Learning_Hybrid_Behavior_Planning_for_Autonomous/review]] — 계층적 비전-언어 계획과 하이브리드 행동 계획은 모두 복잡한 조작 작업을 다루지만 서로 다른 계층적 구조를 사용한다.
- 🔗 후속 연구: [[papers/1702_Task_and_Motion_Planning_for_Humanoid_Loco-manipulation/review]] — 휴머노이드 로코-조작을 위한 작업 및 모션 계획이 계층적 비전-언어 계획의 확장된 형태이다.
- 🏛 기반 연구: [[papers/1973_Hierarchical_Planning_and_Control_for_Box_Loco-Manipulation/review]] — 상자 로코-조작을 위한 계층적 계획이 다단계 조작의 기반 기술이다.
- 🏛 기반 연구: [[papers/1847_Commanding_Humanoid_by_Free-form_Language_A_Large_Language_A/review]] — Free-form language commanding이 hierarchical vision-language planning의 고수준 계획 기반이 됩니다.
- 🔄 다른 접근: [[papers/1992_Humanoid_Agent_via_Embodied_Chain-of-Action_Reasoning_with_M/review]] — Embodied chain-of-action reasoning이 3계층 hierarchical framework와 다른 방식으로 다단계 조작을 해결합니다.
- 🔗 후속 연구: [[papers/1663_SafeHumanoid_VLM-RAG-driven_Control_of_Upper_Body_Impedance/review]] — SafeHumanoid의 VLM-RAG driven control이 hierarchical VLM planning을 안전성 측면에서 확장합니다.
- 🔄 다른 접근: [[papers/2096_MetaWorld-X_Hierarchical_World_Modeling_via_VLM-Orchestrated/review]] — 복잡한 조작 작업을 이 논문은 3계층 구조로, MetaWorld-X는 VLM 오케스트레이션으로 해결한다.
- 🔗 후속 연구: [[papers/1842_CLOT_Closed-Loop_Global_Motion_Tracking_for_Whole-Body_Human/review]] — CLOT의 closed-loop 추적 기술을 다단계 조작 작업의 저수준 제어기로 확장 적용한 형태다.
- 🔗 후속 연구: [[papers/1638_Reinforcement_Learning_with_Data_Bootstrapping_for_Dynamic_S/review]] — Data bootstrapping을 vision-language planning과 결합한 확장 연구
- 🔗 후속 연구: [[papers/1702_Task_and_Motion_Planning_for_Humanoid_Loco-manipulation/review]] — 계층적 비전-언어 계획과 접촉 모드 통일 TAMP를 결합하면 언어 지시로부터 복잡한 로코-조작이 가능하다
- 🔗 후속 연구: [[papers/1617_PILOT_A_Perceptive_Integrated_Low-level_Controller_for_Loco-/review]] — PILOT의 perception-based control을 hierarchical vision-language planning으로 확장
- 🔄 다른 접근: [[papers/1992_Humanoid_Agent_via_Embodied_Chain-of-Action_Reasoning_with_M/review]] — 3계층 hierarchical framework가 embodied chain-of-action reasoning과 다른 방식으로 다단계 조작을 해결합니다.
- 🔄 다른 접근: [[papers/2018_HYPERmotion_Learning_Hybrid_Behavior_Planning_for_Autonomous/review]] — 하이브리드 행동 계획과 계층적 비전-언어 계획은 모두 복합적인 로코-조작 작업을 다루지만 서로 다른 통합 방식을 사용한다.
- 🏛 기반 연구: [[papers/2157_Towards_Proprioception-Aware_Embodied_Planning_for_Dual-Arm/review]] — Hierarchical Vision-Language Planning의 다단계 계획 기법이 dual-arm 휴머노이드의 고유감각 인식 구현화 계획을 위한 기반 방법론을 제공합니다.
- 🔄 다른 접근: [[papers/2166_ULTRA_Unified_Multimodal_Control_for_Autonomous_Humanoid_Who/review]] — hierarchical vision-language planning과 ULTRA의 unified multimodal controller는 다단계 휴머노이드 제어의 서로 다른 패러다임을 제시함
