---
title: "1480_Moto_Latent_Motion_Token_as_the_Bridging_Language_for_Learni"
authors:
  - "Yi Chen"
  - "Yuying Ge"
  - "Weiliang Tang"
  - "Yizhuo Li"
  - "Yixiao Ge"
date: "2024.12"
doi: ""
arxiv: ""
score: 4.0
essence: "이 논문은 비디오에서 비지도 학습으로 latent motion token을 학습하여 로봇 조작 태스크를 위한 사전학습의 중간 표현으로 사용하고, Moto-GPT를 통해 motion token의 자동회귀 예측으로 motion prior를 학습한 후 co-fine-tuning으로 실제 로봇 제어로 전이하는 방법을 제안한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Egocentric_Human_Data"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Chen et al._2024_Moto Latent Motion Token as the Bridging Language for Learning Robot Manipulation from Videos.pdf"
---

# Moto: Latent Motion Token as the Bridging Language for Learning Robot Manipulation from Videos

> **저자**: Yi Chen, Yuying Ge, Weiliang Tang, Yizhuo Li, Yixiao Ge, Mingyu Ding, Ying Shan, Xihui Liu | **날짜**: 2024-12-05 | **URL**: [https://arxiv.org/abs/2412.04445](https://arxiv.org/abs/2412.04445)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of Moto’s three training stages: (1) The Latent Motion Tokenizer encodes key visual motions between v*

이 논문은 비디오에서 비지도 학습으로 latent motion token을 학습하여 로봇 조작 태스크를 위한 사전학습의 중간 표현으로 사용하고, Moto-GPT를 통해 motion token의 자동회귀 예측으로 motion prior를 학습한 후 co-fine-tuning으로 실제 로봇 제어로 전이하는 방법을 제안한다.

## Motivation

- **Known**: LLM의 자동회귀 사전학습이 NLP에서 성공했으며, 최근 로봇 학습에서도 vision-language-action 모델이나 비디오 사전학습 기반 접근이 시도되고 있다.
- **Gap**: 기존 비디오 사전학습은 정적 프레임이나 픽셀 레벨 토큰에 초점을 맞추었으나, 로봇 조작에 직접적으로 유용한 motion 수준의 표현 학습과 그 전이 메커니즘이 부족하다.
- **Why**: 풍부한 비디오 데이터를 활용하여 action 라벨 없이 motion 지식을 학습하고 이를 로봇 제어로 효과적으로 전이할 수 있다면 데이터 비용 문제를 크게 완화할 수 있기 때문이다.
- **Approach**: VQ-VAE 기반 Latent Motion Tokenizer로 연속 프레임 간의 동작을 압축된 discrete token으로 변환하고, GPT 기반 Moto-GPT를 motion token의 다음 토큰 예측으로 사전학습한 후, action query token을 삽입하는 co-fine-tuning으로 로봇 액션 예측으로 전이한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. The overview of Moto, which utilizes Latent Motion Tokens as a bridging “language” for autoregressive pretrain*

- **Latent Motion Token 표현**: VQ-VAE 기반으로 학습된 latent motion token이 의미론적으로 해석 가능하며 human-to-robot 간 cross-embodiment 전이 능력을 보임
- **Motion Prior 학습**: 사전학습된 Moto-GPT가 플ausible motion trajectory 예측과 output likelihood를 통한 trajectory rationality 평가 능력을 획득
- **로봇 제어 성능**: 사전학습된 motion prior를 포함한 Moto-GPT가 CALVIN 벤치마크에서 유의미한 성능 향상을 달성, 특히 제한된 학습 데이터 상황에서 우수한 견고성과 효율성 시연

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of Moto’s three training stages: (1) The Latent Motion Tokenizer encodes key visual motions between v*

- Latent Motion Tokenizer 학습: VQ-VAE 인코더가 연속된 두 프레임을 입력받아 discrete token으로 압축하고, 디코더가 첫 번째 프레임과 토큰으로부터 두 번째 프레임을 재구성하도록 정규화하여 프레임 간 변화(동작)를 캡처
- Moto-GPT 사전학습: 토큰화된 motion trajectory 시퀀스에 대해 initial frame과 text instruction을 조건으로 하여 next latent motion token을 예측하는 autoregressive 학습
- Co-fine-tuning 전이: action query token을 각 시간 단계의 motion token chunk 옆에 삽입하고, learnable module이 action query의 출력으로 저수준 액션을 예측하면서 동시에 motion token에 대해서는 기존의 next-token prediction 목적 함수를 유지

## Originality

- Motion token이라는 hardware-agnostic 중간 표현을 도입하여 비디오 사전학습과 로봇 제어 간의 의미론적 간극을 효과적으로 연결
- Unsupervised Latent Motion Tokenizer와 autoregressive Moto-GPT의 조합으로 action 라벨 없이도 motion prior를 대규모로 학습 가능
- Co-fine-tuning 메커니즘으로 학습된 motion token 표현을 유지하면서 동시에 로봇 액션 예측을 가능하게 하는 우아한 설계

## Limitation & Further Study

- Latent Motion Tokenizer의 성능이 VQ-VAE 기반 아키텍처에 의존하므로, 복잡한 다중 객체 인터랙션이나 빠른 동작에서의 제한 가능성
- Co-fine-tuning 시 action 라벨이 필요하므로 완전한 비지도 학습이 아니며, 실제 로봇 환경으로의 시뮬-투-리얼 전이 성능이 충분히 검증되지 않음
- 현재 평가가 주로 CALVIN 벤치마크에 집중되어 있으므로, 더 다양한 로봇 플랫폼과 조작 복잡도에 대한 일반화 능력 검증이 필요
- 후속 연구로는 더 큰 규모의 비디오 데이터(Internet-scale)로 사전학습 시 성능 향상 정량화, 실제 로봇에서의 직접 검증, 그리고 다중 모달리티(depth, proprioception) 통합 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 latent motion token을 통해 비디오 사전학습과 로봇 제어를 우아하게 연결하는 창의적인 접근을 제시하며, motion prior의 학습과 전이에 대한 명확한 검증을 제공한다. 데이터 효율성과 해석 가능성 측면에서 로봇 학습에 의미 있는 기여를 하지만, 실제 로봇 환경에서의 광범위한 검증과 다양한 조작 복잡도에 대한 일반화 능력 증명이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1515_Phantom_Training_Robots_Without_Robots_Using_Only_Human_Vide/review]] — Phantom과 동일하게 인간 비디오를 활용하지만 Moto는 latent motion token이라는 중간 표현을 통해 차별화된 접근을 한다.
- 🏛 기반 연구: [[papers/1448_Latent_Action_Pretraining_from_Videos/review]] — 비디오에서의 latent action pretraining 연구가 Moto의 motion token 학습 방법론의 이론적 기초를 제공한다.
- 🏛 기반 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — 대규모 비디오 생성 사전학습의 기본 원리를 latent motion token learning에 적용하는 이론적 토대를 제공한다.
- 🔄 다른 접근: [[papers/1448_Latent_Action_Pretraining_from_Videos/review]] — 둘 다 비디오에서 motion representation을 학습하지만 VQ-VAE 기반 양자화와 latent motion token의 접근법 차이를 비교할 수 있다.
- 🔄 다른 접근: [[papers/1330_CLAM_Continuous_Latent_Action_Models_for_Robot_Learning_from/review]] — 둘 다 latent action modeling을 다루지만 CLAM은 continuous latent space에, Moto는 latent motion token에 중점을 둡니다.
