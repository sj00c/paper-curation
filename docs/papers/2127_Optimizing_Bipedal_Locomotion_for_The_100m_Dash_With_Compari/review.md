---
title: "2127_Optimizing_Bipedal_Locomotion_for_The_100m_Dash_With_Compari"
authors:
  - "Devin Crowley"
  - "Jeremy Dao"
  - "Helei Duan"
  - "Kevin Green"
  - "Jonathan Hurst"
date: "2025.08"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 이족 로봇 Cassie의 고속 주행 보행을 위해 보행 매개변수(stride frequency, swing ratio)를 체계적으로 최적화하고, 그 결과를 인간의 주행 역학과 비교하며, 최종적으로 100m 대시 기네스 월드레코드를 달성한 완전한 컨트롤러를 제시한다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Exercise_Learning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Crowley et al._2025_Optimizing Bipedal Locomotion for The 100m Dash With Comparison to Human Running.pdf"
---

# Optimizing Bipedal Locomotion for The 100m Dash With Comparison to Human Running

> **저자**: Devin Crowley, Jeremy Dao, Helei Duan, Kevin Green, Jonathan Hurst, Alan Fern | **날짜**: 2025-08-05 | **URL**: [https://arxiv.org/abs/2508.03070](https://arxiv.org/abs/2508.03070)

---

## Essence

![Figure 3](figures/fig3.webp)

*Fig. 3: The top 5 most efficient freq (above) and ratio*

이 논문은 이족 로봇 Cassie의 고속 주행 보행을 위해 보행 매개변수(stride frequency, swing ratio)를 체계적으로 최적화하고, 그 결과를 인간의 주행 역학과 비교하며, 최종적으로 100m 대시 기네스 월드레코드를 달성한 완전한 컨트롤러를 제시한다.

## Motivation

- **Known**: Sim-to-real RL을 이용한 이족 보행 학습이 효과적이며, 선행 연구에서는 고정된 보행 매개변수나 손으로 튜닝한 매핑을 사용했다. 인간의 주행 역학은 사족동물 대비 효율적으로 알려져 있다.
- **Gap**: 이족 로봇의 고속 주행을 위해 속도에 따라 동적으로 조절되는 보행 매개변수의 최적화 방법이 부재했으며, 로봇 보행과 인간 주행 역학의 체계적 비교 연구가 미흡했다.
- **Why**: 보행 매개변수의 원리 있는 최적화는 이족 로봇이 높은 속도에서 안정적이고 효율적으로 달릴 수 있게 하며, 이는 실제 로봇 응용으로의 확장 가능성을 보여주는 것이 중요하다.
- **Approach**: PPO 기반 sim-to-real RL을 통해 광범위한 보행 매개변수 조합과 속도에서 정책을 훈련한 후, 시뮬레이션에서 에너지 효율 기반 점수 메트릭으로 각 속도에서 최적의 매개변수를 선택하고, 이를 완전한 100m 대시 컨트롤러에 통합한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: The top 5 most efficient freq (above) and ratio*

- **보행 매개변수 최적화**: 손으로 튜닝한 매핑과 질적으로 다른 속도-매개변수 곡선을 발견하여, 특히 중간 속도(2-4 m/s)에서 더 낮은 stride frequency가 효율적임을 보임
- **인간-로봇 보행 비교**: 형태학적 차이에도 불구하고 Cassie의 최적화된 보행 역학이 광범위한 속도에서 인간 주행의 핵심 특성과 유사함을 입증
- **기네스 월드레코드 달성**: 최적화된 보행을 통합한 컨트롤러로 이족 로봇 100m 대시 기록 수립
- **완전한 100m 대시 컨트롤러**: 정지 상태에서의 시작, 고속 주행, 안정적 정지를 포함한 실제 규칙을 만족하는 컨트롤러 개발

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Hand-tuned mapping from the speed command to the*

- MuJoCo 물리 엔진과 dynamics randomization을 사용한 sim-to-real PPO 훈련으로 35차원 상태(관절 위치/속도, 골반 방향), clock signal, 보행 매개변수, 목표 속도를 입력으로 받아 10개 액추에이터 제어
- 0-5 m/s 속도 범위에서 hand-tuned 매핑의 ±0.2(ratio), ±0.625(freq) 오프셋 내 균등분포에서 모든 매개변수 조합으로 정책 훈련
- 각 속도에서 100 policy step 동안 수집한 궤적에 대해 속도 오차, Cost of Transport, 토크 비용, 모터 속도의 4가지 비용을 가중 결합하여 각 매개변수 조합 평가
- 상위 5개 효율적인 매개변수 조합의 추이를 3차 다항식 회귀로 분석하여 속도별 최적 매개변수 곡선 도출
- 최적화된 보행을 LSTM 기반 고수준 컨트롤러에 통합하고 실제 로봇 하드웨어에 배포

## Originality

- **체계적 매개변수 탐색**: 선행 연구의 고정값이나 임의 손-튜닝 대신 광범위한 매개변수 공간을 원리적으로 탐색하는 첫 시도
- **이족 로봇 고속 주행**: 기존 2.0 m/s 수준을 넘어 5 m/s 이상의 고속 주행을 달성한 첫 사례
- **정량적 인간-로봇 비교**: 기존 생체역학 문헌을 바탕으로 로봇과 인간의 주행 역학을 정량적으로 비교한 첫 체계적 연구
- **실제 기록 달성**: 이론적 기여를 넘어 기네스 월드레코드라는 구체적 실세계 성과로 검증

## Limitation & Further Study

- 직선 주행만 대상으로 하며, 회전이나 불규칙한 지형 등 복잡한 환경에서의 보행 최적화는 미다룸
- 점수 메트릭이 효율성 3개 항목 vs 속도 충실도 1개 항목으로 비균형적이어서 속도 추적 성능이 제약될 수 있음
- 시뮬레이션 기반 최적화이므로 sim-to-real gap으로 인한 하드웨어 성능 저하 가능성 존재
- Cassie의 특정 형태에 최적화된 것으로 다른 이족 로봇 플랫폼으로의 일반화 가능성 불명확
- 후속 연구로 동적 환경, 불규칙 지형, 방향 변경을 포함한 보행 최적화 및 다양한 로봇 형태에 대한 확장 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 이족 로봇의 고속 주행을 위한 보행 매개변수의 첫 체계적 최적화를 제시하고, 인간 주행 역학과의 흥미로운 비교를 통해 이론적 깊이를 제공하며, 기네스 월드레코드 달성으로 실질적 임팩트를 입증한 우수한 연구이다.

## Related Papers

- 🏛 기반 연구: [[papers/1834_Chasing_Stability_Humanoid_Running_via_Control_Lyapunov_Func/review]] — 제어 Lyapunov 함수를 통한 휴머노이드 달리기 안정성 이론이 고속 주행 최적화의 기반을 제공한다.
- 🔗 후속 연구: [[papers/1925_FastStair_Learning_to_Run_Up_Stairs_with_Humanoid_Robots/review]] — 휴머노이드의 빠른 계단 오르기 학습을 평지 고속 주행으로 확장한 발전된 응용이다.
- 🧪 응용 사례: [[papers/1826_Biomechanical_Comparisons_Reveal_Divergence_of_Human_and_Hum/review]] — 인간과 휴머노이드의 생체역학적 비교 분석을 실제 100m 대시 기록 달성에 적용한 구체적 사례이다.
- 🔄 다른 접근: [[papers/2063_Learning_Soccer_Skills_for_Humanoid_Robots_A_Progressive_Per/review]] — 축구 스킬 학습이라는 다른 운동 영역에서 점진적 훈련을 통해 휴머노이드의 운동 능력을 향상시킨 사례이다.
- 🏛 기반 연구: [[papers/1919_Exceeding_the_Maximum_Speed_Limit_of_the_Joint_Angle_for_the/review]] — Optimizing Bipedal Locomotion의 고속 주행 최적화가 Exceeding the Maximum Speed Limit의 관절 각도 최대 속도 한계 극복에 필요한 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1637_Reinforcement_Learning_for_Versatile_Dynamic_and_Robust_Bipe/review]] — Reinforcement learning for versatile bipedal locomotion이 Cassie 로봇의 100m 대시 최적화에서 이족 보행의 다양한 매개변수 조정의 기술적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1656_Robust_and_Versatile_Bipedal_Jumping_Control_through_Reinfor/review]] — Robust bipedal jumping control이 100m 대시의 보행 매개변수 최적화를 점프와 같은 다른 고속 동적 움직임으로 확장한 형태입니다.
- 🧪 응용 사례: [[papers/1709_The_Duke_Humanoid_Design_and_Control_For_Energy_Efficient_Bi/review]] — Duke Humanoid의 에너지 효율적 보행 기술을 100m 달리기 최적화에 적용할 수 있습니다.
- 🧪 응용 사례: [[papers/1859_DecARt_Leg_Design_and_Evaluation_of_a_Novel_Humanoid_Robot_L/review]] — 100m 달리기 최적화가 DecARt Leg의 FAST 메트릭과 agile locomotion 능력을 실제 경쟁적 운동 성능에서 검증할 수 있다
- 🔗 후속 연구: [[papers/2121_OmniXtreme_Breaking_the_Generality_Barrier_in_High-Dynamic_H/review]] — 100m 대시 최적화의 체계적인 보행 매개변수 조정이 OmniXtreme의 고동역 humanoid 제어를 특정 고속 운동 성능으로 확장한 사례입니다.
