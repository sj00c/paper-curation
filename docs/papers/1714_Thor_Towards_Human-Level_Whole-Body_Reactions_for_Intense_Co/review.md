---
title: "1714_Thor_Towards_Human-Level_Whole-Body_Reactions_for_Intense_Co"
authors:
  - "Gangyang Li"
  - "Qing Shi"
  - "Youhao Hu"
  - "Jincheng Hu"
  - "Zhongyuan Wang"
date: "2025.11"
doi: "10.48550/arXiv.2510.26280"
arxiv: ""
score: 4.0
essence: "Thor는 humanoid 로봇이 강한 접촉 상호작용 환경에서 인간 수준의 전신 반응을 생성하도록 하는 프레임워크로, force-adaptive torso-tilt (FAT2) 보상 함수와 decoupled reinforcement learning 아키텍처를 제안한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2025_Thor Towards Human-Level Whole-Body Reactions for Intense Contact-Rich Environments.pdf"
---

# Thor: Towards Human-Level Whole-Body Reactions for Intense Contact-Rich Environments

> **저자**: Gangyang Li, Qing Shi, Youhao Hu, Jincheng Hu, Zhongyuan Wang, Xinlong Wang, Shaqi Luo | **날짜**: 2025-11-05 | **DOI**: [10.48550/arXiv.2510.26280](https://doi.org/10.48550/arXiv.2510.26280)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2.*

Thor는 humanoid 로봇이 강한 접촉 상호작용 환경에서 인간 수준의 전신 반응을 생성하도록 하는 프레임워크로, force-adaptive torso-tilt (FAT2) 보상 함수와 decoupled reinforcement learning 아키텍처를 제안한다.

## Motivation

- **Known**: Humanoid는 서비스, 산업, 구조 응급 분야에서 큰 잠재력을 가지지만, 강렬한 접촉 상호작용 중 전신 안정성을 유지하면서 인간 같은 반응을 생성하기는 어렵다.
- **Gap**: 기존 모델 기반 제어는 정확한 로봇 모델링이나 하드코딩된 정책에 의존하며, RL 기반 방법들은 humanoid의 높은 차원성과 불안정성으로 인해 강력한 힘 상호작용 작업에서 최적화되지 못한다.
- **Why**: Humanoid가 화재 대피 문, 무거운 물체 이동 등 고강도 힘 상호작용 작업을 수행하려면 동역학적 모델 없이도 강건한 전신 제어 능력을 갖춰야 하기 때문이다.
- **Approach**: Thor는 상체, 허리, 하체로 decoupled된 actor-critic 네트워크를 설계하고, 인간 생체역학에서 영감을 받은 FAT2 보상 함수로 힘에 반응하는 자세 조정을 장려하며, 도메인 랜덤화와 curriculum learning을 통해 sim-to-real 전이를 해결한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Humanoids performing tasks involving forceful interactions with the*

- **Decoupled RL 아키텍처**: 상체(14 DoF), 허리(3 DoF), 하체(12 DoF)를 독립적인 actor-critic 네트워크로 분리하여 high-dimensional humanoid 제어 문제를 완화
- **FAT2 보상 함수**: 로봇의 힘 분석을 기반으로 설계되어 인간처럼 몸통을 적응적으로 기울이도록 유도하여 강력한 상호작용력 생성
- **실세계 성능 검증**: Unitree G1에서 후진 167.7 N, 전진 145.5 N의 최대 견인력 달성 (baseline 대비 68.9%, 74.7% 개선)
- **다양한 작업 수행**: 소방 문 개방(60 N), 로드 박스 견인(130 N), 휠체어 밀기, 화이트보드 닦기 등 실무 작업 성공
- **높은 빈도 추론**: Decoupled 아키텍처로 제한된 온보드 자원에서 50Hz 고속 제어 가능

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- 상체, 허리, 하체의 세 가지 actor-critic 모듈을 설계하되, 각각 독립적인 정책 네트워크(π_u, π_w, π_l)와 가치 함수를 가짐
- 모든 모듈이 전신 관찰(proprioception, motion command)을 공유하고 특권 정보(end-effector 힘의 크기와 방향)를 critic에만 제공
- FAT2 보상 함수: 로봇의 질량 중심 위치와 외부 힘을 기반으로 허용 가능한 몸통 기울기 범위를 동적으로 계산
- 상체는 human motion dataset을 통해 모션 추적 학습, 하체는 명령된 속도 추적 학습
- Two-stage curriculum learning: 1단계는 간단한 환경에서 강건한 자세 학습, 2단계는 고강도 작업 학습
- Domain randomization: End-effector에 가하는 외부 힘의 방향과 크기를 무작위화하여 sim-to-real 격차 해소
- PD 컨트롤러를 통해 정책 네트워크의 출력(원하는 관절 위치)을 실제 joint torque로 변환

## Originality

- 허리를 중간 제어 모듈로 활용하는 3-부분 decoupled 아키텍처 제안으로 상체-하체 상호작용 조정 개선
- 인간 생체역학에 기반한 FAT2 보상 함수로 단순 모터 토크 증가가 아닌 자세 적응을 통한 힘 상호작용 향상
- Privileged information(힘 정보)을 critic에만 제공하고 actor에는 제공하지 않는 비대칭적 학습 전략
- 강제적 접촉 상호작용을 위한 domain randomization 전략의 체계적 적용

## Limitation & Further Study

- 실험이 단일 로봇(Unitree G1)에만 국한되어 다른 humanoid 플랫폼에서의 일반화 검증 부족
- FAT2 보상 함수 설계가 특정 신체 모양에 최적화되어 다양한 humanoid 형태에 대한 적응성 미확인
- 높은 차원 문제는 완화되었으나 각 모듈 간 coordination mechanism의 명시적 설계가 부재
- 후속연구로 다양한 humanoid 플랫폼 검증, 동적 작업 환경(불균형한 지형 등)에서의 성능 평가, 모듈 간 의존성 분석이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Thor는 decoupled RL 아키텍처와 인간 생체역학 기반 FAT2 보상 함수를 통해 humanoid의 강력한 힘 상호작용 능력을 크게 향상시킨 우수한 연구로, 실세계 성능 검증과 다양한 작업 시연을 통해 높은 실용적 가치를 입증했다.

## Related Papers

- 🔗 후속 연구: [[papers/1799_AMO_Adaptive_Motion_Optimization_for_Hyper-Dexterous_Humanoi/review]] — AMO의 적응형 전신 제어가 Thor의 강한 접촉 반응 능력을 더욱 정교하게 확장합니다.
- 🧪 응용 사례: [[papers/1908_Embrace_Collisions_Humanoid_Shadowing_for_Deployable_Contact/review]] — Thor의 접촉 대응 기술이 충돌을 적극 활용하는 humanoid shadowing에 직접 적용 가능합니다.
- 🔄 다른 접근: [[papers/1836_CHIP_Adaptive_Compliance_for_Humanoid_Control_through_Hindsi/review]] — 둘 다 접촉 상황에서의 compliance 제어를 다루지만 CHIP은 힌드사이트 경험을 활용합니다.
- 🏛 기반 연구: [[papers/1684_SoftMimic_Learning_Compliant_Whole-body_Control_from_Example/review]] — 순응적 전신 제어의 기반 기술을 강한 접촉 상호작용 환경으로 확장하여 인간 수준의 전신 반응을 생성하는 프레임워크로 발전시켰다.
- 🔗 후속 연구: [[papers/1690_Stability-Aware_Retargeting_for_Humanoid_Multi-Contact_Teleo/review]] — 접촉 상호작용에서의 안정성 제어 기술을 강한 접촉 환경으로 확장하여 force-adaptive torso-tilt과 decoupled 아키텍처를 제안했다.
- 🔄 다른 접근: [[papers/1922_FALCON_Learning_Force-Adaptive_Humanoid_Loco-Manipulation/review]] — 접촉이 풍부한 환경에서의 휴머노이드 제어를 위해 서로 다른 접근(인간 수준 전신 반응 vs force-adaptive 로코-조작)을 통해 강건성을 달성한다.
- 🏛 기반 연구: [[papers/1964_HAFO_A_Force-Adaptive_Control_Framework_for_Humanoid_Robots/review]] — Force-adaptive 제어 프레임워크의 개념을 강한 접촉 상호작용에서 인간 수준의 반응을 생성하는 Thor 시스템으로 확장하여 구현했다.
- 🏛 기반 연구: [[papers/1684_SoftMimic_Learning_Compliant_Whole-body_Control_from_Example/review]] — 강한 접촉 상호작용에서 전신 반응을 생성하는 기반 기술을 순응적 제어라는 관점에서 확장하여 외부 힘에 대한 적응을 구현했다.
- 🏛 기반 연구: [[papers/1690_Stability-Aware_Retargeting_for_Humanoid_Multi-Contact_Teleo/review]] — 강한 접촉 상호작용에서의 안정성 제어 기술을 텔레오퍼레이션 환경으로 확장하여 다중 접촉 상황의 안정성을 보장했다.
- 🏛 기반 연구: [[papers/1799_AMO_Adaptive_Motion_Optimization_for_Hyper-Dexterous_Humanoi/review]] — Thor의 접촉 대응 전신 제어 개념이 AMO의 hyper-dexterous whole-body control 개발의 기반이 됩니다.
- 🔗 후속 연구: [[papers/1964_HAFO_A_Force-Adaptive_Control_Framework_for_Humanoid_Robots/review]] — Thor의 intense contact에 대한 human-level reaction 연구를 dual-agent 최적화를 통한 하체-상체 통합 제어로 발전시켰습니다.
