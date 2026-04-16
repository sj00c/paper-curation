---
title: "1644_RoboCasa_Large-Scale_Simulation_of_Everyday_Tasks_for_Genera"
authors:
  - "Soroush Nasiriany"
  - "Abhiram Maddukuri"
  - "Lance Zhang"
  - "Adeet Parikh"
  - "Aaron Lo"
date: "2024.06"
doi: ""
arxiv: ""
score: 4.0
essence: "RoboCasa는 kitchen 환경에 중점을 둔 대규모 로봇 시뮬레이션 프레임워크로, 생성형 AI를 활용하여 다양한 3D 자산과 task를 확보하고 100K 이상의 synthetic trajectory로 generalist robot 학습을 가능하게 한다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Egocentric_Manipulation_Imitation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Nasiriany et al._2024_RoboCasa Large-Scale Simulation of Everyday Tasks for Generalist Robots.pdf"
---

# RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots

> **저자**: Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, Yuke Zhu | **날짜**: 2024-06-04 | **URL**: [https://arxiv.org/abs/2406.02523](https://arxiv.org/abs/2406.02523)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of RoboCasa. RoboCasa is a simulation framework for training generalist robot agents. Four pillars unde*

RoboCasa는 kitchen 환경에 중점을 둔 대규모 로봇 시뮬레이션 프레임워크로, 생성형 AI를 활용하여 다양한 3D 자산과 task를 확보하고 100K 이상의 synthetic trajectory로 generalist robot 학습을 가능하게 한다.

## Motivation

- **Known**: 로봇 학습을 위해서는 대규모 dataset이 필요하며, 현실 세계 데이터 수집은 비용과 노력이 많이 든다. 최근 simulation 기반의 로봇 학습과 imitation learning이 주목받고 있다.
- **Gap**: 기존 simulation framework들은 realistic physics, diverse scenes/assets, room-scale 환경, 대규모 dataset을 모두 만족하는 경우가 드물다. 또한 생성형 AI를 활용한 대규모 asset과 task 생성을 통합한 프레임워크가 부재했다.
- **Why**: 로봇 학습의 scaling을 위해서는 현실적이고 다양한 환경에서의 대규모 합성 데이터가 필수적이며, 이는 real-world 로봇 배포의 성능 향상으로 이어진다.
- **Approach**: RoboCasa는 MuJoCo 기반의 modular framework에 generative AI 도구(text-to-3D, text-to-image)를 활용하여 2,500+ 3D object, 120 kitchen scene, 100 task를 구축하고, human demonstration과 MimicGen을 통한 automated trajectory generation으로 dataset을 확대한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of RoboCasa. RoboCasa is a simulation framework for training generalist robot agents. Four pillars unde*

- **Framework 구성**: realistic kitchen scene, diverse interactable furniture/appliances, cross-embodiment support (mobile manipulator, humanoid, quadruped)를 갖춘 simulation framework 개발
- **AI 활용 asset/task 생성**: text-to-3D, text-to-image, LLM 활용으로 2,500+ object (150+ category), 100 task (atomic 25 + composite 75) 구축
- **대규모 dataset**: human demonstration과 MimicGen 기반 automated generation으로 100K+ trajectory 확보
- **Scaling 검증**: synthetic data 증가에 따른 성능 향상을 실증하였고, real-world kitchen에서 simulation co-training의 effectiveness 증명

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Kitchen Floor Plans. We consult home planning and architecture magazines and compile a list of common kitchen fl*

- Kitchen 설계: architecture/home design magazine 참고하여 다양한 kitchen layout과 style 모델링
- Object asset: 2,500+ 3D object를 text-to-3D 모델로 생성하여 150+ category 확보
- Environment texture: text-to-image 모델로 rendering realism 향상
- Task design: 25개 atomic task (picking, placing, opening door, twisting knob)와 LLM 제안 기반 75개 composite task (washing dishes, frying, restocking) 구성
- Dataset augmentation: MimicGen 확장으로 atomic task에 100K trajectory 자동 생성
- Learning: behavioral cloning으로 human demonstration + generated data를 활용한 policy 학습
- Real-world validation: real kitchen 환경에서 sim-trained policy의 transfer 성능 평가

## Originality

- 기존 framework 대비 처음으로 realistic object physics + room-scale scene + AI-generated asset/task + large-scale dataset을 통합
- LLM을 활용한 naturalistic task design - human-centered Internet content로부터 ecological statistics 추출
- Generative AI (text-to-3D, text-to-image, LLM)를 systematic하게 활용하여 simulator 확장 가능성 입증
- MimicGen을 적응시켜 kitchen manipulation task에 대한 automated trajectory generation pipeline 개발

## Limitation & Further Study

- 현재는 kitchen 환경에만 집중하여 home의 다른 공간(bedroom, bathroom, living room)으로의 확장 필요
- Real-world transfer는 제한된 kitchen 환경에서만 검증되었으며, 더 다양한 실제 환경에서의 평가 필요
- LLM 기반 task 생성이 실제 인간의 행동 다양성을 충분히 포괄하지 못할 가능성
- Text-to-3D로 생성된 asset의 물리 특성(mass, friction, shape accuracy) 검증 부재
- Cross-embodiment 지원이 있으나, 실제 여러 embodiment에서의 sim-to-real transfer 성능 비교 부족

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RoboCasa는 generative AI를 활용하여 robot learning을 위한 대규모 realistic simulation을 구축한 의미 있는 contribution이며, 실제 real-world transfer 성공을 보여줌으로써 sim-to-real robot learning의 실질적 경로를 제시한다. 다만 현재 kitchen 환경 집중과 제한된 real-world 검증은 향후 개선이 필요하다.

## Related Papers

- 🏛 기반 연구: [[papers/1794_AGILE_A_Comprehensive_Workflow_for_Humanoid_Loco-Manipulatio/review]] — AGILE의 표준화된 sim-to-real 워크플로우가 RoboCasa의 대규모 시뮬레이션 데이터를 실제 로봇으로 전이하는 필수 기반
- 🔗 후속 연구: [[papers/1951_Genie_Sim_30__A_High-Fidelity_Comprehensive_Simulation_Platf/review]] — Genie Sim 3.0의 고충실도 시뮬레이션이 RoboCasa의 kitchen 환경을 더 포괄적인 시뮬레이션 플랫폼으로 확장
- 🔄 다른 접근: [[papers/1252_ActiveUMI_Robotic_Manipulation_with_Active_Perception_from_R/review]] — 대규모 synthetic trajectory 생성과 VoxPoser의 zero-shot 자연언어 조작은 로봇 학습의 서로 다른 데이터 활용 전략
- 🔄 다른 접근: [[papers/1824_BiGym_A_Demo-Driven_Mobile_Bi-Manual_Manipulation_Benchmark/review]] — RoboCasa는 kitchen 중심 시뮬레이션을, BiGym은 이동형 양손 조작에 중점을 두어 범용 로봇 학습을 다르게 접근함
- 🔗 후속 연구: [[papers/2009_HumanoidGen_Data_Generation_for_Bimanual_Dexterous_Manipulat/review]] — HumanoidGen의 양손 정교 조작 데이터 생성이 RoboCasa의 kitchen task 중심 synthetic trajectory를 확장함
- 🔄 다른 접근: [[papers/1887_DreamGen_Unlocking_Generalization_in_Robot_Learning_through/review]] — 두 논문 모두 generalist robot 학습을 위한 대규모 데이터를 다루지만 RoboCasa는 시뮬레이션 trajectory에, DreamGen은 unlocking generalization에 집중한다
- 🔄 다른 접근: [[papers/1673_Sim-and-Real_Co-Training_A_Simple_Recipe_for_Vision-Based_Ro/review]] — 두 논문 모두 시뮬레이션과 실제 환경의 혼합 학습을 다루지만, 일반적인 co-training과 대규모 일상 작업이라는 다른 규모를 다룬다.
- 🔄 다른 접근: [[papers/1252_ActiveUMI_Robotic_Manipulation_with_Active_Perception_from_R/review]] — VoxPoser의 LLM+VLM 기반 자연언어 조작과 RoboCasa의 대규모 시뮬레이션 환경은 상호 보완적인 일반화 접근법
- 🔗 후속 연구: [[papers/1824_BiGym_A_Demo-Driven_Mobile_Bi-Manual_Manipulation_Benchmark/review]] — RoboCasa의 대규모 시뮬레이션 환경과 BiGym의 mobile bi-manual benchmark가 함께 포괄적인 manipulation 학습 환경을 구성한다.
- 🔗 후속 연구: [[papers/1794_AGILE_A_Comprehensive_Workflow_for_Humanoid_Loco-Manipulatio/review]] — RoboCasa의 대규모 시뮬레이션 데이터를 AGILE의 표준화된 워크플로우로 실제 로봇에 신뢰성 있게 전이
- 🧪 응용 사례: [[papers/1868_DexHub_and_DART_Towards_Internet_Scale_Robot_Data_Collection/review]] — RoboCasa의 large-scale simulation이 DexHub 데이터베이스와 연계되어 더 포괄적인 로봇 학습 환경을 조성한다.
- 🧪 응용 사례: [[papers/2021_Implicit_Kinodynamic_Motion_Retargeting_for_Human-to-humanoi/review]] — 대규모 로봇 시뮬레이션 환경에서 IKMR 프레임워크를 통한 인간-휴머노이드 모션 변환 기술을 검증할 수 있는 플랫폼을 제공한다.
- 🔄 다른 접근: [[papers/2082_LHM-Humanoid_Learning_a_Unified_Policy_for_Long-Horizon_Huma/review]] — 일반적인 조작을 위한 대규모 시뮬레이션과 장시간 휴머노이드 전신 조작이라는 다른 접근법을 제시한다.
- 🏛 기반 연구: [[papers/2089_ManiSkill-HAB_A_Benchmark_for_Low-Level_Manipulation_in_Home/review]] — 일반적인 조작을 위한 대규모 시뮬레이션의 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/2100_Mimicking-Bench_A_Benchmark_for_Generalizable_Humanoid-Scene/review]] — RoboCasa의 일상 작업 시뮬레이션 프레임워크를 실제 3D 장면과 인간 상호작용 데이터로 확장한 종합 벤치마크이다.
- 🔗 후속 연구: [[papers/2104_MolmoSpaces_A_Large-Scale_Open_Ecosystem_for_Robot_Navigatio/review]] — RoboCasa의 everyday tasks 시뮬레이션이 MolmoSpaces의 대규모 실내 환경 생태계로 크게 확장된 것이다
