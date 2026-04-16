---
title: "1709_The_Duke_Humanoid_Design_and_Control_For_Energy_Efficient_Bi"
authors:
  - "Boxi Xia"
  - "Bokuan Li"
  - "Jacob Lee"
  - "Michael Scutari"
  - "Boyuan Chen"
date: "2024.09"
doi: ""
arxiv: ""
score: 4.0
essence: "Duke Humanoid은 동적 보행이 가능한 오픈소스 10-DoF 인형로봇으로, 패시브 다이내믹스를 활용하는 reinforcement learning 정책을 통해 에너지 효율적인 이족 보행을 달성한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Humanoid_Locomotion_and_Control"
  - "sub/Terrain-Adaptive_Humanoid_Locomotion"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xia et al._2024_The Duke Humanoid Design and Control For Energy Efficient Bipedal Locomotion Using Passive Dynamics.pdf"
---

# The Duke Humanoid: Design and Control For Energy Efficient Bipedal Locomotion Using Passive Dynamics

> **저자**: Boxi Xia, Bokuan Li, Jacob Lee, Michael Scutari, Boyuan Chen | **날짜**: 2024-09-29 | **URL**: [https://arxiv.org/abs/2409.19795](https://arxiv.org/abs/2409.19795)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Duke Humanoid v1.0: a) The frontal plane symmetry*

Duke Humanoid은 동적 보행이 가능한 오픈소스 10-DoF 인형로봇으로, 패시브 다이내믹스를 활용하는 reinforcement learning 정책을 통해 에너지 효율적인 이족 보행을 달성한다.

## Motivation

- **Known**: 상용 인형로봇은 폐쇄형 시스템이고 일부 오픈소스 로봇은 동적 보행 능력이 제한적이다. 패시브 다이내믹스는 전통적 제어에서 에너지 효율 향상에 성공했으나, end-to-end learning 프레임워크에서는 아직 충분히 탐색되지 않았다.
- **Gap**: 오픈소스 하드웨어와 소프트웨어를 모두 갖추면서 동적 보행이 가능한 인형로봇 플랫폼의 부족, 그리고 reinforcement learning 기반 제어에서 패시브 다이내믹스를 명시적으로 활용하는 방법의 미흡함.
- **Why**: 에너지 효율적인 보행은 실제 배포 시 충전 빈도를 줄여 운영 비용을 감소시키며, 오픈소스 플랫폼은 연구자들의 커스터마이제이션과 저수준 시스템 접근을 가능하게 한다.
- **Approach**: 인간의 골격 비율을 모방한 대칭적 엉덩이 배치와 직선 무릎 설계로 패시브 워킹을 가능하게 하고, joint torque를 명시적으로 modulate하여 패시브와 액티브 제어 간 전환을 유도하는 reinforcement learning 알고리즘을 개발했다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Mechanical Design Overview: a) Major dimensions*

- **오픈소스 플랫폼 구현**: 하드웨어와 소프트웨어 모두 오픈소스화되어 연구자의 커스터마이제이션과 저수준 접근을 지원하는 인형로봇 플랫폼 제공
- **Zero-shot 정책 배포**: 시뮬레이션에서 학습한 reinforcement learning 정책을 실제 하드웨어에 파인튜닝 없이 직접 배포 가능
- **에너지 효율 개선**: 패시브 정책이 저속 보행(<0.5m/s)에서 시뮬레이션 기준 50%, 실제 로봇에서 31%의 운송 비용(cost of transport) 감소 달성
- **경쟁력 있는 토크 성능**: 유사 크기의 다른 인형로봇 대비 HFE와 KFE 조인트의 최대 토크가 우수함(각각 264 N·m, 238 N·m)

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Mechanical Design Overview: a) Major dimensions*

- 인간의 femur, tibia, foot length 및 stance width 비율을 참고하여 기계적 설계 수행
- 대칭적 엉덩이 배치와 직선 무릎으로 정적 안정성 확보
- Joint torque modulation을 통해 passive 및 active 제어 간 명시적 전환을 학습하도록 reinforcement learning 프레임워크 설계
- 병렬 linkage 구조로 knee와 ankle joint 구현하여 무게와 관성 감소
- 시뮬레이션 환경에서 RL 정책 학습 후 zero-shot 배포 검증

## Originality

- Reinforcement learning 프레임워크 내에서 패시브 다이내믹스를 명시적으로 활용하는 접근은 기존의 전통적 제어 기반 패시브 워킹 연구와 차별화됨
- Human physiology를 모방하는 설계 원칙(대칭 엉덩이, 직선 무릎)을 동적 보행 가능한 오픈소스 플랫폼에 통합한 시도
- Hardware와 control을 동시에 최적화하는 co-design 접근으로 기존 폐쇄형 상용 로봇과 기능 제한적 오픈소스 로봇의 간극 해소

## Limitation & Further Study

- **속도 범위 제한**: 에너지 효율 개선이 저속 보행(<0.5m/s)에서 주로 달성되므로 고속 보행 시 효과 검증 필요
- **안정성 분석 부족**: 실제 로봇 실험에서 안정성 마진이나 외란에 대한 강건성 분석이 제시되지 않음
- **페이로드 적응성**: 페이로드 추가 시 패시브 정책의 일반화 능력에 대한 평가 부재
- **비교 기준 제한**: 동일 하드웨어 기반 baseline RL 정책과의 비교만 있고, 다른 에너지 효율화 제어 방법과의 직접 비교 부족
- **후속 연구**: 고속 보행 조건에서의 패시브 다이내믹스 활용 방안, 불규칙한 지형에서의 적응 능력 개선, 페이로드 변화에 대한 강건성 향상 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 오픈소스 인형로봇 플랫폼과 패시브 다이내믹스 기반 에너지 효율 개선을 결합하여 humanoid 보행 연구에 실질적 기여를 한다. 특히 reinforcement learning 내 passive dynamics의 명시적 활용과 zero-shot 배포 검증은 학술적·실용적 가치가 높으나, 속도 범위와 일반화 능력의 검증이 더 필요하다.

## Related Papers

- 🏛 기반 연구: [[papers/1677_SKATER_Synthesized_Kinematics_for_Advanced_Traversing_Effici/review]] — Duke Humanoid의 패시브 다이내믹스 활용 원리가 롤러스케이팅의 에너지 효율적 이동에 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1657_Robust_Humanoid_Walking_on_Compliant_and_Uneven_Terrain_with/review]] — 패시브 다이내믹스 기반 에너지 효율성과 terrain randomization 기반 robust성은 이족 보행의 서로 다른 최적화 목표이다.
- 🔄 다른 접근: [[papers/1796_AGILOped_Agile_Open-Source_Humanoid_Robot_for_Research/review]] — 둘 다 오픈소스 humanoid 플랫폼이지만 AGILOped는 더 높은 동적 성능에 초점을 맞춥니다.
- 🔄 다른 접근: [[papers/1715_ToddlerBot_Open-Source_ML-Compatible_Humanoid_Platform_for_L/review]] — ToddlerBot과 같이 저비용 오픈소스 humanoid 플랫폼이지만 다른 크기와 용도로 설계되었습니다.
- 🧪 응용 사례: [[papers/2127_Optimizing_Bipedal_Locomotion_for_The_100m_Dash_With_Compari/review]] — Duke Humanoid의 에너지 효율적 보행 기술을 100m 달리기 최적화에 적용할 수 있습니다.
- 🏛 기반 연구: [[papers/1818_Berkeley_Humanoid_A_Research_Platform_for_Learning-based_Con/review]] — 학습 기반 제어를 위한 연구 플랫폼의 개념을 에너지 효율성에 중점을 둔 10-DoF 휴머노이드로 구체화하여 패시브 다이내믹스를 활용했다.
- 🔗 후속 연구: [[papers/2065_Learning_Symmetric_and_Low-energy_Locomotion/review]] — 대칭적이고 저에너지 보행의 개념을 Duke Humanoid라는 구체적 플랫폼에서 패시브 다이내믹스와 강화학습을 결합하여 실현했다.
- 🔄 다른 접근: [[papers/1864_Demonstrating_Berkeley_Humanoid_Lite_An_Open-source_Accessib/review]] — 오픈소스 휴머노이드 개발을 위해 서로 다른 접근(에너지 효율적 10-DoF vs 접근성 중심 Berkeley Humanoid Lite)을 통해 연구 커뮤니티에 기여한다.
- 🔗 후속 연구: [[papers/1677_SKATER_Synthesized_Kinematics_for_Advanced_Traversing_Effici/review]] — 롤러스케이팅 기술이 Duke Humanoid의 패시브 다이내믹스와 결합되어 더욱 에너지 효율적인 고속 이동이 가능하다.
- 🔄 다른 접근: [[papers/1657_Robust_Humanoid_Walking_on_Compliant_and_Uneven_Terrain_with/review]] — Deep RL terrain adaptation과 passive dynamics 활용은 모두 에너지 효율적인 이족 보행을 위한 서로 다른 접근 방식이다.
- 🔄 다른 접근: [[papers/1715_ToddlerBot_Open-Source_ML-Compatible_Humanoid_Platform_for_L/review]] — Duke Humanoid와 같이 오픈소스 humanoid 플랫폼이지만 ToddlerBot은 미니어처 크기와 ML 호환성에 특화되었습니다.
- 🏛 기반 연구: [[papers/1776_A_Framework_for_Optimal_Ankle_Design_of_Humanoid_Robots/review]] — 발목 최적 설계 프레임워크가 Duke Humanoid의 패시브 다이내믹스 기반 보행에서 하체 메커니즘 최적화에 직접 적용된다.
- 🔄 다른 접근: [[papers/1796_AGILOped_Agile_Open-Source_Humanoid_Robot_for_Research/review]] — 둘 다 저비용 오픈소스 humanoid이지만 Duke는 에너지 효율, AGILOped는 동적 성능에 특화되었습니다.
- 🔄 다른 접근: [[papers/1894_ECO_Energy-Constrained_Optimization_with_Reinforcement_Learn/review]] — 에너지 효율적인 휴머노이드 보행에서 constrained RL과 하드웨어 설계 최적화라는 서로 다른 에너지 효율성 접근법을 제시한다.
