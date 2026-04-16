---
title: "1619_PolygMap_A_Perceptive_Locomotion_Framework_for_Humanoid_Robo"
authors:
  - "Bingquan Li"
  - "Ning Wang"
  - "Tianwei Zhang"
  - "Zhicheng He"
  - "Yucong Wu"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "PolygMap은 LiDAR, RGB-D 카메라, IMU를 융합하여 실시간 다각형 계단 평면 의미지도를 구축하고, 이를 기반으로 인간형 로봇의 계단 등반을 위한 발디딤 계획을 수행하는 지각 기반 보행 계획 프레임워크이다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/LiDAR_Terrain_Perception"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2025_PolygMap A Perceptive Locomotion Framework for Humanoid Robot Stair Climbing.pdf"
---

# PolygMap: A Perceptive Locomotion Framework for Humanoid Robot Stair Climbing

> **저자**: Bingquan Li, Ning Wang, Tianwei Zhang, Zhicheng He, Yucong Wu | **날짜**: 2025-10-14 | **URL**: [https://arxiv.org/abs/2510.12346](https://arxiv.org/abs/2510.12346)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: The system integrates joint recorders, depth sensing and LIO estimator. Robot pose is obtained via fusing forwar*

PolygMap은 LiDAR, RGB-D 카메라, IMU를 융합하여 실시간 다각형 계단 평면 의미지도를 구축하고, 이를 기반으로 인간형 로봇의 계단 등반을 위한 발디딤 계획을 수행하는 지각 기반 보행 계획 프레임워크이다.

## Motivation

- **Known**: 이족 보행 로봇의 계단 등반은 기존에 강력한 자체 균형 조절과 높은 대역폭의 추적 안정화기를 이용한 brute-force 기하학적 섭동 처리 방식으로 접근해왔다. 이러한 방식은 명시적인 환경 기하학 지각과 발디딤 영역 인식이 부족하여 보수적인 보행과 높은 발디딤 불확실성을 초래한다.
- **Gap**: 계단 환경에서 낮은 질감, 검은색 흡수 재료, 시점 변화로 인한 깊이 측정 오류, 이족 보행 중 신체 진동과 카메라 롤링 셔터 효과, 그리고 odometry-mapping 결합으로 인한 국소 드리프트 축적 등의 문제로 인해 견고한 발디딤 영역 표현의 실시간 생성이 어렵다.
- **Why**: 인간형 로봇이 실제 환경에서 건물 검사, 긴급 대응, 산업 협업 등 다양한 시나리오에 배치되면서 장시간 계단 등반의 신뢰성과 안정성 확보가 필수적이기 때문이다.
- **Approach**: 다중 센서 융합(LiDAR + RGB-D + IMU)을 통해 실시간 odometry 추정과 깊이 이미지 처리를 수행하고, anisotropic diffusion filtering, Sobel operator, Canny algorithm, RANSAC을 이용하여 다각형 의미지도를 구축한 후, 안전 영역 침식과 재도달성 검사를 거쳐 발디딤 후보를 생성한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Polygmap-based footstep motion planning logic*

- **실시간 다중 센서 융합 기반 상태 추정**: LiDAR-Inertial Odometry(LIO)와 forward kinematics를 결합한 Kalman filter 기반 pose 추정으로 정확한 robot state 획득
- **GPU 친화적 다각형 의미지도 생성**: NVIDIA Orin에서 20-30 Hz의 전신 동작 계획 출력을 달성하는 효율적인 기하학적 추출 파이프라인 구현
- **안전 제약 기반 발디딤 계획**: 안전 영역 침식, 충돌 회피, 재도달성 검사를 통한 발 궤적 계획 실현
- **실제 환경 검증**: 실내 외 다양한 계단 환경에서 견고한 등반 성능 입증

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Polygmap-based footstep motion planning logic*

- Multi-sensor fusion: LIO(Livox Mid360 LiDAR + IMU)로 global odometry 추정, forward kinematics로 proprioceptive state 계산, Kalman filter로 통합
- Depth image processing: Anisotropic diffusion filtering으로 노이즈 제거, Sobel operator로 surface normal map 계산, Canny algorithm으로 contour 추출
- Polygon fitting: RANSAC을 이용한 평면 피팅으로 다각형 의미지도 구축
- Foothold generation: Safe region에 대한 morphological erosion 수행, nearest neighbor search로 reach 가능한 발디딤 위치 선택
- Trajectory planning: Collision-free foot trajectory planning으로 최종 발디딤 경로 생성
- Real-time integration: Loosely coupled scheme으로 LIO pose를 fusion framework에 통합하여 시스템 견고성 강화

## Originality

- LiDAR와 RGB-D의 다중 센서 융합을 통한 상호보완적 계단 인식: LiDAR는 저조도 환경에서도 작동하며 odometry 제공, RGB-D는 고해상도 깊이 정보로 발디딤 영역 정밀화
- Forward kinematics와 LIO의 loosely coupled fusion: Proprioceptive와 exteroceptive 정보를 Kalman filter로 통합하여 신체 진동과 카메라 노이즈 영향 감소
- Anisotropic diffusion + Sobel + Canny + RANSAC 파이프라인: 계단의 낮은 질감과 검은색 표면 등 도전적 조건에서 견고한 다각형 추출 실현
- 안전 영역 침식 기반 발디딤 선택: 단순한 평면 fitting을 넘어 안정성과 재도달성을 동시에 고려한 foothold candidate 생성

## Limitation & Further Study

- RGB-D 카메라(Realsense L515)의 성능이 고흡수성 표면에서 저하될 수 있어 검은색 또는 흡수율 높은 계단에서의 견고성 미흡
- 20-30 Hz의 planning 주기로 인한 고속 계단 등반 시 반응성 제한 가능성
- Forward kinematics 기반 state estimation이 모델 오류나 joint encoder 부정확도에 민감할 수 있음
- 현재 validation이 특정 계단 형태에 제한될 가능성이 있으며, 나선형 계단이나 불규칙한 계단면에 대한 일반화 성능 미지수
- 후속 연구: 다중 카메라 시점 활용, thermal imaging 통합, 심화 학습 기반 plane segmentation, 동적 보행 중 foothold 재계획 메커니즘 개발 등

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: PolygMap은 다중 센서 융합을 통해 계단 환경의 인식 불확실성을 효과적으로 대응하고, 실시간 의미지도 생성과 안전 제약 기반 발디딤 계획을 실현함으로써 인간형 로봇의 신뢰성 있는 계단 등반을 달성했다. 실제 환경 검증과 NVIDIA Orin 구현을 통해 실용성을 입증한 점에서 높은 가치가 있으나, 특정 표면 재질에 대한 견고성 개선과 더 높은 갱신률이 향후 과제이다.

## Related Papers

- 🏛 기반 연구: [[papers/1633_Real-Time_Polygonal_Semantic_Mapping_for_Humanoid_Robot_Stai/review]] — PolygMap의 실시간 다각형 의미 맵핑이 Real-Time Polygonal Semantic Mapping의 GPU 가속 알고리즘을 직접 활용한다
- 🔄 다른 접근: [[papers/1658_RPL_Learning_Robust_Humanoid_Perceptive_Locomotion_on_Challe/review]] — 두 논문 모두 지각 기반 휴머노이드 보행을 다루지만 PolygMap은 계단 등반에, RPL은 복잡한 지형에서의 견고한 보행에 집중한다
- 🔗 후속 연구: [[papers/2162_TTT-Parkour_Rapid_Test-Time_Training_for_Perceptive_Robot_Pa/review]] — PolygMap의 계단 등반 계획이 TTT-Parkour의 test-time 적응과 결합되어 더 동적인 환경 대응이 가능하다
- 🔗 후속 연구: [[papers/1696_Success_in_Humanoid_Reinforcement_Learning_under_Partial_Obs/review]] — PolygMap의 지각 기반 보행 계획과 부분 관찰 하에서의 안정적인 휴머노이드 학습을 결합하면 더 견고한 계단 등반이 가능하다
- 🏛 기반 연구: [[papers/1710_The_invariant_extended_Kalman_filter_as_a_stable_observer/review]] — IEKF의 안정적인 상태 추정 이론이 PolygMap의 LiDAR-RGB-D-IMU 센서 융합 시스템의 수학적 기반을 제공한다
- 🔄 다른 접근: [[papers/1978_Hiking_in_the_Wild_A_Scalable_Perceptive_Parkour_Framework_f/review]] — 둘 다 지각 기반 휴머노이드 보행을 다루지만 PolygMap은 계단 특화, HIKING은 일반적인 파쿠어 환경에 초점을 맞춘다
- 🔗 후속 연구: [[papers/1693_STATE-NAV_Stability-Aware_Traversability_Estimation_for_Bipe/review]] — PolygMap의 계단 인식을 일반적인 terrain traversability estimation으로 확장
- 🔄 다른 접근: [[papers/1658_RPL_Learning_Robust_Humanoid_Perceptive_Locomotion_on_Challe/review]] — RPL과 PolygMap 모두 지각 기반 휴머노이드 보행을 다루지만 전자는 복잡한 지형에서의 견고성에, 후자는 계단 등반에 특화되어 있다
- 🔄 다른 접근: [[papers/1696_Success_in_Humanoid_Reinforcement_Learning_under_Partial_Obs/review]] — 둘 다 부분 관찰 상황을 다루지만 고정 길이 과거 관찰 vs 멀티모달 센서 융합으로 접근이 다르다
- 🔗 후속 연구: [[papers/1710_The_invariant_extended_Kalman_filter_as_a_stable_observer/review]] — IEKF의 안정적 상태 추정 이론이 PolygMap의 멀티모달 센서 융합 시스템에 수학적으로 견고한 기반을 제공한다
- 🔄 다른 접근: [[papers/1613_PhysHSI_Towards_a_Real-World_Generalizable_and_Natural_Human/review]] — 두 논문 모두 LiDAR 기반 환경 인식을 사용하지만 PhysHSI는 객체 상호작용에, PolygMap은 계단 등반에 특화되어 있다
- 🔗 후속 연구: [[papers/1633_Real-Time_Polygonal_Semantic_Mapping_for_Humanoid_Robot_Stai/review]] — Real-Time Polygonal Semantic Mapping의 GPU 가속 알고리즘이 PolygMap의 전체 지각 기반 보행 프레임워크에서 핵심 기술로 활용된다
- 🔄 다른 접근: [[papers/1939_Gait-Adaptive_Perceptive_Humanoid_Locomotion_with_Real-Time/review]] — 실시간 하향식 깊이 기반 높이맵 재구성과 PolygMap의 다각형 지각 프레임워크는 서로 다른 지형 인식 방법입니다.
