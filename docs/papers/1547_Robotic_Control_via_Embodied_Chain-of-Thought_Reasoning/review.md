---
title: "1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning"
authors:
  - "Michał Zawalski"
  - "William Chen"
  - "Karl Pertsch"
  - "Oier Mees"
  - "Chelsea Finn"
date: "2024.07"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-language-action (VLA) 모델에 embodied chain-of-thought 추론을 도입하여 로봇 정책이 행동 예측 전에 계획, 부작업, 움직임, 시각적 특징에 대해 다단계 추론을 수행하도록 훈련시킨다. 합성 데이터 생성 파이프라인을 통해 OpenVLA의 절대 성공률을 28% 향상시켰다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zawalski et al._2024_Robotic Control via Embodied Chain-of-Thought Reasoning.pdf"
---

# Robotic Control via Embodied Chain-of-Thought Reasoning

> **저자**: Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, Sergey Levine | **날짜**: 2024-07-11 | **URL**: [https://arxiv.org/abs/2407.08693](https://arxiv.org/abs/2407.08693)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1:*

Vision-language-action (VLA) 모델에 embodied chain-of-thought 추론을 도입하여 로봇 정책이 행동 예측 전에 계획, 부작업, 움직임, 시각적 특징에 대해 다단계 추론을 수행하도록 훈련시킨다. 합성 데이터 생성 파이프라인을 통해 OpenVLA의 절대 성공률을 28% 향상시켰다.

## Motivation

- **Known**: VLA는 인터넷 사전학습 vision-language 모델을 기반으로 로봇 정책의 견고성과 일반화 능력을 개선했다. 언어 모델에서 chain-of-thought 추론은 복잡한 문제 해결 성능을 크게 향상시킨다.
- **Gap**: 표준 VLA에 단순히 CoT 프롬핑을 적용하면 훈련 예제가 단순해서 효과적이지 않고, 의미론적 추론만으로는 감각 관찰과 로봇 상태에 근거해야 하는 로봇 정책에 불충분하다.
- **Why**: 로봇이 새로운 상황에서 단순 반응 제어가 아닌 신중한 추론을 통해 일반화 능력을 높일 수 있으며, 해석 가능성과 자연언어를 통한 정정도 가능해진다.
- **Approach**: Embodied Chain-of-Thought (ECoT)는 VLA가 객체 경계상자, 엔드이펙터 위치 등 시각적으로 근거된 특징과 부작업 계획을 통합하여 다단계 추론을 수행하도록 훈련한다. 대규모 로봇 데이터셋에서 합성 훈련 데이터를 생성하는 확장 가능한 파이프라인을 설계했다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5: Qualitative ECoT predictions from our model for two successful trajectories (left, middle) and*

- **성능 향상**: 추가 로봇 훈련 데이터 없이 OpenVLA의 절대 성공률을 28% 증가시켰으며, 새로운 객체, 장면, 시점, 지시사항에 대한 일반화 작업에서 입증됨
- **해석 가능성 및 상호작용성**: 정책 실패가 더 해석 가능해지고 인간이 자연언어 피드백을 통해 추론 체인을 수정하여 행동을 대화형으로 정정할 수 있음
- **전이 학습**: 모델이 보이지 않은 구체화(embodiments)와 작업에 ECoT 추론을 전이하는 능력을 학습함

## How

![Figure 4](figures/fig4.webp)

*Figure 4: Our pipeline for generating synthetic embodied chain-of-thought data at scale for a given robot*

- Pre-trained open-vocabulary object detector를 사용하여 객체 경계상자 추론 생성
- 대규모 언어 모델(LLM)을 활용하여 작업 계획과 부작업 추론 자동 생성
- VLA를 자동회귀 모델로 훈련하여 지시사항과 관찰값으로부터 CoT와 액션을 순차적으로 생성
- 의미론적 추론(부작업 계획, 다음 작업)과 구체화된 추론(객체 경계상자, 그리퍼 위치, 움직임 원시형)을 interleave
- 합성 데이터 생성 파이프라인으로 기존 로봇 데이터셋으로부터 감독 신호 자동 생성

## Originality

- 로봇 제어에 맞게 CoT를 구체화(embodied)하여 순수 의미론적 추론만이 아닌 시각적, 공간적 추론을 통합한 새로운 접근
- VLA 정책이 고수준 계획과 저수준 제어 모두에서 추론하도록 훈련하는 최초의 체계적 방법
- 약한 오픈소스 LLM 백본에서도 효과적인 embodied 추론을 가능하게 하는 합성 데이터 생성 파이프라인

## Limitation & Further Study

- 합성 데이터 생성의 품질이 object detector와 LLM의 성능에 의존하므로, 이들 도구의 한계가 전파될 수 있음
- 실험이 주로 조작 작업에 국한되어 있으며 더 다양한 로봇 작업 유형에 대한 평가 필요
- 추론 단계 추가로 인한 계산 비용 및 실행 시간 증가에 대한 자세한 분석 부재
- 후속 연구로 ECoT가 다중 모달(multi-modal) 추론과 더 복잡한 장기 계획 시나리오에서 확장되어야 함

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 로봇 제어에 chain-of-thought 추론을 창의적으로 적용하면서 시각적 근거화를 통해 실제 로봇 정책의 일반화를 현저히 개선했다. 합성 데이터 생성 파이프라인과 함께 해석 가능성 향상은 실제 로봇 응용에 큰 가치를 제공한다.

## Related Papers

- 🔄 다른 접근: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — ThinkAct과 함께 VLA 모델의 추론 강화를 다루지만 이 연구는 embodied CoT에, ThinkAct은 강화 시각 추론에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 기본 VLA 구조를 확장하여 embodied chain-of-thought 추론 능력을 추가함으로써 성능을 크게 향상시켰다.
- 🔄 다른 접근: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — 장기 계획 수립에서 embodied chain-of-thought는 다단계 추론을, reflection 메커니즘은 반성적 계획을 통해 문제를 해결한다.
- 🏛 기반 연구: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — Inner Monologue의 언어 기반 추론 메커니즘이 embodied chain-of-thought의 다단계 추론 파이프라인 설계에 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — CoT-VLA가 시각적 chain-of-thought에 중점을 두는 반면, Embodied CoT는 행동 예측을 위한 전체적인 embodied reasoning 과정을 다룬다.
- 🔗 후속 연구: [[papers/1381_Embodied-Reasoner_Synergizing_Visual_Search_Reasoning_and_Ac/review]] — Chain-of-Thought Reasoning이 Embodied-Reasoner의 Observation-Thought-Action 궤적을 실제 로봇 제어로 확장합니다.
- 🔗 후속 연구: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — 내적 독백을 통한 추론을 embodied chain-of-thought로 더 체계화하고 발전시킨 접근법이다.
- 🔗 후속 연구: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — RationalVLA의 rational reasoning 능력이 embodied chain-of-thought 추론과 결합되면 더욱 강력한 로봇 의사결정 시스템을 구축할 수 있다.
- 🔄 다른 접근: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — 장기 지평 로봇 조작에서 reflection 메커니즘과 chain-of-thought 추론이라는 서로 다른 계획 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1585_ThinkBot_Embodied_Instruction_Following_with_Thought_Chain_R/review]] — 사고 체인 추론을 embodied chain-of-thought reasoning으로 확장한 발전된 형태입니다.
- 🔗 후속 연구: [[papers/1610_Visual_Embodied_Brain_Let_Multimodal_Large_Language_Models_S/review]] — embodied chain-of-thought reasoning을 MLLM 기반 지각-추론-제어 통합으로 확장하여 더 포괄적인 embodied reasoning을 제시합니다.
- 🏛 기반 연구: [[papers/1618_VLA-Reasoner_Empowering_Vision-Language-Action_Models_with_R/review]] — Embodied Chain-of-Thought가 VLA-Reasoner의 추론 기반 로봇 제어의 이론적 토대를 제공한다.
- 🏛 기반 연구: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — embodied chain-of-thought reasoning이 visual CoT의 로봇 적용을 위한 핵심 이론적 기반
