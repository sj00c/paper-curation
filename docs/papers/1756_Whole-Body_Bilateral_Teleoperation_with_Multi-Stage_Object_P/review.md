---
title: "1756_Whole-Body_Bilateral_Teleoperation_with_Multi-Stage_Object_P"
authors:
  - "Donghoon Baek"
  - "Amartya Purushottam"
  - "Jason J. Choi"
  - "Joao Ramos"
date: "2025.08"
doi: ""
arxiv: ""
score: 4.0
essence: "휠 달린 인간형 로봇의 원격조종 시스템에 다단계 물체 관성 매개변수 온라인 추정을 통합하여, 무거운 물체의 들기·운반 작업을 동적으로 수행할 수 있는 프레임워크를 제시한다."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Tactile_Contact_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Baek et al._2025_Whole-Body Bilateral Teleoperation with Multi-Stage Object Parameter Estimation for Wheeled Humanoid.pdf"
---

# Whole-Body Bilateral Teleoperation with Multi-Stage Object Parameter Estimation for Wheeled Humanoid Locomanipulation

> **저자**: Donghoon Baek, Amartya Purushottam, Jason J. Choi, Joao Ramos | **날짜**: 2025-08-13 | **URL**: [https://arxiv.org/abs/2508.09846](https://arxiv.org/abs/2508.09846)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the whole-body bilateral teleoperation framework. (Left) A human pilot controls a wheeled humanoid w*

휠 달린 인간형 로봇의 원격조종 시스템에 다단계 물체 관성 매개변수 온라인 추정을 통합하여, 무거운 물체의 들기·운반 작업을 동적으로 수행할 수 있는 프레임워크를 제시한다.

## Motivation

- **Known**: 인간형 로봇의 생동감 있는 동작과 인간-로봇 협력을 위한 양방향 원격조종(bilateral teleoperation) 기술이 진전되었으며, 동적 유사성과 haptic force feedback를 통한 동기화 방법이 알려져 있다.
- **Gap**: 기존 인간형 로봇의 원격조종은 경량 물체만 다루었고, 물체의 관성 매개변수를 모르는 상황에서 무거운 물체를 들어올리고 운반하는 작업에는 대응하지 못했으며, 관성 매개변수 식별 방법은 장시간 지속 여기 신호나 센서가 필요했다.
- **Why**: 물체의 동역학을 추정하면 로봇이 새로운 평형점으로 동작을 자동 조정할 수 있어 조종자의 인지 부담을 줄이고 안정적인 haptic feedback을 유지하면서 더 무거운 부하를 다룰 수 있게 되므로 실제 작업 적용성을 크게 높인다.
- **Approach**: Vision 기반 물체 크기 추정, VLM(Vision-Language Model) 사전 정보, decoupled hierarchical sampling strategy를 순차적으로 통합하는 3단계 온라인 추정 프로세스를 개발하고, 이를 고충실도 simulation과 실제 하드웨어에서 병렬 실행하여 real-time parameter 업데이트를 달성한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Lifting and delivering a heavy water bottle (∼1/3 of robot’s weight)*

- **다단계 온라인 물체 매개변수 추정**: VLM 사전 정보와 hierarchical sampling을 통해 지속 여기 신호나 F/T 센서 없이도 물리적으로 타당한 관성 매개변수를 빠르게 추정
- **물체 인식 양방향 원격조종 프레임워크**: 추정된 물체 동역학을 활용하여 operator의 haptic feedback을 개선하고 복잡한 loco-manipulation을 가능하게 함
- **Sim-to-real 적응 전략**: 고충실도 simulation과 hardware 간의 직접 연계로 parameter 추정의 정확성과 신뢰성 향상
- **적응형 조작 제어**: Control Barrier Function과 물체 매개변수 추정을 통합한 robust control framework 개발
- **실제 검증**: 로봇 체중의 약 1/3에 해당하는 무거운 물체(물병)를 들기, 운반, 놓기 작업을 real-time으로 성공적 수행

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Overview of the multi-stage object inertial parameter estimation*

- Vision 기반 3D 물체 크기 추정 (CenterSnap 사용)
- VLM을 통한 초기 관성 매개변수 후보 생성으로 탐색 공간 축소
- Hierarchical sampling: 질량·무게중심 추정 후 물체 크기로부터 관성 추정
- Decoupled multi-hypothesis scheme으로 VLM 오류에 대한 강건성 확보
- 고충실도 rigid-body simulation과 실제 hardware에서 병렬 sampling 기반 refinement
- Kinematic arm retargeting과 dynamic locomotion retargeting를 결합한 원격조종 매핑
- Gain-scheduled LQR과 task-space controller를 활용한 whole-body control
- CBF(Control Barrier Function) 기반 안전성 필터 적용
- HMI(Human-Machine Interface)를 통한 전체 신체 haptic feedback 제공

## Originality

- VLM 사전 정보를 활용하여 물체 매개변수 추정의 탐색 공간을 크게 축소하는 혁신적 접근
- 지속 여기 신호나 F/T 센서 없이 online parameter estimation을 가능하게 하는 다단계 구조의 창안
- Hierarchical sampling 전략으로 물리적 타당성을 자동 보장하는 방법론
- Sim-to-real 적응을 통해 sampling 기반 추정의 신뢰성을 향상시키는 독자적 전략
- 물체 동역학 추정을 bilateral teleoperation과 명시적으로 통합하여 조종자의 인지 부담을 경감하는 시스템 설계

## Limitation & Further Study

- VLM의 오류에 대한 의존도 및 강건성—multi-hypothesis 스키마가 완벽한 보정을 보장하지 않을 수 있음
- 실험이 한정된 형태의 물체(물병)에 대해서만 검증되었으며, 다양한 물체 형상·재질에 대한 일반화 가능성이 미흡
- 로봇 체중의 1/3 수준까지만 검증되었으므로 더 무거운 부하에 대한 성능 미지수
- Simulation과 hardware 간의 discrepancy 처리 방법이 제한적일 수 있음
- 후속 연구: 다양한 물체 형상·특성에 대한 일반화, 더 큰 부하에서의 성능 검증, VLM 대체 또는 정교화 방법 개발, 실시간 환경 변화(접촉 미끄러짐 등)에 대한 robust estimation 강화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 VLM과 hierarchical sampling을 결합한 혁신적 물체 매개변수 추정과 이를 bilateral teleoperation에 통합함으로써 로봇의 무거운 부하 취급 능력을 획기적으로 향상시켰다. 시스템 설계, 기술 구현, 실험 검증 모두 우수하며 로봇 조작 작업의 실용화에 중요한 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1672_SignBot_Learning_Human-to-Humanoid_Sign_Language_Interaction/review]] — 휴머노이드의 인간과의 상호작용에서 물리적 협력(물체 조작)과 의사소통(수화)이라는 서로 다른 상호작용 방식을 다룬다.
- 🔗 후속 연구: [[papers/1970_Heavy_lifting_tasks_via_haptic_teleoperation_of_a_wheeled_hu/review]] — 무거운 물체 조작에서 다단계 매개변수 추정과 haptic teleoperation이라는 보완적 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1991_Human-Robot_Collaboration_for_the_Remote_Control_of_Mobile_H/review]] — mobile humanoid의 원격 제어에서 물체 조작과 인간-로봇 협력이라는 관련 연구 영역을 다룬다.
- 🔄 다른 접근: [[papers/1839_CLONE_Closed-Loop_Whole-Body_Humanoid_Teleoperation_for_Long/review]] — 두 시스템 모두 전신 휴머노이드 원격조작을 다루지만 CLONE은 closed-loop 제어에, 이 연구는 물체 매개변수 추정에 중점을 둡니다.
- 🏛 기반 연구: [[papers/1921_ExtremControl_Low-Latency_Humanoid_Teleoperation_with_Direct/review]] — 저지연 원격조작 기술이 물체 매개변수를 실시간으로 추정하고 적용하는 기반 기술을 제공합니다.
- 🔗 후속 연구: [[papers/1672_SignBot_Learning_Human-to-Humanoid_Sign_Language_Interaction/review]] — 휴머노이드의 인간과의 상호작용에서 의사소통(수화)과 물리적 협력(물체 조작)이라는 보완적 기능을 다룬다.
- 🔗 후속 연구: [[papers/1706_TeleOpBench_A_Simulator-Centric_Benchmark_for_Dual-Arm_Dexte/review]] — TeleOpBench의 쌍팔 벤치마크와 전신 양방향 텔레오퍼레이션을 결합하면 더 포괄적인 조작 평가가 가능하다
- 🏛 기반 연구: [[papers/1835_CHILD_Controller_for_Humanoid_Imitation_and_Live_Demonstrati/review]] — 전신 양측 텔레오퍼레이션의 다단계 객체 처리 기술이 CHILD의 전신 관절 수준 제어 시스템 설계에 기초적인 프레임워크를 제공한다.
- 🏛 기반 연구: [[papers/1839_CLONE_Closed-Loop_Whole-Body_Humanoid_Teleoperation_for_Long/review]] — 전신 양측 텔레오퍼레이션의 다단계 객체 처리 기술이 CLONE의 장시간 작업에서 위치 드리프트 최소화에 필요한 기술적 토대를 제공한다.
- 🔗 후속 연구: [[papers/1931_Flow_Matching_Imitation_Learning_for_Multi-Support_Manipulat/review]] — 전신 양손 원격조작이 다중 지지점 조작의 실제 적용으로 확장될 수 있다.
- 🏛 기반 연구: [[papers/1963_H2-COMPACT_Human-Humanoid_Co-Manipulation_via_Adaptive_Conta/review]] — Whole-body bilateral teleoperation 기술이 human-humanoid co-manipulation의 기반이 됩니다.
- 🏛 기반 연구: [[papers/1983_HOMIE_Humanoid_Loco-Manipulation_with_Isomorphic_Exoskeleton/review]] — Whole-body bilateral teleoperation이 HOMIE의 loco-manipulation 통합 제어의 기반이 됩니다.
- 🔗 후속 연구: [[papers/2043_Learning_Adaptive_Neural_Teleoperation_for_Humanoid_Robots_F/review]] — Learning Adaptive의 적응형 신경 텔레오퍼레이션이 전신 양측 텔레오퍼레이션의 다단계 객체 처리와 결합되어 더 정교한 조작 가능
- 🔄 다른 접근: [[papers/2163_TWIST_Teleoperated_Whole-Body_Imitation_System/review]] — 전신 모방 원격조작과 양손 정교 원격조작은 모두 원격조작이지만 서로 다른 범위와 접근법을 사용한다.
- 🔄 다른 접근: [[papers/2147_TeleGate_Whole-Body_Humanoid_Teleoperation_via_Gated_Expert/review]] — gated expert selection 대신 다단계 객체 인식을 통한 전신 양손 원격조종 접근법을 제시한다.
