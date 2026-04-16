---
title: "1550_Robots_Enact_Malignant_Stereotypes"
authors:
  - "Andrew Hundt"
  - "William Agnew"
  - "Vicky Zeng"
  - "Severin Kacianka"
  - "Matthew Gombolay"
date: "2022.07"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 CLIP 같은 대규모 기초 모델을 활용하는 로봇 조작 시스템이 실제 물리적 환경에서 인종, 성별 고정관념과 과학적으로 입증되지 않은 골상학을 체계적으로 재현하는 것을 처음으로 실증적으로 입증한다."
tags:
  - "cat/Robot_Policy_Learning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Robotic_Policy_Scaling"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Hundt et al._2022_Robots Enact Malignant Stereotypes.pdf"
---

# Robots Enact Malignant Stereotypes

> **저자**: Andrew Hundt, William Agnew, Vicky Zeng, Severin Kacianka, Matthew Gombolay | **날짜**: 2022-07-23 | **URL**: [https://arxiv.org/abs/2207.11569](https://arxiv.org/abs/2207.11569)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. An example trial showing harmful robot behavior that is, in aggregate, racially stratified like White supremacis*

본 논문은 CLIP 같은 대규모 기초 모델을 활용하는 로봇 조작 시스템이 실제 물리적 환경에서 인종, 성별 고정관념과 과학적으로 입증되지 않은 골상학을 체계적으로 재현하는 것을 처음으로 실증적으로 입증한다.

## Motivation

- **Known**: ML 시스템에서 컴퓨터 비전, NLP, CLIP 같은 대규모 이미지-캡션 모델의 편향성과 차별이 널리 문서화되어 있다. 로봇에 대한 해로운 영향도 논의되었지만 실증적 연구가 부족하다.
- **Gap**: 기초 모델을 탑재한 로봇이 물리적 세계에서 어떻게 편향을 실행하는지에 대한 첫 번째 대규모 실증 평가 연구가 부재하며, 이는 실시간 로봇 배포에서 긴급한 문제다.
- **Why**: 로봇은 소프트웨어의 모든 편향 문제를 가지면서도 신체화로 인해 돌이킬 수 없는 물리적 해를 야기할 수 있으며, 자율 로봇에는 인간 개입이 없어 위험성이 극대화된다.
- **Approach**: CLIP 기반 로봇 조작 방법에 대한 감시 실험을 수행하여, 인종과 성별로 다양한 인간 얼굴 이미지가 있는 물체와 고정관념 용어가 포함된 작업 지시어를 제시하고, 로봇의 행동 패턴을 분석한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. An example trial showing harmful robot behavior that is, in aggregate, racially stratified like White supremacis*

- **첫 실증 연구**: 배포된 로봇이 인종, 성별, 골상학적 악성 고정관념을 대규모로 실행하는 것을 최초 입증
- **벤치마크 개발**: 악성 고정관념의 좁지만 중요한 부분집합에 대해 기초 모델을 평가하는 새로운 벤치마크 제시
- **상태 최적화 성과**: 자동 정지(e-stop)된 로봇이 고정관념적 행동을 결코 실행하지 않음으로써 주요 작업에서 최첨단 성능 달성
- **학제 간 종합**: 로봇공학과 AI 윤리 간 격차를 드러내고 설계 정의, 정체성 안전 평가, 윤리 검토의 필요성 강조
- **정책 제언**: 해로운 로봇 학습 방법의 일시 중지, 재설계, 단계적 폐지 및 포괄적 정책 변경을 촉구

## How

![Figure 2](figures/fig2.webp)

*Fig. 2. Experiment summary for all commands, counting objects placed in the brown box across combination pairs of race a*

- CLIP 기반 로봇 조작 시스템에 다양한 인종·성별 얼굴 이미지가 있는 물체 제시
- 범죄자를 갈색 상자에 넣기' 같은 고정관념 용어 포함 자연어 지시어 결합", '각 명령에 대한 로봇의 물체 선택 및 배치 우선순위를 성별·인종별로 정량 분석
- 자동 정지 로봇의 거부 행동 성능과 비교하여 벤치마킹
- 과학기술사회학(STS), 비판 이론, 로봇공학, AI 윤리를 종합한 사회기술적 분석

## Originality

- 로봇이 물리적으로 편향을 실행하는 방식에 대한 첫 번째 체계적 실증 연구
- 악성 고정관념을 평가하기 위한 새로운 벤치마크 설계
- 로봇공학과 AI 윤리, 설계 정의, 정체성 안전 평가 프레임워크를 통합하는 학제 간 접근
- 기초 모델의 편향이 로봇 자율성에서 물리적 해로 변환되는 과정을 구체적으로 기술

## Limitation & Further Study

- 한 가지 CLIP 기반 로봇 조작 방법만 감시하여 결과의 일반화 가능성 제한 가능
- 실제 배포 로봇에서의 대규모 현장 실험이 부재하며 제어된 실험 환경에 국한
- 고정관념 용어 선택과 얼굴 이미지 선정에서의 주관적 판단이 영향을 미칠 수 있음
- 로봇이 거부 또는 정지 명령을 따르도록 구현하는 기술적 방법에 대한 상세 제시 부족
- 후속 연구는 다양한 로봇 플랫폼과 기초 모델 확대, 실제 배포 환경에서의 검증, 설계 정의·정체성 안전 평가 프레임워크의 실제 개발과 적용 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 로봇공학에서 기초 모델의 편향이 물리적 세계에서 실제로 재현되는 현상을 처음으로 실증적으로 입증하며, 로봇 자율성의 위험성을 강조하는 중요한 기여다. 학제 간 접근과 명확한 정책 제언으로 로봇공학 공동체의 우선적 행동 변화를 촉구하는 의미 있는 작업이다.

## Related Papers

- 🔗 후속 연구: [[papers/1458_LLM-Driven_Robots_Risk_Enacting_Discrimination_Violence_and/review]] — 로봇이 악성 고정관념을 재현한다는 발견이 LLM 기반 로봇의 차별과 폭력 위험으로 확장되어 더 광범위한 AI 안전성 문제를 드러낸다.
- 🔄 다른 접근: [[papers/1440_Jailbreaking_LLM-Controlled_Robots/review]] — 두 연구 모두 LLM/VLM 제어 로봇의 안전성 문제를 다루지만 하나는 편향, 다른 하나는 의도적 공격이라는 다른 위협을 분석한다.
- 🏛 기반 연구: [[papers/1501_On_the_Vulnerability_of_LLMVLM-Controlled_Robotics/review]] — LLM/VLM 제어 로봇의 취약성 분석이 고정관념 재현 문제를 더 광범위한 보안 위협의 맥락에서 이해하는 기반을 제공한다.
- 🏛 기반 연구: [[papers/1440_Jailbreaking_LLM-Controlled_Robots/review]] — 로봇이 악의적 고정관념을 행동으로 구현하는 위험성의 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1458_LLM-Driven_Robots_Risk_Enacting_Discrimination_Violence_and/review]] — LLM 기반 로봇의 차별과 폭력 위험이 Robots Enact Malignant Stereotypes 연구에서 제기된 편향 문제를 더욱 구체적으로 확장한다.
- ⚖️ 반론/비판: [[papers/1501_On_the_Vulnerability_of_LLMVLM-Controlled_Robotics/review]] — 로봇의 악의적 스테레오타입 문제와 달리 이 연구는 기술적 취약성에 초점을 맞춰 LLM/VLM 로봇 시스템의 다른 측면을 다룬다.
