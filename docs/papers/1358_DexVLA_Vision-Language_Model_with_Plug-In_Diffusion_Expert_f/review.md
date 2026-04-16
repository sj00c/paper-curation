---
title: "1358_DexVLA_Vision-Language_Model_with_Plug-In_Diffusion_Expert_f"
authors:
  - "Junjie Wen"
  - "Yichen Zhu"
  - "Jinming Li"
  - "Zhibin Tang"
  - "Chaomin Shen"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "DexVLA는 billion 규모의 diffusion-based action expert를 plug-in 형태로 vision-language model에 통합하고, 3단계 embodied curriculum learning 전략을 통해 다양한 로봇 형태에서 복잡한 long-horizon task를 수행할 수 있는 VLA 프레임워크를 제안한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_AI_Architectures"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wen et al._2025_DexVLA Vision-Language Model with Plug-In Diffusion Expert for General Robot Control.pdf"
---

# DexVLA: Vision-Language Model with Plug-In Diffusion Expert for General Robot Control

> **저자**: Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, Feifei Feng | **날짜**: 2025-02-09 | **URL**: [https://arxiv.org/abs/2502.05855](https://arxiv.org/abs/2502.05855)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: DexVLA architecture and embodied curriculum learning. Our model employs a three-stage*

DexVLA는 billion 규모의 diffusion-based action expert를 plug-in 형태로 vision-language model에 통합하고, 3단계 embodied curriculum learning 전략을 통해 다양한 로봇 형태에서 복잡한 long-horizon task를 수행할 수 있는 VLA 프레임워크를 제안한다.

## Motivation

- **Known**: Vision-language-action (VLA) 모델은 인터넷 규모 데이터로 사전 학습된 VLM을 활용하여 generalist robot policy 학습에 유망한 접근법이다. 다만 현재의 VLA 모델들은 VLM 컴포넌트 확대에 중점을 두면서 action space representation과 data scarcity라는 병목을 해결하지 못하고 있다.
- **Gap**: 기존 VLA 모델들은 action expert 설계를 소홀히 하고 cross-embodiment 학습에 제한적이며, 장기 복잡 task 완성을 위해 external high-level policy(예: SayCan)에 의존하는 문제가 있다.
- **Why**: 로봇이 다양한 환경과 형태에서 여러 task를 수행할 수 있도록 하는 것은 로봇 학습의 중심 과제이며, 이를 위해서는 효율적인 action representation과 직접적인 언어 지시 능력이 필수적이다.
- **Approach**: DexVLA는 billion-parameter diffusion expert를 VLM과 분리 가능한 형태로 설계하고, 3단계 curriculum learning(cross-embodiment pre-training, embodiment-specific alignment, task-specific adaptation)을 통해 점진적으로 복잡도를 높여가며 학습한다. 또한 sub-step reasoning을 활용하여 VLA 모델이 직접 long-horizon task를 분해하고 수행할 수 있도록 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Dexterous skills in diverse tasks and scenarios. Our proposed DexVLA method enables generalized*

- **Cross-embodiment 학습**: Single-arm, bimanual, dexterous hand, mobile bimanual 등 다양한 로봇 형태에서 효과적으로 작동하며 일반화 성능을 시연
- **데이터 효율성**: 100시간의 demonstration data만으로 학습하면서도 OpenVLA, Octo, π0 등 기존 SOTA 모델 대비 우수한 성능 달성
- **Novel embodiment 적응**: 100개 미만의 demonstration으로 새로운 로봇 형태에 대한 dexterous skill 습득 가능
- **Long-horizon task 수행**: Sub-step reasoning 활용으로 external high-level policy 없이 laundry folding 같은 복잡한 task를 직접 언어 프롬프트로 수행
- **실시간 추론**: 단일 Nvidia A6000 GPU에서 60Hz 속도로 동작하는 효율적인 추론

## How

![Figure 2](figures/fig2.webp)

*Figure 2: DexVLA architecture and embodied curriculum learning. Our model employs a three-stage*

- Qwen2-VL을 base VLM으로 사용하고, image encoder로 로봇 관찰을 embedding space로 투영
- VLM의 출력을 reasoning tokens과 action tokens로 분리하여 action tokens를 projection module을 통해 diffusion expert input으로 변환
- Diffusion expert는 transformer 기반 architecture로 각 embodiment별 multi-head action head를 포함하여 cross-embodiment learning 가능하게 구성
- Stage 1: Diffusion expert만 cross-embodiment 데이터로 사전 학습하여 low-level motor skills 학습
- Stage 2: 학습된 diffusion expert와 VLM을 통합하여 특정 로봇에 alignment, expert의 visual/language 컴포넌트는 폐기
- Stage 3: Sub-step reasoning 주석이 포함된 demonstration으로 post-training하여 long-horizon task 능력 강화
- 각 stage에서는 점진적으로 task 복잡도를 증가시켜 curriculum learning 구현

## Originality

- 기존 VLA 모델과 달리 billion-parameter scale의 독립적 diffusion-based action expert를 plug-in 형태로 설계
- Cross-embodiment learning을 위해 multi-head architecture를 diffusion expert에 도입한 novel 구조
- 3단계 embodiment curriculum learning strategy로 단계적이고 체계적인 학습 프로세스 제시
- Sub-step reasoning annotation을 활용하여 VLA 모델이 직접 long-horizon task planning을 수행하도록 한 end-to-end 접근
- 기존 external high-level policy에 의존하지 않으면서도 복잡한 task 수행 가능하게 한 paradigm shift

## Limitation & Further Study

- 제시된 실험이 주로 manipulation task에 집중되어 있으며, navigation이나 다른 유형의 로봇 task에 대한 검증이 부족
- 100시간 데이터 사용과 비교 모델들(OpenVLA, π0 등)이 훨씬 큰 규모의 데이터를 사용한 점을 고려할 때, 동일한 데이터 규모에서의 공정한 비교 부재
- Dexterous hand 같은 고도로 복잡한 제어 공간에서의 성능이 fully validated되지 않은 것으로 보임
- Sub-step reasoning annotation의 작성 비용과 scalability에 대한 논의 부족
- Long-horizon task의 성공률이 다소 제한적일 수 있으며, contact-rich manipulation에서의 failure case 분석 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: DexVLA는 diffusion-based action expert의 plug-in 설계와 embodied curriculum learning 전략으로 VLA의 효율성과 일반화 능력을 크게 향상시킨 작업이다. 특히 external high-level policy 없이 복잡한 long-horizon task를 직접 수행할 수 있다는 점과 제한된 데이터로 다양한 로봇에 적응할 수 있다는 점이 현실적 가치가 높으나, 공정한 비교 실험과 더 광범위한 task 검증이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1287_π_0_A_Vision-Language-Action_Flow_Model_for_General_Robot_Co/review]] — DexVLA의 diffusion expert 통합과 π0의 flow matching 행동 생성은 VLA 모델에서 행동 생성의 서로 다른 확률적 접근법이다.
- 🔗 후속 연구: [[papers/1522_RDT-1B_a_Diffusion_Foundation_Model_for_Bimanual_Manipulatio/review]] — DexVLA의 diffusion action expert와 RDT-1B의 diffusion foundation model은 양손 조작에서 diffusion 기반 정책의 발전을 보여준다.
- 🏛 기반 연구: [[papers/1375_Efficient_Diffusion_Transformer_Policies_with_Mixture_of_Exp/review]] — Efficient Diffusion Transformer의 혼합 전문가 모델은 DexVLA의 diffusion expert 통합에 효율적인 구조적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 오픈소스 VLA 아키텍처와 학습 방법론이 DexVLA의 billion 규모 diffusion expert 통합의 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1363_Diffusion_Transformer_Policy/review]] — Diffusion Transformer Policy의 기본 구조를 DexVLA가 VLA 프레임워크로 확장하고 embodied curriculum learning과 결합합니다.
- 🔄 다른 접근: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — Unified Vision-Language-Action Model은 DexVLA와 유사한 통합 모델이지만 diffusion expert 없이 다른 통합 전략을 사용합니다.
- 🔗 후속 연구: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — 대규모 VLA 모델의 구체적 구현과 embodied learning 전략을 제시합니다.
- 🔄 다른 접근: [[papers/1287_π_0_A_Vision-Language-Action_Flow_Model_for_General_Robot_Co/review]] — π0의 flow matching 기반 행동 생성과 DexVLA의 diffusion expert 접근법은 VLA 모델에서 행동 생성의 서로 다른 방법론이다.
- 🔗 후속 연구: [[papers/1356_DexGraspVLA_A_Vision-Language-Action_Framework_Towards_Gener/review]] — DexVLA의 plug-in diffusion expert와 DexGraspVLA의 diffusion 기반 저수준 컨트롤러는 모두 diffusion을 VLA에 통합하는 방향성을 공유한다.
