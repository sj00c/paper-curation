---
title: "1932_FocusNav_Spatial_Selective_Attention_with_Waypoint_Guidance"
authors:
  - "Yang Zhang"
  - "Jianming Ma"
  - "Liyun Yan"
  - "Zhanxiang Cao"
  - "Yazhou Zhang"
date: "2026.01"
doi: ""
arxiv: ""
score: 4.0
essence: "FocusNav는 인간형 로봇의 국소 항법을 위해 Waypoint-Guided Spatial Cross-Attention (WGSCA)와 Stability-Aware Selective Gating (SASG) 모듈을 결합한 공간 선택적 주의 프레임워크를 제안한다. 예측된 무충돌 경로점을 기준으로 환경 지각을 동적으로 조정하여 불안정 시 원거리 정보를 제거함으로써 동적·복잡한 환경에서의 견고한 항법을 달성한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Terrain_Foothold_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2026_FocusNav Spatial Selective Attention with Waypoint Guidance for Humanoid Local Navigation.pdf"
---

# FocusNav: Spatial Selective Attention with Waypoint Guidance for Humanoid Local Navigation

> **저자**: Yang Zhang, Jianming Ma, Liyun Yan, Zhanxiang Cao, Yazhou Zhang, Haoyang Li, Yue Gao | **날짜**: 2026-01-19 | **URL**: [https://arxiv.org/abs/2601.12790](https://arxiv.org/abs/2601.12790)

---

## Essence

![Figure 4](figures/fig4.webp)

*Fig. 4: Overview of the FocusNav framework. (a) Multi-modal perception encoder fuses spatially aligned LiDAR and depth*

FocusNav는 인간형 로봇의 국소 항법을 위해 Waypoint-Guided Spatial Cross-Attention (WGSCA)와 Stability-Aware Selective Gating (SASG) 모듈을 결합한 공간 선택적 주의 프레임워크를 제안한다. 예측된 무충돌 경로점을 기준으로 환경 지각을 동적으로 조정하여 불안정 시 원거리 정보를 제거함으로써 동적·복잡한 환경에서의 견고한 항법을 달성한다.

## Motivation

- **Known**: 기존 인간형 로봇 항법은 LiDAR, RGB-D 센서 기반의 elevation/depth map 또는 point cloud 처리 방식을 사용하며, Vision-Language Navigation (VLN) 방식도 대부분 이산 방향이나 연속 속도 명령을 출력하는 velocity-command-tracking 패러다임에 의존한다. 생물학적 '대뇌-소뇌' 조화 메커니즘과 Perception-Prediction-Attention (PPA) 패러다임이 알려져 있다.
- **Gap**: 기존 VLN 방식은 고수준 지각 계획과 저수준 운동 제어 사이의 건축적 분리로 인해 전역 최적 해를 찾지 못하며, velocity-command-tracking 패러다임은 빠른 속도 변동과 민첩한 보행 조정을 충분히 지원하지 못한다. 특히 동시에 동적 장애물 회피와 불규칙 지형 견고 주행을 달성하는 것은 아직 미해결 과제이다.
- **Why**: 인간형 로봇의 실제 배포는 복잡하고 동적인 현실환경에서의 항법 능력에 의해 엄격히 제약되며, 이는 조작과 이동의 통합적 활용을 방해하는 핵심 병목 지점이다. 불규칙하고 밀집된 장애물이 많은 환경에서 안전한 국소 항법을 달성하는 것이 로봇 응용의 잠재력을 완전히 해방하는 데 중대하다.
- **Approach**: 생물학적 PPA 패러다임에서 영감을 받아, GuideOracle이라는 특권 정책으로 최적의 경로점 추적 신호를 생성한 후, WGSCA 메커니즘으로 시각 기반 항법 정책이 예측된 경로점을 기준으로 환경 특징을 집계하도록 유도한다. SASG 모듈은 실시간 안정성을 감지하여 불안정 시 원거리 정보를 제거함으로써 보행 안정성을 우선시한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Snapshots of dynamic obstacle avoidance on stairs.*

- **Waypoint-Guided Spatial Cross-Attention (WGSCA) 메커니즘**: 예측된 무충돌 경로점을 기준으로 환경 특징 집계를 공간적으로 앵커링하여 의도된 동작 궤적과 정렬된 지각을 보장
- **Stability-Aware Selective Gating (SASG) 모듈**: 로봇의 동적 안정성을 실시간 모니터링하여 불안정 감지 시 원거리 정보를 동적으로 제거, 즉각적인 발판 안전성 우선시
- **견고한 성능 개선**: Unitree G1 인간형 로봇에서 장애물 회피 효율성, 운동 안정성, 항법 성공률 측면에서 기존 방법들을 현저히 능가
- **복잡한 환경 적응**: 계단, 불규칙 지형, 동적 장애물이 있는 시나리오에서 안정적인 항법 달성

## How

![Figure 4](figures/fig4.webp)

*Fig. 4: Overview of the FocusNav framework. (a) Multi-modal perception encoder fuses spatially aligned LiDAR and depth*

- GuideOracle 특권 정책을 통해 시뮬레이션 환경의 완전한 관찰성을 활용하여 정밀한 지역 맵과 목표 좌표 접근으로 최적 감독 신호 생성
- WGSCA: 경로점 시퀀스를 환경 특징 인코더와의 spatial cross-attention을 통해 특징 집계를 경로 계획에 정렬
- SASG: 로봇 안정성 지표(예: CoM 높이, 접촉 상태)를 실시간 모니터링하여 임계값 이하에서 원거리 지각 정보의 가중치 제거 또는 마스킹
- 멀티모달 지각 인코더(LiDAR + depth camera)로부터 통합된 환경 특징 추출
- 강화학습 기반 정책 훈련으로 경로점 추적 및 장애물 회피를 동시 최적화

## Originality

- 생물학적 PPA 패러다임을 명시적으로 인간형 로봇 항법에 적용하는 개념적 창신성으로 지각-예측-주의 메커니즘을 기술적으로 구현
- WGSCA가 경로점 기반 spatial cross-attention을 제안하여 기존의 velocity-command-tracking 패러다임의 건축적 분리를 극복하는 구조적 혁신
- SASG 모듈이 실시간 안정성을 주의 메커니즘에 피드백하여 불규칙 지형에서의 즉각적 대응 능력을 강화하는 참신한 설계
- GuideOracle 특권 정책으로 고수준 계획과 저수준 제어 간 최적 신호 브리지를 제공하는 차별화된 감독 학습 전략

## Limitation & Further Study

- 실험이 단일 로봇 플랫폼(Unitree G1)에 제한되어 일반화 가능성 검증 부재
- SASG의 안정성 임계값이 수동 조정되므로 다양한 환경 조건에 대한 자동 적응 메커니즘 미흡
- 시뮬레이션 기반 GuideOracle 훈련이 sim-to-real 전이 오류를 완전히 제거하지 못할 가능성
- 계산 복잡성과 온보드 실행 시간에 대한 분석 및 최적화 부재
- 후속 연구: (1) 다양한 로봇 플랫폼으로 확장, (2) 적응형 안정성 임계값 학습, (3) 동적 환경에서의 장시간 자율 항법 평가, (4) 에지 컴퓨팅 환경에서의 실시간 성능 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: FocusNav는 생물학적 영감과 기술적 혁신을 결합하여 인간형 로봇의 복잡한 동적 환경 항법이라는 중대한 과제를 체계적으로 해결한다. WGSCA와 SASG 모듈의 설계가 우수하고 실제 로봇 실험으로 검증되었으나, 단일 플랫폼 실험과 수동 파라미터 조정이라는 제약이 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1713_Thinking_in_360_Humanoid_Visual_Search_in_the_Wild/review]] — 둘 다 humanoid의 환경 인식과 navigation을 다루지만, FocusNav는 waypoint 기반 선택적 주의에, Thinking in 360°는 전방위 시각 탐색에 집중합니다.
- 🔗 후속 연구: [[papers/2087_LookOut_Real-World_Humanoid_Egocentric_Navigation/review]] — LookOut의 실제 환경 egocentric navigation 연구를 waypoint 안내와 안정성 인식이 결합된 더 정교한 프레임워크로 발전시켰습니다.
- 🔄 다른 접근: [[papers/1941_Gallant_Voxel_Grid-based_Humanoid_Locomotion_and_Local-navig/review]] — 둘 다 복잡한 3D 환경에서의 humanoid navigation을 다루지만, FocusNav는 selective attention을, Gallant는 voxel grid 기반 인식을 사용합니다.
- 🔗 후속 연구: [[papers/1713_Thinking_in_360_Humanoid_Visual_Search_in_the_Wild/review]] — 공간 인식 기반 네비게이션에서 360도 파노라마 탐색과 선택적 주의 메커니즘이 상호 보완적이다.
- 🏛 기반 연구: [[papers/1807_ARMOR_Egocentric_Perception_for_Humanoid_Robot_Collision_Avo/review]] — 충돌 회피를 위한 공간적 선택적 주의 메커니즘이 ARMOR의 transformer 기반 지각 정책의 이론적 기반을 제공한다
- 🔗 후속 연구: [[papers/1845_Collision-Free_Humanoid_Traversal_in_Cluttered_Indoor_Scenes/review]] — 공간 선택적 주의 메커니즘이 어수선한 실내 환경에서의 충돌 회피를 향상시킵니다.
- 🔄 다른 접근: [[papers/1941_Gallant_Voxel_Grid-based_Humanoid_Locomotion_and_Local-navig/review]] — 둘 다 공간 인식 기반 humanoid navigation을 다루지만, Gallant는 voxel grid 기반 전체 3D 환경 이해에, FocusNav는 waypoint 안내 selective attention에 집중합니다.
- 🧪 응용 사례: [[papers/1975_Hierarchical_visuomotor_control_of_humanoids/review]] — FocusNav의 spatial selective attention 기법이 고차원 시각-운동 제어의 attention mechanism으로 활용될 수 있다.
- 🏛 기반 연구: [[papers/2057_Learning_Humanoid_Navigation_from_Human_Data/review]] — 공간 선택적 주의와 waypoint 가이드의 원리가 EgoNav의 360도 시각 메모리 기반 내비게이션에 대한 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/2064_Learning_Social_Navigation_from_Positive_and_Negative_Demons/review]] — 웨이포인트 가이드를 통한 공간 선택적 주의 기반 네비게이션의 다른 접근법을 제시한다.
- 🔗 후속 연구: [[papers/2087_LookOut_Real-World_Humanoid_Egocentric_Navigation/review]] — 웨이포인트 가이드를 통한 공간 선택적 주의의 확장된 네비게이션 접근법을 보여준다.
- 🔗 후속 연구: [[papers/2101_Mobi-π_Mobilizing_Your_Robot_Learning_Policy/review]] — 정책 모빌라이제이션을 waypoint 가이드와 결합하여 더 효과적인 공간 선택적 주의 메커니즘을 구현할 수 있다.
- 🏛 기반 연구: [[papers/2110_No_More_Marching_Learning_Humanoid_Locomotion_for_Short-Rang/review]] — FocusNav의 공간 선택적 주의와 waypoint 안내 기법이 No More Marching의 constellation 기반 보상 함수 설계에 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/2111_NoMaD_Goal_Masked_Diffusion_Policies_for_Navigation_and_Expl/review]] — FocusNav의 waypoint guidance가 NoMaD의 goal-oriented navigation과 goal-free exploration 통합 설계에 영감을 제공했다
- 🔗 후속 연구: [[papers/2117_Omni-Perception_Omnidirectional_Collision_Avoidance_for_Legg/review]] — FocusNav의 공간 선택적 주의 메커니즘을 동적 환경에서 전방향 충돌 회피라는 더 복잡한 작업으로 확장한 연구이다.
