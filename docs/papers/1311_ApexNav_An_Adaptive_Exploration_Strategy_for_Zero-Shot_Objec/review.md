---
title: "1311_ApexNav_An_Adaptive_Exploration_Strategy_for_Zero-Shot_Objec"
authors:
  - "Mingjie Zhang"
  - "Yuheng Du"
  - "Chengkai Wu"
  - "Jinni Zhou"
  - "Zhenchao Qi"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "ApexNav는 의미론적 정보의 환경 분포를 분석하여 강한 의미론적 신호가 있을 때는 의미 기반 탐색을, 약할 때는 기하학 기반 탐색으로 적응적으로 전환하고, target-centric semantic fusion을 통해 노이즈가 있는 탐지에도 강건한 zero-shot object navigation 프레임워크이다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Visual_Language_Navigation"
  - "sub/Semantic_Navigation_Exploration"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_ApexNav An Adaptive Exploration Strategy for Zero-Shot Object Navigation with Target-centric Semant.pdf"
---

# ApexNav: An Adaptive Exploration Strategy for Zero-Shot Object Navigation with Target-centric Semantic Fusion

> **저자**: Mingjie Zhang, Yuheng Du, Chengkai Wu, Jinni Zhou, Zhenchao Qi, Jun Ma, Boyu Zhou | **날짜**: 2025-04-20 | **URL**: [https://arxiv.org/abs/2504.14478](https://arxiv.org/abs/2504.14478)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: System Architecture of ApexNav. Before the episode, an LLM offline generates a similar object list. The agent bu*

ApexNav는 의미론적 정보의 환경 분포를 분석하여 강한 의미론적 신호가 있을 때는 의미 기반 탐색을, 약할 때는 기하학 기반 탐색으로 적응적으로 전환하고, target-centric semantic fusion을 통해 노이즈가 있는 탐지에도 강건한 zero-shot object navigation 프레임워크이다.

## Motivation

- **Known**: Object goal navigation은 미지의 환경에서 목표 객체를 찾아가는 문제로, LLM과 VLM을 활용한 zero-shot 방법들이 등장했다. 그러나 기존 방법들은 의미론적 단서에 과도하게 의존하거나 단일 프레임 탐지에 기반한 신뢰도 낮은 목표 식별의 문제를 가지고 있다.
- **Gap**: 의미론적 신호가 약한 환경에서 의미 기반 탐색은 비효율적이며, max-confidence fusion 기반 접근은 높은 신뢰도의 오탐지에 취약하다. 또한 기존 방법들은 의미론적 신호의 분포를 고려하지 않고 고정된 또는 탐욕적 전략을 사용한다.
- **Why**: Object navigation의 효율성과 신뢰도는 로봇 자동화와 구조 및 수색 로봇 분야에서 실제 적용을 위해 매우 중요하며, 실환경에서의 노이즈와 occlusion에 강건한 방법이 필요하다.
- **Approach**: 환경의 의미론적 분포를 분석하여 탐색 전략을 적응적으로 전환하는 적응형 탐색 전략과, 다중 프레임 관측을 맥락 인식 신뢰도 가중치로 통합하는 target-centric semantic fusion 방법을 제안한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Real-world Demonstration of ApexNav. We test ApexNav on various*

- **적응형 탐색 전략**: 의미론적 신호가 강할 때와 약할 때를 구분하여 의미 기반 탐색과 기하학 기반 탐색을 동적으로 전환하고, frontier 선택을 Traveling Salesman Problem으로 모델링하여 탐욕적 선택의 한계를 극복
- **Target-centric semantic fusion**: 목표 객체와 유사 객체의 장기 메모리를 유지하면서 다중 프레임 관측을 맥락 인식 신뢰도 가중치로 통합하여 노이즈가 있는 탐지에도 강건한 목표 식별 가능
- **벤치마크 성능**: HM3Dv1에서 SR 5.5%, SPL 8.6% 상대 개선, HM3Dv2에서 SR 19.8%, SPL 16.9% 상대 개선으로 state-of-the-art 달성
- **실환경 검증**: 다양한 실제 환경에서의 실험으로 실용성 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: System Architecture of ApexNav. Before the episode, an LLM offline generates a similar object list. The agent bu*

- Frontier map을 2D probabilistic grid에서 raycasting으로 구성하고 PCA 클러스터링으로 단순화
- Semantic score map을 BLIP-2 VLM의 image-text matching 유사도로 구성
- LLM을 사용하여 오프라인에서 target 객체와 유사 객체 리스트 생성
- 의미론적 신호 분포를 분석하여 의미 기반과 기하학 기반 탐색 모드 전환
- Target-centric fusion에서 다중 프레임 탐지 결과를 맥락 인식 신뢰도로 가중합
- 안전 waypoint navigation 모듈로 선택된 waypoint에 대한 action evaluation 기반 이동 수행

## Originality

- 환경의 의미론적 분포를 분석하여 탐색 전략을 적응적으로 전환하는 아이디어는 인간의 탐색 행동을 모델링한 새로운 접근
- Target-centric semantic fusion은 유사 객체까지 고려한 다중 프레임 통합 방식으로, 기존의 max-confidence fusion보다 더 정교한 노이즈 처리
- Frontier 선택을 TSP로 모델링하여 기존의 greedy 기반 frontier 선택의 한계 극복
- Zero-shot ObjectNav에서 의미론적 신호와 기하학적 정보의 효율적 트레이드오프를 체계적으로 다룬 첫 시도

## Limitation & Further Study

- 적응형 탐색의 의미론적 신호 분포 분석 기준이 명확하지 않으며, 전환 임계값의 설정이 환경에 따라 민감할 수 있음
- BLIP-2 VLM에 의존하므로 VLM의 성능 한계가 직접적으로 영향을 미침
- TSP 기반 frontier 순서 결정의 계산 복잡도가 frontier 수에 따라 증가할 수 있음
- 실환경 실험이 제한적이며, 극도로 복잡한 환경이나 매우 유사한 외관의 객체들이 많은 환경에서의 성능은 미평가
- 후속 연구에서는 적응형 전환의 자동 학습, 경량화된 fusion 알고리즘, 다양한 환경에서의 실증적 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ApexNav는 의미론적 신호와 기하학적 정보의 효율적 트레이드오프를 통해 zero-shot object navigation의 효율성과 신뢰도를 모두 향상시킨 우수한 연구이다. 실환경 검증과 강력한 벤치마크 성능, 체계적인 ablation study를 통해 각 컴포넌트의 효과를 명확히 입증했으나, 적응형 전환 기준의 명확화와 더 광범위한 실환경 실험이 필요하다.

## Related Papers

- 🔗 후속 연구: [[papers/1600_UniGoal_Towards_Universal_Zero-shot_Goal-oriented_Navigation/review]] — adaptive exploration을 zero-shot navigation에서 universal goal-oriented navigation으로 확장한 발전된 연구
- 🧪 응용 사례: [[papers/1507_OpenBench_A_New_Benchmark_and_Baseline_for_Semantic_Navigati/review]] — ApexNav의 의미론적 적응 탐색 전략을 평가할 수 있는 새로운 semantic navigation 벤치마크
- 🔄 다른 접근: [[papers/1319_BeliefMapNav_3D_Voxel-Based_Belief_Map_for_Zero-Shot_Object/review]] — 둘 다 zero-shot object navigation을 다루지만 ApexNav는 의미-기하학 적응적 탐색을, BeliefMapNav는 3D voxel belief map을 사용하는 다른 접근법입니다.
- 🔗 후속 연구: [[papers/1497_OctoNav_Towards_Generalist_Embodied_Navigation/review]] — ApexNav의 적응적 탐색 전략은 OctoNav의 일반화된 embodied navigation 프레임워크에서 활용될 수 있는 핵심 기술입니다.
- 🔗 후속 연구: [[papers/1319_BeliefMapNav_3D_Voxel-Based_Belief_Map_for_Zero-Shot_Object/review]] — ApexNav의 zero-shot 탐색 전략을 3D belief map과 LLM 추론으로 발전시킨 고도화된 접근법입니다.
- 🔗 후속 연구: [[papers/1396_ForesightNav_Learning_Scene_Imagination_for_Efficient_Explor/review]] — zero-shot object navigation의 적응형 탐색을 scene imagination으로 더욱 발전시킨 형태이다.
- 🔄 다른 접근: [[papers/1463_LOVON_Legged_Open-Vocabulary_Object_Navigator/review]] — 동일한 open-vocabulary 객체 네비게이션 문제에 대해 legged robot vs wheeled robot 플랫폼에서의 서로 다른 구현 방식을 보여준다.
- 🔗 후속 연구: [[papers/1443_L3MVN_Leveraging_Large_Language_Models_for_Visual_Target_Nav/review]] — adaptive exploration을 LLM 기반 navigation과 결합하여 zero-shot 성능을 더욱 향상시킬 수 있다.
- 🧪 응용 사례: [[papers/1490_NavigateDiff_Visual_Predictors_are_Zero-Shot_Navigation_Assi/review]] — zero-shot navigation assistant의 개념을 adaptive exploration과 결합하여 미지 환경에서의 객체 네비게이션 성능을 향상시킨다.
- 🔄 다른 접근: [[papers/1497_OctoNav_Towards_Generalist_Embodied_Navigation/review]] — OctoNav의 Think-Before-Action과 달리 adaptive exploration strategy를 통한 zero-shot object navigation 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1568_Search-TTA_A_Multimodal_Test-Time_Adaptation_Framework_for_V/review]] — ApexNav가 zero-shot 객체 내비게이션에 중점을 두는 반면, Search-TTA는 멀티모달 센서 융합을 통한 시각 탐색 성능 향상에 초점을 맞춘다.
- 🔄 다른 접근: [[papers/1575_SmartWay_Enhanced_Waypoint_Prediction_and_Backtracking_for_Z/review]] — 둘 다 zero-shot object navigation을 다루지만 SmartWay는 waypoint prediction에, ApexNav는 adaptive exploration에 집중한다.
- 🔄 다른 접근: [[papers/1600_UniGoal_Towards_Universal_Zero-shot_Goal-oriented_Navigation/review]] — zero-shot object navigation에서 서로 다른 접근법 - unified framework vs adaptive exploration입니다.
- 🔗 후속 연구: [[papers/1345_CoWs_on_Pasture_Baselines_and_Benchmarks_for_Language-Driven/review]] — Zero-shot 객체 탐색에서 적응적 탐색 전략의 구체적 개선사항을 제시합니다.
