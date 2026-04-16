---
title: "1326_CANVAS_Commonsense-Aware_Navigation_System_for_Intuitive_Hum"
authors:
  - "Suhwan Choi"
  - "Yongjun Cho"
  - "Minchan Kim"
  - "Jaeyoon Jung"
  - "Myunchul Joe"
date: "2024.10"
doi: ""
arxiv: ""
score: 4.0
essence: "CANVAS는 모호하거나 잡음이 있는 인간의 언어 및 시각적 지시(스케치, 텍스트)를 다중모드 입력으로 받아 상식적 이해를 바탕으로 로봇이 인간의 기대에 맞게 네비게이션을 수행하도록 하는 임베딩 러닝 기반 프레임워크이다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Instruction-Following_Robot_Navigation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Choi et al._2024_CANVAS Commonsense-Aware Navigation System for Intuitive Human-Robot Interaction.pdf"
---

# CANVAS: Commonsense-Aware Navigation System for Intuitive Human-Robot Interaction

> **저자**: Suhwan Choi, Yongjun Cho, Minchan Kim, Jaeyoon Jung, Myunchul Joe, Yubeen Park, Minseo Kim, Sungwoong Kim, Sungjae Lee, Hwiseong Park, Jiwan Chung, Youngjae Yu | **날짜**: 2024-10-02 | **URL**: [https://arxiv.org/abs/2410.01273](https://arxiv.org/abs/2410.01273)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Humans often give abstract navigation directions using simple instruction, relying on the recipient’s commonsens*

CANVAS는 모호하거나 잡음이 있는 인간의 언어 및 시각적 지시(스케치, 텍스트)를 다중모드 입력으로 받아 상식적 이해를 바탕으로 로봇이 인간의 기대에 맞게 네비게이션을 수행하도록 하는 임베딩 러닝 기반 프레임워크이다.

## Motivation

- **Known**: 로봇 네비게이션은 목적지 도달을 넘어 시나리오별 목표 최적화가 필요하며, 기존 ROS NavStack 같은 규칙 기반 시스템이나 ViNT, GNM 같은 비전 네비게이션 모델들이 존재한다. 임베딩 러닝은 로봇이 전문가 시연으로부터 학습하게 하는 효과적인 방식이다.
- **Gap**: 기존 방법들은 완전하거나 정확한 지시에 의존하거나 다양한 환경변화에 민감하며, 임베딩 러닝을 활용한 상식 기반 다중모드 네비게이션 시스템과 이를 훈련할 대규모 데이터셋이 부족하다.
- **Why**: 현실의 로봇 네비게이션은 인간이 주는 추상적이고 불완전한 지시를 해석해야 하는데, 이는 인간-로봇 상호작용의 자연성과 사용성을 크게 향상시킬 수 있다. 또한 Sim2Real 전이의 가능성을 보여줌으로써 시뮬레이션 환경에서의 학습이 실제 로봇 배포에 활용될 수 있음을 입증한다.
- **Approach**: CANVAS는 비전-언어 모델의 상식 지식을 활용하여 시각(스케치)과 언어 지시를 점진적 네비게이션 목표로 변환하며, 임베딩 러닝을 통해 인간 시연으로부터 학습한다. 동시에 COMMAND 데이터셋(48시간, 219km의 인간 주석 네비게이션 데이터)을 제시하여 모델 훈련을 지원한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Data collection pipeline for COMMAND dataset. (a) First, we create diverse navigation environments and extract m*

**ROS NavStack 대비 성능 우위**: 모든 환경에서 ROS NavStack을 능가하며, 특히 과수원 환경에서 ROS NavStack이 0% 성공률을 기록할 때 67% 성공률 달성
**대규모 고품질 데이터셋**: COMMAND는 48시간의 주행 데이터로 GoStanford의 약 3배 규모이며 3개 환경(사무실, 거리, 과수원)에서 3,343개의 인간 주석 네비게이션 결과 제공
**강력한 Sim2Real 전이**: 시뮬레이션만으로 훈련되었으나 실제 로봇 배포에서 69% 성공률로 우수한 성능 입증
**상식 제약 준수**: 인간 시연과 유사한 궤적을 따르며 상식 제약 위반이 적음을 정량적으로 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Data collection pipeline for COMMAND dataset. (a) First, we create diverse navigation environments and extract m*

- K-means clustering을 이용하여 연속 웨이포인트를 128개의 이산 웨이포인트 토큰으로 양자화하여 다중모드 동작 분포 모델링 강화
- 비전-언어 모델을 통해 스케치(이미지 상의 궤적)와 텍스트 설명을 입력으로 하여 점진적 네비게이션 목표 생성
- 인간 전문가의 텔레오퍼레이션 시연 데이터를 수집하여 임베딩 러닝 훈련
- 세 가지 서로 다른 환경(실내 사무실, 실외 거리, 과수원)에서 데이터 수집하여 환경 다양성 확보
- Trajectory Deviation Distance(TDD)와 Instruction Violation Rate(IVR) 두 가지 평가 지표 제안
- 시뮬레이션 환경에서 훈련하고 실제 로봇에 배포하여 Sim2Real 전이 검증

## Originality

- 모호하거나 잡음이 많은 인간 지시를 처리할 수 있는 상식 기반 다중모드 네비게이션 프레임워크 제시
- 스케치와 텍스트라는 직관적인 인터페이스를 결합한 새로운 네비게이션 입력 방식
- 기존 ViNT, GNM과 달리 미방문 위치와 환경 변화에 더 강건한 접근
- 상식 준수도를 정량화하기 위한 새로운 평가 지표(TDD, IVR) 도입
- 임베딩 러닝을 통해 보상 함수 설계의 어려움을 우회하는 실용적 해결책

## Limitation & Further Study

- 데이터셋이 세 가지 시뮬레이션 환경으로 제한되어 있으며, 실제 배포 테스트는 제한적
- 인간 주석 데이터의 질과 주석자 간 편향이 최종 성능에 영향을 미칠 수 있음
- 비전-언어 모델의 상식 지식이 충분하지 않거나 새로운 환경의 특수한 상식을 커버하지 못할 수 있음
- K-means 양자화의 토큰 수(128)가 최적인지, 다른 양자화 기법이 더 나을 수 있는지 검토 필요
- 후속연구로는 더 다양한 실제 환경에서의 대규모 배포 실험, 온라인 학습을 통한 적응성 개선, 다국어 지시 처리 등이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: CANVAS는 추상적이고 잡음이 있는 인간 지시를 상식 기반으로 해석하여 로봇 네비게이션을 수행하는 혁신적인 프레임워크이며, 대규모 COMMAND 데이터셋과 함께 강력한 성능(특히 어려운 환경에서 67% vs 0%), 그리고 우수한 Sim2Real 전이(69%)를 입증함으로써 인간-로봇 상호작용의 자연성 향상과 현실 적용 가능성을 효과적으로 제시한다.

## Related Papers

- 🔗 후속 연구: [[papers/1461_LM-Nav_Robotic_Navigation_with_Large_Pre-Trained_Models_of_L/review]] — CANVAS의 상식 기반 네비게이션과 LM-Nav의 대형 사전훈련 모델 기반 로봇 네비게이션은 언어 이해 기반 이동의 보완적 접근법이다.
- 🔄 다른 접근: [[papers/1402_GC-VLN_Instruction_as_Graph_Constraints_for_Training-free_Vi/review]] — CANVAS의 다중모드 지시 처리와 GC-VLN의 그래프 제약 기반 네비게이션은 인간-로봇 네비게이션 인터페이스의 서로 다른 방식이다.
- 🏛 기반 연구: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — Visual Language Maps의 로봇 네비게이션 기술은 CANVAS의 상식 기반 네비게이션 시스템에 공간 표현의 기반을 제공한다.
- 🔗 후속 연구: [[papers/1340_Context-Aware_Entity_Grounding_with_Open-Vocabulary_3D_Scene/review]] — Context-Aware Entity Grounding의 open-vocabulary 개념을 모호한 인간 지시 처리로 확장한 응용입니다.
- 🔄 다른 접근: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — 상식 인식 네비게이션에서 스케치/텍스트 다중모드 입력과 비디오 기반 VLM 계획이 다른 접근법을 제시합니다.
- 🔗 후속 연구: [[papers/1575_SmartWay_Enhanced_Waypoint_Prediction_and_Backtracking_for_Z/review]] — 향상된 경로점 예측과 백트래킹을 CANVAS의 상식 인식 네비게이션에 통합할 수 있습니다.
- 🧪 응용 사례: [[papers/1586_TidyBot_Personalized_Robot_Assistance_with_Large_Language_Mo/review]] — CANVAS는 TidyBot의 개인화된 정리 능력을 직관적 인간-로봇 네비게이션에 적용하는 구체적 사례다.
