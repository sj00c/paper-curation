# Embracing Evolution: A Call for Body-Control Co-Design in Embodied Humanoid Robot

> **저자**: Guiliang Liu, Bo Yue, Yi Jin Kim, Kui Jia | **날짜**: 2025-10-03 | **URL**: [https://arxiv.org/abs/2510.03081](https://arxiv.org/abs/2510.03081)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: The co-design framework for humanoid robots, which can be formulated as a bi-level*

인간형 로봇의 제어 정책과 물리적 구조를 동시에 진화시키는 co-design 메커니즘을 제안하며, 이를 bi-level 최적화 문제로 공식화하여 embodied intelligence 달성의 필수 요소임을 주장하는 위치 논문이다.

## Motivation

- **Known**: 최근 인간형 로봇 연구는 고정된 물리적 구조에서 제어 정책 최적화에 집중하고 있으며, 사족 로봇, 소프트 로봇 등 다른 플랫폼에서는 co-design이 부분적으로 탐구되었다.
- **Gap**: 인간형 로봇에서 co-design의 필요성과 실행 가능성이 충분히 입증되지 않았으며, 물리적 구조 진화와 embodied intelligence 간의 명확한 연결고리가 부재하다.
- **Why**: 생물학적 진화와 유사하게 로봇의 형태와 행동을 동시에 최적화할 수 있다면 다양한 실제 환경과 작업에 더 효과적으로 적응할 수 있으며, 이는 범용 물리 에이전트 개발의 핵심이다.
- **Approach**: bi-level 최적화 프레임워크를 통해 제어 정책 학습과 로봇 물리적 구조 설계를 통합하며, strategic exploration, Sim2Real transfer, meta-policy learning 등의 방법론을 제시한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: The co-design framework for humanoid robots, which can be formulated as a bi-level*

- **Co-design 프레임워크 공식화**: bi-level 최적화 문제로서의 인간형 로봇 co-design 수학적 정의
- **실행 가능성 논증**: 현존하는 learning-based solver와 Sim2Real 기법을 통한 co-design의 알고리즘적 실행 가능성 제시
- **필요성 분석**: methodological, application-driven, community-oriented 관점에서 co-design의 본질적 역할 분석
- **개방 연구 질문 도출**: 단기 혁신부터 장기 목표까지 아우르는 구체적 연구 질문 제시

## How

![Figure 1](figures/fig1.webp)

*Figure 1: The co-design framework for humanoid robots, which can be formulated as a bi-level*

- bi-level 최적화 프레임워크: Level I (embodied robot controlling)과 Level II (embodied robot designing)의 이중 구조로 제어와 설계 문제 분리
- Strategic robot structure exploration을 통한 효율적인 설계 공간 탐색
- Sim2Real transfer learning으로 시뮬레이션 기반 co-design을 실제 로봇에 적용
- Meta-policy learning을 활용한 다양한 로봇 형태에 대한 일반화된 제어 정책 학습
- Vision-Language Model 기반 추론 모델과 MDP 기반 행동 모델의 계층적 아키텍처 활용

## Originality

- 인간형 로봇 특화 co-design 문제의 최초 체계적 공식화 및 위치 논문으로서의 종합적 논의
- Embodied intelligence의 필수 요소로서 co-design의 역할을 methodological, application, community 관점에서 다층적으로 분석
- 기존 사족 로봇 등의 co-design 연구를 인간형 로봇의 복잡한 다자유도 시스템으로 확장하려는 시도
- 생물학적 진화 원리를 로보틱스에 적용하는 철학적 기초 제시

## Limitation & Further Study

- 위치 논문으로서 구체적 실험 결과나 정량적 평가가 부재하며, 제안된 방법론의 실제 성능 입증 필요
- Sim2Real transfer의 domain gap 해결 방법이 충분히 구체화되지 않았으며, 실제 로봇의 물리적 제약 조건 반영 부족
- 계산 복잡도와 수렴 성능에 대한 분석 및 기존 고정 설계 대비 성능 향상의 정량적 근거 제시 필요
- 인간형 로봇의 다양한 형태(전신형, 간단형, 바퀴형 등)에 대한 co-design 적용 가능성 차이 분석 부족
- 후속 연구로 실제 로봇 하드웨어에서의 co-design 실험 및 장시간 적응 성능 평가, 계산 효율성 개선, multi-task co-design 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 인간형 로봇의 embodied intelligence 달성을 위해 co-design의 필수성을 체계적으로 주장하고 실행 가능한 방법론을 제시하는 영향력 있는 위치 논문이다. 다만 구체적인 실험 검증과 정량적 성능 평가를 통한 후속 연구로 보강될 필요가 있다.
