---
title: "1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan"
authors:
  - "Jiazhao Zhang"
  - "Kunyu Wang"
  - "Rongtao Xu"
  - "Gengze Zhou"
  - "Yicong Hong"
date: "2024.02"
doi: ""
arxiv: ""
score: 4.0
essence: "NaVid는 비디오 기반 대규모 VLM을 활용하여 시각-언어 네비게이션에서 RGB 카메라 입력만으로 로봇의 다음 행동을 계획하는 첫 시도이며, 지도나 깊이 정보 없이 시뮬레이션과 실제 환경 모두에서 최고 성능을 달성한다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Visual_Language_Navigation"
  - "sub/Multimodal_Navigation_Systems"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2024_NaVid Video-based VLM Plans the Next Step for Vision-and-Language Navigation.pdf"
---

# NaVid: Video-based VLM Plans the Next Step for Vision-and-Language Navigation

> **저자**: Jiazhao Zhang, Kunyu Wang, Rongtao Xu, Gengze Zhou, Yicong Hong, Xiaomeng Fang, Qi Wu, Zhizheng Zhang, He Wang | **날짜**: 2024-02-24 | **URL**: [https://arxiv.org/abs/2402.15852](https://arxiv.org/abs/2402.15852)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: The overview of NaVid. The inputs of NaVid consist of the RGB frames from the online video observation {x0, · · *

NaVid는 비디오 기반 대규모 VLM을 활용하여 시각-언어 네비게이션에서 RGB 카메라 입력만으로 로봇의 다음 행동을 계획하는 첫 시도이며, 지도나 깊이 정보 없이 시뮬레이션과 실제 환경 모두에서 최고 성능을 달성한다.

## Motivation

- **Known**: VLN은 자율 구현 AI의 핵심 과제로, 기존 방법들은 이산 환경에서 주로 연구되었거나 RGBD, 오도메터, 지도 등 다양한 입력을 필요로 한다. 최근 대규모 VLM의 발전으로 다양한 AI 분야에서 뛰어난 일반화 성능을 보였다.
- **Gap**: 기존 VLN 방법들은 오도메터 노이즈, 깊이 인식의 도메인 갭, Sim-to-Real 전이에서의 문제가 있으며, 이산 환경 또는 텍스트 기반 관찰 인코딩으로 제한된다. 연속 환경에서 RGB만으로 end-to-end 네비게이션을 수행하는 실용적인 VLA 모델이 부재하다.
- **Why**: 대규모 VLM은 웹 규모 사전 학습을 통해 강력한 일반화 능력을 입증했으며, VLN의 Sim-to-Real 전이와 도메인 일반화는 실제 로봇 배포에 필수적인 문제이다.
- **Approach**: NaVida는 사전 학습된 vision encoder와 LLM을 결합하여 비디오 형태의 로봇 관찰을 instruction-queried token과 instruction-agnostic token으로 인코딩한다. 510k 네비게이션 샘플과 763k 웹 데이터로 학습하여 연속 환경에서 low-level executable action을 직접 추론한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: (a) Success Rate of NaVid on different steps during*

- **VLN-CE 벤치마크 성능**: R2R-CE 데이터셋에서 최고 수준의 성능 달성
- **크로스 데이터셋 일반화**: R2R-RxR 평가에서 큰 성능 향상 시연
- **Sim-to-Real 강건성**: RGB 입력만으로 4개 다양한 실내 장면에서 200개 명령어에 대해 약 66% 성공률 달성
- **단순화된 입력**: 지도, 오도메터, 깊이 정보 없이 모노큘러 RGB 비디오만 필요
- **시공간 컨텍스트 인코딩**: 비디오 기반 모델링으로 로봇의 역사적 궤적을 효과적으로 인코딩

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: The overview of NaVid. The inputs of NaVid consist of the RGB frames from the online video observation {x0, · · *

- Vision encoder를 사용하여 RGB 프레임에서 instruction-queried token(지시문 관련)과 instruction-agnostic token(전역 정보)의 두 종류 토큰 추출
- Cross-Modality Projector로 시각 토큰을 언어 공간으로 매핑
- BERT 기반 instruction identifier로 인스트럭션 처리
- Vicuna-7B LLM을 사전 학습된 상태에서 활용하여 네비게이션 추론
- Action 공간을 정량적 인자(이동 거리 cm, 회전 각도)를 포함한 언어 형태로 정의
- 역사 관찰과 현재 관찰의 토큰 수를 다르게 설정하여 적응적 컨텍스트 제공

## Originality

- 연속 환경에서 VLN을 위한 첫 번째 비디오 기반 VLM 제안으로, RGB만 사용한 end-to-end 네비게이션은 인간의 네비게이션 방식을 모방
- instruction-queried와 instruction-agnostic 토큰의 이중 인코딩 메커니즘으로 선택적 시각 특징 추출
- LLM 기반 VLN 방법 대비 더 현실적인 모델링으로 이산 공간이 아닌 연속 환경에서 저수준 실행 가능한 동작 직접 추론
- 오도메터, 깊이, 지도에 대한 의존성 제거로 Sim-to-Real 갭 자연스럽게 해결

## Limitation & Further Study

- 실제 환경 평가가 4개 장면으로 제한되어 더 광범위한 다양성 검증 필요
- 66% 성공률은 아직 실용적 배포에 완전히 충분하지 않으며, 실패 사례 분석 부재
- 비디오 기반 모델의 계산 복잡도와 추론 속도에 대한 논의 미흡
- 긴 지시문이나 복잡한 환경에서의 성능 한계 미분석
- 후속 연구로 더 많은 실제 환경 데이터, 다중 모드 입력 조합, 동적 장애물 처리 등이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: NaVid는 VLM의 강력한 일반화 능력을 VLN에 성공적으로 적용한 혁신적 연구로, RGB만으로 연속 환경에서 실제 로봇 네비게이션을 수행하는 첫 실용적 VLA 모델이다. Sim-to-Real 전이의 오랜 문제를 우아하게 해결하고 우수한 크로스 데이터셋 일반화를 보여준다.

## Related Papers

- 🏛 기반 연구: [[papers/1604_Video_Language_Planning/review]] — video language planning의 기본 이론을 제공하여 NaVid의 비디오 기반 VLM을 활용한 네비게이션 계획 수립에 필수적인 방법론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1595_TRAVEL_Training-Free_Retrieval_and_Alignment_for_Vision-and-/review]] — VLN에서 video-based VLM vs training-free retrieval and alignment라는 서로 다른 시각적 정보 처리 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1589_TopV-Nav_Unlocking_the_Top-View_Spatial_Reasoning_Potential/review]] — top-view spatial reasoning을 video-based VLM과 결합하여 더 강력한 공간 이해 능력을 갖춘 네비게이션 시스템을 구축한다.
- 🔄 다른 접근: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — 기존 시각-언어 네비게이션 연구들과 달리 NaVid는 비디오 기반 VLM으로 지도나 깊이 없이 네비게이션을 수행한다.
- 🏛 기반 연구: [[papers/1603_V-JEPA_2_Self-Supervised_Video_Models_Enable_Understanding_P/review]] — NaVid의 비디오 기반 VLM 접근법이 V-JEPA 2의 자기지도 비디오 모델의 이해 능력을 로봇 네비게이션에 활용하는 기초를 제공합니다.
- 🔗 후속 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — NaVid의 비디오 기반 행동 계획이 대규모 비디오 생성형 사전학습의 시각-운동 정책으로 확장되어 더 강력한 네비게이션 능력을 달성할 수 있습니다.
- 🔄 다른 접근: [[papers/1319_BeliefMapNav_3D_Voxel-Based_Belief_Map_for_Zero-Shot_Object/review]] — Zero-shot 객체 네비게이션에서 3D voxel belief map과 비디오 기반 VLM 계획이 다른 접근법을 제시합니다.
- 🔗 후속 연구: [[papers/1432_Improving_Vision-and-Language_Navigation_with_Image-Text_Pai/review]] — 이미지-텍스트 사전학습을 비디오 기반 VLM으로 확장하여 네비게이션의 다음 단계 계획을 가능하게 했다.
- 🔄 다른 접근: [[papers/1414_Ground_Slow_Move_Fast_A_Dual-System_Foundation_Model_for_Gen/review]] — NaVid의 video 기반 VLM planning과 다르게 dual-system으로 고수준 추론과 저수준 제어를 분리하는 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1470_MapNav_A_Novel_Memory_Representation_via_Annotated_Semantic/review]] — VLN에서 annotated semantic map vs video 기반 예측의 다른 메모리 표현 방식
- 🔗 후속 연구: [[papers/1486_Multimodal_Perception_for_Goal-oriented_Navigation_A_Survey/review]] — 멀티모달 네비게이션 서베이의 inference domain 관점이 NaVid의 비디오 기반 VLM 계획과 결합되어 더 정교한 네비게이션 추론을 가능하게 한다.
- 🔗 후속 연구: [[papers/1490_NavigateDiff_Visual_Predictors_are_Zero-Shot_Navigation_Assi/review]] — video-based VLM을 활용한 navigation planning과 NavigateDiff의 visual prediction 방법을 결합하면 더 강력한 navigation 시스템을 구축할 수 있다.
- 🔄 다른 접근: [[papers/1507_OpenBench_A_New_Benchmark_and_Baseline_for_Semantic_Navigati/review]] — OpenBench의 스마트 로지스틱스 접근법과 NaVid의 video-based VLM navigation은 다른 센서 모달리티로 동일한 navigation 문제를 해결한다.
- 🔗 후속 연구: [[papers/1508_Openfly_A_comprehensive_platform_for_aerial_vision-language/review]] — 항공 VLN 플랫폼은 NaVid의 비디오 기반 VLM 계획과 결합하여 더 정교한 항공 네비게이션을 구현할 수 있습니다.
- 🔗 후속 연구: [[papers/1575_SmartWay_Enhanced_Waypoint_Prediction_and_Backtracking_for_Z/review]] — VLM을 활용한 waypoint 예측을 video 기반 다음 단계 계획으로 확장할 수 있습니다.
- 🔄 다른 접근: [[papers/1549_RoboTron-Nav_A_Unified_Framework_for_Embodied_Navigation_Int/review]] — vision-language navigation에서 RoboTron-Nav는 통합 프레임워크로, NaVid는 VLM 기반 단계별 계획으로 접근한다.
- 🔄 다른 접근: [[papers/1595_TRAVEL_Training-Free_Retrieval_and_Alignment_for_Vision-and-/review]] — NaVid는 TRAVEL과 같은 VLN 문제를 비디오 기반 VLM으로 해결하는 다른 접근법을 제공한다.
- 🔗 후속 연구: [[papers/1630_WMNav_Integrating_Vision-Language_Models_into_World_Models_f/review]] — NaVid의 비디오 기반 VLM 내비게이션을 world model과 메모리 구조를 통합하여 더 강건한 navigation 시스템으로 발전시켰다.
- 🔗 후속 연구: [[papers/1604_Video_Language_Planning/review]] — NaVid는 Video Language Planning의 비디오 기반 계획 생성을 네비게이션 도메인으로 특화하여 발전시킨 접근법입니다.
- 🧪 응용 사례: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — NaVid는 VLN 서베이가 다루는 vision-language navigation의 비디오 기반 구체적 구현 사례다.
- 🔄 다른 접근: [[papers/1326_CANVAS_Commonsense-Aware_Navigation_System_for_Intuitive_Hum/review]] — 상식 인식 네비게이션에서 스케치/텍스트 다중모드 입력과 비디오 기반 VLM 계획이 다른 접근법을 제시합니다.
- 🔄 다른 접근: [[papers/1329_CityNavAgent_Aerial_Vision-and-Language_Navigation_with_Hier/review]] — 둘 다 vision-language navigation이지만 CityNavAgent는 aerial 환경에서 LLM 기반으로, NaVid는 지상에서 VLM 기반으로 접근합니다.
- 🔗 후속 연구: [[papers/1378_Embodied_Navigation_Foundation_Model/review]] — NaVid의 비디오 기반 VLM 계획이 NavFoM의 foundation model을 실시간 네비게이션으로 확장하는 방법을 제시합니다.
- 🔗 후속 연구: [[papers/1300_A_Survey_on_Vision-Language-Action_Models_for_Autonomous_Dri/review]] — VLM 기반 네비게이션 계획을 자율주행에 확장 적용한다.
- 🔄 다른 접근: [[papers/1303_Advances_in_Embodied_Navigation_Using_Large_Language_Models/review]] — 비디오 기반 VLM을 활용한 다른 네비게이션 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1342_CorrectNav_Self-Correction_Flywheel_Empowers_Vision-Language/review]] — self-correction 대신 video 기반 VLM을 활용한 다른 navigation 성능 향상 방법론
