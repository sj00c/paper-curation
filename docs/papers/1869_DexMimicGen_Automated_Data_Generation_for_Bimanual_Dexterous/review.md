# DexMimicGen: Automated Data Generation for Bimanual Dexterous Manipulation via Imitation Learning

> **저자**: Zhenyu Jiang, Yuqi Xie, Kevin Lin, Zhenjia Xu, Weikang Wan, Ajay Mandlekar, Linxi Fan, Yuke Zhu | **날짜**: 2024-10-31 | **URL**: [https://arxiv.org/abs/2410.24185](https://arxiv.org/abs/2410.24185)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: DexMimicGen Overview. DexMimicGen offers an efficient pipeline*

DexMimicGen은 소수의 인간 시연으로부터 simulation에서 자동으로 대규모 궤적 데이터를 생성하여 양손 dexterous 로봇 조작 학습을 위한 imitation learning 데이터 수집 병목을 해결하는 시스템이다.

## Motivation

- **Known**: Imitation learning은 인간 시연으로부터 로봇 조작 기술을 학습하는 효과적인 방법이며, MimicGen은 단일 팔 로봇에 대해 자동 데이터 생성을 성공적으로 적용했다.
- **Gap**: 양손 dexterous 로봇의 경우 두 팔과 multi-fingered 손을 동시에 제어해야 하고 팔 간 조정이 필요하여, 기존 MimicGen 접근법을 직접 적용할 수 없으며 전문화된 해결책이 필요하다.
- **Why**: 양손 humanoid 로봇의 teleoperation 데이터 수집은 높은 비용과 인력이 소요되며 operator의 부담이 크기 때문에, 자동화된 simulation 기반 데이터 생성은 대규모 dataset 구축을 가능하게 한다.
- **Approach**: DexMimicGen은 per-arm 기반 subtask 분할, 동기화 전략, 순서 제약 메커니즘을 도입하여 parallel, coordination, sequential 세 가지 유형의 양손 조작 subtask를 처리한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: DexMimicGen Overview. DexMimicGen offers an efficient pipeline*

- **자동 데이터 생성 시스템**: 60개의 인간 시연으로부터 21K개의 생성된 데모를 9개의 simulation 환경에서 생성
- **양손 조정 메커니즘**: Asynchronous per-arm 실행, 동기화, 순서 제약을 통해 independent, coordinated, sequential subtask 처리 가능
- **실제 배포 검증**: Real-to-sim-to-real 파이프라인을 통해 can sorting 작업에서 90% 성공률 달성 (인간 시연만 사용시 0%)

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: DexMimicGen Workflow. Left: segment source demonstrations for each arm through manually defined heuristics or hu*

- 각 팔에 대해 독립적으로 subtask를 분할하는 per-arm 분할 전략 적용
- Coordination subtask에서 두 팔의 정렬을 위한 동기화 메커니즘 구현
- Sequential subtask에서 올바른 action 순서를 보장하는 ordering constraint 메커니즘
- Source demonstration으로부터 변환된 객체 중심의 manipulation segment를 simulation에서 replay
- 성공한 생성 궤적만 dataset에 유지하여 물리적 타당성 보증
- Behavioral Cloning으로 생성된 dataset에서 policy 학습

## Originality

- MimicGen의 단일 팔 접근법을 양손 dexterous 조작으로 확장한 첫 시도
- Parallel, coordination, sequential 세 가지 subtask 유형을 명시적으로 정의하고 각각 다른 메커니즘으로 처리
- Per-arm 기반 asynchronous 실행 전략으로 두 팔의 독립적이면서도 조정된 행동 가능하게 함
- Real-to-sim-to-real 파이프라인으로 실제 humanoid 로봇 배포 달성

## Limitation & Further Study

- 세 가지 subtask 유형의 분류가 모든 양손 작업을 포괄하는지 불명확하며, 더 복잡한 상호작용 패턴이 있을 수 있음
- 가정 A3 (object pose 관찰 가능성)이 모든 실제 시나리오에서 만족되기 어려울 수 있음
- Simulation 대 실제 환경 간의 domain gap이 완전히 해결되지 않음
- 대규모 dataset 생성 시 computation cost 분석 부재
- 단일 can sorting 작업만 실제 배포하여 다양한 작업에서의 일반화 능력 미검증
- 후속 연구: 더 복잡한 양손 조정 패턴, 자동 subtask 분할, vision-based state estimation 통합 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: DexMimicGen은 양손 dexterous 로봇 조작을 위한 자동 데이터 생성의 실질적인 해결책을 제시하며, MimicGen을 의미 있게 확장하고 실제 humanoid 배포로 그 효과를 입증했으나, 한계된 실제 작업 검증과 일반화 능력 평가가 필요하다.
