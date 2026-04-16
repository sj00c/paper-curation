---
title: "1300_A_Survey_on_Vision-Language-Action_Models_for_Autonomous_Dri"
authors:
  - "Sicong Jiang"
  - "Zilin Huang"
  - "Kangan Qian"
  - "Ziang Luo"
  - "Tianze Zhu"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 Vision-Language-Action (VLA) 모델을 자율주행에 적용하는 최초의 종합 서베이로, 20개 이상의 대표 모델을 분석하고 시각 인식, 자연어 이해, 제어를 통합하는 패러다임의 발전 과정을 추적한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Robot_Policy_Learning"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Jiang et al._2025_A Survey on Vision-Language-Action Models for Autonomous Driving.pdf"
---

# A Survey on Vision-Language-Action Models for Autonomous Driving

> **저자**: Sicong Jiang, Zilin Huang, Kangan Qian, Ziang Luo, Tianze Zhu, Yang Zhong, Yihong Tang, Menglin Kong, Yunlong Wang, Siwen Jiao, Hao Ye, Zihao Sheng, Xin Zhao, Tuopu Wen, Zheng Fu, Sikai Chen, Kun Jiang, Diange Yang, Seongjin Choi, Lijun Sun | **날짜**: 2025-06-30 | **URL**: [https://arxiv.org/abs/2506.24044](https://arxiv.org/abs/2506.24044)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Comparisons of autonomous driving paradigms. (a) End-to-end driving offers direct perception-to-control mappin*

본 논문은 Vision-Language-Action (VLA) 모델을 자율주행에 적용하는 최초의 종합 서베이로, 20개 이상의 대표 모델을 분석하고 시각 인식, 자연어 이해, 제어를 통합하는 패러다임의 발전 과정을 추적한다.

## Motivation

- **Known**: End-to-End 자율주행은 센서 입력을 직접 제어 명령으로 매핑하며, VLM4AD는 장면 설명 및 설명가능성을 추가했으나 행동 결정 문제는 미해결 상태였다.
- **Gap**: 기존 VLM 기반 자율주행 연구는 인식 중심이며 언어 출력과 저수준 제어 간 느슨한 결합 문제가 있고, VLA 패러다임의 종합적 개요가 부재했다.
- **Why**: VLA4AD는 고수준 지시 해석, 복잡한 교통 장면 추론, 자율 의사결정을 통합하여 설명가능하고 사회적으로 정렬된 자율주행을 실현할 수 있으며, 모서리 사례와 분포 외 시나리오에서의 강건성을 개선할 수 있다.
- **Approach**: 아키텍처 구성 요소를 형식화하고, 초기 설명자부터 추론 중심 VLA 모델로의 진화를 추적하며, 20개 이상의 대표 모델을 비교 분석하고, 데이터셋, 벤치마크, 평가 프로토콜을 정리했다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of the VLA4AD Architecture.*

- **최초의 포괄적 VLA4AD 서베이**: VLA 패러다임의 첫 번째 종합 개요 제공
- **아키텍처 패턴 정식화**: 최근 연구에서 공유되는 아키텍처 구성 요소 체계화
- **20개 이상 모델 비교**: 자율주행 도메인에서 VLA 진행 상황의 대표 모델 비교 분석
- **데이터셋 및 벤치마크 통합**: nuScenes, Impromptu VLA, SimLingo, NuInteract 등 기존 자료 정리
- **평가 프로토콜 정의**: 주행 안전성, 정확도, 설명 품질을 함께 측정하는 프로토콜 제시
- **미해결 과제 상세화**: 강건성, 실시간 효율성, 형식 검증의 개방 과제 상세 분석

## How

![Figure 1](figures/fig1.webp)

*Figure 1. Comparisons of autonomous driving paradigms. (a) End-to-end driving offers direct perception-to-control mappin*

- 기존 End-to-End, VLM4AD, VLA4AD 패러다임의 계층적 비교를 통해 진화 과정 추적
- Multi-Modal Encoder, LLM/VLM, Action Decoder 등 VLA 아키텍처의 공통 구성 요소 분류
- Fine-tuning, Chain-of-Thought 메모리, 저수준 제어 통합 등 훈련 패러다임 분석
- Drive safety, accuracy, explanation quality를 함께 측정하는 평가 프로토콜 설계
- LoRA(Low-Rank Adaptation), TS-VLM 등 효율성 향상 기법 통합
- Closed-loop 평가와 시뮬레이션 기반 스트레스 테스트 활용

## Originality

- VLA4AD에 대한 최초의 종합 서베이로서 새로운 연구 영역 정의
- End-to-End, VLM4AD, VLA4AD의 세 패러다임 간 명확한 구분 제시
- 아키텍처, 훈련 방법, 평가 프로토콜의 체계적 분류 체계 제안
- petabyte-scale 데이터셋과 합성 코퍼스의 역할 강조
- 강건성, 실시간 효율성, 형식 검증의 구체적 미해결 과제 제시

## Limitation & Further Study

- 서베이는 2025년 6월 시점의 스냅샷이므로 급속히 변화하는 VLA 분야의 최신 발전을 완전히 반영할 수 없음
- 20개 모델의 비교가 논문에서 상세히 제시되지 않아 개별 모델의 성능 차이가 명확하지 않음
- 실세계 배포에 대한 폐쇄 루프 평가 결과가 제한적이며, 시뮬레이션과 실제 환경 간 갭 미해결
- 형식 검증, 안전성 인증 등 규제 측면의 고려가 부분적
- 후속 연구로는 표준화된 벤치마크 및 오픈 소스 툴킷 개발, 실세계 데이터에서의 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 VLA4AD 분야의 최초의 종합 서베이로서 아키텍처, 진화 과정, 모델 비교를 체계적으로 정리하고 개방 과제를 명확히 정의함으로써, 설명가능하고 견고한 자율주행 시스템 개발을 위한 중요한 참고 자료를 제공한다.

## Related Papers

- 🔗 후속 연구: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — 자율주행용 VLA 모델 서베이는 로봇틱스 foundation model 종합 조사의 특정 도메인 확장판이다.
- 🧪 응용 사례: [[papers/1400_GAIA-1_A_Generative_World_Model_for_Autonomous_Driving/review]] — GAIA-1의 자율주행용 생성 세계 모델은 VLA 모델의 자율주행 적용 사례를 구체적으로 보여준다.
- 🏛 기반 연구: [[papers/1307_An_Anatomy_of_Vision-Language-Action_Models_From_Modules_to/review]] — VLA 모델의 모듈별 분석은 자율주행용 VLA 시스템 이해에 필수적인 구조적 기초를 제공한다.
- 🔗 후속 연구: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — VLM 기반 네비게이션 계획을 자율주행에 확장 적용한다.
- 🔄 다른 접근: [[papers/1490_NavigateDiff_Visual_Predictors_are_Zero-Shot_Navigation_Assi/review]] — 시각적 예측기를 활용한 제로샷 네비게이션이라는 다른 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1607_Vision-Language_Navigation_A_Survey_and_Taxonomy/review]] — Vision-Language Navigation의 전반적인 분류체계와 기초 개념을 제공합니다.
- 🔄 다른 접근: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — 로봇 비전에서 multimodal fusion vs autonomous driving에 특화된 VLA 모델이라는 서로 다른 도메인별 접근법을 비교 분석한다.
