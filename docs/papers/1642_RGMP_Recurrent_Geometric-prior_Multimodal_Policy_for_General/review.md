---
title: "1642_RGMP_Recurrent_Geometric-prior_Multimodal_Policy_for_General"
authors:
  - "Xuetao Li"
  - "Wenke Huang"
  - "Nengyuan Pan"
  - "Kaiyan Zhao"
  - "Songhua Yang"
date: "2025.11"
doi: ""
arxiv: ""
score: 4.0
essence: "기하학적 추론과 데이터 효율성을 결합한 RGMP는 humanoid robot 조작을 위해 Geometric-prior Skill Selector와 Adaptive Recursive Gaussian Network를 통합하여 87% 성공률과 5배 데이터 효율을 달성한다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "sub/Latent_Human_Motion"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2025_RGMP Recurrent Geometric-prior Multimodal Policy for Generalizable Humanoid Robot Manipulation.pdf"
---

# RGMP: Recurrent Geometric-prior Multimodal Policy for Generalizable Humanoid Robot Manipulation

> **저자**: Xuetao Li, Wenke Huang, Nengyuan Pan, Kaiyan Zhao, Songhua Yang, Yiming Wang, Mengde Li, Mang Ye, Jifeng Xuan, Miao Li | **날짜**: 2025-11-12 | **URL**: [https://arxiv.org/abs/2511.09141](https://arxiv.org/abs/2511.09141)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Pipeline of RGMP. Upon receiving a speech command, the robot utilizes GSS to identify and localize the target*

기하학적 추론과 데이터 효율성을 결합한 RGMP는 humanoid robot 조작을 위해 Geometric-prior Skill Selector와 Adaptive Recursive Gaussian Network를 통합하여 87% 성공률과 5배 데이터 효율을 달성한다.

## Motivation

- **Known**: Vision-Language Model은 의미론적 작업 계획에 능하지만 공간-기하학적 추론이 부족하며, diffusion model과 transformer는 높은 데이터 요구량과 계산 비용으로 인해 실제 배포가 제한된다.
- **Gap**: 현재 데이터 기반 방법들은 unseen scenario에서의 기하학적 추론을 무시하고 robot-target 관계를 비효율적으로 모델링하며, 제한된 데모에서의 데이터 효율적인 visuomotor 제어와 기하학적 일관성을 갖춘 skill 선택이 결여되어 있다.
- **Why**: Humanoid robot이 실제 환경에서 diverse한 작업을 효율적으로 수행하려면 기하학적 추론 능력과 sparse demonstration으로부터의 학습이 필수적이며, 이는 데이터 수집 비용 절감과 cross-domain 일반화를 가능하게 한다.
- **Approach**: GSS는 geometric inductive bias를 VLM에 주입하여 shape 기반 skill 선택을 수행하고, ARGN은 Rotary Position Embedding과 adaptive decay mechanism을 활용하여 recursive global spatial relationship을 모델링하며 GMM으로 6-DoF 궤적을 compact하게 인코딩한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of our framework. By applying seman-*

- **Geometric-prior Skill Selector (GSS)**: 20개의 규칙 기반 기하학적 제약만으로 VLM을 강화하여 unseen scene에서 geometric consistency를 만족하는 적응적 skill sequence를 생성
- **Adaptive Recursive Gaussian Network (ARGN)**: Rotary Position Embedding과 adaptive decay mechanism을 통해 vanishing gradient 문제를 해결하고 task-critical patch의 가중치를 동적으로 증폭
- **실시간 성능**: Humanoid robot과 desktop dual-arm robot에서 87% task success rate 달성 및 state-of-the-art 대비 5배 높은 데이터 효율
- **Cross-domain 일반화**: Geometric-semantic reasoning과 recursive Gaussian adaptation의 결합으로 unseen object에 대한 robust generalization 실현

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Pipeline of RGMP. Upon receiving a speech command, the robot utilizes GSS to identify and localize the target*

- VLM의 low-rank geometric adapter를 통해 object shape와 좌표 정보를 기반으로 pretrained skill library에서 parameterized skill 선택
- Spatial Mixing Block에서 RoPE로 각 image patch와 최종 action 간의 implicit association을 설정
- Recursive computation으로 첫 번째부터 마지막 visual patch까지 progressive하게 global spatial relationship 모델링
- Adaptive Decay Mechanism으로 historical memory의 decay rate를 동적으로 제어하여 vanishing gradient 완화
- Gaussian Mixture Model로 6-DoF robotic arm의 6개 joint를 각각 제어하는 distinct motion을 approximate
- Multi-scale visual cue를 hierarchical fusion block으로 retaining한 후 GMM encoder에 공급하여 goal-conditional density modeling 수행

## Originality

- 기하학적 추론과 의미론적 task planning을 명시적으로 연결하는 geometric-object decomposition mechanism이 처음 제시됨
- Adaptive decay mechanism을 통해 recursive computation의 vanishing gradient 문제를 로봇 학습 맥락에서 해결한 novel approach
- RoPE와 recursive computation을 결합하여 directional spatial dependency를 temporally-consistent latent space에서 캡처하는 독창적인 설계
- GMM을 통한 hierarchical Gaussian process로 robot-object interaction을 compact하게 parameterize하는 새로운 표현

## Limitation & Further Study

- Geometric prior가 20개 규칙 기반 제약으로 고정되어 있어 더 복잡한 기하학적 시나리오로의 확장성이 제한될 수 있음
- 평가가 두 개의 robotic platform에만 제한되어 다양한 embodiment에 대한 일반화 능력 검증 부족
- Sparse demonstration 환경에서의 성능 한계점(예: 최소 몇 개의 demo가 필요한지)이 명시되지 않음
- 실시간 inference 속도와 computational cost에 대한 구체적인 분석 부족
- 다른 최신 data-efficient 방법(예: meta-learning 기반 접근)과의 직접적인 비교 미흡
- 후속 연구로 end-to-end learning을 통한 geometric prior의 자동 발견, dynamic environment에서의 online adaptation, 더 많은 robot morphology에 대한 확장 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RGMP는 기하학적 추론과 데이터 효율성의 결합을 통해 humanoid robot 조작의 중요한 문제를 해결하며, GSS와 ARGN의 설계가 정교하고 실제 로봇에서 strong empirical result를 달성한 우수한 연구이다. 다만 기하학적 제약의 자동화와 더 광범위한 실증 평가가 이루어진다면 더욱 강력할 것으로 판단된다.

## Related Papers

- 🔄 다른 접근: [[papers/1812_Behavior_Foundation_Model_for_Humanoid_Robots/review]] — RGMP의 기하학적 추론 기반 정책과 BFM의 행동 기반 파운데이션 모델은 휴머노이드 조작의 서로 다른 일반화 전략
- 🏛 기반 연구: [[papers/1863_DemoHLM_From_One_Demonstration_to_Generalizable_Humanoid_Loc/review]] — DemoHLM의 단일 데모 기반 학습이 RGMP의 데이터 효율성 달성을 위한 핵심 방법론적 기반
- 🔗 후속 연구: [[papers/1935_From_Language_to_Locomotion_Retargeting-free_Humanoid_Contro/review]] — 언어 기반 휴머노이드 제어가 RGMP의 기하학적 추론을 자연언어 명령으로 확장하는 발전 방향
- 🏛 기반 연구: [[papers/1946_Generalizable_Geometric_Prior_and_Recurrent_Spiking_Feature/review]] — RGMP의 기하학적 추론이 Generalizable Geometric Prior의 recurrent spiking feature 방법론을 휴머노이드 조작에 적용한 것이다
- 🔄 다른 접근: [[papers/1947_Generalizable_Humanoid_Manipulation_with_3D_Diffusion_Polici/review]] — 두 논문 모두 일반화 가능한 휴머노이드 조작을 다루지만 RGMP는 기하학적 prior에, Generalizable Humanoid Manipulation은 3D diffusion policy에 집중한다
- 🔗 후속 연구: [[papers/1678_SkillBlender_Towards_Versatile_Humanoid_Whole-Body_Loco-Mani/review]] — RGMP의 87% 성공률 달성 경험이 SkillBlender의 다양한 whole-body skill 결합에서 성능 최적화 가이드라인을 제공할 수 있다
- 🧪 응용 사례: [[papers/1779_A_Humanoid_Visual-Tactile-Action_Dataset_for_Contact-Rich_Ma/review]] — RGMP의 geometric reasoning을 실제 manipulation dataset에 적용한 사례
- 🔄 다른 접근: [[papers/1812_Behavior_Foundation_Model_for_Humanoid_Robots/review]] — 행동 기반 파운데이션 모델과 RGMP의 기하학적 추론 정책은 휴머노이드 일반화의 서로 다른 사전학습 전략
- 🔗 후속 연구: [[papers/1863_DemoHLM_From_One_Demonstration_to_Generalizable_Humanoid_Loc/review]] — RGMP의 데이터 효율적 기하학적 추론을 DemoHLM의 극단적 데이터 효율성으로 확장한 형태
- 🔄 다른 접근: [[papers/1946_Generalizable_Geometric_Prior_and_Recurrent_Spiking_Feature/review]] — 둘 다 기하학적 정보와 정책 학습을 결합하지만 RGMP-S는 spiking 신경망을, RGMP는 multimodal policy를 사용한다.
- 🔗 후속 연구: [[papers/2111_NoMaD_Goal_Masked_Diffusion_Policies_for_Navigation_and_Expl/review]] — RGMP의 geometric-prior multimodal policy가 NoMaD의 unified diffusion policy로 더욱 일반화된 것이다
