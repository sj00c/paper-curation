---
title: "1329_CityNavAgent_Aerial_Vision-and-Language_Navigation_with_Hier"
authors:
  - "Weichen Zhang"
  - "Chen Gao"
  - "Shiquan Yu"
  - "Ruiying Peng"
  - "Baining Zhao"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "CityNavAgent는 계층적 의미 계획(HSPM)과 전역 메모리 모듈을 통합하여 도시 환경에서 드론이 자연어 지시를 따라 네비게이션하는 aerial VLN 작업을 수행하는 LLM 기반 에이전트이다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/LLM_Task_Planning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_CityNavAgent Aerial Vision-and-Language Navigation with Hierarchical Semantic Planning and Global M.pdf"
---

# CityNavAgent: Aerial Vision-and-Language Navigation with Hierarchical Semantic Planning and Global Memory

> **저자**: Weichen Zhang, Chen Gao, Shiquan Yu, Ruiying Peng, Baining Zhao, Qian Zhang, Jinqiang Cui, Xinlei Chen, Yong Li | **날짜**: 2025-05-08 | **URL**: [https://arxiv.org/abs/2505.05622](https://arxiv.org/abs/2505.05622)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: The overall workflow of CityNavAgent.*

CityNavAgent는 계층적 의미 계획(HSPM)과 전역 메모리 모듈을 통합하여 도시 환경에서 드론이 자연어 지시를 따라 네비게이션하는 aerial VLN 작업을 수행하는 LLM 기반 에이전트이다.

## Motivation

- **Known**: 기존 ground VLN 에이전트들은 실내·실외 환경에서 좋은 성능을 달성했으나, aerial VLN은 미리 정의된 네비게이션 그래프가 없고 장시간 탐색 시 action space가 지수적으로 확장되어 어려움을 겪고 있다.
- **Gap**: 기존 방법들은 aerial VLN의 복잡한 도시 장면 이해(고도별 의미 밀도 변화)와 장시간 motion planning의 지수적 복잡성(m^n)을 충분히 해결하지 못하고 있으며, STMR 같은 이전 방법들은 높이 정보를 활용하지 않는다.
- **Why**: Aerial VLN은 드론 기반 구조 재난 대응, 운송, 도시 검사 등 실제 응용 분야에서 인간-로봇 상호작용 비용을 줄이고 3D 공간 추론 능력을 요구하는 중요한 embodied AI 문제이다.
- **Approach**: Open-vocabulary perception module로 도시 장면의 복잡한 의미를 추출하고, HSPM으로 navigation task를 landmark-level, object-level, motion-level의 계층적 sub-goals로 분해하여 action space를 축소한다. 추가로 global memory module이 역사적 궤적을 topological graph에 저장하여 재방문 대상의 네비게이션을 단순화한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: CityNavAgent consists of three key modules. The open-vocabulary module extracts open-vocabulary*

- **Aerial VLN 벤치마크에서 최고 성능 달성**: 두 개의 aerial VLN 벤치마크에서 state-of-the-art 성능을 달성하고 success rate와 path following에서 유의미한 개선을 보였다.
- **장시간 네비게이션 복잡도 감소**: 계층적 의미 계획을 통해 지수적 action space 복잡도(m^n)를 선형적으로 축소했다.
- **높이 정보 통합**: 이전 STMR과 달리 3D 공간의 높이 정보를 활용하여 네비게이션 오류를 감소시켰다.
- **Zero-shot 네비게이션 가능**: LLM의 reasoning 능력을 활용하여 미리 정의된 그래프 없이 zero-shot 환경에서 동작한다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2: CityNavAgent consists of three key modules. The open-vocabulary module extracts open-vocabulary*

- Open-vocabulary perception: LLM을 통한 scene captioning과 prompt engineering으로 instruction 관련 객체 추출, vision foundation model을 이용한 open-vocabulary image grounding
- Hierarchical semantic planning: Landmark-level planning에서 전체 경로의 주요 landmark 시퀀스 결정 → Object-level planning에서 landmark 도달을 위한 객체 추론 → Motion-level planning에서 최종 waypoint와 action sequence 예측
- Global memory module: Historical trajectory를 topological graph 형태로 저장하여 재방문 대상의 네비게이션 성능 향상
- Planning frequency control: 상위 계획(landmark-level)은 낮은 빈도로, 하위 계획(motion-level)은 높은 빈도로 수행하여 효율성 극대화

## Originality

- Aerial VLN에 특화된 계층적 의미 계획 프레임워크 제안 - 기존 방법들의 discrete graph 기반 접근과 달리 continuous 3D space에서 계층적 abstraction 도입
- Urban environment의 의미 밀도 동적 변화를 명시적으로 고려한 설계
- Global memory를 topological graph로 표현하여 long-term navigation에서 재사용성 제공
- Zero-shot LLM 기반 접근으로 사전 학습 데이터나 pre-defined graph 불필요

## Limitation & Further Study

- Open-vocabulary perception의 LLM captioning이 복잡한 도시 장면에서 모든 의미있는 객체를 정확히 추출하지 못할 수 있음
- Hierarchical planning의 각 level 간 오류 전파(error propagation) 문제 미분석
- Global memory의 topological graph 구성 방식과 메모리 용량 제한에 대한 상세한 논의 부족
- 실제 드론 플랫폼에서의 검증이 부재하며 시뮬레이션 환경에서만 평가됨
- 후속연구로 시각적 오류에 대한 강건성 개선, 동적 도시 환경(건설 중인 지역, 이동하는 객체) 처리, 실제 드론 배포 실험 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: CityNavAgent는 aerial VLN의 미해결 과제들(복잡한 도시 장면 이해, 지수적 action space)을 체계적으로 해결하는 창의적인 계층적 계획 프레임워크를 제시하며, 벤치마크에서 state-of-the-art 성능을 달성한 의미있는 연구이다. 다만 실제 드론 검증과 오류 전파 분석이 필요하다.

## Related Papers

- 🧪 응용 사례: [[papers/1508_Openfly_A_comprehensive_platform_for_aerial_vision-language/review]] — aerial VLN의 도시 환경 네비게이션 개념을 포괄적인 aerial vision-language 플랫폼으로 확장 적용
- 🏛 기반 연구: [[papers/1432_Improving_Vision-and-Language_Navigation_with_Image-Text_Pai/review]] — image-text paired learning이 aerial VLN에서 계층적 의미 계획의 핵심 기반 기술
- 🔄 다른 접근: [[papers/1443_L3MVN_Leveraging_Large_Language_Models_for_Visual_Target_Nav/review]] — 대규모 언어 모델을 활용한 다른 시각적 타겟 네비게이션 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1461_LM-Nav_Robotic_Navigation_with_Large_Pre-Trained_Models_of_L/review]] — 대규모 사전학습 모델을 활용한 로봇 네비게이션의 기초 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1505_Open-vocabulary_Queryable_Scene_Representations_for_Real_Wor/review]] — 오픈 어휘 장면 표현을 항공 네비게이션으로 확장 적용한다.
- 🔄 다른 접근: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — 둘 다 vision-language navigation이지만 CityNavAgent는 aerial 환경에서 LLM 기반으로, NaVid는 지상에서 VLM 기반으로 접근합니다.
- 🧪 응용 사례: [[papers/1303_Advances_in_Embodied_Navigation_Using_Large_Language_Models/review]] — LLM 기반 embodied navigation 서베이에서 제시된 방법론을 도시 aerial 환경이라는 특수한 도메인에 적용한 사례입니다.
- 🏛 기반 연구: [[papers/1441_JanusVLN_Decoupling_Semantics_and_Spatiality_with_Dual_Impli/review]] — JanusVLN의 의미론적-공간적 분리 개념이 CityNavAgent의 계층적 의미 계획 구조의 기초가 됩니다.
- 🔄 다른 접근: [[papers/1507_OpenBench_A_New_Benchmark_and_Baseline_for_Semantic_Navigati/review]] — 대규모 지역 네비게이션에서 OpenStreetMap 기반 시스템 vs hierarchical aerial vision-language navigation이라는 서로 다른 스케일의 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1508_Openfly_A_comprehensive_platform_for_aerial_vision-language/review]] — 항공 비전-언어 네비게이션의 기반 기술은 CityNavAgent의 계층적 항공 네비게이션에도 적용됩니다.
- 🧪 응용 사례: [[papers/1303_Advances_in_Embodied_Navigation_Using_Large_Language_Models/review]] — CityNavAgent는 LLM 기반 네비게이션의 구체적 구현 사례로서 aerial domain에 특화된 응용입니다.
