---
title: "1436_InstructVLA_Vision-Language-Action_Instruction_Tuning_from_U"
authors:
  - "Shuai Yang"
  - "Hao Li"
  - "Bin Wang"
  - "Yilun Chen"
  - "Yang Tian"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "InstructVLA는 Vision-Language Model의 추론 능력을 보존하면서 로봇 조작 성능을 달성하는 end-to-end VLA 모델이며, Vision-Language-Action Instruction Tuning (VLA-IT) 패러다임을 통해 multimodal reasoning과 action generation을 동시에 최적화한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yang et al._2025_InstructVLA Vision-Language-Action Instruction Tuning from Understanding to Manipulation.pdf"
---

# InstructVLA: Vision-Language-Action Instruction Tuning from Understanding to Manipulation

> **저자**: Shuai Yang, Hao Li, Bin Wang, Yilun Chen, Yang Tian, Tai Wang, Hanqing Wang, Feng Zhao, Yiyi Liao, Jiangmiao Pang | **날짜**: 2025-07-23 | **URL**: [https://arxiv.org/abs/2507.17520](https://arxiv.org/abs/2507.17520)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Method overview. InstructVLA integrates vision-language understanding with precise*

InstructVLA는 Vision-Language Model의 추론 능력을 보존하면서 로봇 조작 성능을 달성하는 end-to-end VLA 모델이며, Vision-Language-Action Instruction Tuning (VLA-IT) 패러다임을 통해 multimodal reasoning과 action generation을 동시에 최적화한다.

## Motivation

- **Known**: RT-2, OpenVLA 등의 기존 VLA 모델들은 vision-language 능력과 조작 성능 중 하나를 희생하거나 task-specific 데이터에만 제한되며, pre-trained VLM의 catastrophic forgetting 문제를 겪는다.
- **Gap**: VLM의 유연한 multimodal reasoning을 보존하면서 동시에 정확한 action generation을 달성하고, embodied reasoning을 효과적으로 조작 성능에 연결하는 메커니즘이 부재하다.
- **Why**: 로봇이 실제 환경에서 효과적으로 작동하려면 복잡한 instruction을 이해하고 reasoning하면서도 정확한 조작을 수행해야 하므로, 이 두 능력의 통합은 실용적인 human-robot interaction을 위해 필수적이다.
- **Approach**: VLA-IT 패러다임에서 mixture-of-experts adaptation을 활용하여 latent action queries를 통해 VLM backbone을 보존하면서 action generation을 학습하고, standard VLM corpora와 650K 크기의 VLA-IT 데이터셋을 jointly 학습한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Simpler-Instruct. Six representative test cases with instructions and InstructVLA responses.*

- **SimplerEnv 성능**: SpatialVLA 대비 33% 향상 달성
- **일반화 능력**: SimplerEnv-Instruct 벤치마크에서 fine-tuned OpenVLA 대비 96% 향상, GPT-4o 보조 action expert 대비 29% 향상
- **Multimodal 성능**: baseline VLM들을 초과하는 multimodal task 성능 달성
- **Inference-time scaling**: textual reasoning을 활용한 조작 성능 향상 (시뮬레이션 및 실제 환경)
- **데이터셋 및 벤치마크**: 650K 샘플 VLA-IT 데이터셋과 80-task SimplerEnv-Instruct 벤치마크 제시

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of the InstructVLA. InstructVLA integrates the multimodal reasoning capa-*

- 두 단계 훈련: (1) Action Pretraining에서 language-based motion description으로부터 distilled latent action queries를 사용하여 VLM-driven action expert 학습, (2) VLA-IT에서 mixture-of-experts adaptation으로 textual reasoning과 action generation 통합
- Multimodal web data, manipulation dataset, VLA-IT corpus를 jointly 학습하여 자동으로 textual reasoning과 action generation 간 switching 가능
- SimplerEnv-Instruct 벤치마크 구성: closed-loop manipulation과 high-level instruction reasoning을 모두 포함한 80개 zero-shot task
- Latent action queries를 통해 low-level control learning을 VLM backbone으로부터 decoupling하여 multimodal reasoning capability 보존

## Originality

- VLA 영역에서 처음으로 VLM의 reasoning 능력을 조작 성능 향상에 명시적으로 활용하고 이를 체계화한 VLA-IT 패러다임 제시
- Mixture-of-experts adaptation을 통한 novel한 multimodal knowledge와 action generation의 통합 메커니즘
- Embodied reasoning (scene understanding, task decomposition)을 manipulation instruction tuning에 포함한 새로운 데이터 annotation 전략
- Inference-time scaling의 개념을 VLA에 도입하여 textual reasoning으로 조작 성능 향상 입증

## Limitation & Further Study

- SimplerEnv-Instruct는 수작업으로 설계된 80개 task로 제한되어 있으며, 더 광범위한 open-world scenario에서의 일반화 능력은 미평가
- Real-world 실험이 제한적이며, 다양한 embodiment에서의 성능 일관성이 충분히 검증되지 않음
- 650K VLA-IT 데이터셋 구축 비용 및 확장성 이슈에 대한 논의 부족
- Latent action queries의 학습 안정성과 다양한 조작 task에 대한 표현 능력의 한계 분석 필요
- 후속 연구: (1) open-world instruction following을 위한 larger-scale benchmark 구축, (2) cross-embodiment transfer 메커니즘 개발, (3) real-time inference 최적화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: InstructVLA는 VLA 분야에서 multimodal reasoning과 precise action generation의 균형을 이루는 중요한 진전을 보여주며, VLA-IT 패러다임과 mixture-of-experts 통합 방식은 신선한 기술적 기여를 제시한다. 다만 real-world 검증 범위와 open-world generalization에 대한 추가 평가가 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA와 다르게 VLM의 추론 능력을 보존하면서 로봇 조작 성능을 달성하는 instruction tuning 방식을 제안한다.
- 🏛 기반 연구: [[papers/1611_Visual_Instruction_Tuning/review]] — Visual Instruction Tuning의 기본 개념을 vision-language-action 도메인으로 확장하여 적용한다.
- 🔗 후속 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-2의 web knowledge transfer를 instruction tuning으로 발전시켜 multimodal reasoning과 action을 동시 최적화한다.
- 🔗 후속 연구: [[papers/1404_Gemini_Robotics_Bringing_AI_into_the_Physical_World/review]] — Gemini 2.0의 추론 능력을 활용한 VLA 접근법으로 InstructVLA의 instruction tuning 개념과 상호 보완적이다.
- 🔗 후속 연구: [[papers/1605_VIMA_General_Robot_Manipulation_with_Multimodal_Prompts/review]] — InstructVLA는 VIMA의 멀티모달 instruction following을 VLA 프레임워크로 확장한 후속 연구다.
- 🔗 후속 연구: [[papers/1611_Visual_Instruction_Tuning/review]] — visual instruction tuning을 로봇의 vision-language-action instruction tuning으로 확장하여 embodied AI 도메인에 특화시킵니다.
- 🔄 다른 접근: [[papers/1324_Bridging_Language_and_Action_A_Survey_of_Language-Conditione/review]] — 인스트럭션 튜닝을 통한 다른 언어-행동 연결 방법을 제시한다.
