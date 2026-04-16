---
title: "1303_Advances_in_Embodied_Navigation_Using_Large_Language_Models"
authors:
  - "Jinzhou Lin"
  - "Han Gao"
  - "Xuxiang Feng"
  - "Rongtao Xu"
  - "Changwei Wang"
date: "2023.11"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 Large Language Models (LLMs)과 embodied intelligence의 융합에 초점을 맞춰 LLM 기반 navigation 모델들의 최신 동향을 종합적으로 조사하고, 기존 모델과 데이터셋의 장단점을 분석한 서베이이다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lin et al._2023_Advances in Embodied Navigation Using Large Language Models A Survey.pdf"
---

# Advances in Embodied Navigation Using Large Language Models: A Survey

> **저자**: Jinzhou Lin, Han Gao, Xuxiang Feng, Rongtao Xu, Changwei Wang, Man Zhang, Li Guo, Shibiao Xu | **날짜**: 2023-11-01 | **URL**: [https://arxiv.org/abs/2311.00530](https://arxiv.org/abs/2311.00530)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: This presentation exhibit a temporal map depicting the works of embodied navigation from 2022 to 2024, and we*

이 논문은 Large Language Models (LLMs)과 embodied intelligence의 융합에 초점을 맞춰 LLM 기반 navigation 모델들의 최신 동향을 종합적으로 조사하고, 기존 모델과 데이터셋의 장단점을 분석한 서베이이다.

## Motivation

- **Known**: LLM은 GPT 같은 Transformer 기반 모델로 자연어 처리에서 우수한 성능을 보였고, embodied intelligence는 센서 데이터를 통해 환경과 상호작용하는 지능형 에이전트를 연구해왔다.
- **Gap**: 기존 Vision-and-Language Navigation (VLN) 연구들이 주로 시각-언어 통합에 집중한 반면, LLM을 활용한 embodied navigation의 체계적인 분류와 비교 분석이 부족하며, multimodal 데이터 융합과 실시간 응답성 향상에 대한 연구가 제한적이다.
- **Why**: 자율주행과 로봇 작업 계획 분야에서 LLM 기반 navigation이 빠르게 발전하고 있으며, 환경 이해와 의사결정 지원에서 LLM의 잠재력이 크기 때문에 현황 파악과 향후 방향 제시가 중요하다.
- **Approach**: LLM이 embodied navigation에서 수행하는 두 가지 역할 - 'Grounded Language Understanding'을 통한 정보 추출과 'Few-Shot Planning'을 통한 직접 행동 생성 - 을 구분하여 분석하고, 주요 모델, 방법론, 데이터셋을 비교하였다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: The first type utilizes LLMs to analyze incoming visual or textual data to extract goal-relevant information, up*

- **종합적 리뷰**: LLM 기반 navigation 모델들의 체계적 분류와 비교분석을 통해 현재 연구 수준의 전체상을 제시
- **데이터셋 분석**: 주요 navigation 데이터셋의 적용성, 문제점, 한계를 상세히 분석하여 연구자들의 데이터셋 선택에 실질적 조언 제공
- **과제 및 방향 도출**: 실제 응용에서 직면한 도전과제(latency, multimodal fusion, spatial reasoning)를 식별하고 향후 연구 방향과 혁신적 응용 시나리오 제시

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: The first type utilizes LLMs to analyze incoming visual or textual data to extract goal-relevant information, up*

- LLM의 역할을 두 가지로 분류: semantic understanding (입력 데이터 분석으로 목표 관련 정보 추출)과 planning (직접 행동 생성)
- Transformer 아키텍처의 self-attention mechanism을 활용한 long-range dependency 처리
- Vision Transformers (ViT), CLIP, DALL-E 등 multimodal 모델을 활용한 visual-linguistic 통합
- Reinforcement learning을 활용한 고수준 제어와 저수준 제어 분리
- Point clouds, voice prompts 등 다양한 센서 데이터의 multimodal 통합
- Zero-shot learning과 few-shot planning 기법을 통한 최소 샘플 데이터로의 학습

## Originality

- LLM-based embodied navigation에 특화된 첫 번째 종합 서베이로, 기존 일반적인 vision-language navigation 리뷰와 차별화
- LLM의 역할을 'information-providing'과 'planning'으로 명확히 분류하여 개념적 틀 제시", '시간 변화에 따른 embodied navigation 발전 과정을 temporal map으로 시각화하고 5개 대표 모델의 프레임워크 비교

## Limitation & Further Study

- 논문이 2024년까지의 연구만 포함하여 그 이후 빠르게 진화하는 LLM 기술(GPT-4V, GPT-4o 등)의 최신 적용 사례 누락 가능성
- 실제 로봇 시스템 구현에서의 computational resource 제약과 latency 감소에 대한 구체적 솔루션 제시 부족
- Spatial reasoning과 데이터 다양성 문제에 대한 정량적 분석 및 벤치마킹 결과 부재
- Multimodal integration의 최적화 전략에 대한 이론적 또는 경험적 가이드라인 미흡
- 후속 연구로는 domain-specific LLM fine-tuning, edge computing 환경에서의 경량 모델 개발, 실시간 navigation을 위한 latency 최적화 기법이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 빠르게 성장하는 LLM 기반 embodied navigation 분야에 대한 첫 번째 체계적 서베이로서, 현재까지의 연구 성과를 명확히 분류하고 미래 방향을 제시하는 중요한 기여를 한다. 다만, 기술적 깊이와 실제 구현상의 도전과제에 대한 더욱 구체적인 분석이 보강된다면 실무자들에게 더욱 유용한 자료가 될 것이다.

## Related Papers

- 🏛 기반 연구: [[papers/1324_Bridging_Language_and_Action_A_Survey_of_Language-Conditione/review]] — language-conditioned manipulation 서베이가 LLM 기반 네비게이션 연구의 언어 처리 방법론적 기반을 제공
- 🔗 후속 연구: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — vision-language navigation의 전반적 조사를 LLM 특화 관점으로 심화 발전시킨 연구
- 🔗 후속 연구: [[papers/1497_OctoNav_Towards_Generalist_Embodied_Navigation/review]] — 범용적 embodied navigation으로 LLM 기반 네비게이션을 확장한다.
- 🔄 다른 접근: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — 비디오 기반 VLM을 활용한 다른 네비게이션 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1561_SayPlan_Grounding_Large_Language_Models_using_3D_Scene_Graph/review]] — 3D 장면 그래프를 활용한 LLM 기반 계획의 기초 방법론을 제공한다.
- 🧪 응용 사례: [[papers/1329_CityNavAgent_Aerial_Vision-and-Language_Navigation_with_Hier/review]] — CityNavAgent는 LLM 기반 네비게이션의 구체적 구현 사례로서 aerial domain에 특화된 응용입니다.
- 🔗 후속 연구: [[papers/1442_JARVIS-1_Open-World_Multi-task_Agents_with_Memory-Augmented/review]] — JARVIS-1은 LLM 기반 네비게이션을 메모리 증강과 멀티태스크로 확장한 발전된 형태입니다.
- 🧪 응용 사례: [[papers/1329_CityNavAgent_Aerial_Vision-and-Language_Navigation_with_Hier/review]] — LLM 기반 embodied navigation 서베이에서 제시된 방법론을 도시 aerial 환경이라는 특수한 도메인에 적용한 사례입니다.
- 🔗 후속 연구: [[papers/1324_Bridging_Language_and_Action_A_Survey_of_Language-Conditione/review]] — language-conditioned manipulation을 LLM 기반 navigation으로 확장하여 더 넓은 embodied AI 영역을 포괄
