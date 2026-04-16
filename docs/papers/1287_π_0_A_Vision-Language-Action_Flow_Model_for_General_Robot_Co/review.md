---
title: "1287_π_0_A_Vision-Language-Action_Flow_Model_for_General_Robot_Co"
authors:
  - "Kevin Black"
  - "Noah Brown"
  - "Danny Driess"
  - "Adnan Esmail"
  - "Michael Equi"
date: "2024.10"
doi: ""
arxiv: ""
score: 4.0
essence: "π0는 사전학습된 vision-language model (VLM)을 기반으로 flow matching을 통해 연속적인 로봇 행동을 생성하는 generalist robot policy를 제안한다. 다양한 로봇 플랫폼에서 10,000시간 이상의 데이터로 사전학습한 후 미세조정을 통해 세탁물 접기, 테이블 청소, 박스 조립 등 복잡한 손작업을 수행할 수 있다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Black et al._2024_$π_0$ A Vision-Language-Action Flow Model for General Robot Control.pdf"
---

# $π_0$: A Vision-Language-Action Flow Model for General Robot Control

> **저자**: Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, Ury Zhilinsky | **날짜**: 2024-10-31 | **URL**: [https://arxiv.org/abs/2410.24164](https://arxiv.org/abs/2410.24164)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Our generalist robot policy uses a pre-trained vision-language model (VLM) backbone, as well as a diverse cross-*

π0는 사전학습된 vision-language model (VLM)을 기반으로 flow matching을 통해 연속적인 로봇 행동을 생성하는 generalist robot policy를 제안한다. 다양한 로봇 플랫폼에서 10,000시간 이상의 데이터로 사전학습한 후 미세조정을 통해 세탁물 접기, 테이블 청소, 박스 조립 등 복잡한 손작업을 수행할 수 있다.

## Motivation

- **Known**: Vision-language model은 인터넷 규모의 의미론적 지식을 보유하고 있으며, 로봇 학습에서 대규모 사전학습은 데이터 부족, 일반화, 견고성 문제를 해결할 수 있다. 최근 VLA (vision-language-action) 모델들이 자동회귀 이산화를 통해 로봇 제어를 시도하고 있다.
- **Gap**: 기존 VLA 모델들은 autoregressive discretization을 사용하여 행동을 텍스트 토큰처럼 표현하므로 연속적인 손작업의 미세한 움직임을 효과적으로 제어하기 어렵다. 또한 단일 로봇 플랫폼이나 제한된 작업에만 적용되어 generality가 부족하다.
- **Why**: 로봇이 현실 세계에서 유연하고 일반적이며 민첩한 시스템이 되려면 다양한 환경과 작업에 적응할 수 있는 generalist policy가 필수적이다. 이는 인공지능의 근본적인 문제인 물리적 상황 인식과 다목적성을 달성하는 데 중요하다.
- **Approach**: VLM 백본 위에 flow matching 기반의 action expert를 추가하여 연속 행동 분포를 생성하고, cross-embodiment training으로 다양한 로봇 플랫폼(단일팔, 쌍팔, 모바일 매니퓨레이터)의 데이터를 통합한다. 사전학습/후학습 분리 방식으로 다양성과 정확성을 모두 확보한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: π0 controls a mobile manipulator to fold laundry. Our model is pre-trained on diverse data from 7 distinct robot*

- **Cross-embodiment generalist policy**: 7개의 서로 다른 로봇 구성과 68개 작업에서 사전학습하여 다양한 로봇 플랫폼에서 작동 가능
- **Flow matching 기반 연속 행동 생성**: Action chunking과 flow matching을 결합하여 최대 50Hz 제어 주파수로 손작업 수행 가능
- **다양한 작업 수행 능력**: 직접 프롬프트로 zero-shot 수행, 언어 명령 따르기, 미세조정을 통한 새로운 기술 습득
- **복잡한 다단계 작업 달성**: 세탁물 접기, 테이블 청소, 접시 전자레인지 넣기, 계란 상자에 쌓기, 박스 조립, 식료품 봉투 담기 등 수행

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Overview of our framework. We start with a pre-training mixture, which consists of both our own dexterous*

- Pre-trained VLM 백본을 로봇 제어용으로 개선하여 인터넷 규모의 의미론적 지식 상속
- Flow matching (diffusion의 변형)을 통해 복잡한 연속 행동 분포 모델링
- Action expert를 VLM에 부착하여 flow-based 출력 생성
- 10,000시간 이상의 다양한 로봇 데이터로 사전학습 (pre-training)
- 고품질 큐레이션 데이터로 미세조정 (post-training) 수행
- Action chunking 아키텍처를 사용하여 정확하고 유연한 제어 실현
- 고레벨 VLM policy와 결합하여 시간적으로 확장된 복잡 작업 수행

## Originality

- VLM 기반 로봇 정책에 flow matching을 처음으로 결합하여 연속 행동 표현 개선
- Cross-embodiment training으로 여러 로봇 타입(단일팔, 쌍팔, 모바일 매니퓰레이터)의 이질적 action space 통합
- Pre-training/post-training 분리를 통해 다양성과 정확성의 균형 달성 (기존 VLA 모델은 단순 미세조정만 사용)
- Action expert 설계로 표준 VLM을 연속 행동 생성으로 확장하는 novel 아키텍처 제시

## Limitation & Further Study

- 10,000시간 규모의 대규모 데이터셋 구축과 다양한 로봇 플랫폼 수집의 현실적 어려움으로 재현성 제한 가능
- Flow matching의 계산 복잡도가 실시간 성능에 미치는 영향에 대한 자세한 분석 부족
- 평가 대상 작업들이 주로 손작업 중심이므로 이동, 항법 등 다른 로봇 기능에 대한 일반화 가능성 미검증
- 미세조정 데이터 크기와 품질 요구사항에 대한 정량적 분석 및 최소 필요량 제시 부족
- 후속 연구는 더 다양한 로봇 체계와 환경에서의 성능 검증, 도메인 간 전이 학습 메커니즘 분석, 장기 자율성 및 안전성 강화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: π0는 flow matching을 VLM 기반 로봇 정책에 처음 적용하고 cross-embodiment 학습으로 다양한 로봇 플랫폼을 통합하여 generalist robot foundation model의 새로운 기준을 제시한다. 10,000시간 이상의 대규모 데이터와 정교한 학습 레시피를 통해 실제 세계에서 복잡한 손작업을 수행 가능함을 보여주며, 로봇 학습의 확장성과 실용성을 크게 향상시키는 중요한 기여이다.

## Related Papers

- 🔄 다른 접근: [[papers/1358_DexVLA_Vision-Language_Model_with_Plug-In_Diffusion_Expert_f/review]] — π0의 flow matching 기반 행동 생성과 DexVLA의 diffusion expert 접근법은 VLA 모델에서 행동 생성의 서로 다른 방법론이다.
- 🔗 후속 연구: [[papers/1318_Being-H05_Scaling_Human-Centric_Robot_Learning_for_Cross-Emb/review]] — π0의 generalist robot policy와 Being-H0.5의 cross-embodiment 일반화는 모두 범용 로봇 정책을 지향한다.
- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 오픈소스 VLA 모델은 π0의 vision-language-action 정책 설계에 기초 프레임워크를 제공한다.
- ⚖️ 반론/비판: [[papers/1336_CogACT_A_Foundational_Vision-Language-Action_Model_for_Syner/review]] — cognition과 action을 분리하는 접근법으로 π0의 통합적 flow matching 방식과 대조된다.
- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — 연속적 행동 생성을 위한 diffusion 기반 정책 학습의 기초 이론을 제공한다.
- 🔗 후속 연구: [[papers/1494_NORA-15_A_Vision-Language-Action_Model_Trained_using_World_M/review]] — π₀의 flow-based action 생성 아키텍처를 NORA-1.5가 world model과 결합하여 발전시킨다.
- 🔄 다른 접근: [[papers/1603_V-JEPA_2_Self-Supervised_Video_Models_Enable_Understanding_P/review]] — 둘 다 vision-based robot control을 다루지만 V-JEPA 2는 self-supervised video learning을, π_0는 flow model을 사용한다.
- 🔗 후속 연구: [[papers/1318_Being-H05_Scaling_Human-Centric_Robot_Learning_for_Cross-Emb/review]] — Being-H0.5의 cross-embodiment 일반화와 π0의 generalist robot policy는 범용 로봇 정책의 서로 다른 확장 방향이다.
- ⚖️ 반론/비판: [[papers/1336_CogACT_A_Foundational_Vision-Language-Action_Model_for_Syner/review]] — 통합된 flow matching과 달리 cognition과 action을 명시적으로 분리하는 대조적 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1358_DexVLA_Vision-Language_Model_with_Plug-In_Diffusion_Expert_f/review]] — DexVLA의 diffusion expert 통합과 π0의 flow matching 행동 생성은 VLA 모델에서 행동 생성의 서로 다른 확률적 접근법이다.
