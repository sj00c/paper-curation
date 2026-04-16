---
title: "1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L"
authors:
  - "Yunhai Feng"
  - "Jiaming Han"
  - "Zhuoran Yang"
  - "Xiangyu Yue"
  - "Sergey Levine"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-language models (VLMs)의 장기 지평 로봇 조작 능력을 향상시키기 위해 reflection 메커니즘과 diffusion 기반 dynamics 모델을 결합한 test-time computation 프레임워크를 제안한다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robot_Policy_Learning"
  - "sub/Action-Value_Reasoning_Systems"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Feng et al._2025_Reflective Planning Vision-Language Models for Multi-Stage Long-Horizon Robotic Manipulation.pdf"
---

# Reflective Planning: Vision-Language Models for Multi-Stage Long-Horizon Robotic Manipulation

> **저자**: Yunhai Feng, Jiaming Han, Zhuoran Yang, Xiangyu Yue, Sergey Levine, Jianlan Luo | **날짜**: 2025-02-23 | **URL**: [https://arxiv.org/abs/2502.16707](https://arxiv.org/abs/2502.16707)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Reflective planning. Our method uses a VLM to propose*

Vision-language models (VLMs)의 장기 지평 로봇 조작 능력을 향상시키기 위해 reflection 메커니즘과 diffusion 기반 dynamics 모델을 결합한 test-time computation 프레임워크를 제안한다.

## Motivation

- **Known**: VLMs은 인터넷 규모의 시각-언어 이해 능력을 가지고 있지만, 복잡한 물리 추론과 장기 지평 계획에서는 여전히 제한적이다. 기존 robotic planning 방법들은 기호적 표현에 의존하거나 단일 단계 결정만 수행한다.
- **Gap**: VLMs은 정교한 물리 제약 이해와 오류 누적 문제를 다루는 장기 지평 추론 능력이 부족하다. 또한 미래 상태 예측을 통한 행동 검증 메커니즘이 없어 suboptimal한 결정을 하기 쉽다.
- **Why**: 다단계 로봇 조작 작업은 물리 제약을 정확히 이해하고 장기 지평에서 오류 누적을 처리해야 하는 현실적이고 중요한 문제이며, VLMs의 기존 한계를 해결하면 로봇 자동화의 폭넓은 적용이 가능해진다.
- **Approach**: Diffusion 기반 dynamics 모델로 미래 상태를 시각적으로 예측하고, VLM이 이 예측을 바탕으로 자신의 행동 계획을 비판적으로 검토하고 개선하는 reflection 메커니즘을 도입한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4. Filmstrip of our method solving a complicated assembly task. Frames are indexed by timestep. The goal image is*

- **성능 우위**: 최신 상용 VLM 모델들과 Monte Carlo Tree Search(MCTS)를 포함한 기존 post-training 방법들을 유의미하게 능가한다.
- **효율성**: 감독된 fine-tuning(SFT)과 동일한 양의 학습 데이터를 사용하면서도 우수한 성능을 유지하고 계산 효율성을 확보한다.
- **일반화 가능성**: 조작 작업을 넘어 시각 이해와 순차적 의사결정이 필요한 다른 도메인으로 확장 가능한 일반적 프레임워크를 제시한다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Training data generation. Training data for the reflection mechanism is collected by relabeling the rollouts. *

- 현재 이미지와 목표 이미지를 입력받아 VLM이 초기 행동을 제안한다.
- Diffusion dynamics 모델을 사용하여 제안된 행동들의 미래 H-step 상태를 시각적으로 생성한다.
- VLM이 상상된 미래 상태를 분석하여 초기 계획의 suboptimality를 비판적으로 평가한다.
- Reflection 과정을 통해 더 나은 행동을 제안하도록 VLM을 유도한다.
- Training 데이터는 expert 정책의 rollout에서 (Q1, A1) 행동 제안과 (Q2, A2) reflection 두 가지 예제 쌍으로 재레이블링된다.
- Test-time에 diffusion 모델과 reflection 메커니즘을 반복적으로 적용하여 성능을 향상시킨다.

## Originality

- **Visual imagination + Reflection 결합**: 단순 future state 예측을 넘어 VLM이 예측된 미래를 기반으로 자신의 계획을 비판적으로 검토하는 reflection 메커니즘은 로봇 계획 분야에서 새로운 접근법이다.
- **Test-time computation 강조**: 사전학습된 VLM의 재훈련 없이 test-time에 구조화된 추론 메커니즘을 추가하여 성능을 크게 향상시키는 패러다임을 제시한다.
- **장기 물리 추론 개선**: Diffusion 모델의 시각적 예측과 VLM의 reflection을 결합하여 장기 지평에서의 물리 기반 추론 능력을 직접적으로 증강한다.
- **일반적 프레임워크**: 조작 작업에 특화되지 않고 다양한 시각-언어 기반 순차 의사결정 문제로 확장 가능한 구조를 설계한다.

## Limitation & Further Study

- **Diffusion 모델의 예측 오류**: 장기 지평에서 diffusion 기반 dynamics 모델의 누적된 예측 오류가 reflection의 효과를 제한할 수 있다.
- **계산 비용**: 매 단계마다 diffusion 모델의 여러 샘플 생성과 VLM의 다중 추론이 필요하여 실시간 로봇 제어에는 제약이 있을 수 있다.
- **학습 데이터 의존성**: Reflection 메커니즘의 효과는 고품질 expert 정책 데이터에 의존하며, 데이터 부족 환경에서의 성능 저하 가능성이 있다.
- **특정 도메인 평가**: 현재 실험은 조작 작업 내 특정 유형의 문제(interlocking objects)에 집중되어 있으며, 더 다양한 로봇 작업에 대한 평가가 필요하다.
- **후속 연구**: (1) 예측 오류 축적을 완화하기 위한 더 강력한 dynamics 모델 개발, (2) Test-time 계산 비용 감소 방안, (3) 더 다양한 로봇 도메인으로의 일반화 검증이 필요하다.

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VLMs의 물리 추론 능력을 reflection 메커니즘과 visual prediction을 통해 우아하게 향상시키는 방법론을 제시하며, test-time computation으로 재훈련 없이 성능을 크게 개선하는 실질적 기여를 한다. 로봇 조작 분야의 중요한 진전이나, 계산 효율성과 실제 로봇 시스템으로의 적용 가능성에 대한 추가 검증이 필요하다.

## Related Papers

- 🔗 후속 연구: [[papers/1538_RoboCerebra_A_Large-scale_Benchmark_for_Long-horizon_Robotic/review]] — large-scale benchmark에서 평가되는 장기 지평선 조작을 reflective planning과 dynamics model을 통해 실제로 해결하는 구체적인 방법론을 제시한다.
- 🔄 다른 접근: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — VLM의 장기 지평선 능력 향상에서 reflection mechanism vs reinforced visual reasoning이라는 서로 다른 test-time computation 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — rational VLA model의 이론적 기반을 제공하여 reflective planning에서 사용되는 VLM의 추론 능력과 dynamics model 통합에 필요한 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — 장기 지평 로봇 조작에서 reflection 메커니즘과 chain-of-thought 추론이라는 서로 다른 계획 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — Inner Monologue의 언어 기반 계획이 reflection 메커니즘과 결합되어 더욱 정교한 다단계 장기 계획을 수립할 수 있다.
- 🔄 다른 접근: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — 두 논문 모두 VLM의 장기 계획 능력을 다루지만 reflection과 상태 유지의 접근법이 다르다.
- 🏛 기반 연구: [[papers/1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI/review]] — World model 기반 embodied AI의 전반적 이해가 reflective planning 연구의 기초가 된다.
- 🏛 기반 연구: [[papers/1497_OctoNav_Towards_Generalist_Embodied_Navigation/review]] — OctoNav의 Think-Before-Action 추론이 Reflective Planning의 단계별 시각-언어 계획 수립 방법론과 유사한 철학적 기반을 공유한다.
- 🔄 다른 접근: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — 장기 계획 수립에서 embodied chain-of-thought는 다단계 추론을, reflection 메커니즘은 반성적 계획을 통해 문제를 해결한다.
- 🔄 다른 접근: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — Reflective Planning은 Statler의 상태 기반 추론을 다단계 계획에 적용하는 유사한 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1604_Video_Language_Planning/review]] — multi-stage 계획을 위한 서로 다른 접근법 - video planning vs reflective planning입니다.
- 🔗 후속 연구: [[papers/1341_CoPAL_Corrective_Planning_of_Robot_Actions_with_Large_Langua/review]] — 멀티스테이지 반성적 계획으로 CoPAL의 계층적 계획을 확장한다.
- 🏛 기반 연구: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — Reflective Planning의 multi-stage 추론 개념이 CoT-VLA의 시각적 chain-of-thought 구조의 기초가 됩니다.
- 🔄 다른 접근: [[papers/1379_Embodied-R_Collaborative_Framework_for_Activating_Embodied_S/review]] — Reflective Planning의 multi-stage task planning과 Embodied-R의 collaborative VLM-LM framework는 embodied reasoning에서 서로 다른 계획 수립 접근법이다.
