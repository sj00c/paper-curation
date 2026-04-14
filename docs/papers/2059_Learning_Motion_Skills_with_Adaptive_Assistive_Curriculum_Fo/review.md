# Learning Motion Skills with Adaptive Assistive Curriculum Force in Humanoid Robots

> **저자**: Zhanxiang Cao, Yang Zhang, Buqing Nie, Huangxuan Lin, Haoyang Li, Yue Gao | **날짜**: 2025-06-29 | **URL**: [https://arxiv.org/abs/2506.23125](https://arxiv.org/abs/2506.23125)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

인간의 학습 방식에서 영감을 받아, 보조 힘(assistive force) 에이전트가 상태 의존적 힘을 적용하여 휴머노이드 로봇의 복잡한 동작 학습을 가속화하는 A2CF 프레임워크를 제안한다.

## Motivation

- **Known**: RL과 IL을 이용한 휴머노이드 로봇 학습이 발전했으나, 복잡한 동작 습득은 여전히 느리고 불안정하다. 인간은 외부 지원(부모의 도움, 코치의 안내)을 통해 동작 기술을 효율적으로 학습한다.
- **Gap**: 로봇 학습 시스템은 인간처럼 적응적인 외부 지원을 받지 못하므로, 학습 속도와 안정성을 개선할 방법이 필요하다.
- **Why**: 휴머노이드 로봇이 걷기, 춤추기, 백플립 같은 복잡한 동작을 효율적으로 학습할 수 있다면 로봇의 실용성과 응용 범위가 크게 확대된다.
- **Approach**: dual-agent 시스템에서 motion 정책 에이전트와 assistive force 에이전트를 함께 학습하되, 초기에는 강한 보조 힘을 제공하고 로봇의 숙련도에 따라 점진적으로 감소시키는 curriculum 메커니즘을 도입한다.

## Achievement


- **수렴 속도**: 기준 방법 대비 30% 더 빠른 수렴 달성
- **실패율 감소**: 40% 이상의 실패율 감소
- **정책 견고성**: 최종적으로 외부 지원 없이도 안정적으로 작동하는 정책 생성
- **실제 배포**: 시뮬레이션에서 학습한 정책이 실제 휴머노이드 로봇으로 성공적으로 전이됨

## How

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **확장된 행동 공간**: motion 에이전트의 joint position 행동과 assistive force 에이전트의 6D 공간 힘 행동을 결합
- **Hypercube 기반 Curriculum**: 보조 힘의 bounded action space를 6D 초입방체로 정의하고, 적용된 힘의 크기와 학습 지표에 따라 경계(η_k)를 적응적으로 조정
- **특권 정보(Privileged Information) 통합**: 시뮬레이션에서만 제공되는 추가 정보를 활용하여 일반화 성능 개선
- **초기 상태 분포 설계**: 적절한 초기 보조 힘 범위 사전 정보 제공
- **무작위 마스킹**: 외부 지원에 대한 과도한 의존도 방지
- **POMDP 모델링**: 관측 가능 상태(joint 위치/속도, 각속도 등)와 특권 정보를 구분하여 문제 정의

## Originality

- 인간의 motor learning 패턴(점진적 보조 감소)을 로봇 RL에 처음으로 체계적으로 도입
- Adaptive hypercube 기반 curriculum 메커니즘으로 보조 힘을 동적으로 조절
- Dual-agent 아키텍처에서 motion 정책과 assistive force 정책을 joint action learner로 통합
- 특권 정보와 random masking을 결합하여 시뮬레이션-실제 환경 간 전이 학습 강화

## Limitation & Further Study

- 세 가지 벤치마크(걷기, 춤, 백플립)에서만 검증되어, 다른 복잡한 동작으로의 일반화 가능성 미확인
- 실제 로봇 실험이 제한적일 수 있으며, 더 다양한 로봇 플랫폼에서의 성능 검증 필요
- 보조 힘이 실제 로봇에서 항상 안전하게 적용될 수 있는지에 대한 안전성 분석 부족
- 초기 보조 힘 범위(η_0) 설정의 민감도 분석 및 hyperparameter 선택 기준 명확화 필요
- 다른 assistive learning 방식(예: imitation learning 기반 보조)과의 비교 분석 부재

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 인간의 motor learning 원리를 로봇 RL에 창의적으로 적용하여 학습 효율성을 크게 개선한 우수한 연구이며, adaptive curriculum 메커니즘과 실제 배포 성공이 주요 강점이다.
