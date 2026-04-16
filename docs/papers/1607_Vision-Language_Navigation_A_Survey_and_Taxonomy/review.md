---
title: "1607_Vision-Language_Navigation_A_Survey_and_Taxonomy"
authors:
  - "Wansen Wu"
  - "Tao Chang"
  - "Xinmeng Li"
date: "2021.08"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 Vision-Language Navigation(VLN) 분야를 종합적으로 조사하고, 언어 지시의 특성에 따라 single-turn/multi-turn, goal-oriented/route-oriented, passive/interactive 등으로 체계적으로 분류한 택소노미를 제시한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Visual_Language_Navigation"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Instruction-Following_Robot_Navigation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wu et al._2021_Vision-Language Navigation A Survey and Taxonomy.pdf"
---

# Vision-Language Navigation: A Survey and Taxonomy

> **저자**: Wansen Wu, Tao Chang, Xinmeng Li | **날짜**: 2021-08-26 | **URL**: [https://arxiv.org/abs/2108.11544](https://arxiv.org/abs/2108.11544)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2. The knowledge graph is summarized in this review.*

본 논문은 Vision-Language Navigation(VLN) 분야를 종합적으로 조사하고, 언어 지시의 특성에 따라 single-turn/multi-turn, goal-oriented/route-oriented, passive/interactive 등으로 체계적으로 분류한 택소노미를 제시한다.

## Motivation

- **Known**: Vision과 Language를 결합한 navigation 연구가 증가하고 있으며, 기존 조사들은 Embodied AI나 multimodal vision-language 분야에 국한되어 있다. R2R, REVERIE 등 다양한 VLN 태스크와 데이터셋이 제안되었다.
- **Gap**: 기존 조사들은 VLN 태스크 자체에 특화된 포괄적 분류 체계와 비교 분석이 부족하며, 다양한 VLN 태스크들의 본질적 차이점과 각 모델의 설계 요구사항 간 관계를 명확히 하는 연구가 필요하다.
- **Why**: VLN은 인간의 기대치에 더 부합하는 인공지능 태스크이며, 자연어 처리, 컴퓨터 비전, 로보틱스를 통합하는 복잡한 문제로 체계적인 이해와 분류가 필수적이다.
- **Approach**: 언어 지시의 제시 방식(단회/다회)과 형태(목표/경로)에 따라 VLN 태스크를 계층적으로 분류하고, 각 카테고리별 데이터셋, 시뮬레이터, 모델 설계 특성을 상세히 분석한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2. The knowledge graph is summarized in this review.*

- **포괄적 VLN 택소노미**: 단회/다회, 목표/경로 지향, 수동/상호작용 기반의 4단계 분류 체계 제시로 VLN 태스크의 본질적 차이를 명확히 함
- **광범위한 태스크 및 데이터셋 카탈로그**: R2R, REVERIE, ALFRED 등 40개 이상의 VLN 관련 태스크와 Matterport3D, Gibson 등 시뮬레이터를 체계적으로 정리
- **모델 설계 요구사항 분석**: 각 VLN 카테고리가 요구하는 에이전트의 서로 다른 기능(경로 계획, 상호작용, 객체 조작 등)을 명확히 구분
- **한계점 및 개선 방향 제시**: 기존 VLN 모델과 태스크 설정의 제한사항을 분석하고 지식 통합 및 실물 환경 구현의 미래 기회를 제안

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. The knowledge graph is summarized in this review.*

- 언어 지시 제시 방식에 따른 1차 분류: single-turn vs multi-turn
- Single-turn 태스크의 2차 분류: goal-oriented(목표 위치 지정)와 route-oriented(상세 경로 지정)
- Multi-turn 태스크의 2차 분류: passive(미리 결정된 지시)와 interactive(에이전트 질의 가능)
- 각 카테고리별 주요 데이터셋, 시뮬레이터, 태스크 특성을 표(Table I)로 정렬하여 비교 분석
- Knowledge graph(Figure 2)를 통해 태스크, 데이터셋, 시뮬레이터 간 관계를 시각화

## Originality

- VLN 분야에 최초로 **언어 지시 특성 기반의 체계적 택소노미** 제시로 기존 environment 기반 분류의 한계를 극복
- Single-turn/multi-turn과 goal-oriented/route-oriented의 조합을 통한 **4단계 계층적 분류 체계** 개발
- Passive/interactive 구분을 통해 **에이전트와 환경의 상호작용 방식**을 명시적으로 모델링
- 40개 이상의 VLN 관련 태스크를 단일 프레임워크로 통합하여 **포괄적 학술 지형도** 제시

## Limitation & Further Study

- **시각적 환경의 다양성 미흡**: 실내/실외 환경만 다루며, 더 복잡한 혼합 환경(혼잡한 거리, 역동적 장애물 등)에 대한 고려 부족
- **실제 로봇 환경과의 괴리**: 대부분 시뮬레이션 환경 기반이며 RobotSlang 외 실물 환경 태스크가 극히 제한적
- **언어 지시의 복잡도 제한**: 현재 태스크들이 상대적으로 단순한 자연어 지시를 사용하며, 모호성, 다의성, 암묵적 참조 등 현실적 복잡성 부족
- **멀티모달 상호작용의 제한**: 음성, 제스처 등 추가 모달리티 통합 필요성 미제시
- **후속 연구 방향**: (1) 실물 환경에서의 VLN 모델 검증, (2) 외부 지식(상식, 의미론적 정보) 통합, (3) 동적 환경과 예측 불가능한 상황 처리, (4) 다국어 및 다문화 언어 지시 지원

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 VLN 분야의 첫 번째 포괄적 조사로서, 언어 지시의 특성 기반 4단계 택소노미를 제시하여 산재된 VLN 태스크들을 통일된 프레임워크로 정리했다. 명확한 분류 체계와 광범위한 문헌 커버리지는 연구자들이 VLN의 전체 landscape를 이해하고 미래 연구 방향을 설정하는 데 큰 도움이 될 것으로 예상된다.

## Related Papers

- 🏛 기반 연구: [[papers/1324_Bridging_Language_and_Action_A_Survey_of_Language-Conditione/review]] — language-conditioned control의 포괄적 서베이가 VLN 분야의 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1486_Multimodal_Perception_for_Goal-oriented_Navigation_A_Survey/review]] — VLN을 goal-oriented navigation의 multimodal perception으로 확장한 포괄적 조사입니다.
- 🔗 후속 연구: [[papers/1575_SmartWay_Enhanced_Waypoint_Prediction_and_Backtracking_for_Z/review]] — VLN 분류 체계를 바탕으로 zero-shot continuous environment에 특화된 발전입니다.
- 🧪 응용 사례: [[papers/1443_L3MVN_Leveraging_Large_Language_Models_for_Visual_Target_Nav/review]] — L3MVN은 VLN 서베이에서 분류한 언어 기반 시각 네비게이션의 구체적인 구현 사례를 제시한다.
- 🧪 응용 사례: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — NaVid는 VLN 서베이가 다루는 vision-language navigation의 비디오 기반 구체적 구현 사례다.
- 🧪 응용 사례: [[papers/1507_OpenBench_A_New_Benchmark_and_Baseline_for_Semantic_Navigati/review]] — OpenBench는 VLN 서베이에서 다룬 semantic navigation을 위한 실제 벤치마크와 baseline을 제공한다.
- 🧪 응용 사례: [[papers/1441_JanusVLN_Decoupling_Semantics_and_Spatiality_with_Dual_Impli/review]] — JanusVLN은 VLN 서베이의 분류 체계에 해당하는 의미론과 공간성을 분리한 구체적 구현 사례다.
- 🔗 후속 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — VLN survey의 체계적 분류가 Pure VLA Models survey와 결합되어 vision-language-action 전반에 대한 더 포괄적인 이해를 제공한다.
- 🏛 기반 연구: [[papers/1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI/review]] — World Models for Embodied AI의 포괄적 조사가 VLN taxonomy의 이론적 배경과 미래 발전 방향을 제시한다.
- 🔄 다른 접근: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — 둘 다 로봇 분야의 comprehensive review이지만 VLN survey는 navigation에, Foundation Model Driven Robotics는 foundation model에 집중한다.
- 🧪 응용 사례: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — VLA Models의 concepts와 applications가 VLN taxonomy를 action까지 포함한 더 넓은 프레임워크로 확장하는 데 활용된다.
- 🏛 기반 연구: [[papers/1432_Improving_Vision-and-Language_Navigation_with_Image-Text_Pai/review]] — Vision-Language Navigation 서베이에서 제시된 기본 개념들을 웹 데이터 활용으로 발전시킨다.
- 🏛 기반 연구: [[papers/1414_Ground_Slow_Move_Fast_A_Dual-System_Foundation_Model_for_Gen/review]] — Vision-Language Navigation Survey가 DualVLN의 dual-system navigation model 설계의 이론적 배경과 방법론을 제공합니다.
- 🔗 후속 연구: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — vision-language navigation에 대한 기존 survey를 multimodal fusion 기법과 최신 VLM 응용으로 확장하여 더 포괄적인 로봇 비전 연구 방향을 제시한다.
- 🏛 기반 연구: [[papers/1486_Multimodal_Perception_for_Goal-oriented_Navigation_A_Survey/review]] — 멀티모달 목표 지향 네비게이션 서베이가 Vision-Language Navigation의 기존 분류 체계를 멀티모달 인식으로 확장한 연구이다.
- 🔄 다른 접근: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — 기존 시각-언어 네비게이션 연구들과 달리 NaVid는 비디오 기반 VLM으로 지도나 깊이 없이 네비게이션을 수행한다.
- 🏛 기반 연구: [[papers/1497_OctoNav_Towards_Generalist_Embodied_Navigation/review]] — Vision-Language Navigation 분야의 전반적 동향을 이해하는 데 필요한 기초 서베이이다.
- 🏛 기반 연구: [[papers/1575_SmartWay_Enhanced_Waypoint_Prediction_and_Backtracking_for_Z/review]] — Vision-Language Navigation 분야의 체계적 분류와 현황을 제시하는 기반 연구입니다.
- 🏛 기반 연구: [[papers/1549_RoboTron-Nav_A_Unified_Framework_for_Embodied_Navigation_Int/review]] — vision-language navigation의 포괄적인 survey와 taxonomy를 제공하여 RoboTron-Nav의 unified embodied navigation framework 설계에 필요한 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1378_Embodied_Navigation_Foundation_Model/review]] — Vision-Language Navigation Survey가 NavFoM의 크로스-구현체 네비게이션 모델 설계의 이론적 배경과 방법론을 제공합니다.
- 🏛 기반 연구: [[papers/1300_A_Survey_on_Vision-Language-Action_Models_for_Autonomous_Dri/review]] — Vision-Language Navigation의 전반적인 분류체계와 기초 개념을 제공합니다.
- 🔗 후속 연구: [[papers/1303_Advances_in_Embodied_Navigation_Using_Large_Language_Models/review]] — vision-language navigation의 전반적 조사를 LLM 특화 관점으로 심화 발전시킨 연구
