---
title: "1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit"
authors:
  - "Andrew Szot"
  - "Alex Clegg"
  - "Eric Undersander"
  - "Erik Wijmans"
  - "Yili Zhao"
date: "2021.06"
doi: ""
arxiv: ""
score: 4.0
essence: "Habitat 2.0는 가정용 로봇의 물체 재배치 작업을 학습하기 위한 고성능 물리 시뮬레이션 플랫폼이며, ReplicaCAD 데이터셋, 최적화된 시뮬레이터, Home Assistant Benchmark를 제공한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/GPU-Accelerated_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Szot et al._2021_Habitat 2.0 Training Home Assistants to Rearrange their Habitat.pdf"
---

# Habitat 2.0: Training Home Assistants to Rearrange their Habitat

> **저자**: Andrew Szot, Alex Clegg, Eric Undersander, Erik Wijmans, Yili Zhao, John Turner, Noah Maestre, Mustafa Mukadam, Devendra Chaplot, Oleksandr Maksymets, Aaron Gokaslan, Vladimir Vondrus, Sameer Dharur, Franziska Meier, Wojciech Galuba, Angel Chang, Zsolt Kira, Vladlen Koltun, Jitendra Malik, Manolis Savva, Dhruv Batra | **날짜**: 2021-06-28 | **URL**: [https://arxiv.org/abs/2106.14405](https://arxiv.org/abs/2106.14405)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: A mobile manipulator (Fetch robot) simulated in Habitat 2.0 performing rearrangement tasks in a*

Habitat 2.0는 가정용 로봇의 물체 재배치 작업을 학습하기 위한 고성능 물리 시뮬레이션 플랫폼이며, ReplicaCAD 데이터셋, 최적화된 시뮬레이터, Home Assistant Benchmark를 제공한다.

## Motivation

- **Known**: 기존 시뮬레이터들은 로봇 학습을 위해 존재하지만, 물리 시뮬레이션이 느리고 대규모 인터랙티브 환경에서의 복잡한 조작 작업을 충분히 지원하지 못한다.
- **Gap**: 높은 성능의 물리 시뮬레이터, 현실적인 가정 환경 데이터, 그리고 이동 조작 로봇의 능력을 체계적으로 평가할 수 있는 벤치마크 태스크가 부족하다.
- **Why**: 가정용 로봇의 자율 작업 수행 능력 개발은 과학적·사회적 가치가 높으며, 현실의 느린 하드웨어 실험 대신 시뮬레이션에서 효율적으로 학습할 수 있는 인프라가 필수적이다.
- **Approach**: 물리 시뮬레이션 성능 최적화, 전문가 제작 3D 자산 데이터셋 구축, 그리고 일반화 능력을 테스트하는 구조화된 태스크 세트를 개발했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: A mobile manipulator (Fetch robot) simulated in Habitat 2.0 performing rearrangement tasks in a*

- **ReplicaCAD**: 111개의 고유한 아파트 레이아웃과 92개의 저작 객체(열고 닫을 수 있는 캐비닛, 서랍 등)를 포함한 900+ 시간의 전문 아티스트 작업으로 완성한 대화형 3D 데이터셋
- **고성능 시뮬레이터**: 단일 GPU에서 8,200 SPS(273× real-time), 8-GPU 노드에서 26,000 SPS(850× real-time)를 달성하여 기존 대비 100배 성능 향상
- **Home Assistant Benchmark**: TidyHouse, PrepareGroceries, SetTable 등 현실적인 가정 조작 작업으로 구성된 벤치마크
- **비교 분석**: 계층적 강화학습이 단순 RL보다 우수하지만 hand-off 문제를 겪으며, Sense-Plan-Act 파이프라인은 더 취약함을 증명

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Interleaved physics and rendering. Top shows*

- Bullet 물리 엔진과 Magnum 렌더링 라이브러리를 사용하여 고성능 아키텍처 설계
- Piecewise-rigid 객체와 관절형(articulated) 로봇을 지원하는 시뮬레이션 엔진 개발
- GeometricGoal 사양을 사용하여 초기 위치에서 목표 위치로의 물체 이동을 정의한 태스크 설계
- RGB-D 카메라, 관절 센서, 자기 감지 센서만 사용하도록 제약하여 현실성 증대
- Reinforcement Learning(계층적 정책)과 Sense-Plan-Act 파이프라인을 체계적으로 비교
- 새로운 객체, 용기, 아파트 레이아웃에 대한 일반화 능력을 중심으로 평가

## Originality

- 기존 Habitat 1.0의 네비게이션 기능을 물리 기반 이동 조작으로 확장하며, 물리 시뮬레이션 성능을 전례 없는 수준까지 최적화
- 현실의 가정 환경과 매칭되는 artist-authored 3D 데이터셋을 고품질로 구축하여 시뮬-투-리얼 갭 감소
- RL 정책과 고전적 SPA 파이프라인의 장단점을 구조화된 태스크에서 최초로 대규모 비교 분석
- Hand-off problem 등 계층적 정책의 구체적 문제를 명시적으로 식별 및 분석

## Limitation & Further Study

- Non-rigid dynamics(변형 물체, 유체, 천 등)와 물리 상태 변환(자르기, 드릴링 등)은 지원하지 않아 일부 현실적 작업 표현 제한
- 추상화된 그래스핑(abstract grasping)을 사용하므로 세밀한 손가락 제어나 현실의 복잡한 파지 문제는 미반영
- 계층적 정책에서 STRIPS 완벽 태스크 플래너 가정으로 인해 현실 적용 시 계획 부정확성에 대한 연구 필요
- 새로운 객체 유형이나 완전히 다른 주거 공간으로의 일반화 한계 평가 필요
- 시뮬-투-리얼 전이 성능에 대한 실제 로봇 검증 부족

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Habitat 2.0은 embodied AI 연구를 위한 완전한 인프라(데이터, 시뮬레이터, 벤치마크)를 제공하며, 100배 성능 향상으로 대규모 실험을 가능하게 하고, RL vs SPA 비교를 통해 이동 조작 문제에 대한 실질적 통찰을 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1544_robosuite_A_Modular_Simulation_Framework_and_Benchmark_for_R/review]] — robosuite의 기본적인 로봇 시뮬레이션 프레임워크를 가정용 로봇의 물체 재배치 작업에 특화하여 발전시킨다.
- 🔗 후속 연구: [[papers/1279_BEHAVIOR_Robot_Suite_Streamlining_Real-World_Whole-Body_Mani/review]] — BEHAVIOR Robot Suite의 whole-body manipulation 개념을 가정 환경의 재배치 작업으로 구체화하여 적용한다.
- 🔄 다른 접근: [[papers/1508_Openfly_A_comprehensive_platform_for_aerial_vision-language/review]] — Openfly의 aerial 환경과 다르게 가정 내 지상 로봇의 물체 조작에 특화된 시뮬레이션 플랫폼을 제공한다.
- 🔗 후속 연구: [[papers/1317_BEHAVIOR-1K_A_Human-Centered_Embodied_AI_Benchmark_with_1000/review]] — BEHAVIOR-1K는 Habitat 2.0의 가정용 로봇 학습 환경을 1000개 작업으로 대폭 확장한 벤치마크임
- 🔄 다른 접근: [[papers/1430_iGibson_10_a_Simulation_Environment_for_Interactive_Tasks_in/review]] — iGibson과 Habitat 2.0 모두 실내 로봇 시뮬레이션을 제공하지만 상호작용 vs 재배치 작업에 특화된 차이가 있음
- 🏛 기반 연구: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — ManiSkill3의 GPU 병렬화 기술이 Habitat 2.0의 대규모 물리 시뮬레이션 성능 향상에 기여함
- 🏛 기반 연구: [[papers/1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit/review]] — 물리 시뮬레이션 환경에서 가정용 로봇 작업 학습의 기초 플랫폼입니다.
- 🔗 후속 연구: [[papers/1430_iGibson_10_a_Simulation_Environment_for_Interactive_Tasks_in/review]] — Habitat 2.0의 interactive rearrangement 개념을 108개 방을 포함한 더 대규모 환경으로 발전시켰다.
- 🏛 기반 연구: [[papers/1469_ManiSkill3_GPU_Parallelized_Robotics_Simulation_and_Renderin/review]] — ManiSkill3의 접촉이 풍부한 물리 엔진이 Habitat 2.0의 환경 상호작용 시뮬레이션 기술을 기반으로 발전된다.
- 🏛 기반 연구: [[papers/1531_RLBench_The_Robot_Learning_Benchmark__Learning_Environment/review]] — Habitat 2.0의 시뮬레이션 환경 기술이 RLBench의 로봇 학습 벤치마크 구현에 환경적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1544_robosuite_A_Modular_Simulation_Framework_and_Benchmark_for_R/review]] — 두 프레임워크 모두 로봇 학습 환경을 제공하지만 조작과 네비게이션의 다른 초점을 가진다.
- 🧪 응용 사례: [[papers/1586_TidyBot_Personalized_Robot_Assistance_with_Large_Language_Mo/review]] — Habitat 2.0의 가정용 로봇 환경은 TidyBot의 개인화된 정리 작업을 시뮬레이션에서 훈련할 수 있는 플랫폼을 제공한다.
- 🔄 다른 접근: [[papers/1317_BEHAVIOR-1K_A_Human-Centered_Embodied_AI_Benchmark_with_1000/review]] — BEHAVIOR-1K와 Habitat 2.0은 모두 가정 환경 기반 embodied AI 시뮬레이션이지만 작업 범위와 복잡도가 다르다.
- 🏛 기반 연구: [[papers/1304_ALFRED_A_Benchmark_for_Interpreting_Grounded_Instructions_fo/review]] — Habitat 2.0의 home assistant training 환경을 egocentric vision과 자연어 지시사항 매핑 학습을 위한 구체적인 벤치마크로 발전시킨 연구입니다.
- 🔄 다른 접근: [[papers/1417_GRUtopia_Dream_General_Robots_in_a_City_at_Scale/review]] — Habitat 2.0의 가정 환경과 다르게 대규모 도시 환경에서 로봇 학습을 위한 시뮬레이션 플랫폼을 제공한다.
