---
title: "1497_OctoNav_Towards_Generalist_Embodied_Navigation"
authors:
  - "Chen Gao"
  - "Liankai Jin"
  - "Xingyu Peng"
  - "Jiazhao Zhang"
  - "Yue Deng"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "자유형식의 멀티모달 멀티기능 지시를 따를 수 있는 일반화된 embodied navigation 에이전트를 위해 OctoNav-Bench 벤치마크와 OctoNav-R1 방법을 제안한다. Think-Before-Action 추론을 통해 복잡한 네비게이션 작업에서 향상된 성능을 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_AI_Architectures"
  - "cat/Robot_Policy_Learning"
  - "sub/Semantic_Task_Generalization"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Gao et al._2025_OctoNav Towards Generalist Embodied Navigation.pdf"
---

# OctoNav: Towards Generalist Embodied Navigation

> **저자**: Chen Gao, Liankai Jin, Xingyu Peng, Jiazhao Zhang, Yue Deng, Annan Li, He Wang, Si Liu | **날짜**: 2025-06-11 | **URL**: [https://arxiv.org/abs/2506.09839](https://arxiv.org/abs/2506.09839)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: On the left, we present the large-scale OctoNav-Bench, which contains diverse instruction-*

자유형식의 멀티모달 멀티기능 지시를 따를 수 있는 일반화된 embodied navigation 에이전트를 위해 OctoNav-Bench 벤치마크와 OctoNav-R1 방법을 제안한다. Think-Before-Action 추론을 통해 복잡한 네비게이션 작업에서 향상된 성능을 달성한다.

## Motivation

- **Known**: 기존 embodied navigation 연구는 ObjNav, ImgNav, VLN 등 개별 작업으로 분리되어 있으며, 각각 별도의 데이터셋과 방법이 설계되어 있다. 최근 일반화된 navigation 에이전트 구축을 시도하는 작업들이 있지만 여전한 한계가 있다.
- **Gap**: 기존 벤치마크와 방법들은 단일 기능 또는 단일 모달리티만 포함하며 자유형식의 멀티모달 멀티기능 지시를 동시에 처리할 수 없다. 또한 일반화된 reasoning 능력을 갖춘 navigation 에이전트 개발이 부족하다.
- **Why**: 일반화된 navigation 에이전트는 실제 로봇 애플리케이션에서 다양한 작업을 유연하게 처리할 수 있어야 하며, 이는 embodied AI의 핵심 기능이다. Think-before-action을 통한 reasoning은 복잡한 지시 이해도를 향상시킬 수 있다.
- **Approach**: 400+개 장면과 45k+개 자동 생성된 지시-궤적 쌍, 그리고 TBA-CoT 데이터셋을 포함하는 대규모 OctoNav-Bench를 구축한다. MLLM 기반의 VLA 모델인 OctoNav-R1을 Action-/TBA-SFT, Nav-GRPO, Online RL 세 단계의 Hybrid Training Paradigm으로 학습한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: On the left, we present the large-scale OctoNav-Bench, which contains diverse instruction-*

- **OctoNav-Bench 벤치마크**: 400+개 연속 환경의 3D 장면에서 45k+개의 자유형식 멀티모달 멀티기능 지시-궤적 쌍과 10k+개의 TBA-CoT 데이터셋을 제공하는 대규모 통합 벤치마크 구축
- **OctoNav-R1 모델**: 자유형식 멀티모달 멀티기능 지시를 따르고 2D 시각 관찰로부터 저수준 행동을 직접 생성하는 VLA 기반 navigation 에이전트 개발
- **Hybrid Training Paradigm**: Action-/TBA-SFT, Nav-GRPO, Online RL을 통합하여 명시적 thinking 프로세스를 가진 모델 학습 방법 제안
- **성능 향상**: ObjNav, PointNav, ImgNav, Ins-ImgNav, VLN 모든 기능에서 기존 방법(NaVid, Uni-NaVid, NavGPT-2 등)을 초과하는 성능 달성
- **Sim2Real 일반화**: 실제 로봇 배포에서 실제 환경 미세조정 없이 초기 sim-to-real 전이 능력 입증

## How

![Figure 4](figures/fig4.webp)

*Figure 4: Overview of the HTP for training OctoNav-R1. The model takes multi-model instruction*

- 자동 annotation 파이프라인을 통해 HM3D, MP3D, Gibson, ProcTHOR 등 다양한 환경에서 자유형식 지시-궤적 쌍 생성
- Qwen-VL과 DeepSeek-R1을 활용하여 각 행동 뒤의 reasoning 과정을 포함하는 TBA-CoT 데이터셋 구축
- MLLM을 VLA 모델로 변환하여 egocentric 시각 관찰로부터 저수준 행동(move forward, turn left/right 등)을 직접 예측
- Action-SFT/TBA-SFT 단계에서 지도학습으로 cold-start 초기화
- Nav-GRPO 단계에서 group relative policy optimization을 사용하여 thinking 능력 개선
- Online RL 단계에서 환경 상호작용을 통한 추가 학습으로 성능 최적화

## Originality

- 기존 개별 navigation 작업들을 통합하여 자유형식 멀티모달 멀티기능 지시 처리가 가능한 첫 번째 통합 벤치마크와 방법 제시
- Think-Before-Action (TBA-CoT)이라는 새로운 개념으로 navigation에서 명시적 reasoning 프로세스 도입 (DeepSeek-R1의 thinking-before-answer 영감)
- VLA 모델에 RL을 통합하는 Hybrid Training Paradigm으로 기존 SFT 기반 VLA 학습 방식의 한계 극복
- continuous 환경 설정으로 그래프 기반 네비게이션의 제약 극복하고 실제 로봇 배포 가능성 증대

## Limitation & Further Study

- 현재 sim2real 성능은 '초기(preliminary)' 수준이므로 실제 환경에서의 안정적 성능 검증 필요", 'TBA-CoT 데이터 생성에 LLM(Qwen-VL, DeepSeek-R1) 의존으로 인한 annotation 품질의 일관성 문제 가능성
- 자유형식 지시의 다양성이 충분한지, 그리고 학습된 패턴이 정말 일반화되는지에 대한 더 깊은 분석 필요
- 다양한 환경과 실제 실내/실외 환경에서의 성능 평가 부재
- 후속 연구: (1) 더 다양한 실제 환경에서의 시뮬레이션 및 로봇 배포 확대, (2) TBA-CoT 데이터셋의 자동 품질 검증 메커니즘 개발, (3) 다양한 robot embodiment으로의 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 fragmented된 embodied navigation 작업들을 통합하는 포괄적인 벤치마크와 방법을 처음 제시하며, Think-Before-Action을 통한 명시적 reasoning 도입으로 일반화된 navigation 에이전트 개발에 중요한 기여를 한다. 초기 sim2real 결과는 실용적 가능성을 시사하지만, 추가 실제 환경 검증이 필요하다.

## Related Papers

- 🔗 후속 연구: [[papers/1463_LOVON_Legged_Open-Vocabulary_Object_Navigator/review]] — OctoNav의 일반화된 네비게이션이 LOVON의 다리 로봇 개방형 어휘 객체 네비게이션과 결합되어 더 복잡한 지형에서의 네비게이션을 실현한다.
- 🔄 다른 접근: [[papers/1600_UniGoal_Towards_Universal_Zero-shot_Goal-oriented_Navigation/review]] — 둘 다 목표 지향 네비게이션에 초점을 맞추지만, OctoNav는 멀티모달 지시를, UniGoal은 제로샷 범용성에 집중한다.
- 🏛 기반 연구: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — OctoNav의 Think-Before-Action 추론이 Reflective Planning의 단계별 시각-언어 계획 수립 방법론과 유사한 철학적 기반을 공유한다.
- 🔄 다른 접근: [[papers/1342_CorrectNav_Self-Correction_Flywheel_Empowers_Vision-Language/review]] — 두 논문 모두 vision-language 네비게이션에서 자기교정 메커니즘을 활용하지만 적용 도메인이 다르다.
- 🏛 기반 연구: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — Vision-Language Navigation 분야의 전반적 동향을 이해하는 데 필요한 기초 서베이이다.
- 🔗 후속 연구: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — Voyager의 open-ended 탐색 개념을 구체적인 네비게이션 작업으로 특화하여 발전시킨다.
- 🏛 기반 연구: [[papers/1383_EmbSpatial-Bench_Benchmarking_Spatial_Understanding_for_Embo/review]] — OctoNav의 spatial understanding 능력을 평가하기 위한 embodied navigation benchmark와 평가 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1311_ApexNav_An_Adaptive_Exploration_Strategy_for_Zero-Shot_Objec/review]] — OctoNav의 Think-Before-Action과 달리 adaptive exploration strategy를 통한 zero-shot object navigation 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1563_Scaling_Instructable_Agents_Across_Many_Simulated_Worlds/review]] — OctoNav의 generalist navigation을 다양한 시뮬레이션 환경에서 확장하여 instructable agents로 발전시킬 수 있다.
- 🔗 후속 연구: [[papers/1378_Embodied_Navigation_Foundation_Model/review]] — OctoNav의 generalist navigation을 더 크고 포괄적인 cross-embodiment foundation model로 확장 발전
- 🔗 후속 연구: [[papers/1303_Advances_in_Embodied_Navigation_Using_Large_Language_Models/review]] — 범용적 embodied navigation으로 LLM 기반 네비게이션을 확장한다.
- 🔗 후속 연구: [[papers/1311_ApexNav_An_Adaptive_Exploration_Strategy_for_Zero-Shot_Objec/review]] — ApexNav의 적응적 탐색 전략은 OctoNav의 일반화된 embodied navigation 프레임워크에서 활용될 수 있는 핵심 기술입니다.
