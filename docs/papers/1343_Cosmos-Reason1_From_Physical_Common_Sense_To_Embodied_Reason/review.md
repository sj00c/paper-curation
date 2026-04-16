---
title: "1343_Cosmos-Reason1_From_Physical_Common_Sense_To_Embodied_Reason"
authors:
  - ""
  - ""
  - "Alisson Azzolini"
  - "Junjie Bai"
  - "Hannah Brandon"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "NVIDIA에서 제시한 Cosmos-Reason1은 비디오를 입력으로 받아 물리적 상식과 구체화된 추론(embodied reasoning)을 통해 자연언어로 신체적 의사결정을 생성하는 멀티모달 LLM입니다. 계층적 온톨로지 기반 데이터 큐레이션과 Physical AI SFT 및 RL 학습으로 물리적 AI 추론 능력을 강화합니다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robot_Policy_Learning"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/NVIDIA et al._2025_Cosmos-Reason1 From Physical Common Sense To Embodied Reasoning.pdf"
---

# Cosmos-Reason1: From Physical Common Sense To Embodied Reasoning

> **저자**: , , Alisson Azzolini, Junjie Bai, Hannah Brandon, Jiaxin Cao, Prithvijit Chattopadhyay, Huayu Chen, Jinju Chu, Yin Cui, Jenna Diamond, Yifan Ding, Liang Feng, Francesco Ferroni, Rama Govindaraju, Jinwei Gu, Siddharth Gururani, Imad El Hanafi, Zekun Hao, Jacob Huffman, Jingyi Jin, Brendan Johnson, Rizwan Khan, George Kurian, Elena Lantz, Nayeon Lee, Zhaoshuo Li, Xuan Li, Maosheng Liao, Tsung-Yi Lin, Yen-Chen Lin, Ming-Yu Liu, Xiangyu Lu, Alice Luo, Andrew Mathau, Yun Ni, Lindsey Pavao, Wei Ping, David W. Romero, Misha Smelyanskiy, Shuran Song, Lyne Tchapmi, Andrew Z. Wang, Boxin Wang, Haoxiang Wang, Fangyin Wei, Jiashu Xu, Yao Xu, Dinghao Yang, Xiaodong Yang, Zhuolin Yang, Jingxu Zhang, Xiaohui Zeng, Zhe Zhang | **날짜**: 2025-03-18 | **URL**: [https://arxiv.org/abs/2503.15558](https://arxiv.org/abs/2503.15558)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: An overview of Cosmos-Reason1. Cosmos-Reason1 contains two multimodal large language models of*

NVIDIA에서 제시한 Cosmos-Reason1은 비디오를 입력으로 받아 물리적 상식과 구체화된 추론(embodied reasoning)을 통해 자연언어로 신체적 의사결정을 생성하는 멀티모달 LLM입니다. 계층적 온톨로지 기반 데이터 큐레이션과 Physical AI SFT 및 RL 학습으로 물리적 AI 추론 능력을 강화합니다.

## Motivation

- **Known**: LLM의 chain-of-thought 추론이 수학과 코딩 문제 해결에서 뛰어난 성과를 보였으나, 일반적으로 물리적 세계와의 연결성이 약합니다. 최근 multimodal LLM은 시각 정보를 통합하고 있지만 embodied agent의 의사결정을 직접적으로 지원하는 모델은 제한적입니다.
- **Gap**: 기존 LLM은 물리 법칙에 기반한 상식 추론과 다양한 embodiment(로봇, 휴머노이드, 자율주행)에 걸친 일반화된 embodied reasoning 능력이 부족합니다. 또한 물리적 AI 추론을 평가하는 체계적인 벤치마크와 온톨로지가 정의되지 않았습니다.
- **Why**: 물리적 AI는 로봇, 자율주행, 휴머노이드 등 실세계 상호작용을 요구하는 시스템의 핵심이며, 이들이 올바른 의사결정을 내리려면 물리 세계에 대한 깊은 이해와 장기 추론 능력이 필수적입니다.
- **Approach**: 공간(Space), 시간(Time), 기본 물리학(Fundamental Physics)으로 구성된 계층적 온톨로지와 5가지 embodied agent 유형에 대한 2차원 온톨로지를 정의하여 Physical AI 능력을 체계화합니다. 이를 바탕으로 약 4M개의 비디오-텍스트 쌍을 큐레이션하고 SFT와 rule-based RL로 7B/56B 모델을 학습합니다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: An overview of Cosmos-Reason1. Cosmos-Reason1 contains two multimodal large language models of*

- **물리적 AI 온톨로지 정의**: Space(4개), Time(5개), Fundamental Physics(7개) 총 16개 서브카테고리를 포함한 체계적 온톨로지와 embodied reasoning을 위한 2차원 온톨로지 제시
- **포괄적 벤치마크 구축**: Physical common sense 3개 벤치마크(Space, Time, Fundamental Physics) 604개 질문 및 embodied reasoning 6개 벤치마크 610개 질문으로 평가 체계 확립
- **대규모 데이터 큐레이션**: 온톨로지 기반으로 4M개 비디오-텍스트 쌍(캡션, MCQ, chain-of-thought) 구축 및 DeepSeek-R1 증류 활용
- **Physical AI SFT와 RL의 효과 입증**: Rule-based, verifiable reward(인간 주석 MCQ + 비디오 자체 구조 기반 자동 생성 MCQ)를 활용한 RL 학습으로 모든 벤치마크에서 유의미한 개선 달성
- **오픈소스 공개**: 코드와 사전학습 모델(Cosmos-Reason1-7B, 56B)을 NVIDIA Open Model License 하에 GitHub에 공개하여 Physical AI 발전 촉진

## How


- **아키텍처**: Decoder-only multimodal LLM으로 vision encoder → projector → pre-trained LLM 파이프라인 구성; dense Transformer와 hybrid Mamba-MLP-Transformer 백본 실험
- **데이터 큐레이션 파이프라인**: 두 가지 파이프라인으로 (1) 인간 주석 기반 physical common sense/embodied reasoning 데이터, (2) DeepSeek-R1 증류로 chain-of-thought 추적 생성
- **Physical AI SFT**: 온톨로지 정렬 데이터로 supervised fine-tuning 수행하여 기초 능력 확보
- **Physical AI RL**: 두 가지 rule-based MCQ 보상 설계 (인간 주석 MCQ + 비디오 퍼즐/시간 화살표 등 자동 생성 MCQ)로 reinforcement learning 수행
- **평가 방법론**: 물리적 이해(Space/Time/Fundamental Physics)와 embodied reasoning 능력을 별도 벤치마크로 평가하여 세분화된 분석

## Originality

- **Physical AI 온톨로지의 첫 체계적 정의**: 물리적 AI 추론의 핵심 능력을 공간-시간-물리학 범주로 처음 명확히 구조화하고, 다양한 embodiment 유형에 걸친 일반화된 embodied reasoning 프레임워크 제시
- **Rule-based RL 보상의 자동 생성**: 비디오 자체의 시공간 구조(spatiotemporal patches 셔플, 시간 화살표 판정)를 활용한 자동 MCQ 생성으로 대규모 verifiable reward 확보
- **Physical AI 벤치마크의 체계적 구축**: 온톨로지에 정렬된 포괄적 벤치마크로 물리적 AI 진전을 객관적으로 측정할 수 있는 표준 평가체계 제공
- **멀티모달 chain-of-thought로 embodied decision 생성**: 단순 action 예측이 아닌 설명적 통찰과 구체화된 의사결정을 자연언어로 함께 생성하는 통합 접근

## Limitation & Further Study

- **평가 범위의 한계**: 벤치마크가 비디오 기반 이해에 제한되며, 실제 물리 환경에서의 embodied agent 성능 검증 부재
- **데이터 큐레이션 비용**: 4M 규모의 어노테이션과 DeepSeek-R1 증류가 필요하여 재현성과 확장성의 어려움 존재
- **제한된 embodiment 다양성**: 현재 인간, 로봇 팔, 휴머노이드, 자율주행에 집중하며, 다른 물리적 상호작용 양식에 대한 일반화 불명확
- **RL 보상 설계의 수동성**: 자동 생성 MCQ는 비디오 구조 기반이므로, 더 복잡한 물리 현상에 대한 보상 설계 전략 필요
- **후속 연구 방향**: (1) 실제 로봇 플랫폼에서의 embodied agent 성능 검증, (2) 더 다양한 물리 도메인(유동역학, 변형 물체 등)으로 확장, (3) 온톨로지 자체의 완성도 평가 및 보정 메커니즘 개발, (4) 더 효율적인 RL 보상 자동 생성 방법 탐색

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Cosmos-Reason1은 물리적 AI 추론의 근본적인 개념화에서부터 벤치마크 구축, 모델 학습까지 일관성 있게 접근한 포괄적 연구입니다. 물리 상식과 embodied reasoning을 위한 첫 체계적 온톨로지 정의와 rule-based RL 보상의 자동 생성이라는 두 가지 주요 기여가 돋보이며, 오픈소스 공개로 물리적 AI 커뮤니티에 즉각적인 영향을 미칠 가능성이 높습니다.

## Related Papers

- 🔗 후속 연구: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — Cosmos-Reason1의 물리적 상식 추론과 CoT-VLA의 시각적 chain-of-thought는 모두 VLA 모델의 추론 능력 강화를 위한 보완적 접근법이다.
- 🔄 다른 접근: [[papers/1364_Diffusion-VLA_Generalizable_and_Interpretable_Robot_Foundati/review]] — Cosmos-Reason1의 물리적 AI 추론과 Diffusion-VLA의 추론-행동 통합은 VLA 모델에서 추론 능력 구현의 서로 다른 방법론이다.
- 🏛 기반 연구: [[papers/1439_IPR-1_Interactive_Physical_Reasoner/review]] — IPR-1의 인터랙티브 물리적 추론은 Cosmos-Reason1의 구체화된 추론 능력에 기초적인 물리 이해 프레임워크를 제공한다.
- 🏛 기반 연구: [[papers/1580_Streaming_Flow_Policy_Simplifying_diffusionflow-matching_pol/review]] — 물리적 상식과 추론 능력이 Streaming Flow Policy의 실시간 로봇 제어에 필요한 기초적 이해를 제공합니다.
- 🔗 후속 연구: [[papers/1343_Cosmos-Reason1_From_Physical_Common_Sense_To_Embodied_Reason/review]] — Physical AI SFT와 RL 학습 방법론이 embodied reasoning 능력을 강화하는 새로운 훈련 패러다임을 제시합니다.
- 🏛 기반 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — 구체화된 멀티모달 언어 모델의 기초적인 개념과 접근법을 제공합니다.
- 🔄 다른 접근: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — 비전-언어-액션 추론을 위한 다른 강화 시각적 추론 접근 방식입니다.
- 🔄 다른 접근: [[papers/1439_IPR-1_Interactive_Physical_Reasoner/review]] — 둘 다 물리 추론을 다루지만 interactive world model vs common sense reasoning이라는 다른 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1614_VL-Nav_A_Neuro-Symbolic_Approach_for_Reasoning-based_Vision-/review]] — physical common sense reasoning이 neuro-symbolic VLN의 추론 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — CoT-VLA의 시각적 chain-of-thought와 Cosmos-Reason1의 물리적 추론은 VLA 모델의 단계별 추론 능력을 상호 보완적으로 강화한다.
- 🔄 다른 접근: [[papers/1364_Diffusion-VLA_Generalizable_and_Interpretable_Robot_Foundati/review]] — Diffusion-VLA의 reasoning injection과 Cosmos-Reason1의 물리적 추론은 VLA 모델 추론 능력 구현의 서로 다른 방법론이다.
- 🔄 다른 접근: [[papers/1383_EmbSpatial-Bench_Benchmarking_Spatial_Understanding_for_Embo/review]] — embodied AI의 공간 추론 능력을 physical common sense 관점에서 평가하는 다른 접근법입니다.
