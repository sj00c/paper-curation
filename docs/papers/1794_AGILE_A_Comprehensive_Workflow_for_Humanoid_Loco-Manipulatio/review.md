# AGILE: A Comprehensive Workflow for Humanoid Loco-Manipulation Learning

> **저자**:  | **날짜**: 2026-03-31 | **URL**: [https://arxiv.org/abs/2603.20147](https://arxiv.org/abs/2603.20147)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of agile learning workflow. The workflow covers prepare-training, batch cloud training*

AGILE는 휴머노이드 로봇의 강화학습 정책 개발을 위한 엔드투엔드 워크플로우로, 환경 검증, 재현 가능한 학습, 통합 평가, 디스크립터 기반 배포의 4단계를 표준화하여 시뮬레이션-실세계 전이의 신뢰성을 향상시킨다.

## Motivation

- **Known**: 강화학습을 통해 인상적인 휴머노이드 행동을 시뮬레이션에서 구현할 수 있으며, Isaac Gym/Lab 등의 GPU 기반 시뮬레이터와 Holosoma, HumanoidVerse 등의 학습 프레임워크가 존재한다.
- **Gap**: 현재 휴머노이드 RL 개발은 환경 검증, 학습, 평가, 배포 단계가 체계적으로 연결되지 않아 환경 오류가 학습 후에 발견되고, 정책 내보내기 시 joint 순서 불일치 등의 silent bug가 발생하며, 실제 배포 전 정량적 검증이 부족하다.
- **Why**: 휴머노이드 로봇의 실제 배포는 매우 까다로운 작업이며, 구조화된 워크플로우를 통해 재현성과 신뢰성을 확보하는 것이 휴머노이드 RL의 실용화에 필수적이다.
- **Approach**: Isaac Lab과 RSL-RL을 기반으로 네 단계 파이프라인을 구현하여: (1) interactive GUI를 통한 사전 검증, (2) 자동화된 하이퍼파라미터 스윕과 알고리즘 강화를 포함한 재현 가능한 학습, (3) deterministic scenario 테스트와 stochastic rollout을 결합한 통합 평가, (4) YAML I/O 디스크립터를 통한 일관된 정책 내보내기를 제공한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of agile learning workflow. The workflow covers prepare-training, batch cloud training*

- **구조화된 라이프사이클**: 환경 검증부터 배포까지 4단계 워크플로우를 표준화하여 휴머노이드 RL을 체계적인 공학 프로세스로 전환
- **통합 평가 프레임워크**: deterministic scenario 테스트와 stochastic rollout을 결합하며 joint jerk, limit violation 등의 배포 지향적 motion quality 메트릭을 제공
- **다중 작업 검증**: Unitree G1과 Booster T1 두 플랫폼에서 velocity tracking, height-controlled locomotion, stand-up, motion imitation, loco-manipulation 등 5개 작업으로 sim-to-real 전이 성공 입증
- **알고리즘 강화 라이브러리**: L2C2, reward normalization, value-bootstrapped terminations, symmetry augmentation, virtual harness 등 여러 sim-to-real transfer 기법을 ablation을 통해 검증하고 통합

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of agile learning workflow. The workflow covers prepare-training, batch cloud training*

- **Prepare 단계**: joint control, object manipulation, reward visualization용 interactive debug GUI로 모델 오류와 MDP 오설정을 GPU 학습 전에 빠르게 식별
- **Train 단계**: Isaac Lab 기반 parallel GPU 시뮬레이션 환경에서 자동화된 hyperparameter sweep, experiment tracking, 토글 가능한 algorithmic enhancements 제공
- **Evaluate 단계**: 두 가지 평가 방식을 통합—deterministic scenario 테스트로 특정 동작 검증, randomized command rollout으로 robustness 평가, 동시에 per-joint motion quality 메트릭(jerk, limit violations) 수집
- **Deploy 단계**: 학습된 정책을 self-contained YAML I/O descriptor와 함께 자동 내보내기하여 joint ordering, action scaling 등을 해결하고 MuJoCo 시뮬레이션 및 실제 하드웨어에서 일관된 inference pipeline 제공
- **Decoupled whole-body control**: frozen locomotion 정책을 lower-body API로 활용하고 독립적인 upper-body expert가 VLA fine-tuning용 demonstration 수집하는 모듈화된 접근

## Originality

- **워크플로우 중심 접근**: 알고리즘 혁신보다는 현실적인 RL 개발 라이프사이클 전체를 체계화하는 infrastructure 중심 접근이 distinctive
- **descriptor 기반 배포**: YAML I/O descriptor를 통한 명시적인 인터페이스 표준화로 silent bug 제거 및 cross-simulator 검증 가능성 확보
- **통합 evaluation framework**: deterministic과 stochastic 평가를 단일 pipeline에서 조합하고 motion quality 메트릭을 자동화된 regression testing에 활용
- **오픈소스 공개**: Isaac Lab과 RSL-RL을 기반으로 사전학습된 체크포인트와 함께 배포하여 재현성과 접근성 극대화

## Limitation & Further Study

- **시뮬레이터 범위 제한**: 현재 Isaac Lab 기반이므로 MuJoCo, PyBullet 등 다른 물리 엔진의 native 지원이 부족하며, 다중 시뮬레이터 백엔드 지원은 미흡
- **도메인 갭 근본 해결 부족**: sim-to-real transfer 강화 기법들(L2C2, randomization 등)은 포함하지만, 물리적 차이의 근본적인 갭을 완전히 해소하지는 못함
- **하드웨어 플랫폼 일반화**: 두 플랫폼(Unitree G1, Booster T1)에서만 검증되었으므로 다른 humanoid 로봇으로의 일반화 정도가 불명확
- **후속 연구 방향**: (1) 더 다양한 물리 엔진 지원 추가, (2) 자동화된 domain randomization 정책 설계, (3) 실시간 online adaptation 메커니즘 통합, (4) 다양한 embodiment에 대한 워크플로우 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: AGILE는 휴머노이드 RL의 실제 배포 단계에서 야기되는 현실적 문제들을 직시하고 이를 해결하기 위한 체계적인 엔지니어링 워크플로우를 제시한다. 알고리즘 혁신보다는 infrastructure 중심이지만, 재현성, 신뢰성, 배포 가능성 측면에서 매우 실용적이며 5개 작업과 2개 플랫폼에서의 성공적인 sim-to-real 전이로 효과를 입증했다.
