---
title: "1526_Real-World_Humanoid_Locomotion_with_Reinforcement_Learning"
authors:
  - "Ilija Radosavovic"
  - "Tete Xiao"
  - "Bike Zhang"
  - "Trevor Darrell"
  - "Jitendra Malik"
date: "2023.03"
doi: ""
arxiv: ""
score: 4.0
essence: "Causal transformer 기반의 학습 정책을 대규모 모델프리 강화학습으로 시뮬레이션에서 훈련하고 실제 휴머노이드 로봇에 제로샷으로 배포하여 다양한 실외 환경에서 안정적인 보행을 달성했다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Action-Value_Reasoning_Systems"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Radosavovic et al._2023_Real-World Humanoid Locomotion with Reinforcement Learning.pdf"
---

# Real-World Humanoid Locomotion with Reinforcement Learning

> **저자**: Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, Koushil Sreenath | **날짜**: 2023-03-06 | **URL**: [https://arxiv.org/abs/2303.03381](https://arxiv.org/abs/2303.03381)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Deployment to outdoor environments. We deploy our model to a number of outdoor*

Causal transformer 기반의 학습 정책을 대규모 모델프리 강화학습으로 시뮬레이션에서 훈련하고 실제 휴머노이드 로봇에 제로샷으로 배포하여 다양한 실외 환경에서 안정적인 보행을 달성했다.

## Motivation

- **Known**: 고전 제어 방법과 최적화 기반 전략은 안정적인 휴머노이드 보행을 보여주었으나, 새로운 환경으로의 일반화가 어렵다. 학습 기반 방법은 이족 보행에서도 성공 사례가 있다.
- **Gap**: 기존 학습 기반 접근법은 LSTM이나 명시적 환경 특성 추정기에 의존하는데, 관찰-행동 이력을 통한 맥락 내 적응(in-context learning)의 가능성이 충분히 탐색되지 않았다.
- **Why**: 휴머노이드 로봇이 공장 자동화, 고령 인구 지원, 행성 탐사 등에 활용될 수 있으므로, 다양한 환경에 적응하는 범용 제어기 개발은 로보틱스의 중요한 과제이다.
- **Approach**: Causal transformer를 사용하여 proprioceptive 관찰과 행동의 이력을 입력으로 받아 다음 행동을 예측하도록 설계하고, domain randomization을 적용한 대규모 강화학습으로 훈련하여 제로샷 배포한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Indoor and simulation experiments. We test the robustness of our controller to (A)*

- **실외 환경 배포**: 1주일 풀타임 테스트 기간 동안 콘크리트, 잔디, 러닝 트랙 등 다양한 실외 환경에서 안정적인 보행을 달성하고 낙상 없음
- **외부 교란 강건성**: 요가볼 던지기, 막대 밀기, 뒤로부터 끌기 등의 갑작스러운 외력에 대해 안정성 유지
- **다양한 지형 적응**: 고무, 천, 케이블, 버블 랩으로 덮인 거친 지형 및 최대 8.7% 경사도 성공적 이동
- **짐 운반**: 다양한 질량과 무게중심을 가진 짐(백팩, 손가방, 쓰레기봉투 등) 운반 능력 시현
- **최첨단 방법과의 비교**: 계단과 불안정한 지표면에서 회사 제어기보다 우수한 성능
- **적응형 행동**: 지형 유형에 따른 점진적 보행 변화 및 장애물에 대한 빠른 적응 시현

## How


- Causal transformer 아키텍처로 proprioceptive 관찰과 과거 행동 이력을 처리
- Domain randomization을 사용한 시뮬레이션 환경 앙상블에서 대규모 모델프리 강화학습 훈련
- Teacher imitation과 강화학습의 결합 훈련
- Digit humanoid 로봇(1.6m 높이, 45kg, 30 자유도)에 훈련된 정책 직접 배포
- 제로샷 시나리오로 시뮬레이션에서 만나지 않은 실제 지형에 대응

## Originality

- Humanoid 보행에서 LSTM 대신 causal transformer를 사용하여 관찰-행동 이력의 in-context learning 가능성을 입증
- 명시적 환경 추정기 없이 암묵적 이력 인코딩만으로 환경 적응 달성
- Full-sized humanoid 로봇의 실제 환경 배포에서 강화학습 기반 제어의 실행 가능성 최초 증명
- Transformer 아키텍처의 효과를 체계적으로 분석하고 비교하는 ablation study 제공

## Limitation & Further Study

- 카메라 같은 추가 센서 부재로 계단 같은 큰 장애물에 대응 불가능하고 트래핑 위험
- 시뮬레이션 훈련 시 8.7% 이하 경사도 학습으로 인한 극단적 지형 일반화 한계 불명확
- 단일 로봇(Digit) 플랫폼에서의 검증으로 다른 humanoid 로봇으로의 이전성 미검증
- 후속 연구: 시각 센서 통합으로 장애물 회피 성능 향상, 다양한 humanoid 플랫폼 적용, 더 복잡한 조작 태스크 확장, 실시간 적응 메커니즘의 이론적 분석 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Causal transformer 기반의 강화학습 정책을 실제 humanoid 로봇에 성공적으로 배포한 중요한 사례로, 학습 기반 제어의 실용성과 일반화 능력을 보여준다. 아키텍처 선택에 대한 체계적 검증과 다양한 실세계 환경에서의 광범위한 실험을 통해 높은 기술적·실용적 가치를 제시한다.

## Related Papers

- 🧪 응용 사례: [[papers/1390_Expressive_Whole-Body_Control_for_Humanoid_Robots/review]] — expressive whole-body control의 개념을 causal transformer 기반 강화학습 정책에 적용하여 실제 휴머노이드 로봇의 안정적인 보행을 실현한다.
- 🏛 기반 연구: [[papers/1475_MetaMorph_Learning_Universal_Controllers_with_Transformers/review]] — universal controller 학습을 위한 transformer 기반 방법론을 제공하여 휴머노이드 locomotion의 대규모 모델프리 강화학습에 필요한 아키텍처 설계 기반을 제공한다.
- 🔗 후속 연구: [[papers/1451_Learning_Human-to-Humanoid_Real-Time_Whole-Body_Teleoperatio/review]] — human-to-humanoid teleop 기술을 강화학습 기반 locomotion과 결합하여 더 자연스럽고 적응적인 휴머노이드 제어 시스템을 구축한다.
- 🔄 다른 접근: [[papers/1491_NaVILA_Legged_Robot_Vision-Language-Action_Model_for_Navigat/review]] — humanoid locomotion에서 transformer 기반 RL과 달리 NaVILA는 legged robot의 vision-language navigation에 특화된 접근법이다.
- 🏛 기반 연구: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — real-world humanoid locomotion을 위한 deep reinforcement learning의 이론적 기초와 실제 적용 사례를 제공한다.
- 🔗 후속 연구: [[papers/1328_Chain-of-Action_Trajectory_Autoregressive_Modeling_for_Robot/review]] — real-world humanoid locomotion을 bipedal locomotion의 이론적 기초 위에서 더 복잡한 outdoor 환경으로 확장할 수 있다.
- 🧪 응용 사례: [[papers/1328_Deep_Reinforcement_Learning_for_Bipedal_Locomotion_A_Brief_S/review]] — 강화학습을 휴머노이드 로코모션이라는 구체적 영역에 적용한 사례를 제공한다.
- 🏛 기반 연구: [[papers/1390_Expressive_Whole-Body_Control_for_Humanoid_Robots/review]] — 인간형 로봇의 locomotion에 대한 강화학습 기반 제어의 기초 연구입니다.
- 🔗 후속 연구: [[papers/1431_Impact_of_Static_Friction_on_Sim2Real_in_Robotic_Reinforceme/review]] — 실제 휴머노이드 로코모션 연구는 정적 마찰 분석을 이족 보행 로봇의 실제 환경 적응에 적용합니다.
- 🔗 후속 연구: [[papers/1463_LOVON_Legged_Open-Vocabulary_Object_Navigator/review]] — 강화학습 기반 휴머노이드 보행을 객체 네비게이션과 결합하여 legged robot의 장시간 탐색을 가능하게 했다.
- 🔄 다른 접근: [[papers/1449_Learned_Perceptive_Forward_Dynamics_Model_for_Safe_and_Platf/review]] — 둘 다 사족 로봇의 복잡한 지형 네비게이션을 다루지만 perceptive FDM + MPPI vs pure RL이라는 다른 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1451_Learning_Human-to-Humanoid_Real-Time_Whole-Body_Teleoperatio/review]] — 강화학습 기반 휴머노이드 보행 제어가 H2O의 전신 제어 프레임워크에 기반이 된다.
- 🏛 기반 연구: [[papers/1484_MuJoCo_Playground/review]] — MuJoCo 기반의 실제 휴머노이드 로코모션 연구는 MuJoCo Playground가 제공하는 시뮬레이션 환경의 실용성을 검증합니다.
- 🔄 다른 접근: [[papers/1572_Sim-to-Real_Reinforcement_Learning_for_Vision-Based_Dexterou/review]] — Real-World Humanoid Locomotion은 sim-to-real 접근법을 보행에 적용하여 조작과 다른 embodiment에서의 RL 적용 사례를 제시한다.
- 🔗 후속 연구: [[papers/1625_VR-Robo_A_Real-to-Sim-to-Real_Framework_for_Visual_Robot_Nav/review]] — Real-World Humanoid Locomotion의 실제 로봇 배포 경험은 VR-Robo의 sim-to-real 프레임워크 검증에 중요한 참고사례입니다.
- 🏛 기반 연구: [[papers/1628_WholeBodyVLA_Towards_Unified_Latent_VLA_for_Whole-Body_Loco-/review]] — 실제 humanoid 로봇의 locomotion 제어 경험을 제공하여 WholeBodyVLA의 실용적인 loco-manipulation 구현에 핵심적인 기반을 마련한다.
- 🏛 기반 연구: [[papers/1491_NaVILA_Legged_Robot_Vision-Language-Action_Model_for_Navigat/review]] — Real-World Humanoid Locomotion의 RL 기반 보행 제어 기술이 NaVILA의 legged robot locomotion policy 구현에 필수적 기초가 된다.
