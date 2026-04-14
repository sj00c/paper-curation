# Composite Motion Learning with Task Control

> **저자**:  | **날짜**:  | **URL**: [https://dl.acm.org/doi/abs/10.1145/3592447](https://dl.acm.org/doi/abs/10.1145/3592447)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

인간 학습에서의 외부 지원 개념을 로봇에 적용하여, A2CF(Adaptive Assistive Curriculum Force)라는 이중 에이전트 RL 프레임워크를 제안한다. 보조력 에이전트가 초기 학습 단계에서 상태 종속적 보조력을 제공하고 로봇의 숙련도 향상에 따라 점진적으로 감소시킨다.

## Motivation

- **Known**: RL과 IL을 통한 humanoid 로봇의 복잡한 동작 학습이 진행되고 있으며, 인간 발달 과정에서 부모나 코치의 물리적 지원이 학습을 가속화한다는 것이 알려져 있다.
- **Gap**: 기존 humanoid 로봇 학습 방법은 초기 단계에서 비효율적 탐색, 국소 최적값 함정, 불안정성 문제를 겪으며, HoST 같은 기존 보조 방법도 상태에 종속적이지 않은 고정 보조력을 사용한다.
- **Why**: Humanoid 로봇이 walking, dancing, backflips 같은 고차원 복잡 동작을 효율적으로 습득할 수 있도록 학습 속도 향상과 실패율 감소가 중요하며, 궁극적으로 독립적 수행을 위한 안정적 정책 획득이 필수적이다.
- **Approach**: POMDP 프레임워크에서 motion 정책 에이전트와 assistive force 에이전트의 이중 에이전트 시스템을 joint action learners로 훈련하고, 쌍곡체 기반 curriculum을 통해 보조력을 적응적으로 감소시킨다.

## Achievement


- **학습 수렴 속도**: baseline 대비 30% 더 빠른 수렴 달성
- **신뢰성 향상**: 실패율 40% 이상 감소
- **실제 배포 성공**: 시뮬레이션에서 학습한 정책이 support-free로 물리 humanoid 로봇에서 작동
- **다중 과제 검증**: bipedal walking, choreographed dancing, backflips 세 가지 벤치마크에서 일관된 개선

## How

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **확장된 action space**: motion 에이전트의 joint 위치 제어 action과 assistive force 에이전트의 6-D spatial force 제어 action 결합
- **Hypercube 기반 보조력 curriculum**: 정규화된 보조력 크기 ||F_k||/||η_k||가 threshold 이하로 떨어지면 경계값 η_k를 감소시키고, skill acquisition 감지 시 추가 decay 적용
- **Privileged information 활용**: 시뮬레이션 중 privileged 정보(o_priv_t)를 활용하여 generalization 향상
- **초기 상태 분포 설계**: 적절히 설계된 초기 보조력 경계값으로 assistive force 에이전트에 강력한 사전정보(prior) 제공
- **Random masking**: 과도한 외부 의존성 방지를 위해 무작위 마스킹 적용

## Originality

- 인간 모터 학습의 외부 지원 개념을 상태 종속적 adaptive 메커니즘으로 구현한 점이 혁신적
- HoST 등 선행 연구의 고정 보조력과 달리, 쌍곡체 기반 curriculum을 통해 동적으로 보조력 경계를 조정하는 알고리즘 제안
- Joint action learners 프레임워크 내에서 이중 에이전트 협력 메커니즘 설계
- Privileged information, 초기 분포, random masking을 결합하여 과의존성 방지 및 sim-to-real transfer 강화

## Limitation & Further Study

- **보조력 경계 초기값 민감도**: η_0의 선택이 학습 성능에 미치는 영향에 대한 상세 분석 부족
- **과제 범위 제한**: 세 가지 특정 과제(walking, dancing, backflips)에서만 검증되어 다른 humanoid 동작에 대한 일반화 가능성 미지수
- **실제 로봇 실험 규모**: Real-world 실험이 제한적이므로 다양한 환경 및 로봇 플랫폼에서의 강건성 검증 필요
- **계산 비용**: 이중 에이전트 훈련의 계산 오버헤드 및 실시간 control 적용 가능성에 대한 분석 부족
- **Curriculum 설계 자동화**: 현재 curriculum 파라미터(δ, ε)의 자동 조정 메커니즘 미제시

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 인간 학습 원리에 영감을 받아 상태 종속적 adaptive 보조력을 제공하는 A2CF 프레임워크는 humanoid 로봇의 복잡 동작 학습을 효과적으로 가속화하며, 시뮬레이션과 실제 로봇 모두에서 검증된 실용적 가치가 높다.
