---
title: "1306_All_Robots_in_One_A_New_Standard_and_Unified_Dataset_for_Ver"
authors:
  - "Zhiqiang Wang"
  - "Hao Zheng"
  - "Yunshuang Nie"
  - "Wenjun Xu"
  - "Qingwei Wang"
date: "2024.08"
doi: ""
arxiv: ""
score: 4.0
essence: "ARIO는 로봇 embodied AI 에이전트 학습을 위한 통합 데이터 표준과 약 300만 에피소드의 대규모 데이터셋으로, 258개 로봇 시리즈와 5가지 감각 모달리티를 포함하여 범용적이고 강건한 로봇 에이전트 개발을 가능하게 한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2024_All Robots in One A New Standard and Unified Dataset for Versatile, General-Purpose Embodied Agents.pdf"
---

# All Robots in One: A New Standard and Unified Dataset for Versatile, General-Purpose Embodied Agents

> **저자**: Zhiqiang Wang, Hao Zheng, Yunshuang Nie, Wenjun Xu, Qingwei Wang, Hua Ye, Zhe Li, Kaidong Zhang, Xuewen Cheng, Wanxi Dong, Chang Cai, Liang Lin, Feng Zheng, Xiaodan Liang | **날짜**: 2024-08-20 | **URL**: [https://arxiv.org/abs/2408.10899](https://arxiv.org/abs/2408.10899)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. All robots in one.*

ARIO는 로봇 embodied AI 에이전트 학습을 위한 통합 데이터 표준과 약 300만 에피소드의 대규모 데이터셋으로, 258개 로봇 시리즈와 5가지 감각 모달리티를 포함하여 범용적이고 강건한 로봇 에이전트 개발을 가능하게 한다.

## Motivation

- **Known**: 기존 embodied AI 데이터셋들(RoboNet, RT-1, Open X-Embodiment 등)은 특정 작업에 최적화되거나 데이터 형식이 표준화되지 않았으며, 주로 시각 데이터에만 의존하고 멀티모달 정보가 부족하다.
- **Gap**: 기존 데이터셋들은 표준화된 형식 부재, 불충분한 데이터 다양성, 불충분한 데이터 규모, 포괄적인 감각 모달리티 부재(이미지, 3D 비전, 텍스트, 촉각, 청각을 동시에 포함하는 데이터셋 없음), 시뮬레이션과 실제 데이터 결합 부족 등의 문제가 있다.
- **Why**: 범용적이고 강건한 embodied AI 에이전트 개발을 위해서는 다양한 로봇 플랫폼, 환경, 작업을 포괄하는 통일된 대규모 멀티모달 데이터셋이 필수적이며, 이를 통해 sim-to-real 전이 학습과 cross-embodiment 전이를 연구할 수 있다.
- **Approach**: ARIO 표준은 collection-series-task-episode의 4계층 계층적 구조와 타임스탬프 기반 데이터 정렬을 도입하여 다양한 로봇 타입의 제어 및 모션 데이터를 통합 형식으로 표현한다. 이 표준을 바탕으로 실제 로봇 데이터 수집, 시뮬레이션(Habitat, MuJoCo, SeaWave), 기존 오픈소스 데이터셋 변환을 통해 약 300만 에피소드의 대규모 통합 데이터셋을 구축했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. All robots in one.*

- **포괄적 감각 모달리티**: 이미지, 3D point cloud, 음성, 텍스트, 촉각 등 5가지 감각 모달리티를 통합한 최초의 대규모 데이터셋 제공
- **통합 데이터 형식**: series-task-episode 계층 구조와 타임스탬프 기반 동기화로 다양한 로봇 타입(bimanual, single-arm, navigational, humanoid)과 제어 객체를 표준화된 형식으로 표현
- **대규모 다양한 데이터**: 258개 로봇 시리즈, 321,064개 작업, 약 300만 에피소드로 구성된 현존 최대 규모의 embodied AI 데이터셋
- **시뮬레이션과 실제 데이터 결합**: 실제 로봇 수집(3,662 에피소드), 시뮬레이션(703,088 에피소드), 오픈소스 변환(2,326,438 에피소드)을 통해 sim-to-real 갭 연구 가능
- **표준화 및 정제**: 기존 오픈소스 데이터셋들을 ARIO 표준으로 정제 및 변환하여 호환성과 사용성 향상

## How

![Figure 3](figures/fig3.webp)

*Figure 3. Collection pipeline of ARIO.*

- 4계층 계층적 데이터 구조(collection → series → task → episode) 설계로 조직적인 데이터 관리
- 타임스탬프 메커니즘을 통한 다양한 센서 프레임률과 로봇 액션 빈도의 동기화
- information.yaml(시리즈 메타데이터), description.yaml(작업 메타데이터)을 통한 포괄적 문서화
- 자체 구축 로봇 플랫폼에서의 실제 데이터 수집, Habitat/MuJoCo/SeaWave 등 다양한 시뮬레이션 플랫폼 활용
- RoboNet, RT-1, BC-Z 등 기존 오픈소스 데이터셋의 자동 변환 및 표준화 파이프라인
- 5가지 감각 모달리티(2D image, RGB-D, point cloud, audio, tactile, text)를 각 에피소드에서 동시 수집

## Originality

- **최초의 통합 멀티모달 embodied AI 데이터셋 표준**: 이미지, 3D 비전, 음성, 텍스트, 촉각을 동시에 포함하는 통합 표준 제시
- **타임스탬프 기반 동기화 메커니즘**: 다양한 센서와 로봇의 비동기 데이터를 정확하게 정렬하는 실용적 솔루션
- **cross-platform 데이터 변환 파이프라인**: 기존 이질적 데이터셋들을 자동으로 표준 형식으로 변환하는 대규모 정제 작업
- **sim-to-real 연구 기반 제공**: 동일 작업에 대한 시뮬레이션과 실제 데이터를 병렬로 제공하는 구조

## Limitation & Further Study

- **데이터 품질 편차**: 변환된 오픈소스 데이터셋들의 원본 품질 편차에 따른 통합 데이터셋의 일관성 문제 가능성
- **센서 모달리티 희소성**: 모든 에피소드가 5가지 모달리티를 포함하지 않을 수 있어 완전한 멀티모달 학습에 한계
- **로봇 형태학적 이질성**: 다양한 로봇 모폴로지의 제어 신호 차이에 대한 정규화 방법론 상세 설명 부족
- **벤치마크 평가 부재**: 제시된 데이터셋으로 학습한 에이전트의 성능과 일반화 능력에 대한 정량적 벤치마크 평가 결과 미제시
- **후속 연구**: (1) ARIO 기반 foundation model 학습 및 평가 벤치마크 개발, (2) 불완전한 모달리티 데이터에 대한 처리 전략 연구, (3) 시뮬레이션-실제 데이터 간 domain gap 최소화 기법 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ARIO는 embodied AI 분야의 근본적인 데이터 표준화 문제를 해결하고 최초의 포괄적 멀티모달 대규모 통합 데이터셋을 제공하여 범용 로봇 에이전트 개발에 중대한 기여를 한다. 다만 제시된 데이터셋으로 학습한 에이전트의 실제 성능 벤치마크가 부재한 점이 아쉽지만, 데이터 표준과 인프라 자체의 가치는 매우 높다.

## Related Papers

- 🔄 다른 접근: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Open X-Embodiment 데이터셋과 비교하여 더 통합된 로봇 데이터 표준을 제시한다.
- 🏛 기반 연구: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — 대규모 로봇 학습을 위한 데이터셋 구축의 기초 사례를 제공한다.
- 🔗 후속 연구: [[papers/1348_Data_Scaling_Laws_in_Imitation_Learning_for_Robotic_Manipula/review]] — 로봇 모방 학습에서 데이터 스케일링 법칙을 ARIO 데이터셋으로 확장 연구한다.
- 🧪 응용 사례: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — ARIO의 통합 데이터 표준이 cross-embodied learning 연구에서 실제로 활용될 수 있는 데이터 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1372_DROID_A_Large-Scale_In-The-Wild_Robot_Manipulation_Dataset/review]] — 야생 환경 로봇 조작 데이터 DROID와 다양한 로봇 시리즈 포함 ARIO가 다른 데이터 수집 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1475_MetaMorph_Learning_Universal_Controllers_with_Transformers/review]] — All Robots in One 연구는 MetaMorph가 추구하는 범용 로봇 제어기의 데이터셋 통합 관점을 제공합니다.
- 🏛 기반 연구: [[papers/1499_OmniVLA_An_Omni-Modal_Vision-Language-Action_Model_for_Robot/review]] — OmniVLA의 통합 데이터셋 활용이 기반으로 하는 unified robot learning dataset
- 🏛 기반 연구: [[papers/1541_RoboMIND_Benchmark_on_Multi-embodiment_Intelligence_Normativ/review]] — 통일된 다중 로봇 데이터셋 표준은 모든 로봇을 하나로 통합하는 비전과 언어 데이터셋의 기반이 됩니다.
- 🏛 기반 연구: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — All Robots in One은 CrossFormer가 달성하려는 통합된 다중 embodiment 제어를 위한 표준화된 데이터셋을 제공한다.
- 🏛 기반 연구: [[papers/1629_Whom_to_Trust_Elective_Learning_for_Distributed_Gaussian_Pro/review]] — All Robots in One의 통합 데이터셋이 Pri-GP의 분산 로봇 학습을 위한 표준화된 기반을 제공한다.
- 🏛 기반 연구: [[papers/1633_X-VLA_Soft-Prompted_Transformer_as_Scalable_Cross-Embodiment/review]] — Cross-embodiment learning을 위한 통합 데이터셋과 표준화 방법론의 기본 토대를 제공한다.
- 🏛 기반 연구: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — BridgeData V2의 대규모 데이터 수집 방법론이 ARIO와 같은 통합 로봇 데이터셋 개발의 기초가 됩니다.
