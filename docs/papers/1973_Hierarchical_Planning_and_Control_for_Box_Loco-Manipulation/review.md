# Hierarchical Planning and Control for Box Loco-Manipulation

> **저자**: Zhaoming Xie, Jonathan Tseng, Sebastian Starke, Michiel van de Panne, C. Karen Liu | **날짜**: 2023-06-15 | **URL**: [https://arxiv.org/abs/2306.09532](https://arxiv.org/abs/2306.09532)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2. System overview. We design four motion primitives for locomotion and manipulation which can be*

물리 기반 시뮬레이션 인간 캐릭터가 box rearrangement 작업을 수행하기 위해 계획, diffusion model, 강화학습을 계층적으로 조합하는 시스템을 제시한다.

## Motivation

- **Known**: 물리 기반 캐릭터 애니메이션에서 이동과 조작 기술을 개별적으로는 성숙했으나, 두 기술을 유연하게 결합하는 것은 여전히 도전적이다.
- **Gap**: 기존 physics-based loco-manipulation 방법들은 단순화된 상호작용에 의존하거나 계산 비용이 크며, 다양한 객체 속성(크기, 무게, 높이)에 대한 일반화 능력이 부족하다.
- **Why**: 인간처럼 행동하는 가상 캐릭터 개발은 컴퓨터 애니메이션과 로봇공학에서 근본적이며, 실제 환경에서의 물체 정리 작업은 현실적인 응용 시나리오다.
- **Approach**: 고수준의 A* planner로 경로를 계획하고, diffusion model로 현실적인 보행 궤적을 생성하며, 강화학습 기반 physics-controlled policy로 움직임을 모방한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. We develop loco-manipulation skills for box-carrying physics-based characters. This is achieved via a*

- **계층적 제어 아키텍처**: 추상화 수준에 따라 계획과 제어를 분리하여 다양한 배치 작업에 일반화 가능하게 함
- **Diffusion model 기반 locomotion 생성**: bidirectional root representation을 도입하여 waypoint 조건을 만족하는 현실적인 보행 궤적 생성
- **Object-aware RL policy**: 단일 motion clip으로부터 학습하여 다양한 상자 무게, 크기, 높이에 일반화 가능한 물체 조작 기술 습득
- **실제 작업 수행**: 장애물이 있는 클러터된 환경에서 상자를 픽업, 운반, 배치하는 완전 자동화된 작업 달성

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. System overview. We design four motion primitives for locomotion and manipulation which can be*

- 고수준: A* pathfinding으로 pick-up과 place-down 위치 사이의 기본 경로 계획
- 중간 수준: diffusion model에 bidirectional root control을 적용하여 waypoint 조건을 만족하는 kinematic locomotion 궤적 생성
- 저수준: imitation-based deep reinforcement learning으로 diffusion 생성 궤적과 motion clip을 추적하는 physics-based control policy 학습
- Motion primitives: walk-only, walk-and-carry, pickup, place-down의 4가지 기본 동작을 조합하여 복합 작업 수행
- Generalization: object-aware reward formulation으로 다양한 객체 특성에 대응하는 robust carrying behavior 구현

## Originality

- Physics-based character animation에 diffusion model을 활용한 최초의 시도로, 단순성과 유연성을 모두 확보
- Bidirectional root representation으로 diffusion model의 waypoint 추종 정확도 향상
- 단일 motion clip에서 출발하여 RL을 통해 다양한 객체 속성에 일반화되는 manipulation skill 학습 방식의 독창성
- High-level planner, mid-level diffusion trajectory generation, low-level physics control의 3단계 계층 구조의 명확한 설계

## Limitation & Further Study

- Diffusion model의 sampling 시간과 계산 비용에 대한 분석 및 최적화 방안 부족
- 단일 human skeleton 및 특정 환경 설정에만 제한되어 있으며, 다양한 체형이나 환경의 일반화 능력 미검증
- Motion capture 데이터의 부족으로 pickup/placement 동작을 단일 clip에 의존하고 있어, 더 다양한 접근 방식에 대한 확장성 제한
- 후속 연구: (1) 실제 로봇에의 sim-to-real transfer, (2) 더 복잡한 multi-object manipulation 및 협력 작업, (3) 사용자 상호작용 및 지시학습 통합

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 물리 기반 캐릭터 애니메이션에서 loco-manipulation의 도전적인 문제를 diffusion model과 RL을 계층적으로 조합하여 우아하게 해결하며, 높은 기술적 완성도와 실용적 가치를 동시에 갖춘 우수한 연구이다.
