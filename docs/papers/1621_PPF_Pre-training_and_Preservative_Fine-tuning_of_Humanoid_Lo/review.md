---
title: "1621_PPF_Pre-training_and_Preservative_Fine-tuning_of_Humanoid_Lo"
authors:
  - "Hyunyoung Jung"
  - "Zhaoyuan Gu"
  - "Ye Zhao"
  - "Hae-Won Park"
  - "Sehoon Ha"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "본 연구는 모델 기반 제어기의 모방학습(Pre-training)과 강화학습을 결합하되, 모델 가정이 성립하는 상태에서만 정규화하는 MAR(Model-Assumption-based Regularization)을 통해 인간형 로봇의 보행 정책을 학습하는 PPF 프레임워크를 제안한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Jung et al._2025_PPF Pre-training and Preservative Fine-tuning of Humanoid Locomotion via Model-Assumption-based Reg.pdf"
---

# PPF: Pre-training and Preservative Fine-tuning of Humanoid Locomotion via Model-Assumption-based Regularization

> **저자**: Hyunyoung Jung, Zhaoyuan Gu, Ye Zhao, Hae-Won Park, Sehoon Ha | **날짜**: 2025-04-14 | **URL**: [https://arxiv.org/abs/2504.09833](https://arxiv.org/abs/2504.09833)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

본 연구는 모델 기반 제어기의 모방학습(Pre-training)과 강화학습을 결합하되, 모델 가정이 성립하는 상태에서만 정규화하는 MAR(Model-Assumption-based Regularization)을 통해 인간형 로봇의 보행 정책을 학습하는 PPF 프레임워크를 제안한다.

## Motivation

- **Known**: 기존 연구들은 모델 기반 제어(MPC)와 학습 기반 접근법을 각각 또는 혼합하여 이족 보행에 적용했으나, 학습 단계에서 재앙적 망각(catastrophic forgetting)으로 인해 사전학습된 주기적 보행 패턴을 잃는 문제가 있었다.
- **Gap**: 특히 인간형 로봇은 사족 로봇보다 불안정한 역학을 가지므로, 강화학습 파인튜닝 시 원본 모방학습 행동의 손실을 방지하면서도 모델 기반 제어기의 한계를 넘어 더 복잡한 지형과 고속 보행을 처리해야 한다.
- **Why**: 인간형 로봇이 다양한 실제 환경에서 신뢰할 수 있게 작동하려면 강건한 보행 정책이 필수이며, 특히 모방학습과 강화학습의 장점을 결합하면서 재앙적 망각을 완화하는 방법이 중요하다.
- **Approach**: 본 연구는 ALIP 모델 기반 제어기의 상태 가정(일정한 높이, 수직 속도 0)의 위반 여부를 감지하여, 가정이 성립할 때만 모델 기반 제어기 행동으로의 정규화 강도를 조정하는 적응적 MAR을 제안한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **MAR 기반 적응 정규화**: 모델 가정 위반 정도를 측정하여 동적으로 정규화 가중치를 조정함으로써 재앙적 망각 완화
- **고속 보행 달성**: 시뮬레이션 및 실제 로봇(Digit)에서 1.5 m/s의 전진 속도 달성
- **다양한 지형 강건성**: 미끄러운 지면(poppy seeds, olive oil), 경사면, 울퉁불퉁한 지형, 모래 지형 등에서 안정적 보행 성공
- **성능 개선**: 기준 방법들 대비 높은 속도 추적 성능을 uneven 및 sloped 지형에서 달성

## How

![Figure 3](figures/fig3.webp)

*Fig. 3.*

- Pre-training 단계: MBC(ALIP 기반 발 배치 제어기 + 전신 역동역학 제어기)의 행동을 신경망 정책으로 모방
- Fine-tuning 단계: 강화학습을 통해 정책을 개선하되, 모델 가정 위반도(z ≠ z̄ 또는 ż ≠ 0 등)를 계산
- MAR 적용: 모델 가정이 성립하는 상태(낮은 위반도)에서는 높은 정규화 가중치로 MBC 행동에 정렬, 가정 위반 시 가중치 감소로 정책의 개선 허용
- 하이퍼파라미터 조정: 정규화 강도와 보상 함수를 조정하여 속도, 안정성, 강건성의 균형 달성
- Sim-to-real 전이: 시뮬레이션에서 학습된 정책을 실제 Digit 로봇에 직접 적용

## Originality

- 기존의 고정 정규화 계수 대신 모델 가정 위반도에 따른 **동적 적응 정규화** 제안
- ALIP 모델의 명시적 가정(일정 높이, 수직 속도 0)을 정량적 위반 지표로 변환하여 정규화에 활용한 점이 창신
- 인간형 로봇의 불안정성을 고려한 모델-학습 기반 하이브리드 접근으로, 기존 사족 로봇 방법의 단순 확장이 아닌 인간형 특화 개선

## Limitation & Further Study

- ALIP 모델 기반 제어기에 의존하므로, 다른 모델 기반 제어기(예: LIPM, full-body dynamics)에 대한 적용성 검증 부족
- 모델 가정 위반도 계산 및 정규화 가중치 결정의 수학적 명확성 부족(구체적 수식이나 휴리스틱 기준 명시 필요)
- 실제 하드웨어 실험이 제한적(Digit 로봇 1대만 사용)이고, 다양한 환경 변수(예: 로봇 무게, 동역학 변화)에 대한 일반화 성능 미평가
- **후속 연구**: 다양한 모델 기반 제어기로의 확장, 더 강건한 모델 가정 위반도 지표 개발, 대규모 하드웨어 배포 시 도메인 적응 방법 추가 연구 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 모델 기반과 학습 기반 제어의 장점을 결합하면서 재앙적 망각을 완화하는 MAR이라는 창신적 정규화 기법을 제안하며, 실제 인간형 로봇에서 1.5 m/s의 고속 보행과 다양한 지형 강건성을 달성하여 실용적 가치가 높다.

## Related Papers

- 🔄 다른 접근: [[papers/1881_Distillation-PPO_A_Novel_Two-Stage_Reinforcement_Learning_Fr/review]] — Model-based pre-training과 RL 결합을 two-stage distillation 접근법으로 해결
- 🏛 기반 연구: [[papers/1905_Embedding_Classical_Balance_Control_Principles_in_Reinforcem/review]] — Classical control principles를 RL에 통합하는 방법론적 기반 제공
- 🏛 기반 연구: [[papers/1881_Distillation-PPO_A_Novel_Two-Stage_Reinforcement_Learning_Fr/review]] — humanoid locomotion의 pre-training과 fine-tuning 방법론이 Distillation-PPO의 2단계 프레임워크 설계에 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1916_Evolutionary_Continuous_Adaptive_RL-Powered_Co-Design_for_Hu/review]] — 둘 다 하드웨어와 제어 정책의 동시 최적화를 다루지만 EA-CoRL은 진화 알고리즘을, PPF는 사전학습을 사용한다.
- 🔗 후속 연구: [[papers/1962_H-Zero_Cross-Humanoid_Locomotion_Pretraining_Enables_Few-sho/review]] — PPF의 pre-training과 fine-tuning 개념을 cross-humanoid에서 few-shot novel embodiment로의 일반화까지 확장한 포괄적인 프레임워크입니다.
