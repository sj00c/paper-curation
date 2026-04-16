---
title: "1668_SEEC_Stable_End-Effector_Control_with_Model-Enhanced_Residua"
authors:
  - "Jaehwi Jang"
  - "Zhuoheng Wang"
  - "Ziyi Zhou"
  - "Feiyang Wu"
  - "Ye Zhao"
date: "2025.09"
doi: "10.48550/arXiv.2509.21231"
arxiv: ""
score: 4.0
essence: "SEEC는 model-enhanced residual learning을 통해 휴머노이드 로봇의 보행 중 팔 end-effector를 안정적으로 제어하는 프레임워크로, 하지 유도 교란에 대해 모델 기반 보상 신호를 RL 정책에 통합한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Jang et al._2025_SEEC Stable End-Effector Control with Model-Enhanced Residual Learning for Humanoid Loco-Manipulati.pdf"
---

# SEEC: Stable End-Effector Control with Model-Enhanced Residual Learning for Humanoid Loco-Manipulation

> **저자**: Jaehwi Jang, Zhuoheng Wang, Ziyi Zhou, Feiyang Wu, Ye Zhao | **날짜**: 2025-09-25 | **DOI**: [10.48550/arXiv.2509.21231](https://doi.org/10.48550/arXiv.2509.21231)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: System framework overview of SEEC. Our SEEC framework decouples the humanoid loco-manipulation controller into u*

SEEC는 model-enhanced residual learning을 통해 휴머노이드 로봇의 보행 중 팔 end-effector를 안정적으로 제어하는 프레임워크로, 하지 유도 교란에 대해 모델 기반 보상 신호를 RL 정책에 통합한다.

## Motivation

- **Known**: 모델 기반 제어기는 정확한 end-effector 제어를 달성하지만 실제 마찰 및 백래시 같은 요소 모델링에 어려움이 있으며, RL 기반 방법은 비현실적 요소를 더 잘 완화하지만 훈련 조건에 과적합되는 경향이 있다.
- **Gap**: 기존 end-to-end RL 접근법은 제어되지 않는 팔 움직임을 야기하고 예측 불가능한 보행 제어기에 적응하지 못하며, 정책 최적화만으로는 보상 전략 발견에 의존한다.
- **Why**: 휴머노이드 로봇이 실제 환경에서 물체를 운반하거나 협력 작업을 수행하려면 보행 중 정밀하고 안정적인 manipulation이 필수적이며, 기저부 움직임으로 인한 end-effector 가속도 증폭은 추적 오류와 접촉력 불안정성을 초래한다.
- **Approach**: 모델 기반 제어로부터 해석적 가속도 보상 신호를 추출하여 RL 정책으로 증류하고, 섭동 생성기를 통해 다양한 보행 패턴을 상체 정책 훈련에 노출시켜 모듈식 설계로 미학습 제어기에도 일반화한다.

## Achievement


- **Model-Enhanced Residual Learning**: 모델 기반 전문성과 학습 기반 적응성을 통합하여 정확한 가속도 보상과 모델 부정확성 및 파라미터 불확실성 극복
- **교란 적응 및 무재훈련 전이**: Perturbation 생성 전략으로 다양한 보행 관련 교란에 노출되어 미학습 보행 제어기로의 zero-shot 전이 달성
- **실제 로봇 배포**: Booster T1 휴머노이드 로봇에서 시뮬레이션-현실 전이를 통해 다양한 loco-manipulation 작업에서 기준선 대비 우수한 성능 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: System framework overview of SEEC. Our SEEC framework decouples the humanoid loco-manipulation controller into u*

- 상하체 제어기를 분리하여 하체는 보행, 상체는 보행 교란 보상에 집중
- 모델 기반 동역학으로부터 필요한 보상 토크를 계산하여 residual policy 훈련의 목표로 설정
- Base movement 데이터 생성 및 perturbation 생성기를 통해 훈련 중 다양한 보행 패턴 시뮬레이션
- 상체 정책이 특정 하체 제어기에 의존하지 않도록 구조화하여 모듈식 재사용성 확보
- IsaacLab 시뮬레이터에서 훈련 후 Booster T1로 직접 배포

## Originality

- **모듈식 분리 설계**: 기존 joint training 대신 perturbation 생성으로 상체 정책이 독립적으로 다양한 교란에 적응 가능하도록 설계
- **모델-학습 하이브리드**: 단순 보상 페널티가 아닌 모델 기반 보상 신호의 명시적 증류로 더 원칙적인 접근
- **무재훈련 미학습 제어기 적응**: 섭동 데이터 생성 전략으로 훈련 시 미경험한 보행 제어기에도 general하게 동작
- **Full humanoid 실제 배포**: 이론을 실제 Booster T1 플랫폼에서 검증한 첫 사례

## Limitation & Further Study

- **Arm-to-base back-coupling 무시**: 팔이 동역학적으로 가볍다는 가정이 더 무거운 manipulation이나 큰 보상 토크에서 성립하지 않을 수 있음
- **보행 제어기 안정성 의존**: Robust 보행 제어기 가정으로, 불안정한 보행 시스템에서는 적용 제약 가능
- **실제 환경 평가 부재**: 시뮬레이션과 제한된 실제 로봇 실험으로 복잡한 실제 환경에서의 성능 미검증
- **후속 연구 방향**: (1) 양방향 coupling 모델링으로 일반화, (2) 적응적 dynamic model 학습, (3) 불규칙한 지형과 접촉 동역학 포함한 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SEEC는 모델 기반 제어의 정밀성과 RL의 적응성을 효과적으로 결합하며, perturbation 생성을 통한 모듈식 설계로 미학습 제어기에도 robust하게 전이되는 점에서 높은 독창성을 보인다. 실제 휴머노이드 로봇 배포와 다양한 loco-manipulation 작업 검증으로 실용성도 입증하였다.

## Related Papers

- 🔄 다른 접근: [[papers/1980_HiWET_Hierarchical_World-Frame_End-Effector_Tracking_for_Lon/review]] — model-enhanced residual learning vs hierarchical world-frame tracking이라는 다른 end-effector 제어 방식입니다.
- 🔗 후속 연구: [[papers/1922_FALCON_Learning_Force-Adaptive_Humanoid_Loco-Manipulation/review]] — 안정적인 팔 제어가 force-adaptive manipulation으로 확장되어 더 복잡한 조작이 가능해집니다.
- 🏛 기반 연구: [[papers/1980_HiWET_Hierarchical_World-Frame_End-Effector_Tracking_for_Lon/review]] — SEEC의 모델 강화 잔차 기반 end-effector 제어가 HiWET의 세계 좌표계 추적 시스템의 핵심 토대가 된다.
- 🏛 기반 연구: [[papers/2149_TOP_Time_Optimization_Policy_for_Stable_and_Accurate_Standin/review]] — SEEC의 stable end-effector control이 TOP의 상체 동작 시간 최적화에서 end-effector 안정성 보장의 기술적 토대를 제공합니다.
