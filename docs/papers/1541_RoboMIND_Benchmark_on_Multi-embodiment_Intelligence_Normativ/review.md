---
title: "1541_RoboMIND_Benchmark_on_Multi-embodiment_Intelligence_Normativ"
authors:
  - "Kun Wu"
  - "Chengkai Hou"
  - "Jiaming Liu"
  - "Zhengping Che"
  - "Xiaozhu Ju"
date: "2024.12"
doi: ""
arxiv: ""
score: 4.0
essence: "RoboMIND는 4종류의 로봇 embodiment을 통해 수집된 107k개의 demonstration trajectory로 구성된 대규모 통합 로봇 조작 데이터셋으로, 통일된 데이터 수집 표준과 5k개의 failure case를 포함한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_AI_Architectures"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Robotic_Interaction_Datasets"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wu et al._2024_RoboMIND Benchmark on Multi-embodiment Intelligence Normative Data for Robot Manipulation.pdf"
---

# RoboMIND: Benchmark on Multi-embodiment Intelligence Normative Data for Robot Manipulation

> **저자**: Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, Shichao Fan, Xinhua Wang, Fei Liao, Zhen Zhao, Guangyu Li, Zhao Jin, Lecheng Wang, Jilei Mao, Ning Liu, Pei Ren, Qiang Zhang, Yaoxu Lyu, Mengzhen Liu, Jingyang He, Yulin Luo, Zeyu Gao, Chenxuan Li, Chenyang Gu, Yankai Fu, Di Wu, Xingyu Wang, Sixiang Chen, Zhenyu Wang, Pengju An, Siyuan Qian, Shanghang Zhang, Jian Tang | **날짜**: 2024-12-18 | **URL**: [https://arxiv.org/abs/2412.13877](https://arxiv.org/abs/2412.13877)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of RoboMIND. We introduce RoboMIND (Multi-embodiment Intelligence Normative Data for Robot Manipulation*

RoboMIND는 4종류의 로봇 embodiment을 통해 수집된 107k개의 demonstration trajectory로 구성된 대규모 통합 로봇 조작 데이터셋으로, 통일된 데이터 수집 표준과 5k개의 failure case를 포함한다.

## Motivation

- **Known**: 로봇 조작 정책의 일반화를 위해서는 다양한 작업, 환경, 로봇 타입을 포함하는 대규모 데이터셋이 필수적이다. 기존 로봇 데이터셋들은 개별 연구실에서 서로 다른 수집 표준으로 구축되어 있다.
- **Gap**: 기존 데이터셋들은 단일 로봇 타입에 중심을 두거나 비일관된 데이터 수집 표준을 사용하고 있으며, failure case에 대한 상세한 annotation과 digital twin 환경이 부족하다.
- **Why**: 통일된 표준으로 수집된 다양한 embodiment의 고품질 데이터는 일반화 성능이 우수한 조작 정책 학습과 교차 로봇 전이 학습을 가능하게 한다.
- **Approach**: Franka Emika Panda, UR5e, AgileX dual-arm robot, X-Humanoid 로봇에 대해 human teleoperation을 통해 통일된 프로토콜로 데이터를 수집하고, Isaac Sim에서 digital twin 환경을 구축하여 추가 학습 데이터 생성을 용이하게 했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of RoboMIND. We introduce RoboMIND (Multi-embodiment Intelligence Normative Data for Robot Manipulation*

- **대규모 다중 embodiment 데이터셋**: 479개의 다양한 작업과 96개의 객체 클래스를 포함한 107k trajectory, 305.5시간의 상호작용 데이터를 통일된 플랫폼에서 수집
- **Failure case 주석**: 5k개의 real-world failure demonstration에 상세한 원인 주석을 제공하여 RLHF 기반 정책 학습 지원
- **Digital twin 환경**: Isaac Sim에서 real-world task와 asset을 복제하여 저비용 추가 데이터 수집 및 효율적 평가 가능
- **높은 성능과 일반화**: Vision-Language-Action (VLA) 모델을 통해 높은 조작 성공률과 강력한 일반화 능력 달성
- **포괄적 멀티모달 정보**: RGB-D multi-view observations, proprioceptive state information, linguistic task descriptions를 포함

## How

![Figure 4](figures/fig4.webp)

*Fig. 4: We define 8 quality assurance criteria in the data collection process. Touch Excess: Unnecessary contact with ob*

- Human teleoperation을 통해 자연스러운 인간의 동작 패턴을 포착하여 로봇으로 매핑
- Franka Emika Panda, X-Humanoid Tien Kung, AgileX Cobot Magic V2.0, UR5e의 4종류 로봇으로부터 다양한 embodiment 데이터 수집
- 질 보증을 위해 8개의 QA 기준을 데이터 수집 과정에 정의하여 적용
- 10k개 trajectory에 대해 frame-level 상세 주석 제공
- 다양한 imitation learning 방법과 state-of-the-art VLA 모델을 사용하여 데이터셋 품질 검증
- Single-task와 multi-task 시나리오 모두에서 광범위한 실험 수행

## Originality

- **통일된 멀티 embodiment 수집**: 기존 Open X-Embodiment과 달리 동일한 표준 프로토콜을 따르는 단일 플랫폼에서 4종류 로봇의 데이터를 수집한 첫 시도
- **Failure case 상세 주석**: Real-world failure trajectory에 대한 원인 주석을 포함하여 negative learning 활용 가능
- **Humanoid 로봇과 dexterous hand 통합**: Dual dexterous hand를 갖춘 humanoid robot 데이터를 대규모로 포함한 최초
- **Digital twin 동시 구축**: Real-world task 기반 digital twin 환경을 함께 제공하여 시뮬레이션-현실 간 학습 가능

## Limitation & Further Study

- **환경 제약**: 실험실 환경에서만 수집되어 극한 환경이나 예상 외 시나리오에 대한 일반화 제한 가능
- **Linguistic task description 정확도**: 자동 또는 반자동으로 생성된 설명의 품질에 따른 VLA 모델 성능 변동 가능성
- **Embodiment 간 정보 전이**: 상이한 kinematic structure의 로봇 간 정책 전이 성능이 제한될 수 있음
- **Real-to-sim gap**: Digital twin 환경의 physics simulation 정확도 편차로 인한 현실 적용 시 성능 저하 가능
- **후속 연구**: (1) 더 다양한 환경과 시나리오에서의 데이터 수집 확대, (2) Cross-embodiment policy transfer 메커니즘 개발, (3) Failure case로부터의 자동 학습 알고리즘 개발 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RoboMIND는 통일된 수집 표준으로 구축된 최대 규모의 멀티 embodiment 로봇 데이터셋으로서, failure case 주석과 digital twin 환경을 포함하여 일반화 가능한 로봇 조작 정책 학습을 위한 중요한 자원을 제공한다. 데이터셋의 규모, 다양성, 고품질성에서 기존 연구들을 크게 능가하며 후속 로봇 학습 연구에 상당한 영향을 미칠 것으로 예상된다.

## Related Papers

- 🏛 기반 연구: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Open X-Embodiment의 다중 로봇 데이터셋 구축 경험이 RoboMIND의 multi-embodiment 벤치마크 설계 방법론의 기반이다.
- 🔗 후속 연구: [[papers/1372_DROID_A_Large-Scale_In-The-Wild_Robot_Manipulation_Dataset/review]] — DROID 데이터셋의 in-the-wild 수집 방식이 RoboMIND의 다중 embodiment 환경으로 확장되어 더 포괄적인 벤치마크를 구성한다.
- 🔄 다른 접근: [[papers/1346_Cross-Platform_Scaling_of_Vision-Language-Action_Models_from/review]] — RoboMIND와 cross-platform VLA scaling은 모두 다중 로봇 플랫폼을 다루지만 데이터셋과 모델 확장이라는 다른 관점에서 접근한다.
- 🔄 다른 접근: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — RoboMIND와 BridgeData V2 모두 대규모 로봇 학습 데이터셋이지만 다중 embodiment와 단일 플랫폼이라는 다른 접근법을 가집니다.
- 🔗 후속 연구: [[papers/1536_RoboBrain_A_Unified_Brain_Model_for_Robotic_Manipulation_fro/review]] — 다중 embodiment 데이터는 RoboBrain과 같은 통합 뇌 모델이 다양한 로봇 플랫폼에서 일반화될 수 있게 합니다.
- 🏛 기반 연구: [[papers/1306_All_Robots_in_One_A_New_Standard_and_Unified_Dataset_for_Ver/review]] — 통일된 다중 로봇 데이터셋 표준은 모든 로봇을 하나로 통합하는 비전과 언어 데이터셋의 기반이 됩니다.
- 🔗 후속 연구: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Open X-Embodiment 데이터셋의 다중 로봇 플랫폼 경험이 RoboMIND의 multi-embodiment 벤치마크 설계에 직접적인 확장 기반을 제공한다.
- 🏛 기반 연구: [[papers/1536_RoboBrain_A_Unified_Brain_Model_for_Robotic_Manipulation_fro/review]] — ShareRobot 대규모 데이터셋은 RoboMIND와 같은 다중 embodiment 데이터 수집 표준에 중요한 참조점을 제공합니다.
