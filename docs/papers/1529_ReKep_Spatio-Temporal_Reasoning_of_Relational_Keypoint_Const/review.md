---
title: "1529_ReKep_Spatio-Temporal_Reasoning_of_Relational_Keypoint_Const"
authors:
  - "Wenlong Huang"
  - "Chen Wang"
  - "Yunzhu Li"
  - "Ruohan Zhang"
  - "Li Fei-Fei"
date: "2024.09"
doi: ""
arxiv: ""
score: 4.0
essence: "ReKep는 로봇 조작 작업을 3D 키포인트를 입력으로 하는 Python 함수 형태의 제약 조건으로 표현하며, 대규모 비전 모델과 비전-언어 모델을 활용하여 자동으로 이러한 제약을 생성하고 계층적 최적화로 실시간 로봇 제어를 실현한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_AI_Architectures"
  - "sub/3D_Keypoint_Manipulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2024_ReKep Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation.pdf"
---

# ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation

> **저자**: Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, Li Fei-Fei | **날짜**: 2024-09-03 | **URL**: [https://arxiv.org/abs/2409.01652](https://arxiv.org/abs/2409.01652)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Relational Keypoint Constraints (ReKep) specify diverse manipulation behaviors as an opti-*

ReKep는 로봇 조작 작업을 3D 키포인트를 입력으로 하는 Python 함수 형태의 제약 조건으로 표현하며, 대규모 비전 모델과 비전-언어 모델을 활용하여 자동으로 이러한 제약을 생성하고 계층적 최적화로 실시간 로봇 제어를 실현한다.

## Motivation

- **Known**: 로봇 조작은 공간-시간적 제약으로 표현될 수 있으며, 기존에는 강체 자세(rigid-body poses) 또는 학습 기반 표현이 사용되었다. 하지만 강체 자세는 기하학 정보가 필요하고 변형 가능한 물체에 대응 불가능하며, 학습 기반 방식은 수작업 레이블링이 필요하다.
- **Gap**: 제약 조건을 표현할 때 1) 다양한 작업에 대응 가능하고 2) 수작업 레이블링이 불필요하며 3) 실시간 최적화 가능한 형식이 부재하다.
- **Why**: 로봇이 다양한 환경과 작업에서 자율적으로 복잡한 조작 행동(다단계, bimanual, 반응적 행동 등)을 수행하려면 작업별 데이터나 환경 모델 없이도 제약 조건을 자동 생성하고 실시간 실행할 수 있는 표현이 필수적이다.
- **Approach**: DINOv2로 의미론적 키포인트를 제안하고 GPT-4o가 RGB-D 관찰과 자연어 지시로부터 제약 함수를 코드로 작성하며, 계층적 최적화(waypoint 해결 후 receding-horizon 제어)로 SE(3) end-effector 궤적을 실시간으로 생성한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Experiment tasks and visualization of optimization results. Seven tasks are designed to validate*

- **자동 제약 생성**: 대규모 비전 모델과 VLM을 결합하여 RGB-D 관찰과 자연어 지시만으로 ReKep을 자동 생성
- **다중 플랫폼 구현**: 휠 달린 단일 팔과 고정식 dual-arm 플랫폼에서 다양한 조작 작업 수행
- **복합 행동 지원**: 다단계(multi-stage), 야외(in-the-wild), bimanual, 반응적(reactive) 조작 행동을 작업별 데이터 없이 수행
- **실시간 성능**: 계층적 최적화를 통해 약 10 Hz 주기의 실시간 인식-행동 루프 달성
- **일반화 능력**: 다양한 객체와 환경에서 작업별 환경 모델이나 매개변수 조정 없이 작동

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of ReKep. DINOv2 [5] first proposes keypoints in the scene, which are overlaid on*

- DINOv2 self-supervised vision model로부터 장면의 semantic keypoint 제안
- 제안된 keypoint를 시각화한 RGB-D 이미지와 자연어 지시를 GPT-4o에 입력하여 Python 함수 형태의 제약 조건 생성
- 추적된 keypoint에 기반하여 제약 함수를 재평가하는 hierarchical optimization: (1) waypoint solver로 SE(3) sub-goal 해결, (2) receding-horizon controller로 dense action sequence 생성
- closed-loop perception-action에서 keypoint 추적 및 제약 재평가를 통한 적응적 제어
- 여러 ReKep을 시간순으로 조합하여 multi-stage task 표현

## Originality

- keypoint 기반 표현과 foundation model 자동 생성의 결합으로 scalable하고 일반화 가능한 새로운 제약 표현 제안
- VLM의 코드 생성 능력을 활용하여 복잡한 spatio-temporal 관계를 Python 함수로 직접 표현
- DINOv2(fine-grained pixel-level features)와 GPT-4o(visual reasoning)의 보완적 강점을 결합한 시각 기반 프롬팅 기법
- 계층적 최적화와 receding-horizon 제어로 실시간 실행 가능한 제약 기반 조작 프레임워크 구축
- 작업별 데이터나 환경 모델 없이 6-12 DoF 작업 수행 가능한 통합 시스템 구현

## Limitation & Further Study

- VLM의 코드 생성 정확도에 의존하므로 복잡한 기하학적 관계가 포함된 작업에서 생성 실패 가능성
- keypoint 추적의 정확도가 전체 시스템 성능을 제한할 수 있으며, occlusion이나 동적 장면에서 문제 발생 가능
- DINOv2와 GPT-4o 같은 대규모 모델에 대한 의존성으로 인한 계산 비용과 외부 API 의존성
- 현재 구현에서 약 10 Hz 주기는 매우 빠른 동작이 필요한 작업에는 제한적일 수 있음
- 후속 연구: (1) 더 강건한 keypoint 추적 방법 개발, (2) 온디바이스 또는 open-source VLM 활용으로 의존성 감소, (3) 복잡한 기하학적 제약 자동 생성 개선, (4) 동적 환경과 multi-agent 상황 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ReKep은 keypoint 기반 제약 표현과 foundation model 기반 자동 생성을 결합하여 일반화 가능하고 실시간 실행 가능한 로봇 조작 시스템을 제시한다. 다양한 작업 실연과 두 가지 로봇 플랫폼 구현으로 실질적 가치를 입증하며, 작업별 데이터 없는 generalist 로봇 구현의 중요한 진전을 나타낸다.

## Related Papers

- 🔄 다른 접근: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — ReKep의 3D 키포인트 제약과 VoxPoser의 3D value maps는 3D 공간 정보를 로봇 조작에 활용하는 서로 다른 접근법이다.
- 🏛 기반 연구: [[papers/1574_SKT_Integrating_State-Aware_Keypoint_Trajectories_with_Visio/review]] — SKT의 state-aware keypoint trajectories 기술이 ReKep의 spatio-temporal keypoint constraints 설계의 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — RoboPoint의 spatial affordance prediction이 ReKep의 3D 키포인트 기반 제약을 더 정교한 공간 이해로 발전시킨다.
- 🔄 다른 접근: [[papers/1517_PointWorld_Scaling_3D_World_Models_for_In-The-Wild_Robotic_M/review]] — ReKep과 PointWorld 모두 3D 공간 정보를 활용하지만 키포인트 제약과 포인트 플로우라는 다른 표현 방식을 사용합니다.
- 🔄 다른 접근: [[papers/1517_PointWorld_Scaling_3D_World_Models_for_In-The-Wild_Robotic_M/review]] — PointWorld와 ReKep 모두 3D 포인트 기반 조작을 다루지만 월드 모델링과 키포인트 제약이라는 다른 접근법을 사용합니다.
- 🧪 응용 사례: [[papers/1567_SE3-Equivariant_Robot_Learning_and_Control_A_Tutorial_Survey/review]] — ReKep은 SE(3) equivariance를 관계형 keypoint 제약에 적용하여 시공간 추론을 수행하는 구체적 응용이다.
- 🔄 다른 접근: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — ReKep과 함께 공간적 추론을 통한 로봇 조작을 다루지만 RoboPoint는 affordance keypoint에, ReKep은 관계형 키포인트에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — ReKep의 관계적 키포인트 추론과 VoxPoser의 3D value map을 결합하면 더 복잡한 공간 관계를 다룰 수 있다
- 🏛 기반 연구: [[papers/1297_A_Real-to-Sim-to-Real_Approach_to_Robotic_Manipulation_with/review]] — ReKep의 관계형 keypoint 개념이 VLM 기반 keypoint reward 함수 설계의 핵심 이론적 기반
