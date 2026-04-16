---
title: "1390_Expressive_Whole-Body_Control_for_Humanoid_Robots"
authors:
  - "Xuxin Cheng"
  - "Yandong Ji"
  - "Junming Chen"
  - "Ruihan Yang"
  - "Ge Yang"
date: "2024.02"
doi: ""
arxiv: ""
score: 4.0
essence: "인간형 로봇이 인간의 모션 캡처 데이터를 학습하여 표현력 있는 전신 움직임을 수행하도록 강화학습 기반의 제어 정책을 제안하며, 상체는 참조 모션을 모방하되 하체는 속도 명령만 따르도록 제약을 완화하여 실제 로봇에서의 동작을 가능하게 함."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Humanoid_Robot_Teleoperation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Cheng et al._2024_Expressive Whole-Body Control for Humanoid Robots.pdf"
---

# Expressive Whole-Body Control for Humanoid Robots

> **저자**: Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, Xiaolong Wang | **날짜**: 2024-02-26 | **URL**: [https://arxiv.org/abs/2402.16796](https://arxiv.org/abs/2402.16796)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of our framework. Our framework is able to train on data from various sources such as static human moti*

인간형 로봇이 인간의 모션 캡처 데이터를 학습하여 표현력 있는 전신 움직임을 수행하도록 강화학습 기반의 제어 정책을 제안하며, 상체는 참조 모션을 모방하되 하체는 속도 명령만 따르도록 제약을 완화하여 실제 로봇에서의 동작을 가능하게 함.

## Motivation

- **Known**: 기존의 physics-based character animation은 그래픽 분야에서 자연스러운 제어 정책을 생성하지만, 현실의 로봇 하드웨어에 과도한 액추에이터 이득을 요구하고 자유도 불일치 문제가 있음. 심화강화학습 기반 보행 제어는 다양한 다리 로봇에서 견고성을 입증했음.
- **Gap**: 인간 모션 캡처 데이터의 큰 자유도와 로봇의 제한된 자유도 사이의 간극, 그리고 그래픽 기법의 현실 로봇 적용 불가능성으로 인해 다양한 표현력 있는 인간형 로봇 제어가 실제 환경에서 실현되지 못함.
- **Why**: 인간형 로봇이 단순한 작업 수행을 넘어 인간과 자연스럽고 표현력 있게 상호작용할 수 있다면 로봇의 활용도와 수용성이 크게 증가할 수 있으며, 이는 인간-로봇 협력의 새로운 가능성을 열어줌.
- **Approach**: 상체 모방 제약과 하체 속도 추적을 분리하는 이중 목표 강화학습 프레임워크를 도입하고, 시뮬레이션에서 다양한 지형으로 훈련 후 Sim2Real 전이를 통해 실제 Unitree H1 로봇에 배포함.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Our Robot demonstrates diverse and expressive whole-body movements in different scenarios. Top Row: The robot is*

- **다양한 표현력 있는 동작**: 로봇이 춤추기, 악수하기, 손 흔들기, 좀비 보행 등 다양한 스타일의 보행과 상체 표현을 인간과 함께 실제 환경에서 수행 가능
- **견고한 지형 적응성**: 자갈길, 나무칩 길, 잔디, 경사진 포장도로, 연석 등 다양한 지형에서 안정적으로 동작
- **소수 모션 데이터로 효율적 학습**: 780개의 CMU MoCap 데이터(약 3.7시간)를 활용하여 기존 방법 대비 훨씬 적은 학습 데이터로 우수한 성능 달성
- **배포 용이성**: 조이스틱 명령으로 직관적 제어 가능하며 단일 네트워크로 운영되어 실시간 배포에 적합

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of our framework. Our framework is able to train on data from various sources such as static human moti*

- CMU MoCap 데이터에서 신체 상호작용, 무거운 물체 조작, 거친 지형 모션을 제외하여 큐레이션
- 인간 모션을 로봇의 운동학 구조에 맞게 retargeting하여 호환 가능한 모션 클립 라이브러리 구성
- 목표 공간을 표현 목표 Ge(상체 관절 9개, 키포인트 18개)와 근 움직임 목표 Gm(속도, 자세, 높이)으로 분리
- 강화학습 보상 함수를 상체 모방 항(expression goal)과 하체 속도 추적 항(root movement goal)으로 설계
- 다양한 지형과 매개변수 변동성으로 시뮬레이션 훈련 시 도메인 랜더마이제이션 적용
- 정책 상태 분포를 분석하여 학습 효율성 검증 및 모션 샘플링 전략 최적화

## Originality

- 기존 physics-based character animation과 RL 기반 보행 제어의 한계를 동시에 극복하는 하이브리드 접근법
- 상체와 하체의 제약 조건을 차등적으로 적용하는 이중 목표 설계로 기존의 일괄적 모방 전략과 차별화
- CMU MoCap 같은 기존 대규모 모션 데이터셋을 로봇 제어에 효과적으로 재활용하는 새로운 방법론
- 실제 인간형 로봇(Unitree H1)에서 처음으로 다양한 표현력 있는 모션을 성공적으로 시연한 학습 기반 접근

## Limitation & Further Study

- 현재 방법은 상체 모션만 표현력 있게 모방하고 하체는 속도만 추적하므로, 하체의 표현력 있는 동작(예: 발차기, 점프)은 제한됨
- CMU MoCap 데이터의 편향된 분포(Fig. 3)가 특정 유형의 모션에 대한 학습 성능에 영향을 미칠 수 있음
- 현재 연구는 보행 중심이며, 물체 조작과 같은 전신 상호작용이 필요한 복잡한 작업에 대한 확장이 필요
- Unitree H1 로봇 특화로 다른 인간형 로봇 플랫폼으로의 일반화 가능성 검증 부족
- 후속 연구로는 diffusion model이나 video-to-skeleton 모델 같은 다양한 모션 생성 소스의 활용, 하체 표현력 확장, 복잡한 조작 작업의 통합 등이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 인간 모션 캡처 데이터를 실제 인간형 로봇에 효과적으로 적용하는 창의적인 문제 분해 방식과 차등적 제약 설계로, 학습 기반 인간형 로봇 제어 분야에서 처음으로 다양한 표현력 있는 동작을 실현함. 명확한 동기, 실제 로봇 검증, 그리고 우수한 성과에도 불구하고 기술적 신규성이 개별 컴포넌트 수준에서는 제한적이며, 하체 표현력과 다양한 작업 확장에 대한 연구가 필요함.

## Related Papers

- 🔗 후속 연구: [[papers/1279_BEHAVIOR_Robot_Suite_Streamlining_Real-World_Whole-Body_Mani/review]] — 인간형 로봇의 표현력 있는 전신 제어와 BEHAVIOR Robot Suite의 전신 조작은 휴머노이드 로봇의 상호 보완적인 움직임 기술이다.
- 🏛 기반 연구: [[papers/1451_Learning_Human-to-Humanoid_Real-Time_Whole-Body_Teleoperatio/review]] — 인간-휴머노이드 실시간 전신 텔레오퍼레이션 학습은 표현력 있는 전신 제어의 인간 모션 캡처 학습에 데이터 수집 기반을 제공한다.
- 🔄 다른 접근: [[papers/1426_HumanPlus_Humanoid_Shadowing_and_Imitation_from_Humans/review]] — 표현력 있는 전신 제어와 HumanPlus 휴머노이드 섀도잉은 인간 동작 모방의 서로 다른 학습 및 제어 접근법이다.
- 🧪 응용 사례: [[papers/1498_OmniH2O_Universal_and_Dexterous_Human-to-Humanoid_Whole-Body/review]] — OmniH2O는 표현력 있는 전신 제어 방법론을 범용적인 인간-휴머노이드 제어 시스템으로 실용화함
- 🏛 기반 연구: [[papers/1526_Real-World_Humanoid_Locomotion_with_Reinforcement_Learning/review]] — 인간형 로봇의 locomotion에 대한 강화학습 기반 제어의 기초 연구입니다.
- 🔗 후속 연구: [[papers/1279_BEHAVIOR_Robot_Suite_Streamlining_Real-World_Whole-Body_Mani/review]] — BEHAVIOR Robot Suite의 전신 조작과 인간형 로봇의 표현력 있는 전신 제어는 상호 보완적인 휴머노이드 조작 기술이다.
- 🏛 기반 연구: [[papers/1451_Learning_Human-to-Humanoid_Real-Time_Whole-Body_Teleoperatio/review]] — 표현력 있는 전신 제어 정책이 H2O의 실시간 원격조종 시스템 설계의 기술적 기반이 됨
- 🏛 기반 연구: [[papers/1498_OmniH2O_Universal_and_Dexterous_Human-to-Humanoid_Whole-Body/review]] — whole-body 휴머노이드 제어 기술은 OmniH2O의 전신 텔레오퍼레이션 구현에 필수적인 기반입니다.
- 🧪 응용 사례: [[papers/1526_Real-World_Humanoid_Locomotion_with_Reinforcement_Learning/review]] — expressive whole-body control의 개념을 causal transformer 기반 강화학습 정책에 적용하여 실제 휴머노이드 로봇의 안정적인 보행을 실현한다.
- 🔗 후속 연구: [[papers/1628_WholeBodyVLA_Towards_Unified_Latent_VLA_for_Whole-Body_Loco-/review]] — expressive whole-body control을 vision-language-action framework로 확장하여 더 지능적인 전신 제어를 제시합니다.
