---
title: "1317_BEHAVIOR-1K_A_Human-Centered_Embodied_AI_Benchmark_with_1000"
authors:
  - "Chengshu Li"
  - "Ruohan Zhang"
  - "Josiah Wong"
  - "Cem Gokmen"
  - "Sanjana Srivastava"
date: "2024.03"
doi: ""
arxiv: ""
score: 4.0
essence: "BEHAVIOR-1K는 1,461명의 일반인 조사를 통해 도출한 1,000개의 일상 활동을 정의하고, 이를 realistic physics simulation과 rendering을 지원하는 OMNIGIBSON 환경에서 실행할 수 있는 embodied AI 벤치마크이다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/GPU-Accelerated_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2024_BEHAVIOR-1K A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Si.pdf"
---

# BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation

> **저자**: Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gokmen, Sanjana Srivastava, Roberto Martín-Martín, Chen Wang, Gabrael Levine, Wensi Ai, Benjamin Martinez, Hang Yin, Michael Lingelbach, Minjune Hwang, Ayano Hiranaka, Sujay Garlanka, Arman Aydin, Sharon Lee, Jiankai Sun, Mona Anvari, Manasi Sharma, Dhruva Bansal, Samuel Hunter, Kyu-Young Kim, Alan Lou, Caleb R Matthews, Ivan Villa-Renteria, Jerry Huayang Tang, Claire Tang, Fei Xia, Yunzhu Li, Silvio Savarese, Hyowon Gweon, C. Karen Liu, Jiajun Wu, Li Fei-Fei | **날짜**: 2024-03-14 | **URL**: [https://arxiv.org/abs/2403.09227](https://arxiv.org/abs/2403.09227)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Developing a Human-Centered Benchmark for Embodied AI. Left: human preference score over*

BEHAVIOR-1K는 1,461명의 일반인 조사를 통해 도출한 1,000개의 일상 활동을 정의하고, 이를 realistic physics simulation과 rendering을 지원하는 OMNIGIBSON 환경에서 실행할 수 있는 embodied AI 벤치마크이다.

## Motivation

- **Known**: 컴퓨터 비전과 NLP에서 벤치마크의 중요성이 확립되었으며, 로보틱스 커뮤니티도 여러 시뮬레이션 벤치마크를 개발해왔다. 그러나 기존 벤치마크는 연구자 기반 설계와 다양성-현실성 간의 trade-off 문제를 가지고 있다.
- **Gap**: 기존 벤치마크들은 실제 인간의 필요와 선호도를 충분히 반영하지 못하고 있으며, 1,000개 규모의 diverse activities를 모두 realistic simulation으로 지원하는 통합 플랫폼이 부재하다.
- **Why**: human-centered AI는 실제 사용자의 needs, goals, values를 반영해야 하며, diverse한 일상 활동을 realistic하게 시뮬레이션할 수 있는 벤치마크는 embodied AI와 로봇 학습 연구의 발전을 가속화할 수 있다.
- **Approach**: Amazon Mechanical Turk에서 1,461명을 대상으로 2,090개 활동에 대한 선호도 조사를 수행하여 1,000개의 상위 활동을 선정하고, Nvidia Omniverse와 PhysX 5 기반의 OMNIGIBSON 환경에서 이들 활동을 rigid bodies, deformable bodies, liquids의 realistic physics simulation으로 구현했다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Elements of BEHAVIOR-1K. Our benchmark comprises two elements: BEHAVIOR-1K DATASET*

- **Human-Grounded Benchmark Design**: 1,461명의 일반 대중 조사를 통해 인간의 실제 선호도에 기반한 1,000개 일상 활동 정의
- **BEHAVIOR-1K Dataset**: 50개의 diverse scenes (주택, 정원, 레스토랑, 사무실 등)와 9,000+ 개의 rich physical/semantic annotations을 가진 3D 객체 모델 제공
- **OMNIGIBSON Simulation Environment**: rigid bodies, deformable bodies, liquids의 realistic physics simulation과 temperature, toggled, soaked, dirtiness 등 확장된 object states 지원
- **Sim-to-Real Validation**: mobile manipulator를 사용한 시뮬레이션-현실 간 전이 학습 초기 연구 제시
- **Difficulty Analysis**: state-of-the-art RL 알고리즘들이 해결하기 어려운 long-horizon, complex manipulation 활동임을 실증

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Comparison of Visual Realism: We evaluate OMNIGIBSON’s visual realism against other simulation*

- Time-use surveys와 WikiHow 기사에서 약 2,000개의 활동 소싱
- Amazon Mechanical Turk에서 1,461명 참여자를 대상으로 10-point Likert scale로 각 활동당 50개 응답 수집
- Gini index 0.158로 측정된 높은 분산의 활동 선호도 분포 확인
- Predicate logic으로 활동의 초기 조건, 목표 조건, 관련 객체, 상태 전이 정의
- Nvidia Omniverse와 PhysX 5를 기반으로 OMNIGIBSON 개발 및 확장 object states 구현
- Reinforcement learning (DRL algorithms)과 sampling-based motion planning을 활용한 baseline 평가
- Mobile manipulator의 현실 로봇 실험을 통한 simulation-to-reality gap 검증

## Originality

- **Human-Centric Survey-Based Design**: 기존 벤치마크와 달리 실제 일반 대중의 선호도 조사를 통해 활동 선정 (최초)
- **Scale and Diversity**: 1,000개 활동, 50개 장면, 9,000+ 객체 모델로 unprecedented scale의 diverse embodied AI benchmark 구현
- **Realistic Physics-Semantic Integration**: rigid/deformable bodies, liquids, extended object states를 통합한 포괄적 physics simulation
- **Commonsense Knowledge Base**: Predicate logic 기반의 structured activity definitions로 활동의 semantics 명시적 표현
- **Empirical Difficulty Assessment**: long-horizon, complex manipulation 활동의 difficulty를 체계적으로 분석

## Limitation & Further Study

- Simulation-to-reality gap이 존재하며, mobile manipulator 예제만 제시되어 다양한 로봇 플랫폼에 대한 전이 성능 미검증
- State-of-the-art RL 알고리즘들이 현저히 낮은 성공률을 보여 immediate practical applicability 제한
- 1,000개 활동 중 일부만 상세히 분석되어 전체 활동의 특성 완전히 파악 어려움
- Human preference score가 활동의 실제 complexity/difficulty와의 correlation 분석 부족
- 후속 연구에서 advanced learning algorithms, meta-learning, curriculum learning 등을 통한 성능 개선 필요
- 다양한 로봇 morphology (bipedal, mobile base 등)에 대한 확장 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: BEHAVIOR-1K는 human-grounded survey, 대규모 diverse activities, realistic physics simulation을 통합하여 embodied AI 연구의 새로운 표준을 제시한 획기적인 벤치마크이다. 실제 인간 필요에 기반한 설계와 unprecedented scale의 다양성은 로봇 학습 커뮤니티에 significant impact을 미칠 것으로 예상된다.

## Related Papers

- 🔗 후속 연구: [[papers/1312_ARNOLD_A_Benchmark_for_Language-Grounded_Task_Learning_With/review]] — BEHAVIOR-1K의 1,000개 일상 활동과 ARNOLD의 언어 기반 조작 작업은 현실적 물리 시뮬레이션 기반 벤치마크의 확장이다.
- 🔄 다른 접근: [[papers/1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit/review]] — BEHAVIOR-1K와 Habitat 2.0은 모두 가정 환경 기반 embodied AI 시뮬레이션이지만 작업 범위와 복잡도가 다르다.
- 🏛 기반 연구: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — ManiSkill3의 GPU 병렬화 로봇 시뮬레이션은 BEHAVIOR-1K의 대규모 일상 활동 시뮬레이션에 기술적 기초를 제공한다.
- 🔄 다른 접근: [[papers/1430_iGibson_10_a_Simulation_Environment_for_Interactive_Tasks_in/review]] — 상호작용 작업을 위한 iGibson 1.0과 일상 활동 중심의 BEHAVIOR-1K가 다른 벤치마크 접근법을 제시합니다.
- 🔗 후속 연구: [[papers/1563_Scaling_Instructable_Agents_Across_Many_Simulated_Worlds/review]] — 여러 시뮬레이션 세계에서의 지시 따르기 에이전트 스케일링을 BEHAVIOR-1K 벤치마크로 확장할 수 있습니다.
- 🔗 후속 연구: [[papers/1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit/review]] — BEHAVIOR-1K는 Habitat 2.0의 가정용 로봇 학습 환경을 1000개 작업으로 대폭 확장한 벤치마크임
- 🏛 기반 연구: [[papers/1430_iGibson_10_a_Simulation_Environment_for_Interactive_Tasks_in/review]] — BEHAVIOR-1K의 human-centered embodied task 개념을 15개 대규모 실내 장면으로 확장한 구현체이다.
- 🧪 응용 사례: [[papers/1522_RDT-1B_a_Diffusion_Foundation_Model_for_Bimanual_Manipulatio/review]] — RDT의 bimanual manipulation 능력을 BEHAVIOR-1K의 다양한 human-centered embodied tasks에서 평가하고 적용할 수 있다.
- 🔄 다른 접근: [[papers/1531_RLBench_The_Robot_Learning_Benchmark__Learning_Environment/review]] — BEHAVIOR-1K와 함께 대규모 로봇 학습 벤치마크를 제공하지만 RLBench는 손 설계 태스크에, BEHAVIOR-1K는 인간 중심 태스크에 집중한다.
- 🏛 기반 연구: [[papers/1539_RoboFactory_Exploring_Embodied_Agent_Collaboration_with_Comp/review]] — BEHAVIOR-1K의 human-centered embodied AI 벤치마크가 RoboFactory의 다중 에이전트 조작 태스크 설계의 기반을 제공한다.
- 🏛 기반 연구: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — BEHAVIOR-1K의 인간 중심적 벤치마크 설계 철학이 VLABench의 자연어 지시와 상식 추론 평가 설계에 기반이 된다
- 🔗 후속 연구: [[papers/1312_ARNOLD_A_Benchmark_for_Language-Grounded_Task_Learning_With/review]] — ARNOLD의 연속적 객체 상태 이해와 BEHAVIOR-1K의 1,000개 일상 활동은 복잡한 물리 시뮬레이션 기반 언어 조건부 작업의 진화이다.
