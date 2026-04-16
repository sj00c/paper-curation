---
title: "1599_Unified_Vision-Language-Action_Model"
authors:
  - "Yuqi Wang"
  - "Xinghang Li"
  - "Wenxuan Wang"
  - "Junbo Zhang"
  - "Yingyan Li"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "UniVLA는 vision, language, action을 discrete token으로 통일하여 autoregressive sequence modeling으로 joint하게 학습하는 unified vision-language-action model이다. World model을 post-training에 통합하여 비디오에서 temporal dynamics를 학습하고 downstream policy learning을 강화한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2025_Unified Vision-Language-Action Model.pdf"
---

# Unified Vision-Language-Action Model

> **저자**: Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, Zhaoxiang Zhang | **날짜**: 2025-06-24 | **URL**: [https://arxiv.org/abs/2506.19850](https://arxiv.org/abs/2506.19850)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: We present UniVLA, a unified vision-language-action model. Unlike prior VLA*

UniVLA는 vision, language, action을 discrete token으로 통일하여 autoregressive sequence modeling으로 joint하게 학습하는 unified vision-language-action model이다. World model을 post-training에 통합하여 비디오에서 temporal dynamics를 학습하고 downstream policy learning을 강화한다.

## Motivation

- **Known**: 기존 VLA 모델들은 VLM의 semantic comprehension을 활용하여 action signal을 생성하지만, 주로 static image에서 action으로의 late-fusion 전략을 사용한다. RT-2, OpenVLA 등이 pure action prediction 패러다임을 선도하고 있다.
- **Gap**: 기존 접근법들은 heterogeneous modalities를 unified representation으로 모델링하지 못하며, temporal과 causal dependencies를 충분히 포착하지 못한다. 또한 static paradigm으로 인해 대규모 비디오 데이터의 temporal information을 효과적으로 활용하지 못한다.
- **Why**: Unified multimodal modeling은 더 긴밀한 cross-modal integration을 가능하게 하며, world model을 통한 causal dynamics 학습은 특히 long-horizon task와 out-of-distribution 시나리오에서 정책 학습을 크게 향상시킬 수 있다.
- **Approach**: Vision, language, action을 shared vocabulary의 discrete token으로 변환하고 unified autoregressive framework에서 모델링한다. Markov chain 기반의 interleaved observation-action sequence 구조로 causal dependencies를 자연스럽게 통합하고, world model post-training을 통해 대규모 robotic video에서 temporal dynamics를 학습한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: We present UniVLA, a unified vision-language-action model. Unlike prior VLA*

- **State-of-the-art 성능**: LIBERO 95.5% (vs π0-FAST 85.5%), CALVIN, SimplerEnv-Bridge 등에서 기존 방법 대비 유의미한 성능 향상 달성
- **Unified multimodal capability**: 단일 architecture로 action prediction, spatial reasoning, video prediction 등 다양한 multimodal tasks 지원
- **Large-scale video training**: Discrete token 기반 설계로 대규모 robotic video 데이터의 효과적인 활용 가능
- **Broad applicability**: Real-world ALOHA manipulation과 autonomous driving 시나리오까지 확장 가능성 실증
- **World model의 효과**: Post-training world model이 downstream policy learning의 data efficiency와 training efficiency를 크게 향상시킴

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of the UniVLA framework. Our model unifies information from different*

- Vision, language, action을 tokenizer를 통해 discrete token sequence로 변환하여 unified vocabulary 구성
- Shared autoregressive language model backbone을 사용하여 모든 modality를 jointly modeling
- Interleaved observation-action sequence 구조로 temporal causal structure 자연스럽게 반영
- Post-training 단계에서 world model task (video prediction)을 통해 environment dynamics 학습
- Learned dynamics를 downstream policy learning에 knowledge transfer하여 sample efficiency와 generalization 향상
- Multiple post-training tasks (text supervision, vision supervision, action supervision) 동시 지원

## Originality

- Vision-language-action의 세 modality를 처음으로 unified discrete token framework에서 joint하게 모델링
- 기존 pure action prediction과 visual-guided action prediction 패러다임을 통합한 novel architecture 제시
- World model을 post-training stage에 명시적으로 통합하여 policy learning과의 synergy 창출
- Autoregressive sequence modeling으로 temporal과 causal structure를 native하게 반영하는 새로운 관점 제안

## Limitation & Further Study

- Real-world 평가가 ALOHA와 driving으로 제한적이며, 더 다양한 embodied AI 시나리오에서의 검증 필요
- Discrete tokenization으로 인한 정보 손실과 token vocabulary size의 적절한 설정에 대한 ablation 분석 부족
- World model post-training의 computational cost와 training time에 대한 상세 분석 미흡
- Generalization capability에 대한 systematic analysis 필요 (domain gap, task distribution shift 등)
- Token-based 접근의 inference latency와 실시간 control 적용성에 대한 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: UniVLA는 heterogeneous modalities를 unified discrete token 프레임워크로 통합하고 world model post-training으로 temporal dynamics를 학습하는 혁신적인 VLA 모델이다. 다중 벤치마크에서 SOTA 성능을 달성했으며, multimodal capability와 large-scale video training 가능성으로 generalist embodied AI의 새로운 방향을 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — open-source vision-language-action model의 기반이 되는 통합 모델링 접근법입니다.
- 🔄 다른 접근: [[papers/1598_Unified_Video_Action_Model/review]] — vision-language-action 통합을 위한 서로 다른 모델링 방법 - autoregressive vs diffusion입니다.
- 🔗 후속 연구: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — InternVLA의 통합 접근법을 discrete token 기반으로 확장한 발전된 모델입니다.
- 🔗 후속 연구: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — 3D 환경에서의 vision-language-action 통합을 통해 UniVLA의 unified token approach를 3차원 세계 모델로 확장합니다.
- 🏛 기반 연구: [[papers/1392_FAST_Efficient_Action_Tokenization_for_Vision-Language-Actio/review]] — efficient action tokenization 방법을 제공하여 UniVLA의 discrete token 통일 접근법에 핵심 기술적 기반을 제공합니다.
- 🧪 응용 사례: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — 비디오 foundation model을 활용한 세계 시뮬레이션으로 UniVLA의 world model 통합을 물리적 AI 응용으로 확장합니다.
- 🔄 다른 접근: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — 둘 다 VLA 통합을 추구하지만, UniVLA는 discrete token 통합을, VLA-0는 구조 변경 없는 텍스트 표현을 사용한다.
- 🏛 기반 연구: [[papers/1626_WHALE_Towards_Generalizable_and_Scalable_World_Models_for_Em/review]] — World model을 통한 temporal dynamics 학습의 이론적 기반을 제공하여 UniVLA의 post-training 통합 방법론을 뒷받침한다.
- 🔄 다른 접근: [[papers/1592_TraceVLA_Visual_Trace_Prompting_Enhances_Spatial-Temporal_Aw/review]] — 둘 다 VLA 모델의 spatial-temporal 처리를 개선하지만, TraceVLA는 visual trace를, UniVLA는 통합된 토큰화를 사용한다.
- 🔄 다른 접근: [[papers/1598_Unified_Video_Action_Model/review]] — 비디오와 액션의 통합 학습에 대한 서로 다른 접근법 - diffusion vs autoregressive modeling입니다.
- 🔄 다른 접근: [[papers/1624_VQ-VLA_Improving_Vision-Language-Action_Models_via_Scaling_V/review]] — 둘 다 action을 token으로 표현하지만, VQ-VLA는 vector quantization을, UniVLA는 discrete token 통합을 사용한다.
- 🔄 다른 접근: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — 둘 다 VLA 통합을 추구하지만, VLA-0는 구조 변경 없는 단순함을, UniVLA는 discrete token 통합을 추구한다.
- 🔄 다른 접근: [[papers/1385_EO-1_An_Open_Unified_Embodied_Foundation_Model_for_General_R/review]] — Unified Vision-Language-Action Model과 EO-1은 모두 통합 embodied foundation model을 목표로 하지만 다른 아키텍처 설계를 사용합니다.
- 🔄 다른 접근: [[papers/1358_DexVLA_Vision-Language_Model_with_Plug-In_Diffusion_Expert_f/review]] — Unified Vision-Language-Action Model은 DexVLA와 유사한 통합 모델이지만 diffusion expert 없이 다른 통합 전략을 사용합니다.
