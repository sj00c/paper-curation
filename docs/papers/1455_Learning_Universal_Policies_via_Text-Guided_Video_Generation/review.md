---
title: "1455_Learning_Universal_Policies_via_Text-Guided_Video_Generation"
authors:
  - "Yilun Du"
  - "Mengjiao Yang"
  - "Bo Dai"
  - "Hanjun Dai"
  - "Ofir Nachum"
date: "2023.01"
doi: ""
arxiv: ""
score: 4.0
essence: "텍스트 조건부 video generation을 사용하여 다양한 환경에서 작동하는 범용 정책을 학습하는 방법을 제안하며, 현재 이미지와 텍스트 목표 설명으로부터 미래 프레임 시퀀스를 생성한 후 inverse dynamics model로 액션을 추출한다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_AI_Architectures"
  - "sub/LLM_Task_Planning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Du et al._2023_Learning Universal Policies via Text-Guided Video Generation.pdf"
---

# Learning Universal Policies via Text-Guided Video Generation

> **저자**: Yilun Du, Mengjiao Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Joshua B. Tenenbaum, Dale Schuurmans, Pieter Abbeel | **날짜**: 2023-01-31 | **URL**: [https://arxiv.org/abs/2302.00111](https://arxiv.org/abs/2302.00111)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Text-Conditional Video Generation as Universal Policies. Text-conditional video generations*

텍스트 조건부 video generation을 사용하여 다양한 환경에서 작동하는 범용 정책을 학습하는 방법을 제안하며, 현재 이미지와 텍스트 목표 설명으로부터 미래 프레임 시퀀스를 생성한 후 inverse dynamics model로 액션을 추출한다.

## Motivation

- **Known**: 텍스트 기반 이미지 합성 모델들이 뛰어난 조합적 일반화 능력을 보이고 있으며, 강화학습에서 다양한 작업을 수행하는 범용 에이전트 구축이 중요한 목표이다.
- **Gap**: 서로 다른 상태-액션 공간을 가진 환경들 간의 지식 공유와 일반화가 어렵고, 환경별로 서로 다른 reward function 설계가 필요하다는 문제가 있다.
- **Why**: 범용 정책 학습은 다양한 로봇 작업과 환경에 확장 가능한 AI 에이전트 구축을 가능하게 하며, 인터넷 규모의 video 데이터를 활용한 지식 전이를 통해 실제 로봇 제어에 적용할 수 있다.
- **Approach**: Unified Predictive Decision Process (UPDP)라는 새로운 추상화를 제안하여 이미지를 환경 간 범용 인터페이스로, 텍스트를 작업 지정자로 사용하고, video diffusion 모델을 통해 텍스트 조건부 video generation을 수행한 후 액션을 회귀한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Combinatorial Video Generation. Generated videos for unseen language goals at test time.*

- **조합적 일반화**: 텍스트의 조합적 특성을 활용하여 미학습한 새로운 객체 배치와 기하학적 관계에 일반화 가능
- **다중 작업 학습**: video prediction으로 다양한 언어 조건부 작업 간 학습이 가능하며 테스트 시간에 파인튜닝 없이 새로운 작업에 일반화
- **계층적 및 조향 가능한 계획**: 희소한 프레임 시퀀스부터 세부 계획으로 정제하는 계층적 생성과 테스트 시간 제약 조건 추가를 통한 계획 조정 가능
- **인터넷 규모 지식 전이**: 대규모 텍스트-비디오 데이터셋으로 사전학습된 model을 통해 현실적인 로봇 동작 합성 가능

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Given an input observation and text instruction, we*

- UPDP 추상화 도입: 이미지 공간 X, 텍스트 공간 C, 수평선 H, 조건부 video generator ρ(·|x₀, c)로 정의
- Video diffusion 모델 활용: 현재 이미지 프레임과 텍스트 목표 설명을 조건으로 하여 H-step 이미지 시퀀스 생성
- Inverse dynamics 모델: 생성된 비디오로부터 underlying 액션 추출
- 오프라인 RL 설정: 기존 경험 데이터셋 D로부터 ρ와 정책 π 학습
- Multi-task 학습: 다양한 작업의 (이미지, 액션, 텍스트 설명) 데이터로 unified 정책 훈련
- 계층적 샘플링: 희소 프레임을 먼저 생성한 후 상세화하는 두 단계 생성 프로세스

## Originality

- MDP 대신 UPDP라는 새로운 추상화 프레임워크 제안으로 환경 다양성 문제 해결
- Video를 범용 인터페이스로 사용하여 서로 다른 상태-액션 공간을 가진 환경들을 통합
- Planning과 액션 선택을 분리하여 환경-무종속 계획 가능
- 인터넷 규모 video 데이터를 실제 로봇 제어에 활용하는 새로운 지식 전이 경로 제시

## Limitation & Further Study

- 오프라인 RL 설정으로 제한되어 온라인 학습이나 환경과의 상호작용 미지원
- Inverse dynamics 모델의 정확도에 의존하므로 액션 추출 오류 누적 가능
- Video generation의 계산 비용이 높을 수 있어 실시간 제어 적용에 한계
- 인터넷 video 데이터의 다양성이 특정 로봇 형태나 환경에는 일반화 어려울 수 있음
- **후속연구**: 온라인 강화학습과의 결합, 더 효율적인 액션 추출 방법, 다양한 로봇 플랫폼에 대한 적응 메커니즘 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 video generation을 통한 범용 정책 학습이라는 창의적인 접근으로 환경 다양성과 reward 설계 문제를 우아하게 해결하며, 조합적 일반화와 인터넷 규모 지식 전이를 통해 강화학습 분야에 상당한 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1400_GAIA-1_A_Generative_World_Model_for_Autonomous_Driving/review]] — 둘 다 text-guided video generation을 통한 정책 학습이지만 범용적 접근 vs 자율주행 특화라는 다른 범위를 가진다.
- 🏛 기반 연구: [[papers/1604_Video_Language_Planning/review]] — Video Language Planning의 개념을 text-conditioned video generation으로 구체적으로 구현한 사례이다.
- 🔗 후속 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — large-scale video generative pre-training을 text-guided universal policy learning으로 활용한 응용이다.
- 🔗 후속 연구: [[papers/1598_Unified_Video_Action_Model/review]] — 텍스트 가이드 비디오 생성을 unified video action model로 더 체계화하고 일반화했다.
- 🔗 후속 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — 텍스트 기반 비디오 생성을 통한 정책 학습이 비디오 foundation model의 물리적 추론 능력을 로봇 제어에 직접 활용하는 방식으로 발전한다.
- 🔄 다른 접근: [[papers/1406_Genie_Envisioner_A_Unified_World_Foundation_Platform_for_Rob/review]] — 둘 다 생성 모델을 통한 로봇 행동 합성에 초점을 맞추지만, Universal Policies는 비디오 생성을, Genie Envisioner는 통합 플랫폼에 집중한다.
- 🏛 기반 연구: [[papers/1396_ForesightNav_Learning_Scene_Imagination_for_Efficient_Explor/review]] — Learning Universal Policies via Text-Guided Video Generation의 비디오 생성을 통한 정책 학습이 ForesightNav의 scene imagination 기반 탐색에 기초가 된다.
- 🔄 다른 접근: [[papers/1400_GAIA-1_A_Generative_World_Model_for_Autonomous_Driving/review]] — 둘 다 video generation을 통한 정책 학습을 다루지만 자율주행 특화 vs 범용적 접근이라는 차이가 있다.
- 🔗 후속 연구: [[papers/1604_Video_Language_Planning/review]] — text-guided video generation을 로봇 작업의 상세한 계획 생성으로 확장한 응용입니다.
