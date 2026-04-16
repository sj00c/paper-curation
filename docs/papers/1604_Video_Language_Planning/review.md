---
title: "1604_Video_Language_Planning"
authors:
  - "Yilun Du"
  - "Mengjiao Yang"
  - "Pete Florence"
  - "Fei Xia"
  - "Ayzaan Wahid"
date: "2023.10"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-Language Model과 Text-to-Video Model을 결합하여 트리 서치를 통해 장기 수평선 로봇 작업을 위한 상세한 비디오 계획을 생성하는 Video Language Planning(VLP) 알고리즘을 제시한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Instruction-Following_Robot_Navigation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Du et al._2023_Video Language Planning.pdf"
---

# Video Language Planning

> **저자**: Yilun Du, Mengjiao Yang, Pete Florence, Fei Xia, Ayzaan Wahid, Brian Ichter, Pierre Sermanet, Tianhe Yu, Pieter Abbeel, Joshua B. Tenenbaum, Leslie Kaelbling, Andy Zeng, Jonathan Tompson | **날짜**: 2023-10-16 | **URL**: [https://arxiv.org/abs/2310.10625](https://arxiv.org/abs/2310.10625)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Video Language Planning uses forward tree search via vision-language models and text-to-video*

Vision-Language Model과 Text-to-Video Model을 결합하여 트리 서치를 통해 장기 수평선 로봇 작업을 위한 상세한 비디오 계획을 생성하는 Video Language Planning(VLP) 알고리즘을 제시한다.

## Motivation

- **Known**: LLM은 추상적인 텍스트 계획을 생성할 수 있지만 물리적 제약을 반영하기 어렵고, Text-to-Video Model은 객체의 동역학을 학습할 수 있지만 단기 비디오만 생성 가능하다.
- **Gap**: LLM의 고수준 추상화 능력과 Text-to-Video Model의 저수준 동역학 모델링을 통합하여 장기 수평선 작업을 계획하는 방법이 부재하다.
- **Why**: 로봇이 복잡한 다단계 조작 작업을 수행하기 위해서는 물리적으로 타당한 상세 계획이 필요하며, 이를 통해 실제 로봇 배포 시 성공률을 크게 향상시킬 수 있다.
- **Approach**: Vision-Language Model을 정책과 휴리스틱 함수로, Text-to-Video Model을 동역학 모델로 사용하여 트리 서치 절차를 구성하고, 생성된 비디오 계획을 Goal-Conditioned Policy로 실행 가능한 로봇 액션으로 변환한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Video Accuracy vs Planning Budget. Left: VLP scales positively with more compute budget; it is*

- **알고리즘 설계**: Vision-Language Model과 Text-to-Video Model을 synergistic하게 결합한 VLP 알고리즘으로 수백 프레임에 걸친 장기 비디오 계획 생성 가능
- **계산 효율성**: 계산 예산에 따라 성능이 확장되어 검색 깊이와 분기 인수를 증가시킬 수 있음
- **실무 검증**: 3개의 로봇 하드웨어 플랫폼에서 PaLM-E와 RT-2를 포함한 기존 방법들보다 현저히 높은 작업 완료율 달성
- **일반화 능력**: Internet-scale 데이터로 사전학습된 모델을 활용하여 새로운 객체와 구성에 대한 일반화 성능 입증

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Video Language Planning uses forward tree search via vision-language models and text-to-video*

- VLM 정책 πVLM(x, g)을 사용하여 현재 이미지와 목표에 조건화된 추상 텍스트 액션 생성
- Text-to-Video Model fVM(x, a)로 각 액션에 대한 단기 비디오 시퀀스 예측
- VLM 휴리스틱 함수 HVLM(x, g)로 각 예측 상태가 작업 완료에 얼마나 기여하는지 평가
- Forward Tree Search를 통해 가장 유망한 분기를 재귀적으로 확장
- 생성된 비디오 계획의 각 중간 프레임에 조건화된 Goal-Conditioned Policy로 저수준 제어 액션 추론

## Originality

- Vision-Language Model과 Text-to-Video Model의 상호보완적 특성을 처음으로 체계적으로 결합한 계획 알고리즘
- Text-to-Video Model을 동역학 모델로 사용하여 장기 계획에 적용한 혁신적인 접근
- 불완전한 언어 라벨이 있는 비디오 데이터로부터 학습할 수 있는 강점을 활용한 설계
- 비디오 계획과 Goal-Conditioned Policy의 통합을 통한 실제 로봇 배포 파이프라인 구축

## Limitation & Further Study

- Text-to-Video Model이 생성하는 비디오의 시각적 충실도 제한으로 인한 장기 계획의 오차 누적 가능성
- VLM의 정책과 휴리스틱 함수가 충분히 정확한 추상화를 제공해야 하는 의존성
- 계산 비용이 높아 실시간 계획 및 동적 환경에서의 적응성 제한
- 후속연구: 비디오 생성 모델의 장기 일관성 개선, 더 효율적인 트리 서치 알고리즘 개발, 부분 관측 환경에서의 적응 메커니즘

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 대규모 사전학습 모델의 상호보완적 강점을 영리하게 통합하여 실제 로봇 시스템에서 획기적인 성능 향상을 달성한 혁신적 연구이며, 계획 문제에 대한 현대적 재검토를 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — video foundation model이 video language planning의 text-to-video 생성 기반이 됩니다.
- 🔗 후속 연구: [[papers/1455_Learning_Universal_Policies_via_Text-Guided_Video_Generation/review]] — text-guided video generation을 로봇 작업의 상세한 계획 생성으로 확장한 응용입니다.
- 🔄 다른 접근: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — multi-stage 계획을 위한 서로 다른 접근법 - video planning vs reflective planning입니다.
- 🏛 기반 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — 대규모 비디오 생성 사전훈련 연구는 VLP의 text-to-video 모델 구성 요소에 대한 기술적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1407_Genie_Generative_Interactive_Environments/review]] — Genie는 VLP와 유사하게 생성 모델을 통한 환경 시뮬레이션을 제공하지만 대화형 환경 생성에 집중한다.
- 🔄 다른 접근: [[papers/1406_Genie_Envisioner_A_Unified_World_Foundation_Platform_for_Rob/review]] — Genie Envisioner는 VLP와 같은 생성 모델 기반 로봇 계획을 통합된 세계 기반 플랫폼으로 제공한다.
- 🔄 다른 접근: [[papers/1561_SayPlan_Grounding_Large_Language_Models_using_3D_Scene_Graph/review]] — Video Language Planning과 SayPlan은 장기 계획에서 비디오 vs 3D 장면 그래프라는 서로 다른 표현 방식을 사용합니다.
- 🔗 후속 연구: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — NaVid는 Video Language Planning의 비디오 기반 계획 생성을 네비게이션 도메인으로 특화하여 발전시킨 접근법입니다.
- 🔗 후속 연구: [[papers/1406_Genie_Envisioner_A_Unified_World_Foundation_Platform_for_Rob/review]] — Video Language Planning의 개념을 정책 학습, 평가, 시뮬레이션을 통합하는 플랫폼으로 확장했다.
- 🏛 기반 연구: [[papers/1455_Learning_Universal_Policies_via_Text-Guided_Video_Generation/review]] — Video Language Planning의 개념을 text-conditioned video generation으로 구체적으로 구현한 사례이다.
- 🏛 기반 연구: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — video language planning의 기본 이론을 제공하여 NaVid의 비디오 기반 VLM을 활용한 네비게이션 계획 수립에 필수적인 방법론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-2와 Video Language Planning은 모두 언어 지식을 로봇 제어에 활용하지만 end-to-end action과 planning 중심이라는 다른 접근을 보여준다.
- 🔄 다른 접근: [[papers/1561_SayPlan_Grounding_Large_Language_Models_using_3D_Scene_Graph/review]] — SayPlan과 Video Language Planning은 모두 장기 계획 생성에서 서로 다른 표현 방식(3DSG vs 비디오)을 사용합니다.
- 🔗 후속 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — video foundation model을 video language planning의 시뮬레이션 환경으로 활용할 수 있습니다.
