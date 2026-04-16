---
title: "1486_Multimodal_Perception_for_Goal-oriented_Navigation_A_Survey"
authors:
  - "I-Tak Ieong"
  - "Hao Tang"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 자율 네비게이션을 위한 멀티모달 인식 기법들을 inference domain이라는 통합 관점에서 조직화하고 분석하는 포괄적인 서베이로, 약 200개의 관련 논문을 검토하여 시각, 언어, 음향 정보를 활용한 네비게이션 접근법들의 공통 원리와 차이를 체계적으로 제시한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Ieong and Tang_2025_Multimodal Perception for Goal-oriented Navigation A Survey.pdf"
---

# Multimodal Perception for Goal-oriented Navigation: A Survey

> **저자**: I-Tak Ieong, Hao Tang | **날짜**: 2025-04-22 | **URL**: [https://arxiv.org/abs/2504.15643](https://arxiv.org/abs/2504.15643)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Timeline of the historical development of navigation tasks and their representative approaches. Different colors*

이 논문은 자율 네비게이션을 위한 멀티모달 인식 기법들을 inference domain이라는 통합 관점에서 조직화하고 분석하는 포괄적인 서베이로, 약 200개의 관련 논문을 검토하여 시각, 언어, 음향 정보를 활용한 네비게이션 접근법들의 공통 원리와 차이를 체계적으로 제시한다.

## Motivation

- **Known**: 지난 10년간 목표 지향 네비게이션은 단순한 기하학적 경로 계획에서 deep learning 기반의 정교한 멀티모달 추론으로 진화했으며, PointNav, ImageNav, ObjectNav, AudioGoalNav 등 다양한 네비게이션 과제들이 개발되어 왔다.
- **Gap**: 기존 문헌에서는 서로 다른 네비게이션 과제들이 공유하는 근본적인 computational foundation과 reasoning mechanism을 통일된 관점에서 분석하지 못하고 있으며, 멀티모달 정보의 통합 가능성과 과제를 체계적으로 검토하지 않았다.
- **Why**: 다양한 네비게이션 과제들 간의 공통 원리를 파악하면 새로운 연구 방향을 도출할 수 있고, 멀티모달 인식의 통합을 이해하는 것은 더욱 강력한 자율 에이전트 개발에 필수적이다.
- **Approach**: 논문은 inference domain이라는 개념을 중심으로 navigation 방법들을 6가지 범주(latent map-based, implicit representation, graph-based, linguistic, embedding-based, diffusion model-based)로 조직화하고, 각 네비게이션 과제(PointNav, ObjectNav, ImageNav, AudioGoalNav)에서 이들 domain이 어떻게 나타나는지 분석한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Timeline of the historical development of navigation tasks and their representative approaches. Different colors*

- **inference domain 기반 분석틀 제시**: 목표 지향 네비게이션 방법들을 6가지 주요 inference domain으로 분류하고, 기하학적 추론에서 의미적 이해로의 진화 과정을 체계화
- **cross-task 통찰력 도출**: latent map-based 방법이 기하학적 일관성을 유지하고, implicit representation이 end-to-end 학습을 지원하며, linguistic domain이 상식 지식을 활용하는 등 각 domain의 distinctive strengths 식별
- **200개 논문의 종합적 검토**: PointNav부터 AudioGoalNav까지 다양한 네비게이션 과제에서 사용된 approaches의 계층적 분류 및 비교
- **멀티모달 통합의 과제와 기회 조사**: visual, linguistic, acoustic 정보의 융합 가능성과 implementation 도전과제 분석

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Timeline of the historical development of navigation tasks and their representative approaches. Different colors*

- 수학적 framework를 통한 통일된 문제 정의: 상태공간 S, 관측공간 O, 행동공간 A, 목표공간 G로 모든 네비게이션 과제 형식화
- 각 inference domain별 computational foundations 분석: latent map-based는 differentiable projections를 이용한 2D/3D mapping, implicit representation은 RNN/transformer를 이용한 internal state representation 등
- 네비게이션 과제별 섹션 구성: PointNav, ObjectNav, ImageNav, AudioGoalNav 각각에서 주요 방법들을 inference domain별로 분류하고 비교
- 시간적 진화 추적: Figure 1의 timeline을 통해 각 과제와 방법들의 historical development 시각화
- 데이터셋 및 evaluation metrics 정리: HM3D, Gibson, Matterport3D, AI2-THOR 등 주요 시뮬레이션 환경의 특성 비교

## Originality

- **inference domain이라는 새로운 분석 패러다임**: 기존의 task-centric 분류 대신 방법론의 근본적인 reasoning mechanism을 중심으로 조직화하여 cross-task insights 제공
- **멀티모달 통합의 체계적 분석**: visual, linguistic, acoustic modality를 다루는 모든 네비게이션 과제를 단일 framework 내에서 비교
- **diffusion model-based domain의 emergence 강조**: 최신 generative modeling 접근법을 기존 5가지 domain과 함께 제시하여 미래 방향 제시
- **200개 논문의 종합적 integration**: 대규모 문헌 검토를 통해 분산된 연구들의 공통 패턴과 distinctive strengths를 체계적으로 도출

## Limitation & Further Study

- **실제 환경에서의 검증 부족**: 대부분 분석이 시뮬레이션 환경(Habitat, AI2-THOR)에 기반하고 있으며, 실제 로봇 플랫폼에서의 성능 비교가 제한적
- **멀티모달 fusion의 깊이 부족**: linguistic과 acoustic modality의 통합이 주로 linguistic domain에 집중되어 있고, 진정한 의미의 3-modal fusion 사례가 부족할 수 있음
- **computational efficiency 분석 미흡**: 각 inference domain의 computational cost와 실시간 성능 비교가 상세하지 않아 실제 배포 가능성 평가 어려움
- **새로운 데이터셋 개발의 필요성**: 현존 데이터셋들이 특정 환경(실내, 특정 구조)에 편중되어 있어 more diverse 시나리오의 벤치마크 필요
- **향후 연구 방향**: (1) real-world deployment를 위한 sim-to-real transfer learning 강화, (2) 더욱 효율적인 diffusion model-based approaches 개발, (3) multimodal fusion을 위한 공통 representation 학습

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 inference domain이라는 혁신적인 분석 틀을 통해 여러 네비게이션 과제를 통합적으로 이해할 수 있게 한 종합적이고 잘 구성된 서베이로, 분야의 역사적 발전과 현재 상황을 명확하게 제시하며 멀티모달 AI 네비게이션 연구의 미래 방향을 제시하는 데 큰 가치가 있다.

## Related Papers

- 🏛 기반 연구: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — 멀티모달 목표 지향 네비게이션 서베이가 Vision-Language Navigation의 기존 분류 체계를 멀티모달 인식으로 확장한 연구이다.
- 🔗 후속 연구: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — 멀티모달 네비게이션 서베이의 inference domain 관점이 NaVid의 비디오 기반 VLM 계획과 결합되어 더 정교한 네비게이션 추론을 가능하게 한다.
- 🧪 응용 사례: [[papers/1463_LOVON_Legged_Open-Vocabulary_Object_Navigator/review]] — 멀티모달 네비게이션의 이론적 프레임워크가 LOVON의 다리 로봇 개방형 어휘 객체 네비게이션에 실제 적용된다.
- 🏛 기반 연구: [[papers/1441_JanusVLN_Decoupling_Semantics_and_Spatiality_with_Dual_Impli/review]] — JanusVLN의 spatial-geometric과 semantic 정보 분리 접근법이 멀티모달 목표 지향 네비게이션의 핵심 설계 원리를 제공한다.
- 🔗 후속 연구: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — VLN을 goal-oriented navigation의 multimodal perception으로 확장한 포괄적 조사입니다.
