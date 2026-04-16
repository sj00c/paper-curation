---
title: "1629_Quantum_deep_reinforcement_learning_for_humanoid_robot_navig"
authors:
  - "Romerik Lokossou"
  - "Birhanu Shimelis Girma"
  - "Ozan K. Tonguz"
  - "Ahmed Biyabani"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 Soft Actor-Critic(SAC) 알고리즘을 parameterized quantum circuit으로 구현한 quantum deep reinforcement learning(QDRL)을 humanoid robot navigation 작업에 적용하여, 고차원 상태-행동 공간에서 고전적 RL보다 92% 더 적은 스텝으로 8% 높은 성능을 달성했다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lokossou et al._2025_Quantum deep reinforcement learning for humanoid robot navigation task.pdf"
---

# Quantum deep reinforcement learning for humanoid robot navigation task

> **저자**: Romerik Lokossou, Birhanu Shimelis Girma, Ozan K. Tonguz, Ahmed Biyabani | **날짜**: 2025-09-14 | **URL**: [https://arxiv.org/abs/2509.11388](https://arxiv.org/abs/2509.11388)

---

## Essence

![Figure 4](figures/fig4.webp)

*Fig. 4. Return of Classical SAC versus Quantum SAC in the Walker2d-v4*

이 논문은 Soft Actor-Critic(SAC) 알고리즘을 parameterized quantum circuit으로 구현한 quantum deep reinforcement learning(QDRL)을 humanoid robot navigation 작업에 적용하여, 고차원 상태-행동 공간에서 고전적 RL보다 92% 더 적은 스텝으로 8% 높은 성능을 달성했다.

## Motivation

- **Known**: Quantum RL은 wheeled robots나 robotic arms 같은 단순한 환경에서 성공을 거두었으며, hybrid quantum-classical 구조가 parameter 수를 줄이고 수렴 속도를 개선할 수 있음이 알려져 있다.
- **Gap**: 기존 quantum RL 연구들은 주로 간단한 gym 환경이나 낮은 observation/action space를 가진 작은 로봇들에 집중했으며, humanoid robot처럼 고차원 복잡한 환경에서의 QDRL 적용은 미흡했다.
- **Why**: Humanoid robot navigation은 높은 차원의 상태 공간, 동적 균형 유지, 복잡한 모터 제어가 필요한 실제 응용 문제로서, quantum computing을 활용하여 학습 효율성을 개선하는 것은 실용적 로봇공학에 중요한 의미가 있다.
- **Approach**: Parameterized quantum circuit을 이용한 hybrid quantum-classical SAC 구조를 MuJoCo의 Humanoid-v4와 Walker2d-v4 환경에 구현하고, 고전적 SAC와의 성능 비교를 통해 quantum advantage를 검증했다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4. Return of Classical SAC versus Quantum SAC in the Walker2d-v4*

- **학습 효율성 향상**: Quantum SAC가 classical SAC 대비 92% 더 적은 스텝(228.36 vs 246.40 평균 리턴)으로 8% 높은 성능 달성
- **고차원 환경 확장**: 기존 wheeled robot/robotic arm에서 humanoid robot으로 QDRL 적용 범위 확대
- **Hybrid 아키텍처 검증**: Parameterized quantum circuit과 classical deep RL의 결합이 복잡한 navigation 작업에서 실질적 이점 제공 확인

## How

![Figure 3](figures/fig3.webp)

*Fig. 3. Quantum deep learning model with parametrized quantum circuit*

- OpenAI Gym의 Walker2D-v4 및 Humanoid-v4 환경을 시뮬레이션 벤치마크로 사용
- Soft Actor-Critic(SAC) 알고리즘의 policy와 value network을 parameterized quantum circuit으로 구현
- Quantum computing의 superposition, entanglement, quantum interference 특성을 활용하여 parameter space 축소
- Classical SAC와 quantum SAC의 학습 곡선, 평균 리턴, 수렴 스텝 수를 비교 분석
- Data re-uploading 전략을 활용한 고차원 state space 처리

## Originality

- Humanoid robot navigation이라는 고차원, 고복잡도 환경에서 QDRL을 처음으로 적용한 연구
- 기존의 양자 영감 알고리즘(quantum-inspired) 대신 실제 parameterized quantum circuit을 사용하는 hybrid approach
- 단일 component(예: critic만)이 아닌 전체 SAC 구조의 양자화 시도
- Nav-Q와의 차별성: training 전 과정에서 quantum computing을 활용하면서도 실제 환경의 humanoid robot 시뮬레이션에 적용

## Limitation & Further Study

- **시뮬레이션 환경 제한**: MuJoCo 시뮬레이션에만 제한되며 실제 로봇 하드웨어 검증 부재
- **양자 하드웨어 부재**: 실제 양자 컴퓨터가 아닌 디지털 시뮬레이션 기반이므로 진정한 양자 이점 검증 불충분
- **통계적 신뢰도**: 단일 실행 결과만 제시되어 여러 초기값/시드에 대한 robustness 분석 부족
- **배포 가능성**: Nav-Q와 달리 inference 단계에서도 양자 하드웨어 필요성 언급 부족
- **후속 연구**: 더 복잡한 humanoid 작업(예: 계단 오르기, 불균형 지면), 다중 에이전트 시나리오, 실제 양자 하드웨어 기반 구현, 양자 회로 깊이 최적화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 humanoid robot navigation이라는 도전적 고차원 문제에 QDRL을 처음 적용한 의미 있는 연구로, 양자 컴퓨팅의 실용적 잠재력을 보여주지만, 시뮬레이션 환경 제한과 실제 양자 하드웨어 부재로 인해 근본적인 양자 이점의 증명은 아직 불완전하다.

## Related Papers

- 🏛 기반 연구: [[papers/1688_Spectral_Normalization_for_Lipschitz-Constrained_Policies_on/review]] — Spectral Normalization의 Lipschitz 제약 정책이 quantum deep RL에서 안정적인 학습과 수렴성 보장의 이론적 기초를 제공함
- 🔄 다른 접근: [[papers/1926_FastTD3_Simple_Fast_and_Capable_Reinforcement_Learning_for_H/review]] — Quantum DRL은 parameterized quantum circuit을, FastTD3는 간단하고 빠른 고전적 RL을 사용하여 휴머노이드 제어를 다르게 접근함
- 🧪 응용 사례: [[papers/2064_Learning_Social_Navigation_from_Positive_and_Negative_Demons/review]] — Learning Social Navigation의 양음 시연 학습이 quantum DRL의 고차원 상태-행동 공간 학습을 사회적 내비게이션에 적용한 사례임
- 🔄 다른 접근: [[papers/1629_Quantum_deep_reinforcement_learning_for_humanoid_robot_navig/review]] — Classical SAC를 quantum circuit으로 구현하여 효율성을 개선한 혁신적 접근법
- 🔗 후속 연구: [[papers/1881_Distillation-PPO_A_Novel_Two-Stage_Reinforcement_Learning_Fr/review]] — Quantum RL의 효율성을 two-stage learning framework에 적용 가능한 확장 연구
