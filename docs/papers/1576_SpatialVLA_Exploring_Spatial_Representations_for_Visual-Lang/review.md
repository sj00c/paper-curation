---
title: "1576_SpatialVLA_Exploring_Spatial_Representations_for_Visual-Lang"
authors:
  - "Delin Qu"
  - "Haoming Song"
  - "Qizhi Chen"
  - "Yuanqi Yao"
  - "Xinyi Ye"
date: "2025.01"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇 조작을 위한 3D 공간 이해를 강화한 VLA 모델 SpatialVLA를 제안하며, Ego3D Position Encoding과 Adaptive Action Grids를 통해 이질적인 로봇 간 일반화 가능한 공간 표현을 학습한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Qu et al._2025_SpatialVLA Exploring Spatial Representations for Visual-Language-Action Model.pdf"
---

# SpatialVLA: Exploring Spatial Representations for Visual-Language-Action Model

> **저자**: Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, Xuelong Li | **날짜**: 2025-01-27 | **URL**: [https://arxiv.org/abs/2501.15830](https://arxiv.org/abs/2501.15830)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of SpatialVLA. Given an image observation ot and a task instruction L, the model processes the image*

로봇 조작을 위한 3D 공간 이해를 강화한 VLA 모델 SpatialVLA를 제안하며, Ego3D Position Encoding과 Adaptive Action Grids를 통해 이질적인 로봇 간 일반화 가능한 공간 표현을 학습한다.

## Motivation

- **Known**: 최근 Vision-Language-Action 모델들이 대규모 로봇 데이터셋으로 사전학습되어 다양한 로봇 조작 작업을 수행할 수 있으나, 기존 VLA 모델들은 2D 관찰에만 의존하고 3D 물리 환경에 대한 정확한 공간 이해가 부족하다.
- **Gap**: 이질적인 로봇 embodiment 간에 3D 공간 정렬이 이루어지지 않으며, 서로 다른 로봇의 행동 특성(자유도, 제어기, 작업공간)으로 인해 일반화 가능한 공간 행동 표현 학습이 어렵다.
- **Why**: 로봇 조작의 성공은 본질적으로 3D 공간 구조 이해에 달려있으며, 다양한 로봇 환경과 작업에 걸쳐 강력한 공간 지능을 갖춘 일반화 로봇 정책이 필요하다.
- **Approach**: Ego3D Position Encoding으로 2D 시각 특징에 3D 공간 정보를 주입하고, Adaptive Action Grids로 연속 로봇 행동을 적응적 이산화된 공간 격자로 표현하여 로봇 간 행동 공간을 통일한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: We present SpatialVLA, a spatial-enhanced vision-language-action model that is trained on 1.1 Million real robot*

- **대규모 사전학습**: 110만 개의 실제 로봇 에피소드로 사전학습되어 다양한 로봇 환경과 작업에 걸쳐 일반화 가능한 조작 정책 학습
- **우수한 Zero-shot 성능**: 사전학습된 모델이 직접 다양한 작업을 zero-shot으로 수행 가능하며 우수한 복잡 로봇 궤적 추론 능력 시연
- **효율적인 적응**: Adaptive Action Grids의 재이산화를 통해 새로운 로봇 환경에 효율적으로 미세조정 가능
- **빠른 추론 속도**: 토큰당 공간 행동으로 인한 감소된 토큰 수로 20 Hz 이상의 빠른 추론 속도 달성
- **우수한 일반화 능력**: 시점/텍스처/조명 변화, 보지 못한 객체, 보지 못한 로봇 환경, 공간 배치 변화 등 다양한 시나리오에서 뛰어난 in-distribution 일반화 및 out-of-distribution 적응 능력

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of SpatialVLA. Given an image observation ot and a task instruction L, the model processes the image*

- **Ego3D Position Encoding**: Egocentric 카메라 프레임에서 3D 위치 인코딩 도출으로 특정 로봇-카메라 캘리브레이션 불필요하고 다양한 로봇 embodiment에 보편 적용 가능
- **Adaptive Action Grids**: 전체 로봇 에피소드의 통계적 행동 분포에 따라 연속 7D 행동(Δ T, Δ R, G)을 3개의 공간 행동 토큰으로 이산화하고 이들에 대해 공간 행동 토큰 학습
- **Post-training 적응**: 새로운 로봇 환경의 Gaussian 분포로부터 행동 격자와 공간 임베딩을 적응적으로 재이산화하여 로봇 특화 공간 행동 학습
- **자동회귀 예측**: PaliGemma 2 기반 vision-language 모델에서 자동회귀 방식으로 공간 행동 토큰을 순차적으로 예측
- **Cross-embodiment 학습**: 1.1 Million의 다양한 로봇 에피소드로 다중 로봇 환경과 작업에 걸쳐 공간 정렬된 행동 표현 학습

## Originality

- **공간 표현의 체계적 설계**: Ego3D Position Encoding과 Adaptive Action Grids를 통해 관찰과 행동 양측에서 통합된 3D 공간 표현 제시로 기존 VLA 모델의 2D 한계 극복
- **로봇 무관 공간 정렬**: Egocentric 카메라 프레임 기반 접근으로 로봇 특화 캘리브레이션 없이 이질적 로봇 간 관찰 공간 정렬
- **적응적 행동 격자 재이산화**: 사전학습된 행동 격자를 새로운 로봇의 행동 분포에 따라 재이산화하는 유연한 적응 메커니즘 제안
- **대규모 Cross-embodiment 평가**: 24개의 실제 로봇 작업과 3개의 시뮬레이션 환경을 통한 광범위한 일반화 능력 검증

## Limitation & Further Study

- **카메라 의존성**: Ego3D Position Encoding이 egocentric 카메라 프레임에 의존하므로 카메라가 없는 로봇이나 다중 카메라 시스템에서의 적용 명확성 부족
- **이산화 해상도 제한**: Adaptive Action Grids의 이산화 해상도가 고정되어 매우 미세한 조작이 필요한 작업에서의 성능 제약 가능성
- **계산 효율성**: 110만 개 에피소드 사전학습에 필요한 계산 비용 상세 정보 부재
- **후속연구 방향**: 다중 모달리티 센서(힘 피드백, 촉각 정보) 통합, 더 복잡한 bimanual 조작, 동적 환경에서의 실시간 적응, 공간 표현의 이론적 분석 심화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 VLA 모델에 체계적인 3D 공간 이해를 도입하고 이질적 로봇 간 일반화를 달성한 중요한 기여를 제시하며, 광범위한 실험을 통해 제안 방법의 효과를 입증했으나, 카메라 의존성과 이산화 해상도 제약 등의 한계가 존재한다.

## Related Papers

- 🔗 후속 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — RT-1의 기본 로봇 제어에 3D 공간 이해 강화와 이질적 로봇 간 일반화 능력을 추가한 공간적으로 발전된 형태이다.
- 🔄 다른 접근: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — 로봇을 위한 3D 이해에서 SpatialVLA는 spatial representation에, 3D-VLA는 generative world model에 초점을 맞춘 다른 접근법이다.
- 🏛 기반 연구: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — VoxPoser의 3D value maps와 compositional manipulation 개념이 SpatialVLA의 3D 공간 표현 설계에 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1567_SE3-Equivariant_Robot_Learning_and_Control_A_Tutorial_Survey/review]] — SE(3)-Equivariant 학습의 수학적으로 엄밀한 3D 기하학적 표현이 SpatialVLA의 공간 이해 강화 방법론의 이론적 기초가 된다.
- 🔗 후속 연구: [[papers/1517_PointWorld_Scaling_3D_World_Models_for_In-The-Wild_Robotic_M/review]] — PointWorld의 3D world model 개념을 로봇 조작에 특화된 ego3D position encoding과 adaptive action grid로 확장했다.
- 🔄 다른 접근: [[papers/1419_H3DP_Triply-Hierarchical_Diffusion_Policy_for_Visuomotor_Lea/review]] — 둘 다 spatial representation을 VLA에 통합하지만 depth-aware layering vs explicit spatial reasoning이라는 다른 방법론을 사용한다.
- 🔗 후속 연구: [[papers/1438_InternVLA-M1_A_Spatially_Guided_Vision-Language-Action_Frame/review]] — 공간 표현을 VLA에 통합하는 InternVLA-M1의 접근법을 spatial representation으로 더 일반화했다.
- 🔗 후속 연구: [[papers/1487_Multimodal_Spatial_Language_Maps_for_Robot_Navigation_and_Ma/review]] — Multimodal Spatial Language Maps의 공간 표현 방법론이 SpatialVLA의 시각-언어-행동 모델에서 더 정교한 공간적 이해로 확장됩니다.
- 🔄 다른 접근: [[papers/1499_OmniVLA_An_Omni-Modal_Vision-Language-Action_Model_for_Robot/review]] — VLA 모델에서 omni-modal vs spatial representation의 다른 다양성 추구 방식
- 🧪 응용 사례: [[papers/1567_SE3-Equivariant_Robot_Learning_and_Control_A_Tutorial_Survey/review]] — SpatialVLA는 SE(3) equivariance 개념을 VLA 모델의 공간 표현에 적용하여 조작 성능을 향상시킨다.
- 🔗 후속 연구: [[papers/1589_TopV-Nav_Unlocking_the_Top-View_Spatial_Reasoning_Potential/review]] — TopV-Nav의 top-view spatial reasoning이 SpatialVLA의 spatial representation 탐구와 결합되어 더 강력한 공간 이해 능력을 제공한다.
- 🧪 응용 사례: [[papers/1383_EmbSpatial-Bench_Benchmarking_Spatial_Understanding_for_Embo/review]] — SpatialVLA는 EmbSpatial-Bench에서 평가하는 공간 이해 능력을 VLA 모델에 직접 통합하는 구체적인 적용 사례입니다.
