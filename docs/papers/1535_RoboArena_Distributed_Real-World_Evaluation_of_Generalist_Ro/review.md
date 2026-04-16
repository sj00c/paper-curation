---
title: "1535_RoboArena_Distributed_Real-World_Evaluation_of_Generalist_Ro"
authors:
  - "Pranav Atreya"
  - "Karl Pertsch"
  - "Tony Lee"
  - "Moo Jin Kim"
  - "Arhan Jain"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "RoboArena는 분산된 평가자 네트워크를 통해 실제 환경에서 일반화된 로봇 정책을 pairwise 비교하고 집계하여 정책 순위를 도출하는 크라우드소싱 기반 평가 프레임워크이다. 600회 이상의 실제 로봇 평가를 통해 중앙 집중식 평가보다 정확한 정책 순위를 제공함을 입증했다."
tags:
  - "cat/Robot_Policy_Learning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Robotic_Policy_Scaling"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Atreya et al._2025_RoboArena Distributed Real-World Evaluation of Generalist Robot Policies.pdf"
---

# RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies

> **저자**: Pranav Atreya, Karl Pertsch, Tony Lee, Moo Jin Kim, Arhan Jain, Artur Kuramshin, Clemens Eppner, Cyrus Neary, Edward Hu, Fabio Ramos, Jonathan Tremblay, Kanav Arora, Kirsty Ellis, Luca Macesanu, Marcel Torne Villasevil, Matthew Leonard, Meedeum Cho, Ozgur Aslan, Shivin Dass, Jie Wang, William Reger, Xingfang Yuan, Xuning Yang, Abhishek Gupta, Dinesh Jayaraman, Glen Berseth, Kostas Daniilidis, Roberto Martin-Martin, Youngwoon Lee, Percy Liang, Chelsea Finn, Sergey Levine | **날짜**: 2025-06-22 | **URL**: [https://arxiv.org/abs/2506.18123](https://arxiv.org/abs/2506.18123)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: We present RoboArena, a distributed real-world evaluation framework for generalist robot*

RoboArena는 분산된 평가자 네트워크를 통해 실제 환경에서 일반화된 로봇 정책을 pairwise 비교하고 집계하여 정책 순위를 도출하는 크라우드소싱 기반 평가 프레임워크이다. 600회 이상의 실제 로봇 평가를 통해 중앙 집중식 평가보다 정확한 정책 순위를 제공함을 입증했다.

## Motivation

- **Known**: 기존 로봇 벤치마크는 고정된 작업과 환경에 대한 표준화된 평가나 중앙 집중식 챌린지에 의존하며, 일반화된 정책을 광범위한 작업과 환경에서 평가하기 어렵다. 최근 언어 모델과 vision-language 모델 분야에서는 Chatbot Arena와 같은 크라우드소싱 벤치마크가 성공했다.
- **Gap**: 일반화된 로봇 정책의 평가는 표준화된 환경 재현의 어려움과 확장성 제약으로 인해 종합적이고 신뢰할 수 있는 성능 비교가 불가능하다. 로봇 분야에서는 아직 크라우드소싱 기반의 분산 평가 접근법이 부재하다.
- **Why**: 일반화된 로봇 정책이 다양한 작업과 환경에서 수행할 수 있도록 발전함에 따라, 이들의 실제 성능을 공정하고 포괄적으로 평가할 새로운 방식이 필요하다. 분산 평가는 확장성, 신뢰성, 접근성을 개선하여 로봇 정책 개발 생태계를 촉진할 수 있다.
- **Approach**: 평가자들이 자유롭게 작업과 환경을 선택하여 pairwise double-blind 비교를 수행하고, 다양한 작업과 환경에 걸친 선호도 피드백을 집계하여 정책 순위를 도출한다. DROID 로봇 플랫폼을 사용하여 7개 학술 기관의 평가자 네트워크에서 7개의 일반화 정책을 평가했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: We present RoboArena, a distributed real-world evaluation framework for generalist robot*

- **분산 평가 프레임워크 개발**: 600회 이상의 pairwise 실제 로봇 평가를 통해 중앙 집중식 평가보다 정확한 정책 순위를 달성했으며, 같은 에피소드 수에서 더 높은 품질의 순위를 제공함
- **확장성 및 신뢰성**: 표준화된 환경 조건 없이도 double-blind 평가와 집계를 통해 신뢰할 수 있는 결과를 도출하고, 여러 기관의 평가자가 비동기적으로 기여 가능
- **종합 평가 데이터**: 4284개 평가 에피소드를 포함한 현재까지 가장 광범위한 일반화 로봇 정책 평가 제공
- **LLM 기반 정성 분석**: 평가 결과로부터 정책의 강점과 약점을 LLM 보조 분석을 통해 추출

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Pipeline for extracting qualitative policy characteristics from RoboArena’s rich evaluation*

- 7개 학술 기관에서 분산된 평가자 네트워크 구축 및 DROID 로봇 플랫폼 사용
- 평가자가 선택한 임의의 작업과 환경에서 두 정책 간 pairwise A/B 비교 수행
- 각 비교에서 선호도와 자유 형식의 언어 설명 수집
- Pairwise 비교 결과를 집계하여 전역 정책 순위 계산 (Bradley-Terry 모델 또는 유사 접근법 사용)
- LLM을 사용하여 평가 결과의 자유 형식 설명으로부터 정책의 정성적 특성, 강점, 약점 추출
- Oracle 순위(모든 정책을 모든 작업에서 평가)와의 비교를 통해 방법의 정확성 검증

## Originality

- 로봇 정책 평가 분야에서 크라우드소싱 분산 접근법의 첫 적용으로, 언어 모델 벤치마크(Chatbot Arena)의 성공 패턴을 로봇 분야에 맞게 적응
- 표준화된 환경 재현 없이도 pairwise 비교를 통해 신뢰할 수 있는 순위를 도출하는 혁신적인 방법론
- Double-blind 평가를 통해 평가자 편향을 완화하고, 여러 기관의 분산 네트워크로 신뢰성을 강화
- 개방형 커뮤니티 기반 평가 시스템으로 지속적인 확장과 참여가 가능한 플랫폼 구축

## Limitation & Further Study

- 평가 초기 단계로 7개 정책만 평가됨 - 향후 더 많은 정책 포함 필요
- DROID 로봇 플랫폼에 국한된 실험 - 다른 로봇 하드웨어 플랫폼으로의 확장 미미
- 평가자의 주관성과 개인차로 인한 변동성 - 더 정교한 집계 알고리즘이나 평가자 교육 프로토콜 개발 필요
- 작업 선택의 편향 가능성 - 특정 카테고리의 작업이 과다/과소 평가될 수 있음
- 정량적 성능 메트릭 부재 - 정성적 평가에만 의존하여 세부 성능 분석 제한
- 후속 연구: 더 많은 정책 및 기관 참여, 다양한 로봇 플랫폼 지원, 평가자 편향 최소화 방법론 개발, 작업 선택 편향 완화 메커니즘

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RoboArena는 일반화 로봇 정책의 평가라는 중요한 문제에 대해 혁신적인 분산 크라우드소싱 접근법을 제시하며, 600회의 실제 로봇 평가를 통해 방법의 효과성을 입증했다. 오픈 커뮤니티 플랫폼으로서 로봇 정책 벤치마킹 생태계에 상당한 기여를 할 수 있는 획기적인 연구이다.

## Related Papers

- 🔄 다른 접근: [[papers/1314_AutoEval_Autonomous_Evaluation_of_Generalist_Robot_Manipulat/review]] — RoboArena의 분산 평가와 AutoEval의 자율 평가는 로봇 정책 성능 측정을 위한 서로 다른 자동화 접근법이다.
- 🏛 기반 연구: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — VLABench의 language-conditioned robotics 벤치마크 설계가 RoboArena의 실제 환경 평가 프레임워크의 이론적 기반이다.
- 🔗 후속 연구: [[papers/1386_Evaluating_Real-World_Robot_Manipulation_Policies_in_Simulat/review]] — 시뮬레이션 기반 로봇 정책 평가를 실제 환경의 분산 평가로 확장하여 더 현실적인 성능 검증을 제공한다.
- 🔄 다른 접근: [[papers/1546_Robot_Utility_Models_General_Policies_for_Zero-Shot_Deployme/review]] — RoboArena와 함께 범용 로봇 정책의 실제 평가를 다루지만 RUM은 제로샷 배포에, RoboArena는 분산 평가에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1629_Whom_to_Trust_Elective_Learning_for_Distributed_Gaussian_Pro/review]] — Pri-GP의 분산 신뢰 기반 학습을 로봇 평가 환경으로 확장하여 다중 에이전트 로봇 시스템의 신뢰성 있는 협력을 가능하게 한다.
- 🧪 응용 사례: [[papers/1314_AutoEval_Autonomous_Evaluation_of_Generalist_Robot_Manipulat/review]] — 분산 실세계 일반화 로봇 평가 시스템의 구체적인 적용 사례입니다.
