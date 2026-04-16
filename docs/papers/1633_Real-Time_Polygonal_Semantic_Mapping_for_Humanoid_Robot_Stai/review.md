---
title: "1633_Real-Time_Polygonal_Semantic_Mapping_for_Humanoid_Robot_Stai"
authors:
  - "Teng Bin"
  - "Jianming Yao"
  - "Tin Lun Lam"
  - "Tianwei Zhang"
date: "2024.11"
doi: ""
arxiv: ""
score: 4.0
essence: "인형로봇의 계단 등반을 위해 GPU 가속 anisotropic diffusion 필터링과 RANSAC 기반 평면 추출을 활용한 실시간 다각형 의미 맵핑 알고리즘을 제시한다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Computational_Optimization_and_Tools"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/LiDAR_Terrain_Perception"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bin et al._2024_Real-Time Polygonal Semantic Mapping for Humanoid Robot Stair Climbing.pdf"
---

# Real-Time Polygonal Semantic Mapping for Humanoid Robot Stair Climbing

> **저자**: Teng Bin, Jianming Yao, Tin Lun Lam, Tianwei Zhang | **날짜**: 2024-11-04 | **URL**: [https://arxiv.org/abs/2411.01919](https://arxiv.org/abs/2411.01919)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the Planar Polygonal Semantic Mapping System Framework. The system inputs are depth images and*

인형로봇의 계단 등반을 위해 GPU 가속 anisotropic diffusion 필터링과 RANSAC 기반 평면 추출을 활용한 실시간 다각형 의미 맵핑 알고리즘을 제시한다.

## Motivation

- **Known**: 컴퓨터 비전과 SLAM 분야에서 순서화된 깊이 이미지로부터의 평면 추출이 순서 없는 포인트 클라우드 방식보다 실시간 성능과 정확도 면에서 우수하다는 것이 알려져 있다.
- **Gap**: 현존 방법들은 필터링 기법이 평면 추출에 미치는 영향을 간과하여 시뮬레이션과 실제 센서 데이터 간 성능 차이가 발생하며, 인형로봇의 안정적 지지면 요구 사항을 충족시키지 못한다.
- **Why**: 인형로봇은 계단 등반 같은 복잡한 작업 수행 시 정확한 환경 인식과 신뢰성 있는 의미 맵이 필수적이며, 추출된 평면의 정규 벡터와 높이 정확도는 로봇의 안전성을 직접적으로 좌우한다.
- **Approach**: Anisotropic diffusion을 통해 깊이 이미지 노이즈를 감소시키면서 에지를 보존하고, GPU 병렬 처리로 RANSAC 기반 평면 추출을 가속화하여 30 Hz 이상의 실시간 처리를 달성한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Planar polygon semantic mapping results of spiral*

- **실시간 성능**: 30 Hz 이상의 프레임 처리율로 각 프레임을 센서 사이클 시간 내에 처리
- **노이즈 감소**: Anisotropic diffusion 필터링으로 그래디언트 점프로 인한 노이즈를 최소화하면서 에지 세부사항 보존
- **GPU 가속화**: Anisotropic diffusion과 RANSAC 기반 평면 추출 과정을 GPU 병렬 처리로 최적화
- **전역 일관성 맵**: 로봇 자세 추정을 활용한 다각형 병합 및 수직 방향 오도메트리 드리프트 보정
- **실제 센서 적용**: 시뮬레이션 대비 실제 깊이 카메라 데이터에서 성능 향상 입증

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Overview of processing.*

- 깊이 이미지를 GPU 메모리로 전송 후 anisotropic diffusion 필터링 적용
- Sobel 연산자를 이용해 정규 벡터 이미지 계산
- Canny 엣지 검출로 평면 윤곽 추출 및 다각형으로 간단히 표현
- RANSAC 알고리즘으로 각 다각형 영역에 최적의 평면 방정식 적합
- 오도메트리/SLAM 자세 추정을 활용하여 새로운 다각형을 기존 의미 맵에 병합
- 다각형 병합 시 수직 방향 오도메트리 드리프트 추정 및 보정

## Originality

- 기존 supervoxel 기반 평면 분할의 비효율성을 극복하기 위해 GPU 기반 anisotropic diffusion 필터링을 깊이 이미지에 직접 적용
- 실시간 처리 조건에서 정규 벡터 품질과 에지 보존의 균형을 맞추는 새로운 접근법
- 인형로봇의 가트 계획과 의미 맵을 통합한 시스템 구현
- 평면 추출 정확도 향상을 위한 수직 방향 드리프트 보정 메커니즘

## Limitation & Further Study

- Light-absorbing 표면에서 LiDAR 기반 Realsense L515 센서의 성능 저하
- Anisotropic diffusion의 반복 횟수와 확산 계수 선택에 대한 자동화된 파라미터 최적화 부재
- 수직 방향 드리프트 보정이 간단한 방식으로 구현되어 장시간 누적 오차 처리 미흡
- 동적 장애물과 빠르게 변화하는 환경에서의 맵 업데이트 전략 상세 설명 부족
- 다양한 지형과 계단 구조에 대한 광범위한 실험 데이터 제시 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 GPU 가속을 활용한 anisotropic diffusion 필터링과 RANSAC 기반 다각형 추출을 결합하여 인형로봇의 복잡한 지형 네비게이션을 위한 실시간 의미 맵핑 문제를 효과적으로 해결했다. 시뮬레이션과 실제 센서 데이터 간의 성능 격차를 줄이고 로봇의 안전한 보행 계획을 지원하는 실용적인 시스템으로서의 가치가 크다.

## Related Papers

- 🔄 다른 접근: [[papers/1941_Gallant_Voxel_Grid-based_Humanoid_Locomotion_and_Local-navig/review]] — Gallant의 복셀 그리드 기반 국소 내비게이션이 PyRoki의 다각형 의미 맵핑과는 다른 공간 표현 방식으로 계단 등반 문제에 접근한다.
- 🔗 후속 연구: [[papers/2117_Omni-Perception_Omnidirectional_Collision_Avoidance_for_Legg/review]] — Omni-Perception의 전방향 충돌 회피 기술이 실시간 다각형 의미 맵핑의 안전성을 크게 향상시킬 수 있다.
- 🏛 기반 연구: [[papers/1693_STATE-NAV_Stability-Aware_Traversability_Estimation_for_Bipe/review]] — STATE-NAV의 안정성 인식 보행성 추정이 LiDAR 기반 계단 등반 알고리즘의 핵심 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1619_PolygMap_A_Perceptive_Locomotion_Framework_for_Humanoid_Robo/review]] — Real-Time Polygonal Semantic Mapping의 GPU 가속 알고리즘이 PolygMap의 전체 지각 기반 보행 프레임워크에서 핵심 기술로 활용된다
- 🧪 응용 사례: [[papers/1939_Gait-Adaptive_Perceptive_Humanoid_Locomotion_with_Real-Time/review]] — 실시간 다각형 맵핑 기술이 Gait-Adaptive Perceptive Locomotion의 실시간 지형 인식에 직접 적용될 수 있다
- 🔄 다른 접근: [[papers/2010_HumanoidPano_Hybrid_Spherical_Panoramic-LiDAR_Cross-Modal_Pe/review]] — 두 논문 모두 휴머노이드의 환경 인식을 다루지만 전자는 계단 등반용 다각형 맵핑에, 후자는 panoramic-LiDAR 융합에 집중한다
- 🏛 기반 연구: [[papers/1619_PolygMap_A_Perceptive_Locomotion_Framework_for_Humanoid_Robo/review]] — PolygMap의 실시간 다각형 의미 맵핑이 Real-Time Polygonal Semantic Mapping의 GPU 가속 알고리즘을 직접 활용한다
- 🧪 응용 사례: [[papers/1802_An_Empirical_Evaluation_of_Four_Off-the-Shelf_Proprietary_Vi/review]] — VIO 시스템 평가 결과를 실시간 polygonal semantic mapping에 적용하여 휴머노이드 계단 오르기를 지원한다.
- 🏛 기반 연구: [[papers/1811_BeamDojo_Learning_Agile_Humanoid_Locomotion_on_Sparse_Footho/review]] — 의미론적 매핑이 BeamDojo의 다각형 발 보상 함수 설계에서 발판 인식 및 계획에 필요한 기반 기술이다
- 🏛 기반 연구: [[papers/1845_Collision-Free_Humanoid_Traversal_in_Cluttered_Indoor_Scenes/review]] — 실내 환경에서의 의미적 매핑이 장애물 회피 경로 계획의 기초가 됩니다.
- 🔗 후속 연구: [[papers/1858_cuRoboV2_Dynamics-Aware_Motion_Generation_with_Depth-Fused_D/review]] — 실시간 다각형 의미 맵핑의 GPU 가속 기술을 cuRoboV2의 TSDF/ESDF 인식 파이프라인과 결합하여 더 정확한 환경 인식이 가능하다.
- 🧪 응용 사례: [[papers/1884_DPL_Depth-only_Perceptive_Humanoid_Locomotion_via_Realistic/review]] — DPL의 현실적인 깊이 합성 기술이 polygonal semantic mapping과 결합되어 휴머노이드의 실내 네비게이션 성능을 향상시킬 수 있다.
- 🏛 기반 연구: [[papers/1892_E-SDS_Environment-aware_See_it_Do_it_Sorted_-_Automated_Envi/review]] — Real-Time Polygonal Semantic Mapping이 E-SDS의 환경 인식 지형 센서 분석을 위한 기본적인 매핑 기술을 제공한다.
- 🔗 후속 연구: [[papers/1941_Gallant_Voxel_Grid-based_Humanoid_Locomotion_and_Local-navig/review]] — Real-Time Polygonal Semantic Mapping의 기초 연구를 voxel grid와 z-grouped CNN을 활용한 더 효과적인 3D 제약 지형 횡단 시스템으로 발전시켰습니다.
- 🏛 기반 연구: [[papers/1971_Heracles_Bridging_Precise_Tracking_and_Generative_Synthesis/review]] — RAPT의 분포 외 감지와 실패 처리 방법론이 Heracles의 극단적 교란 상황 대응의 이론적 기반이 된다.
- 🧪 응용 사례: [[papers/2056_Learning_Humanoid_Locomotion_over_Challenging_Terrain/review]] — 지각적 내부 모델이 다각형 의미 매핑을 통한 계단 보행에 직접 적용되어 실제 환경에서의 안정성을 보여준다.
