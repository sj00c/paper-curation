# Embedding Classical Balance Control Principles in Reinforcement Learning for Humanoid Recovery

> **저자**: Nehar Poddar, Stephen McCrory, Luigi Penco, Geoffrey Clark, Hakki Erhan Svil, Robert Griffin | **날짜**: 2026-03-09 | **DOI**: [10.48550/arXiv.2603.08619](https://doi.org/10.48550/arXiv.2603.08619)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

고전적 균형 제어 원리(capture point, center-of-mass, centroidal momentum)를 강화학습의 privileged critic 입력과 보상 형성에 직접 임베딩하여, 인간형 로봇의 낙상 회복을 위한 통합 정책을 학습한다. 단일 정책으로 발목/엉덩이 전략, 보정 스텝, 다중접촉 일어서기를 포괄하며 93.4% 회복률을 달성한다.

## Motivation

- **Known**: 강화학습은 일어서기 동작을 입증했으나 기존 접근법들은 회복을 순수 작업-보상 문제로 취급하여 명시적 균형 상태 표현이 없다. 고전적 안정성 분석(ZMP, capture point, DCM)은 모델 기반 제어에서 잘 확립되어 있다.
- **Gap**: 균형 인식 신호 없이 critic은 보상 이력만으로 회복 가능성을 추론해야 하므로 광범위한 교란 스펙트럼에서 일반화가 제한된다. 기존 RL 방법들은 참조 궤적이나 스크립트된 접촉 없이 전체 회복 스펙트럼을 포괄하는 단일 정책을 구현하지 못했다.
- **Why**: 인간형 로봇의 낙상 회복 불능은 비구조화된 환경에서의 실용적 배치를 심각하게 제한하므로, 균형 구조를 학습 프레임워크에 명시적으로 임베딩하면 학습 효율성과 일반화를 동시에 개선할 수 있다.
- **Approach**: 비대칭 actor-critic 구조를 사용하여 actor는 proprioception만 입력받고, critic은 capture point, CoM 상태, centroidal momentum을 privileged 입력으로 받으며 이들 메트릭을 보상 형성에 직접 활용한다. 낙상 유도와 일어서기를 명시적으로 순환하는 curriculum을 통해 전체 회복 시퀀스를 학습한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **통합 정책 범위**: 발목/엉덩이 안정화, 스텝 회복, 순응형 낙상, 손/팔꿈치/무릎을 이용한 다중접촉 일어서기까지 전체 회복 스펙트럼을 단일 정책으로 구현
- **높은 성공률**: Unitree H1-2에서 무작위 초기 자세와 예측 불가능한 낙상 구성에 대해 93.4% 회복률 달성
- **균형 구조의 필수성**: ablation 연구에서 privileged critic 입력과 capture point 보상 제거 시 일어서기 학습이 완전히 실패(stuck-low 종료율 0.067→1.0), 이들이 우연의 구조가 아닌 의미 있는 학습 신호임을 입증
- **제로샷 하드웨어 이전**: 정책 수정 없이 Unitree H1-2 하드웨어 10회 시행과 MuJoCo로의 sim-to-sim 이전에서 교환 환경 일반화 검증
- **참조 불필요한 학습**: 모션 참조, 키프레임, 스크립트된 접촉 없이 학습

## How


- PPO 기반 on-policy actor-critic 프레임워크 사용
- Actor: 모든 자유도에 대한 상대 관절 위치 목표 출력, 저수준 PD 제어기가 추적
- Critic: capture point, CoM 상태(위치/속도), centroidal momentum을 privileged 입력으로 수신
- 보상 형성: 이들 균형 메트릭 주위에 직접 구성된 보상항 포함
- Curriculum: 낙상 유도와 일어서기를 명시적으로 순환하여 전체 회복 시퀀스 학습
- Unitree H1-2에서 Isaac Lab 시뮬레이터로 훈련
- 배포 정책은 proprioceptive 관찰만 사용하여 하드웨어 이전 가능

## Originality

- 균형 메트릭을 privileged critic 입력으로 직접 임베딩하는 비대칭 actor-critic 구조의 novel 설계
- capture point, CoM 상태, centroidal momentum을 보상 형성에 직접 통합하는 balance-informed 보상 설계
- 참조 궤적, 스크립트된 접촉, 키프레임 없이 전체 회복 스펙트럼(발목→엉덩이→스텝→다중접촉)을 포괄하는 단일 정책
- 낙상 유도-일어서기 순환 curriculum의 명시적 설계로 비주기적 복합 접촉 시나리오 커버
- ablation을 통해 균형 구조가 우연이 아닌 필수 학습 신호임을 정량적으로 입증

## Limitation & Further Study

- 하드웨어 검증이 10회 시행으로 제한적이며 장기 안정성 데이터 부족
- Capture point 추정 등 균형 메트릭 계산이 simulation에서 완벽히 가능하나 실제 하드웨어에서의 추정 정확도 및 계산 비용에 대한 상세 분석 미흡
- MuJoCo로의 sim-to-sim 이전은 검증했으나 다른 로봇 플랫폼(예: 다른 anthropomorphic 디자인)으로의 일반화 미검증
- 다양한 바닥 재질, 극한 환경(미끄러운 표면, 불규칙 지형) 등에서의 강건성 평가 부재
- Curriculum 설계의 상세한 하이퍼파라미터 선택 및 다른 curriculum 전략과의 비교 분석 제한적
- 후속 연구: 하드웨어에서 균형 메트릭 실시간 추정 방법 개발, 다양한 로봇 플랫폼 및 지형에 대한 일반화 평가, 극한 환경에서의 강건성 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 고전적 균형 제어 원리를 강화학습에 체계적으로 임베딩하는 creative한 접근으로, ablation을 통해 이 구조의 필수성을 입증하고 93.4% 회복률로 강력한 실증 결과를 제시한다. 다만 하드웨어 검증 규모와 다양한 환경에서의 일반화 평가가 보강되면 더욱 설득력 있을 것이다.
