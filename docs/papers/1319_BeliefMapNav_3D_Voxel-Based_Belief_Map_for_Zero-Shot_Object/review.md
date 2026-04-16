---
title: "1319_BeliefMapNav_3D_Voxel-Based_Belief_Map_for_Zero-Shot_Object"
authors:
  - "Zibo Zhou"
  - "Yue Hu"
  - "Lingkai Zhang"
  - "Zonglin Li"
  - "Siheng Chen"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 3D voxel 기반 belief map을 활용하여 zero-shot object navigation에서 LLM의 의미론적 추론과 계층적 공간 정보를 통합함으로써 로봇이 사전 학습이나 사전 구축 맵 없이 자연어로 지정된 대상을 미지의 환경에서 찾을 수 있도록 한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhou et al._2025_BeliefMapNav 3D Voxel-Based Belief Map for Zero-Shot Object Navigation.pdf"
---

# BeliefMapNav: 3D Voxel-Based Belief Map for Zero-Shot Object Navigation

> **저자**: Zibo Zhou, Yue Hu, Lingkai Zhang, Zonglin Li, Siheng Chen | **날짜**: 2025-05-27 | **URL**: [https://arxiv.org/abs/2506.06487](https://arxiv.org/abs/2506.06487)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: BeliefMapNav pipeline: The agent initializes with a 360° rotation. During exploration,*

본 논문은 3D voxel 기반 belief map을 활용하여 zero-shot object navigation에서 LLM의 의미론적 추론과 계층적 공간 정보를 통합함으로써 로봇이 사전 학습이나 사전 구축 맵 없이 자연어로 지정된 대상을 미지의 환경에서 찾을 수 있도록 한다.

## Motivation

- **Known**: 기존 zero-shot object navigation 방법은 BEV value map 기반 방식 또는 LLM/VLM 기반 추론 방식으로 나뉘지만, 두 접근법 모두 공간 추론의 한계와 정확도 부족 문제를 겪고 있다.
- **Gap**: 현존 방법들은 LLM/VLM의 제한된 공간 이해 능력으로 인해 정확한 대상 위치 예측에 실패하며, greedy 네비게이션 전략으로 인해 탐색 효율성이 떨어진다.
- **Why**: 가정 환경의 물체 회수, 산업 시설의 결함 감지, 창고 운영 등 실제 로봇 응용에서 사전 맵 없이 유연하게 대상을 찾는 능력이 필수적이다.
- **Approach**: 계층적 공간 의미론과 LLM 기반 상식을 3D voxel space에 통합하는 belief map을 구축하고, frontier 관찰 belief 추정 및 확률 기반 경로 계획을 통해 효율적인 네비게이션을 수행한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Visualization of the prior belief map, visibility map, and the posterior belief map, with an*

- **3D Voxel-Based Belief Map**: 계층적 공간 구조와 LLM 의미론적 priors, 실시간 관찰을 통합하여 3D 공간에서 대상 위치의 정확한 prior 및 posterior 분포 추정
- **BeliefMapNav 시스템**: belief map 기반 frontier 관찰 belief 추정과 기댓값 거리 최소화를 통한 순차적 경로 계획으로 효율적인 탐색 달성
- **State-of-the-Art 성능**: HM3D에서 SR 5.86%, SPL 46.4% 개선, MP3D 및 HSSD에서도 27.8~46.4% 성능 향상

## How

![Figure 2](figures/fig2.webp)

*Figure 2: BeliefMapNav pipeline: The agent initializes with a 360° rotation. During exploration,*

- LLM에 대상과 prompt를 입력하여 target-adaptive semantic cues 생성
- RGB-D 센서 입력과 agent 포즈를 기반으로 3D hierarchical semantic map 구성
- Belief map과 visibility map을 결합하여 각 frontier의 FOV에서 대상 감지 확률의 posterior observation belief 계산
- Expected distance cost 최소화를 통한 최적 frontier 선택 및 순차적 경로 계획
- Target 감지 후 정확한 네비게이션으로 성공 조건 만족

## Originality

- 3D voxel-based belief map이라는 구조적 표현으로 계층적 공간 의미론과 LLM 기반 의미론을 명시적으로 통합하는 새로운 접근
- Visibility map과의 결합을 통한 posterior belief 업데이트로 dynamic한 불확실성 모델링
- FOV 기반 frontier observation belief 추정과 기댓값 최소화 계획이 결합된 효율성 최적화 전략
- Open-vocabulary zero-shot 설정에서 사전 구축 맵과 task-specific 학습 제거

## Limitation & Further Study

- 계산 복잡도: 3D voxel map 유지 및 실시간 belief 업데이트의 메모리 및 연산 요구사항이 명시되지 않음
- LLM 의존성: LLM의 성능에 크게 의존하므로 LLM의 오류나 hallucination에 취약할 수 있음
- 제한된 평가 환경: HM3D, MP3D, HSSD 벤치마크는 실내 환경에 국한되며 실외 환경 성능 미평가
- Depth 센서 의존성: RGB-D 센서 요구로 RGB-only 환경에서 적용 불가
- 후속 연구: 다중 에이전트 협력 탐색, 동적 환경 적응, 계산 효율성 개선, 실외/혼합 환경 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 3D voxel-based belief map을 통해 LLM 의미론과 공간 구조를 효과적으로 통합하고 확률 기반 경로 계획으로 zero-shot object navigation 성능을 대폭 향상시킨 우수한 기여이다. 다만 실제 로봇 배치 시 계산 복잡도와 LLM 오류에 대한 강건성 검토가 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1470_MapNav_A_Novel_Memory_Representation_via_Annotated_Semantic/review]] — 3D voxel belief map 대신 annotated semantic map을 활용한 다른 메모리 기반 네비게이션 접근법
- 🏛 기반 연구: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — visual language map의 공간-언어 표현 개념이 3D voxel belief map 설계의 이론적 기반
- 🏛 기반 연구: [[papers/1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me/review]] — CLIP-Fields의 의미론적 필드 개념이 BeliefMapNav의 3D voxel 기반 belief map 구축의 이론적 기초를 제공합니다.
- 🔗 후속 연구: [[papers/1311_ApexNav_An_Adaptive_Exploration_Strategy_for_Zero-Shot_Objec/review]] — ApexNav의 zero-shot 탐색 전략을 3D belief map과 LLM 추론으로 발전시킨 고도화된 접근법입니다.
- 🔄 다른 접근: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — Zero-shot 객체 네비게이션에서 3D voxel belief map과 비디오 기반 VLM 계획이 다른 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1505_Open-vocabulary_Queryable_Scene_Representations_for_Real_Wor/review]] — 실세계를 위한 open-vocabulary 쿼리 가능 장면 표현이 belief map 기반 네비게이션의 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1600_UniGoal_Towards_Universal_Zero-shot_Goal-oriented_Navigation/review]] — 범용 zero-shot 목표 지향 네비게이션과 3D belief map 기반 객체 네비게이션을 결합할 수 있습니다.
- 🔄 다른 접근: [[papers/1589_TopV-Nav_Unlocking_the_Top-View_Spatial_Reasoning_Potential/review]] — object navigation에서 서로 다른 지도 표현 - top-view reasoning vs 3D voxel-based belief map입니다.
- 🔗 후속 연구: [[papers/1630_WMNav_Integrating_Vision-Language_Models_into_World_Models_f/review]] — WMNav의 메모리 기반 탐색 전략을 zero-shot object navigation으로 확장한 접근법이다.
- 🔗 후속 연구: [[papers/1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me/review]] — CLIP-Fields의 의미론적 필드가 BeliefMapNav의 3D voxel belief map 구축에 기술적 토대를 제공합니다.
- 🔄 다른 접근: [[papers/1311_ApexNav_An_Adaptive_Exploration_Strategy_for_Zero-Shot_Objec/review]] — 둘 다 zero-shot object navigation을 다루지만 ApexNav는 의미-기하학 적응적 탐색을, BeliefMapNav는 3D voxel belief map을 사용하는 다른 접근법입니다.
