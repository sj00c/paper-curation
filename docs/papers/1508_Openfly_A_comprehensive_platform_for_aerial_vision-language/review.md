---
title: "1508_Openfly_A_comprehensive_platform_for_aerial_vision-language"
authors:
  - "Yunpeng Gao"
  - "Chenhui Li"
  - "Zhongrui You"
  - "Junli Liu"
  - "Zhen Li"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "OpenFly는 항공 Vision-Language Navigation을 위한 종합 플랫폼으로, 4개 렌더링 엔진, 자동화된 데이터 생성 툴체인, 100k 궤적의 대규모 데이터셋, 그리고 keyframe-aware VLN 모델을 제공한다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/GPU-Accelerated_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Gao et al._2025_Openfly A comprehensive platform for aerial vision-language navigation.pdf"
---

# Openfly: A comprehensive platform for aerial vision-language navigation

> **저자**: Yunpeng Gao, Chenhui Li, Zhongrui You, Junli Liu, Zhen Li, Pengan Chen, Qizhi Chen, Zhonghan Tang, Liansheng Wang, Penghui Yang, Yiwen Tang, Yuhang Tang, Shuai Liang, Songyi Zhu, Ziqin Xiong, Yifei Su, Xinyi Ye, Jianan Li, Yan Ding, Dong Wang, Xuelong Li, Zhigang Wang, Bin Zhao | **날짜**: 2025-02-25 | **URL**: [https://arxiv.org/abs/2502.18041](https://arxiv.org/abs/2502.18041)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of OpenFly. This work consists of (1) the integration of 4 rendering engines, significantly*

OpenFly는 항공 Vision-Language Navigation을 위한 종합 플랫폼으로, 4개 렌더링 엔진, 자동화된 데이터 생성 툴체인, 100k 궤적의 대규모 데이터셋, 그리고 keyframe-aware VLN 모델을 제공한다.

## Motivation

- **Known**: 실내 및 지상 기반 VLN은 광범위하게 연구되었으며, R2R, REVERIE, VLN-CE 등의 벤치마크가 존재한다. 최근 AerialVLN과 OpenUAV가 항공 VLN을 시작했으나 데이터 규모와 다양성이 제한적이다.
- **Gap**: 기존 항공 VLN 연구는 AirSim과 Unreal Engine에만 의존하여 데이터 다양성이 부족하고, 수동 주석으로 인한 높은 수집 비용으로 데이터 규모가 10k 궤적 수준에 그친다.
- **Why**: UAV는 항공 촬영, 구조 작업, 물품 운송 등 실제 응용 분야가 많으며, 대규모 고품질 항공 VLN 데이터셋은 embodied AI 발전에 필수적이다.
- **Approach**: OpenFly는 Unreal Engine, GTA V, Google Earth, 3D Gaussian Splatting을 통합하여 환경 다양성을 확보하고, point cloud 획득, 의미론적 분할, 궤적 생성, instruction 자동 생성의 완전 자동화 파이프라인을 개발했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of OpenFly. This work consists of (1) the integration of 4 rendering engines, significantly*

- **다중 렌더링 엔진 통합**: UE, GTA V, Google Earth, 3D GS를 단일 플랫폼에 통합하여 광범위한 디지털 자산 활용 가능
- **자동화 데이터 생성**: 조종사 조작과 수동 주석의 의존성을 제거한 완전 자동화 파이프라인으로 데이터 수집 비용 대폭 절감
- **대규모 벤치마크**: 18개 장면에서 100k 궤적을 수집한 지금까지 최대 규모의 항공 VLN 데이터셋 구축
- **우수한 성능**: OpenFly-Agent가 보인 VLN 환경에서 14.0% (seen), 7.9% (unseen) 성능 향상
- **Real-to-sim 렌더링**: 3D GS 기술로 실제 환경 이미지를 정확하게 시뮬레이션된 3D 장면으로 변환

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Framework of the automatic data generation. Multiple rendering engines are integrated*

- **점군 획득**: 각 장면의 3D 공간 점유 정보를 LiDAR Acquisition API로 자동 수집
- **의미론적 분할**: 장면 내 landmark를 자동 식별하여 waypoint 후보 선정
- **궤적 생성**: landmark와 점군 정보를 활용하여 충돌 없는 항공 경로를 자동 탐색
- **Instruction 생성**: GPT-4o 같은 VLM을 활용하여 UAV 시점 이미지와 궤적으로부터 언어 instruction 자동 생성
- **Keyframe-aware 모델**: 적응형 frame-level sampling으로 지시어 관련 landmark를 포함한 중요 관측에 집중하여 성능과 효율성 동시 개선

## Originality

- 항공 VLN을 위해 처음으로 4개 이상의 렌더링 엔진을 통합한 플랫폼 개발
- Real-to-sim 렌더링으로 실제 환경을 정확한 3D 시뮬레이션 환경으로 변환하는 혁신적 접근
- Point cloud, 의미론적 분할, 궤적 생성, instruction 생성을 통합한 완전 자동화 파이프라인 구축
- Keyframe-aware sampling을 통해 항공 VLN의 특성상 높은 frame rate 데이터에서 핵심 정보 추출
- 100k 규모 벤치마크로 항공 VLN 연구의 quantitative 평가 기반 확립

## Limitation & Further Study

- 현재 18개 장면으로 제한되어 있으며, 더욱 광범위한 지리적 다양성 확보 필요
- 3D GS 기반 real-to-sim 렌더링의 정확도가 극도로 복잡한 동적 환경에서 저하될 가능성
- 자동 instruction 생성이 VLM에 의존하므로 생성된 instruction의 품질과 다양성이 모델에 좌우됨
- 현재 모델은 정적 환경 가정하에 설계되어 있으며, 동적 장애물이나 실제 기상 조건 반영 필요
- 실제 UAV 하드웨어 배포 시 시뮬레이션과의 domain gap 해소를 위한 추가 연구 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: OpenFly는 항공 VLN 연구의 데이터 부족 문제를 획기적으로 해결한 종합 플랫폼으로, 다중 렌더링 엔진 통합, 완전 자동화 파이프라인, 100k 규모 벤치마크를 통해 embodied AI 분야에 중요한 기여를 한다. 제안된 keyframe-aware 모델도 항공 VLN의 특수성을 반영한 효과적인 접근법이다.

## Related Papers

- 🔄 다른 접근: [[papers/1443_L3MVN_Leveraging_Large_Language_Models_for_Visual_Target_Nav/review]] — OpenFly와 L3MVN 모두 항공 네비게이션을 다루지만 VLN과 시각적 타겟 네비게이션이라는 다른 접근법을 사용합니다.
- 🔗 후속 연구: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — 항공 VLN 플랫폼은 NaVid의 비디오 기반 VLM 계획과 결합하여 더 정교한 항공 네비게이션을 구현할 수 있습니다.
- 🏛 기반 연구: [[papers/1329_CityNavAgent_Aerial_Vision-and-Language_Navigation_with_Hier/review]] — 항공 비전-언어 네비게이션의 기반 기술은 CityNavAgent의 계층적 항공 네비게이션에도 적용됩니다.
- 🔄 다른 접근: [[papers/1420_Habitat_20_Training_Home_Assistants_to_Rearrange_their_Habit/review]] — Openfly의 aerial 환경과 다르게 가정 내 지상 로봇의 물체 조작에 특화된 시뮬레이션 플랫폼을 제공한다.
- 🧪 응용 사례: [[papers/1329_CityNavAgent_Aerial_Vision-and-Language_Navigation_with_Hier/review]] — aerial VLN의 도시 환경 네비게이션 개념을 포괄적인 aerial vision-language 플랫폼으로 확장 적용
