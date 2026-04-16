---
title: "1556_RT-H_Action_Hierarchies_Using_Language"
authors:
  - "Suneel Belkhale"
  - "Tianli Ding"
  - "Ted Xiao"
  - "Pierre Sermanet"
  - "Quon Vuong"
date: "2024.03"
doi: ""
arxiv: ""
score: 4.0
essence: "RT-H는 로봇 모방 학습에서 언어 기반 행동 계층 구조를 제안하여, 고수준 작업 설명과 저수준 로봇 액션 사이의 중간 단계로 '언어 모션(language motion)'을 예측함으로써 다양한 작업 간 데이터 공유를 개선한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Instruction-Following_Robot_Navigation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Belkhale et al._2024_RT-H Action Hierarchies Using Language.pdf"
---

# RT-H: Action Hierarchies Using Language

> **저자**: Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, Dorsa Sadigh | **날짜**: 2024-03-04 | **URL**: [https://arxiv.org/abs/2403.01823](https://arxiv.org/abs/2403.01823)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Given a task in language like “close the pistachio jar” and an image of the scene, RT-H utilizes a Vision Langua*

RT-H는 로봇 모방 학습에서 언어 기반 행동 계층 구조를 제안하여, 고수준 작업 설명과 저수준 로봇 액션 사이의 중간 단계로 '언어 모션(language motion)'을 예측함으로써 다양한 작업 간 데이터 공유를 개선한다.

## Motivation

- **Known**: 최근 로봇 모방 학습에서 언어 조건부 정책(language-conditioned policies)이 시각적 관찰과 고수준 작업 설명으로부터 액션을 예측하는 데 사용되고 있으며, 의미적으로 유사한 작업들 간 데이터 공유를 통해 성능을 향상시킨다.
- **Gap**: 작업이 의미적으로 더 다양해질수록(예: '콜라 캔 집기' vs '컵 붓기') 작업 설명 간 데이터 공유가 어려워져 많은 시연 데이터가 필요하며, 이는 학습 효율성을 제한한다.
- **Why**: 다양한 멀티태스크 데이터셋에서 효과적인 데이터 공유 메커니즘을 개발하면 로봇의 샘플 효율성과 강건성을 크게 향상시킬 수 있으며, 더 나아가 런타임 중 인간의 언어 기반 피드백을 통한 정정이 가능해진다.
- **Approach**: RT-H는 vision-language model(VLM) 기반의 두 단계 계층 구조를 도입하여, 먼저 고수준 작업과 시각 관찰로부터 fine-grained한 언어 모션을 예측하고, 이 언어 모션을 추가 조건으로 하여 최종 로봇 액션을 예측한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Results on Diverse+Kitchen multi-task dataset, consisting of eight challenging evaluation tasks. 95% Wilson Scor*

- **다양한 멀티태스크 데이터셋에서 성능 개선**: RT-2 대비 15% 향상된 성공률 달성
- **언어 모션 기반 정정의 높은 효율성**: 언어 모션 보정만으로도 거의 완벽한 성공률(near perfect success rates) 달성
- **대화형 학습의 우수성**: IWR 등 기존 interactive imitation learning 방법 대비 50% 향상된 성능 달성
- **장면 및 객체 변동에 대한 우수한 일반화**: RT-2보다 변화된 환경에 대한 더 나은 일반화 능력 입증
- **자동 언어 모션 추출**: 로봇 고유감각(proprioception)으로부터 2500개 이상의 언어 모션을 수동 주석 없이 자동 추출

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: RT-H Overview. Left: Our method leverages language to create an action hierarchy for policy learning. We separat*

- RT-2 VLM 백본을 기반으로 하는 end-to-end 프레임워크 구축
- 단일 모델을 통해 언어 모션 쿼리와 액션 쿼리 모두 수행하여 인터넷 규모 지식 활용
- 로봇 proprioception 데이터로부터 자동화된 언어 모션 추출 방식 개발
- 각 단계에서 관찰, 고수준 작업 설명, 예측된 언어 모션을 모두 조건으로 하여 액션 예측
- 인간 개입 시 언어 모션 수준에서 정정을 받고 이를 학습하는 메커니즘 구현

## Originality

- **계층 구조의 세밀성**: 기존 작업-액션 직접 매핑에서 벗어나 중간 단계인 언어 모션 도입으로 더 세밀한 데이터 공유 구조 제시
- **문맥 의존적 언어 모션**: 고정된 프리미티브가 아닌 현재 작업과 장면에 따라 학습되는 동적 언어 모션 개념 제안
- **인간 피드백의 새로운 패러다임**: 저수준 액션 정정이 아닌 언어 모션 수준의 정정을 통해 더 직관적이고 학습하기 쉬운 상호작용 가능
- **자동 언어 모션 추출**: 수동 주석 없이 proprioception 데이터로부터 대규모 언어 모션 라이브러리 자동 생성

## Limitation & Further Study

- 언어 모션 추출 방식이 proprioception 데이터에 의존하므로, 다른 유형의 로봇이나 센서 구성에 대한 확장성 제한 가능성
- 자동 추출된 언어 모션의 품질과 의미적 일관성에 대한 상세한 분석 및 평가 부족
- 인간 개입 학습에 있어 다양한 사용자 그룹(전문가 vs 비전문가)에 대한 광범위한 평가 미흡
- 언어 모션 계층의 추가에 따른 계산 오버헤드 분석 및 실시간 제어 환경에서의 실용성 평가 필요
- 후속 연구: 다양한 로봇 플랫폼으로의 확장, 언어 모션의 자동 추출 정확도 개선, 장기 수행 작업에 대한 계층 구조 확대 검토

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RT-H는 언어를 활용한 행동 계층 구조라는 우아한 아이디어를 통해 멀티태스크 로봇 학습의 데이터 효율성을 크게 향상시키며, 인간 개입의 새로운 패러다임까지 제시하여 실제 로봇 시스템에서의 적용 가능성이 높다.

## Related Papers

- 🔗 후속 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — RT-1의 기본 robotics transformer를 language motion 중간 표현으로 확장하여 더 효과적인 작업 간 데이터 공유와 계층적 제어를 달성한다.
- 🔄 다른 접근: [[papers/1328_Chain-of-Action_Trajectory_Autoregressive_Modeling_for_Robot/review]] — 로봇 학습에서 language-based action hierarchy vs trajectory autoregressive modeling이라는 서로 다른 행동 표현 및 학습 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1566_Scaling_Up_and_Distilling_Down_Language-Guided_Robot_Skill_A/review]] — language-guided robot skill learning의 기초 이론을 제공하여 RT-H의 언어 기반 행동 계층 구조와 skill 간 데이터 공유에 필요한 방법론적 토대를 제공한다.
- 🔗 후속 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-H의 언어 기반 행동 계층 구조는 RT-2의 언어-행동 통합 방식을 더욱 세밀하게 발전시킨 접근법이다.
- 🔄 다른 접근: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — CoT-VLA는 RT-H와 유사하게 중간 추론 단계를 사용하지만 시각적 사고 체인을 활용하는 다른 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1618_VLA-Reasoner_Empowering_Vision-Language-Action_Models_with_R/review]] — VLA-Reasoner는 RT-H의 언어 기반 계층과 유사한 추론 능력을 VLA 모델에 통합하는 대안적 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1584_ThinkAct_Vision-Language-Action_Reasoning_via_Reinforced_Vis/review]] — ThinkAct는 RT-H와 같이 고수준과 저수준 행동을 연결하지만 강화 시각적 추론을 통한 다른 메커니즘을 사용한다.
- 🏛 기반 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Code as Policies의 언어 기반 로봇 제어 개념이 RT-H의 언어 모션 예측과 행동 계층 구조 설계에 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1422_Hi_Robot_Open-Ended_Instruction_Following_with_Hierarchical/review]] — 로봇의 계층적 제어에서 RT-H는 언어 기반 행동 계층으로, Hi Robot은 오픈엔드 instruction following으로 접근한다.
- 🔄 다른 접근: [[papers/1321_Bootstrap_Your_Own_Skills_Learning_to_Solve_New_Tasks_with_L/review]] — 둘 다 hierarchical action을 다루지만 BOSS는 스킬 체이닝에, RT-H는 language-guided action hierarchy에 중점을 둡니다.
