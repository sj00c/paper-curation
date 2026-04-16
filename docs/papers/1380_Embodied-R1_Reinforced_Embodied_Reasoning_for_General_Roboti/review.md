---
title: "1380_Embodied-R1_Reinforced_Embodied_Reasoning_for_General_Roboti"
authors:
  - "Yifu Yuan"
  - "Haiqin Cui"
  - "Yaoting Huang"
  - "Yibin Chen"
  - "Fei Ni"
date: "2025.08"
doi: ""
arxiv: ""
score: 4.0
essence: "Embodied-R1은 '포인팅'을 통일된 embodiment-agnostic 중간 표현으로 정의하고, Reinforced Fine-tuning(RFT)으로 훈련된 3B VLM으로서 로봇 조작의 perception-action gap을 효과적으로 극복한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robot_Policy_Learning"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yuan et al._2025_Embodied-R1 Reinforced Embodied Reasoning for General Robotic Manipulation.pdf"
---

# Embodied-R1: Reinforced Embodied Reasoning for General Robotic Manipulation

> **저자**: Yifu Yuan, Haiqin Cui, Yaoting Huang, Yibin Chen, Fei Ni, Zibin Dong, Pengyi Li, Yan Zheng, Hongyao Tang, Jianye Hao | **날짜**: 2025-08-19 | **URL**: [https://arxiv.org/abs/2508.13998](https://arxiv.org/abs/2508.13998)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 Overview of the Embodied-R1 framework and its zero-shot manipulation performance.*

Embodied-R1은 '포인팅'을 통일된 embodiment-agnostic 중간 표현으로 정의하고, Reinforced Fine-tuning(RFT)으로 훈련된 3B VLM으로서 로봇 조작의 perception-action gap을 효과적으로 극복한다.

## Motivation

- **Known**: Vision-Language-Action(VLA) 모델들은 강한 시각 인식 능력을 보이지만, 새로운 환경에서 조작 성능이 크게 저하되는 'seeing-to-doing gap' 문제가 있다. 이는 데이터 부족과 로봇 형태의 이질성 때문이다.
- **Gap**: 기존 포인팅 방식들은 affordance point, visual trace, target region 등 단편적인 형태만 제공하며, Supervised Fine-Tuning(SFT) 기반의 고정된 Chain-of-Thought 템플릿은 새로운 작업으로의 일반화를 제한한다.
- **Why**: 로봇 조작의 일반화는 다양한 환경과 로봇 플랫폼에서 작동해야 하기 때문에 중요하며, embodiment-agnostic 표현과 강력한 추론 능력이 현실적 배포에 필수적이다.
- **Approach**: 포인팅의 4가지 핵심 능력(REG, RRG, OFG, VTG)을 정의하고, 이를 지원하는 Embodied-Points-200K 데이터셋을 구성한다. RFT 기반 2단계 커리큘럼으로 훈련하여 다중 해답의 모호성을 해결하고 자유로운 추론을 가능하게 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1 Overview of the Embodied-R1 framework and its zero-shot manipulation performance.*

- **벤치마크 성과**: 11개의 embodied spatial 및 pointing 벤치마크에서 state-of-the-art 성능 달성
- **시뮬레이션 성과**: SIMPLEREnv에서 56.2% 성공률 달성
- **실제 로봇 성과**: 8개의 XArm 실제 작업에서 87.5% 성공률 달성 (task-specific fine-tuning 없음)
- **기준선 대비 개선**: 강한 기준선 대비 62% 성능 개선
- **강건성**: 조명 변화, 배경 변화, 높이 변화 등 다양한 시각적 방해에 대한 높은 강건성 입증

## How

![Figure 3](figures/fig3.webp)

*Figure 3 Overview of training data: In stage 1, we focus on improving the model’s spatial reasoning capability,*

- Embodied-Points-200K 데이터셋 구성: 다양한 embodied 및 일반 시각 추론 데이터셋에서 고품질 인스턴스를 수집하고 검증
- 2단계 RFT 커리큘럼: 첫 번째 단계에서 기본 능력 학습, 두 번째 단계에서 정교한 능력 학습
- 다중 작업 보상 설계: Format Reward, Accuracy Reward, Point in Mask Reward, Point Distance Reward, Environment Reward 등 5가지 보상 신호 설계
- 자유로운 추론 생성: <think> 태그를 통한 명시적 추론과 <answer> 태그를 통한 포인팅 좌표 생성으로 유연한 문제 해결
- Action Executor 통합: 생성된 포인팅 신호를 low-level action primitives로 변환하는 executor와 연결

## Originality

- 포인팅을 통일된 embodiment-agnostic 중간 표현으로 처음 체계화한 점
- 포인팅의 4가지 핵심 능력(REG, RRG, OFG, VTG)을 명확히 정의한 점
- embodied reasoning에 RFT를 적용하여 SFT의 고정 템플릿 제약을 극복한 점
- 포인팅의 다중 해답 모호성을 RFT로 직접 해결하는 접근법의 참신성
- 포인팅-중심 표현과 RFT 패러다임의 결합이 perception-action gap 해결의 효과적인 경로임을 증명한 점

## Limitation & Further Study

- 3B 파라미터 크기로 제한되어 있어 더 큰 모델의 성능 잠재력을 탐색할 여지가 있음
- 실제 로봇 실험이 단일 플랫폼(XArm)에 집중되어 있어 다양한 로봇 형태에 대한 일반화 검증 필요
- Embodied-Points-200K 데이터셋의 크기와 다양성이 향후 더 확장될 수 있는 여지
- Visual disturbance 실험이 조명, 배경, 높이로 제한되어 더 많은 종류의 방해 조건에 대한 평가 필요
- 후속연구로 더 복잡한 multi-step manipulation tasks와 협력 로봇 작업에의 확장 가능성 탐색 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Embodied-R1은 포인팅이라는 명확한 중간 표현과 RFT 기반 훈련 방식으로 embodied AI의 오래된 perception-action gap 문제에 우아한 해결책을 제시하며, 실제 로봇에서의 강력한 zero-shot 성능으로 그 실질적 가치를 입증한다.

## Related Papers

- 🏛 기반 연구: [[papers/1415_Grounding_DINO_Marrying_DINO_with_Grounded_Pre-Training_for/review]] — Grounding DINO의 시각적 grounding 기법이 Embodied-R1의 포인팅 기반 중간 표현 설계의 핵심 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen/review]] — RLinf-VLA는 Embodied-R1의 RFT 훈련 방법을 다양한 VLA 모델로 확장하여 더 일반적인 강화 학습 프레임워크를 제공합니다.
- 🧪 응용 사례: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — RoboPoint의 spatial affordance prediction이 Embodied-R1의 포인팅 기반 perception-action 연결의 구체적인 구현 방법을 제시합니다.
- 🔄 다른 접근: [[papers/1521_RationalVLA_A_Rational_Vision-Language-Action_Model_with_Dua/review]] — RationalVLA의 dual vision encoder와 Embodied-R1의 pointing-based representation은 VLM에서 perception-action gap을 서로 다르게 해결하는 접근법이다.
- 🔗 후속 연구: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — ThinkAct의 vision-language-action reasoning이 Embodied-R1의 reinforced fine-tuning을 통한 embodied reasoning으로 더욱 발전한 형태이다.
- 🏛 기반 연구: [[papers/1619_VLA-RFT_Vision-Language-Action_Reinforcement_Fine-tuning_wit/review]] — VLA-RFT의 vision-language-action reinforcement fine-tuning 방법론이 Embodied-R1의 RFT 기반 훈련 접근법에 기초가 된다.
- 🔄 다른 접근: [[papers/1439_IPR-1_Interactive_Physical_Reasoner/review]] — IPR-1도 물리적 추론을 통해 로봇 조작을 개선하지만 world model 롤아웃을 통한 상호작용적 학습에 중점을 둡니다.
- 🏛 기반 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — PaLM-E는 Embodied-R1이 기반으로 하는 대규모 비전-언어 모델의 embodied AI 적용에 대한 초기 연구입니다.
- 🏛 기반 연구: [[papers/1403_Gemini_Robotics_15_Pushing_the_Frontier_of_Generalist_Robots/review]] — 강화학습 기반 embodied reasoning이 Gemini Robotics-ER 1.5의 추론 능력 구현에 기반이 된다.
- 🔄 다른 접근: [[papers/1439_IPR-1_Interactive_Physical_Reasoner/review]] — Embodied-R1도 물리적 추론을 로봇 조작에 적용하지만 포인팅 기반 중간 표현을 사용하는 반면, IPR-1은 상호작용적 학습에 중점을 둡니다.
- 🔄 다른 접근: [[papers/1492_Neural_Brain_A_Neuroscience-inspired_Framework_for_Embodied/review]] — Neural Brain과 Embodied-R1 모두 embodied reasoning을 다루지만 신경과학적 접근과 강화학습 접근으로 차별화됩니다.
- 🔄 다른 접근: [[papers/1585_ThinkBot_Embodied_Instruction_Following_with_Thought_Chain_R/review]] — embodied instruction following에서 서로 다른 추론 접근법을 제시합니다.
- 🔗 후속 연구: [[papers/1614_VL-Nav_A_Neuro-Symbolic_Approach_for_Reasoning-based_Vision-/review]] — reinforced embodied reasoning을 neuro-symbolic 접근법과 결합할 수 있습니다.
