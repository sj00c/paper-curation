---
title: "1677_SKATER_Synthesized_Kinematics_for_Advanced_Traversing_Effici"
authors:
  - "Junchi Gu"
  - "Feiyang Yuan"
  - "Weize Shi"
  - "Tianchen Huang"
  - "Haopeng Zhang"
date: "2026.01"
doi: ""
arxiv: ""
score: 4.0
essence: "휴머노이드 로봇의 발에 4개의 수동 바퀴를 장착하고 Deep Reinforcement Learning을 통해 롤러스케이팅 스위즐 보행을 학습시켜 전통적인 보행 대비 충격력 75.86%, 에너지 소비 63.34% 감소를 달성했다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Humanoid_Locomotion_and_Control"
  - "sub/Terrain-Adaptive_Humanoid_Locomotion"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Gu et al._2026_SKATER Synthesized Kinematics for Advanced Traversing Efficiency on a Humanoid Robot via Roller Ska.pdf"
---

# SKATER: Synthesized Kinematics for Advanced Traversing Efficiency on a Humanoid Robot via Roller Skate Swizzles

> **저자**: Junchi Gu, Feiyang Yuan, Weize Shi, Tianchen Huang, Haopeng Zhang, Xiaohu Zhang, Yu Wang, Wei Gao, Shiwu Zhang | **날짜**: 2026-01-08 | **URL**: [https://arxiv.org/abs/2601.04948](https://arxiv.org/abs/2601.04948)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: The SKATER system: a humanoid robot equipped*

휴머노이드 로봇의 발에 4개의 수동 바퀴를 장착하고 Deep Reinforcement Learning을 통해 롤러스케이팅 스위즐 보행을 학습시켜 전통적인 보행 대비 충격력 75.86%, 에너지 소비 63.34% 감소를 달성했다.

## Motivation

- **Known**: 최근 휴머노이드 로봇의 보행 및 주행 기술이 발전했으나 발이 지면에 닿을 때마다 높은 충격력이 발생하여 관절 손상과 에너지 비효율이 문제이다. 롤러스케이팅은 낮은 충격력을 특징으로 하는 생체역학적으로 가치있는 운동이다.
- **Gap**: 기존 휴머노이드 로봇의 롤러스케이팅 연구는 극히 드물며, 대부분의 선행 연구는 사족 로봇이나 궤적 계획 기반의 낮은 속도 방법에 국한되어 있다. 이족 휴머노이드에서 nonholonomic 제약을 고려한 DRL 기반 접근은 미개척 영역이다.
- **Why**: 롤러스케이팅은 발 접촉 충격을 최소화하여 관절 수명 연장과 에너지 효율 향상을 동시에 달성할 수 있으며, 이는 장시간 운영이 필요한 로봇 시스템에서 매우 중요한 특성이다.
- **Approach**: implicit gait reward function과 multi-stage curriculum learning을 적용한 DRL 프레임워크를 개발하고, domain randomization을 통해 sim-to-real transfer를 실현하여 SKATER 로봇에서 스위즐 스케이팅을 학습한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: Comparison of foot contact force profiles: (a) roller skating locomotion with continuous ground contact and stab*

- **SKATER 로봇 개발**: 33 DoF 휴머노이드 로봇에 4개의 수동 인라인 바퀴 장착으로 롤러스케이팅 가능 플랫폼 구현
- **DRL 제어 프레임워크**: implicit gait reward function과 multi-stage curriculum learning을 통합한 스위즐 스케이팅 학습 시스템 구축
- **성능 향상**: 전통적 보행 대비 Impact Intensity 75.86% 감소, Cost of Transport 63.34% 감소
- **sim-to-real 전이**: 시뮬레이션에서 학습한 정책을 물리 로봇에 성공적으로 배포
- **부드러운 운동**: 롤러스케이팅의 연속적인 슬라이딩 특성으로 관절 운동 매끄러움 증가

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Deep reinforcement learning control framework for SKATER. The policy network processes proprioceptive and*

- SKATER 하드웨어: 25 DoF 휴머노이드 로봇에 각 발 밑에 4개의 수동 휠 탑재
- DRL 프레임워크: policy network가 자체감각 및 외적감각 센서 데이터 처리 → 관절 수준 명령 생성
- Reward function 설계: 롤러스케이팅의 내재적 특성(대칭성, 물리적 일관성, 기하학적 제약)을 기반으로 한 implicit guidance
- Multi-stage curriculum learning: 훈련 중 과제 복잡도를 점진적으로 증가
- Domain randomization: 환경 파라미터 변화를 시뮬레이션에서 적용하여 robust 정책 획득
- Sim-to-real transfer: 시뮬레이션 정책을 물리 로봇에 배포 및 검증

## Originality

- 휴머노이드 로봇의 롤러스케이팅 연구에서 순수 DRL 기반 접근 방식 제시 (기존은 model-based 궤적 계획 위주)
- Nonholonomic 제약을 명시적으로 모델링하지 않고 implicit reward function으로 자동 학습
- Swizzle 스케이팅이라는 특화된 보행 패턴을 DRL로 습득하는 첫 사례
- Multi-stage curriculum learning과 domain randomization의 조합으로 sim-to-real 성공 달성
- 기존 ZMP/MPC 기반 접근의 제약을 벗어난 새로운 패러다임 제시

## Limitation & Further Study

- 실제 환경에서의 지면 마찰 특성 변화(얼음, 습한 표면 등)에 대한 일반화 성능 미검증
- Swizzle 스케이팅에 국한된 학습으로 다른 스케이팅 패턴(cross-over, backward 등) 적용 미확인
- 로봇의 속도 범위가 제한적일 수 있으며 고속 스케이팅에서의 안정성 미기술
- 학습 정책의 해석가능성 및 generalization bound에 대한 이론적 분석 부족
- 후속연구: (1) 다양한 환경 조건에서의 적응형 제어, (2) 복수 스케이팅 패턴 학습, (3) 경사진 지형 및 장애물 회피 능력 추가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 휴머노이드 로봇의 에너지 효율과 관절 수명 향상을 위해 롤러스케이팅이라는 창의적인 솔루션을 제시하고, DRL 기반 제어 프레임워크를 통해 현실적인 구현을 달성한 혁신적 연구이다. 85~76% 수준의 높은 성능 개선과 sim-to-real 전이의 성공은 로봇 운동 제어 분야에 실질적 기여를 한다.

## Related Papers

- 🔗 후속 연구: [[papers/1709_The_Duke_Humanoid_Design_and_Control_For_Energy_Efficient_Bi/review]] — 롤러스케이팅 기술이 Duke Humanoid의 패시브 다이내믹스와 결합되어 더욱 에너지 효율적인 고속 이동이 가능하다.
- 🔄 다른 접근: [[papers/1657_Robust_Humanoid_Walking_on_Compliant_and_Uneven_Terrain_with/review]] — 수동 바퀴를 활용한 스위즐 보행과 전통적인 terrain adaptation은 모두 충격과 에너지를 줄이는 서로 다른 보행 전략이다.
- 🔄 다른 접근: [[papers/1656_Robust_and_Versatile_Bipedal_Jumping_Control_through_Reinfor/review]] — 롤러스케이팅과 점프 제어 모두 동적 움직임이지만 연속적 vs 폭발적 동작이라는 대조적 특성입니다.
- 🏛 기반 연구: [[papers/1894_ECO_Energy-Constrained_Optimization_with_Reinforcement_Learn/review]] — 에너지 효율적인 traversal이 에너지 제약 최적화 강화학습의 실제 적용 사례입니다.
- 🔄 다른 접근: [[papers/1656_Robust_and_Versatile_Bipedal_Jumping_Control_through_Reinfor/review]] — 점프 제어와 롤러스케이팅 모두 동적 locomotion이지만 공중 vs 지면 접촉이라는 대조적 방법입니다.
- 🔗 후속 연구: [[papers/1657_Robust_Humanoid_Walking_on_Compliant_and_Uneven_Terrain_with/review]] — Terrain randomization 기반 robust walking이 롤러스케이팅과 같은 특수한 지형 적응 기법으로 확장되어 더 다양한 환경 대응이 가능하다.
- 🏛 기반 연구: [[papers/1709_The_Duke_Humanoid_Design_and_Control_For_Energy_Efficient_Bi/review]] — Duke Humanoid의 패시브 다이내믹스 활용 원리가 롤러스케이팅의 에너지 효율적 이동에 이론적 기반을 제공한다.
