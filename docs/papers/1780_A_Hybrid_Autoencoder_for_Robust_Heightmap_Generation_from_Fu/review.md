---
title: "1780_A_Hybrid_Autoencoder_for_Robust_Heightmap_Generation_from_Fu"
authors:
  - "Dennis Bank"
  - "Joost Cordes"
  - "Thomas Seel"
  - "Simon F. G. Ehlers"
date: "2026.02"
doi: ""
arxiv: ""
score: 4.0
essence: "인형로봇의 불규칙한 지형 보행을 위해 깊이 카메라와 LiDAR 데이터를 융합하여 높이맵을 생성하는 하이브리드 Encoder-Decoder 구조를 제시하며, CNN과 GRU를 결합한 신경망이 시간적 일관성을 유지하면서 공간 특성을 추출한다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/LiDAR_Terrain_Perception"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bank et al._2026_A Hybrid Autoencoder for Robust Heightmap Generation from Fused Lidar and Depth Data for Humanoid Ro.pdf"
---

# A Hybrid Autoencoder for Robust Heightmap Generation from Fused Lidar and Depth Data for Humanoid Robot Locomotion

> **저자**: Dennis Bank, Joost Cordes, Thomas Seel, Simon F. G. Ehlers | **날짜**: 2026-02-05 | **URL**: [https://arxiv.org/abs/2602.05855](https://arxiv.org/abs/2602.05855)

---

## Essence


인형로봇의 불규칙한 지형 보행을 위해 깊이 카메라와 LiDAR 데이터를 융합하여 높이맵을 생성하는 하이브리드 Encoder-Decoder 구조를 제시하며, CNN과 GRU를 결합한 신경망이 시간적 일관성을 유지하면서 공간 특성을 추출한다.

## Motivation

- **Known**: 단일 센서 기반의 지형 인식 시스템은 조명 민감성, 지연, 계산 복잡성 등의 문제가 있으며, SLAM 및 elevation mapping 같은 전통적 기법은 사전 처리 파이프라인이 필요하다.
- **Gap**: 다중 센서 데이터를 효율적으로 융합하면서도 로봇의 즉각적인 보행 정책에 최적화된 중간 표현(heightmap)을 생성하는 학습 기반 프레임워크가 부재하다.
- **Why**: 인형로봇은 높은 무게중심과 양발 구조로 인해 보행 안정성이 취약하므로, 신뢰할 수 있는 지형 인식과 예측 행동이 불규칙한 인간 중심 환경에서의 안전한 보행 배치에 필수적이다.
- **Approach**: CNN 인코더로 깊이와 LiDAR 데이터(spherical projection으로 변환)의 공간 특성을 추출하고, GRU 기반의 공유 디코더로 시간적 일관성을 통합하여 최적화된 높이맵을 생성한다. 또한 reinforcement learning(PPO)으로 훈련된 보행 정책이 heightmap 해상도(7 cm)에 맞춰 최적화된다.

## Achievement


- **다중 센서 융합의 효과**: 깊이 카메라만 사용한 경우 대비 7.2%, LiDAR만 사용한 경우 대비 9.9% 재구성 정확도 개선
- **시간적 일관성 향상**: 3.2초 temporal context 통합으로 mapping drift 감소
- **최적 해상도 식별**: 6-8 cm 범위(특히 7 cm)의 heightmap 격자 간격이 지형 특성 감지와 학습 안정성 사이의 최적 균형점 제시
- **실시간 처리 가능성**: spherical projection 기반 LiDAR 처리로 계산 복잡도 및 지연 감소

## How


- **Spherical projection**: LIVOX MID-360 point cloud를 276×40 범위-방위각-경사각 range image로 변환하고, gap-filling 및 3×3 median filter로 전처리
- **분리된 CNN 인코더**: 깊이 영상(160×120)과 LiDAR range image(276×40)를 각각 4단계 strided convolution으로 처리하여 256차원 latent representation 추출
- **다중모달 융합**: 두 인코더의 256차원 벡터를 IMU 파생 15차원 로봇 상태 벡터, 이전 timestep 165차원 heightmap prediction과 concatenate 후 선형 변환 및 layer normalization으로 통합
- **GRU 디코더**: 융합된 다중모달 표현을 시간축 방향으로 처리하여 robot-centric heightmap 재구성
- **Heightmap 최적화**: 0.98 m × 0.7 m 크기, 7 cm 해상도의 heightmap을 로봇 중심에서 전방 0.2 m으로 이동 배치
- **보행 정책 학습**: Isaac Lab 환경에서 PPO 기반 deep reinforcement learning으로 heightmap을 observation space에 포함하는 23 DoF 관절 제어 정책 훈련

## Originality

- CNN과 GRU를 결합한 하이브리드 encoder-decoder 구조로 공간 특성 추출과 시간적 일관성을 동시에 달성하는 설계
- Spherical projection을 통한 효율적인 LiDAR 처리로 structured 2D range image 표현 활용
- 깊이 카메라와 LiDAR의 보완적 특성(조명 민감성 vs. 동적 환경 지연)을 명시적으로 활용하는 다중 센서 융합 전략
- 보행 정책의 학습 안정성과 지형 특성 감지 능력 사이의 trade-off를 체계적으로 분석하여 최적 heightmap 해상도 도출
- Reward shaping(발 공중 시간 대칭성, 슬라이딩 접촉 페널티)을 통해 heightmap 기반의 예측 행동 유도

## Limitation & Further Study

- 실제 로봇 플랫폼에서의 검증 부재 — Isaac Lab 시뮬레이션 환경에서만 평가되었으므로, 현실의 센서 노이즈, 보정 오차, 계산 리소스 제약에서의 성능 미지수
- Temporal context 길이(3.2초)의 선택 근거 부족 — 다양한 동적 환경(빠른 보행, 급격한 지형 변화)에서의 최적성 검증 필요
- 적응형 heightmap 해상도 — 고정된 7 cm 해상도가 모든 지형(계단, 불규칙한 암석 등)에 최적인지 미검증
- 계산량 및 지연 분석 부족 — spherical projection의 효율성 주장에도 불구하고, 실제 end-to-end latency 측정치 부재
- 후속 연구 방향: (1) 실제 인형로봇(예: Atlas, H1)에서의 현장 실험, (2) 시뮬-실제 도메인 간 격차(sim-to-real gap) 최소화 기법, (3) 동적 heightmap 해상도 적응 메커니즘 개발, (4) 극단적 날씨(눈, 빗물)나 투명/반사 물질에 대한 견고성 향상

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 인형로봇의 지형 인식과 보행 제어를 연결하는 실용적이고 체계적인 학습 기반 프레임워크로, 다중 센서 융합과 heightmap 표현의 최적화를 통해 명확한 성능 개선을 달성했다. 다만 실제 로봇에서의 검증과 지연 분석이 보충되면 산업 적용 가능성이 한층 높아질 것으로 예상된다.

## Related Papers

- 🔄 다른 접근: [[papers/1798_AME-2_Agile_and_Generalized_Legged_Locomotion_via_Attention-/review]] — 지형 인식을 위해 LiDAR 데이터를 활용하는 유사한 접근이지만 하나는 높이맵 생성, 다른 하나는 attention 기반 맵 인코딩을 사용한다.
- 🔗 후속 연구: [[papers/1843_CMR_Contractive_Mapping_Embeddings_for_Robust_Humanoid_Locom/review]] — 관찰 노이즈에 강건한 representation learning으로 LiDAR 기반 높이맵의 노이즈 문제를 해결할 수 있는 발전된 접근법이다.
- 🧪 응용 사례: [[papers/1939_Gait-Adaptive_Perceptive_Humanoid_Locomotion_with_Real-Time/review]] — 실시간 지형 높이맵 생성 기술을 실제 인지적 휴머노이드 보행에 적용한 구체적 사례이다.
- 🏛 기반 연구: [[papers/1802_An_Empirical_Evaluation_of_Four_Off-the-Shelf_Proprietary_Vi/review]] — 상용 VIO 시스템들의 성능 벤치마크가 LiDAR-카메라 융합 높이맵 생성에서 센서 선택의 기반 자료를 제공합니다.
- 🔗 후속 연구: [[papers/2010_HumanoidPano_Hybrid_Spherical_Panoramic-LiDAR_Cross-Modal_Pe/review]] — 구형 파노라마-LiDAR 교차 모달 인식을 높이맵 기반 지형 탐지와 결합한 확장된 접근법입니다.
- 🏛 기반 연구: [[papers/1802_An_Empirical_Evaluation_of_Four_Off-the-Shelf_Proprietary_Vi/review]] — 4개 상용 VIO 시스템의 성능 평가가 LiDAR-깊이 카메라 융합에서 센서 선택과 비교의 기반 자료를 제공합니다.
- 🔗 후속 연구: [[papers/1843_CMR_Contractive_Mapping_Embeddings_for_Robust_Humanoid_Locom/review]] — LiDAR 기반 지형 인식의 노이즈 문제를 contractive representation learning으로 해결하여 더 강건한 시스템을 구현한다.
- 🏛 기반 연구: [[papers/1850_Contrastive_Representation_Learning_for_Robust_Sim-to-Real_T/review]] — 높이맵 생성 기술이 지형 인식 정책 학습의 기반이 됩니다.
- 🔄 다른 접근: [[papers/1798_AME-2_Agile_and_Generalized_Legged_Locomotion_via_Attention-/review]] — 지형 인식을 위해 하나는 attention 기반 맵 인코딩, 다른 하나는 하이브리드 오토인코더를 사용하는 상호 보완적 접근법이다.
- 🏛 기반 연구: [[papers/1939_Gait-Adaptive_Perceptive_Humanoid_Locomotion_with_Real-Time/review]] — 퓨전 기반 견고한 높이맵 생성의 하이브리드 오토인코더 기술이 실시간 지형 인식의 핵심 기반입니다.
