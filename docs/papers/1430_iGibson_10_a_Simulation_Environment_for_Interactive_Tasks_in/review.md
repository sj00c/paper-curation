---
title: "1430_iGibson_10_a_Simulation_Environment_for_Interactive_Tasks_in"
authors:
  - "Bokui Shen"
  - "Fei Xia"
  - "Chengshu Li"
  - "Roberto Martín-Martín"
  - "Linxi Fan"
date: "2020.12"
doi: ""
arxiv: ""
score: 4.0
essence: "iGibson 1.0은 15개의 완전히 상호작용 가능한 현실적 실내 장면(108개 방)을 포함하는 로봇 시뮬레이션 환경으로, 대규모 장면에서 조작과 네비게이션을 포함한 대화형 작업을 학습할 수 있게 한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/GPU-Accelerated_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shen et al._2020_iGibson 1.0 a Simulation Environment for Interactive Tasks in Large Realistic Scenes.pdf"
---

# iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes

> **저자**: Bokui Shen, Fei Xia, Chengshu Li, Roberto Martín-Martín, Linxi Fan, Guanzhi Wang, Claudia Pérez-D'Arpino, Shyamal Buch, Sanjana Srivastava, Lyne P. Tchapmi, Micael E. Tchapmi, Kent Vainio, Josiah Wong, Li Fei-Fei, Silvio Savarese | **날짜**: 2020-12-05 | **URL**: [https://arxiv.org/abs/2012.02924](https://arxiv.org/abs/2012.02924)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Robot performs an interactive task in iGibson 1.0. It operates*

iGibson 1.0은 15개의 완전히 상호작용 가능한 현실적 실내 장면(108개 방)을 포함하는 로봇 시뮬레이션 환경으로, 대규모 장면에서 조작과 네비게이션을 포함한 대화형 작업을 학습할 수 있게 한다.

## Motivation

- **Known**: 기존 로봇 시뮬레이션 환경들(Gibson, Habitat, AI2Thor 등)은 순수 네비게이션 작업에만 집중하거나 단순화된 상호작용 모드를 제공하여, 현실적인 대규모 장면에서 완전한 물리 기반 상호작용을 지원하지 못한다.
- **Gap**: 실제 로봇이 수행해야 하는 복잡한 물리 기반 조작과 모바일 조작 작업을 대규모 현실적 가정용 환경에서 학습할 수 있는 통합적 시뮬레이션 플랫폼이 부재하다.
- **Why**: 현실적인 대규모 환경에서의 시뮬레이션은 로봇의 감각운동 정책(sensorimotor policy)을 robust하게 학습하고 실제 로봇으로의 전이(transfer)를 가능하게 하며, 효율적인 모방 학습(imitation learning)을 지원한다.
- **Approach**: 실제 세계의 3D 재구성을 기반으로 15개의 상호작용 가능한 장면을 생성하고, Physics-Based Rendering(PBR), 도메인 랜더마이제이션, 통합된 motion planner, 그리고 인간-로봇 인터페이스를 제공한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Fifteen interactive iGibson 1.0 scenes modelled after real-world reconstructions, preserving layout, distributio*

- **완전 상호작용 환경**: 15개의 실제 가정을 모델링한 장면에서 108개의 방과 570개의 객체를 포함하며, 모든 객체가 물리 엔진을 통해 완전히 상호작용 가능
- **고품질 센서 신호**: RGB, depth, segmentation, LiDAR, optical flow 등을 포함한 현실적인 가상 센서 신호 생성과 PBR을 통한 고충질 렌더링
- **도메인 랜더마이제이션**: 재료의 시각적 속성과 물리적 속성, 객체 형태를 변경하면서 상호작용성을 유지하는 메커니즘
- **개발 도구**: sampling-based motion planner와 인간-로봇 인터페이스를 통한 효율적인 demonstration 수집 및 imitation learning 지원
- **확장성**: CubiCasa5K와 3D-Front 레이아웃 지원으로 12,000개 이상의 추가 상호작용 가능 장면 제공
- **실증적 성과**: visual representation 학습이 downstream manipulation 작업 훈련을 가속화하고, navigation agent의 일반화 능력 향상 입증

## How

![Figure 4](figures/fig4.webp)

*Fig. 4: Robot interacting in iGibson 1.0 (large picture: 3rd person*

- 실제 세계 3D 스캔의 정적 메시를 동적 scene graph로 변환하여 articulated object model 통합
- 객체 모델에 재료 및 동역학 속성에 대한 주석 달기(metallic, roughness, normal maps)
- PyBullet 물리 엔진을 활용한 완전한 rigid body와 articulated body 시뮬레이션
- Physics-Based Rendering(PBR)을 통해 재료 정보를 기반으로 한 고품질 이미지 생성
- Domain randomization: 객체 배치의 분포를 보존하면서 재료 속성과 객체 형태 변경
- Sampling-based motion planner(RRT 기반)를 통한 충돌 없는 궤적 생성
- GUI 인터페이스를 통한 인간 사용자의 대화형 조작으로 demonstration 수집

## Originality

- Gibson 이전 버전의 정적 환경과 달리 완전한 물리 기반 상호작용을 지원하는 첫 대규모 현실적 홈 환경 시뮬레이터
- 실제 가정의 객체 배치 분포와 레이아웃을 보존하면서 완전한 articulated object 상호작용을 가능하게 한 점
- 도메인 랜더마이제이션, high-fidelity 센서 신호, motion planner, 인간 인터페이스를 통합한 통일된 플랫폼 제공
- Interactability를 고려한 시각 표현 학습이 downstream 작업 성능을 향상시킨다는 실증적 증명

## Limitation & Further Study

- 15개의 기본 제공 장면이 제한적이며, 확장을 위해 외부 데이터셋(CubiCasa5K, 3D-Front)에 의존
- 실제 센서의 노이즈, 지연, 하드웨어 한계 등을 완전히 시뮬레이션하지 못할 가능성
- 학습한 정책의 실제 로봇으로의 성공적인 전이(sim-to-real transfer)에 대한 실증 결과가 제한적
- 인간 demonstration 수집의 편의성에도 불구하고 대규모 demonstration 데이터셋 구축의 scalability 미흡
- **후속 연구**: (1) 더 다양한 환경과 작업 도메인 추가, (2) sim-to-real transfer의 체계적 평가, (3) 더 복잡한 다중 에이전트 상호작용 시나리오 지원

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: iGibson 1.0은 대규모 현실적 환경에서 완전한 물리 기반 상호작용을 지원하는 획기적인 로봇 시뮬레이션 플랫폼으로, 조작, 모바일 조작, 네비게이션 등 다양한 embodied AI 작업 연구를 가능하게 한다. 풍부한 도구 지원과 오픈소스 공개를 통해 로봇공학 커뮤니티에 큰 영향을 미칠 것으로 기대된다.

## Related Papers

- 🔄 다른 접근: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — 둘 다 대규모 로봇 시뮬레이션 환경이지만 interactive task focus vs GPU parallelized manipulation이라는 다른 특화 방향을 가진다.
- 🏛 기반 연구: [[papers/1317_BEHAVIOR-1K_A_Human-Centered_Embodied_AI_Benchmark_with_1000/review]] — BEHAVIOR-1K의 human-centered embodied task 개념을 15개 대규모 실내 장면으로 확장한 구현체이다.
- 🔗 후속 연구: [[papers/1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit/review]] — Habitat 2.0의 interactive rearrangement 개념을 108개 방을 포함한 더 대규모 환경으로 발전시켰다.
- 🏛 기반 연구: [[papers/1544_robosuite_A_Modular_Simulation_Framework_and_Benchmark_for_R/review]] — robosuite의 모듈화된 시뮬레이션 프레임워크가 iGibson의 대규모 상호작용 환경 구축 기반이 됨
- 🔄 다른 접근: [[papers/1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit/review]] — iGibson과 Habitat 2.0 모두 실내 로봇 시뮬레이션을 제공하지만 상호작용 vs 재배치 작업에 특화된 차이가 있음
- 🔄 다른 접근: [[papers/1290_3D_Gaussian_Splatting_for_Real-Time_Radiance_Field_Rendering/review]] — 실시간 고품질 시각화에서 Gaussian Splatting과 iGibson의 물리 시뮬레이션이 다른 접근법을 제공합니다.
- 🔄 다른 접근: [[papers/1317_BEHAVIOR-1K_A_Human-Centered_Embodied_AI_Benchmark_with_1000/review]] — 상호작용 작업을 위한 iGibson 1.0과 일상 활동 중심의 BEHAVIOR-1K가 다른 벤치마크 접근법을 제시합니다.
- 🔄 다른 접근: [[papers/1417_GRUtopia_Dream_General_Robots_in_a_City_at_Scale/review]] — iGibson의 상호작용 중심 시뮬레이션과 다르게 대규모 도시 스케일에서 embodied AI scaling law 탐구에 특화된다.
