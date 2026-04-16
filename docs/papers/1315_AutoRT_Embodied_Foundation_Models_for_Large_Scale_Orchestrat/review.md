---
title: "1315_AutoRT_Embodied_Foundation_Models_for_Large_Scale_Orchestrat"
authors:
  - "Michael Ahn"
  - "Debidatta Dwibedi"
  - "Chelsea Finn"
  - "Montse Gonzalez Arenas"
  - "Keerthana Gopalakrishnan"
date: "2024.01"
doi: ""
arxiv: ""
score: 4.0
essence: "AutoRT는 VLM과 LLM을 활용하여 로봇 함대의 대규모 자율 데이터 수집을 오케스트레이션하는 시스템으로, 77,000개의 실제 로봇 에피소드를 다양한 미지의 환경에서 수집했다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Robot_Foundation_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Ahn et al._2024_AutoRT Embodied Foundation Models for Large Scale Orchestration of Robotic Agents.pdf"
---

# AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents

> **저자**: Michael Ahn, Debidatta Dwibedi, Chelsea Finn, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Karol Hausman, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Sean Kirmani, Isabel Leal, Edward Lee, Sergey Levine, Yao Lu, Isabel Leal, Sharath Maddineni, Kanishka Rao, Dorsa Sadigh, Pannag Sanketi, Pierre Sermanet, Quan Vuong, Stefan Welker, Fei Xia, Ted Xiao, Peng Xu, Steve Xu, Zhuo Xu | **날짜**: 2024-01-23 | **URL**: [https://arxiv.org/abs/2401.12963](https://arxiv.org/abs/2401.12963)

---

## Essence

![Figure 5](figures/fig5.webp)

*Fig. 5 shows the visual diversity across each of AutoRT’s data collection policies, along with the*

AutoRT는 VLM과 LLM을 활용하여 로봇 함대의 대규모 자율 데이터 수집을 오케스트레이션하는 시스템으로, 77,000개의 실제 로봇 에피소드를 다양한 미지의 환경에서 수집했다.

## Motivation

- **Known**: Foundation model(VLM, LLM)은 언어, 비전, 액션을 통합하여 인터넷 규모의 데이터로 학습되었으나, embodied foundation model 훈련은 물리적 세계의 실제 데이터 부족이 핵심 병목이다.
- **Gap**: 기존 자율 데이터 수집은 제약된 lab 환경에 국한되고, 대규모 로봇 함대의 다양한 미지 환경에서의 in-the-wild 데이터 수집과 인간 감독의 효율적 활용 방법이 미해결이다.
- **Why**: embodied foundation model의 성능 향상을 위해 물리적 세계의 다양하고 대규모의 실제 로봇 데이터가 필수적이며, 이는 로봇 배포의 스케일링과 일반화 능력 향상에 직결된다.
- **Approach**: AutoRT는 VLM으로 장면 이해와 affordance 발견을 수행하고, LLM으로 다양한 작업을 자동 제안하며, Robot Constitution을 통해 안전성과 인간 선호도 정렬을 보장한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: On the left is AutoRT robot usage and on the right is t-SNE visualization of tasks, colored by collect*

- **대규모 실제 로봇 데이터 수집**: 4개 건물의 20+ 로봇으로부터 77,000개 에피소드(원격 조작 및 자율 정책 혼합) 수집
- **효율적 인력 활용**: 1명의 인간 감독자가 3-5개 모바일 매니퓨레이터 동시 감독 가능
- **높은 데이터 다양성**: AutoRT 수집 데이터가 기존 방식 대비 현저히 다양함을 실증
- **인간 선호도 정렬**: LLM 기반 instruction following과 constitutional prompting으로 로봇 행동이 인간 선호도에 부합
- **실제 환경 자율성**: LLM 제어 로봇이 실제 환경에서 자율 주행, 목표 자가 제안, 행동 실행을 최초 수행

## How

![Figure 5](figures/fig5.webp)

*Fig. 5 shows the visual diversity across each of AutoRT’s data collection policies, along with the*

- **장면 이해**: Open vocabulary object detector와 VLM으로 환경의 객체를 인식하고 시각-언어 임베딩으로 표현
- **탐색 단계**: Natural language map(Chen et al. 2023 기반)을 이용하여 관심 영역을 샘플링하고 로봇 네비게이션 가이드
- **작업 제안**: LLM이 scene description과 고수준 목표(user prompt)로부터 실행 가능한 작업 후보 생성
- **Affordance 필터링**: Robot Constitution(안전 규칙 3개 카테고리)과 인간 감독 가용성을 고려하여 실행할 작업과 정책 선택
- **정책 선택**: 자율 정책 πauto 또는 인간 원격 조작 πteleop 중 최적의 정책 결정
- **안전 메커니즘**: Constitutional AI 영감의 규칙 기반 시스템으로 로봇 행동 제약

## Originality

- **최초의 실제 환경 LLM 제어 로봇 자율성**: 시뮬레이션(Voyager)과 달리 실제 다중 건물 환경에서 장시간 LLM 기반 자율 운영 달성
- **Foundation model 기반 오케스트레이션**: VLM과 LLM을 활용한 대규모 로봇 함대의 지능형 작업 할당 프레임워크 제시
- **Robot Constitution 도입**: Constitutional AI를 로봇 안전과 인간 선호도 정렬에 적용한 새로운 접근법
- **하이브리드 데이터 수집 전략**: 원격 조작과 자율 정책을 동적으로 조합하여 인간 감독의 한정된 대역폭을 효율적으로 활용
- **대규모 실제 환경 실증**: 4개 건물, 20+ 로봇, 7개월의 실제 배포로 in-the-wild 데이터 수집의 실현 가능성 입증

## Limitation & Further Study

- **스케일의 제약**: 현재 20+ 로봇에 국한되어 있으며, 수백~수천 규모의 로봇 함대로의 확장성 미검증
- **작업 다양성의 한계**: 주로 조작 관련 작업에 중점이 있으며, 더 복잡한 multi-robot 협업 작업 부족
- **LLM 오류와 hallucination**: LLM의 부정확한 task proposal이나 안전 위반 사례에 대한 정량적 분석 부족
- **안전성 평가의 한계**: Robot Constitution이 모든 edge case를 커버하는지, 실제 인간-로봇 상호작용 시 안전 검증 미흡
- **수렴성과 최적성**: 정책 선택(자율 vs 원격 조작)이 언제 최적인지에 대한 이론적 분석 부족
- **후속 연구 방향**: (1) 수천 규모 로봇 함대로의 확장, (2) LLM hallucination 대응 기법 강화, (3) 안전성 형식 검증, (4) 다중 로봇 협업 작업으로 확대, (5) 수집 데이터의 downstream task 성능 평가 확대

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: AutoRT는 foundation model을 활용한 대규모 로봇 함대 오케스트레이션의 최초 실증 사례로서, 실제 환경에서의 자율성과 안전성의 균형을 이룬 혁신적 시스템이다. 77,000 에피소드의 실제 데이터 수집 및 효율적 인력 활용 달성은 embodied AI의 스케일링에 중대한 기여를 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1355_DreamDojo_A_Generalist_Robot_World_Model_from_Large-Scale_Hu/review]] — AutoRT의 대규모 로봇 데이터 수집과 DreamDojo의 인간 동영상 기반 세계 모델은 모두 대규모 데이터를 통한 로봇 학습 기반을 제공한다.
- 🔗 후속 연구: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — AutoRT의 77,000 에피소드 수집과 BridgeData V2의 대규모 로봇 학습 데이터셋은 실제 로봇 데이터 확장의 연속선상에 있다.
- 🧪 응용 사례: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — Octo의 오픈소스 generalist 로봇 정책은 AutoRT의 대규모 데이터 수집을 활용한 실용적 응용 사례이다.
- 🏛 기반 연구: [[papers/1315_AutoRT_Embodied_Foundation_Models_for_Large_Scale_Orchestrat/review]] — AutoRT의 대규모 자율 데이터 수집 개념이 로봇 foundation model 개발의 핵심 인프라를 제공합니다.
- 🔗 후속 연구: [[papers/1540_RoboGen_Towards_Unleashing_Infinite_Data_for_Automated_Robot/review]] — RoboGen은 AutoRT의 대규모 데이터 수집을 자동화된 로봇 생성과 결합하여 더 확장한 개념입니다.
- 🏛 기반 연구: [[papers/1355_DreamDojo_A_Generalist_Robot_World_Model_from_Large-Scale_Hu/review]] — DreamDojo의 대규모 인간 동영상 학습과 AutoRT의 로봇 함대 데이터 수집은 모두 대규모 데이터 기반 로봇 학습의 기초를 제공한다.
- 🔄 다른 접근: [[papers/1467_Manipulate-Anything_Automating_Real-World_Robots_using_Visio/review]] — AutoRT와 Manipulate-Anything 모두 자동화된 로봇 데이터 생성을 목표하지만 대규모 오케스트레이션 vs 단일 환경 접근의 차이가 있음
- 🔗 후속 연구: [[papers/1484_MuJoCo_Playground/review]] — MuJoCo Playground의 빠른 정책 훈련은 AutoRT의 대규모 로봇 오케스트레이션에 필요한 효율적인 학습 기반을 제공합니다.
- 🧪 응용 사례: [[papers/1493_Neural_Scaling_Laws_in_Robotics/review]] — Neural Scaling Laws의 정량적 분석이 AutoRT의 대규모 로봇 시스템 설계에서 최적 모델 크기 결정에 실용적 지침을 제공한다.
- 🧪 응용 사례: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Open X-Embodiment 데이터셋을 활용하여 AutoRT의 large-scale robot orchestration과 data collection을 수행할 수 있다.
- 🔄 다른 접근: [[papers/1586_TidyBot_Personalized_Robot_Assistance_with_Large_Language_Mo/review]] — 개인화된 로봇 학습을 위한 서로 다른 접근법 - few-shot learning vs large-scale orchestration입니다.
- 🔗 후속 연구: [[papers/1594_Transferring_Foundation_Models_for_Generalizable_Robotic_Man/review]] — AutoRT는 기초 모델의 대규모 로봇 학습 오케스트레이션을 통해 일반화 가능한 조작을 실현하는 확장된 접근법입니다.
- 🏛 기반 연구: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — AutoRT는 DRL 정책을 실제 로봇에 대규모로 배포하는 orchestration 프레임워크로, 실세계 성공 사례 조사의 핵심 기반을 제공합니다.
