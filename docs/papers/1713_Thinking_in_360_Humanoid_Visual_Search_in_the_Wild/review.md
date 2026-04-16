---
title: "1713_Thinking_in_360_Humanoid_Visual_Search_in_the_Wild"
authors:
  - "Heyang Yu"
  - "Yinan Han"
  - "Xiangyu Zhang"
  - "Baiqiao Yin"
  - "Bowen Chang"
date: "2025.11"
doi: ""
arxiv: ""
score: 4.0
essence: "인간처럼 360° 파노라마 환경에서 머리 회전을 통해 능동적으로 물체를 탐색하거나 경로를 찾는 embodied 시각 탐색 에이전트를 제안하고, 실내 장면을 넘어 지하철역·쇼핑몰·거리 등 복잡한 현실 환경을 대상으로 한 H*Bench 벤치마크를 구축했다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/LiDAR_Terrain_Perception"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yu et al._2025_Thinking in 360° Humanoid Visual Search in the Wild.pdf"
---

# Thinking in 360°: Humanoid Visual Search in the Wild

> **저자**: Heyang Yu, Yinan Han, Xiangyu Zhang, Baiqiao Yin, Bowen Chang, Xiangyu Han, Xinhao Liu, Jing Zhang, Marco Pavone, Chen Feng, Saining Xie, Yiming Li | **날짜**: 2025-11-25 | **URL**: [https://arxiv.org/abs/2511.20351](https://arxiv.org/abs/2511.20351)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. We pose a fundamental question: can an AI agent actively search for objects or paths in a 3D world like a huma*

인간처럼 360° 파노라마 환경에서 머리 회전을 통해 능동적으로 물체를 탐색하거나 경로를 찾는 embodied 시각 탐색 에이전트를 제안하고, 실내 장면을 넘어 지하철역·쇼핑몰·거리 등 복잡한 현실 환경을 대상으로 한 H*Bench 벤치마크를 구축했다.

## Motivation

- **Known**: 최근 MLLM 기반의 시각 탐색 방법들이 정적 2D 이미지 내 물체 탐색에서 우수한 성능을 보이고 있으며, RL 기반 post-training이 모델의 추론 능력을 향상시킬 수 있다는 것이 알려져 있다.
- **Gap**: 기존 시각 탐색 연구는 정적 이미지에 제한되어 있고 물리적 embodiment과 3D 세계와의 상호작용을 고려하지 않으며, 현실의 하드웨어 제약을 우회하면서도 인간 수준의 능동적 공간 추론을 수행할 수 있는 스케일러블한 방법이 부족하다.
- **Why**: humanoid robots, assistive technology, AR 등 현실 응용에서 복잡한 환경에서 능동적으로 정보를 탐색할 수 있는 에이전트의 필요성이 높으며, 이는 조작과 네비게이션 같은 embodied task의 선행 조건이다.
- **Approach**: 360° 파노라마를 경량 시뮬레이터로 활용하여 머리 회전에 따른 폐쇄 루프 perception-action 사이클을 구현하고, humanoid object search (HOS)와 humanoid path search (HPS) 두 가지 embodied task를 정의한 뒤, SFT와 RL을 통해 Qwen2.5-VL을 post-training했다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4. Comparison of In-task (train and test on the same task family) and Cross-task (train on one task family and te*

- **H*Bench 벤치마크 구축**: 지하철역, 쇼핑몰, 거리, 공공기관 등 시각적으로 복잡한 in-the-wild 장면을 포함하는 최초의 humanoid visual search 벤치마크 제시
- **성능 향상**: Post-training을 통해 Qwen2.5-VL의 object search 성공률을 14.83%에서 47.38%로, path search를 6.44%에서 24.94%로 3배 이상 향상
- **성능 한계 규명**: 최신 proprietary 모델도 약 30% 수준의 성공률을 보여 현 MLLM의 공간 추론 능력의 한계를 정량화
- **Scalable 프레임워크**: 실제 3D 시뮬레이터나 로봇 하드웨어 없이 360° 파노라마만으로 embodied reasoning을 연구할 수 있는 확장 가능한 플랫폼 제안

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Pipeline Illustration. Stage 1 (SFT) provides the foundational ability to map perspective images to plausible *

- 360° 파노라마 이미지에서 현재 head orientation에 해당하는 좁은 시야각 뷰를 추출하여 MLLM의 입력으로 제공
- HOS task: 목표 물체의 위치를 파악하고 최적의 head orientation을 예측하도록 학습
- HPS task: 목적지로 향하는 네비게이션 가능 경로를 식별하고 ground plane 상의 방향 벡터 생성
- Supervised fine-tuning (SFT)으로 기본 능력을 학습한 후, reinforcement learning (RL)을 적용하여 embodied planning 능력 강화
- In-task 및 Cross-task generalization 평가를 통해 모델의 범용성 및 공간 추론 능력 검증

## Originality

- **Humanoid visual search 개념**: 기존의 정적 2D 이미지 탐색에서 벗어나 능동적 head rotation을 통한 360° embodied 시각 탐색으로 확장한 첫 시도
- **Hardware-free embodied reasoning**: 실제 로봇이나 3D 시뮬레이터 없이 360° 파노라마를 활용한 경량 플랫폼 제안
- **In-the-wild 벤치마크**: 기존 가구 장면 중심 벤치마크를 벗어나 지하철역, 쇼핑몰, 거리 등 구조적·의미적·체적 복잡성이 높은 현실 환경에 초점
- **Dual embodied task**: HOS와 HPS 두 가지 핵심 embodied task를 체계적으로 정의하고 평가

## Limitation & Further Study

- **Path search의 낮은 성능**: HPS의 최고 성공률이 약 25%에 불과하여 복잡한 공간 상식(spatial commonsense) 요구 능력의 한계 노출
- **단일 파노라마 제약**: 360° 파노라마만으로는 표현 가능한 embodied task의 범위가 제한적이며, 장거리 네비게이션이나 멀티 홉 탐색은 다루지 못함
- **MLLM 기반 접근의 근본적 한계**: 모델이 vision-action을 정확하게 매칭하지 못하거나 부적절한 경로 방향을 제시하는 failure case가 존재
- **후속 연구 방향**: (1) 공간 추론 능력을 강화하기 위한 새로운 post-training 기법, (2) multi-step reasoning을 지원하는 에이전트 아키텍처, (3) 실제 로봇 플랫폼으로의 transfer learning 연구가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: humanoid visual search라는 새로운 embodied AI 문제를 정의하고 현실적이고 도전적인 H*Bench 벤치마크를 제시함으로써 MLLM 기반 에이전트의 공간 추론 능력을 체계적으로 평가할 수 있는 기틀을 마련했으며, SFT와 RL을 통한 성능 향상을 보여주되 남은 큰 도전과제도 명확히 규명한 높은 가치의 연구이다.

## Related Papers

- 🔗 후속 연구: [[papers/1932_FocusNav_Spatial_Selective_Attention_with_Waypoint_Guidance/review]] — 공간 인식 기반 네비게이션에서 360도 파노라마 탐색과 선택적 주의 메커니즘이 상호 보완적이다.
- 🏛 기반 연구: [[papers/2104_MolmoSpaces_A_Large-Scale_Open_Ecosystem_for_Robot_Navigatio/review]] — 대규모 로봇 네비게이션 생태계에서 360도 시각 탐색이 다양한 환경에서의 일반화 능력을 제공할 수 있다.
- 🧪 응용 사례: [[papers/1774_A_Behavior_Architecture_for_Fast_Humanoid_Robot_Door_Travers/review]] — 도어 통과와 같은 구체적 작업에서 360도 시각 탐색이 필요한 환경 인식 능력을 제공합니다.
- 🏛 기반 연구: [[papers/2117_Omni-Perception_Omnidirectional_Collision_Avoidance_for_Legg/review]] — 전방향 충돌 회피를 위한 omnidirectional perception과 360도 시각 탐색의 이론적 기반을 공유합니다.
- 🔗 후속 연구: [[papers/1939_Gait-Adaptive_Perceptive_Humanoid_Locomotion_with_Real-Time/review]] — 실시간 지형 인식을 통한 보행 제어에 360도 환경 인식 기능을 통합할 수 있습니다.
- 🔗 후속 연구: [[papers/2087_LookOut_Real-World_Humanoid_Egocentric_Navigation/review]] — 실제 환경에서의 휴머노이드 네비게이션을 360° 파노라마 시각 탐색으로 확장하여 복잡한 현실 환경에서의 능동적 물체 탐색을 실현했다.
- 🧪 응용 사례: [[papers/1845_Collision-Free_Humanoid_Traversal_in_Cluttered_Indoor_Scenes/review]] — 360° 시각 탐색 기술을 실내 환경을 넘어 복잡한 현실 공간으로 확장하여 충돌 없는 휴머노이드 이동을 실현했다.
- 🧪 응용 사례: [[papers/1774_A_Behavior_Architecture_for_Fast_Humanoid_Robot_Door_Travers/review]] — 도어 통과 작업에서 360도 시각 탐색을 통한 환경 인식이 GPU 가속 인식 시스템을 보완할 수 있습니다.
- 🧪 응용 사례: [[papers/1879_DIJIT_A_Robotic_Head_for_an_Active_Observer/review]] — DIJIT의 생체모방 쌍안 로봇 헤드 기술이 실제 환경에서 360도 시각 탐색을 수행하는 구체적 응용사례입니다.
- 🔄 다른 접근: [[papers/1892_E-SDS_Environment-aware_See_it_Do_it_Sorted_-_Automated_Envi/review]] — 환경 인식 보행에서 VLM 기반 자동 정책 학습과 visual search를 통한 in-the-wild navigation의 서로 다른 환경 적응 접근법을 비교한다.
- 🔄 다른 접근: [[papers/1932_FocusNav_Spatial_Selective_Attention_with_Waypoint_Guidance/review]] — 둘 다 humanoid의 환경 인식과 navigation을 다루지만, FocusNav는 waypoint 기반 선택적 주의에, Thinking in 360°는 전방위 시각 탐색에 집중합니다.
- 🏛 기반 연구: [[papers/1911_Emergent_Active_Perception_and_Dexterity_of_Simulated_Humano/review]] — 360° 시각적 탐색 연구가 PDC 프레임워크의 egocentric vision 기반 능동적 인식을 위한 기본적인 시각 탐색 기술을 제공한다.
- 🏛 기반 연구: [[papers/1998_Humanoid_Occupancy_Enabling_A_Generalized_Multimodal_Occupan/review]] — 360도 visual search가 휴머노이드의 일반화된 환경 인식 시스템의 기반이 됩니다.
- 🏛 기반 연구: [[papers/2057_Learning_Humanoid_Navigation_from_Human_Data/review]] — 야생 환경에서의 휴머노이드 시각 탐색 능력이 자율 내비게이션의 기반 제공
- 🏛 기반 연구: [[papers/2071_Learning_to_Look_Seeking_Information_for_Decision_Making_via/review]] — 야생에서의 휴머노이드 시각 탐색의 이론적 기반과 구현 방법을 제공한다.
- 🏛 기반 연구: [[papers/2080_Let_Humanoids_Hike_Integrative_Skill_Development_on_Complex/review]] — 야생에서의 휴머노이드 시각 탐색의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/2087_LookOut_Real-World_Humanoid_Egocentric_Navigation/review]] — 야생에서의 휴머노이드 시각 탐색의 이론적 기반과 구현 방법을 제공한다.
- 🔗 후속 연구: [[papers/2111_NoMaD_Goal_Masked_Diffusion_Policies_for_Navigation_and_Expl/review]] — NoMaD의 goal masked diffusion을 360도 시각 탐색과 결합하여 더 포괄적인 야생 환경 내비게이션을 달성할 수 있다.
