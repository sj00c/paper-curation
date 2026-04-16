---
title: "1503_OneTwoVLA_A_Unified_Vision-Language-Action_Model_with_Adapti"
authors:
  - "Fanqi Lin"
  - "Ruiqian Nai"
  - "Yingdong Hu"
  - "Jiacheng You"
  - "Junming Zhao"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "OneTwoVLA는 단일 통합 vision-language-action 모델로서 reasoning과 acting을 모두 수행하며, 작업 실행 중 critical moment에서는 explicit reasoning을, 그 외에는 reasoning 기반 action generation으로 adaptively switch한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lin et al._2025_OneTwoVLA A Unified Vision-Language-Action Model with Adaptive Reasoning.pdf"
---

# OneTwoVLA: A Unified Vision-Language-Action Model with Adaptive Reasoning

> **저자**: Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, Yang Gao | **날짜**: 2025-05-17 | **URL**: [https://arxiv.org/abs/2505.11917](https://arxiv.org/abs/2505.11917)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview. OneTwoVLA is a single unified vision-language-action model capable of both reasoning*

OneTwoVLA는 단일 통합 vision-language-action 모델로서 reasoning과 acting을 모두 수행하며, 작업 실행 중 critical moment에서는 explicit reasoning을, 그 외에는 reasoning 기반 action generation으로 adaptively switch한다.

## Motivation

- **Known**: 최근 dual-system 접근법은 VLM을 System Two(high-level reasoning)로, VLA를 System One(low-level acting)으로 분리하여 사용한다. 하지만 두 시스템 간 상호 이해 부족과 latency 문제가 존재한다.
- **Gap**: 기존 dual-system 방식은 두 시스템이 각각의 capabilities를 인식하지 못하고, System Two의 지연 응답으로 인해 outdated guidance를 제공할 수 있다. 또한 일부 unified model은 reasoning을 효율적으로 수행하지 못하거나 reasoning 없이 작동하여 성능이 저하된다.
- **Why**: 로봇이 long-horizon task planning, error detection and recovery, natural human-robot interaction을 수행하려면 reasoning과 acting의 synergistic 관계가 필수적이며, 단일 통합 모델이 이를 효과적으로 구현할 수 있다.
- **Approach**: OneTwoVLA는 decision token([BOR]/[BOA])을 통해 reasoning vs acting을 adaptive하게 결정하는 unified model을 제안한다. 또한 embodied reasoning-centric vision-language data 합성 pipeline을 설계하여 robot data와 co-training한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Task completion times on Tomato-Egg.*

- **Long-horizon task planning**: flat VLA 대비 30%, dual-system VLA 대비 24% 성능 향상을 달성하며, novel task instruction에 대한 generalization 가능
- **Error detection and recovery**: real-time 오류 감지 및 correction strategy 추론으로 agile recovery action 수행
- **Natural human-robot interaction**: human intervention 즉시 반응 및 ambiguity 상황에서 proactive clarification 추구
- **Generalizable visual grounding**: spatial relationships, object attributes, semantic features에 대한 superior understanding으로 robot training data 외 object로도 generalization

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Inference flow of OneTwoVLA in two modes.*

- Unified model πθ가 two modes로 작동: reasoning mode (I1:n_t, I1:n_ref, ℓ, R을 입력으로 textual reasoning ˆR 생성), acting mode (추가로 st를 입력으로 action chunk At 생성)
- Algorithm 1의 inference pipeline: decide() → [BOR]이면 reason() 호출하여 R 업데이트, [BOA]이면 act() 호출하여 action 실행
- Robot data curation: task demonstrations에 scene description, subtask planning, error description, action guidance 등의 reasoning content 포함
- Vision-language data synthesis pipeline: embodied reasoning을 포함한 high-quality VL data 대규모 생성으로 robot data와 co-training
- Reference images I1:n_ref 활용으로 observation history 확보하여 ambiguous state 방지

## Originality

- Dual-system framework의 근본적 한계를 identified하고, unified model을 통한 seamless reasoning-acting synergy 달성
- Adaptive decision mechanism ([BOR]/[BOA] tokens)으로 reasoning efficiency와 execution efficiency의 balance 제시
- Embodied reasoning-centric vision-language data synthesis pipeline을 통한 scalable co-training 방식 제안
- Reference image 메커니즘으로 observation history를 명시적으로 활용하는 novel approach

## Limitation & Further Study

- Reasoning content의 구체적 format (scene description, plan, historical summary, next-step instruction)이 고정적으로 설계됨에 따른 flexibility 제약 가능성
- Vision-language data 합성 quality가 co-training 효과에 크게 의존하는데, data 품질 보증 mechanism 상세 기술 부족
- 실제 robot hardware에서의 deployment 결과 제시 부족 (주로 simulation 기반 평가로 보임)
- Reasoning token 수 증가에 따른 inference latency 증가에 대한 분석 및 최적화 전략 제시 필요
- Human-robot interaction 평가가 qualitative example 위주로 보이며, quantitative metrics 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: OneTwoVLA는 dual-system의 근본적 문제를 unified model로 해결하면서 adaptive reasoning-acting mechanism을 통해 효율성과 성능의 balance를 달성한 혁신적 접근법이다. Embodied vision-language co-training strategy와 함께 long-horizon robot control의 새로운 표준을 제시하며, ICLR 2026 발표의 significance를 충분히 입증한다.

## Related Papers

- 🔄 다른 접근: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — VLA 모델에서 adaptive reasoning-action switching vs reinforced visual reasoning이라는 서로 다른 추론-행동 통합 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action/review]] — System-2 thinking을 adaptive reasoning과 결합하여 상황에 따라 추론 깊이를 조절하는 더 효율적인 VLA 시스템을 구축한다.
- 🏛 기반 연구: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — visual chain-of-thought reasoning의 기본 이론을 제공하여 OneTwoVLA의 adaptive reasoning 메커니즘 설계에 필요한 방법론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1509_OpenHelix_A_Short_Survey_Empirical_Analysis_and_Open-Source/review]] — OneTwoVLA의 adaptive reasoning 접근법과 OpenHelix의 dual-system 아키텍처는 reasoning과 acting을 분리하는 다른 전략을 제시한다.
- ⚖️ 반론/비판: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — unified VLA vs triple-system 기반의 다른 시스템 통합 철학
- 🏛 기반 연구: [[papers/1616_VLA-Adapter_An_Effective_Paradigm_for_Tiny-Scale_Vision-Lang/review]] — OneTwoVLA의 적응형 아키텍처 설계가 VLA-Adapter의 Bridge Attention 기반 연결 방법론의 이론적 기반을 제공한다.
