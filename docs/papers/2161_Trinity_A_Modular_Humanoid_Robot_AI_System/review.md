# Trinity: A Modular Humanoid Robot AI System

> **저자**: Jingkai Sun, Qiang Zhang, Gang Han, Wen Zhao, Zhe Yong, Yan He, Jiaxu Wang, Jiahang Cao, Yijie Guo, Renjing Xu | **날짜**: 2025-03-11 | **URL**: [https://arxiv.org/abs/2503.08338](https://arxiv.org/abs/2503.08338)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of the Modular Humanoid Robot AI System. In this system, task instructions are processed by both a visi*

LLM, VLM, RL을 통합한 모듈식 인간형 로봇 AI 시스템 Trinity를 제안하여 복잡한 환경에서 효율적인 제어를 실현한다. 계층적 아키텍처를 통해 언어 이해, 시각 인식, 동작 제어를 조화롭게 수행한다.

## Motivation

- **Known**: RL은 인간형 로봇의 동작 제어 성능을 향상시켰고, LLM과 VLM은 의미론적 계획과 환경 인식 능력을 제공한다. 하지만 기존 연구들은 이들 기술을 독립적으로 적용하거나 단순한 로봇 구성에만 적용해왔다.
- **Gap**: 복잡한 전신 제어와 조작이 필요한 인간형 로봇에서 RL, LLM, VLM을 효과적으로 통합하는 방법이 부재하며, 실제 로봇 플랫폼에서의 검증도 제한적이다.
- **Why**: 인간형 로봇이 인간 생활 공간에서 복잡한 작업을 수행하려면 언어 이해, 시각 인식, 안정적 동작 제어가 동시에 필요하며, 이는 로봇 지능화의 핵심 과제이다.
- **Approach**: 모듈식 계층 구조를 통해 LLM (의미론적 태스크 계획), VLM (환경 인식), RL (동작 제어)을 분리하고 상호작용하게 설계하여, 각 모듈의 독립적 최적화와 협력적 동작을 동시에 실현한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Process of a humanoid robot opening a door. The humanoid robot begins*

- **첫 통합 시스템**: LLM, VLM, RL을 인간형 로봇에 처음 통합하여 실제 대형 로봇에서의 실행 가능성과 효과성을 입증했다.
- **모듈식 계층 설계**: 복잡한 문제를 분해하고 교체 가능한 모델들로 처리하여 유연성과 확장성을 향상시켰다.
- **해석성과 안전성**: 다중 모듈 간 상호작용을 통해 시스템 해석성을 보장하고 로봇 동작의 안전성을 확보한다.

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of the Modular Humanoid Robot AI System. In this system, task instructions are processed by both a visi*

- LLM을 사용하여 자연어 지시사항으로부터 의미론적 이해와 장기 태스크 계획을 수행
- VLM으로 환경 인식과 객체 감지를 통해 조작 대상의 위치와 특성을 파악
- RL 기반 보행 정책(locomotion policy)과 손 제어기(hand controller)로 안정적인 동작 제어 구현
- Arm Planner를 통해 상지 움직임에 대응하여 하지와 무게중심을 조정하여 균형 유지
- 시뮬레이션 환경에서 RL 정책을 학습하고 실제 로봇에 배포

## Originality

- 인간형 로봇의 전신 제어 문제에 RL, LLM, VLM을 처음으로 통합한 시스템 설계
- 보행(locomotion) 정책과 조작(manipulation) 네트워크를 분리하여 로코-조작 능력 향상
- 계층적 모듈 구조를 통해 각 기술의 장점을 활용하면서 시스템 안정성과 해석성을 동시에 확보
- 실제 대형 인간형 로봇 플랫폼에서의 포괄적 시스템 검증

## Limitation & Further Study

- 시뮬레이션-현실 간의 차이(sim-to-real gap)가 여전히 존재하며, 특히 복잡한 상호작용과 변형 가능한 환경에서의 일반화 능력 제한
- 데이터 수집 비용이 높으며, 특정 시나리오에 대한 의존성이 존재
- 모듈 간 통신 오류 또는 개별 모듈의 실패가 시스템 전체에 미치는 영향에 대한 분석 부재
- 후속 연구로 더 강력한 sim-to-real 전이 학습 기법, 온라인 학습과 적응(adaptation) 능력 강화, 복잡한 멀티-태스크 학습 방법 개발이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Trinity는 RL, LLM, VLM을 효과적으로 통합한 혁신적 인간형 로봇 AI 시스템으로, 모듈식 설계를 통해 유연성과 해석성을 확보하고 실제 로봇에서의 동작을 입증함으로써 구현적 가치가 높다. 다만 sim-to-real 갭과 모듈 간 상호작용의 견고성에 대한 심화 분석이 필요하다.
