---
title: "1493_Neural_Scaling_Laws_in_Robotics"
authors:
  - "Sebastian Sartor"
  - "Neil Thompson"
date: "2024.05"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇공학 분야에서 신경망 스케일링 법칙을 처음으로 체계적으로 정량화한 메타분석 연구로, 327개 논문을 분석하여 데이터 크기, 모델 크기, 계산 자원이 로봇 작업 성능에 미치는 영향을 규명했다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robot_Policy_Learning"
  - "sub/Embodied_AI_Research"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Sartor and Thompson_2024_Neural Scaling Laws in Robotics.pdf"
---

# Neural Scaling Laws in Robotics

> **저자**: Sebastian Sartor, Neil Thompson | **날짜**: 2024-05-22 | **URL**: [https://arxiv.org/abs/2405.14005](https://arxiv.org/abs/2405.14005)

---

## Essence

![Figure 3](figures/fig3.webp)

*Fig. 3: Scaling laws in robotics: (a, c, e) show scaling across*

로봇공학 분야에서 신경망 스케일링 법칙을 처음으로 체계적으로 정량화한 메타분석 연구로, 327개 논문을 분석하여 데이터 크기, 모델 크기, 계산 자원이 로봇 작업 성능에 미치는 영향을 규명했다.

## Motivation

- **Known**: 언어 모델링과 컴퓨터 비전 분야에서는 신경망 스케일링 법칙이 광범위하게 연구되었으며, power-law 관계를 따르는 성능 개선이 확인되었다. 로봇공학에도 foundation model이 도입되고 있으나 스케일링 법칙의 체계적 분석은 부재했다.
- **Gap**: 로봇공학 분야에서 Robot Foundation Models(RFMs)와 Large Language Models(LLMs)의 스케일링 법칙에 대한 종합적 정량화가 이루어지지 않았으며, 실제 로봇 작업 성능으로 직접 번역되는 지표를 기반으로 한 연구도 부족했다.
- **Why**: 로봇 시스템의 스케일링 법칙을 이해하면 성능 예측, 자원 배분 최적화, 실험 비용 절감, 환경 지속성 향상이 가능하며, 일반 목적 로봇 시스템 개발을 위한 중요한 이론적 기초가 된다.
- **Approach**: 327개 로봇공학 관련 논문의 메타분석을 통해 다양한 로봇 작업에서 데이터 크기, 모델 크기, 계산 자원에 따른 성능 변화를 수집 및 분석하여 power-law 관계식의 계수를 추출했다.

## Achievement


- **스케일링 법칙의 보편성 확인**: 로봇공학에서도 다른 ML 분야와 마찬가지로 power-law 관계를 따르는 스케일링 법칙이 성립함을 입증
- **우월한 로봇 작업 개선률**: 언어 작업 대비 로봇 작업 성능이 증가된 자원에 따라 훨씬 빠르게 향상됨을 발견
- **신흥 능력의 출현**: 모델이 확장됨에 따라 새로운 로봇 능력이 출현하는 현상 관찰
- **성능 예측 가능성**: 주어진 자원에 대한 성능을 예측하고 목표 성능 달성에 필요한 자원 추정 가능

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Growth of Robotics (a) and Scaling Laws (b) research*

- Google Scholar 기반 2021-2024년 로봇 foundation model 논문 수집 및 분류
- RFMs(Pre-trained Visual Representations, Vision-Language Models, Vision-Language-Action Models)와 LLMs in robotics 구분
- 각 논문에서 데이터 크기(D), 모델 크기(N), 계산 자원(C)과 성능 메트릭 추출
- Power-law 함수 L(D) = A/D^α, L(N) = B/N^β, L(C) = F/C^γ에 적합(fit)
- 스케일링 계수(α, β, γ) 추정 및 언어, 비전 도메인과 비교 분석
- 오차 막대(error bar)를 포함한 시각화를 통한 결과 표현

## Originality

- 로봇공학 분야에서 신경망 스케일링 법칙을 다룬 **첫 번째 종합 연구**
- 327개 논문 메타분석을 통한 **대규모 경험적 정량화**
- **실제 로봇 작업 성능**을 기반으로 한 스케일링 법칙 분석 (기존 cross-entropy 손실 중심과 차별)
- RFMs와 LLMs 두 카테고리를 모두 포함한 **종합적 분석 범위**

## Limitation & Further Study

- 로봇 데이터셋 규모 제약: 현실 세계 데이터 수집 비용이 높아 인터넷 규모 데이터셋 부재로 인한 스케일링 한계 존재
- Sim-to-real gap: 시뮬레이션 기반 연구가 실제 로봇 성능으로 일반화되지 않을 가능성
- 성능 메트릭 다양성: 다양한 로봇 작업의 성공 기준이 상이하여 메타분석 과정에서 정규화 어려움
- 신흥 능력의 정량화 부족: 새로운 로봇 능력의 출현이 정성적으로만 기술되어 정량적 분석 필요
- 후속 연구: (1) Vision-Language-Action(VLA) 모델의 동작 학습 스케일링 심화 분석, (2) 로봇 시뮬레이션 플랫폼(RoboCasa, Genesis, Nvidia Cosmos) 기반 데이터 생성 효율성 재평가, (3) In-context learning과 prompt engineering의 로봇 적용 스케일링 법칙 규명

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 로봇공학에서 신경망 스케일링 법칙을 최초로 체계적으로 정량화하여 미래 일반 목적 로봇 시스템 개발의 이론적 기초를 제공하는 중요한 메타분석 연구이다. 다만 현실적인 로봇 데이터 수집 한계와 작업 성공 기준의 다양성으로 인한 메타분석의 한계는 개선이 필요하다.

## Related Papers

- 🏛 기반 연구: [[papers/1348_Data_Scaling_Laws_in_Imitation_Learning_for_Robotic_Manipula/review]] — 로봇공학의 신경망 스케일링 법칙이 Data Scaling Laws in Imitation Learning의 모방 학습 스케일링 연구에 이론적 기반을 제공한다.
- 🧪 응용 사례: [[papers/1315_AutoRT_Embodied_Foundation_Models_for_Large_Scale_Orchestrat/review]] — Neural Scaling Laws의 정량적 분석이 AutoRT의 대규모 로봇 시스템 설계에서 최적 모델 크기 결정에 실용적 지침을 제공한다.
- 🔗 후속 연구: [[papers/1566_Scaling_Up_and_Distilling_Down_Language-Guided_Robot_Skill_A/review]] — 로봇공학 스케일링 법칙이 Scaling Up and Distilling Down의 언어 기반 로봇 스킬 학습에서 효율적 스케일링 전략 수립에 활용된다.
- 🧪 응용 사례: [[papers/1511_PaLI-X_On_Scaling_up_a_Multilingual_Vision_and_Language_Mode/review]] — scaling law 분석을 multilingual vision-language model에 적용한 구체적 사례
- 🔗 후속 연구: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — 로봇 스케일링 법칙을 vision-language-action model 구축에 적용한 확장 연구
- 🔗 후속 연구: [[papers/1372_DROID_A_Large-Scale_In-The-Wild_Robot_Manipulation_Dataset/review]] — DROID와 같은 대규모 데이터셋은 Neural Scaling Laws가 제시하는 데이터 크기와 성능 관계를 실증하는 구체적 사례입니다.
- 🔄 다른 접근: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Open X-Embodiment는 스케일링 법칙을 실제 다중 실시화 데이터로 검증하는 반면, Neural Scaling Laws는 이론적 분석에 중점을 둡니다.
- 🏛 기반 연구: [[papers/1513_Parallels_Between_VLA_Model_Post-Training_and_Human_Motor_Le/review]] — Neural Scaling Laws가 VLA 모델의 post-training 효과를 정량적으로 이해하는 이론적 기반을 제공한다.
- 🧪 응용 사례: [[papers/1511_PaLI-X_On_Scaling_up_a_Multilingual_Vision_and_Language_Mode/review]] — multilingual VLM scaling을 통해 neural scaling laws를 실증한 구체적 사례
- 🏛 기반 연구: [[papers/1542_RoboMonkey_Scaling_Test-Time_Sampling_and_Verification_for_V/review]] — Neural Scaling Laws의 이론적 기반을 VLA 모델의 테스트 시간 스케일링으로 확장한다.
- 🏛 기반 연구: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — 로봇공학에서의 신경망 스케일링 법칙 연구가 VLA 모델의 데이터 활용과 아키텍처 스케일링 분석에 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1348_Data_Scaling_Laws_in_Imitation_Learning_for_Robotic_Manipula/review]] — 로봇 공학에서 신경망 스케일링 법칙에 대한 포괄적인 확장 연구입니다.
- 🔗 후속 연구: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — Neural Scaling Laws는 DRL 성공 사례 조사에서 제시된 스케일링 원칙을 이론적으로 확장하고 일반화합니다.
- 🧪 응용 사례: [[papers/1417_GRUtopia_Dream_General_Robots_in_a_City_at_Scale/review]] — GRUtopia가 제공하는 100k 규모의 상호작용 장면이 로봇공학에서 신경망 스케일링 법칙을 검증하는 실험 환경으로 활용된다.
