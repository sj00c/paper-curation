---
title: "1413_GraspVLA_a_Grasping_Foundation_Model_Pre-trained_on_Billion-"
authors:
  - "Shengliang Deng"
  - "Mi Yan"
  - "Songlin Wei"
  - "Haixin Ma"
  - "Yuxin Yang"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "SynGrasp-1B라는 10억 프레임 규모의 합성 데이터셋을 기반으로 GraspVLA라는 Vision-Language-Action 기반 집기 모델을 제시하며, 합성 데이터만으로 사전학습하여 실세계에서 강력한 제로샷 일반화와 소수샷 적응성을 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Dexterous_Spatial_Grasping"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Deng et al._2025_GraspVLA a Grasping Foundation Model Pre-trained on Billion-scale Synthetic Action Data.pdf"
---

# GraspVLA: a Grasping Foundation Model Pre-trained on Billion-scale Synthetic Action Data

> **저자**: Shengliang Deng, Mi Yan, Songlin Wei, Haixin Ma, Yuxin Yang, Jiayi Chen, Zhiqi Zhang, Taoyu Yang, Xuheng Zhang, Wenhao Zhang, Heming Cui, Zhizheng Zhang, He Wang | **날짜**: 2025-05-06 | **URL**: [https://arxiv.org/abs/2505.03233](https://arxiv.org/abs/2505.03233)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: GraspVLA is a grasping foundation model pre-trained exclusively on billion-scale syn-*

SynGrasp-1B라는 10억 프레임 규모의 합성 데이터셋을 기반으로 GraspVLA라는 Vision-Language-Action 기반 집기 모델을 제시하며, 합성 데이터만으로 사전학습하여 실세계에서 강력한 제로샷 일반화와 소수샷 적응성을 달성한다.

## Motivation

- **Known**: VLA 모델은 NLP/CV 분야의 파운데이션 모델 성공에 영감을 받아 개발되었으나, 기존 VLA 모델들은 비용이 많이 드는 실세계 데이터에 크게 의존하고 있다.
- **Gap**: 합성 데이터의 잠재력은 로봇 조작 학습에서 크게 과소평가되었으며, 대규모 합성 행동 데이터로만 학습한 VLA 모델의 실행 가능성이 체계적으로 탐구되지 않았다.
- **Why**: 합성 데이터는 실세계 데이터 수집의 비용과 노동 집약성을 획기적으로 줄일 수 있으며, 이를 통해 파운데이션 모델의 민주화와 접근성을 크게 향상시킬 수 있다.
- **Approach**: Progressive Action Generation이라는 통합 Chain-of-Thought 프로세스를 통해 자동회귀 지각 작업과 flow-matching 기반 행동 생성을 결합하고, 합성 데이터와 인터넷 데이터를 함께 학습하여 시뮬레이션-현실 간극을 완화하고 개방 어휘 일반화를 달성한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: GraspVLA is a grasping foundation model pre-trained exclusively on billion-scale syn-*

- **SynGrasp-1B 데이터셋**: 240개 카테고리의 10,680개 객체를 포함한 전 세계 최초의 10억 프레임 규모 로봇 집기 데이터셋 구축
- **Progressive Action Generation**: 지각 작업을 중간 단계로 취급하는 통합 Chain-of-Thought 프로세스로 합성 및 인터넷 데이터의 보완적 학습 가능
- **직접 시뮬-현실 전이**: 합성 데이터만으로 학습하여 실세계에서 직접 배포 가능하며 충돌 회복 능력을 가진 폐루프 정책 제공
- **강력한 제로샷 성능**: AnyGrasp 대비 투명 객체에서 현저히 우수하며 시뮬레이션 및 실세계 벤치마크에서 우수한 일반화 능력 입증
- **소수샷 적응성**: 사용자 선호도와 특화된 응용 시나리오(예: 컵 내부 회피, 밀집된 병 순차 집기)에 효율적으로 적응

## How

![Figure 3](figures/fig3.webp)

*Figure 3: GraspVLA consists of an autoregressive vision-language backbone and a flow-matching*

- Objaverse의 LVIS 부분집합에서 10,680개 객체 메시를 선별하고 랜덤 스케일링 및 물리적 배치를 통해 다양한 장면 생성
- Grasp synthesis 알고리즘으로 안정적인 antipodal grasps 생성 및 CuRoB 운동 계획기를 사용한 충돌 없는 궤적 계획
- 포토리얼리스틱 렌더링과 광범위한 domain randomization으로 배경, 조명, 공간, 객체 카테고리, 방해물 등의 변동 포함
- 자동회귀 vision-language backbone과 flow-matching 기반 행동 생성 모듈을 결합한 엔드투엔드 아키텍처 설계
- 시각적 그라운딩 및 집기 자세 예측을 중간 단계로 하는 Chain-of-Thought 프로세스로 합성 및 인터넷 데이터 공동 학습

## Originality

- VLA 모델을 위한 합성 데이터만의 순수 사전학습 패러다임 제안으로 기존의 실세계 데이터 중심 접근과 근본적으로 다른 방식 제시
- Progressive Action Generation으로 지각 작업을 행동 생성의 인과적 중간 단계로 모델링하여 합성과 인터넷 데이터의 보완적 학습 가능하게 함
- 전 세계 최초의 10억 프레임 규모 합성 로봇 행동 데이터셋 구축으로 대규모 데이터 시대의 로봇 학습 기반 마련
- 개방 어휘 집기 달성을 위해 합성 데이터의 기하학적 정보와 인터넷 데이터의 의미론적 지식을 명시적으로 결합하는 설계

## Limitation & Further Study

- 현재는 집기라는 특정 조작 스킬에만 초점을 맞추고 있으며, 다른 조작 작업(예: 푸싱, 조립)으로의 확장 가능성이 미흐음
- 합성 데이터와 실세계 간의 정확한 도메인 갭 분석이 부족하며, 어떤 domain randomization 요소가 시뮬-현실 전이에 가장 중요한지 명확하지 않음
- 인터넷 데이터와의 공동 학습이 개방 어휘 성능 개선에 얼마나 기여하는지에 대한 ablation 분석의 상세함이 필요
- 후속 연구로 다양한 로봇 형태와 엔드이펙터에 대한 일반화, 동적 환경과 멀티 에이전트 시나리오 확장, 더 효율적인 소수샷 적응 메커니즘 개발이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 로봇 조작 학습을 위한 합성 데이터의 대규모 활용 가능성을 최초로 체계적으로 입증하며, 10억 프레임 규모의 고품질 데이터셋과 혁신적인 Progressive Action Generation 메커니즘을 통해 실세계 배포 가능한 강력한 기반 모델을 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1356_DexGraspVLA_A_Vision-Language-Action_Framework_Towards_Gener/review]] — 둘 다 grasping VLA 모델이지만 billion-scale synthetic data vs plug-in diffusion expert라는 다른 학습 전략을 사용한다.
- 🏛 기반 연구: [[papers/1523_Re3Sim_Generating_High-Fidelity_Simulation_Data_via_3D-Photo/review]] — 3D-prior 기반 고해상도 시뮬레이션 데이터 생성 개념을 grasping 특화 합성 데이터셋 구축에 적용했다.
- 🔗 후속 연구: [[papers/1354_Dex1B_Learning_with_1B_Demonstrations_for_Dexterous_Manipula/review]] — Dex1B의 대규모 demonstration 학습 개념을 grasping 도메인에 합성 데이터로 확장했다.
- 🔗 후속 연구: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — BridgeData V2의 대규모 로봇 데이터 개념을 합성 데이터로 확장하여 10억 프레임 규모의 집기 데이터셋을 구축한다.
- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA와 다르게 합성 데이터 사전학습에 특화된 VLA 모델로 실세계 일반화에 대한 다른 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1297_A_Real-to-Sim-to-Real_Approach_to_Robotic_Manipulation_with/review]] — keypoint 기반 접근법 대신 대규모 그래스핑 데이터로 사전 학습된 foundation model을 활용하는 다른 조작 방법론
- 🏛 기반 연구: [[papers/1356_DexGraspVLA_A_Vision-Language-Action_Framework_Towards_Gener/review]] — 대규모 그립 데이터로 사전학습된 foundation model이 손가락 그립 VLA의 기반이 됩니다.
