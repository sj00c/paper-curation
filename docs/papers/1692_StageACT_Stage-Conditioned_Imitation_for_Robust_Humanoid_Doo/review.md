---
title: "1692_StageACT_Stage-Conditioned_Imitation_for_Robust_Humanoid_Doo"
authors:
  - "Moonyoung Lee"
  - "Dong Ki Kim"
  - "Jai Krishna Bandi"
  - "Max Smith"
  - "Aileen Liao"
date: "2025.09"
doi: "10.48550/arXiv.2509.13200"
arxiv: ""
score: 4.0
essence: "StageACT는 휴머노이드 로봇의 도어 오픈 작업을 위해 저수준 정책에 작업 단계(task stage) 정보를 조건으로 추가한 단계-조건부 모방 학습 프레임워크를 제안하며, 부분 관찰성 환경에서 강건성을 크게 향상시킨다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lee et al._2025_StageACT Stage-Conditioned Imitation for Robust Humanoid Door Opening.pdf"
---

# StageACT: Stage-Conditioned Imitation for Robust Humanoid Door Opening

> **저자**: Moonyoung Lee, Dong Ki Kim, Jai Krishna Bandi, Max Smith, Aileen Liao, Ali-akbar Agha-mohammadi, Shayegan Omidshafiei | **날짜**: 2025-09-18 | **DOI**: [10.48550/arXiv.2509.13200](https://doi.org/10.48550/arXiv.2509.13200)

---

## Essence

![Figure 3](figures/fig3.webp)

*Fig. 3: The StageACT framework combines stage-level guidance with low-*

StageACT는 휴머노이드 로봇의 도어 오픈 작업을 위해 저수준 정책에 작업 단계(task stage) 정보를 조건으로 추가한 단계-조건부 모방 학습 프레임워크를 제안하며, 부분 관찰성 환경에서 강건성을 크게 향상시킨다.

## Motivation

- **Known**: 휴머노이드 로봇은 이족보행과 조작 능력을 결합하여 인간 환경에서 작동할 수 있으며, 도어 오픈은 DARPA Robotics Challenge 이래 표준 벤치마크로 인식되어 왔다. 그러나 기존 접근법들은 바퀴 달린 플랫폼이나 사족 로봇에 초점을 맞추었고, 휴머노이드의 자율 도어 오픈은 대부분 원격 조종에 의존했다.
- **Gap**: 도어 오픈은 핸들 래치 상태와 같은 관찰 불가능한 정보를 추론해야 하는 장 지평선, 부분 관찰 작업으로서 표준 behavior cloning을 mode collapse에 취약하게 만든다. 휴머노이드 로봇에서 외부 센싱이나 사전 도어 정보 없이 접촉-풍부한 로코-조작을 자율적으로 수행할 수 있는 방법이 부족하다.
- **Why**: 도어는 건축 공간에서 가장 흔한 통로이며 로봇의 행동 영역을 제한하므로, 도어 오픈 기술은 휴머노이드 로봇의 실제 환경 적응에 필수적이다. 부분 관찰성과 장 지평선 특성을 극복하는 것은 현실의 복잡한 조작 작업으로의 확장을 가능하게 한다.
- **Approach**: 인간의 직관적 전략에서 영감을 얻어 도어 오픈 작업을 접근, 악수, 래치 해제, 밀기 등의 단계로 분해하고, 저수준 정책을 이산적 작업 단계 입력으로 조건화하여 부분 관찰성을 해결한다. 단계 정보는 동일한 관찰로부터 다양한 행동을 구분하고 실패 시 이전 단계로의 복귀를 가능하게 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Autonomous door opening by the G1 humanoid robot in a real-world office. Time-synchronized front (top) and back *

- **첫 휴머노이드 자율 로코-조작**: 외부 센싱이나 특권적 도어 정보 없이 인간 시연만으로 훈련된 휴머노이드 도어 오픈 정책의 최초 시연
- **성능 향상**: 미시청 도어에서 55% 성공률을 달성하여 최고 기준선 대비 2배 이상 개선
- **의도적 행동 유도**: 단계 프롬프팅을 통한 명시적 행동 가이드로 복구 행동(recovery behavior) 활성화
- **경량 메커니즘**: 간단한 단계 조건화가 장 지평선 로코-조작에서 강력한 효과를 발휘함을 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the whole-body teleoperation setup for the G1 humanoid*

- Apple Vision Pro 기반 전신 원격 조종으로 Unitree G1 휴머노이드에서 도어 오픈 시연 수집 (상체와 하체 분리 제어로 자연스러운 인터페이스 제공)
- 각 시연을 approaching, grasping, unlatching, pushing 등의 이산 단계로 라벨링
- 저수준 정책을 단계 정보로 조건화하여 동일 관찰에서의 모호성 해결 및 접촉 동역학 전이 구분
- Stage-conditioned policy가 표준 behavior cloning보다 넓은 문맥 윈도우를 효과적으로 활용하도록 설계
- 단계 프롬프팅을 통해 정책이 이전 단계로 재진입하여 실패 복구 가능

## Originality

- 휴머노이드 로봇의 자율 도어 오픈 첫 시연 (기존 휴머노이드 연구는 원격 조종에 의존)
- 접촉-풍부한 로코-조작에서 단계 조건화의 효과를 체계적으로 입증한 최초 연구
- 부분 관찰성 문제 해결을 위해 명시적 모든 가정 없이 구조화된 시간 정보 활용
- 단계 프롬프팅을 통한 적응적 행동 유도 메커니즘의 새로운 적용

## Limitation & Further Study

- 현재 결과는 특정 환경(실제 사무실)과 단일 로봇(Unitree G1) 기반이므로 다양한 도어 유형 및 로봇 플랫폼으로의 일반화 검증 필요
- 55% 성공률은 실용적 배포에 아직 부족하며, 실패 모드에 대한 상세 분석 부재
- 단계 라벨링의 수동 과정이 확장성 저해 가능성 - 자동 단계 감지 메커니즘 개발 필요
- 부분 관찰성의 구체적인 소스(래치 상태, 도어 방향 등)에 대한 명시적 모델링 부재
- 다른 조작 작업으로의 전이 가능성에 대한 평가 부족

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 휴머노이드 도어 오픈이라는 도전적인 실제 문제에서 단순하지만 효과적인 단계 조건화 방식으로 현저한 성능 향상을 달성했으며, 장 지평선 부분 관찰 작업에 대한 실질적 시사점을 제공한다. 다만 일반화와 신뢰성 관점에서 추가 검증이 필요하고, 수동 라벨링 프로세스의 자동화가 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1627_PvP_Data-Efficient_Humanoid_Robot_Learning_with_Propriocepti/review]] — 두 논문 모두 부분 관찰성 문제를 다루지만, 작업 단계 조건부와 고유수용성 인식이라는 다른 정보 활용 방식을 사용한다.
- 🔗 후속 연구: [[papers/2124_Open-TeleVision_Teleoperation_with_Immersive_Active_Visual_F/review]] — 몰입형 능동 시각 원격조작을 단계 조건부 모방 학습으로 확장하여 더 강건한 자율 실행을 실현한다.
- 🏛 기반 연구: [[papers/1774_A_Behavior_Architecture_for_Fast_Humanoid_Robot_Door_Travers/review]] — 휴머노이드 로봇 도어 통과를 위한 빠른 행동 아키텍처의 기초를 제공한다.
- 🔄 다른 접근: [[papers/1743_UniTracker_Learning_Universal_Whole-Body_Motion_Tracker_for/review]] — 부분 관찰성 환경에서의 휴머노이드 제어를 다루며, 작업 단계 조건부 학습과 CVAE 기반 다양성 생성이라는 서로 다른 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1973_Hierarchical_Planning_and_Control_for_Box_Loco-Manipulation/review]] — 박스 loco-manipulation에서 계층적 계획과 단계별 조건부 모방 학습이 상호 보완적인 제어 전략을 제공한다.
- 🔄 다른 접근: [[papers/1683_SoccerDiffusion_Toward_Learning_End-to-End_Humanoid_Robot_So/review]] — 복잡한 작업(도어 오픈 vs 축구)에서 diffusion 기반 제어를 위해 서로 다른 조건부 정보(작업 단계 vs 게임 상황)를 활용한다.
- 🔗 후속 연구: [[papers/1696_Success_in_Humanoid_Reinforcement_Learning_under_Partial_Obs/review]] — 부분 관찰성 환경에서의 강건성 향상 개념을 작업 단계 정보를 조건으로 하는 모방 학습으로 구체화하여 성능을 개선했다.
- 🏛 기반 연구: [[papers/2025_INTENTION_Inferring_Tendencies_of_Humanoid_Robot_Motion_Thro/review]] — 휴머노이드 모션의 의도 추론 개념을 작업 단계라는 명시적 조건으로 확장하여 부분 관찰 환경에서의 강건성을 달성했다.
- 🔄 다른 접근: [[papers/1683_SoccerDiffusion_Toward_Learning_End-to-End_Humanoid_Robot_So/review]] — 복잡한 작업(축구 vs 도어 오픈)에서 diffusion 기반 제어를 위해 서로 다른 조건부 정보(게임 상황 vs 작업 단계)를 활용한다.
- 🔗 후속 연구: [[papers/1696_Success_in_Humanoid_Reinforcement_Learning_under_Partial_Obs/review]] — 부분 관찰 환경에서의 강건성 향상을 작업 단계 정보 없이도 달성할 수 있는 history encoder 기법으로 일반화하여 적용했다.
- 🏛 기반 연구: [[papers/1743_UniTracker_Learning_Universal_Whole-Body_Motion_Tracker_for/review]] — 부분 관찰성 문제 해결에서 CVAE 기반 다양성과 작업 단계 조건부 접근법이 상호 보완적이다.
- 🔗 후속 연구: [[papers/1854_Coordinated_Humanoid_Robot_Locomotion_with_Symmetry_Equivari/review]] — StageACT의 stage-conditioned imitation과 함께 대칭성 기반 정책이 robust한 humanoid control을 위한 완전한 프레임워크를 구성한다.
