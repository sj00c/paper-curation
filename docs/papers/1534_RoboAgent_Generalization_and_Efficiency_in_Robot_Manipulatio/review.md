---
title: "1534_RoboAgent_Generalization_and_Efficiency_in_Robot_Manipulatio"
authors:
  - "Homanga Bharadhwaj"
  - "Jay Vakil"
  - "Mohit Sharma"
  - "Abhinav Gupta"
  - "Shubham Tulsiani"
date: "2023.09"
doi: ""
arxiv: ""
score: 4.0
essence: "RoboAgent는 semantic augmentation과 action chunking을 활용하여 7,500개의 데모만으로 12개의 조작 스킬을 수행하는 범용 로봇 조작 에이전트를 학습한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Multimodal_Sensor_Encoding"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bharadhwaj et al._2023_RoboAgent Generalization and Efficiency in Robot Manipulation via Semantic Augmentations and Action.pdf"
---

# RoboAgent: Generalization and Efficiency in Robot Manipulation via Semantic Augmentations and Action Chunking

> **저자**: Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, Vikash Kumar | **날짜**: 2023-09-05 | **URL**: [https://arxiv.org/abs/2309.01918](https://arxiv.org/abs/2309.01918)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Two stage framework: [Left] Semantic augmentation stage diversifies the robot data offline us-*

RoboAgent는 semantic augmentation과 action chunking을 활용하여 7,500개의 데모만으로 12개의 조작 스킬을 수행하는 범용 로봇 조작 에이전트를 학습한다.

## Motivation

- **Known**: 로봇 조작을 위한 대규모 데이터셋 수집은 비용이 많이 들고, 최근 연구들이 대규모 데이터(100K+)를 활용한 멀티태스크 정책 학습을 시도하고 있다.
- **Gap**: 기존 방법들은 우수한 일반화 성능을 위해 대량의 데이터를 필요로 하지만, 제한된 데이터 예산 내에서 효율적으로 일반화 가능한 정책을 학습하는 문제는 미해결 상태이다.
- **Why**: 실제 로봇 배포 환경에서는 항상 예측 불가능한 상황에 직면하므로, 제한된 데이터로 높은 일반화 성능을 달성하는 것이 실용적으로 매우 중요하다.
- **Approach**: semantic augmentation으로 오프라인 데이터를 증강하고, MT-ACT(Multi-Task Action-Chunking Transformers) 아키텍처를 통해 action chunking과 multimodal 데이터를 효과적으로 처리한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: A glimpse of the diverse manipulation capabilities of RoboAgent– a single agent capable of 12 ma-*

- **데이터 효율성**: 기존 대규모 방법(135K)의 약 1/18 규모인 7,500개 데모만으로 12개 스킬 학습
- **일반화 성능**: 보이지 않은 환경에서 기존 방법 대비 40% 이상의 성능 향상 달성
- **스킬 다양성**: 단일 정책으로 38개 태스크에 걸친 12개의 고유한 조작 스킬 수행
- **오픈소스 기여**: 98,050개의 데모를 포함한 RoboSet을 공개하여 로봇 학습 커뮤니티에 기여

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Two stage framework: [Left] Semantic augmentation stage diversifies the robot data offline us-*

- Semantic augmentation: foundation model 기반 inpainting을 사용한 오프라인 데이터 증강으로 데이터 다양성 확보
- Action chunking: 시간적 상관성을 활용하여 per-step 대신 action chunk 예측으로 covariate shift 완화
- MT-ACT 아키텍처: CNN 인코더, FiLM 모듈, CVAE 기반 latent encoding을 통해 multimodal 데이터 처리
- Language conditioning: 자연어 명령어를 통한 유연한 태스크 지정으로 다양한 스킬 활성화
- Temporal aggregation: 시간 축 방향 정보 통합으로 정책 예측의 안정성 향상

## Originality

- 기존의 세그먼테이션 마스크나 객체 메시 없이 완전 자동화된 semantic augmentation 방식 제시
- Action chunking과 multimodal data 처리를 통합한 MT-ACT 아키텍처의 설계
- 제한된 데이터에서의 generalization 성능 향상에 대한 체계적인 실증 분석 제공
- 상용 하드웨어로 수집된 대규모 오픈소스 로봇 조작 데이터셋(RoboSet) 공개

## Limitation & Further Study

- 주로 kitchen 환경에서의 테스트로 다른 도메인으로의 일반화 가능성이 불명확함
- Semantic augmentation의 품질이 foundation model의 성능에 의존하므로 모델 선택에 민감할 수 있음
- 실시간 성능, 계산 효율성, 하드웨어 요구사항에 대한 분석이 부족함
- 후속 연구: 다양한 환경/도메인으로의 확장, 더 큰 action chunk 크기의 효과 분석, sim-to-real transfer 성능 평가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 제한된 데이터 예산에서 실질적인 로봇 조작 능력을 달성하는 실용적인 방법을 제시하며, semantic augmentation과 action chunking의 조합이 효과적임을 입증하였다. 오픈소스 데이터셋 공개와 함께 로봇 학습 분야에 중요한 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1565_Scaling_Robot_Learning_with_Semantically_Imagined_Experience/review]] — 의미적으로 상상된 경험을 통한 로봇 학습 확장 기법이 RoboAgent의 semantic augmentation 방법론의 이론적 기초가 된다.
- 🔄 다른 접근: [[papers/1331_CLASS_Contrastive_Learning_via_Action_Sequence_Supervision_f/review]] — CLASS와 함께 효율적인 로봇 조작 학습을 다루지만 RoboAgent는 semantic augmentation에, CLASS는 contrastive learning에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — RT-1의 대규모 데이터 학습 방법론을 semantic augmentation으로 더 효율적으로 개선하여 적은 데모로도 범용 조작을 달성한다.
- 🔄 다른 접근: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — 범용 로봇 조작 에이전트 구축에서 RoboAgent는 semantic augmentation을, Octo는 대규모 오픈소스 데이터를 활용한다.
- 🏛 기반 연구: [[papers/1348_Data_Scaling_Laws_in_Imitation_Learning_for_Robotic_Manipula/review]] — 모방학습에서의 데이터 스케일링 법칙이 RoboAgent의 효율적인 7,500개 데모 학습 전략 설계에 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1566_Scaling_Up_and_Distilling_Down_Language-Guided_Robot_Skill_A/review]] — RoboAgent의 semantic augmentation을 language-guided skill acquisition과 결합하여 더 효율적인 robot learning을 실현할 수 있다.
