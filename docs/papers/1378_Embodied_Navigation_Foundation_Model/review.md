---
title: "1378_Embodied_Navigation_Foundation_Model"
authors:
  - "Jiazhao Zhang"
  - "Anqi Li"
  - "Yunpeng Qi"
  - "Minghan Li"
  - "Jiahang Liu"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "NavFoM은 8백만 개의 네비게이션 샘플로 학습된 크로스-구현체·크로스-태스크 기반 네비게이션 모델로, 다양한 로봇 플랫폼과 네비게이션 작업에서 미세 조정 없이 최첨단 성능을 달성한다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Multimodal_Navigation_Systems"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_Embodied Navigation Foundation Model.pdf"
---

# Embodied Navigation Foundation Model

> **저자**: Jiazhao Zhang, Anqi Li, Yunpeng Qi, Minghan Li, Jiahang Liu, Shaoan Wang, Haoran Liu, Gengze Zhou, Yuze Wu, Xingxing Li, Yuxin Fan, Wenjun Li, Zhibo Chen, Fei Gao, Qi Wu, Zhizheng Zhang, He Wang | **날짜**: 2025-09-15 | **URL**: [https://arxiv.org/abs/2509.12129](https://arxiv.org/abs/2509.12129)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: We provide an illustration of architecture (left) alongside real-world experiment results (right). The*

NavFoM은 8백만 개의 네비게이션 샘플로 학습된 크로스-구현체·크로스-태스크 기반 네비게이션 모델로, 다양한 로봇 플랫폼과 네비게이션 작업에서 미세 조정 없이 최첨단 성능을 달성한다.

## Motivation

- **Known**: 최근 Vision-Language Models는 일반적인 비전-언어 작업에서 뛰어난 제로샷 성능을 보이지만, 신체화된 네비게이션에서는 좁은 작업 설정과 구현체별 아키텍처에 제한되어 있다.
- **Gap**: 기존 크로스-태스크 네비게이션 방법은 일정한 카메라 구성을 가정하고, 크로스-구현체 네비게이션은 특정 네비게이션 작업에만 제한되어 있어, 다양한 구현체와 작업을 모두 처리할 수 있는 통합 기초 모델이 부재하다.
- **Why**: 네비게이션은 신체화된 AI의 핵심 능력이며, 다양한 로봇 플랫폼과 작업을 처리할 수 있는 일반화된 모델은 실제 배포 및 신체화 AI의 실용성을 크게 향상시킬 수 있다.
- **Approach**: Temporal-Viewpoint Indicator (TVI) 토큰을 도입하여 다양한 카메라 구성과 시간적 맥락을 임베딩하고, 토큰 예산 제약 하에서 동적 샘플링 전략인 Budget-Aware Temporal Sampling (BATS)을 적용하여 실제 배포 요구 사항을 충족한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Benchmark performance of NavFoM, we compare NavFoM with SOTA baselines on each bench-*

- **크로스-구현체 일반화**: 이족 로봇, 사족 로봇, 드론, 바퀴 달린 로봇, 차량 등 다양한 구현체에서 미세 조정 없이 작동
- **크로스-태스크 성능**: Vision-and-Language Navigation, 객체 검색, 목표 추적, 자율주행 등 다양한 네비게이션 작업에서 경쟁력 있는 성능 달성
- **벤치마크 성과**: VLN-CE RxR에서 SR 64.4% (다중 카메라), HM3D-OVON에서 SR 45.2% (제로샷)로 이전 SOTA 능가
- **실제 배포 효율성**: BATS 전략으로 토큰 예산 제약 하에서 추론 속도와 성능의 균형 달성
- **실제 세계 검증**: 인간형 로봇, 사족 로봇, 드론, 바퀴 달린 로봇 등 다양한 로봇 플랫폼에서 강력한 일반화 능력 확인

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Pipeline of NavFoM. Our method provides a unified framework for handling multiple tasks, includ-*

- 8.02백만 개의 네비게이션 샘플과 4.76백만 개의 오픈 월드 지식 샘플(이미지 및 비디오 QA)의 통합 데이터셋 구성
- Temporal-Viewpoint Indicator (TVI) 토큰으로 카메라 뷰포인트와 시간 컨텍스트 정보 임베딩
- Budget-Aware Temporal Sampling (BATS) 전략으로 망각 곡선 기반의 동적 토큰 샘플링 구현
- 비전 인코더, 크로스모달 프로젝터, Large Language Model을 통합한 통합 아키텍처로 멀티모달 네비게이션 입력 처리
- 이미지 QA 및 비디오 QA 샘플과 네비게이션 데이터의 엔드-투-엔드 공동 학습

## Originality

- **최초의 대규모 크로스-구현체·크로스-태스크 네비게이션 기초 모델**: 4가지 구현체와 4가지 주요 네비게이션 작업을 통합하는 처음의 시도
- **Temporal-Viewpoint Indicator 토큰 도입**: 다양한 카메라 구성과 시간 맥락을 명시적으로 인코딩하여 구현체 간 일반화 개선
- **Budget-Aware Temporal Sampling 전략**: 토큰 예산 제약 하에서 효율적인 시간 정보 활용을 위한 망각 곡선 기반 접근
- **대규모 멀티소스 데이터셋 구성**: 공개 네비게이션 데이터셋, 가상 웹 비디오 데이터, QA 데이터의 통합으로 약 13백만 개 샘플의 포괄적 데이터셋 구축

## Limitation & Further Study

- **실제 세계 데이터의 제한성**: 웹 비디오 기반 의사 네비게이션 데이터 활용으로 인한 시뮬레이션과 현실의 도메인 갭 존재 가능성
- **특정 환경 조건에 대한 검증 부족**: 극단적인 조명, 날씨 조건, 혼잡한 실내 환경 등에서의 성능 평가 필요
- **동적 장애물 처리 능력 불명확**: 이동하는 사람, 차량 등 동적 요소가 있는 환경에서의 강건성 논의 미흡
- **후속 연구 방향**: 더 많은 실제 세계 로봇 데이터 수집, 추가 구현체(수중 로봇, 인간형 로봇의 손 조작) 포함, 실시간 환경 적응 능력 개선 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: NavFoM은 신체화된 AI 분야에서 크로스-구현체·크로스-태스크 네비게이션을 처음으로 통합적으로 해결한 대규모 기초 모델로, TVI 토큰과 BATS 전략의 혁신적 설계로 다양한 로봇 플랫폼과 네비게이션 작업에서 미세 조정 없이 강력한 일반화 능력을 입증하였다.

## Related Papers

- 🔗 후속 연구: [[papers/1497_OctoNav_Towards_Generalist_Embodied_Navigation/review]] — OctoNav의 generalist navigation을 더 크고 포괄적인 cross-embodiment foundation model로 확장 발전
- 🏛 기반 연구: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — cross-embodied learning의 통합 정책 개념이 navigation foundation model의 핵심 설계 기반
- 🏛 기반 연구: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — Vision-Language Navigation Survey가 NavFoM의 크로스-구현체 네비게이션 모델 설계의 이론적 배경과 방법론을 제공합니다.
- 🔗 후속 연구: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — NaVid의 비디오 기반 VLM 계획이 NavFoM의 foundation model을 실시간 네비게이션으로 확장하는 방법을 제시합니다.
- 🧪 응용 사례: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — Visual Language Maps가 NavFoM의 크로스-태스크 네비게이션을 공간 표현과 결합한 구체적인 적용 방법을 제공합니다.
- 🏛 기반 연구: [[papers/1461_LM-Nav_Robotic_Navigation_with_Large_Pre-Trained_Models_of_L/review]] — LM-Nav의 large pre-trained model 기반 navigation이 NavFoM의 foundation model 기반 네비게이션 프레임워크 개발에 기초가 된다.
- 🔗 후속 연구: [[papers/1488_NavDP_Learning_Sim-to-Real_Navigation_Diffusion_Policy_with/review]] — embodied navigation foundation model을 diffusion policy와 결합하여 더 일반적인 navigation 능력을 달성할 수 있다.
- 🏛 기반 연구: [[papers/1492_Neural_Brain_A_Neuroscience-inspired_Framework_for_Embodied/review]] — embodied navigation foundation model의 이론적 기반을 제공하여 Neural Brain 프레임워크의 navigation 모듈 설계에 필요한 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1575_SmartWay_Enhanced_Waypoint_Prediction_and_Backtracking_for_Z/review]] — SmartWay의 waypoint 기반 navigation을 foundation model 관점에서 확장하여 더 일반적인 embodied navigation으로 발전시킬 수 있다.
- 🔄 다른 접근: [[papers/1587_Time-Transient_Wireless_RF_Sensor_with_Differentiative_Detec/review]] — RF 센서와 Embodied Navigation Foundation Model은 환경 인식에서 서로 다른 센싱 모달리티를 제공합니다.
- 🔄 다른 접근: [[papers/1491_NaVILA_Legged_Robot_Vision-Language-Action_Model_for_Navigat/review]] — Embodied Navigation Foundation Model과 동일한 embodied navigation을 다루지만 NaVILA는 legged robot에 특화된 접근법을 사용한다.
