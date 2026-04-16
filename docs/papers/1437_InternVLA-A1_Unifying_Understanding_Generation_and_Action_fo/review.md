---
title: "1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo"
authors:
  - "Junhao Cai"
  - "Zetao Cai"
  - "Jiafei Cao"
  - "Yilun Chen"
  - "Zeyu He"
date: "2026.01"
doi: ""
arxiv: ""
score: 4.0
essence: "InternVLA-A1은 Mixture-of-Transformers 아키텍처를 통해 의미 이해, 시각적 예측, 행동 실행을 통합하여 로봇 조작 성능을 향상시키는 Vision-Language-Action 모델이다. 실세계 로봇 데이터, 합성 시뮬레이션 데이터, 인간 비디오를 포함한 692M 프레임의 이질적 데이터로 사전학습되어 동적 조작 작업에서 26.7% 성능 향상을 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Video_Action_Generation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Cai et al._2026_InternVLA-A1 Unifying Understanding, Generation and Action for Robotic Manipulation.pdf"
---

# InternVLA-A1: Unifying Understanding, Generation and Action for Robotic Manipulation

> **저자**: Junhao Cai, Zetao Cai, Jiafei Cao, Yilun Chen, Zeyu He, Lei Jiang, Hang Li, Hengjie Li, Yang Li, Yufei Liu, Yanan Lu, Qi Lv, Haoxiang Ma, Jiangmiao Pang, Yu Qiao, Zherui Qiu, Yanqing Shen, Xu Shi, Yang Tian, Bolun Wang, Hanqing Wang, Jiaheng Wang, Tai Wang, Xueyuan Wei, Chao Wu, Yiman Xie, Boyang Xing, Yuqiang Yang, Yuyin Yang, Qiaojun Yu, Feng Yuan, Jia Zeng, Jingjing Zhang, Shenghan Zhang, Shi Zhang, Zhuoma Zhaxi, Bowen Zhou, Yuanzhen Zhou, Yunsong Zhou, Hongrui Zhu, Yangkun Zhu, Yuchen Zhu | **날짜**: 2026-01-05 | **URL**: [https://arxiv.org/abs/2601.02456](https://arxiv.org/abs/2601.02456)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. InternVLA-A1 unifies scene understanding, visual foresight generation, and action execution*

InternVLA-A1은 Mixture-of-Transformers 아키텍처를 통해 의미 이해, 시각적 예측, 행동 실행을 통합하여 로봇 조작 성능을 향상시키는 Vision-Language-Action 모델이다. 실세계 로봇 데이터, 합성 시뮬레이션 데이터, 인간 비디오를 포함한 692M 프레임의 이질적 데이터로 사전학습되어 동적 조작 작업에서 26.7% 성능 향상을 달성한다.

## Motivation

- **Known**: 기존 MLLM 기반 VLA 모델은 뛰어난 의미 이해 능력을 보유하지만 물리 역학 추론이 부족하고, World Model 기반 접근은 의미 정보 손실과 비디오 예측 오류에 취약하다.
- **Gap**: 현재 VLA 모델들은 의미론적 추론과 동적 예측 능력을 효과적으로 결합하지 못하고 있으며, 동적 환경(예: 컨베이어 벨트)에서의 적응성이 제한적이다.
- **Why**: 로봇의 일반화 능력 향상과 동적 환경에서의 신뢰성 있는 조작을 위해서는 의미 이해와 물리 역학 예측을 통합하는 것이 필수적이며, 이는 실세계 응용의 핵심 과제이다.
- **Approach**: 세 개의 전문가(scene understanding, visual foresight generation, action execution)로 구성된 통합 Mixture-of-Transformers 아키텍처를 설계하고, 실제 로봇 데이터, 합성 시뮬레이션 데이터, 인간 비디오의 이질적 데이터 소스로 joint training을 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. InternVLA-A1 unifies scene understanding, visual foresight generation, and action execution*

- **정적 조작 성능**: π0.5 대비 4.4% 성능 향상 달성
- **동적 조작 성능**: π0.5 대비 26.7% 성능 향상으로 동적 환경에서의 뛰어난 우수성 입증
- **시뮬레이션 벤치마크**: RoboTwin 2.0에서 2.6% 향상
- **모델 규모**: 2B, 3B 파라미터 스케일로 효율적 배포 가능
- **데이터 규모**: 692M 프레임의 대규모 이질적 데이터로 사전학습

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Framework of InternVLA-A1. The architecture comprises three experts: (1) an under-*

- Mixture-of-Transformers 아키텍처를 통해 세 개의 전문가를 unified masked self-attention 메커니즘으로 조화롭게 연결
- InternVL3과 Qwen3-VL을 기반으로 구축하여 강력한 의미 이해 능력 확보
- Scene understanding 전문가: MLLM 기반 의미 정보 추출
- Generation 전문가: 비디오 예측을 통한 시각적 foresight 생성
- Action execution 전문가: 의미론적 지도 하에서 연속 행동 생성
- 실세계 로봇 데이터, 합성 시뮬레이션 데이터, 인간 비디오의 hybrid training strategy로 sim-to-real gap 최소화
- Domain randomization을 활용한 robust 정책 학습

## Originality

- MLLM의 의미 이해와 World Model의 동적 예측을 처음으로 효과적으로 통합한 unified 아키텍처 제시
- 의미론적 grounding을 강화한 비디오 예측 방식으로 기존 World Model의 brittleness 해결
- 세 가지 이질적 데이터 소스(실세계, 시뮬레이션, 인간 비디오)의 joint training 파이프라인을 통한 혁신적 데이터 활용 전략
- 동적 환경에서 특히 강력한 성능 달성으로 기존 모델의 한계 극복

## Limitation & Further Study

- 12개의 실세계 작업으로 평가하였으나 더 광범위한 다양한 작업에 대한 평가 필요
- 시뮬레이션과 실세계 간의 완전한 gap 제거 여부는 미확인
- 모델 규모(2B, 3B)가 상대적으로 작아 더 큰 규모에서의 성능 확장성에 대한 검증 필요
- 비디오 예측 오류에 대한 구체적인 robustness 분석이 부족
- 후속 연구에서 더 복잡한 다단계 작업(multi-step manipulation)에 대한 평가와 더 큰 파라미터 규모의 모델 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: InternVLA-A1은 의미 이해와 동적 예측을 통합하는 혁신적 아키텍처와 이질적 데이터 source의 효과적 활용으로 로봇 조작의 일반화 문제를 크게 향상시켰다. 특히 동적 환경에서의 26.7% 성능 향상은 실세계 응용의 중요한 진전을 보여주며, VLA 분야의 주요 기여이다.

## Related Papers

- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — 둘 다 통합된 VLA 모델을 제시하지만, InternVLA-A1은 Mixture-of-Transformers 아키텍처를, OpenVLA는 일반화된 오픈소스 접근법을 택한다.
- 🏛 기반 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — InternVLA-A1의 시각적 예측 능력이 World Simulation with Video Foundation Models의 물리적 추론 기반 위에 구축된다.
- 🔗 후속 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — InternVLA-A1이 대규모 비디오 생성 사전학습의 방법론을 로봇 조작에 특화된 형태로 확장 적용한다.
- 🔄 다른 접근: [[papers/1374_DynamicVLA_A_Vision-Language-Action_Model_for_Dynamic_Object/review]] — DynamicVLA와 유사하게 동적 환경을 다루지만 Mixture-of-Transformers로 이해, 생성, 행동을 통합하는 다른 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1375_Efficient_Diffusion_Transformer_Policies_with_Mixture_of_Exp/review]] — 둘 다 Mixture-of-Experts 아키텍처를 사용하지만 video generation과 diffusion policy의 접근법 차이를 분석할 수 있다.
- 🔗 후속 연구: [[papers/1424_HiMoE-VLA_Hierarchical_Mixture-of-Experts_for_Generalist_Vis/review]] — hierarchical mixture-of-experts를 video action generation에 확장하여 더 복잡한 동적 조작 작업을 처리할 수 있다.
- ⚖️ 반론/비판: [[papers/1464_Magma_A_Foundation_Model_for_Multimodal_AI_Agents/review]] — 멀티모달 기초 모델의 이해-생성-행동 통합에서 다른 아키텍처 관점 제시
- 🏛 기반 연구: [[papers/1438_InternVLA-M1_A_Spatially_Guided_Vision-Language-Action_Frame/review]] — 통합된 이해-생성-행동 모델의 기본 구조가 InternVLA-M1의 공간 그라운딩 프레임워크에 기반이 된다.
- 🔄 다른 접근: [[papers/1481_Motus_A_Unified_Latent_Action_World_Model/review]] — 둘 다 unified vision-language-action model을 다루지만 latent action world model과 mixture-of-transformers의 접근법 차이를 비교할 수 있다.
- 🔄 다른 접근: [[papers/1511_PaLI-X_On_Scaling_up_a_Multilingual_Vision_and_Language_Mode/review]] — multilingual vision-language model에서 PaLI-X vs InternVLA의 다른 scaling 접근
- 🔗 후속 연구: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — InternVLA의 통합 접근법을 discrete token 기반으로 확장한 발전된 모델입니다.
- 🏛 기반 연구: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — InternVLA의 understanding, generation, action 통합 방법론이 VLA-0의 단순한 텍스트 기반 action 표현의 이론적 토대를 제공한다.
- 🔗 후속 연구: [[papers/1358_DexVLA_Vision-Language_Model_with_Plug-In_Diffusion_Expert_f/review]] — 대규모 VLA 모델의 구체적 구현과 embodied learning 전략을 제시합니다.
