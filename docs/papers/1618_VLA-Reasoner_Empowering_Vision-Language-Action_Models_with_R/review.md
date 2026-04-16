---
title: "1618_VLA-Reasoner_Empowering_Vision-Language-Action_Models_with_R"
authors:
  - "Wenkai Guo"
  - "Guanxing Lu"
  - "Haoyuan Deng"
  - "Zhenyu Wu"
  - "Yansong Tang"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "VLA-Reasoner는 Vision-Language-Action 모델에 test-time MCTS를 통합하여 장기 지평 로봇 조작 작업에서 누적 편차를 해결하고 미래 상태를 예측하는 플러그인 프레임워크이다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Robot_Policy_Learning"
  - "sub/LLM_Task_Planning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Guo et al._2025_VLA-Reasoner Empowering Vision-Language-Action Models with Reasoning via Online Monte Carlo Tree Se.pdf"
---

# VLA-Reasoner: Empowering Vision-Language-Action Models with Reasoning via Online Monte Carlo Tree Search

> **저자**: Wenkai Guo, Guanxing Lu, Haoyuan Deng, Zhenyu Wu, Yansong Tang, Ziwei Wang | **날짜**: 2025-09-26 | **URL**: [https://arxiv.org/abs/2509.22643](https://arxiv.org/abs/2509.22643)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: The overall pipeline of VLA-Reasoner. At test time, a lightweight and modified MCTS searches for the optimal act*

VLA-Reasoner는 Vision-Language-Action 모델에 test-time MCTS를 통합하여 장기 지평 로봇 조작 작업에서 누적 편차를 해결하고 미래 상태를 예측하는 플러그인 프레임워크이다.

## Motivation

- **Known**: VLA 모델은 imitation learning으로 일반적인 로봇 조작 작업에서 강력한 성능을 달성하지만, 단기 시야 next-action 예측에만 의존하여 장기 궤적 작업에서 증분 편차로 인해 성능이 떨어진다.
- **Gap**: 기존 VLA는 현재 상태만 고려하여 미래 상태의 영향을 foreseeing하지 못하고, 광범위한 action space에서 효율적으로 탐색하며 중간 상태를 평가할 메커니즘이 부족하다.
- **Why**: 장기 지평 작업에서 누적되는 편차를 해결하고 test-time에 추론 능력을 통합함으로써 더 강건하고 해석 가능한 로봇 조작을 가능하게 할 수 있으며, 이는 확장 가능한 구체화된 지능 달성의 경로를 제시한다.
- **Approach**: VLA-Reasoner는 world model을 사용하여 가능한 action 궤적을 샘플링하고 rollout하며, MCTS로 탐색 효율을 높이고, KDE 기반 신뢰도 샘플링과 offline value estimation을 통해 dense feedback을 제공한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: VLA-Reasoner augments VLA models with test-time rea-*

- **플러그인 프레임워크**: 기존 VLA 모델에 손쉽게 부착 가능하며 다양한 task, 환경, 로봇 embodiment에 걸쳐 일관된 개선 달성
- **적응형 MCTS**: KDE 기반 expert-like 샘플링으로 VLA 쿼리 감소 및 효율적 탐색, offline value estimation으로 중간 상태 평가
- **벤치마크 성과**: LIBERO 벤치마크에서 기준 VLA를 경쟁 모델 수준으로 향상, 실제 로봇에서 적은 데이터로 fine-tuned VLA보다 높은 성공률 달성
- **해석 가능성**: Test-time 추론을 통해 잠재적 결과를 foresee하고 장기 피드백으로 편차 보정하는 구조화된 탐색

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: The overall pipeline of VLA-Reasoner. At test time, a lightweight and modified MCTS searches for the optimal act*

- VLA의 one-step 예측을 root로 사용하여 MCTS 트리 구성
- World model W(s_{t+1} | a_t, s_t)를 통해 시뮬레이션된 미래 상태 생성
- Kernel Density Estimation 기반 신뢰도 분포 π_θ(D_a)에서 action 샘플링으로 redundant VLA 쿼리 제거
- Offline 데이터 기반 value function으로 중간 상태 평가 및 백프로파게이션
- Injection 강도 α를 통해 원본 VLA 예측과 reasoned action을 균형있게 결합: a_t = α(a^{VLA}_t) + (1-α)(a^{Reasoner}_t)

## Originality

- VLA에 test-time MCTS 적용의 참신한 결합으로 기존 model-based planning과 차별화
- KDE 기반 신뢰도 샘플링으로 action space 탐색 최적화—vanilla MCTS의 naive 샘플링 대신 expert-like prior 활용
- Offline value estimation 전략으로 sparse episode-end feedback을 dense intermediate feedback으로 변환
- Plug-and-play 아키텍처로 임의의 VLA 모델에 적용 가능한 범용성

## Limitation & Further Study

- World model의 정확도에 크게 의존—누적 예측 오차가 트리 깊이와 함께 증가할 수 있음
- MCTS의 online computation cost가 실시간 제어 시 병목이 될 가능성
- Offline value estimation이 training distribution 밖의 상태에서 부정확할 수 있음
- α 값 선택이 task별 수동 튜닝을 요구할 수 있으며, 동적 적응 메커니즘 미흡
- **후속연구**: 더 정확한 world model 학습 기법 탐구, 경량 MCTS 구현, 온라인 적응형 value function, 다중 도메인에서 일반화 능력 향상

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VLA-Reasoner는 test-time 추론을 통해 VLA의 근본적인 단기 시야 문제를 체계적으로 해결하는 우아한 프레임워크로, KDE 샘플링과 offline value estimation의 실질적 기여와 함께 시뮬레이션과 실제 로봇에서 일관된 개선을 보여주는 의미 있는 연구이다.

## Related Papers

- 🏛 기반 연구: [[papers/1542_RoboMonkey_Scaling_Test-Time_Sampling_and_Verification_for_V/review]] — test-time sampling and verification이 VLA에서 MCTS 기반 reasoning의 기반이 됩니다.
- 🔄 다른 접근: [[papers/1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action/review]] — VLA에서 추론 능력 강화를 위한 서로 다른 접근법 - MCTS vs system-2 thinking입니다.
- 🔗 후속 연구: [[papers/1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen/review]] — reinforcement learning framework를 test-time MCTS와 결합할 수 있습니다.
- 🏛 기반 연구: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — Embodied Chain-of-Thought가 VLA-Reasoner의 추론 기반 로봇 제어의 이론적 토대를 제공한다.
- 🔄 다른 접근: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — ThinkAct가 VLA-Reasoner와 다른 강화 비전-언어-행동 추론 방식으로 로봇의 사고와 행동을 통합한다.
- 🔗 후속 연구: [[papers/1382_EmbodiedVSR_Dynamic_Scene_Graph-Guided_Chain-of-Thought_Reas/review]] — VLA-Reasoner의 vision-language-action reasoning이 EmbodiedVSR에서 scene graph와 결합되어 더욱 정교한 공간 추론으로 발전했다.
- 🔄 다른 접근: [[papers/1556_RT-H_Action_Hierarchies_Using_Language/review]] — VLA-Reasoner는 RT-H의 언어 기반 계층과 유사한 추론 능력을 VLA 모델에 통합하는 대안적 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1364_Diffusion-VLA_Generalizable_and_Interpretable_Robot_Foundati/review]] — VLA 모델의 추론 능력을 더욱 체계적인 reasoning 프레임워크로 발전시킵니다.
