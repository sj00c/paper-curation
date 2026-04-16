---
title: "1379_Embodied-R_Collaborative_Framework_for_Activating_Embodied_S"
authors:
  - "Baining Zhao"
  - "Ziyou Wang"
  - "Jianjie Fang"
  - "Chen Gao"
  - "Fanhang Man"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "Embodied-R은 대규모 Vision-Language Model(VLM)과 소규모 Language Model(LM)을 협력시키고 RL을 통해 embodied video에서의 spatial reasoning 능력을 활성화하는 프레임워크이다. 단 5k개의 embodied video 샘플로 훈련하여 OpenAI-o1, Gemini-2.5-pro 수준의 성능을 달성한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhao et al._2025_Embodied-R Collaborative Framework for Activating Embodied Spatial Reasoning in Foundation Models v.pdf"
---

# Embodied-R: Collaborative Framework for Activating Embodied Spatial Reasoning in Foundation Models via Reinforcement Learning

> **저자**: Baining Zhao, Ziyou Wang, Jianjie Fang, Chen Gao, Fanhang Man, Jinqiang Cui, Xin Wang, Xinlei Chen, Yong Li, Wenwu Zhu | **날짜**: 2025-04-17 | **URL**: [https://arxiv.org/abs/2504.12680](https://arxiv.org/abs/2504.12680)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: The proposed Embodied-R is a collaborative embodied spatial reasoning framework integrating a Vision-Language*

Embodied-R은 대규모 Vision-Language Model(VLM)과 소규모 Language Model(LM)을 협력시키고 RL을 통해 embodied video에서의 spatial reasoning 능력을 활성화하는 프레임워크이다. 단 5k개의 embodied video 샘플로 훈련하여 OpenAI-o1, Gemini-2.5-pro 수준의 성능을 달성한다.

## Motivation

- **Known**: VLM의 perception 능력은 이미 충분히 검증되었으나, embodied spatial reasoning 능력은 여전히 제한적이다. 최근 o1/o3, DeepSeek-R1 등이 RL과 chain-of-thought를 통해 complex reasoning 문제에서 우수한 성능을 보였다.
- **Gap**: video 기반 spatial reasoning은 지각-추론의 상호작용, 시공간적 복잡성, embodied input의 특수성 등으로 인해 기존 SFT 방식으로는 충분한 supervision이 불가능하다. 또한 대규모 모델의 perception 능력을 활용하면서도 계산 비용을 낮추는 방법이 부재한다.
- **Why**: embodied AI가 AGI 달성을 위한 핵심 요소이며, spatial reasoning 능력은 navigation, planning, manipulation 등 실제 3D 환경에서의 에이전트 행동에 필수적이다.
- **Approach**: 신경과학에서 영감을 얻아 perception과 reasoning을 분리한 협력 프레임워크를 제안하고, keyframe extraction으로 computational cost를 줄인다. 논리적 일관성을 고려하는 novel reward system을 가진 RL을 사용하여 slow-thinking 능력을 학습시킨다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Case Analysis: Embodied-R has initially developed the ability for slow-thinking: it can think before answering*

- **성능 달성**: 3B LM을 사용한 Embodied-R이 5k 샘플 훈련으로 OpenAI-o1, Gemini-2.5-pro와 동등한 수준의 in-distribution, out-of-distribution embodied spatial reasoning 성능 달성
- **Emergent thinking**: 체계적 분석(systematic analysis)과 문맥 통합(contextual integration) 등의 slow-thinking 패턴 자동 발현
- **효율적 설계**: 대규모 VLM의 perception 능력을 활용하면서 소규모 LM의 reasoning만 RL로 훈련하여 computational cost 최소화
- **Novel reward design**: think-answer 논리적 일관성을 고려한 reward로 reasoning process와 최종 답변의 정렬 향상

## How

![Figure 2](figures/fig2.webp)

*Figure 2: The proposed Embodied-R is a collaborative embodied spatial reasoning framework integrating a Vision-Language*

- **Keyframe extraction**: video의 시간적 연속성을 활용하여 중요 프레임만 추출하고 VLM의 입력 토큰 길이 관리
- **Sequential perception**: VLM으로 keyframe들로부터 순차적으로 semantic information 추출하여 online reasoning 시뮬레이션
- **Collaborative architecture**: 대규모 VLM이 perception 담당, 소규모 LM이 reasoning 담당으로 역할 분리
- **RL training with novel rewards**: rule-based rewards (from DeepSeek-R1-Zero)와 logical consistency rewards의 결합으로 GRPO 훈련
- **Reasoning prompt design**: reasoning question과 semantic information을 소규모 LM에 입력하여 reasoning process와 답변 생성

## Originality

- embodied spatial reasoning에 RL을 처음 적용한 연구로, think-answer logical consistency라는 novel reward 개념 도입
- 대규모와 소규모 모델의 협력을 통해 perception과 reasoning을 명확히 분리한 프레임워크는 신경과학 기반의 창의적 설계
- embodied video의 특수성(egocentric perspective, temporal continuity, spatial redundancy)을 고려한 keyframe extraction 및 sequential processing 방식의 고안
- SFT와 RL 훈련의 generalization 차이를 체계적으로 분석한 thorough empirical investigation

## Limitation & Further Study

- 소규모 LM의 추론 능력은 여전히 학습된 reward signal에 의존하므로, 새로운 reasoning task에 대한 zero-shot generalization은 제한적일 수 있음
- 5k embodied video 샘플이라는 제한적 데이터로 훈련했으므로, 더 diverse한 embodied scenario에서의 일반화 능력 검증 필요
- keyframe extraction 방식이 heuristic 기반인데, learned keyframe selection 메커니즘으로의 개선 가능성
- VLM의 hallucination 문제가 perception 단계에서 직접 reasoning에 영향을 미치는 error propagation 문제는 충분히 다루어지지 않음
- 후속연구로 larger-scale embodied video dataset 확보, 다양한 embodied reasoning task로의 확장, 더 효율적인 video encoding 방식 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: embodied spatial reasoning에 RL을 처음 적용하고 대규모-소규모 모델의 협력이라는 창의적 설계로 competitive한 성능을 달성한 중요한 연구이다. 다만 reward design의 일반성과 새로운 task에 대한 generalization 능력 검증이 향후 과제이다.

## Related Papers

- 🔄 다른 접근: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — Reflective Planning의 multi-stage task planning과 Embodied-R의 collaborative VLM-LM framework는 embodied reasoning에서 서로 다른 계획 수립 접근법이다.
- 🔗 후속 연구: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — Inner Monologue의 embodied reasoning through planning이 Embodied-R에서 VLM과 LM의 협력을 통한 spatial reasoning으로 더욱 발전했다.
- 🏛 기반 연구: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — Statler의 state-maintaining language model이 Embodied-R의 대규모 VLM과 소규모 LM 협력 구조에서 상태 유지 메커니즘의 기초를 제공한다.
- 🔄 다른 접근: [[papers/1536_RoboBrain_A_Unified_Brain_Model_for_Robotic_Manipulation_fro/review]] — Embodied-R과 동일하게 통합된 embodied reasoning을 추구하지만 RoboBrain은 조작에 특화되고 ShareRobot 데이터셋을 활용한다.
