---
title: "1385_EO-1_An_Open_Unified_Embodied_Foundation_Model_for_General_R"
authors:
  - "Delin Qu"
  - "Haoming Song"
  - "Qizhi Chen"
  - "Zhaoqing Chen"
  - "Xianqiang Gao"
date: "2025.08"
doi: ""
arxiv: ""
score: 4.0
essence: "EO-1은 interleaved vision-text-action 사전학습을 통해 multimodal embodied reasoning과 robot control을 통합한 unified embodied foundation model이며, 1.5M 샘플의 EO-Data1.5M 데이터셋과 함께 개발되었다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Qu et al._2025_EO-1 An Open Unified Embodied Foundation Model for General Robot Control.pdf"
---

# EO-1: An Open Unified Embodied Foundation Model for General Robot Control

> **저자**: Delin Qu, Haoming Song, Qizhi Chen, Zhaoqing Chen, Xianqiang Gao, Dong Wang, Xinyi Ye, Qi Lv, Modi Shi, Guanghui Ren, Cheng Ruan, Maoqing Yao, Haoran Yang, Jiacheng Bao, Bin Zhao, Xuelong Li | **날짜**: 2025-08-28 | **URL**: [https://arxiv.org/abs/2508.21112](https://arxiv.org/abs/2508.21112)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: EO-1 Model Architecture. EO-1 model is a Vision-Language-Action (VLA) model that adopts a*

EO-1은 interleaved vision-text-action 사전학습을 통해 multimodal embodied reasoning과 robot control을 통합한 unified embodied foundation model이며, 1.5M 샘플의 EO-Data1.5M 데이터셋과 함께 개발되었다.

## Motivation

- **Known**: 최근 vision-language-action (VLA) 모델들은 대규모 로봇 데이터와 visual-text 데이터의 co-training을 통해 일반적 로봇 제어에서 진전을 이루었다. 하지만 기존 VLA 모델들은 주로 시퀀스 끝에서만 로봇 액션을 생성하므로 vision, language, action 간의 시간적 동역학과 인과관계를 제대로 포착하지 못한다.
- **Gap**: 현존하는 VLA 모델들은 multimodal embodied reasoning과 physical action의 유연한 상호작용을 지원하지 못하며, 인간처럼 추론이 액션을 안내하고 액션 결과가 후속 추론을 정보하는 interleaved synergy를 달성하지 못한다.
- **Why**: 개방형 세계에서 자율 로봇이 diverse task를 수행하고 인간 수준의 유연성을 갖추려면 multimodal embodied reasoning과 dexterous action의 seamless integration이 필수적이며, 이는 advanced embodied AI 시스템의 핵심 목표이다.
- **Approach**: unified decoder-only transformer 아키텍처를 통해 auto-regressive decoding과 flow matching denoising을 통합하고, VLM 기반의 shared parameter를 modality-specific objective로 최적화하며, causal attention을 전체 interleaved vision-text-action 시퀀스에 적용한다. 또한 VLM과 human annotation을 활용하여 embodied reasoning QA pair와 robot action을 temporal order로 연결한 interleaved embodied dataset을 구성한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: (a) Statistics of EO-Robotics Dataset (EO-Data1.5M) and Benchmark (EO-Bench). (b) Dataset*

- **Unified Architecture**: 별도의 action-specific parameter 없이 multimodal embodied reasoning과 real robot control을 shared backbone에 통합하여 seamless cross-modal interaction을 실현
- **Interleaved Embodied Dataset**: 1.5M 샘플 규모의 EO-Data1.5M을 통해 vision, text, action의 temporal dynamics와 causal dependency를 포착하는 interleaved vision-text-action pretraining 가능
- **Real-world Generalization**: ERQA, LIBERO, SimplerEnv, EO-Bench 등 multiple embodied reasoning 및 robot control benchmark에서 기존 open-source 모델 대비 우수한 성능 달성
- **Open Release**: 모델 가중치, training code, interleaved embodied dataset 전체를 공개하여 community의 further research 촉진

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Interleaved rectifying sampling strategy. Our method samples variable-length subsequences from*

- VLM 기반 unified decoder-only transformer에 two MLP를 추가하여 continuous robotic action을 encode/decode
- Pre-trained VLM의 shared parameter를 text generation을 위한 next-token prediction과 robot action을 위한 flow matching으로 dual objective로 최적화
- Web vision-language data와 real robot episode를 통합하되, real robot episode를 VLM과 human이 embodied temporal/spatial QA pair로 annotate
- Interleaved format design을 통해 robot action에 대해 flexible하게 embodied reasoning QA를 associate하여 rich world knowledge와 cross-modal interaction 포착
- Causal attention을 전체 interleaved sequence에 적용하여 reasoning과 acting 간의 sequential dependency 포착

## Originality

- 기존 VLA 모델과 달리 action generation을 시퀀스 끝이 아닌 interleaved position에서 수행하여 reasoning-acting의 mutual-informed integration 실현
- Unified architecture로 action-specific module 없이 vision/language와 action 간의 직접적인 knowledge transfer 달성
- Scalable data curation pipeline을 통해 web data와 real robot data를 meaningfully combine하는 interleaved embodied dataset 구축
- Auto-regressive decoding과 flow matching denoising을 single unified model에 synergistically 통합하여 both discrete text와 continuous action 생성 가능

## Limitation & Further Study

- 논문에서 real-world evaluation의 scope과 robot embodiment diversity에 대한 명확한 제한 사항이 구체적으로 제시되지 않음
- 3B parameter 모델의 scaling behavior와 더 큰 모델 크기에서의 성능 향상 가능성에 대한 논의 부재
- Annotation quality control과 human annotation의 bias가 final model 성능에 미치는 영향에 대한 systematic analysis 부족
- 후속 연구로 추가적인 embodiment에 대한 generalization 검증과 real-world deployment scenario에서의 robustness 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: EO-1은 interleaved vision-text-action pretraining paradigm을 통해 embodied AI의 근본적인 문제인 reasoning-acting integration을 우아하게 해결하며, 1.5M 규모의 고품질 dataset과 unified architecture의 결합으로 open-world robot control에서 significant advancement를 제시한다. 전체 toolchain의 open release는 community에 substantial contribution을 제공한다.

## Related Papers

- 🔄 다른 접근: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — Unified Vision-Language-Action Model과 EO-1은 모두 통합 embodied foundation model을 목표로 하지만 다른 아키텍처 설계를 사용합니다.
- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 오픈소스 VLA 프레임워크가 EO-1의 unified embodied foundation model 설계의 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1406_Genie_Envisioner_A_Unified_World_Foundation_Platform_for_Rob/review]] — Genie Envisioner의 세계 foundation 플랫폼이 EO-1의 multimodal embodied reasoning을 더 포괄적인 로봇 제어 환경으로 확장합니다.
- 🏛 기반 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — PaLM-E의 embodied multimodal language model이 EO-1의 unified embodied foundation model 개발에 기초적인 아키텍처와 접근 방식을 제공한다.
- 🔗 후속 연구: [[papers/1499_OmniVLA_An_Omni-Modal_Vision-Language-Action_Model_for_Robot/review]] — OmniVLA의 omni-modal approach가 EO-1에서 interleaved vision-text-action pre-training으로 더욱 통합된 embodied foundation model로 발전했다.
- 🔄 다른 접근: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — 3D-VLA와 EO-1 모두 3D 시각 정보를 활용한 embodied foundation model이지만 world model 생성 방식이 다름
- 🏛 기반 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-2의 vision-language-action 통합 방법론은 EO-1의 multimodal embodied reasoning 설계 기반이 됨
- 🔄 다른 접근: [[papers/1464_Magma_A_Foundation_Model_for_Multimodal_AI_Agents/review]] — 통합된 embodied foundation model을 구축하는 다른 접근법
- 🔄 다른 접근: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — embodied multimodal language model에서 PaLM-E vs EO-1의 다른 통합 방식
