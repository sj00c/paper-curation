---
title: "1446_Large_VLM-based_Vision-Language-Action_Models_for_Robotic_Ma"
authors:
  - "Rui Shao"
  - "Wei Li"
  - "Lingsen Zhang"
  - "Renshan Zhang"
  - "Zhiyang Liu"
date: "2025.08"
doi: ""
arxiv: ""
score: 4.0
essence: "대규모 Vision-Language Model(VLM)을 기반으로 한 Vision-Language-Action(VLA) 모델들을 로봇 매니퓰레이션에 적용하는 연구의 첫 번째 체계적 설문조사로, Monolithic 모델과 Hierarchical 모델이라는 두 가지 주요 아키텍처 패러다임을 제시한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Embodied_Language_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shao et al._2025_Large VLM-based Vision-Language-Action Models for Robotic Manipulation A Survey.pdf"
---

# Large VLM-based Vision-Language-Action Models for Robotic Manipulation: A Survey

> **저자**: Rui Shao, Wei Li, Lingsen Zhang, Renshan Zhang, Zhiyang Liu, Ran Chen, Liqiang Nie | **날짜**: 2025-08-18 | **URL**: [https://arxiv.org/abs/2508.13073](https://arxiv.org/abs/2508.13073)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Outline of the organization of our comprehensive survey (top) and a chronological timeline of notable developmen*

대규모 Vision-Language Model(VLM)을 기반으로 한 Vision-Language-Action(VLA) 모델들을 로봇 매니퓰레이션에 적용하는 연구의 첫 번째 체계적 설문조사로, Monolithic 모델과 Hierarchical 모델이라는 두 가지 주요 아키텍처 패러다임을 제시한다.

## Motivation

- **Known**: 대규모 VLM은 이미지-텍스트 데이터셋으로 사전학습되어 시각-언어 이해에 뛰어나며, 전통적 로봇 제어는 규칙 기반 방식으로 미학습 환경에서 일반화 실패한다.
- **Gap**: 기존 연구는 VLM 또는 로봇 매니퓰레이션을 각각 다루고 있어 용어 불일치와 연구 단편화가 심하며, 이 두 분야의 교차점에서의 종합적 분석이 부재하다.
- **Why**: 로봇 매니퓰레이션은 제조, 물류, 의료 등 광범위하게 활용되는데, VLM 기반 VLA 모델이 미학습 객체와 환경에서 고수준 명령 해석 및 복잡한 작업 수행을 가능하게 한다.
- **Approach**: 광범위한 최근 연구를 검토하여 대규모 VLM 기반 VLA 모델을 명확히 정의하고, Monolithic(단일·이중 시스템)과 Hierarchical(계획-실행 분리) 두 가지 주요 아키텍처로 분류하며, 고급 영역 통합 및 데이터셋을 체계적으로 분석한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Comparison of the two principal categories of large VLM-based VLA models. Monolithic models (Sec. 3) integrate*

- **첫 번째 체계적 설문조사**: VLA 모델의 진화 궤적을 종단면 합성과 구조-기능적 비교 분석을 통해 제시
- **명확한 분류 체계**: Monolithic 모델(단일 시스템, 이중 시스템)과 Hierarchical 모델(planner-only, planner-policy)로 구분하여 아키텍처 설계 공간 정의
- **고급 연구 영역 통합**: Reinforcement learning, training-free optimization, learning from human videos, world model integration 등 네 가지 주요 고급 영역 포괄
- **특징 및 특성 종합**: Multimodal fusion, instruction following, 다차원 일반화 능력 등 distinctive characteristics 체계화
- **데이터셋 및 벤치마크 분석**: 시뮬레이션, 실제 환경, 인간 상호작용 데이터를 포함한 다양한 평가 자원 분류

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Outline of the organization of our comprehensive survey (top) and a chronological timeline of notable developmen*

- VLM 진화 및 로봇 매니퓰레이션 학습의 배경 지식 제공(Sec. 2)
- Monolithic 모델의 단일 시스템과 이중 시스템 아키텍처 상세 분석(Sec. 3)
- Hierarchical 모델의 중간 표현(subtasks, keypoints, programs, affordances) 기반 분류 및 분석(Sec. 4)
- RL 기반 최적화, training-free 방법, human video learning, world model 통합 검토(Sec. 5)
- Multimodal fusion, instruction following, generalization 특성 및 datasets/benchmarks 분류(Sec. 6-7)
- Open challenges 및 memory mechanisms, 4D perception, efficient adaptation, multi-agent cooperation 등 향후 방향 제시(Sec. 8)

## Originality

- VLM과 로봇 매니퓰레이션의 교차점을 다루는 첫 번째 종합 설문조사로, 기존 분산된 연구를 통일된 프레임워크로 통합
- Monolithic과 Hierarchical의 명확한 구분을 통해 설계 트레이드오프(시스템 통합 정도, 인지 분해 명시성)를 체계화
- RL, training-free optimization, human video learning, world model 등 네 가지 고급 영역을 통합하는 포괄적 분류체계 제시
- Architecture paradigm, operational strengths, datasets, emerging capabilities(memory, 4D perception, multi-agent cooperation)을 함께 분석하는 다각적 접근

## Limitation & Further Study

- 설문조사 논문으로 새로운 방법론이나 실증적 성과가 없으며, 기존 연구의 재분류에 중점
- VLA 모델의 실제 성능 비교는 연구마다 평가 환경이 다르면 제한적이므로 정량적 벤치마킹 미흡 가능성
- 2025년 이전 연구만 포함되었으므로, 빠르게 발전하는 이 분야의 최신 동향 반영 한계
- **후속 연구 방향**: VLA 모델의 표준화된 평가 환경 개발, memory mechanisms과 4D perception 기술의 구체적 구현 방안 탐색, multi-agent 로봇 협력 시나리오에서의 확장성 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 설문조사는 빠르게 성장하는 VLM 기반 VLA 분야의 첫 번째 체계적 종합으로, 명확한 정의, 일관된 분류체계, 그리고 포괄적 분석을 통해 학계의 연구 단편화를 해소하고 향후 발전 방향을 제시하는 의의가 크다. 정기적 업데이트 계획도 분야의 빠른 진전을 반영하는 강점이다.

## Related Papers

- 🔄 다른 접근: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — 둘 다 VLA 모델의 체계적 분석이지만, Large VLM-based 서베이는 로봇 매니퓰레이션에, Pure VLA 서베이는 VLA 모델 전반에 초점을 둔다.
- 🔗 후속 연구: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — Large VLM-based VLA 서베이가 Vision-Language-Action Models의 일반적 개념을 로봇 매니퓰레이션 영역에서 구체화하고 심화시킨다.
- 🧪 응용 사례: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — Large VLM-based VLA 모델들의 이론적 분류가 VLABench의 언어 조건부 로봇 제어 벤치마크 설계에 실용적 기준을 제공한다.
- 🔗 후속 연구: [[papers/1609_Vision-Language-Action_Models_for_Robotics_A_Review_Towards/review]] — VLA Models for Robotics 리뷰를 대규모 VLM 기반 시스템으로 구체화하여 로봇 매니퓰레이션에 특화한다.
- 🔗 후속 연구: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — What Matters in Building VLA Models은 대규모 VLM 기반 VLA의 핵심 설계 요소를 실용적 관점에서 심화함
