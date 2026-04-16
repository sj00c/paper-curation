---
title: "1353_Describe_Explain_Plan_and_Select_Interactive_Planning_with_L"
authors:
  - "Zihao Wang"
  - "Shaofei Cai"
  - "Guanzhou Chen"
  - "Anji Liu"
  - "Xiaojian Ma"
date: "2023.02"
doi: ""
arxiv: ""
score: 4.0
essence: "오픈월드 환경(예: Minecraft)에서 장기 태스크를 수행하는 멀티태스크 에이전트를 위해, LLM 기반의 대화형 계획 방식 DEPS(Describe, Explain, Plan and Select)를 제안하여 복잡한 의존성과 상태 의존적 실행 가능성 문제를 해결한다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "sub/LLM_Task_Planning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2023_Describe, Explain, Plan and Select Interactive Planning with Large Language Models Enables Open-Wor.pdf"
---

# Describe, Explain, Plan and Select: Interactive Planning with Large Language Models Enables Open-World Multi-Task Agents

> **저자**: Zihao Wang, Shaofei Cai, Guanzhou Chen, Anji Liu, Xiaojian Ma, Yitao Liang | **날짜**: 2023-02-03 | **URL**: [https://arxiv.org/abs/2302.01560](https://arxiv.org/abs/2302.01560)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of our proposed interactive planner architecture.*

오픈월드 환경(예: Minecraft)에서 장기 태스크를 수행하는 멀티태스크 에이전트를 위해, LLM 기반의 대화형 계획 방식 DEPS(Describe, Explain, Plan and Select)를 제안하여 복잡한 의존성과 상태 의존적 실행 가능성 문제를 해결한다.

## Motivation

- **Known**: LLM 기반 플래너는 장기 태스크를 서브골 시퀀스로 분해하여 실행할 수 있지만, 오픈월드 환경에서는 복잡한 서브태스크 의존성과 현재 에이전트 상태를 고려하지 못해 실패율이 높다.
- **Gap**: 기존 연구들은 affordance 함수나 scene descriptor를 통해 환경 피드백을 제공하지만 오픈월드 환경에서 여전히 높은 실패율을 보이며, 병렬 서브골의 순서 결정 시 달성 난이도를 고려하지 못한다.
- **Why**: 멀티태스크 에이전트의 일반화 능력은 AGI 개발의 핵심 마일스톤이며, 오픈월드에서의 계획 신뢰성 향상은 현실적 로봇공학 응용에 필수적이다.
- **Approach**: LLM의 계획 생성 후 실패 시 Description(현황 요약), Explanation(오류 위치 파악), Plan(재계획) 과정을 반복하고, 학습 가능한 Selector 모듈로 도달 가능성을 기반으로 병렬 서브골을 순서 지정한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Planning success rates plummet in open worlds due to new challenges.*

- **Zero-shot Minecraft 멀티태스크 성능**: 71개 이상의 Minecraft 태스크를 안정적으로 완료하는 최초의 zero-shot 기반 멀티태스크 에이전트 달성
- **성능 향상**: 동일한 초기 상태와 goal-conditioned 컨트롤러에서 기존 언어 플래너 대비 약 2배 성공률 향상
- **도메인 일반화**: ALFWorld와 tabletop manipulation 등 비개방형 로봇공학 도메인에서 50% 이상의 상대적 성능 개선 달성
- **ObtainDiamond 도전과제**: 기존 계획 기반 에이전트 중 처음으로 challenging ObtainDiamond 태스크 완료

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of our proposed interactive planner architecture.*

- Descriptor 모듈(VLM 기반)이 controller 실패 시 현재 상태를 자연어로 요약하여 LLM에 피드백 제공
- Explainer(LLM*)가 이전 계획의 오류를 식별하고 실패 원인을 설명
- (Re-)Planner가 Descriptor와 Explainer의 정보를 통합하여 계획을 반복적으로 정제
- Goal Selector가 병렬 후보 서브골들의 완료 예상 스텝 수를 바탕으로 각 서브골의 접근 가능성 순위를 매기고 최적 순서 결정
- 단일 컨트롤러(goal-conditioned policy)가 선택된 서브골을 순차 실행
- 환경으로부터 관측을 받아 다음 사이클의 입력으로 활용하는 폐쇄 루프 구조

## Originality

- 기존 LLM 기반 플래너의 단방향 생성 방식에서 벗어나 Description-Explanation-Planning의 대화형 3단계 피드백 루프 도입
- 학습 가능한 Selector 모듈로 상태 의존적 태스크 실행 가능성 문제를 처음으로 명시적으로 해결
- 오픈월드(Minecraft) 환경에서의 멀티태스크 계획 문제의 두 가지 핵심 도전(복잡한 의존성, 상태 의존적 실행 가능성)을 체계적으로 식별하고 분리된 메커니즘으로 대응
- HPM(Historical Planning Memory)과 같은 보조 메커니즘을 통해 긴 실행 지평에서의 계획 일관성 유지

## Limitation & Further Study

- Selector 모듈의 학습에 필요한 레이블 데이터 수집 과정과 데이터 효율성에 대한 상세 분석 부족
- VLM 기반 Descriptor의 계산 비용과 실시간 응답성에 대한 평가 미흡
- 오픈월드 환경 일반화: Minecraft 중심 실험으로 다른 오픈월드 게임이나 환경으로의 전이 가능성 불명확
- 인컨텍스트 학습 방식의 프롬프트 디자인 민감도와 최적 프롬프트 구성에 대한 심층 분석 부재
- Selector 모듈이 완료 스텝 예측에만 의존하며 서브태스크 실패 확률이나 자원 소비 등 다른 요소를 고려하지 못함
- **후속 연구**: 더 경량의 언어 모델을 사용한 DEPS 적응성 탐구, 멀티에이전트 협력 환경으로의 확장, 및 온라인 러닝으로 Selector 동적 개선

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 오픈월드 멀티태스크 계획의 핵심 도전을 명확히 식별하고 LLM 기반의 대화형 계획 프레임워크로 체계적으로 해결하며, Minecraft에서의 획기적 성과와 도메인 간 일반화 능력으로 구체화된 연구이다. 독창적인 3단계 피드백 루프와 상태 의존적 실행 가능성 처리는 LLM 기반 에이전트 설계에 중요한 패턴을 제시한다.

## Related Papers

- 🧪 응용 사례: [[papers/1477_MineDojo_Building_Open-Ended_Embodied_Agents_with_Internet-S/review]] — DEPS의 대화형 계획 방식을 MineDojo 환경에서 실제로 적용하고 검증할 수 있는 플랫폼
- 🏛 기반 연구: [[papers/1623_Voyager_An_Open-Ended_Embodied_Agent_with_Large_Language_Mod/review]] — Voyager의 오픈엔디드 에이전트 개념이 DEPS 대화형 계획 시스템의 설계 기반
- 🏛 기반 연구: [[papers/1416_Grounding_Large_Language_Models_in_Interactive_Environments/review]] — 대화형 환경에서의 LLM 기반 계획 수립의 기본 원리와 방법론을 제공하여 DEPS의 이론적 기반이 됩니다.
- 🏛 기반 연구: [[papers/1418_Guiding_Pretraining_in_Reinforcement_Learning_with_Large_Lan/review]] — 대규모 언어 모델의 상호작용적 환경 가이드 개념이 DEPS의 LLM 기반 대화형 계획의 기초가 됩니다.
