---
title: "1544_robosuite_A_Modular_Simulation_Framework_and_Benchmark_for_R"
authors:
  - "Yuke Zhu"
  - "Josiah Wong"
  - "Ajay Mandlekar"
  - "Roberto Martín-Martín"
  - "Abhishek Joshi"
date: "2020.09"
doi: ""
arxiv: ""
score: 4.0
essence: "robosuite는 MuJoCo 물리 엔진을 기반으로 하는 모듈식 로봇 시뮬레이션 프레임워크로, 로봇 학습 연구를 위한 벤치마크 환경과 재현 가능한 실험 환경을 제공한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Robot_Policy_Learning"
  - "sub/GPU-Accelerated_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhu et al._2020_robosuite A Modular Simulation Framework and Benchmark for Robot Learning.pdf"
---

# robosuite: A Modular Simulation Framework and Benchmark for Robot Learning

> **저자**: Yuke Zhu, Josiah Wong, Ajay Mandlekar, Roberto Martín-Martín, Abhishek Joshi, Kevin Lin, Abhiram Maddukuri, Soroush Nasiriany, Yifeng Zhu | **날짜**: 2020-09-25 | **URL**: [https://arxiv.org/abs/2009.12293](https://arxiv.org/abs/2009.12293)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: System diagram of robosuite modules. An actor (e.g. a Policy or*

robosuite는 MuJoCo 물리 엔진을 기반으로 하는 모듈식 로봇 시뮬레이션 프레임워크로, 로봇 학습 연구를 위한 벤치마크 환경과 재현 가능한 실험 환경을 제공한다.

## Motivation

- **Known**: 시뮬레이션 기반 로봇 학습은 데이터 기반 알고리즘(reinforcement learning, imitation learning)의 발전으로 다양한 로봇 제어 문제에서 성공을 거두었으나, 재현성 부족과 로봇 하드웨어 접근성 제한이 연구 진전을 방해하고 있다.
- **Gap**: 기존 시뮬레이션 플랫폼들은 유연한 환경 구성과 표준화된 벤치마크 작업이 부족하며, 높은 수준의 컨트롤러 구현과 데이터 수집 유틸리티가 체계적으로 지원되지 않는다.
- **Why**: 표준화된 벤치마크와 모듈식 설계는 로봇 학습 알고리즘의 재현 가능한 평가를 가능하게 하며, 낮은 진입 장벽으로 AI와 로보틱스 교차 분야의 연구를 촉진한다.
- **Approach**: MuJoCo 물리 엔진을 핵심으로 하여 Modeling API와 Simulation API로 구분된 모듈식 아키텍처를 설계하고, Task, Robot, Arena, Object 클래스의 조합으로 절차적 환경 생성을 지원한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Procedurally generated robotic environments with robosuite APIs*

- **모듈식 설계**: 10개의 로봇 모델, 9개의 그리퍼 모델, 4개의 베이스 모델, 6개의 바디 파트 컨트롤러 모드로 구성되어 유연한 환경 구성을 지원
- **표준화된 작업**: 9개의 표준 조작 작업과 다양한 복잡도를 제공하며 최신 알고리즘의 벤치마킹 결과 포함
- **고급 컨트롤러**: joint space, Cartesian space, 역기구학(inverse kinematics), 조작 공간 제어(operational space control) 등 다양한 컨트롤 모드 제공
- **멀티모달 센싱**: RGB 카메라, depth map, segmentation mask, proprioception 등 다양한 센서 신호 지원
- **휴먼 데모 수집**: 키보드, 3D 마우스, GUI 등으로 휴먼 데모 수집 및 재현 기능 제공

## How

![Figure 2](figures/fig2.webp)

*Figure 2: System diagram of robosuite modules. An actor (e.g. a Policy or*

- Modeling API: Task, RobotModel, GripperModel, RobotBaseModel, Object Model, Arena을 조합하여 MJCF 형식의 시뮬레이션 모델 생성
- Simulation API: OpenAI Gym 스타일의 인터페이스로 정책(Policy) 또는 I/O 디바이스에서 액션 입력을 받아 MuJoCo 물리 엔진으로 실행
- Controller 계층: 액션 공간(joint velocity, Cartesian position 등)을 MuJoCo의 토크 커맨드로 변환하는 복합 컨트롤러(composite controller) 구현
- Sensor 계층: MjSim 객체에서 정보를 추출하여 관찰값, 보상, 메타데이터 생성
- Procedural generation: Placement initializer를 통해 매 에피소드마다 유효한 비충돌 객체 배치 샘플링

## Originality

- MuJoCo 기반 빠른 접촉 역학(contact dynamics) 시뮬레이션을 로봇 학습에 특화된 모듈식 구조로 추상화
- 절차적 환경 생성(procedural generation) API를 통해 프로그래매틱하게 새로운 작업과 환경 구성 가능
- 다양한 컨트롤 모드(joint space, Cartesian space, operational space 등)를 composite controller로 통합한 설계
- 휴먼 시연 수집, 재현, 활용을 위한 통합 유틸리티 제공

## Limitation & Further Study

- 시뮬레이션과 실제 로봇 사이의 sim-to-real transfer 성능에 대한 평가 부재
- 물리 시뮬레이션의 정확도 한계(특히 접촉 모델링, 마찰 등)로 인한 현실성 제약
- 대규모 병렬 처리 성능과 확장성에 대한 구체적 분석 부족
- 후속 연구: sim-to-real 갭 감소를 위한 도메인 랜더마이제이션 통합, 더 정교한 물리 모델 추가, 다중 에이전트 환경 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: robosuite는 로봇 학습 커뮤니티를 위한 포괄적이고 잘 설계된 오픈소스 프레임워크로, 모듈식 아키텍처와 표준화된 벤치마크를 통해 재현 가능한 연구를 촉진하며 AI-로보틱스 교차 분야의 진입 장벽을 현저히 낮춘다.

## Related Papers

- 🔄 다른 접근: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — robosuite와 ManiSkill3 모두 로봇 학습을 위한 시뮬레이션 프레임워크이지만 GPU 병렬화의 차이가 있다.
- 🔗 후속 연구: [[papers/1483_MuBlE_MuJoCo_and_Blender_simulation_Environment_and_Benchmar/review]] — robosuite의 기본 시뮬레이션 개념을 MuBlE가 Blender와 결합하여 확장한다.
- 🔄 다른 접근: [[papers/1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit/review]] — 두 프레임워크 모두 로봇 학습 환경을 제공하지만 조작과 네비게이션의 다른 초점을 가진다.
- 🔗 후속 연구: [[papers/1531_RLBench_The_Robot_Learning_Benchmark__Learning_Environment/review]] — robosuite의 모듈식 프레임워크는 RLBench와 같은 더 복잡한 벤치마크 환경 구축의 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit/review]] — robosuite의 기본적인 로봇 시뮬레이션 프레임워크를 가정용 로봇의 물체 재배치 작업에 특화하여 발전시킨다.
- 🏛 기반 연구: [[papers/1430_iGibson_10_a_Simulation_Environment_for_Interactive_Tasks_in/review]] — robosuite의 모듈화된 시뮬레이션 프레임워크가 iGibson의 대규모 상호작용 환경 구축 기반이 됨
- 🔗 후속 연구: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — ManiSkill3의 GPU 병렬화가 robosuite의 모듈형 시뮬레이션 프레임워크를 대규모 병렬 처리로 발전시켜 학습 속도를 획기적으로 향상시킨다.
- 🏛 기반 연구: [[papers/1483_MuBlE_MuJoCo_and_Blender_simulation_Environment_and_Benchmar/review]] — MuBlE는 robosuite의 MuJoCo 기반을 확장하여 Blender 렌더링을 추가한 발전된 시뮬레이션 환경입니다.
- 🏛 기반 연구: [[papers/1530_Revised_identification_of_strain_gradient_elastic_parameters/review]] — robosuite의 물리 시뮬레이션 프레임워크에서 strain gradient 매개변수 식별이 중요한 요소이다.
- 🏛 기반 연구: [[papers/1531_RLBench_The_Robot_Learning_Benchmark__Learning_Environment/review]] — RLBench는 robosuite와 함께 로봇 학습 벤치마크의 표준을 제시하며 더 복잡한 태스크를 다룹니다.
- 🏛 기반 연구: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — robosuite 시뮬레이션 프레임워크가 VLABench의 대규모 로봇 조작 벤치마크 구축의 기술적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1299_A_Survey_of_Robotic_Navigation_and_Manipulation_with_Physics/review]] — 로봇 조작을 위한 모듈러 시뮬레이션 프레임워크로서 물리 시뮬레이터 연구의 기반이 됩니다.
