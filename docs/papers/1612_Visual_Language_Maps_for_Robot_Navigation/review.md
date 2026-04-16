---
title: "1612_Visual_Language_Maps_for_Robot_Navigation"
authors:
  - "Chenguang Huang"
  - "Oier Mees"
  - "Andy Zeng"
  - "Wolfram Burgard"
date: "2022.10"
doi: ""
arxiv: ""
score: 4.0
essence: "시각-언어 모델의 특징을 3D 재구성과 융합하여 공간 정보를 갖춘 의미론적 지도(VLMaps)를 구축하고, 이를 통해 로봇이 자연어 명령으로 공간 관계를 포함한 복잡한 네비게이션 작업을 수행할 수 있게 한다."
tags:
  - "cat/Visual_Language_Navigation"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Visual_Language_Mapping"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2022_Visual Language Maps for Robot Navigation.pdf"
---

# Visual Language Maps for Robot Navigation

> **저자**: Chenguang Huang, Oier Mees, Andy Zeng, Wolfram Burgard | **날짜**: 2022-10-11 | **URL**: [https://arxiv.org/abs/2210.05714](https://arxiv.org/abs/2210.05714)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: VLMaps is a spatial map representation in which pretrained visual-*

시각-언어 모델의 특징을 3D 재구성과 융합하여 공간 정보를 갖춘 의미론적 지도(VLMaps)를 구축하고, 이를 통해 로봇이 자연어 명령으로 공간 관계를 포함한 복잡한 네비게이션 작업을 수행할 수 있게 한다.

## Motivation

- **Known**: 시각-언어 모델(CLIP 등)은 인터넷 규모 데이터로 사전훈련되어 자연어와 이미지 매칭에 효과적이며, 기하학적 지도는 경로 계획에 공간 정밀도를 제공한다.
- **Gap**: 기존 VLM 기반 네비게이션 방법(CoW, LM-Nav)은 객체 중심의 목표에만 제한되며 '소파와 TV 사이'와 같은 공간 관계 표현을 이해하지 못하고, 서로 다른 로봇 형태 간에 지도를 공유할 수 없다.
- **Why**: 자연어로 표현된 공간 관계를 이해하고 로현할 수 있는 로봇 네비게이션은 인간 수준의 지시 따르기를 가능하게 하며, 다양한 로봇 플랫폼 간 지도 공유는 효율성을 크게 높인다.
- **Approach**: LSeg 같은 사전훈련된 VLM으로 RGB-D 비디오에서 픽셀 단위 임베딩을 추출하고, 깊이 정보와 시각 운동 정보를 이용해 이를 3D 지도로 역투영하여 공간-의미론적 지도를 구축한 뒤, LLM과 결합하여 자연어 명령을 공간 목표 시퀀스로 변환한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: VLMaps enables a robot to perform complex zero-shot spatial goal navigation tasks given natural language command*

- **VLMaps 구축**: 추가 라벨링 없이 사전훈련 VLM 특징과 3D 재구성을 융합한 공간 의미론적 지도 표현 개발
- **공간 관계 이해**: '소파와 TV 사이
- 의자 오른쪽 3미터' 같은 상대적 공간 표현을 자연어로 지역화 가능", '**다중 로봇 호환성**: 자연어 장애물 카테고리 목록으로 다양한 로봇 형태에 맞는 장애물 지도를 동적 생성
- **영점 학습 성능**: 추가 데이터 수집이나 모델 미세조정 없이 기존 방법보다 복잡한 자연어 지시를 따르는 능력 입증

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: System overview. A VLMap is created by fusing pretrained visual-language features into the reconstruction of the*

- RGB-D 카메라로부터 각 프레임의 깊이 픽셀을 역투영하여 로컬 포인트 클라우드 생성: Pk = D(u)K⁻¹ũ
- 시각 운동(visual odometry)을 이용한 카메라 포즈 변환으로 로컬 포인트 클라우드를 월드 좌표계로 변환: PW = TWkPk
- LSeg 시각 인코더로 RGB 이미지의 각 픽셀에 대해 CLIP 특징 공간의 밀집 임베딩 계산
- 3D 포인트 좌표를 탑-다운 그리드 지도로 투영하고, 각 그리드 셀에 시각-언어 임베딩을 누적
- 쿼리 텍스트와 그리드 셀 임베딩 간의 코사인 유사도를 계산하여 자연어 장소나 객체 지역화
- LLM을 Socratic 방식으로 활용하여 자연어 명령을 단계적 공간 목표로 분해, VLMap에서 직접 지역화

## Originality

- VLM 특징과 3D 기하학적 지도를 직접 융합하는 새로운 공간 표현 제안 — 기존 의미론적 SLAM은 사전정의된 클래스에 제한되었음
- 개방 어휘(open-vocabulary) 지도에서 공간 관계 쿼리를 지원하는 첫 접근 — CoW와 LM-Nav는 객체 중심 목표만 처리
- LLM과의 결합으로 자연어 명령을 공간 좌표로 변환하는 파이프라인 구현 — 기존에는 이미지-텍스트 매칭에만 사용
- 다양한 로봇 형태를 위한 동적 장애물 지도 생성 메커니즘 개발

## Limitation & Further Study

- LSeg에 의존하므로, 시각적으로 분명하지 않은 공간 개념('입구 근처' 등)은 정확도가 떨어질 수 있음", 'RGB-D 센서와 정확한 시각 운동 추정이 필요하므로, 센서 오류나 장기간 드리프트 영향 분석 부족
- 실험이 제한된 실내 환경과 시뮬레이션 환경에서만 수행되어 대규모 실외 환경 적용성 미검증
- LLM 프롬프팅 방식에 민감할 수 있으며, 복잡한 다단계 공간 추론의 한계에 대한 논의 필요
- 후속 연구: 불확실성 정량화, 장기간 지도 유지보수, 동적 환경 처리, 다중 센서 모달리티 통합

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VLMaps는 사전훈련 VLM과 3D 재구성을 창의적으로 통합하여 공간-의미론적 네비게이션이라는 중요한 문제를 해결하며, 광범위한 실험으로 기존 방법 대비 우월성을 입증한 우수한 연구이다. 다만 센서 정확도, 실외 환경, 동적 장애물 등에 대한 제약 논의가 추가되면 더욱 완성도 높을 것이다.

## Related Papers

- 🏛 기반 연구: [[papers/1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me/review]] — CLIP-Fields의 weakly supervised semantic field가 visual language map의 기반 기술입니다.
- 🔄 다른 접근: [[papers/1561_SayPlan_Grounding_Large_Language_Models_using_3D_Scene_Graph/review]] — 로봇 공간 이해를 위한 서로 다른 접근법 - visual language map vs 3D scene graph입니다.
- 🔗 후속 연구: [[papers/1487_Multimodal_Spatial_Language_Maps_for_Robot_Navigation_and_Ma/review]] — visual language map을 multimodal spatial language map으로 확장한 발전된 연구입니다.
- 🔄 다른 접근: [[papers/1456_LERF_Language_Embedded_Radiance_Fields/review]] — LERF는 VLMaps와 유사하게 언어를 3D 공간에 embedding하지만 radiance field 기반의 다른 접근법을 사용한다.
- 🧪 응용 사례: [[papers/1340_Context-Aware_Entity_Grounding_with_Open-Vocabulary_3D_Scene/review]] — Context-Aware Entity Grounding은 VLMaps가 구축한 3D semantic map에서 개체 grounding을 수행하는 구체적 응용이다.
- 🧪 응용 사례: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — VoxPoser의 composable 3D value maps가 VLMaps의 semantic mapping을 robotic manipulation 작업에 직접 활용할 수 있게 한다.
- 🏛 기반 연구: [[papers/1319_BeliefMapNav_3D_Voxel-Based_Belief_Map_for_Zero-Shot_Object/review]] — visual language map의 공간-언어 표현 개념이 3D voxel belief map 설계의 이론적 기반
- 🏛 기반 연구: [[papers/1382_EmbodiedVSR_Dynamic_Scene_Graph-Guided_Chain-of-Thought_Reas/review]] — Visual Language Maps의 공간-언어 매핑 개념을 동적 scene graph와 결합하여 embodied 추론으로 확장했다.
- 🏛 기반 연구: [[papers/1432_Improving_Vision-and-Language_Navigation_with_Image-Text_Pai/review]] — Visual Language Maps의 기본적인 vision-language navigation 개념을 웹 데이터 사전학습으로 확장한다.
- 🏛 기반 연구: [[papers/1461_LM-Nav_Robotic_Navigation_with_Large_Pre-Trained_Models_of_L/review]] — 시각적 언어 지도의 기본 개념이 LM-Nav의 언어 명령 기반 네비게이션에 적용되었다.
- 🔄 다른 접근: [[papers/1470_MapNav_A_Novel_Memory_Representation_via_Annotated_Semantic/review]] — Vision-Language Navigation에서 메모리 표현 방법으로 Annotated Semantic Map vs Visual Language Map이라는 서로 다른 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1441_JanusVLN_Decoupling_Semantics_and_Spatiality_with_Dual_Impli/review]] — JanusVLN이 Visual Language Maps의 공간-언어 매핑을 dual implicit memory로 발전시켜 더 효율적인 네비게이션을 실현한다.
- 🏛 기반 연구: [[papers/1443_L3MVN_Leveraging_Large_Language_Models_for_Visual_Target_Nav/review]] — visual language maps의 기본 개념을 LLM 기반 navigation 시스템에 통합하는 이론적 토대를 제공한다.
- 🔄 다른 접근: [[papers/1456_LERF_Language_Embedded_Radiance_Fields/review]] — 동일한 언어-공간 매핑 문제를 다른 접근법으로 해결한 대안적 방법
- 🔗 후속 연구: [[papers/1487_Multimodal_Spatial_Language_Maps_for_Robot_Navigation_and_Ma/review]] — Visual Language Maps를 확장하여 오디오 모달리티까지 포함한 AVLMaps로 다중모달 spatial grounding을 실현했다.
- 🏛 기반 연구: [[papers/1499_OmniVLA_An_Omni-Modal_Vision-Language-Action_Model_for_Robot/review]] — OmniVLA의 다중 모달리티 처리가 Visual Language Maps의 공간-언어 매핑 기술을 기반으로 확장된다.
- 🏛 기반 연구: [[papers/1505_Open-vocabulary_Queryable_Scene_Representations_for_Real_Wor/review]] — visual language map의 기본 개념과 구현 방법을 제공하여 NLMap의 open-vocabulary queryable scene representation 구축에 핵심적인 기술적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1507_OpenBench_A_New_Benchmark_and_Baseline_for_Semantic_Navigati/review]] — Visual Language Maps의 공간-언어 매핑 기술이 OpenBench의 OpenStreetMap과 VLM 결합 시스템의 이론적 기반이다.
- 🔗 후속 연구: [[papers/1549_RoboTron-Nav_A_Unified_Framework_for_Embodied_Navigation_Int/review]] — Visual Language Maps의 시각-언어 네비게이션 기술이 RoboTron-Nav의 3D-aware history sampling과 결합되어 더 효과적인 네비게이션을 구현한다.
- 🔄 다른 접근: [[papers/1561_SayPlan_Grounding_Large_Language_Models_using_3D_Scene_Graph/review]] — 시각-언어 지도 대신 3D Scene Graph를 활용한 다른 접근법으로 로봇 공간 이해를 개선합니다.
- 🏛 기반 연구: [[papers/1589_TopV-Nav_Unlocking_the_Top-View_Spatial_Reasoning_Potential/review]] — 로봇 네비게이션을 위한 시각-언어 지도의 기본 개념을 제공하여 TopV-Nav의 top-view 지도 추론에 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1630_WMNav_Integrating_Vision-Language_Models_into_World_Models_f/review]] — Visual Language Maps의 로봇 내비게이션 연구가 VLM 기반 world model을 사용한 Object Goal Navigation의 기반 기술이 되었다.
- 🏛 기반 연구: [[papers/1614_VL-Nav_A_Neuro-Symbolic_Approach_for_Reasoning-based_Vision-/review]] — vision-language navigation을 위한 visual language map의 기본 개념을 제공하여 VL-Nav의 추론 기반 네비게이션에 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1326_CANVAS_Commonsense-Aware_Navigation_System_for_Intuitive_Hum/review]] — Visual Language Maps의 로봇 네비게이션 기술은 CANVAS의 상식 기반 네비게이션 시스템에 공간 표현의 기반을 제공한다.
- 🔗 후속 연구: [[papers/1332_CLIP-Fields_Weakly_Supervised_Semantic_Fields_for_Robotic_Me/review]] — CLIP-Fields의 의미론적 공간 매핑 개념이 Visual Language Maps의 로봇 네비게이션 응용으로 확장된 형태입니다.
- 🧪 응용 사례: [[papers/1378_Embodied_Navigation_Foundation_Model/review]] — Visual Language Maps가 NavFoM의 크로스-태스크 네비게이션을 공간 표현과 결합한 구체적인 적용 방법을 제공합니다.
