---
title: "1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model"
authors:
  - "Haoyu Zhen"
  - "Xiaowen Qiu"
  - "Peihao Chen"
  - "Jincheng Yang"
  - "Xin Yan"
date: "2024.03"
doi: ""
arxiv: ""
score: 4.0
essence: "3D-VLA는 3D 인식, 추론, 행동을 생성형 월드 모델로 통합하는 embodied foundation model이며, 3D LLM 위에 interaction token과 diffusion model을 결합하여 로봇의 목표 이미지/포인트 클라우드 생성과 행동 예측을 수행한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Visual_Language_Navigation"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhen et al._2024_3D-VLA A 3D Vision-Language-Action Generative World Model.pdf"
---

# 3D-VLA: A 3D Vision-Language-Action Generative World Model

> **저자**: Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, Chuang Gan | **날짜**: 2024-03-14 | **URL**: [https://arxiv.org/abs/2403.09631](https://arxiv.org/abs/2403.09631)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of our 3D-VLA pipeline. The left part shows our goal-generation capability. Our model can imagine the*

3D-VLA는 3D 인식, 추론, 행동을 생성형 월드 모델로 통합하는 embodied foundation model이며, 3D LLM 위에 interaction token과 diffusion model을 결합하여 로봇의 목표 이미지/포인트 클라우드 생성과 행동 예측을 수행한다.

## Motivation

- **Known**: 2D 기반의 vision-language-action (VLA) 모델들(RT-2, PALM-E)과 3D 환경에서의 embodied foundation model들이 존재하지만, 이들은 직접적인 perception-to-action 매핑에만 초점을 두며 월드 다이나믹스를 간과한다.
- **Gap**: 기존 embodied 모델들은 2D 입력에 의존하여 3D 물리 세계와의 통합이 부족하며, 인간처럼 미래 상태를 상상하고 계획하는 월드 모델 능력이 없다. 또한 기존 embodied 데이터셋들은 3D 정보가 부족하다.
- **Why**: 로봇의 3D 공간 추론 능력이 '가장 먼 컵을 중간 서랍에 넣기'와 같은 복잡한 명령 수행에 필수적이며, 미래 상태 생성 능력은 더 나은 행동 계획을 가능하게 한다.
- **Approach**: 3D LLM 기반 아키텍처에 scene, object, action token을 도입하고, pretrain된 embodied diffusion model들을 projector를 통해 정렬하여 목표 이미지/포인트 클라우드 생성을 수행한다. 기존 로봇 데이터셋에서 2M의 3D-language-action 쌍을 추출한 대규모 instruction tuning 데이터셋을 구축한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Examples from our 3D Embodied Instruction Tuning Dataset.*

- **3D 기반 월드 모델**: 3D perception, reasoning, action을 unified 아키텍처로 통합하고 multimodal goal generation(RGB-D 이미지, depth, point cloud) 능력을 제공
- **대규모 3D embodied 데이터셋**: 2M의 3D-language-action 데이터 쌍으로 구성된 데이터셋 구축으로 기존 embodied 데이터셋의 3D 정보 부족 문제 해결
- **우수한 성능**: goal generation, goal-based planning, action prediction에서 baseline 모델들을 크게 능가하며, 전통적 언어 기반 task에서도 뛰어난 성능 달성
- **다양한 task 지원**: task captioning, action prediction, localization, multimodal goal generation, robot planning, embodied question answering 등 다양한 embodied task 수행

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of our 3D-VLA pipeline. The left part shows our goal-generation capability. Our model can imagine the*

- 3D LLM(Hong et al., 2023)을 기반으로 하여 scene, object, action 등의 interactive token을 LLM 어휘에 추가
- RGBD-to-RGBD와 point-to-point generation을 위한 embodied diffusion model을 사전학습
- projector를 통해 diffusion decoder와 LLM embedding space를 효율적으로 정렬하여 multimodal goal generation 수행
- 기존 로봇 데이터셋(실제 데이터, 합성 데이터, 인간-객체 상호작용)에서 depth estimator를 이용해 3D 정보 추출 및 point cloud로 변환
- ChatGPT 기반의 자동 파이프라인으로 3D 관련 주석과 언어 설명을 추출하여 2M의 instruction tuning 데이터셋 구축

## Originality

- 3D point cloud를 action token 생성에 활용한 최초의 VLA 모델로, 2D 기반 접근법 대비 3D 공간 이해도 혁신적 제고
- LLM과 diffusion model 사이의 projector 기반 정렬 메커니즘을 통해 multimodal goal generation과 action prediction을 unified 아키텍처로 통합
- 대규모 기존 embodied 데이터셋을 3D 정보로 풍부하게 하는 자동화된 데이터 처리 파이프라인 개발로 4M+ 3D 데이터 쌍 확보

## Limitation & Further Study

- 실제 로봇 환경에서의 성능 검증이 제시되지 않으며, held-in 데이터셋에서의 평가만 제공됨
- depth estimator를 통한 3D 정보 추출 과정에서 발생할 수 있는 오류의 누적 효과 미분석
- 생성된 goal image와 point cloud의 정량적 품질 평가 메트릭이 불명확함
- inference time과 computational cost에 대한 상세한 분석 부족
- 후속 연구로 sim-to-real 전이 학습, 실제 로봇 플랫폼에서의 end-to-end 검증, 다양한 embodiment에 대한 일반화 가능성 탐색 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 3D-VLA는 embodied AI의 새로운 패러다임을 제시하며, 3D 인식과 월드 모델 기반 행동 생성을 통합한 점에서 혁신적이다. 대규모 3D embodied 데이터셋 구축과 multimodal goal generation 능력은 로봇 조작 분야에 상당한 기여를 할 수 있으나, 실제 로봇 환경에서의 검증이 필요하다.

## Related Papers

- 🧪 응용 사례: [[papers/1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI/review]] — 3D-VLA는 World Models 서베이에서 제시된 3D spatial representation과 generative modeling 개념을 실제 로봇 시스템에 구현한 사례입니다.
- 🔄 다른 접근: [[papers/1288_3D_Diffusion_Policy_Generalizable_Visuomotor_Policy_Learning/review]] — 둘 다 3D 공간 정보를 활용한 로봇 정책 학습이지만 3D-VLA는 generative world model 접근법을 취합니다.
- 🏛 기반 연구: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — VoxPoser의 3D value map 개념이 3D-VLA의 3D 공간 표현과 행동 생성 메커니즘의 기초가 됩니다.
- 🏛 기반 연구: [[papers/1631_World_Models/review]] — 3D-VLA의 생성형 월드 모델링 접근법은 World Models의 기본 개념에서 출발하여 3D 공간 추론을 추가한 확장입니다.
- 🔄 다른 접근: [[papers/1360_Diffusion_Models_Are_Real-Time_Game_Engines/review]] — 같은 생성형 월드 모델 문제를 다루지만 3D-VLA는 로봇 행동에, Diffusion Models는 게임 환경에 초점을 맞춘 대안적 접근법입니다.
- 🔄 다른 접근: [[papers/1401_GauDP_Reinventing_Multi-Agent_Collaboration_through_Gaussian/review]] — 둘 다 3D 표현을 VLA에 활용하지만 Gaussian fields vs generative world model이라는 다른 접근법을 사용한다.
- 🔄 다른 접근: [[papers/1481_Motus_A_Unified_Latent_Action_World_Model/review]] — unified world model에서 latent action vs 3D vision-language-action의 다른 통합 방식
- 🔗 후속 연구: [[papers/1483_MuBlE_MuJoCo_and_Blender_simulation_Environment_and_Benchmar/review]] — MuBlE의 시각-물리 통합 환경은 3D-VLA와 같은 3D 비전-언어-액션 모델의 훈련에 활용될 수 있습니다.
- 🏛 기반 연구: [[papers/1517_PointWorld_Scaling_3D_World_Models_for_In-The-Wild_Robotic_M/review]] — 3D 포인트 플로우 기반 월드 모델은 3D-VLA의 3D 비전-언어-액션 생성 모델과 유사한 3D 표현을 공유합니다.
- 🏛 기반 연구: [[papers/1567_SE3-Equivariant_Robot_Learning_and_Control_A_Tutorial_Survey/review]] — 3D-VLA의 3D generative world model이 SE(3) equivariance의 로봇 학습 적용을 구체적으로 보여주는 실례다.
- 🔄 다른 접근: [[papers/1576_SpatialVLA_Exploring_Spatial_Representations_for_Visual-Lang/review]] — 로봇을 위한 3D 이해에서 SpatialVLA는 spatial representation에, 3D-VLA는 generative world model에 초점을 맞춘 다른 접근법이다.
- 🔗 후속 연구: [[papers/1559_RVT_Robotic_View_Transformer_for_3D_Object_Manipulation/review]] — 3D-VLA는 RVT의 3D 표현 아이디어를 확장하여 생성형 월드 모델과 결합한 접근법입니다.
- 🏛 기반 연구: [[papers/1593_TrackVLA_Unleashing_Reasoning_and_Memory_Capabilities_in_VLA/review]] — 3D-VLA의 3D 시각-언어-행동 생성 모델이 TrackVLA++의 공간적 추론 능력 개발의 기반이 되었다.
- 🔗 후속 연구: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — 3D 환경에서의 vision-language-action 통합을 통해 UniVLA의 unified token approach를 3차원 세계 모델로 확장합니다.
- 🔄 다른 접근: [[papers/1385_EO-1_An_Open_Unified_Embodied_Foundation_Model_for_General_R/review]] — 3D-VLA와 EO-1 모두 3D 시각 정보를 활용한 embodied foundation model이지만 world model 생성 방식이 다름
- 🔗 후속 연구: [[papers/1308_An_Embodied_Generalist_Agent_in_3D_World/review]] — 3D-VLA는 LEO의 3D embodied agent 개념을 generative world model로 발전시킨 후속 연구입니다.
