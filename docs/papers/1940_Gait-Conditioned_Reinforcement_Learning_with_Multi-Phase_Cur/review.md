# Gait-Conditioned Reinforcement Learning with Multi-Phase Curriculum for Humanoid Locomotion

> **저자**: Tianhu Peng, Lingfan Bao, Chengxu Zhou | **날짜**: 2025-05-27 | **URL**: [https://arxiv.org/abs/2505.20619](https://arxiv.org/abs/2505.20619)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Human-like multi-gait locomotion on the Unitree G1*

인간에게서 영감을 얻은 보상 형성과 gait-conditioned reward routing을 통해 단일 recurrent policy에서 서서기, 걷기, 달리기 및 전환을 학습하는 통합 reference-free RL 프레임워크를 제시한다.

## Motivation

- **Known**: Reference-기반 방법(AMP 등)은 MoCap 데이터에 의존하고 형태 불일치 문제가 있으며, 다중 기술 학습을 위해 정책 증류나 혼합 전문가 같은 복잡한 구조가 필요하다.
- **Gap**: MoCap 없이 자연스러운 다중 gait 전환을 지원하면서도 보상 간섭을 완화하고 단일 통합 정책으로 구현하는 방법이 부족하다.
- **Why**: 인간형 로봇의 실제 배포를 위해 안정적이고 효율적인 다중 움직임 모드가 필수적이며, 참조 데이터 없이 자연스러운 움직임을 생성할 수 있는 확장 가능한 솔루션이 필요하다.
- **Approach**: Gait ID 기반 동적 보상 라우팅 메커니즘과 직선 무릎 자세, arm-leg swing 조율 등 생물역학 기반 보상 항을 통합하고, 다단계 구조화된 커리큘럼으로 점진적으로 기술 복잡도를 확대한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Human-like multi-gait locomotion on the Unitree G1*

- **Reference-free multi-gait learning**: MoCap 데이터 없이 서서기, 걷기, 달리기, 전환을 단일 recurrent 정책으로 학습
- **Gait-conditioned reward routing**: One-hot gait ID 기반 동적 보상 활성화로 보상 간섭 완화 및 안정적 다중 gait 학습 지원
- **Biomechanically natural motion**: 각속도량 제약, 직선 무릎 자세, 조율된 arm-leg swing 등을 통해 인간처럼 자연스러운 움직임 생성
- **Real robot validation**: Unitree G1 인간형 로봇에서 서서기, 걷기, walk-to-stand 전환 실증

## How


- Gait-conditioned reward routing 메커니즘: gait ID를 통해 현재 모드에 해당하는 보상 목표만 활성화
- Biomechanical reward shaping: 각속도량 페널티, 직선 무릎 자세 장려, arm-leg anti-phase coordination, 발 드래그 최소화, push-off 동역학 등 포함
- Multi-phase curriculum: 초기 서서기 → 걷기 → 달리기 → 전환으로 단계적 복잡도 증가 및 명령 공간 확대
- Recurrent policy architecture: LSTM 기반으로 시간적 동역학 캡처하고 gait 전환 시 smooth 동작 가능
- One-hot gait ID encoding: 관찰에 포함된 compact 가이트 식별자로 정책 조건화

## Originality

- 단순하면서도 효과적인 gait-conditioned reward routing으로 다중 gait를 하나의 통합 정책으로 학습하는 방식
- MoCap 참조 없이 생물역학 원리에서 직접 도출한 보상 항으로 자연스러운 움직임 생성
- Multi-policy 증류나 혼합 전문가 같은 복잡한 모듈식 구조 대신 단일 recurrent 정책으로 다중 기술 통합
- 생물학적 운동 발달에서 영감을 받은 구조화된 다단계 커리큘럼

## Limitation & Further Study

- 시뮬레이션에서 다양한 gait 전환 실현이 실제 로봇에서는 제한적(walk-to-stand 등만 검증)
- 외부 충격이나 극단적 환경에 대한 견고성 평가 부족
- 보상 가중치 튜닝이 여전히 필요하며 완전 자동화된 설계 방법 미제시
- 후속 연구: 더 많은 gait 모드(계단 오르내리기, 점프 등) 확장, 시뮬-투-리얼 간극 감소, 동적 환경 적응성 강화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 gait-conditioned reward routing과 생물역학 기반 보상 설계를 통해 MoCap 없이 자연스러운 다중 gait 학습을 가능하게 하는 우아한 프레임워크를 제시하며, 실제 인간형 로봇에서의 검증으로 실용성을 입증한다.
