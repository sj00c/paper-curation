---
title: "1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A"
authors:
  - ""
  - ""
  - "Arslan Ali"
  - "Junjie Bai"
  - "Maciej Bala"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "Cosmos-Predict2.5는 flow-based architecture 기반의 세계 시뮬레이션 기초 모델로, Text2World, Image2World, Video2World 생성을 단일 모델에 통합하여 로보틱스와 자율주행 시스템을 위한 합성 데이터 생성과 폐루프 시뮬레이션을 가능하게 한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/NVIDIA et al._2025_World Simulation with Video Foundation Models for Physical AI.pdf"
---

# World Simulation with Video Foundation Models for Physical AI

> **저자**: , , Arslan Ali, Junjie Bai, Maciej Bala, Yogesh Balaji, Aaron Blakeman, Tiffany Cai, Jiaxin Cao, Tianshi Cao, Elizabeth Cha, Yu-Wei Chao, Prithvijit Chattopadhyay, Mike Chen, Yongxin Chen, Yu Chen, Shuai Cheng, Yin Cui, Jenna Diamond, Yifan Ding, Jiaojiao Fan, Linxi Fan, Liang Feng, Francesco Ferroni, Sanja Fidler, Xiao Fu, Ruiyuan Gao, Yunhao Ge, Jinwei Gu, Aryaman Gupta, Siddharth Gururani, Imad El Hanafi, Ali Hassani, Zekun Hao, Jacob Huffman, Joel Jang, Pooya Jannaty, Jan Kautz, Grace Lam, Xuan Li, Zhaoshuo Li, Maosheng Liao, Chen-Hsuan Lin, Tsung-Yi Lin, Yen-Chen Lin, Huan Ling, Ming-Yu Liu, Xian Liu, Yifan Lu, Alice Luo, Qianli Ma, Hanzi Mao, Kaichun Mo, Seungjun Nah, Yashraj Narang, Abhijeet Panaskar, Lindsey Pavao, Trung Pham, Morteza Ramezanali, Fitsum Reda, Scott Reed, Xuanchi Ren, Haonan Shao, Yue Shen, Stella Shi, Shuran Song, Bartosz Stefaniak, Shangkun Sun, Shitao Tang, Sameena Tasmeen, Lyne Tchapmi, Wei-Cheng Tseng, Jibin Varghese, Andrew Z. Wang, Hao Wang, Haoxiang Wang, Heng Wang, Ting-Chun Wang, Fangyin Wei, Jiashu Xu, Dinghao Yang, Xiaodong Yang, Haotian Ye, Seonghyeon Ye, Xiaohui Zeng, Jing Zhang, Qinsheng Zhang, Kaiwen Zheng, Andrew Zhu, Yuke Zhu | **날짜**: 2025-10-28 | **URL**: [https://arxiv.org/abs/2511.00062](https://arxiv.org/abs/2511.00062)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overall architecture of [Cosmos-Predict2.5]. As shown on the right, in the latent space, the model*

Cosmos-Predict2.5는 flow-based architecture 기반의 세계 시뮬레이션 기초 모델로, Text2World, Image2World, Video2World 생성을 단일 모델에 통합하여 로보틱스와 자율주행 시스템을 위한 합성 데이터 생성과 폐루프 시뮬레이션을 가능하게 한다.

## Motivation

- **Known**: Physical AI 시스템의 안전한 훈련을 위해서는 고품질의 시각적 세계 시뮬레이터가 필요하며, 이전 세대인 Cosmos-Predict1은 diffusion 기반 비디오 세계 모델을 제시했다.
- **Gap**: 기존 모델은 아키텍처 복잡성, 텍스트 표현 제한, 그리고 물리 AI 도메인에 대한 특화 부족으로 인해 시뮬레이션 충실도와 지시 정렬에서 개선 여지가 있다.
- **Why**: 고품질의 합성 데이터와 시뮬레이션은 실제 환경에서의 위험성과 비용을 줄이면서 embodied intelligence를 대규모로 확장하는 핵심이다.
- **Approach**: 200M 큐레이션된 비디오 클립으로 사전 훈련하고, supervised fine-tuning과 reinforcement learning 기반 post-training으로 정제하며, Cosmos-Reason1 VLM과 통합하여 더 풍부한 텍스트 기반 제어를 제공한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: Domain-specific SFT training improves the performance of the pretrained model on each domain.*

- **통합 아키텍처**: Text2World, Image2World, Video2World 생성을 단일 flow-based 모델에 통합
- **성능 향상**: Cosmos-Predict1 대비 비디오 품질과 지시 정렬에서 상당한 개선
- **모델 규모**: 2B와 14B 두 가지 규모의 모델 제공
- **Cosmos-Transfer2.5**: 3.5배 더 작으면서 더 높은 충실도의 Sim2Real/Real2Real 변환 프레임워크
- **장시간 생성**: 강건한 long-horizon 비디오 생성 능력
- **다중 응용**: 로봇 정책 학습, 자율주행 시뮬레이션, VLA 훈련용 합성 데이터, action-conditioned 세계 생성 지원

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Our video curation pipeline transforms raw, unstructured video data from diverse real-world sources*

- 7단계 비디오 큐레이션 파이프라인: shot 분할, transcoding, 크로핑, 필터링, 캡셔닝, 의미론적 중복 제거, sharding
- 로보틱스, 자율주행, 스마트 공간, 인간 동역학, 물리 등 도메인별 특화 데이터 수집 및 처리
- Flow matching 기반 architecture로 diffusion 모델 대체
- Cosmos-Reason1 VLM과의 통합으로 향상된 텍스트 표현
- Model merging 기법을 활용한 사전 훈련
- Supervised fine-tuning (SFT)과 reinforcement learning 기반 post-training
- Timestep distillation으로 모델 효율화
- Control-net 스타일 Cosmos-Transfer2.5 프레임워크로 세계 변환 작업 처리

## Originality

- Flow matching으로 diffusion 모델의 계산 복잡성 개선
- 단일 모델에 Text2World, Image2World, Video2World를 통합한 설계
- Physical AI 특화 VLM (Cosmos-Reason1)과의 통합으로 향상된 제어성
- RL 기반 post-training으로 모델 정렬 개선
- Domain-specific 큐레이션과 200M 규모 데이터셋 구성
- Control-net 기반 Cosmos-Transfer2.5로 Sim2Real 변환 확장
- Closed-loop 시뮬레이션을 위한 architecture 설계

## Limitation & Further Study

- 장시간(long-horizon) 비디오 생성의 누적 오류에 대한 상세한 분석 부족
- 물리 정확도에 대한 정량적 평가 지표 제시 제한
- 실제 로봇 배포 결과에 대한 광범위한 시연 부족
- 생성된 합성 데이터의 domain gap이 실제 정책 성능에 미치는 영향에 대한 심층 분석 필요
- 계산 자원 요구사항 및 추론 속도에 대한 상세 공개 정보 부족
- 후속 연구: 더 긴 시간 범위의 안정적인 생성, 물리 시뮬레이터와의 더 깊은 통합, 추가 도메인(의료, 산업용) 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 Physical AI 시뮬레이션을 위한 통합된 flow-based 기초 모델을 제시하며, 대규모 데이터, 개선된 아키텍처, 정교한 post-training을 통해 실질적인 성능 향상을 달성했다. 오픈소스 공개로 embodied intelligence 연구의 접근성을 크게 높일 것으로 예상된다.

## Related Papers

- 🏛 기반 연구: [[papers/1407_Genie_Generative_Interactive_Environments/review]] — generative interactive environment가 world simulation foundation model의 기본 아이디어입니다.
- 🔗 후속 연구: [[papers/1604_Video_Language_Planning/review]] — video foundation model을 video language planning의 시뮬레이션 환경으로 활용할 수 있습니다.
- 🔄 다른 접근: [[papers/1452_Learning_Interactive_Real-World_Simulators/review]] — real-world simulation을 위한 서로 다른 접근법 - foundation model vs interactive learning입니다.
- 🔄 다른 접근: [[papers/1400_GAIA-1_A_Generative_World_Model_for_Autonomous_Driving/review]] — 자율주행을 위한 세계 모델링이라는 동일한 목표를 다른 아키텍처로 접근한 선행 연구이다.
- 🔗 후속 연구: [[papers/1406_Genie_Envisioner_A_Unified_World_Foundation_Platform_for_Rob/review]] — Cosmos-Predict2.5의 통합적 세계 시뮬레이션을 로보틱스 플랫폼으로 확장한 unified framework이다.
- 🏛 기반 연구: [[papers/1581_Structured_World_Models_from_Human_Videos/review]] — Human video에서 structured world model을 학습하는 기본 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1360_Diffusion_Models_Are_Real-Time_Game_Engines/review]] — 실시간 게임 엔진으로서의 diffusion model이라는 유사한 실시간 시뮬레이션 접근법이다.
- 🧪 응용 사례: [[papers/1517_PointWorld_Scaling_3D_World_Models_for_In-The-Wild_Robotic_M/review]] — Cosmos-Predict2.5의 3D world modeling을 실제 로보틱스 환경에서 적용할 수 있는 구체적 방법을 제시한다.
- 🔄 다른 접근: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — 둘 다 비디오 생성 기반 시뮬레이션을 다루지만, Cosmos는 세계 시뮬레이션에, GR-1은 로봇 조작에 특화되어 있다.
- 🔄 다른 접근: [[papers/1355_DreamDojo_A_Generalist_Robot_World_Model_from_Large-Scale_Hu/review]] — DreamDojo의 인간 동영상 기반 세계 모델과 비디오 foundation model 기반 세계 시뮬레이션은 영상 데이터 활용의 서로 다른 접근법이다.
- 🔗 후속 연구: [[papers/1400_GAIA-1_A_Generative_World_Model_for_Autonomous_Driving/review]] — video foundation model을 물리적 행동 예측에 활용하는 GAIA-1의 접근법을 일반화했다.
- 🏛 기반 연구: [[papers/1384_EnerVerse_Envisioning_Embodied_Future_Space_for_Robotics_Man/review]] — World Simulation with Video Foundation Models의 비디오 기반 물리 시뮬레이션이 EnerVerse의 video generation과 4D Gaussian Splatting 결합에 기초가 된다.
- 🏛 기반 연구: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — InternVLA-A1의 시각적 예측 능력이 World Simulation with Video Foundation Models의 물리적 추론 기반 위에 구축된다.
- 🔗 후속 연구: [[papers/1452_Learning_Interactive_Real-World_Simulators/review]] — 비디오 파운데이션 모델을 활용한 물리적 상호작용 시뮬레이션으로 UniSim의 접근법을 더 발전시켰다.
- 🔗 후속 연구: [[papers/1455_Learning_Universal_Policies_via_Text-Guided_Video_Generation/review]] — 텍스트 기반 비디오 생성을 통한 정책 학습이 비디오 foundation model의 물리적 추론 능력을 로봇 제어에 직접 활용하는 방식으로 발전한다.
- 🏛 기반 연구: [[papers/1481_Motus_A_Unified_Latent_Action_World_Model/review]] — Motus의 world model 기반이 되는 video foundation model을 활용한 물리적 AI
- 🔄 다른 접근: [[papers/1517_PointWorld_Scaling_3D_World_Models_for_In-The-Wild_Robotic_M/review]] — 3D world model에서 point flow based unified representation vs video foundation model이라는 서로 다른 장면 표현 및 시뮬레이션 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1523_Re3Sim_Generating_High-Fidelity_Simulation_Data_via_3D-Photo/review]] — Video foundation models를 활용한 world simulation 기술이 Re3Sim의 고충실도 시뮬레이션 환경 구축의 핵심 기반 기술이다.
- 🔗 후속 연구: [[papers/1527_Real2Render2Real_Scaling_Robot_Data_Without_Dynamics_Simulat/review]] — 비디오 기반 데이터 생성은 비디오 파운데이션 모델을 활용한 물리적 AI 월드 시뮬레이션과 연결됩니다.
- 🔗 후속 연구: [[papers/1573_SimpleVLA-RL_Scaling_VLA_Training_via_Reinforcement_Learning/review]] — video foundation model 기반 시뮬레이션을 VLA-RL 학습의 데이터 생성에 활용할 수 있습니다.
- 🔄 다른 접근: [[papers/1552_RoboTwin_Dual-Arm_Robot_Benchmark_with_Generative_Digital_Tw/review]] — 로봇을 위한 세계 모델링에서 RoboTwin은 generative digital twin으로, World Simulation은 video foundation model로 접근한다.
- 🔗 후속 연구: [[papers/1581_Structured_World_Models_from_Human_Videos/review]] — SWIM의 구조화된 world model 개념을 확장하여 flow-based architecture로 더 정교한 세계 시뮬레이션을 구현한다.
- 🏛 기반 연구: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — 비디오 foundation model을 통한 세계 시뮬레이션 연구가 TriVLA의 Video Diffusion Model 기반 미래 예측 시스템의 이론적 기반이다.
- 🔗 후속 연구: [[papers/1598_Unified_Video_Action_Model/review]] — video foundation model을 unified video action model로 확장한 응용 연구입니다.
- 🧪 응용 사례: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — 비디오 foundation model을 활용한 세계 시뮬레이션으로 UniVLA의 world model 통합을 물리적 AI 응용으로 확장합니다.
- 🔄 다른 접근: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — World Simulation with Video Foundation Models은 GR-1과 유사한 비디오 기반 접근이지만 물리적 행동보다 시뮬레이션에 중점을 둡니다.
- 🏛 기반 연구: [[papers/1626_WHALE_Towards_Generalizable_and_Scalable_World_Models_for_Em/review]] — 비디오 foundation model을 통한 물리적 AI 시뮬레이션이 WHALE의 확장 가능한 world model 설계에 기반 기술을 제공한다.
- 🔗 후속 연구: [[papers/1631_World_Models/review]] — 기본적인 생성형 world model 개념을 비디오 foundation model과 물리적 AI 액션을 위한 현대적 프레임워크로 발전시켰다.
- 🧪 응용 사례: [[papers/1603_V-JEPA_2_Self-Supervised_Video_Models_Enable_Understanding_P/review]] — 자기지도학습 비디오 모델을 물리적 AI를 위한 세계 시뮬레이션에 적용하여 V-JEPA 2의 실제 활용을 보여줍니다.
- 🏛 기반 연구: [[papers/1604_Video_Language_Planning/review]] — video foundation model이 video language planning의 text-to-video 생성 기반이 됩니다.
- 🔗 후속 연구: [[papers/1347_D2E_Scaling_Vision-Action_Pretraining_on_Desktop_Data_for_Tr/review]] — Video Foundation Models의 물리적 세계 시뮬레이션 능력이 D2E의 데스크톱-로봇 전이 학습에 중요한 표현 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1387_EWMBench_Evaluating_Scene_Motion_and_Semantic_Quality_in_Emb/review]] — World Simulation with Video Foundation Models의 세계 모델 시뮬레이션 기법이 EWMBench의 Embodied World Models 평가 기준 설계의 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1360_Diffusion_Models_Are_Real-Time_Game_Engines/review]] — 물리적 AI를 위한 비디오 기초 모델을 사용한 다른 월드 시뮬레이션 접근법입니다.
