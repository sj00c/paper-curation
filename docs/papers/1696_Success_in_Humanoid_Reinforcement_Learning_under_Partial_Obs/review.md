---
title: "1696_Success_in_Humanoid_Reinforcement_Learning_under_Partial_Obs"
authors:
  - "Wuhao Wang"
  - "Zhiyong Chen"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "부분 관찰 환경에서 고정 길이 과거 관찰 시퀀스를 병렬로 처리하는 novel history encoder를 제안하여, Gymnasium Humanoid-v4 환경에서 부분 관찰 하에서의 안정적인 humanoid 정책 학습을 처음으로 성공시켰다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Terrain_Foothold_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang and Chen_2025_Success in Humanoid Reinforcement Learning under Partial Observation.pdf"
---

# Success in Humanoid Reinforcement Learning under Partial Observation

> **저자**: Wuhao Wang, Zhiyong Chen | **날짜**: 2025-07-25 | **URL**: [https://arxiv.org/abs/2507.18883](https://arxiv.org/abs/2507.18883)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 summarizes the training performance under three partial observability configurations:*

부분 관찰 환경에서 고정 길이 과거 관찰 시퀀스를 병렬로 처리하는 novel history encoder를 제안하여, Gymnasium Humanoid-v4 환경에서 부분 관찰 하에서의 안정적인 humanoid 정책 학습을 처음으로 성공시켰다.

## Motivation

- **Known**: 강화학습은 로봇 제어에 널리 적용되어 왔으나, 부분 관찰성(partial observability) 하에서의 효과적인 정책 학습은 여전히 미해결 과제이며, 특히 humanoid 같은 고차원 작업에서 어렵다. LSTM, Mamba 등 RNN 기반 메모리 접근법이 단순 POMDP 벤치마크에서 성공했으나 humanoid 같은 복잡한 환경에서는 미증명 상태다.
- **Gap**: 기존 연구는 부분 관찰 환경에서 humanoid 정책의 안정적 학습을 입증하지 못했으며, RMF와 ODERMF 같은 최신 메모리 기반 POMDP 방법들도 고차원 humanoid 제어에서 실패한다.
- **Why**: Humanoid 로봇의 제어는 현실의 많은 로봇 시스템에서 센싱이 불완전한 부분 관찰 상황에서 이루어지므로, 부분 관찰 하에서의 안정적 학습이 실제 로봇 제어에 필수적이다.
- **Approach**: 표준 model-free 알고리즘(TD3)에 통합되는 novel history encoder를 제안하며, 이는 과거 관찰의 고정 길이 시퀀스를 순차적 메모리 메커니즘 대신 병렬로 처리하여 숨겨진 상태를 복구한다.

## Achievement


- **부분 관찰 환경에서의 첫 성공**: Gymnasium Humanoid-v4에서 부분 관찰(전체 상태의 1/3~2/3만 사용) 하에서도 완전 관찰 TD3 베이스라인과 동등한 성능 달성
- **기존 방법 대비 우월성**: RMF와 ODERMF는 단일 속성 제거에서도 실패하지만, 제안 방법은 모든 부분 관찰 구성에서 안정적으로 수렴
- **정보 복구 및 중복성 활용**: Remove M, Remove F 설정에서 완전 관찰 베이스라인을 초과하는 성능으로 인코더가 누락된 정보를 효과적으로 복구함을 시사
- **로봇 특성 적응성**: 학습된 정책이 신체 부위 질량 변화 같은 로봇 속성 변화에 적응할 수 있음을 보임

## How


- 상태 공간의 348개 차원을 position, velocity, mass/inertia, force 네 가지 의미론적 속성으로 분류
- 각 속성을 선택적으로 제거하여 부분 관찰 설정 생성 (단일 속성 제거: ~70%, 이중 속성 제거: ~35% 차원 유지)
- 고정 길이 과거 관찰 시퀀스를 병렬로 처리하는 history encoder를 설계하여 각 타임스텝을 동등하게 취급
- TD3 기반 model-free RL 프레임워크에 인코더 통합, 동일한 네트워크 용량과 하이퍼파라미터로 RMF, ODERMF와 공정하게 비교
- 1M 또는 3M 그래디언트 스텝으로 5개 random seed로 학습, 에피소드 리턴 곡선 평균화로 평가

## Originality

- 부분 관찰 humanoid 제어에서의 첫 성공 달성 - 기존 RNN 기반 메모리 방법들의 한계를 극복
- 순차 처리 대신 병렬 처리를 사용하는 novel history encoder 제안 - 기존 LSTM/Mamba 같은 순차 메모리 아키텍처와 근본적으로 다른 접근
- 고차원 복잡 제어 환경에서의 POMDP 해결 - 단순 벤치마크를 넘어 실제적 로봇 제어 규모의 문제 해결

## Limitation & Further Study

- 제안된 history encoder의 구체적 아키텍처와 메커니즘이 논문 본문에서 충분히 설명되지 않았으며, 향후 상세 보고서에서 다룬다고 언급
- 부분 관찰 시뮬레이션에서만 평가되었으며, 실제 로봇 하드웨어에서의 검증 부재
- 네 가지 의미론적 속성 제거 방식만 평가했으며, 다른 부분 관찰 패턴(예: 노이즈, 센싱 오류)의 효과 미검토
- GPU 활용률이 ~10%에 불과하여 환경 상호작용의 CPU 병목 현상을 보임 - 확장성 개선 여지
- 향후 연구는 실제 부분 관찰 특성이 있는 실제 로봇 플랫폼으로의 이전과 다양한 센싱 제약 하에서의 성능 평가가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 3/5
- Overall: 4/5

**총평**: 본 연구는 부분 관찰 환경에서의 고차원 humanoid 제어라는 미해결 문제를 처음으로 성공적으로 해결하며, 병렬 history encoder를 통해 기존 RNN 기반 메모리 방법들을 압도적으로 능가한다. 다만 방법론의 구체적 설명이 부족하고 실제 로봇 검증이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1667_SCDP_Learning_Humanoid_Locomotion_from_Partial_Observations/review]] — 둘 다 부분 관찰 환경에서의 humanoid 학습을 다루지만 SCDP는 다른 관찰 처리 방식을 제안합니다.
- 🔗 후속 연구: [[papers/1984_HoRD_Robust_Humanoid_Control_via_History-Conditioned_Reinfor/review]] — HoRD의 history-conditioned 방법론이 부분 관찰 문제 해결에 더 정교한 접근을 제공합니다.
- 🔄 다른 접근: [[papers/1746_VB-Com_Learning_Vision-Blind_Composite_Humanoid_Locomotion_A/review]] — 시각 정보 결손 상황에서의 로봇 제어라는 유사한 문제를 다른 방식으로 해결합니다.
- 🔄 다른 접근: [[papers/1694_SteadyTray_Learning_Object_Balancing_Tasks_in_Humanoid_Tray/review]] — 둘 다 잔차 학습을 사용하지만 부분 관찰 환경에서의 일반적 학습 vs 특정 균형 작업으로 적용 범위가 다르다
- 🔄 다른 접근: [[papers/1619_PolygMap_A_Perceptive_Locomotion_Framework_for_Humanoid_Robo/review]] — 둘 다 부분 관찰 상황을 다루지만 고정 길이 과거 관찰 vs 멀티모달 센서 융합으로 접근이 다르다
- 🏛 기반 연구: [[papers/1688_Spectral_Normalization_for_Lipschitz-Constrained_Policies_on/review]] — Lipschitz 연속성을 통한 안정적 학습 기법을 부분 관찰 환경으로 확장하여 고정 길이 과거 관찰 시퀀스를 활용한 안정적 정책 학습을 구현했다.
- 🔗 후속 연구: [[papers/1692_StageACT_Stage-Conditioned_Imitation_for_Robust_Humanoid_Doo/review]] — 부분 관찰 환경에서의 강건성 향상을 작업 단계 정보 없이도 달성할 수 있는 history encoder 기법으로 일반화하여 적용했다.
- 🔗 후속 연구: [[papers/2023_InEKFormer_A_Hybrid_State_Estimator_for_Humanoid_Robots/review]] — 부분 관찰 환경에서의 상태 추정 개념을 강화학습 정책 학습으로 확장하여 과거 관찰 정보를 효과적으로 활용하는 방법을 제시했다.
- 🏛 기반 연구: [[papers/1667_SCDP_Learning_Humanoid_Locomotion_from_Partial_Observations/review]] — 부분 관찰 하에서의 휴머노이드 강화학습 성공에 대한 기초적인 연구를 제공한다.
- 🏛 기반 연구: [[papers/1688_Spectral_Normalization_for_Lipschitz-Constrained_Policies_on/review]] — 부분 관찰 환경에서의 안정적 학습 기법을 Lipschitz 연속성 관점에서 보완하여 메모리 효율성과 성능을 동시에 개선했다.
- 🔗 후속 연구: [[papers/1692_StageACT_Stage-Conditioned_Imitation_for_Robust_Humanoid_Doo/review]] — 부분 관찰성 환경에서의 강건성 향상 개념을 작업 단계 정보를 조건으로 하는 모방 학습으로 구체화하여 성능을 개선했다.
- 🔗 후속 연구: [[papers/1694_SteadyTray_Learning_Object_Balancing_Tasks_in_Humanoid_Tray/review]] — 트레이 운반의 잔차 강화학습과 부분 관찰 하에서의 안정적 학습을 결합하면 더 견고한 동적 조작이 가능하다
- 🔗 후속 연구: [[papers/1619_PolygMap_A_Perceptive_Locomotion_Framework_for_Humanoid_Robo/review]] — PolygMap의 지각 기반 보행 계획과 부분 관찰 하에서의 안정적인 휴머노이드 학습을 결합하면 더 견고한 계단 등반이 가능하다
- 🏛 기반 연구: [[papers/1632_RAPT_Model-Predictive_Out-of-Distribution_Detection_and_Fail/review]] — RAPT의 OOD 감지 시스템이 Success in Humanoid RL의 부분 관측 환경에서 정책 신뢰성 모니터링에 필수적이다
- 🔄 다른 접근: [[papers/1746_VB-Com_Learning_Vision-Blind_Composite_Humanoid_Locomotion_A/review]] — 부분 관찰과 시각 결손이라는 유사한 센서 제약 상황에서 서로 다른 해결책을 제시합니다.
- 🧪 응용 사례: [[papers/2062_Learning_Smooth_Humanoid_Locomotion_through_Lipschitz-Constr/review]] — 부분 관측 하에서의 강화학습을 스무스 보행 제어에 적용한 실용적 접근
