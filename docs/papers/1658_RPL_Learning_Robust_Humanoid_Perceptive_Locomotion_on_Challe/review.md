---
title: "1658_RPL_Learning_Robust_Humanoid_Perceptive_Locomotion_on_Challe"
authors:
  - "Yuanhang Zhang"
  - "Younggyo Seo"
  - "Juyue Chen"
  - "Yifu Yuan"
  - "Koushil Sreenath"
date: "2026.02"
doi: ""
arxiv: ""
score: 4.0
essence: "RPL은 두 단계 학습 프레임워크로 terrain-specific 전문가 정책을 depth 카메라 기반 transformer 정책으로 증류하여, 복잡한 지형에서 payload를 탑재한 상태의 견고한 다방향 인형로봇 보행을 실현한다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/LiDAR_Terrain_Perception"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2026_RPL Learning Robust Humanoid Perceptive Locomotion on Challenging Terrains.pdf"
---

# RPL: Learning Robust Humanoid Perceptive Locomotion on Challenging Terrains

> **저자**: Yuanhang Zhang, Younggyo Seo, Juyue Chen, Yifu Yuan, Koushil Sreenath, Pieter Abbeel, Carmelo Sferrazza, Karen Liu, Rocky Duan, Guanya Shi | **날짜**: 2026-02-03 | **URL**: [https://arxiv.org/abs/2602.03002](https://arxiv.org/abs/2602.03002)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2.*

RPL은 두 단계 학습 프레임워크로 terrain-specific 전문가 정책을 depth 카메라 기반 transformer 정책으로 증류하여, 복잡한 지형에서 payload를 탑재한 상태의 견고한 다방향 인형로봇 보행을 실현한다.

## Motivation

- **Known**: 인형로봇 보행 분야에서는 forward 카메라 기반 단일 방향 이동이 주로 연구되었으며, 전통적인 LiDAR 기반 매핑 방식은 상태 추정의 노이즈와 지연 문제를 야기한다.
- **Gap**: 비대칭적 다중 카메라 입력 조건에서의 다방향 보행 및 보행과 조작을 동시에 수행하면서 payload 견고성을 유지하는 연구가 미흡하며, 다중 depth 렌더링의 계산 효율성도 제한적이다.
- **Why**: 인형로봇이 실제 환경에서 다양한 지형을 효율적으로 횡단하면서 물품을 운반하는 능력은 일상 작업 수행의 필수 요소이기 때문이다.
- **Approach**: Stage 1에서 privileged height map을 사용한 terrain-specific 전문가 정책들을 학습하고, Stage 2에서 이들을 multi-view depth 입력 기반의 통합 transformer 정책으로 증류하며, 증류 과정에서 depth feature scaling based on velocity commands(DFSV)와 random side masking(RSM) 기법을 적용한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **효율적 다중 depth 렌더링 시스템**: dynamic robot mesh와 static terrain mesh에 대해 ray-casting을 수행하면서 현실적인 센서 지연, 노이즈, dropout을 모델링하여 기존 시뮬레이터 대비 5배 속도 향상 달성
- **견고한 다방향 보행**: DFSV와 RSM 기법을 통해 비대칭 depth 관측과 미학습 지형 너비에서도 안정적인 양방향 보행 실현
- **실제 로봇 검증**: Unitree G1 인형로봇에서 20° 경사면, 22-30cm 다양한 계단, 60cm 간격 stepping stones 등 복잡한 지형에서 2kg payload 탑재 상태의 안정적 보행 입증
- **decoupled 제어 구조**: FALCON 프레임워크 기반으로 lower-body 보행 정책과 upper-body 조작 정책을 분리하여 전체 신체 제어의 효율성 및 성능 향상

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- Stage 1: Terrain-specific 전문가 정책 학습 - 각 지형 유형(경사면, 계단 상행/하행, stepping stones)별로 privileged height-map 관측을 사용하여 end-effector force perturbation 하에서 decoupled locomotion과 manipulation 기술 습득
- Stage 2: Knowledge distillation - 전문가 정책들을 front/back dual depth cameras 입력을 받는 unified transformer 정책으로 압축
- Depth feature scaling based on velocity commands (DFSV): 명령된 속도에 따라 지각 특성을 적응적으로 조절하여 비대칭 시각 입력 간의 분포 편이(distribution shift) 감소
- Random side masking (RSM): 깊이 이미지의 양측 지형 영역을 변동하는 너비로 랜덤하게 마스킹하여 미학습 지형 너비에 대한 견고성 향상
- Multi-depth rendering 최적화: NVIDIA Warp 기반의 병렬 ray-casting으로 dynamic mesh(자기 폐색 처리)와 static mesh 동시 처리, 현실적 센서 특성 모델링

## Originality

- 비대칭 다중 카메라 입력 처리의 체계적 접근 - DFSV와 RSM을 통해 서로 다른 카메라가 보는 지형 구조의 차이를 정책 학습 단계에서 명시적으로 처리
- Dynamic mesh를 포함한 확장된 depth 렌더링 - 로코-조작(loco-manipulation) 중 발생하는 자기 폐색을 시뮬레이션에서 정확히 모델링
- Privileged information 활용의 효과적 설계 - Stage 1에서만 height map을 사용하고 Stage 2에서는 일반화 가능한 depth 기반 정책으로 전환하는 이원적 학습 구조
- 실제 로봇 검증의 포괄성 - 다양한 terrain width 및 payload 조건에서의 견고성 평가

## Limitation & Further Study

- Depth camera 기반 정책의 본질적 한계 - 희소하고 불연속적인 footholds(stepping stones)에 대해 제한된 전방 시야(lookahead)로 인한 잠재적 실패 케이스 존재 가능
- Sim-to-real gap 해소의 완전성 - 시뮬레이션에서 모델링한 센서 노이즈와 현실의 실제 depth 센서 오류 간 불일치 가능성
- 확장성 제약 - 현재 Unitree G1 로봇 플랫폼 중심으로 검증되었으므로 다른 인형로봇 모델로의 일반화 정도 미정
- 후속 연구 방향: (1) LiDAR 등 추가 센서 modality와의 결합, (2) 더 극단적 지형(암벽, 비정형 지형)으로의 확장, (3) 더 무거운 payload 조건에서의 견고성 개선

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 다단계 학습과 효율적 시뮬레이션을 통해 인형로봇의 복잡 지형 다방향 보행 문제를 체계적으로 해결하며, 특히 비대칭 다중 센서 입력 처리 기법과 payload 견고성 검증에서 실질적 기여를 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1619_PolygMap_A_Perceptive_Locomotion_Framework_for_Humanoid_Robo/review]] — RPL과 PolygMap 모두 지각 기반 휴머노이드 보행을 다루지만 전자는 복잡한 지형에서의 견고성에, 후자는 계단 등반에 특화되어 있다
- 🏛 기반 연구: [[papers/1884_DPL_Depth-only_Perceptive_Humanoid_Locomotion_via_Realistic/review]] — RPL의 depth 카메라 기반 transformer 정책이 DPL의 depth-only perceptive locomotion 방법론을 확장한 것이다
- 🔗 후속 연구: [[papers/1978_Hiking_in_the_Wild_A_Scalable_Perceptive_Parkour_Framework_f/review]] — RPL의 복잡한 지형 보행이 Hiking in the Wild의 scalable perceptive parkour와 결합되어 더 동적인 야외 환경 탐험을 가능하게 한다
- 🔄 다른 접근: [[papers/1939_Gait-Adaptive_Perceptive_Humanoid_Locomotion_with_Real-Time/review]] — depth camera와 LiDAR라는 서로 다른 센서를 사용한 지형 인식 기반 locomotion 접근법입니다.
- 🔗 후속 연구: [[papers/1657_Robust_Humanoid_Walking_on_Compliant_and_Uneven_Terrain_with/review]] — compliant terrain 보행 연구가 payload 추가와 복잡한 지형으로 더욱 도전적인 환경으로 확장됩니다.
- 🔄 다른 접근: [[papers/1619_PolygMap_A_Perceptive_Locomotion_Framework_for_Humanoid_Robo/review]] — 두 논문 모두 지각 기반 휴머노이드 보행을 다루지만 PolygMap은 계단 등반에, RPL은 복잡한 지형에서의 견고한 보행에 집중한다
- 🔗 후속 연구: [[papers/1850_Contrastive_Representation_Learning_for_Robust_Sim-to-Real_T/review]] — 도전적 지형에서의 강건한 지각 기반 보행을 더욱 발전시킵니다.
- 🔄 다른 접근: [[papers/2056_Learning_Humanoid_Locomotion_over_Challenging_Terrain/review]] — 도전적 지형에서의 인식 기반 보행에서 RPL은 강건성에, PIM은 내부 모델에 집중
- 🔄 다른 접근: [[papers/2060_Learning_Perceptive_Humanoid_Locomotion_over_Challenging_Ter/review]] — 거친 지형에서의 인식 기반 휴머노이드 보행을 다른 접근법으로 해결한다.
- 🔗 후속 연구: [[papers/2160_Traversing_Narrow_Paths_A_Two-Stage_Reinforcement_Learning_F/review]] — 도전적인 지형에서의 견고한 지각적 이동 학습이 좁은 경로 통과를 위한 두 단계 강화학습 프레임워크를 더 복잡한 환경으로 확장할 수 있습니다.
