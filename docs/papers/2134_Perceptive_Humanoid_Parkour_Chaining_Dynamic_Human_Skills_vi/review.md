# Perceptive Humanoid Parkour: Chaining Dynamic Human Skills via Motion Matching

> **저자**: Zhen Wu, Xiaoyu Huang, Lujie Yang, Yuanhang Zhang, Koushil Sreenath, Xi Chen, Pieter Abbeel, Rocky Duan, Angjoo Kanazawa, Carmelo Sferrazza, Guanya Shi, C. Karen Liu | **날짜**: 2026-02-17 | **DOI**: [10.48550/arXiv.2602.15827](https://doi.org/10.48550/arXiv.2602.15827)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Perceptive Humanoid Parkour overview. Atomic parkour skills are composed into long-horizon kinematic reference*

Motion matching을 통해 인간의 동작 데이터를 원자적 기술로 합성하고, DAgger와 RL을 결합한 teacher-student 파이프라인으로 단일 깊이 기반 정책으로 증류하여 휴머노이드 로봇이 복잡한 장애물 코스에서 자율적으로 장시간 파쿠르를 수행하도록 한다.

## Motivation

- **Known**: 휴머노이드 로봇의 안정적인 보행은 다양한 지형에서 구현되었지만, 높은 역학적 동작의 민첩성과 적응성을 포착하는 것과 환경에 대한 인식 기반의 장시간 기술 합성은 여전히 미해결 과제이다.
- **Gap**: 인간의 동작 데이터는 일반적으로 매우 희소하며(기술당 1-2개 데모), 기술 간 부드러운 전환과 장시간 과제에서의 적응적 변화 생성이 어렵고, 여러 동적 기술을 단일 정책으로 통합할 때 순수 DAgger 증류의 한계가 있다.
- **Why**: 파쿠르는 높은 차원의 제어 공간에서 동적 기술 실행, 시각 인식을 통한 환경 적응, 다양한 기술의 자동 선택과 전환이 필요한 복합적 도전이며, 이를 해결하면 불규칙한 지형에서 휴머노이드 로봇의 민첩성을 획기적으로 향상시킬 수 있다.
- **Approach**: Motion matching을 nearest-neighbor search 기반으로 원자적 기술들을 장시간 운동학 궤적으로 합성하고, privileged state로 training된 motion-tracking RL expert policies를 depth-conditioned student policy로 DAgger와 RL 목적함수의 결합을 통해 증류한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Perceptive Humanoid Parkour (PHP) enables a Unitree G1 humanoid robot to execute highly dynamic, long-horizon*

- **Motion matching 기반 기술 합성**: OmniRetarget으로 인간 동작을 재타겟팅한 원자적 기술들을 feature space에서의 nearest-neighbor search로 구성하여 다양한 접근 거리와 시간에 적응적인 장시간 궤적 생성
- **확장 가능한 증류 파이프라인**: DAgger와 RL을 결합한 hybrid 목적함수로 여러 expert policies를 단일 depth 기반 multi-skill 정책으로 효율적으로 증류
- **실제 로봇 구현**: Unitree G1 휴머노이드에서 1.25m(로봇 높이의 96%) 높이의 장애물 등반, ~3m/s 속도의 vault, 60초 연속 복합 파쿠르 코스 자율 수행 실증
- **Zero-shot sim-to-real transfer**: 시뮬레이션에서 학습한 depth 정책이 실제 로봇에서 추가 fine-tuning 없이 작동하며, 실시간 장애물 교란에 대한 closed-loop 적응 달성

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Perceptive Humanoid Parkour overview. Atomic parkour skills are composed into long-horizon kinematic reference*

- OmniRetarget을 사용하여 인간 모션 캡처 데이터를 로봇 호환 형태로 재타겟팅
- Motion matching 알고리즘으로 feature space에서 nearest-neighbor search를 수행하여 기술 간 부드러운 전환을 포함한 장시간 kinematic 궤적 생성
- 각 기술별로 motion-tracking RL expert policies를 proprioception과 heightmap으로 training하여 정확한 궤적 추종 학습
- DAgger를 통한 behavior cloning으로 초기 depth 기반 student policy 부트스트랩
- RL 보상 신호(task-level 성공도)를 추가하여 student policy 최적화 및 compounding error 감소
- 학습된 정책에서 depth image와 discrete 2D velocity command로부터 자동 기술 선택 및 실행 메커니즘 구현

## Originality

- 파쿠르 같은 고도로 동적인 휴머노이드 동작에 motion matching을 최초로 적용하여 희소한 인간 동작 데이터의 효율적 활용
- DAgger와 RL을 결합한 hybrid 증류 방식으로 pure imitation의 한계를 극복하고 높은 역학적 기술 학습 성능 향상
- 단일 depth 기반 정책으로 수십 개의 서로 다른 동적 파쿠르 기술을 통합하고 자동 기술 선택 및 부드러운 전환 실현
- 복잡한 장애물 과정에서의 실시간 폐루프 적응 및 zero-shot sim-to-real 전이 달성

## Limitation & Further Study

- Motion matching은 기존 인간 동작 데이터의 질과 다양성에 제한적이며, 캡처되지 않은 새로운 기술 개발 불가
- 현재 프레임워크는 discrete velocity command 기반으로 높은 수준의 자율 계획 기능(예: 복잡한 경로 계획)이 부족
- 깊이 센서만 사용하므로 폐쇄된 공간이나 악광 환경에서의 성능 제한 가능성
- 학습 과정에서 privileged state(heightmap) 정보가 필요하므로 현장 데이터 수집 시 정확한 환경 맵 구성의 어려움
- 후속 연구: 다양한 로봇 형태로의 일반화, 장시간 복합 계획 능력 통합, 다중 센서 기반 정책 확장 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 연구는 motion matching과 hybrid DAgger-RL 증류를 통해 희소한 인간 동작 데이터로부터 복잡한 파쿠르 기술을 효과적으로 합성 및 학습하여 휴머노이드 로봇의 동적 환경 적응 능력을 획기적으로 향상시켰으며, 실제 로봇에서의 강인한 구현과 zero-shot sim-to-real 전이는 높은 실용적 가치를 입증한다.
