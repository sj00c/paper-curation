---
title: "1417_GRUtopia_Dream_General_Robots_in_a_City_at_Scale"
authors:
  - "Hanqing Wang"
  - "Jiahe Chen"
  - "Wensi Huang"
  - "Qingwei Ben"
  - "Tai Wang"
date: "2024.07"
doi: ""
arxiv: ""
score: 4.0
essence: "GRUtopia는 로봇 학습을 위한 최초의 대규모 시뮬레이션 3D 도시 환경으로, 100k개의 상호작용 가능한 장면, LLM 기반 NPC 시스템, 그리고 종합적인 벤치마크를 제공하여 embodied AI의 scaling law 탐구를 가능하게 한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Robotic_Interaction_Datasets"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2024_GRUtopia Dream General Robots in a City at Scale.pdf"
---

# GRUtopia: Dream General Robots in a City at Scale

> **저자**: Hanqing Wang, Jiahe Chen, Wensi Huang, Qingwei Ben, Tai Wang, Boyu Mi, Tao Huang, Siheng Zhao, Yilun Chen, Sizhe Yang, Peizhou Cao, Wenye Yu, Zichao Ye, Jialun Li, Junfeng Long, Zirui Wang, Huiling Wang, Ying Zhao, Zhongying Tu, Yu Qiao, Dahua Lin, Jiangmiao Pang | **날짜**: 2024-07-15 | **URL**: [https://arxiv.org/abs/2407.10943](https://arxiv.org/abs/2407.10943)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Key features of GRUtopia.*

GRUtopia는 로봇 학습을 위한 최초의 대규모 시뮬레이션 3D 도시 환경으로, 100k개의 상호작용 가능한 장면, LLM 기반 NPC 시스템, 그리고 종합적인 벤치마크를 제공하여 embodied AI의 scaling law 탐구를 가능하게 한다.

## Motivation

- **Known**: 최근 embodied AI에서 scaling law가 주목받고 있으며, 실제 로봇 데이터 수집의 높은 비용으로 인해 Sim2Real 패러다임이 중요하다. 기존 시뮬레이션 플랫폼들(Habitat, AI2-THOR 등)은 주로 가정 환경에 집중하고 장면 다양성이 제한적이다.
- **Gap**: 기존 플랫폼들은 장면 다양성과 복잡성 측면에서 제한적이며, 서비스 지향적 환경(병원, 슈퍼마켓 등)에서의 로봇 배치를 대비하기 위한 고품질 대규모 데이터셋과 사회적 상호작용 시뮬레이션이 부재하다.
- **Why**: 일반 로봇이 실제로 배치될 서비스 환경에서의 다양한 작업을 학습하려면 고품질의 대규모 시뮬레이션 데이터와 인간과의 상호작용 시나리오가 필수적이며, 이는 Sim2Real 갭을 줄이고 로봇 학습의 확장성을 높인다.
- **Approach**: GRScenes 데이터셋(89개 카테고리, 100k 장면), GRResidents LLM 기반 NPC 시스템, GRBench 벤치마크를 개발하여 다양한 로봇 플랫폼(특히 legged robot)을 지원하고 Object Loco-Navigation, Social Loco-Navigation, Loco-Manipulation 작업을 포함한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: The richness and diversity of scenes and objects in GRScenes. (a) The distribution of*

- **GRScenes 데이터셋**: 89개 다양한 기능 카테고리, 100k개의 상호작용 가능하고 세밀하게 주석 처리된 장면으로 city-scale 환경 구성 가능
- **GRResidents NPC 시스템**: LLM 기반으로 사회적 상호작용, 작업 생성, 작업 할당을 수행하며 환경 지식과 실시간 장면 인식 활용
- **GRBench 벤치마크**: Object Loco-Navigation, Social Loco-Navigation, Loco-Manipulation의 세 가지 점진적 난이도 작업 제공
- **기존 플랫폼 대비 우수성**: 기존의 8개 장면 타입(Behavior-1K)과 비교해 89개 타입, 가정 환경 중심에서 서비스 환경으로 확대
- **학습 기반 제어 정책 API 제공**: 보행 및 집기-놓기 조작 등 저수준 정책을 API로 제공하여 Sim2Real 갭 축소

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Overview of GRResidents (Sec. 3.2). It comprises two modules: (a) A world knowledge*

- 100k 규모의 상호작용 가능한 장면을 89개 기능 카테고리로 분류하고 부품 수준 모델링, 재질 라벨, 언어 캡션 등 다층 주석 제공
- Isaac Sim을 기반으로 지속적이고 상호작용 가능한 물리 시뮬레이션 구현
- LLM 에이전트 프레임워크와 계층적 장면 인식 모듈을 통합하여 NPC가 객체 속성, 공간 관계, 장면 의미를 이해하고 동적 대화 수행
- NPC를 통해 무한한 수의 장면 인식 작업 자동 생성
- 학습된 저수준 정책(보행, 조작)을 API로 제공하여 고수준 계획에 집중 가능
- LLM 및 VLM 기반 베이스라인 에이전트 개발 및 평가를 통해 벤치마크 검증

## Originality

- Embodied AI를 위한 최초의 city-scale 3D 도시 사회 시뮬레이션 플랫폼 구축
- LLM 기반 NPC 시스템을 단순 작업 할당을 넘어 동적 대화, 실시간 장면 인식, 작업 생성까지 확장
- 기존 가정 환경 중심에서 벗어나 89개 카테고리의 서비스 지향 환경으로 확대하는 혁신적 접근
- 저수준 제어 정책을 API로 제공하여 현실적인 물리 설정에서도 고수준 작업 계획 연구 가능하게 함

## Limitation & Further Study

- 라이선스 문제로 인해 초기 공개 시 100개 장면만 7가지 건물 타입으로 제한되며, 나머지 데이터의 단계적 공개 필요
- Legged robot을 주요 에이전트로 하며 다른 로봇 플랫폼 지원이 제한적
- 현재 버전의 GRBench는 고수준 작업에 초점을 맞추고 있어 저수준 제어 정책 학습 연구에는 직접적 활용 제한
- NPC의 대화 질감, 작업 생성의 현실성에 대한 정량적 평가 결과 부족
- 후속 연구: 데이터셋의 완전한 공개, 더 많은 로봇 플랫폼 지원, 저수준 제어와 고수준 계획의 통합 학습 방법론 개발, NPC 지능의 추가 향상

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: GRUtopia는 embodied AI 연구를 위한 혁신적인 대규모 시뮬레이션 플랫폼으로, 다양한 서비스 환경, 인간과의 사회적 상호작용, 그리고 체계적인 벤치마크를 통해 로봇 학습의 확장성 문제를 해결하는 중요한 기여이다.

## Related Papers

- 🏛 기반 연구: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — GRUtopia의 대규모 시뮬레이션 환경이 ManiSkill3의 GPU 병렬화 기술 기반 위에 구축되어 로봇 학습 데이터 생성을 가능하게 한다.
- 🧪 응용 사례: [[papers/1493_Neural_Scaling_Laws_in_Robotics/review]] — GRUtopia가 제공하는 100k 규모의 상호작용 장면이 로봇공학에서 신경망 스케일링 법칙을 검증하는 실험 환경으로 활용된다.
- 🔄 다른 접근: [[papers/1408_GenSim_Generating_Robotic_Simulation_Tasks_via_Large_Languag/review]] — 둘 다 로봇 학습을 위한 대규모 시뮬레이션 환경 생성에 초점을 맞추지만, GRUtopia는 도시 환경을, GenSim은 LLM 기반 작업 생성에 중점을 둔다.
- 🔄 다른 접근: [[papers/1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit/review]] — Habitat 2.0의 가정 환경과 다르게 대규모 도시 환경에서 로봇 학습을 위한 시뮬레이션 플랫폼을 제공한다.
- 🔗 후속 연구: [[papers/1477_MineDojo_Building_Open-Ended_Embodied_Agents_with_Internet-S/review]] — MineDojo의 인터넷 규모 데이터 개념을 3D 도시 환경으로 확장하여 더 현실적인 로봇 학습 환경을 구축한다.
- 🔄 다른 접근: [[papers/1430_iGibson_10_a_Simulation_Environment_for_Interactive_Tasks_in/review]] — iGibson의 상호작용 중심 시뮬레이션과 다르게 대규모 도시 스케일에서 embodied AI scaling law 탐구에 특화된다.
- 🧪 응용 사례: [[papers/1563_Scaling_Instructable_Agents_Across_Many_Simulated_Worlds/review]] — Scaling Instructable Agents는 GRUtopia의 대규모 시뮬레이션 환경에서 확장 법칙을 탐구하는 실제 적용 사례임
- 🧪 응용 사례: [[papers/1377_Embodied_intelligent_industrial_robotics_Framework_and_techn/review]] — embodied intelligence 프레임워크를 대규모 도시 환경의 범용 로봇 시스템에 실제 적용한 구현 사례
