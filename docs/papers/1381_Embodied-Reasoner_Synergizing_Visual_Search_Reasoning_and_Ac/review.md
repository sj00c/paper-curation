---
title: "1381_Embodied-Reasoner_Synergizing_Visual_Search_Reasoning_and_Ac"
authors:
  - "Wenqi Zhang"
  - "Mengna Wang"
  - "Gangao Liu"
  - "Xu Huixin"
  - "Yiwei Jiang"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "o1 스타일의 심층 추론 패러다임을 embodied 인터랙티브 작업으로 확장하여, 시각 탐색, 추론, 행동을 통합하는 Embodied-Reasoner 모델을 제시한다. 9.3k개의 Observation-Thought-Action 궤적과 3단계 학습 파이프라인을 통해 공간 이해, 시간 추론, 자기 반성 능력을 갖춘 모델을 개발했다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_Embodied-Reasoner Synergizing Visual Search, Reasoning, and Action for Embodied Interactive Tasks.pdf"
---

# Embodied-Reasoner: Synergizing Visual Search, Reasoning, and Action for Embodied Interactive Tasks

> **저자**: Wenqi Zhang, Mengna Wang, Gangao Liu, Xu Huixin, Yiwei Jiang, Yongliang Shen, Guiyang Hou, Zhe Zheng, Hang Zhang, Xin Li, Weiming Lu, Peng Li, Yueting Zhuang | **날짜**: 2025-03-27 | **URL**: [https://arxiv.org/abs/2503.21696](https://arxiv.org/abs/2503.21696)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1.*

o1 스타일의 심층 추론 패러다임을 embodied 인터랙티브 작업으로 확장하여, 시각 탐색, 추론, 행동을 통합하는 Embodied-Reasoner 모델을 제시한다. 9.3k개의 Observation-Thought-Action 궤적과 3단계 학습 파이프라인을 통해 공간 이해, 시간 추론, 자기 반성 능력을 갖춘 모델을 개발했다.

## Motivation

- **Known**: o1, Gemini 2.0 Flash Thinking, DeepSeek R1 등의 심층 추론 모델은 수학과 코딩 작업에서 뛰어난 성능을 보였다. 하지만 이들 모델의 embodied 도메인으로의 확장, 특히 장기 수평선 태스크에서의 효과는 거의 탐구되지 않았다.
- **Gap**: 기존 추론 모델들은 단일 턴 대화에 중점을 두고 있으며, 이미지-행동 인터리빙된 장기적 인터랙션 맥락에서 일관된 다양한 추론(분석, 공간 추론, 반성, 계획)을 생성하지 못한다. 또한 embodied 시나리오의 다양한 추론 양식(상식 추론, 공간 관계 이해, 시간 추론)을 체계적으로 다루지 않는다.
- **Why**: Embodied AI는 실제 환경과의 상호작용을 요구하는 실용적 응용(로봇, 에이전트)에 필수적이며, 심층 추론 능력의 이러한 영역으로의 확장은 장기 계획과 복잡한 작업 해결을 가능하게 한다.
- **Approach**: 9.3k개의 일관된 Observation-Thought-Action 궤적(64k개 인터랙티브 이미지, 90k개 다양한 사고 프로세스)을 합성하고, imitation learning, rejection sampling 기반 자기 탐색, reflection tuning을 포함한 3단계 학습 파이프라인을 제시한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2. Embodied-Reasoner exhibits spontaneous thinking behaviors, e.g., analyzing environmental states (#1,3), reflec*

- **성능 향상**: OpenAI o1, o3-mini, Claude-3.7을 각각 +9%, +24%, +13% 능가
- **논리적 일관성 개선**: 반복 검색과 논리적 불일치 감소 시연
- **장기 작업 강점**: 복잡한 long-horizon 작업에서 특히 뛰어난 성능
- **실제 환경 검증**: 실제 환경에서도 우수성 확인 및 효율적 탐색 행동 시연
- **다양한 사고 능력**: situation analysis, spatial reasoning, task planning, self-reflection, verification 등 5가지 사고 유형 통합

## How

![Figure 3](figures/fig3.webp)

*Figure 3. Left: Data Engine for <Instruction, Interactive Trajectory> synthesis. First, we synthesize instructions from *

- Data Engine을 통해 Observation-Thought-Action 궤적 자동 합성
- Imitation learning으로 기본 행동 학습
- Rejection sampling 기반 self-exploration으로 다양한 탐색 전략 습득
- Reflection tuning으로 자기 오류 수정 및 논리적 일관성 강화
- Image-text interleaved 형태로 시각 입력과 텍스트 사고를 교대로 처리
- 5가지 사고 양식(분석, 공간 추론, 반성, 계획, 검증)을 상황에 맞게 생성

## Originality

- Deep thinking 패러다임의 embodied 도메인 최초 체계적 확장
- Long-horizon interactive task를 위한 다양한 사고 양식(analysis, spatial reasoning, reflection, planning, verification) 통합
- Interactive trajectory 합성을 위한 자동화된 Data Engine 개발
- Rejection sampling과 reflection tuning의 조합을 통한 단계적 역량 강화 파이프라인
- Image-action interleaved context에서 일관된 다중모달 추론 능력 구현

## Limitation & Further Study

- 데이터셋 규모의 제한성(9.3k 궤적)으로 인한 일반화 능력의 불확실성
- 평가가 주로 object search 등 특정 유형의 embodied 작업에 집중되어 있으며, 다른 유형의 상호작용 작업으로의 확대 검증 부족
- 실제 환경 실험의 제한된 범위로 인한 실제 적용 가능성 미검증
- 계산 비용과 응답 시간에 대한 분석 부재
- 후속 연구로 더 복잡한 multi-agent embodied 작업, 지속적 학습 메커니즘, 다양한 환경과 작업 유형으로의 확장이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 심층 추론 모델을 embodied AI 영역으로 처음 체계적으로 확장하여 중요한 연구 공백을 채웠으며, 실험 결과 명확한 성능 향상을 보여준다. 다만 데이터셋 규모와 평가 범위 확대, 실제 환경에서의 추가 검증이 향후 연구에서 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action/review]] — 두 논문 모두 VLA 모델에 System-2 스타일의 심층 추론을 도입하여 복잡한 로봇 제어를 개선하는 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-2의 vision-language-action 아키텍처를 기반으로 한 embodied 추론 능력 확장 연구이다.
- 🔗 후속 연구: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — Inner Monologue의 언어 기반 추론을 embodied 환경에서 시각-행동과 통합한 발전된 형태이다.
- 🔗 후속 연구: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — Chain-of-Thought Reasoning이 Embodied-Reasoner의 Observation-Thought-Action 궤적을 실제 로봇 제어로 확장합니다.
- 🔄 다른 접근: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — Statler는 embodied reasoning을 위해 state-maintaining 접근법을 사용하여 Embodied-Reasoner와 다른 추론 전략을 제시합니다.
- 🔄 다른 접근: [[papers/1585_ThinkBot_Embodied_Instruction_Following_with_Thought_Chain_R/review]] — ThinkBot의 thought chain following과 Embodied-Reasoner의 o1-style deep reasoning은 embodied instruction following에서 서로 다른 추론 체계를 제시한다.
- 🏛 기반 연구: [[papers/1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action/review]] — Embodied-Reasoner의 심층 추론 패러다임을 VLA 모델에 System-2 thinking으로 구체화했다.
- 🔄 다른 접근: [[papers/1482_MP5_A_Multi-modal_Open-ended_Embodied_System_in_Minecraft_vi/review]] — embodied reasoning에서 active perception vs visual search and reasoning이라는 서로 다른 인지 메커니즘 접근법을 제시한다.
