---
title: "1603_V-JEPA_2_Self-Supervised_Video_Models_Enable_Understanding_P"
authors:
  - "Mido Assran"
  - "Adrien Bardes"
  - "David Fan"
  - "Quentin Garrido"
  - "Russell Howes"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "V-JEPA 2는 1백만 시간 이상의 인터넷 규모 비디오로 사전학습한 자기지도학습 비디오 모델로, 비디오 이해·예측·로봇 계획을 모두 가능하게 한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Visual_Language_Navigation"
  - "cat/Robot_Policy_Learning"
  - "sub/Self-Supervised_Vision_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Assran et al._2025_V-JEPA 2 Self-Supervised Video Models Enable Understanding, Prediction and Planning.pdf"
---

# V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning

> **저자**: Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, , , Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, Sergio Arnaud, Abha Gejji, Ada Martin, Francois Robert Hogan, Daniel Dugas, Piotr Bojanowski, Vasil Khalidov, Patrick Labatut, Francisco Massa, Marc Szafraniec, Kapil Krishnakumar, Yong Li, Xiaodong Ma, Sarath Chandar, Franziska Meier, Yann LeCun, Michael Rabbat, Nicolas Ballas | **날짜**: 2025-06-11 | **URL**: [https://arxiv.org/abs/2506.09985](https://arxiv.org/abs/2506.09985)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 V-JEPA 2 Overview. Leveraging 1M hours of internet-scale video and 1M images, we pretrain the V-JEPA 2*

V-JEPA 2는 1백만 시간 이상의 인터넷 규모 비디오로 사전학습한 자기지도학습 비디오 모델로, 비디오 이해·예측·로봇 계획을 모두 가능하게 한다.

## Motivation

- **Known**: 기존 세계 모델 연구는 상호작용 데이터에 의존하여 확장성이 제한적이었고, 비디오 생성 기반 접근법은 계획 능력 평가에 초점을 맞추지 못했다.
- **Gap**: 인터넷 규모 비디오와 적은 상호작용 데이터를 결합하여 실제 로봇 조작에서 제로샷 성능을 달성할 수 있는 세계 모델이 부재했다.
- **Why**: 자기지도학습으로 학습한 예측 표현 공간이 로봇 계획과 실행에 실제로 효과적임을 증명함으로써 일반화 가능한 에이전트 개발의 경로를 제시한다.
- **Approach**: 단계적 학습 절차를 사용하여 먼저 마스크 제거 목표로 V-JEPA 2 인코더를 사전학습하고, 이후 소규모 로봇 상호작용 데이터로 액션 조건부 세계 모델(V-JEPA 2-AC)을 포스트학습한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1 V-JEPA 2 Overview. Leveraging 1M hours of internet-scale video and 1M images, we pretrain the V-JEPA 2*

- **비디오 이해**: Something-Something v2에서 77.3% top-1 정확도를 달성하는 등 세밀한 동작 이해에 우수한 성능을 보임
- **액션 예측**: Epic-Kitchens-100 인간 액션 예측 작업에서 39.7 recall-at-5로 이전 최고 모델 대비 44% 상대 개선 달성
- **비디오 QA**: V-JEPA 2를 LLM과 정렬하여 8B 파라미터 규모에서 PerceptionTest(84.0), TempCompass(76.9) 등 여러 벤치마크에서 최고 성능 달성
- **로봇 계획**: 62시간의 레이블이 없는 로봇 데이터만으로 V-JEPA 2-AC를 포스트학습하여 실제 Franka 로봇에서 제로샷으로 픽앤플레이스 작업 성공

## How

![Figure 2](figures/fig2.webp)

*Figure 2 Multistage training. (Left) We first pretrain the V-JEPA 2 video encoder on internet-scale image and*

- 1M 시간 이상의 인터넷 비디오와 1M개 이미지로 V-JEPA 2 인코더(최대 1B 파라미터)를 마스크 제거 특성 예측 목표로 사전학습
- 프로브 기반 분류 및 LLM 정렬을 통해 비디오 이해 및 예측 능력을 평가
- 학습된 표현 공간에서 액션 조건을 받는 블록-인과 주의 메커니즘을 가진 300M 파라미터 Transformer로 V-JEPA 2-AC를 구성
- 모델 예측 제어(MPC) 루프 내에서 계획을 통해 로봇 조작 작업 수행
- 신경망 구조 및 입력 비디오 길이 등 여러 스케일링 요소를 체계적으로 탐색

## Originality

- JEPA 아키텍처를 인터넷 규모 비디오(1M+ 시간)로 대규모 스케일링하여 실질적인 로봇 계획 능력을 처음으로 달성한 점
- 액션 레이블이 없는 비디오 사전학습과 소규모 상호작용 데이터 포스트학습의 단계적 결합으로 효율적 학습 파이프라인 구성
- 표현 공간에서의 예측 기반 세계 모델이 픽셀 생성 기반 접근법보다 실제 로봇 제어에 더 실용적임을 실증적으로 입증

## Limitation & Further Study

- 로봇 실험은 62시간의 Droid 데이터셋 기반이므로 다양한 로봇 플랫폼이나 작업에 대한 일반화 가능성 평가 필요
- 제로샷 성능이 우수하나, 특정 환경에서의 성능 개선을 위한 적응형 학습(domain adaptation) 전략 부재
- 계획 성능은 V-JEPA 2 표현의 품질에 완전히 의존하므로, 표현 공간의 한계가 직접적으로 계획 성능 제약으로 작용
- 실시간 로봇 제어를 위한 계산 효율성과 지연시간에 대한 평가 미흡
- 향후 다중 로봇 협력, 장기 계획, 복잡한 상호작용이 필요한 작업으로의 확장 연구 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: V-JEPA 2는 인터넷 규모 자기지도학습과 최소한의 로봇 상호작용 데이터를 결합하여 비디오 이해, 예측, 실제 로봇 계획을 모두 달성한 획기적 연구로, 세계 모델 기반 일반 에이전트 개발의 새로운 방향을 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1570_Self-Supervised_Learning_from_Images_with_a_Joint-Embedding/review]] — 이미지에서의 joint-embedding 자기지도학습 방법론을 제공하여 V-JEPA 2의 비디오 자기지도학습에 이론적 기반을 제공합니다.
- 🔗 후속 연구: [[papers/1473_MC-JEPA_A_Joint-Embedding_Predictive_Architecture_for_Self-S/review]] — Minecraft 환경에서의 joint-embedding predictive architecture를 실세계 비디오로 확장하여 더 일반적인 응용을 제시합니다.
- 🧪 응용 사례: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — 자기지도학습 비디오 모델을 물리적 AI를 위한 세계 시뮬레이션에 적용하여 V-JEPA 2의 실제 활용을 보여줍니다.
- 🔗 후속 연구: [[papers/1292_A_Comprehensive_Survey_on_World_Models_for_Embodied_AI/review]] — World Model 서베이에서 제시된 개념들을 V-JEPA 2가 비디오 기반으로 실현한다.
- 🔄 다른 접근: [[papers/1631_World_Models/review]] — World Models와 V-JEPA 2 모두 환경 모델링을 다루지만 비디오와 일반적 접근법이 다르다.
- 🔄 다른 접근: [[papers/1287_π_0_A_Vision-Language-Action_Flow_Model_for_General_Robot_Co/review]] — 둘 다 vision-based robot control을 다루지만 V-JEPA 2는 self-supervised video learning을, π_0는 flow model을 사용한다.
- 🧪 응용 사례: [[papers/1400_GAIA-1_A_Generative_World_Model_for_Autonomous_Driving/review]] — GAIA-1의 generative world model이 V-JEPA 2의 video understanding과 prediction 능력을 자율주행 도메인에 적용할 수 있다.
- 🔗 후속 연구: [[papers/1473_MC-JEPA_A_Joint-Embedding_Predictive_Architecture_for_Self-S/review]] — V-JEPA의 비디오 self-supervised learning을 motion과 content 결합으로 발전
- 🏛 기반 연구: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — NaVid의 비디오 기반 VLM 접근법이 V-JEPA 2의 자기지도 비디오 모델의 이해 능력을 로봇 네비게이션에 활용하는 기초를 제공합니다.
