---
title: "1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag"
authors:
  - "Qingqing Zhao"
  - "Yao Lu"
  - "Moo Jin Kim"
  - "Zipeng Fu"
  - "Zhuoyang Zhang"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 Vision-Language-Action(VLA) 모델에 시각적 chain-of-thought 추론을 도입하여, 로봇이 직접 행동을 생성하기 전에 미래의 부분 목표 이미지를 자동회귀적으로 생성하도록 함으로써 로봇 조작 성능을 향상시킨다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhao et al._2025_CoT-VLA Visual Chain-of-Thought Reasoning for Vision-Language-Action Models.pdf"
---

# CoT-VLA: Visual Chain-of-Thought Reasoning for Vision-Language-Action Models

> **저자**: Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, Ankur Handa, Ming-Yu Liu, Donglai Xiang, Gordon Wetzstein, Tsung-Yi Lin | **날짜**: 2025-03-27 | **URL**: [https://arxiv.org/abs/2503.22020](https://arxiv.org/abs/2503.22020)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of CoT-VLA framework. We build our model on VILA-U [67], a generative multimodal model pretrained on*

이 논문은 Vision-Language-Action(VLA) 모델에 시각적 chain-of-thought 추론을 도입하여, 로봇이 직접 행동을 생성하기 전에 미래의 부분 목표 이미지를 자동회귀적으로 생성하도록 함으로써 로봇 조작 성능을 향상시킨다.

## Motivation

- **Known**: VLA 모델은 사전 학습된 vision-language 모델을 활용하여 자연어 지시와 시각 관찰을 로봇 행동으로 매핑하며 뛰어난 일반화 성능을 보여주었다. 하지만 기존 VLA는 직접적인 입출력 매핑에만 집중하여 중간 추론 단계가 없다.
- **Gap**: 기존 VLA 모델들은 복잡한 조작 작업에 필수적인 중간 추론 단계가 부족하며, 시간적 계획 또는 추론 능력이 결여되어 있다. 또한 행동 주석이 없는 대규모 비디오 데이터를 활용하지 못하고 있다.
- **Why**: 시각적 chain-of-thought 추론을 통해 로봇이 행동 전에 '시각적으로 사고'하게 함으로써 복잡한 작업의 해석성과 성능을 동시에 개선할 수 있다. 또한 행동 주석이 없는 풍부한 비디오 데이터를 활용할 수 있게 된다.
- **Approach**: CoT-VLA는 VILA-U 기반 7B 모델로서, 현재 관찰과 언어 지시에서 부분 목표 이미지를 먼저 생성한 후, 그 이미지와 원래 관찰을 조건으로 하여 짧은 행동 수열을 생성한다. Hybrid attention 메커니즘을 사용하여 텍스트/이미지 생성에는 causal attention을, 행동 예측에는 full attention을 적용한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4. Franka-Tabletop comparisons. Evaluation across six distinct manipulation tasks, with separate models trained p*

- **실제 로봇 조작 성능**: 기존 state-of-the-art VLA 모델 대비 17% 향상된 성능 달성
- **시뮬레이션 벤치마크**: LIBERO, Bridge-V2 등 시뮬레이션 환경에서 6% 성능 향상
- **다중 플랫폼 검증**: Franka 로봇, Bridge-V2 데이터셋 등 여러 로봇 플랫폼에서 state-of-the-art 성능 달성
- **비표지 데이터 활용**: EPIC-KITCHEN-100 같은 행동 주석이 없는 비디오 데이터를 활용하여 시각 추론 능력 향상
- **Action chunking 효과**: 단일 행동이 아닌 행동 수열 예측이 성능 개선에 기여함을 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of CoT-VLA framework. We build our model on VILA-U [67], a generative multimodal model pretrained on*

- VILA-U 기반 multimodal 기초 모델을 Open X-Embodiment dataset 및 행동 주석이 없는 비디오 데이터로 사전 학습
- Hybrid attention 메커니즘 설계: 픽셀과 텍스트 생성에는 causal attention으로 순차적 예측, 행동 예측에는 full attention으로 모든 행동 차원을 동시 예측
- 부분 목표 이미지를 중간 추론 단계로서 자동회귀적으로 생성
- 생성된 부분 목표 이미지와 현재 관찰을 모두 조건으로 하여 행동 수열 생성
- 행동 chunking 기법 적용하여 단계별 행동 생성 대신 짧은 행동 수열 한 번에 생성
- Downstream task에 대해 수집된 로봇 데모로 미세 조정

## Originality

- VLA 프레임워크에 visual chain-of-thought 개념을 처음으로 통합하여, 기존 텍스트 기반 또는 키포인트 기반 intermediate reasoning과 구별됨
- 부분 목표 이미지를 natural intermediate reasoning state로 활용함으로써 추가 전처리 파이프라인 없이도 데모 데이터에서 자연스럽게 활용 가능
- 행동 주석이 없는 비디오 데이터(action-less video)를 VLA 학습에 활용하는 새로운 방식 제시
- Hybrid attention 메커니즘으로 상이한 모달리티의 특성에 맞게 다른 attention 전략 적용

## Limitation & Further Study

- 부분 목표 이미지 생성이 추가적인 추론 단계이므로 계산량 증가 및 생성 오류가 누적될 가능성
- 복잡한 다중 단계 작업에서 부분 목표 이미지의 정확성이 최종 성능에 미치는 영향에 대한 상세 분석 부족
- Open X-Embodiment와 EPIC-KITCHEN-100 데이터의 특성이 결과에 미치는 영향의 구체적 분석 필요
- 실제 환경의 동역학적 오차나 불확실성에 대한 로버스트성 평가 부족
- **후속 연구**: 부분 목표 생성 오류로부터의 회복 메커니즘 개발, 다양한 시각적 표현(예: 점 궤적, 열량도 등)과의 비교, 더 긴 horizon 작업에서의 성능 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 VLA에 visual chain-of-thought 추론을 도입하여 해석성과 성능을 동시에 개선한 혁신적인 작업이며, 행동 주석이 없는 비디오 데이터 활용이라는 실용적 이점과 함께 다양한 실험으로 효과성을 충분히 입증하였다.

## Related Papers

- 🏛 기반 연구: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — embodied chain-of-thought reasoning이 visual CoT의 로봇 적용을 위한 핵심 이론적 기반
- 🔄 다른 접근: [[papers/1428_Hume_Introducing_System-2_Thinking_in_Visual-Language-Action/review]] — visual chain-of-thought와 system-2 thinking의 서로 다른 VLA 추론 능력 향상 접근법
- 🔗 후속 연구: [[papers/1343_Cosmos-Reason1_From_Physical_Common_Sense_To_Embodied_Reason/review]] — CoT-VLA의 시각적 chain-of-thought와 Cosmos-Reason1의 물리적 추론은 VLA 모델의 단계별 추론 능력을 상호 보완적으로 강화한다.
- 🔄 다른 접근: [[papers/1364_Diffusion-VLA_Generalizable_and_Interpretable_Robot_Foundati/review]] — CoT-VLA의 미래 목표 이미지 생성과 Diffusion-VLA의 reasoning injection은 VLA 모델 추론 통합의 서로 다른 접근 방식이다.
- 🔗 후속 연구: [[papers/1328_Chain-of-Action_Trajectory_Autoregressive_Modeling_for_Robot/review]] — Visual CoT의 순차적 추론 개념이 Chain-of-Action의 역방향 궤적 모델링에 추론 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1528_Reflective_Planning_Vision-Language_Models_for_Multi-Stage_L/review]] — Reflective Planning의 multi-stage 추론 개념이 CoT-VLA의 시각적 chain-of-thought 구조의 기초가 됩니다.
- 🔗 후속 연구: [[papers/1343_Cosmos-Reason1_From_Physical_Common_Sense_To_Embodied_Reason/review]] — Cosmos-Reason1의 물리적 상식 추론과 CoT-VLA의 시각적 chain-of-thought는 모두 VLA 모델의 추론 능력 강화를 위한 보완적 접근법이다.
- 🔗 후속 연구: [[papers/1399_From_Seeing_to_Doing_Bridging_Reasoning_and_Decision_for_Rob/review]] — visual reasoning에서 spatial relationship을 활용한 접근법을 chain-of-thought로 확장한 연구입니다.
- 🔄 다른 접근: [[papers/1382_EmbodiedVSR_Dynamic_Scene_Graph-Guided_Chain-of-Thought_Reas/review]] — CoT-VLA의 visual chain-of-thought와 EmbodiedVSR의 dynamic scene graph-guided reasoning은 VLA에서 추론 과정을 서로 다르게 구조화한다.
- 🔗 후속 연구: [[papers/1464_Magma_A_Foundation_Model_for_Multimodal_AI_Agents/review]] — CoT-VLA의 시각적 추론 체인을 확장하여 Set-of-Mark과 Trace-of-Mark로 더 정교한 시공간 추론을 가능하게 한다.
- 🔄 다른 접근: [[papers/1478_MineDreamer_Learning_to_Follow_Instructions_via_Chain-of-Ima/review]] — 둘 다 시각적 추론 체인을 활용하지만, MineDreamer는 상상 기반 계획을, CoT-VLA는 추론 체인 기반 행동 생성에 집중한다.
- 🏛 기반 연구: [[papers/1503_OneTwoVLA_A_Unified_Vision-Language-Action_Model_with_Adapti/review]] — visual chain-of-thought reasoning의 기본 이론을 제공하여 OneTwoVLA의 adaptive reasoning 메커니즘 설계에 필요한 방법론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — CoT-VLA가 시각적 chain-of-thought에 중점을 두는 반면, Embodied CoT는 행동 예측을 위한 전체적인 embodied reasoning 과정을 다룬다.
- 🔄 다른 접근: [[papers/1556_RT-H_Action_Hierarchies_Using_Language/review]] — CoT-VLA는 RT-H와 유사하게 중간 추론 단계를 사용하지만 시각적 사고 체인을 활용하는 다른 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — Vision-Language-Action에서 visual chain-of-thought reasoning의 기반을 제시합니다.
- 🔗 후속 연구: [[papers/1585_ThinkBot_Embodied_Instruction_Following_with_Thought_Chain_R/review]] — 시각적 사고 체인 추론을 VLA 모델에 통합하여 ThinkBot의 사고 체인 추론을 시각 도메인으로 확장한 연구입니다.
- 🔄 다른 접근: [[papers/1592_TraceVLA_Visual_Trace_Prompting_Enhances_Spatial-Temporal_Aw/review]] — 둘 다 VLA 모델의 추론 능력 향상을 목표로 하지만 CoT-VLA는 Chain-of-Thought에, TraceVLA는 visual trace에 집중합니다.
- 🔄 다른 접근: [[papers/1610_Visual_Embodied_Brain_Let_Multimodal_Large_Language_Models_S/review]] — VeBrain과 CoT-VLA는 모두 MLLM의 시각적 추론을 로봇 제어에 활용하지만 통합 vs 연쇄 사고 접근이 다릅니다.
- 🏛 기반 연구: [[papers/1328_Chain-of-Action_Trajectory_Autoregressive_Modeling_for_Robot/review]] — Visual chain-of-thought의 순차적 추론 개념이 Chain-of-Action의 역방향 궤적 모델링에 영감을 제공합니다.
