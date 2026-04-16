---
title: "1600_UniGoal_Towards_Universal_Zero-shot_Goal-oriented_Navigation"
authors:
  - "Hang Yin"
  - "Xiuwei Xu"
  - "Lingqing Zhao"
  - "Ziwei Wang"
  - "Jie Zhou"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "UniGoal은 object category, instance image, text description 등 다양한 목표 유형을 통일된 graph 표현으로 변환하여 LLM 기반의 단일 모델로 세 가지 navigation 작업을 zero-shot으로 수행하는 범용 프레임워크를 제안한다."
tags:
  - "cat/Visual_Language_Navigation"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Open-Vocabulary_Scene_Navigation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yin et al._2025_UniGoal Towards Universal Zero-shot Goal-oriented Navigation.pdf"
---

# UniGoal: Towards Universal Zero-shot Goal-oriented Navigation

> **저자**: Hang Yin, Xiuwei Xu, Lingqing Zhao, Ziwei Wang, Jie Zhou, Jiwen Lu | **날짜**: 2025-03-13 | **URL**: [https://arxiv.org/abs/2503.10630](https://arxiv.org/abs/2503.10630)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Framework of UniGoal. We convert different types of goals into a uniform graph representation and maintain an *

UniGoal은 object category, instance image, text description 등 다양한 목표 유형을 통일된 graph 표현으로 변환하여 LLM 기반의 단일 모델로 세 가지 navigation 작업을 zero-shot으로 수행하는 범용 프레임워크를 제안한다.

## Motivation

- **Known**: 기존 zero-shot navigation 방법들은 LLM을 활용하지만 특정 작업에 특화되어 있으며, 통일된 goal 표현을 학습하는 supervised universal 방법들은 시뮬레이션 환경에 과적합되어 실제 환경에서 일반화 능력이 떨어진다.
- **Gap**: vision 관련 작업(instance image goal navigation)을 포함하면서 동시에 zero-shot 성능을 유지하는 범용 navigation 프레임워크가 부재하다.
- **Why**: 실제 로보틱 응용에서 agent는 다양한 형태의 인간 지시를 처리해야 하므로, 높은 versatility를 갖춘 단일 모델의 범용 navigation 방법이 필수적이다.
- **Approach**: scene과 goal을 모두 graph 구조로 표현하고 graph matching을 통해 matching 정도를 파악한 후, zero-matched/partial-matched/perfect-matched 세 단계에 따라 다른 exploration 전략을 적용하는 multi-stage 정책을 LLM으로 구현한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. State-of-the-art zero-shot goal-oriented navigation meth-*

- **범용성**: Object-goal Navigation, Instance-image-goal Navigation, Text-goal Navigation 세 가지 서로 다른 navigation 작업을 single model로 처리
- **성능**: MatterPort3D, HM3D, RoboTHOR 벤치마크에서 state-of-the-art zero-shot 성능 달성, task-specific zero-shot 방법과 supervised universal 방법을 능가
- **구조적 정보 보존**: 순수 text 대비 graph 표현을 통해 3D scene의 구조적 정보를 최대한 보존하면서 LLM 활용

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Framework of UniGoal. We convert different types of goals into a uniform graph representation and maintain an *

- RGB-D observation을 online 3D scene graph로 변환 (node: 객체, edge: 공간 관계)
- 다양한 goal 유형(category, image, text)을 통일된 graph 표현인 goal graph로 변환
- 각 시간 단계에서 scene graph와 goal graph 간 graph matching 수행
- Matching score에 따라 세 단계의 exploration 정책 적용: (1) Zero-matching 단계에서 goal subgraph 반복 탐색, (2) Partial-matching 단계에서 coordinate projection과 anchor pair alignment로 goal 위치 추론, (3) Perfect-matching 단계에서 scene graph correction과 goal verification 적용
- Blacklist mechanism 도입으로 매칭되지 않은 부분을 freeze하고 새로운 영역 탐색 유도
- LLM을 prompt engineering으로 각 단계의 decision 수행

## Originality

- Goal을 graph로 표현하는 것이 핵심 혁신으로, 기존의 text-only 표현 대비 visual goal(instance image)의 정보를 효과적으로 통합
- Scene graph와 goal graph 간의 graph matching을 기반으로 한 multi-stage exploration policy는 matching 상태를 명시적으로 활용하는 새로운 접근
- Blacklist mechanism은 navigation 과정에서 exploration 효율성을 높이는 실질적인 기술 기여

## Limitation & Further Study

- Scene graph 구성 과정에서 object detection 오류가 누적될 수 있으며, 이것이 최종 navigation 성능에 미치는 영향 분석 부재
- Graph matching의 정확도가 전체 성능의 병목이 될 수 있으나, 다양한 matching 알고리즘의 비교 실험 부족
- Real-world 환경에서의 성능 평가 부재 (시뮬레이션 환경만 평가)
- 후속 연구로는 graph construction의 robustness 향상, sim-to-real gap 감소, 더 복잡한 scene composition 처리 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: UniGoal은 graph 표현을 통해 vision과 language 기반 navigation 작업을 우아하게 통합하고, 실험적으로도 범용성과 zero-shot 성능을 동시에 달성하는 우수한 연구이다. 다만 실제 환경 평가와 graph 구성 robustness에 대한 더 깊은 분석이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1311_ApexNav_An_Adaptive_Exploration_Strategy_for_Zero-Shot_Objec/review]] — zero-shot object navigation에서 서로 다른 접근법 - unified framework vs adaptive exploration입니다.
- 🏛 기반 연구: [[papers/1507_OpenBench_A_New_Benchmark_and_Baseline_for_Semantic_Navigati/review]] — semantic navigation benchmark가 universal goal-oriented navigation의 평가 기반이 됩니다.
- 🔗 후속 연구: [[papers/1367_DivScene_Towards_Open-Vocabulary_Object_Navigation_with_Larg/review]] — open-vocabulary navigation을 다양한 목표 유형으로 확장한 범용 프레임워크입니다.
- 🔗 후속 연구: [[papers/1456_LERF_Language_Embedded_Radiance_Fields/review]] — LERF의 language embedded radiance fields가 UniGoal의 통합된 graph 표현을 3D 공간에서 더욱 풍부하게 확장할 수 있다.
- 🏛 기반 연구: [[papers/1294_A_Generalist_Agent/review]] — Gato의 generalist agent 개념이 UniGoal의 단일 모델로 다양한 navigation 작업을 수행하는 접근법의 이론적 토대가 된다.
- 🔗 후속 연구: [[papers/1319_BeliefMapNav_3D_Voxel-Based_Belief_Map_for_Zero-Shot_Object/review]] — 범용 zero-shot 목표 지향 네비게이션과 3D belief map 기반 객체 네비게이션을 결합할 수 있습니다.
- 🔄 다른 접근: [[papers/1497_OctoNav_Towards_Generalist_Embodied_Navigation/review]] — 둘 다 목표 지향 네비게이션에 초점을 맞추지만, OctoNav는 멀티모달 지시를, UniGoal은 제로샷 범용성에 집중한다.
- 🔗 후속 연구: [[papers/1507_OpenBench_A_New_Benchmark_and_Baseline_for_Semantic_Navigati/review]] — universal zero-shot goal-oriented navigation을 스마트 로지스틱스의 실제 배송 환경에 특화하여 적용한 실용적 확장을 보여준다.
- 🔗 후속 연구: [[papers/1311_ApexNav_An_Adaptive_Exploration_Strategy_for_Zero-Shot_Objec/review]] — adaptive exploration을 zero-shot navigation에서 universal goal-oriented navigation으로 확장한 발전된 연구
- 🔗 후속 연구: [[papers/1367_DivScene_Towards_Open-Vocabulary_Object_Navigation_with_Larg/review]] — DivScene의 오픈 어휘 객체 네비게이션과 UniGoal의 범용 제로샷 목표 지향 네비게이션은 개방형 환경 네비게이션의 발전된 형태이다.
