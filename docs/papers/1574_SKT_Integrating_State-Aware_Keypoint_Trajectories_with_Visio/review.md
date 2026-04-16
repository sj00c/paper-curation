---
title: "1574_SKT_Integrating_State-Aware_Keypoint_Trajectories_with_Visio"
authors:
  - "Xin Li"
  - "Siyuan Huang"
  - "Qiaojun Yu"
  - "Zhengkai Jiang"
  - "Ce Hao"
date: "2024.09"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 Vision-Language Model(VLM)을 활용한 State-aware Keypoint Trajectories(SKT)를 제안하여 다양한 의류 상태에서 로봇의 의류 조작 성능을 향상시킨다. 합성 데이터셋을 통해 단일 모델로 여러 의류 유형을 처리할 수 있는 통합 접근법을 구현한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2024_SKT Integrating State-Aware Keypoint Trajectories with Vision-Language Models for Robotic Garment M.pdf"
---

# SKT: Integrating State-Aware Keypoint Trajectories with Vision-Language Models for Robotic Garment Manipulation

> **저자**: Xin Li, Siyuan Huang, Qiaojun Yu, Zhengkai Jiang, Ce Hao, Yimeng Zhu, Hongsheng Li, Peng Gao, Cewu Lu | **날짜**: 2024-09-26 | **URL**: [https://arxiv.org/abs/2409.18082](https://arxiv.org/abs/2409.18082)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2.*

본 논문은 Vision-Language Model(VLM)을 활용한 State-aware Keypoint Trajectories(SKT)를 제안하여 다양한 의류 상태에서 로봇의 의류 조작 성능을 향상시킨다. 합성 데이터셋을 통해 단일 모델로 여러 의류 유형을 처리할 수 있는 통합 접근법을 구현한다.

## Motivation

- **Known**: 기존의 의류 조작 연구는 의류의 변형 가능성과 다양성으로 인해 의류 유형별 별도 모델이 필요했으며, 3D 데이터와 클래스별 키포인트 인식 모델에 의존했다. 합성 데이터는 로봇 의류 조작에서 확산되고 있지만 고품질 3D 자산 생성과 의미론적 주석이 부족했다.
- **Gap**: 기존 방법들은 평면 의류에 최적화되어 주름진 또는 접힌 의류 상태에서 성능이 저하되며, 다양한 의류 상태에 대한 일반화 능력이 제한적이다. 시각 정보만으로는 의류의 현재 상태와 의미론적 정보를 통합하여 해석하는 데 부족하다.
- **Why**: 가정 자동화와 노인 돌봄 로봇 등 assistive robotics에서 의류 조작은 일상적 작업으로 중요하며, 단일 모델로 다양한 의류를 처리할 수 있는 확장성 있는 솔루션이 필요하다. VLM을 통한 시각-언어 통합은 의류의 복잡한 변형 상태를 더 잘 이해할 수 있게 한다.
- **Approach**: VLM을 미세조정하여 상태 인식 paired keypoint를 예측하는 SKT 프레임워크를 개발하고, 고급 물리 시뮬레이터를 사용해 평면, 변형, 접힘 상태를 포함한 대규모 합성 데이터셋을 생성한다. 시각 특징과 언어 기반 질의를 결합하여 reasoning-based vision-language 작업을 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **통합 paired keypoint trajectories 공식화**: 시각 정보와 의미론적 정보를 결합하여 다양한 의류 상태에 적응할 수 있는 VLM 기반 통합 접근법 제시
- **대규모 합성 데이터셋 구축**: 다양한 의류 상태를 포함한 합성 데이터로 실세계 데이터 수집 부담을 제거하고 일반화 능력 향상
- **Reasoning 기반 VLM 작업**: 의류 상태를 추론하여 키포인트를 동적으로 조정하는 능력으로 정확성과 적응성 개선
- **성능 향상**: 제안 방법이 키포인트 감지 정확도와 작업 성공률을 크게 향상시킴을 실험으로 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- 물리 시뮬레이터와 렌더링 기술을 사용하여 평면, 변형, 접힘 상태의 다양한 의류 구성을 포함한 합성 데이터 생성
- RGB 이미지를 입력으로 사용하여 깊이 이미지보다 풍부한 시각 정보(패턴, 솔기 등) 활용
- VLM을 파인튜닝하여 시각 특징과 의류 부위, 조작 작업에 대한 언어 설명을 함께 처리
- Paired keypoint trajectories를 상태 인식적으로 생성하여 의류의 현재 상태에 따라 적절한 키포인트 출력
- Action decoder를 통해 키포인트 예측에서 로봇 조작 행동 시퀀스로 변환
- Reasoning-based 접근으로 부분적으로 접히거나 변형된 의류에서 관련 키포인트를 추론하여 조정

## Originality

- VLM을 의류 조작에 처음 체계적으로 적용하여 시각-언어 통합을 통한 상태 인식 키포인트 예측 제안
- State-aware paired keypoint trajectories라는 새로운 표현 방식으로 다양한 의류 상태를 통합 처리
- 의류 조작 분야에서 reasoning-based vision-language 작업을 도입하여 동적 적응 능력 추가
- 합성 데이터를 통한 확장 가능한 학습 파이프라인으로 실세계 주석의 부담 제거

## Limitation & Further Study

- 합성 데이터와 실제 의류 간의 도메인 갭이 존재할 수 있으며, 실세계 성능 검증이 제한적으로 제시됨
- VLM의 계산 비용과 추론 속도에 대한 상세한 분석이 부족함
- 특정 의류 유형(예: 신축성 높은 의류, 특수 재질)에 대한 성능이나 실패 사례 분석이 미흡함
- 다른 변형 객체(로프, 케이블 등) 조작 작업으로의 일반화 가능성 논의 필요
- 후속 연구에서는 실시간 적응 학습(online learning) 메커니즘 추가와 실물 로봇 시스템과의 통합 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 VLM을 의류 조작에 창의적으로 적용하여 단일 모델로 다양한 의류 상태를 처리하는 혁신적 접근법을 제시한다. 합성 데이터 활용과 reasoning 기반 설계로 확장성과 적응성을 크게 개선하여 assistive robotics 분야에 중요한 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1468_ManipVQA_Injecting_Robotic_Affordance_and_Physically_Grounde/review]] — ManipVQA는 VLM을 활용한 로봇 조작에서 affordance와 물리적 grounding을 다루는 다른 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1356_DexGraspVLA_A_Vision-Language-Action_Framework_Towards_Gener/review]] — DexGraspVLA는 VLM과 keypoint 기반 접근법을 정교한 조작에 적용하는 유사하지만 다른 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1622_VoxPoser_Composable_3D_Value_Maps_for_Robotic_Manipulation_w/review]] — VoxPoser는 3D value map을 통해 의류 조작과 유사한 복잡한 조작 작업을 해결하는 대안적 접근법이다.
- 🏛 기반 연구: [[papers/1597_UniAff_A_Unified_Representation_of_Affordances_for_Tool_Usag/review]] — UniAff의 통합된 affordance 표현은 의류 조작에서 상태 인식 keypoint의 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1536_RoboBrain_A_Unified_Brain_Model_for_Robotic_Manipulation_fro/review]] — 로봇의 의류 조작에서 SKT는 state-aware keypoint trajectory로, RoboBrain은 통합 MLLM으로 서로 다른 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1574_SKT_Integrating_State-Aware_Keypoint_Trajectories_with_Visio/review]] — VLM 기반 keypoint trajectory 방법이 다양한 의류 상태 처리를 위한 더 정교한 state-aware 시스템으로 발전할 수 있다.
- 🏛 기반 연구: [[papers/1355_DexGarmentLab_Dexterous_Garment_Manipulation_Environment_wit/review]] — DexGarmentLab의 의류 조작 환경이 SKT의 state-aware keypoint trajectory 방법론 개발과 검증에 실험적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1529_ReKep_Spatio-Temporal_Reasoning_of_Relational_Keypoint_Const/review]] — SKT의 state-aware keypoint trajectories 기술이 ReKep의 spatio-temporal keypoint constraints 설계의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1592_TraceVLA_Visual_Trace_Prompting_Enhances_Spatial-Temporal_Aw/review]] — keypoint trajectory를 VLA와 통합하는 기본 개념을 제공하여 TraceVLA의 시공간 추적 메커니즘에 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1597_UniAff_A_Unified_Representation_of_Affordances_for_Tool_Usag/review]] — UniAff의 통합된 affordance 표현은 SKT의 상태 인식 키포인트 추적을 위한 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1297_A_Real-to-Sim-to-Real_Approach_to_Robotic_Manipulation_with/review]] — 상태 인식 keypoint 궤적과 VLM 생성 keypoint reward를 결합하여 더 강력한 조작 정책을 개발할 수 있습니다.
