---
title: "1755_Walk_the_PLANC_Physics-Guided_RL_for_Agile_Humanoid_Locomoti"
authors:
  - "Min Dai"
  - "William D. Compton"
  - "Junheng Li"
  - "Lizhi Yang"
  - "Aaron D. Ames"
date: "2026.01"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 감소된 차수의 발판 계획기와 Control Lyapunov Function (CLF) 기반 보상을 통해 물리학 기반 구조로 강화학습을 안내하여, 제한된 발판에서 인간형 로봇의 정밀한 보행을 달성한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Terrain_Foothold_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Dai et al._2026_Walk the PLANC Physics-Guided RL for Agile Humanoid Locomotion on Constrained Footholds.pdf"
---

# Walk the PLANC: Physics-Guided RL for Agile Humanoid Locomotion on Constrained Footholds

> **저자**: Min Dai, William D. Compton, Junheng Li, Lizhi Yang, Aaron D. Ames | **날짜**: 2026-01-09 | **URL**: [https://arxiv.org/abs/2601.06286](https://arxiv.org/abs/2601.06286)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2. A visual depiction of the model-guided RL architecture used to achieve stepping stones. The left column shows th*

이 논문은 감소된 차수의 발판 계획기와 Control Lyapunov Function (CLF) 기반 보상을 통해 물리학 기반 구조로 강화학습을 안내하여, 제한된 발판에서 인간형 로봇의 정밀한 보행을 달성한다.

## Motivation

- **Known**: 모델 기반 제어는 제약 조건 하에서 실행 가능한 동작을 계획하지만 불확실성에 취약하고, 강화학습은 불확실성 하에서 강건하지만 정밀한 제약 동작 발견에 어려움이 있다.
- **Gap**: 기존 강화학습 기반 접근법은 불연속 지형에서 정확한 발 배치와 단계 순서 결정에 실패하며, 모델 기반 방법은 불완전한 지각에 취약하다.
- **Why**: 인간형 로봇이 재난 지역이나 산업 환경과 같은 실제 환경에서 안전하게 배포되려면 정밀한 발판 위치 제어와 강건한 동작 적응이 모두 필요하다.
- **Approach**: 감소된 차수 stepping planner(Linear Inverted Pendulum 기반)로부터 동역학적으로 일관성 있는 동작 목표를 생성하고, 이를 CLF 보상을 통해 RL 훈련 과정에 통합하는 physics-guided RL 프레임워크를 제안한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Model-guided RL traversing constrained footholds on the Unitree G1*

- **물리학 기반 RL 통합**: 감소된 차수의 stepping planner와 CLF 보상 설계를 통해 RL 훈련 루프에 물리적 제약을 직접 통합하여 계산 효율성을 유지하면서 정밀성 확보
- **데이터셋 독립성**: 인간 모션 데이터셋 수집 및 재타겟팅 파이프라인 제거로 다중 환경에서 일반화된 보행 정책 개발
- **하드웨어 검증**: Unitree G1 인간형 로봇에서 무작위 높이 변화와 간격이 있는 stepping-stone 지형에서 모델 프리 기준선 대비 향상된 안정성, 정밀한 발 배치, 그리고 일관된 성능 개선 달성

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. A visual depiction of the model-guided RL architecture used to achieve stepping stones. The left column shows th*

- **Linear Inverted Pendulum (LIP) 기반 Stepping Planner**: 변하는 높이의 stepping stones를 가상 경사면으로 모델링하여 목표 orbital energy 선택을 통해 forward progression 보장
- **동작 생성**: 폐형 LIP 해를 통해 단계 지속 시간을 해석적으로 계산하여 CoM 목표 상태 도달 보장
- **CLF 기반 보상**: 감소된 차수 모델에서 생성된 reference trajectory와 실제 정책의 추적 오차를 최소화하도록 CLF 보상 설계
- **Teach-Student 패러다임**: 시뮬레이션에서 강화학습으로 정책 훈련 후 하드웨어에 배포
- **다중 지형 훈련**: 계단 상향, 계단 하향, 평면 돌, 높이 변화 돌 등 4가지 지형에서 학습

## Originality

- **Hybrid Model-RL 프레임워크**: 기존의 보상 형성만으로 정밀성을 유도하는 방식과 달리, 물리 기반 planner의 reference trajectories를 CLF를 통해 직접 RL 학습에 통합하는 구조적 혁신
- **stepping-stone 특화 설계**: Linear Inverted Pendulum의 orbital energy 보존 성질과 폐형 해를 활용하여 불연속 지형에 특화된 동작 목표 생성
- **지각 독립성**: 하드웨어에서 완벽한 지형 정보 없이도 학습된 정책으로 실행 가능, 기존 모델 기반 방법의 센서 의존성 제거

## Limitation & Further Study

- **Computational Demand**: LIP 기반 planner가 단순화된 모델이므로, 더 복잡한 비선형 동역학이나 높은 DoF 환경에서의 확장성 미검증
- **지형 제약**: Virtual slope 모델링은 stepping stones 지형에 최적화되어 있어, 극도로 불규칙한 또는 동적 지형에서의 일반화 능력 미지수
- **Training Data**: 4가지 기본 지형에서만 훈련되었으며, 더 다양한 지형 조합이나 극한 조건에서의 성능 미평가
- **후속연구**: (1) 더 높은 차수 모델(centroidal dynamics)과의 통합을 통한 일반화 확대, (2) 시각 기반 지형 인식을 포함한 완전한 end-to-end 파이프라인 개발, (3) 비선형 MPC와의 결합을 통한 동적 환경 대응

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 물리 기반 구조와 강화학습을 효과적으로 결합하여 stepping-stone 보행의 정밀성과 강건성 문제를 우아하게 해결하였으며, 하드웨어 검증과 오픈소스 공개를 통해 높은 실용적 가치를 제공한다.

## Related Papers

- 🔄 다른 접근: [[papers/1789_Adapting_Humanoid_Locomotion_over_Challenging_Terrain_via_Tw/review]] — 둘 다 challenging terrain 보행을 다루지만 PLANC는 물리학 기반 구조로, Transformer 접근법은 sequence modeling으로 해결한다.
- 🔗 후속 연구: [[papers/1798_AME-2_Agile_and_Generalized_Legged_Locomotion_via_Attention-/review]] — AME-2의 attention 기반 맵 인코딩과 불확실성 인식 elevation mapping이 PLANC의 발판 계획 정확도를 향상시킬 수 있다.
- 🧪 응용 사례: [[papers/2162_TTT-Parkour_Rapid_Test-Time_Training_for_Perceptive_Robot_Pa/review]] — TTT-Parkour의 실시간 적응형 parkour 기법이 PLANC의 제한된 발판 보행을 더 복잡한 지형으로 확장하는 데 활용될 수 있다.
- 🔄 다른 접근: [[papers/1789_Adapting_Humanoid_Locomotion_over_Challenging_Terrain_via_Tw/review]] — 둘 다 challenging terrain 보행을 다루지만 Transformer는 sequence modeling에, PLANC는 physics-guided RL에 중점을 둔다.
- 🔄 다른 접근: [[papers/1798_AME-2_Agile_and_Generalized_Legged_Locomotion_via_Attention-/review]] — 둘 다 민첩하고 일반화된 지형 보행을 다루지만 AME-2는 attention 기반에, PLANC는 physics-guided RL에 중점을 둔다.
- 🔄 다른 접근: [[papers/2004_Humanoid_Whole-Body_Locomotion_on_Narrow_Terrain_via_Dynamic/review]] — 민첩한 보행을 이 논문은 좁은 지형에, Walk the PLANC는 물리 가이드 RL로 각각 접근한다.
