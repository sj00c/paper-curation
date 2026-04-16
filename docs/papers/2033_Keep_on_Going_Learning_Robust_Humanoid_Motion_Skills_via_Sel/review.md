---
title: "2033_Keep_on_Going_Learning_Robust_Humanoid_Motion_Skills_via_Sel"
authors:
  - "Yang Zhang"
  - "Zhanxiang Cao"
  - "Buqing Nie"
  - "Haoyang Li"
  - "Zhong Jiangwei"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "인간형 로봇의 장시간 안정적 운영을 위해 선택적 적대적 공격(SA2RT)을 통한 견고한 동작 제어 정책을 학습하는 방법을 제안한다. 공격 예산 제약 하에서 취약한 상태와 행동을 찾아 표적화된 섭동을 가하여 정책을 강화한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_Keep on Going Learning Robust Humanoid Motion Skills via Selective Adversarial Training.pdf"
---

# Keep on Going: Learning Robust Humanoid Motion Skills via Selective Adversarial Training

> **저자**: Yang Zhang, Zhanxiang Cao, Buqing Nie, Haoyang Li, Zhong Jiangwei, Qiao Sun, Xiaoyi Hu, Xiaokang Yang, Yue Gao | **날짜**: 2025-07-11 | **URL**: [https://arxiv.org/abs/2507.08303](https://arxiv.org/abs/2507.08303)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of the SA2RT. The SAP identifies vulnerabilities in motion states and generates adversarial samples b*

인간형 로봇의 장시간 안정적 운영을 위해 선택적 적대적 공격(SA2RT)을 통한 견고한 동작 제어 정책을 학습하는 방법을 제안한다. 공격 예산 제약 하에서 취약한 상태와 행동을 찾아 표적화된 섭동을 가하여 정책을 강화한다.

## Motivation

- **Known**: RL 기반 인간형 로봇 제어는 복잡한 동작을 학습할 수 있으나, domain randomization과 정규화 제약 등의 기존 방법들은 정책의 특정 취약점을 정확히 식별하지 못한다. 신경망 기반 제어기는 센서/액추에이터 노이즈와 외부 섭동에 매우 민감하다.
- **Gap**: 기존의 domain randomization은 비특이적 섭동만 제공하고, 정규화 제약은 탐색과 견고성 간의 트레이드오프가 있으며, 고차원 상태 및 자유도를 가진 인간형 로봇에서 표적화된 취약점 식별과 공격은 체계적으로 탐구되지 않았다.
- **Why**: 인간형 로봇이 일상 환경에서 장시간 신뢰성 있게 작동하려면 정책의 실제 취약점을 찾아내고 선택적으로 강화하는 것이 필수적이며, 이는 시뮬레이션-현실 격차 극복과 실제 배포 성공률 향상에 직결된다.
- **Approach**: Selective Attack Policy(SAP)라는 학습 가능한 적대자 네트워크가 동작 정책의 취약점을 식별하고 공격 예산 제약 하에서 최소한의 섭동으로 최대 영향을 주도록 설계된다. 동작 정책과 공격 정책의 교대 최적화(non-zero sum 게임)를 통해 반복적으로 견고성을 강화한다.

## Achievement


- **지형 통과 성공률**: 적대적 학습 정책이 지형 횡단 성공률을 40% 향상시킴
- **궤적 추적 오차 감소**: 동작 궤적 추적 오류를 32% 감소
- **장시간 안정성**: 장기간 움직임 및 추적 성능을 유지하는 견고한 정책 달성
- **일반화 성능**: 보수적 과적합 없이 실제 센서 노이즈와 환경 변동에 대한 적응력 증대

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of the SA2RT. The SAP identifies vulnerabilities in motion states and generates adversarial samples b*

- Two-player Markov game 프레임워크로 공격자(adversary) 정책 π_α와 피해자(victim) 동작 정책 π_ν를 정의
- 공격 정책이 상태 공간과 행동 공간 모두에서 섭동을 생성하되, 공격 예산 제약으로 희소한 공격만 허용
- 공격 정책의 목적: 동작 정책의 누적 보상을 최소화하는 취약점 식별
- 동작 정책의 목적: 공격자의 섭동에도 불구하고 원래 작업 성능 유지
- 교대 최적화: 공격 정책 개선 → 동작 정책 강화의 반복 사이클
- Unitree G1 인간형 로봇에서 지각 기반 보행과 전신 제어 작업으로 검증
- 배포 시에는 SAP 없이 강화된 동작 정책만 사용

## Originality

- 인간형 로봇의 고차원 상태-행동 공간에서 선택적 취약점 식별을 통한 표적화된 적대적 학습이 체계적으로 제안된 것은 이번이 처음
- 공격 예산 제약을 도입하여 보수적 과적합을 피하면서도 효과적인 취약점 노출 달성
- Non-zero sum game의 교대 최적화로 동적으로 변화하는 정책 취약점에 지속적으로 대응
- 상태 공간과 행동 공간 동시 섭동을 통한 포괄적 견고성 향상

## Limitation & Further Study

- 실험이 Unitree G1 단일 플랫폼에 제한되어 다른 인간형 로봇으로의 일반화 검증 부재
- 공격 예산 제약의 설정이 수동적이며, 최적 예산값 결정에 대한 체계적 지침 부족
- SAP 학습에 필요한 계산 오버헤드 및 학습 시간에 대한 정량적 분석 미흡
- 극단적 환경(매우 불규칙한 지형, 큰 외부 힘) 등에서의 성능 한계 미검토
- 후속 연구: 다중 로봇 플랫폼에서의 정책 전이 학습, 동적 공격 예산 최적화, 실시간 적응형 공격 정책

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 선택적 적대적 공격을 통해 인간형 로봇의 동작 견고성을 체계적으로 강화하는 혁신적인 방법을 제시하며, 실제 로봇 플랫폼에서 40% 성공률 향상 등 괄목할 만한 성과를 입증했다. 다만 단일 로봇 플랫폼 실험과 공격 예산 설정의 일반화 측면에서 개선의 여지가 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1671_SHIELD_Safety_on_Humanoids_via_CBFs_In_Expectation_on_Learne/review]] — 휴머노이드 안전성 확보에서 선택적 적대적 공격 대신 제어 배리어 함수를 활용한 안전 보장 방법을 제시한다.
- 🔗 후속 연구: [[papers/1661_SafeFall_Learning_Protective_Control_for_Humanoid_Robots/review]] — SA2RT를 통한 견고성 강화와 낙하 보호 제어를 결합하여 포괄적인 휴머노이드 안전 시스템을 구축할 수 있다.
- 🏛 기반 연구: [[papers/1632_RAPT_Model-Predictive_Out-of-Distribution_Detection_and_Fail/review]] — 분포 외 상황 탐지 및 실패 처리 메커니즘이 적대적 공격 하에서의 정책 강화에 대한 이론적 토대를 제공한다.
- 🔗 후속 연구: [[papers/1688_Spectral_Normalization_for_Lipschitz-Constrained_Policies_on/review]] — Keep on Going의 선택적 적대적 강화가 Spectral Normalization의 Lipschitz 제약 정책과 결합되어 더 안정적인 견고성 달성
- 🏛 기반 연구: [[papers/1643_RL_from_Physical_Feedback_Aligning_Large_Motion_Models_with/review]] — 물리 피드백을 통한 강화학습이 Keep on Going의 적대적 공격 기반 정책 강화에 실제 환경 기반 검증 제공
- 🔗 후속 연구: [[papers/1834_Chasing_Stability_Humanoid_Running_via_Control_Lyapunov_Func/review]] — sequential skill learning을 통한 robust한 motion skill이 CLF-RL 기반 달리기의 연속성과 안정성을 더욱 향상시킬 수 있다
- 🔗 후속 연구: [[papers/2017_HWC-Loco_A_Hierarchical_Whole-Body_Control_Approach_to_Robus/review]] — HWC-Loco의 계층적 안전 제어가 Keep on Going의 적대적 강화 방법과 결합되어 더 견고한 로봇 제어 달성 가능
