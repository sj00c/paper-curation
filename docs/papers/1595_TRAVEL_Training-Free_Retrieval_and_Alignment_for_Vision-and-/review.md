---
title: "1595_TRAVEL_Training-Free_Retrieval_and_Alignment_for_Vision-and-"
authors:
  - "Navid Rajabi"
  - "Jana Kosecka"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-Language Navigation 문제를 LLM과 VLM을 활용한 모듈식 접근으로 해결하며, 자연어 지시에서 landmark를 추출하고 topological map에서 경로를 검색하여 dynamic programming으로 정렬 점수를 계산한다."
tags:
  - "cat/Visual_Language_Navigation"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Graph-Based_Visual_Navigation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Rajabi and Kosecka_2025_TRAVEL Training-Free Retrieval and Alignment for Vision-and-Language Navigation.pdf"
---

# TRAVEL: Training-Free Retrieval and Alignment for Vision-and-Language Navigation

> **저자**: Navid Rajabi, Jana Kosecka | **날짜**: 2025-02-11 | **URL**: [https://arxiv.org/abs/2502.07306](https://arxiv.org/abs/2502.07306)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Topological Map Construction*

Vision-Language Navigation 문제를 LLM과 VLM을 활용한 모듈식 접근으로 해결하며, 자연어 지시에서 landmark를 추출하고 topological map에서 경로를 검색하여 dynamic programming으로 정렬 점수를 계산한다.

## Motivation

- **Known**: End-to-end sequence-to-sequence 방식이 VLN에서 주로 사용되었으나 landmark grounding과 spatial relationship 이해에 한계가 있으며, 최근 CLIP-Nav와 VLMaps 등의 모듈식 접근이 제안되었다.
- **Gap**: 기존 모듈식 방법들은 단순한 지시만을 처리하거나 작은 규모 데이터셋에서만 평가되었으며, R2R-Habitat과 같은 복잡한 지시에 대한 체계적인 성능 분석이 부족하다.
- **Why**: VLN은 자율주행과 로봇 네비게이션에 필수적인 과제이며, 모듈식 접근은 학습 없이 최신 기초모델을 활용하여 확장성과 해석 가능성을 제공할 수 있다.
- **Approach**: 자연어 지시에서 LLama-3.1을 사용하여 landmark를 추출하고, SigLIP으로 최종 landmark 위치를 인식한 후, topological map에서 top-k 경로 가설을 생성하며, dynamic programming으로 panorama 시퀀스와 landmark 시퀀스 간의 정렬 점수를 계산한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3. SigLIP vs. VLMaps Query Result for Last Landmark Indexing*

- **VLMaps 대비 성능 우위**: R2R-Habitat 데이터셋에서 occupancy map 기반 접근 대비 우수한 성능을 달성하였다.
- **Training-free 방식**: 추가 학습 없이 사전 학습된 LLM과 VLM만으로 zero-shot 성능을 확보하였다.
- **Visual grounding 영향 분석**: 시각적 groundedness가 navigation 성능에 미치는 영향을 정량적으로 분석하고 제시하였다.
- **모듈식 설계의 투명성**: 각 sub-module의 기여도를 명확하게 구분하여 weakness와 strength를 체계적으로 파악하였다.

## How

![Figure 5](figures/fig5.webp)

*Figure 5. Sequence Alignment for Path Ranking (Pano2Land)*

- **LLM 기반 landmark 추출**: LLama-3.1-8B-Instruct를 프롬프트하여 자연어 지시에서 landmark 시퀀스와 방문 순서를 추출한다.
- **Topological map 구성**: 데이터셋의 모든 unique waypoint와 trajectory를 사용하여 각 노드가 360° 파노라마로 표현되는 그래프를 생성한다.
- **Goal landmark 인식**: SigLIP를 사용하여 최종 landmark와 파노라마 이미지 간의 cosine similarity를 계산하여 top-k 목표 노드를 검색한다.
- **Shortest path 생성**: topological map에서 시작 위치에서 최종 landmark의 top-k 위치까지 최단 경로 알고리즘으로 k개 경로 가설을 생성한다.
- **Dynamic programming 정렬**: 각 경로 가설의 파노라마 시퀀스와 landmark 이름 시퀀스 간의 정렬 점수를 VLM의 매치 점수를 비용으로 사용하여 동적 프로그래밍으로 계산한다.
- **경로 평가**: 최고 정렬 점수를 얻은 가설에 대해 nDTW 메트릭을 계산하여 경로의 충실도를 평가한다.

## Originality

- **LLM과 VLM의 체계적 통합**: 기존의 modular approach들과 달리 LLM으로 landmark를 구조화된 형태로 추출하고 VLM으로 각 landmark를 fine-grained하게 grounding하는 통합 프레임워크를 제시하였다.
- **Dynamic programming 기반 정렬**: 단순한 similarity 계산 대신 파노라마 시퀀스와 landmark 시퀀스의 optimal alignment를 찾는 동적 프로그래밍 접근으로 복잡한 지시 처리 능력을 향상시켰다.
- **Zero-shot 성능 달성**: 학습 없이 기존의 학습 기반 방법들을 능가하는 성능을 보임으로써 대규모 모델의 zero-shot 능력을 효과적으로 활용함을 입증하였다.
- **상세한 실패 분석**: LLM과 VLM의 landmark grounding 실패 사례를 정량적으로 분석하여 현재 기초모델의 한계를 구체적으로 제시하였다.

## Limitation & Further Study

- **환경 맵의 의존성**: 알려진 topological map의 존재를 가정하므로 미지의 환경에서의 적용 가능성이 제한된다.
- **Landmark 추출의 한계**: 복잡하거나 모호한 landmark 표현에 대한 LLM의 추출 정확도 한계가 성능을 직접 제약한다.
- **Spatial clause 처리 부족**: 기존 modular approach와 마찬가지로 'before
- after' 등의 temporal/spatial constraint를 충분히 처리하지 못한다.", '**Top-k 경로의 계산 비용**: top-k 가설 생성과 alignment 계산의 computational complexity가 실시간 네비게이션에서 병목이 될 수 있다.
- **단일 최종 landmark 가정**: 여러 목표점이나 반복되는 landmark를 포함한 복잡한 지시 처리에 미적절하다.
- **후속 연구**: (1) 미지 환경에서 온라인 map 구축 및 navigation의 통합, (2) LLM의 landmark 추출 정확도 향상을 위한 few-shot prompting 기법, (3) spatial/temporal constraint를 명시적으로 modeling하는 constraint satisfaction 접근

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 LLM과 VLM을 체계적으로 결합한 modular VLN 접근법으로 training-free 학습이 가능함을 보이며, 복잡한 R2R-Habitat 지시셋에서 기존 방법 대비 우수한 성능을 달성한다. 다만 알려진 맵의 존재 가정과 spatial constraint 처리의 한계는 실제 환경 적용에 있어 개선이 필요하다.

## Related Papers

- 🏛 기반 연구: [[papers/1402_GC-VLN_Instruction_as_Graph_Constraints_for_Training-free_Vi/review]] — graph constraint 기반 training-free VLN의 기반이 되는 그래프 제약 활용 연구입니다.
- 🔗 후속 연구: [[papers/1432_Improving_Vision-and-Language_Navigation_with_Image-Text_Pai/review]] — image-text 페어링을 topological map과 결합한 vision-language navigation의 확장입니다.
- 🔄 다른 접근: [[papers/1441_JanusVLN_Decoupling_Semantics_and_Spatiality_with_Dual_Impli/review]] — VLN에서 서로 다른 모듈식 접근법 - retrieval-alignment vs dual implementation입니다.
- 🔄 다른 접근: [[papers/1443_L3MVN_Leveraging_Large_Language_Models_for_Visual_Target_Nav/review]] — L3MVN은 TRAVEL과 유사하게 대규모 언어 모델을 시각적 네비게이션에 활용하지만 다른 접근 방식을 제시한다.
- 🔄 다른 접근: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — NaVid는 TRAVEL과 같은 VLN 문제를 비디오 기반 VLM으로 해결하는 다른 접근법을 제공한다.
- 🔄 다른 접근: [[papers/1470_MapNav_A_Novel_Memory_Representation_via_Annotated_Semantic/review]] — MapNav는 TRAVEL의 topological map 기반 접근법과 유사하게 주석이 달린 의미론적 지도를 활용한 네비게이션을 제시한다.
- 🔄 다른 접근: [[papers/1575_SmartWay_Enhanced_Waypoint_Prediction_and_Backtracking_for_Z/review]] — SmartWay는 TRAVEL의 경로 검색과 유사한 waypoint 예측과 backtracking을 통한 향상된 네비게이션을 제공한다.
- 🏛 기반 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Code as Policies의 언어 모델 프로그래밍 패러다임이 TRAVEL의 LLM/VLM 기반 모듈식 접근법의 이론적 기반을 제공한다.
- 🧪 응용 사례: [[papers/1561_SayPlan_Grounding_Large_Language_Models_using_3D_Scene_Graph/review]] — SayPlan의 3D scene graph grounding이 TRAVEL의 landmark 추출과 topological map 구축을 더욱 정밀하게 만들 수 있다.
- 🏛 기반 연구: [[papers/1402_GC-VLN_Instruction_as_Graph_Constraints_for_Training-free_Vi/review]] — TRAVEL의 training-free retrieval 개념을 그래프 제약 최적화로 확장한 발전된 형태이다.
- 🔄 다른 접근: [[papers/1432_Improving_Vision-and-Language_Navigation_with_Image-Text_Pai/review]] — 둘 다 vision-language navigation이지만 VLN-BERT는 사전학습에, TRAVEL은 training-free 접근에 집중한다.
- 🏛 기반 연구: [[papers/1470_MapNav_A_Novel_Memory_Representation_via_Annotated_Semantic/review]] — training-free VLN 접근법의 기초 연구로서 MapNav의 효율적인 메모리 표현 설계에 이론적 토대를 제공한다.
- 🔄 다른 접근: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — VLN에서 video-based VLM vs training-free retrieval and alignment라는 서로 다른 시각적 정보 처리 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1342_CorrectNav_Self-Correction_Flywheel_Empowers_Vision-Language/review]] — retrieval and alignment 개념이 self-correction flywheel의 오류 복구 메커니즘 설계에 핵심 기반 제공
