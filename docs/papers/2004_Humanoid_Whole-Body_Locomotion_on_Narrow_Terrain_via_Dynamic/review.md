# Humanoid Whole-Body Locomotion on Narrow Terrain via Dynamic Balance and Reinforcement Learning

> **저자**: Weiji Xie, Chenjia Bai, Jiyuan Shi, Junkai Yang, Yunfei Ge, Weinan Zhang, Xuelong Li | **날짜**: 2025-02-24 | **URL**: [https://arxiv.org/abs/2502.17219](https://arxiv.org/abs/2502.17219)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: The locomotion capabilities of full-sized Humanoid without vision or LiDAR sensors. (a) Narrow Path (25cm):*

ZMP(Zero Moment Point) 기반 리워드와 강화학습을 결합한 동적 균형 메커니즘을 도입하여, 휴머노이드 로봇이 외부 센서 없이 고유감각만으로 좁은 경로와 예상 못한 장애물이 있는 극단적 지형을 안정적으로 통과하도록 하는 전신 보행 알고리즘을 제안한다.

## Motivation

- **Known**: 최근 강화학습 기반 휴머노이드 보행 알고리즘은 규칙적 보행(phase-based gait) 또는 움직임 모방에 의존하며, 병렬 시뮬레이션과 정책 최적화 기법을 통해 일반적 지형에서는 적응 능력을 보여준다. 고전적 제어 방식은 ZMP 개념을 이용하여 동적 안정성을 보장해왔다.
- **Gap**: 기존 강화학습 기반 휴머노이드 보행 방법들은 주기적 보행이나 모션 프리미티브에 의존하여 갑작스러운 불안정성 상황에서 빠르고 다양한 보행 조정을 할 수 없으며, 외부 지각(vision, LiDAR)에 의존하거나 좁은 지형과 같은 극단적 환경에서 동적 균형을 유지하지 못한다.
- **Why**: 휴머노이드 로봇이 인간처럼 미끄러짐, 예상 못한 장애물, 외부 방해에 대응하여 빠르게 발디딤을 조정하고 동적 균형을 회복할 수 있게 하는 것은 실제 복잡한 환경에서의 안정적 이동을 가능하게 하며, 외부 센서 없이 고유감각만으로 이를 달성하면 로봇의 실용성과 자율성을 크게 향상시킨다.
- **Approach**: ZMP 개념을 비평면(non-planar) 표면으로 확장하여 ZMP 선(line of ZMPs)을 형성하고, 이를 이용한 리워드 함수를 설계하여 ZMP 좌표가 지지 다각형 중심 근처에 있도록 유도한다. 비대칭 actor-critic 프레임워크에서 특권 정보(privileged information)로 리워드를 계산하되 정책은 고유감각만으로 학습하여, 실제 로봇 배포 시 외부 지각 없이도 동작하도록 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: The locomotion capabilities of full-sized Humanoid without vision or LiDAR sensors. (a) Narrow Path (25cm):*

- **ZMP 기반 동적 균형 메커니즘**: ZMP를 강화학습 리워드로 통합하여 지지 다각형 내에서의 ZMP 위치를 측정함으로써 복잡한 지형에서의 동적 균형을 실현했다.
- **전신 제어 프레임워크 확장**: reward vectorization, angular momentum regularization, multiplicative action noise 등의 새로운 기법을 도입하여 상체와 하체의 협조적 동작을 가능하게 했다.
- **광범위한 실증 검증**: 시뮬레이션 및 full-sized Unitree H1-2 로봇을 이용한 실제 실험을 통해 좁은 경로(25cm), 미지 장애물, 계단, 외부 밀림, 짐 운반 등 다양한 극단적 시나리오에서 안정성을 입증했다.

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: The overall training process of the proposed method.*

- ZMP를 비평면 표면으로 확장하여 support polygon 중심과의 거리를 이용한 리워드 함수 설계
- 시뮬레이션에서 획득한 특권 정보(contact forces, support polygon, centroid)로 리워드 계산
- 비대칭 actor-critic 프레임워크로 정책은 고유감각(proprioception) 기반 학습, 배포는 외부 센서 불필요
- 전신 제어(whole-body control)에서 상체 스윙을 활용한 동적 균형 보조
- Angular momentum regularization으로 원치 않는 몸 회전 제약, multiplicative action noise로 동작 범위 제어
- Reward vectorization 기법으로 ZMP 기반 리워드, command-following 리워드, regularization 리워드를 각각의 value function과 연결하여 정확한 가치 추정 달성
- PPO(Proximal Policy Optimization) 알고리즘을 기반으로 한 정책 학습

## Originality

- ZMP 개념을 현대 강화학습 기반 휴머노이드 제어에 처음으로 체계적으로 통합한 것
- 비평면 표면에서의 ZMP 라인 개념 도입으로 고전적 지형에서의 ZMP 정의 확장
- 특권 정보를 활용한 비대칭 actor-critic 구조로 시뮬레이션과 실제 배포 간 간극을 해결한 설계
- Reward vectorization 기법 적용으로 복수의 리워드 항이 정확하게 value function에 반영되도록 한 혁신
- 외부 센서 없이 고유감각만으로 극단적 지형(좁은 경로, 미지 장애물)을 통과하는 능력 입증

## Limitation & Further Study

- **지형 다양성**: 논문에서 보여주는 실험 시나리오는 주로 좁은 경로, 계단, 장애물 회피 등에 제한되며, 더욱 다양한 지형(진흙, 모래, 물 등)에서의 성능 검증 필요
- **로봇 플랫폼 특화성**: Unitree H1-2 로봇에 대해서만 실험했으므로, 다른 휴머노이드 로봇(Atlas, Spot, NAO 등)으로의 일반화 가능성 불명확
- **실시간 계산 요구사항**: 논문에서 제시되지 않은 배포 시 계산량, 실시간 성능, 배터리 소모량 등에 대한 분석 부족
- **외부 간섭의 한계**: 강한 외부 밀림이나 넘어질 위험이 있는 수준의 극단적 간섭에 대한 성능 한계 미언급
- **후속 연구 방향**: 더 극단적 지형에서의 적응, 다중 모달 감각(vision, LiDAR)과의 결합을 통한 성능 향상, 실시간 재학습 메커니즘 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 고전적 ZMP 개념을 현대 강화학습에 효과적으로 통합하여 외부 센서 없이 극단적 지형 통과 능력을 확보한 의미 있는 기여를 한다. 실제 full-sized 휴머노이드 로봇에서의 광범위한 실증이 강점이나, 다양한 로봇 플랫폼과 극단적 지형에 대한 일반화 가능성 검증이 필요하다.
