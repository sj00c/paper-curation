---
title: "1597_UniAff_A_Unified_Representation_of_Affordances_for_Tool_Usag"
authors:
  - "Qiaojun Yu"
  - "Siyuan Huang"
  - "Xibin Yuan"
  - "Zhengkai Jiang"
  - "Ce Hao"
date: "2024.09"
doi: ""
arxiv: ""
score: 4.0
essence: "UniAff는 도구 사용과 관절형 객체 조작을 통합하는 MLLM 기반 프레임워크로, 3D motion constraints와 affordances의 통일된 표현을 제시한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Vision-Language_Object_Manipulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yu et al._2024_UniAff A Unified Representation of Affordances for Tool Usage and Articulation with Vision-Language.pdf"
---

# UniAff: A Unified Representation of Affordances for Tool Usage and Articulation with Vision-Language Models

> **저자**: Qiaojun Yu, Siyuan Huang, Xibin Yuan, Zhengkai Jiang, Ce Hao, Xin Li, Haonan Chang, Junbo Wang, Liu Liu, Hongsheng Li, Peng Gao, Cewu Lu | **날짜**: 2024-09-30 | **URL**: [https://arxiv.org/abs/2409.20551](https://arxiv.org/abs/2409.20551)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

UniAff는 도구 사용과 관절형 객체 조작을 통합하는 MLLM 기반 프레임워크로, 3D motion constraints와 affordances의 통일된 표현을 제시한다.

## Motivation

- **Known**: 기존 연구는 관절형 객체 또는 도구 중 하나에만 집중하거나 case-by-case 문제 해결만 가능했으며, LLM을 활용한 이단계 접근법이 제안되어 왔다.
- **Gap**: 도구 사용과 관절형 객체 조작을 통합하는 통일된 표현이 부재하며, 복잡한 3D motion constraints와 affordances를 동시에 처리하는 방법이 한정적이다.
- **Why**: 로봇이 다양한 도구와 관절형 객체를 효과적으로 조작하려면 3D 공간에서의 물리적 제약과 상호작용 영역을 이해해야 하며, 이러한 통합적 이해는 로봇의 적응성과 효율성을 크게 향상시킨다.
- **Approach**: 900개의 관절형 객체(19개 카테고리)와 600개의 도구(12개 카테고리)를 포함한 대규모 합성 데이터셋을 구축하고, SPHINX MLLM을 fine-tuning하여 부품 수준의 6D pose, grasp affordance, functional affordance, manipulation type을 예측한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **통합 프레임워크**: 도구와 관절형 객체의 조작을 하나의 통일된 부품 표현 공식으로 통합한 최초의 MLLM 모델 제안
- **포괄적 데이터셋**: 1,500개 객체에 대한 부품 수준 6D pose, manipulation type, affordance 라벨이 포함된 대규모 synthetic dataset 개발
- **강력한 성능 향상**: HANDAL 데이터셋에서 LISA 대비 11.5% 향상, A3VLM 대비 unseen instance에서 7.07%, unseen category에서 9.60% 성공률 개선
- **현실 환경 적응성**: 시뮬레이션과 실제 로봇 환경 모두에서 검증되어 cross-task 일반화 능력 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- Structured 3D spatial formulation 정의: 각 부품 ψi에 대해 6D pose Ai, bounding box Bi, grasp affordance Gi, functional affordance Fi, joint type Ji, part state Li로 구성된 통일된 표현 도입
- Synthetic data generation: 사전 스캔된 메시 또는 URDF 모델을 활용하여 near-realistic 시뮬레이션에서 자동 라벨링으로 대규모 데이터셋 생성
- MLLM fine-tuning: SPHINX 모델에 VQA 형식으로 dataset을 fine-tuning하여 부품 BBOX, affordance BBOX, manipulation type 예측
- 혼합 시각 인코더: DinoV2와 CLIP을 결합한 mixed visual encoder를 사용하여 다양한 시각 정보 캡처
- Manipulation type 분류: bottle caps, revolute parts, sliding lids, prismatic parts, freedom object 5가지 manipulation type 정의

## Originality

- 도구와 관절형 객체를 단일 부품 표현 공식으로 통합하는 novel한 접근법
- 부품 수준의 6D pose, grasp affordance, functional affordance, joint type을 동시에 예측하는 통합 VQA 기반 framework
- 자동 라벨링을 통한 1,500개 객체 규모의 포괄적 synthetic dataset 개발
- MLLM의 추론 능력을 활용한 affordance 이해의 새로운 패러다임

## Limitation & Further Study

- 합성 데이터 기반 학습으로 인한 domain gap이 존재할 수 있으며, 실제 환경의 복잡한 상황에 대한 일반화 성능 추가 검증 필요
- 현재 model은 하나의 객체에 대한 이해에 중점을 두고 있으며, 다중 객체 상호작용 시나리오로 확장 필요
- manipulation type 분류가 주로 1-DOF 관절에 초점을 맞추고 있어, 더 복잡한 kinematic chain을 가진 객체 처리 개선 필요
- VQA 형식이 특정 쿼리 구조에 의존하므로, 더 자연스러운 언어 상호작용으로의 확장 고려
- 실제 로봇 배포 시 prediction accuracy와 실행 성공률의 gap 분석 및 개선 방향 제시 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: UniAff는 도구와 관절형 객체 조작을 최초로 통합하는 MLLM 기반 프레임워크로, 구조화된 부품 표현과 대규모 synthetic dataset을 통해 로봇 조작의 일반화 능력을 크게 향상시킨 의미 있는 연구 성과이다.

## Related Papers

- 🔄 다른 접근: [[papers/1301_A3VLM_Actionable_Articulation-Aware_Vision_Language_Model/review]] — 둘 다 관절형 객체와 affordance를 다루지만 A3VLM은 actionable articulation에 집중하는 다른 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1369_Do_As_I_Can_Not_As_I_Say_Grounding_Language_in_Robotic_Affor/review]] — 언어 기반 affordance 추론의 기본 개념을 제공하여 UniAff의 통일된 affordance 표현에 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — spatial affordance prediction을 tool usage와 articulated object manipulation으로 확장하여 더 포괄적인 affordance 모델을 제시합니다.
- 🏛 기반 연구: [[papers/1574_SKT_Integrating_State-Aware_Keypoint_Trajectories_with_Visio/review]] — UniAff의 통합된 affordance 표현은 SKT의 상태 인식 키포인트 추적을 위한 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — 3D value map 기반 조작을 affordance와 도구 사용으로 확장하여 더 복합적인 로봇 조작 능력을 구현한다.
- 🔗 후속 연구: [[papers/1468_ManipVQA_Injecting_Robotic_Affordance_and_Physically_Grounde/review]] — ManipVQA의 affordance 개념을 도구 사용까지 확장한 unified representation
- 🔗 후속 연구: [[papers/1506_Open-World_Object_Manipulation_using_Pre-trained_Vision-Lang/review]] — MOO의 open-world object manipulation을 tool usage와 affordance understanding으로 확장하여 더 복잡한 조작 작업을 수행할 수 있다.
- 🏛 기반 연구: [[papers/1574_SKT_Integrating_State-Aware_Keypoint_Trajectories_with_Visio/review]] — UniAff의 통합된 affordance 표현은 의류 조작에서 상태 인식 keypoint의 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — UniAff의 통합된 affordance 표현 개념을 확장하여 언어 지시 기반의 정확한 행동 지점 예측으로 발전시켰다.
- 🔗 후속 연구: [[papers/1301_A3VLM_Actionable_Articulation-Aware_Vision_Language_Model/review]] — UniAff의 통합 affordance 표현은 A3VLM의 물체 중심 행동 가능성 학습을 더 일반화한 접근법입니다.
