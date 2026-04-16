---
title: "1638_Reinforcement_Learning_with_Data_Bootstrapping_for_Dynamic_S"
authors:
  - "Chengyang Peng"
  - "Zhihao Zhang"
  - "Shiting Gong"
  - "Sankalp Agrawal"
  - "Keith A. Redmill"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "Humanoid robot navigation을 위해 고수준 RL 기반 동적 subgoal 생성기와 저수준 MPC 기반 보행 제어기를 결합한 계층적 프레임워크를 제안하며, data bootstrapping 기법으로 학습을 안정화한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Terrain_Foothold_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Peng et al._2025_Reinforcement Learning with Data Bootstrapping for Dynamic Subgoal Pursuit in Humanoid Robot Navigat.pdf"
---

# Reinforcement Learning with Data Bootstrapping for Dynamic Subgoal Pursuit in Humanoid Robot Navigation

> **저자**: Chengyang Peng, Zhihao Zhang, Shiting Gong, Sankalp Agrawal, Keith A. Redmill, Ayonga Hereid | **날짜**: 2025-06-02 | **URL**: [https://arxiv.org/abs/2506.02206](https://arxiv.org/abs/2506.02206)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2. Overall structure of the proposed hierarchical framework for humanoid navigation. The high-level RL-based planne*

Humanoid robot navigation을 위해 고수준 RL 기반 동적 subgoal 생성기와 저수준 MPC 기반 보행 제어기를 결합한 계층적 프레임워크를 제안하며, data bootstrapping 기법으로 학습을 안정화한다.

## Motivation

- **Known**: Bipedal robot navigation은 기존에 기하학적 경로 계획과 실시간 보행 제어를 분리하여 수행하거나, RL 기반 방식을 적용하되 대부분 바퀴형 로봇을 대상으로 하고 샘플 효율성 문제를 겪고 있다.
- **Gap**: Bipedal robot의 고차원 비선형 역학과 불안정성을 고려하면서도 환경의 복잡성을 효과적으로 처리하는 방법이 부재하며, RL 기반 방법의 샘플 비효율성 문제가 특히 심각하다.
- **Why**: Humanoid robot은 혼잡한 인간 환경에서 조작과 보행을 동시에 수행해야 하므로 안전하고 실시간적인 navigation이 핵심이며, 이를 위해서는 동역학 제약과 환경 인식을 통합할 필요가 있다.
- **Approach**: RL 기반 고수준 planner가 로봇-중심 극좌표계에서 동적 subgoal을 생성하고, 저수준 MPC controller가 이를 따르는 안정적인 보행을 생성하며, model-based navigation 방법으로부터의 demonstration data를 활용한 data bootstrapping으로 학습을 가속화한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4. The navigation performance of LMPC, RRT-LMPC,*

- **계층적 프레임워크의 효과성**: RL 기반 고수준 계획과 MPC 기반 저수준 제어의 결합으로 환경 적응성과 동역학적 안정성을 동시에 확보
- **Data bootstrapping 기법**: Model-based 방법으로부터 생성된 demonstration dataset을 replay buffer에 포함시켜 학습 안정성과 수렴 속도를 향상
- **향상된 navigation 성능**: 기존 model-based 방법 및 다양한 learning-based 방법 대비 cluttered 환경에서의 success rate와 adaptability 개선
- **실제 로봇 적용 가능성**: Agility Robotics Digit humanoid에서의 시뮬레이션 검증으로 실제 bipedal robot 적용 가능성 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. Overall structure of the proposed hierarchical framework for humanoid navigation. The high-level RL-based planne*

- 64×64 local occupancy grid map (전방 4.5m, 후방 1.5m, 횡단 6m)과 CoM 상태, 목표 정보를 포함한 heterogeneous state 정의
- 로봇-중심 극좌표계에서 (거리 dc, 방향 ϕc)로 표현된 dynamic subgoal을 action으로 정의
- Soft Actor-Critic (SAC) 알고리즘을 사용하여 Gaussian 분포 기반 stochastic policy π(a|s) 학습
- CNN으로 occupancy map을 처리하고 MLP로 나머지 state 정보를 처리하는 dual-module actor network 구성
- Model-based navigation 방법으로부터 생성된 diverse, informative demonstration dataset을 replay buffer에 추가하여 offline data와 online experience를 혼합
- 저수준 MPC controller는 reduced-order bipedal dynamics를 기반으로 CoM 위치, 보행 안정성, 장애물 회피 제약을 모두 고려하여 robust walking gait 생성

## Originality

- Bipedal robot navigation을 위한 RL과 MPC의 명확한 계층적 분리로, RL의 환경 적응성과 MPC의 동역학적 안정성을 효과적으로 결합
- Robot-centric 극좌표계에서의 dynamic subgoal 생성으로 로봇의 센싱과 제어 성능을 최대화
- Model-based 방법의 demonstration을 data bootstrapping으로 활용하여 RL의 샘플 비효율성 문제를 체계적으로 해결
- Heterogeneous state 표현과 dual-module network 설계로 occupancy map과 로봇 상태 정보를 효과적으로 통합

## Limitation & Further Study

- 시뮬레이션 환경에서만 검증되었으며 실제 Digit 로봇에서의 현실 세계 성능 미검증
- Local occupancy map에 기반한 local planner이므로 global navigation의 최적성 보장 부재
- Model-based demonstration data 생성을 위해 기존 LMPC 방법이 필수적이므로, 순수 learning-based 방식보다 초기 비용 증가
- Random obstacle scenario에서의 평가만 수행되었으며, 동적 장애물이나 인간 보행자가 있는 환경에서의 성능 미평가
- **후속 연구**: (1) 실제 humanoid robot 플랫폼에서의 현장 실험, (2) 동적 환경 및 예측 불가능한 perturbation 처리, (3) 시뮬레이션-현실 간극(sim-to-real gap) 해결, (4) 더 복잡한 환경 기하학 처리

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Bipedal robot navigation을 위한 RL과 MPC의 계층적 결합은 창의적이며, data bootstrapping을 통한 학습 안정화는 실질적 기여이나, 시뮬레이션 환경만의 검증과 동적 환경 미평가가 실제 적용까지의 간격을 남긴다.

## Related Papers

- 🔄 다른 접근: [[papers/2111_NoMaD_Goal_Masked_Diffusion_Policies_for_Navigation_and_Expl/review]] — Hierarchical navigation을 goal-masked diffusion으로 해결한 다른 접근법
- 🔗 후속 연구: [[papers/1974_Hierarchical_Vision-Language_Planning_for_Multi-Step_Humanoi/review]] — Data bootstrapping을 vision-language planning과 결합한 확장 연구
- 🔄 다른 접근: [[papers/1926_FastTD3_Simple_Fast_and_Capable_Reinforcement_Learning_for_H/review]] — 둘 다 강화학습의 효율성 개선을 다루지만 FastTD3는 TD3 최적화에, RL with Data Bootstrapping은 데이터 효율성에 초점을 맞춘다.
