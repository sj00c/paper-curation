---
title: "1559_RVT_Robotic_View_Transformer_for_3D_Object_Manipulation"
authors:
  - "Ankit Goyal"
  - "Jie Xu"
  - "Yijie Guo"
  - "Valts Blukis"
  - "Yu-Wei Chao"
date: "2023.06"
doi: ""
arxiv: ""
score: 4.0
essence: "RVT는 3D 물체 조작을 위해 multi-view transformer를 사용하여 명시적 3D 표현의 계산 비용 문제를 해결하면서 높은 정확도와 확장성을 동시에 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Goyal et al._2023_RVT Robotic View Transformer for 3D Object Manipulation.pdf"
---

# RVT: Robotic View Transformer for 3D Object Manipulation

> **저자**: Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, Dieter Fox | **날짜**: 2023-06-26 | **URL**: [https://arxiv.org/abs/2306.14896](https://arxiv.org/abs/2306.14896)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of RVT. Given RGB-D from sensor(s), we first construct a point cloud of the*

RVT는 3D 물체 조작을 위해 multi-view transformer를 사용하여 명시적 3D 표현의 계산 비용 문제를 해결하면서 높은 정확도와 확장성을 동시에 달성한다.

## Motivation

- **Known**: 3D 물체 조작에서 voxel 기반의 명시적 3D 표현은 view 기반 방법보다 성능이 우수하지만, 계산 비용이 높아 확장성이 제한된다.
- **Gap**: 기존 voxel 기반 방법(PerAct)은 정확하지만 훈련 시간이 매우 길고(16일) 메모리 효율이 낮으며, view 기반 방법은 3D 추론 능력이 부족하다.
- **Why**: 로봇 조작의 실제 활용을 위해서는 높은 정확도와 함께 빠른 훈련 속도 및 배포 효율이 필수적이며, 이는 로봇 학습의 실용성을 크게 향상시킨다.
- **Approach**: RGB-D 입력으로부터 포인트 클라우드를 구성하고 로봇 workspace 주변의 가상 뷰로 재렌더링한 후, multi-view transformer의 attention 메커니즘을 이용하여 뷰 간 정보를 통합한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: RVT scales and performs better*

- **성능 향상**: RLBench의 18개 작업(249개 변형)에서 PerAct 대비 26% 상대적 성공률 향상 달성
- **훈련 효율성**: 동일 성능 달성 시 PerAct 대비 36배 빠른 훈련 속도(16일 → 10시간)
- **추론 속도**: 2.3배 빠른 추론 속도 달성(11.6 fps vs 4.9 fps)
- **다중 작업 일반화**: 단일 RVT 모델이 18개 RLBench 작업 모두에서 우수한 성능 발휘
- **실제 환경 적용**: 약 10개 데모만으로 실제 로봇에서 다양한 조작 작업 수행 가능(5개 작업, 13개 변형)

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of RVT. Given RGB-D from sensor(s), we first construct a point cloud of the*

- RGB-D 센서 입력으로부터 포인트 클라우드 생성
- 로봇 workspace 주변에 가상 카메라를 배치하여 최적의 뷰포인트(예: 테이블 위 직상방)에서 이미지 재렌더링
- 재렌더링된 다중 뷰 이미지를 transformer에 입력
- Transformer 내에서 패치 단위의 self-attention을 먼저 수행한 후 뷰 간 cross-attention 실행
- 뷰별 heatmap과 feature를 생성하여 3D 공간에서 로봇 end-effector pose 예측
- Language 조건을 포함하여 다중 작업 학습 수행
- 키프레임 단위로 target pose와 gripper 상태 예측

## Originality

- 카메라 이미지와 transformer 입력 이미지를 분리하여 가상 뷰로 재렌더링하는 혁신적 접근
- Voxel 기반 방법의 장점을 유지하면서 view 기반 방법의 확장성을 결합한 최초의 효율적 설계
- Multi-view transformer의 계층적 attention 구조(within-image → cross-view) 도입 및 효과 입증
- 단일 카메라만으로도 가상 뷰 생성을 통해 multi-view 표현을 활용 가능하게 한 실용적 설계

## Limitation & Further Study

- RLBench와 제한된 실제 환경(5개 작업)에서만 평가되어 더 다양한 실제 조작 작업에서의 성능 검증 필요
- 가상 뷰 재렌더링 과정에서 정확한 포인트 클라우드 생성이 필수적이므로 RGB-D 센서의 품질에 의존
- Language 조건부 학습을 위해 추가적인 설명 데이터가 필요할 수 있으며, 언어 이해 능력의 한계가 있을 수 있음
- 장기적인 다단계 조작 작업(multi-step horizon)에서의 성능 평가 부족
- 후속 연구로 더 큰 규모의 실제 로봇 데이터셋에서의 검증, 동적 환경에서의 성능 평가, 매니퓰레이션 다양성 확장 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RVT는 voxel 기반의 높은 성능과 view 기반의 확장성을 효과적으로 결합한 혁신적 방법으로, 실질적인 훈련 시간 단축과 성능 향상을 동시에 달성하여 로봇 조작 연구의 발전에 상당한 기여를 한다.

## Related Papers

- 🔗 후속 연구: [[papers/1558_RVT-2_Learning_Precise_Manipulation_from_Few_Demonstrations/review]] — RVT-2는 RVT의 multi-view transformer 접근법을 계승하여 학습 효율성을 크게 개선했습니다.
- 🔗 후속 연구: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — 3D-VLA는 RVT의 3D 표현 아이디어를 확장하여 생성형 월드 모델과 결합한 접근법입니다.
- 🔄 다른 접근: [[papers/1514_Perceiver-Actor_A_Multi-Task_Transformer_for_Robotic_Manipul/review]] — Perceiver-Actor와 RVT는 모두 transformer 기반 3D 조작을 다루지만 서로 다른 아키텍처 설계를 채택합니다.
- 🔄 다른 접근: [[papers/1288_3D_Diffusion_Policy_Generalizable_Visuomotor_Policy_Learning/review]] — 3D Diffusion Policy가 diffusion 기반 접근법으로 3D 조작을 다루는 반면, RVT는 transformer 기반으로 동일한 문제를 해결한다.
- 🔗 후속 연구: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — VoxPoser의 3D value map 개념을 multi-view transformer로 확장하여 더 효율적인 3D 조작 표현을 구현했다.
- 🔗 후속 연구: [[papers/1514_Perceiver-Actor_A_Multi-Task_Transformer_for_Robotic_Manipul/review]] — 3D object manipulation을 위한 transformer 기반 접근법을 RVT의 robotic view transformer와 결합하여 더 정확한 6-DoF 조작 성능을 달성한다.
- 🔗 후속 연구: [[papers/1567_SE3-Equivariant_Robot_Learning_and_Control_A_Tutorial_Survey/review]] — RVT의 3D object manipulation이 SE(3)-equivariant learning을 실제 로봇 조작 태스크로 확장한 구체적 응용 사례다.
- 🏛 기반 연구: [[papers/1558_RVT-2_Learning_Precise_Manipulation_from_Few_Demonstrations/review]] — RVT-2는 기존 RVT의 3D 객체 조작 아키텍처를 기반으로 하여 학습 효율성과 성능을 대폭 개선했다.
- 🏛 기반 연구: [[papers/1302_Adapt3R_Adaptive_3D_Scene_Representation_for_Domain_Transfer/review]] — RVT의 3D object manipulation을 위한 view transformer 개념을 domain transfer를 위한 adaptive 3D scene representation으로 발전시킨 연구입니다.
- 🔗 후속 연구: [[papers/1288_3D_Diffusion_Policy_Generalizable_Visuomotor_Policy_Learning/review]] — RVT의 3D object manipulation을 위한 view transformer 개념을 diffusion policy와 결합하여 모방 학습으로 발전시킨 연구입니다.
