---
title: "1328_Deep_Reinforcement_Learning_for_Bipedal_Locomotion_A_Brief_S"
authors:
  - "Lingfan Bao"
  - "Joseph Humphreys"
  - "Tianhu Peng"
  - "Chengxu Zhou"
date: "2024.04"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 bipedal robot의 locomotion을 위한 Deep Reinforcement Learning(DRL) 기반 프레임워크를 체계적으로 분류, 비교, 분석하는 survey이며, end-to-end와 hierarchical 제어 방식으로 구분하여 각 프레임워크의 구성, 강점, 한계를 평가한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bao et al._2024_Deep Reinforcement Learning for Bipedal Locomotion A Brief Survey.pdf"
---

# Deep Reinforcement Learning for Bipedal Locomotion: A Brief Survey

> **저자**: Lingfan Bao, Joseph Humphreys, Tianhu Peng, Chengxu Zhou | **날짜**: 2024-04-25 | **URL**: [https://arxiv.org/abs/2404.17070](https://arxiv.org/abs/2404.17070)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Classification of DRL-based control schemes. The approaches are broadly categorised into two main paradigms: end*

본 논문은 bipedal robot의 locomotion을 위한 Deep Reinforcement Learning(DRL) 기반 프레임워크를 체계적으로 분류, 비교, 분석하는 survey이며, end-to-end와 hierarchical 제어 방식으로 구분하여 각 프레임워크의 구성, 강점, 한계를 평가한다.

## Motivation

- **Known**: DRL은 bipedal locomotion을 크게 발전시켰으며, 2020년 Cassie에서 처음 successful sim-to-real transfer가 달성되었다. 전통적인 model-based 방법(LIPM, MPC, Trajectory Optimization)은 빠른 수렴과 예측 능력을 제공하지만 동적으로 복잡한 환경에서의 적응성이 제한적이다.
- **Gap**: 현재 DRL 기반 bipedal locomotion 연구는 highly fragmented되어 있으며, training pipeline, reward formulation, observation space, evaluation setup의 불일치로 인해 체계적 벤치마킹과 일반화 가능한 locomotion 개발이 지연되고 있다. 다양한 morphology, terrain, task에 걸친 일반화와 robustness를 달성하는 unified framework이 부재하다.
- **Why**: Bipedal humanoid robot은 인간 환경에서의 seamless interaction, manufacturing, healthcare, search-and-rescue 등 광범위한 실제 응용 가치를 가지고 있으며, 일반화되고 적응 가능한 제어 프레임워크의 개발은 이러한 실제 배포의 기반이 된다.
- **Approach**: 본 survey는 DRL 기반 bipedal locomotion 프레임워크를 end-to-end(상태를 joint-level 제어 출력으로 직접 매핑)와 hierarchical(multi-layer decision-making으로 분해)로 분류하고, 각 범주에서의 학습 접근법, 계층 구조, learning-based 및 model-based 방법의 통합을 분석한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Classification of DRL-based control schemes. The approaches are broadly categorised into two main paradigms: end*

- **프레임워크 분류체계**: End-to-end와 hierarchical 제어 방식으로 DRL 기반 bipedal locomotion 프레임워크를 체계적으로 분류하고 categorical taxonomy 제시
- **학습 패러다임 분석**: Reference-based learning(TO 또는 motion-capture 데이터 기반)과 reference-free learning(scratch에서 자율 학습)의 두 주요 paradigm을 식별 및 비교
- **Hybrid 아키텍처 평가**: Learning-based와 model-based 방법을 결합한 hybrid 제어(cascade-structure, feedback-control hybrid) 설계의 강점과 한계 분석
- **연구 갭 및 미래 방향 제시**: Generalization, adaptability, robustness 달성을 위한 통합 프레임워크 개발의 필요성을 명확히 하고 consolidated methodology 제안

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Representative bipedal and humanoid robots illustrat-*

- 2018-2024년 최근 5년간의 문헌을 Google Scholar, IEEE Xplore, Web of Science, arXiv, CoRL, RSS, ICRA, IROS, Humanoids 등으로부터 체계적으로 검색 및 선별
- Deep Reinforcement Learning" 또는 "Reinforcement Learning"과 "Bipedal Locomotion", "Bipedal Walking", "Humanoid Robot", "Legged Robot" 등의 키워드 조합으로 검색
- 선정 기준: (1) Bipedal robot 특정 DRL framework 연구, (2) 시뮬레이션 및 물리적 robot 관련 연구, (3) Sim-to-real transfer 개선 연구, (4) 신뢰성 있는 데이터베이스 및 주요 학회 출판물
- 각 프레임워크의 composition, strengths, limitations, capabilities를 end-to-end(learning approach 기반) 및 hierarchical(layered structure 기반)로 평가
- 참고 로봇 플랫폼: Cassie, Digit, H1, G1, Atlas 등 diverse morphologies와 actuator 특성을 통한 cross-platform 분석

## Originality

- DRL 기반 bipedal locomotion에 특화된 첫 comprehensive survey로, 기존의 일반 robotics RL review나 model-based method review와 차별화
- End-to-end와 hierarchical 제어를 명확히 분류하고, 각 범주 내에서 learning paradigm과 integration strategy의 세부 분석 제공
- Unified framework의 개념을 단순한 최종 목표가 아닌 fragmented methodology를 organize하는 conceptual scaffold로 재정의하여 새로운 관점 제시
- Sim-to-real transfer, reference-based vs. reference-free learning, hybrid control 등 핵심 research dimensions을 체계적으로 정리

## Limitation & Further Study

- Survey 성격으로 인해 새로운 알고리즘이나 이론적 기여 부재; 기존 문헌의 분류 및 분석에 집중
- 2024년 4월까지의 문헌만 포함되어 그 이후의 rapid advancements(특히 transformer 기반 방법, vision-based policy 등)를 놓칠 가능성
- Generalization과 robustness 측정의 표준화된 벤치마크 부재로, 각 framework 간 정량적 비교가 제한적일 수 있음
- Real-world 배포 시 발생하는 실제 friction, wear, communication latency 등의 현실 요소에 대한 충분한 논의 부족
- **후속 연구 방향**: (1) Unified framework의 구체적 구현과 open-source toolkit 개발, (2) Cross-morphology generalization을 위한 standardized evaluation protocol 제정, (3) Transfer learning과 meta-learning 기법의 bipedal locomotion 적용, (4) Vision-language model 활용한 high-level task instruction 처리, (5) Real-world 환경의 uncertainties를 다루는 robust DRL 알고리즘 개발

## Evaluation

- Novelty: 3/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 survey는 DRL 기반 bipedal locomotion 분야의 fragmented 연구를 체계적으로 정리하고 unified framework을 향한 명확한 research agenda를 제시하는 가치 있는 종합 분석이다. End-to-end와 hierarchical 분류 체계, learning paradigm 비교, hybrid 아키텍처 평가는 이 분야의 종사자들에게 실질적인 guidance를 제공하며, 향후 generalisable bipedal locomotion 개발의 기초를 마련한다.

## Related Papers

- 🧪 응용 사례: [[papers/1526_Real-World_Humanoid_Locomotion_with_Reinforcement_Learning/review]] — 강화학습을 휴머노이드 로코모션이라는 구체적 영역에 적용한 사례를 제공한다.
- 🔗 후속 연구: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — 로봇공학을 위한 DRL의 실제 응용으로 이족 보행을 확장한다.
- 🏛 기반 연구: [[papers/1418_Guiding_Pretraining_in_Reinforcement_Learning_with_Large_Lan/review]] — 강화학습에서 언어 모델을 활용한 사전학습 가이드의 기초를 제공한다.
