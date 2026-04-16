---
title: "1683_SoccerDiffusion_Toward_Learning_End-to-End_Humanoid_Robot_So"
authors:
  - "Florian Vahl"
  - "Jörn Griepenburg"
  - "Jan Gutsche"
  - "Jasper Güldenstein"
  - "Jianwei Zhang"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "SoccerDiffusion은 transformer 기반 diffusion model을 활용하여 RoboCup 경기 녹화 데이터로부터 휴머노이드 로봇 축구의 end-to-end 제어 정책을 학습하고, distillation 기법으로 실시간 추론을 가능하게 한다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Vahl et al._2025_SoccerDiffusion Toward Learning End-to-End Humanoid Robot Soccer from Gameplay Recordings.pdf"
---

# SoccerDiffusion: Toward Learning End-to-End Humanoid Robot Soccer from Gameplay Recordings

> **저자**: Florian Vahl, Jörn Griepenburg, Jan Gutsche, Jasper Güldenstein, Jianwei Zhang | **날짜**: 2025-04-29 | **URL**: [https://arxiv.org/abs/2504.20808](https://arxiv.org/abs/2504.20808)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Architecture of the SoccerDiffusion model. Special tokens for the game*

SoccerDiffusion은 transformer 기반 diffusion model을 활용하여 RoboCup 경기 녹화 데이터로부터 휴머노이드 로봇 축구의 end-to-end 제어 정책을 학습하고, distillation 기법으로 실시간 추론을 가능하게 한다.

## Motivation

- **Known**: Behavioral cloning과 diffusion model은 로봇 제어에서 유용하지만, 기존 연구는 짧은 작업이나 시뮬레이션에 제한되었다. Transformer는 장기 시계열 데이터에서 효과적이다.
- **Gap**: humanoid robot soccer와 같은 장시간 복합 작업에서 diffusion model 기반 imitation learning의 실제 적용과 평가가 부족하다. 실제 경기 데이터로부터 학습하는 end-to-end 접근이 제한적이다.
- **Why**: 휴머노이드 로봇 축구는 고도의 동적 환경에서 복잡한 행동이 필요하며, 수동 설계 대신 데이터 기반 학습은 확장성과 적응성을 높일 수 있다. 실제 경기 데이터는 다양한 행동을 포함하는 풍부한 학습 자료이다.
- **Approach**: RoboCup 경기 녹화에서 수집한 15시간의 multi-modal sensor 데이터(vision, proprioception, game state)로 transformer 기반 diffusion model을 학습하고, distillation을 통해 multi-step 확산 과정을 단일 단계로 축소하여 실시간 추론을 실현한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Qualitative evaluation: (a) walking and (b) fall recovery, both performed*

- **데이터 수집 및 전처리**: RoboCup 2024 및 German Open 2025에서 88개 녹화, 약 15시간의 실제 경기 데이터 확보 및 동기화된 multi-modal 전처리 완성
- **모델 개발**: transformer 기반 diffusion model로 walking, kicking, fall recovery 등 복잡한 운동 행동 학습 가능 입증
- **실시간 추론 실현**: distillation 기법으로 diffusion 단계를 다중에서 단일 단계로 축소하여 embedded platform에서 실시간 실행 가능
- **시뮬레이션 및 물리 로봇 검증**: 학습된 행동이 시뮬레이션과 실제 로봇 모두에서 복제 가능함을 실증
- **커뮤니티 기여**: 데이터셋, 사전 학습 모델, 코드 공개로 향후 연구(RL, preference optimization) 기반 제공

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Architecture of the SoccerDiffusion model. Special tokens for the game*

- ROS 2 Bag의 mcap 파일로부터 센서 측정, 중간 표현, 관절 명령 데이터 추출
- IMU, 관절 데이터는 50 Hz, 이미지는 10 Hz로 resampling 및 동기화 (인과성 보장)
- 이미지를 480×480 픽셀로 다운샘플링, game state를 3가지 상태로 단순화
- 전처리된 데이터를 SQLite 데이터베이스에 저장하여 효율적 쿼리 가능하게 구성
- sensor input을 받아 관절 명령 궤적을 예측하는 transformer 기반 diffusion model 구축
- Diffusion model의 multi-step inference를 distillation으로 단일 단계로 축소
- 시뮬레이션 및 물리 로봇에서 정성적 평가를 통해 행동 복제 능력 검증

## Originality

- 실제 RoboCup 경기 데이터로부터 end-to-end humanoid robot soccer 정책 학습 시도 (기존은 주로 시뮬레이션 또는 단순 작업)
- 장시간 복합 작업에 transformer 기반 diffusion model 적용 (기존 diffusion model 로봇 연구는 짧은 작업 중심)
- Multi-modal sensor input (vision, proprioception, game state)을 통합한 통합 학습 프레임워크
- Distillation을 통한 diffusion model 실시간 추론 최적화 (임베디드 로봇 플랫폼 실행 가능)
- 공개 데이터셋 및 모델 제공으로 재현성과 커뮤니티 기여

## Limitation & Further Study

- **고수준 전략 행동 부족**: 현재 모델은 walking, kicking 등 저수준 운동 행동만 학습, 경기 전술이나 의사결정 능력 제한
- **데이터 규모 제한**: 88개 녹화(15시간)는 상대적으로 제한적이며, 다른 RoboCup 팀의 데이터 미포함 (시간 제약)
- **IMU 데이터 재구성**: RoboCup 2024의 센서 오류로 IMU 데이터를 중간 표현으로부터 재구성하여 accelerometer, gyroscope 정보 부재
- **모든 경우의 수 커버 미흡**: 분포 외 상황에서 성능 저하 가능성 (distrbutional shift)
- **후속 연구 기반 역할**: 단독으로는 기존 수동 프로그래밍 스택을 능가하지 못하며, RL이나 preference optimization의 초기 모델로 제안
- **평가 지표 부재**: 정성적 평가 위주로 정량적 성능 지표(성공률, 정확도 등) 명확하지 않음

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 실제 RoboCup 경기 데이터로부터 humanoid robot soccer 정책을 학습하는 실질적 시도로, transformer 기반 diffusion model과 distillation 기법의 조합으로 end-to-end 학습과 실시간 추론을 동시에 달성했다. 고수준 전략 행동은 제한적이지만 저수준 운동 행동의 효과적 학습과 공개 데이터셋 제공으로 향후 로봇 학습 연구의 견고한 기초를 마련했다.

## Related Papers

- 🔄 다른 접근: [[papers/1662_SafeFlow_Real-Time_Text-Driven_Humanoid_Whole-Body_Control_v/review]] — 두 논문 모두 diffusion 기반 휴머노이드 제어를 다루지만, 축구 경기와 텍스트 명령이라는 다른 응용 분야를 다룬다.
- 🔗 후속 연구: [[papers/2046_Learning_Agile_Striker_Skills_for_Humanoid_Soccer_Robots_fro/review]] — 인간 시연으로부터 축구 스킬을 학습하는 기초 연구를 transformer diffusion으로 end-to-end 학습하도록 발전시킨다.
- 🏛 기반 연구: [[papers/1996_Humanoid_Locomotion_as_Next_Token_Prediction/review]] — 휴머노이드 보행을 next token prediction으로 모델링하는 기초적인 접근법을 제공한다.
- 🔄 다른 접근: [[papers/1695_StyleLoco_Generative_Adversarial_Distillation_for_Natural_Hu/review]] — 확산 모델과 적대적 증류라는 서로 다른 생성 모델 접근법을 사용하여 휴머노이드의 자연스러운 움직임을 학습한다.
- 🔗 후속 연구: [[papers/2074_Learning_Vision-Driven_Reactive_Soccer_Skills_for_Humanoid_R/review]] — 스포츠 로봇 제어에서 축구와 축구라는 동일 종목에 대한 end-to-end 학습과 시각 기반 반응 기술이라는 보완적 접근법을 다룬다.
- 🔗 후속 연구: [[papers/1815_Being-M05_A_Real-Time_Controllable_Vision-Language-Motion_Mo/review]] — 실시간 제어 가능한 비전-언어-모션 모델의 개념을 축구라는 특정 도메인으로 확장하여 경기 데이터 기반 학습을 구현했다.
- 🔄 다른 접근: [[papers/1692_StageACT_Stage-Conditioned_Imitation_for_Robust_Humanoid_Doo/review]] — 복잡한 작업(축구 vs 도어 오픈)에서 diffusion 기반 제어를 위해 서로 다른 조건부 정보(게임 상황 vs 작업 단계)를 활용한다.
- 🔄 다른 접근: [[papers/1662_SafeFlow_Real-Time_Text-Driven_Humanoid_Whole-Body_Control_v/review]] — 두 논문 모두 diffusion 기반 휴머노이드 제어를 다루지만, 텍스트 명령과 축구 경기라는 다른 응용 분야를 다룬다.
- 🔄 다른 접근: [[papers/1692_StageACT_Stage-Conditioned_Imitation_for_Robust_Humanoid_Doo/review]] — 복잡한 작업(도어 오픈 vs 축구)에서 diffusion 기반 제어를 위해 서로 다른 조건부 정보(작업 단계 vs 게임 상황)를 활용한다.
- 🔄 다른 접근: [[papers/1695_StyleLoco_Generative_Adversarial_Distillation_for_Natural_Hu/review]] — 휴머노이드의 자연스러운 움직임 생성에서 적대적 증류와 확산 모델이라는 서로 다른 생성 모델 접근법을 사용한다.
- 🏛 기반 연구: [[papers/2046_Learning_Agile_Striker_Skills_for_Humanoid_Soccer_Robots_fro/review]] — end-to-end 휴머노이드 축구 기술 학습의 기본 원리가 강건한 볼 킥킹 시스템 구현에 대한 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/2063_Learning_Soccer_Skills_for_Humanoid_Robots_A_Progressive_Per/review]] — 점진적 지각-행동 학습이 end-to-end 축구 기술 학습으로 확장되어 더 통합된 접근법을 보여준다.
