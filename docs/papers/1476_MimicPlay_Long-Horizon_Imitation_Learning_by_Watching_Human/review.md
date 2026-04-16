---
title: "1476_MimicPlay_Long-Horizon_Imitation_Learning_by_Watching_Human"
authors:
  - "Chen Wang"
  - "Linxi Fan"
  - "Jiankai Sun"
  - "Ruohan Zhang"
  - "Li Fei-Fei"
date: "2023.02"
doi: ""
arxiv: ""
score: 4.0
essence: "MimicPlay는 저비용의 인간 플레이 데이터에서 고수준 계획을 학습하고 소량의 원격조종 데이터에서 저수준 제어 정책을 학습하는 계층적 모방 학습 프레임워크로, 장기 조작 작업의 데이터 효율성을 대폭 향상시킨다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2023_MimicPlay Long-Horizon Imitation Learning by Watching Human Play.pdf"
---

# MimicPlay: Long-Horizon Imitation Learning by Watching Human Play

> **저자**: Chen Wang, Linxi Fan, Jiankai Sun, Ruohan Zhang, Li Fei-Fei, Danfei Xu, Yuke Zhu, Anima Anandkumar | **날짜**: 2023-02-24 | **URL**: [https://arxiv.org/abs/2302.12422](https://arxiv.org/abs/2302.12422)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Human is able to complete a long-horizon task much faster than a teleoperated robot. This*

MimicPlay는 저비용의 인간 플레이 데이터에서 고수준 계획을 학습하고 소량의 원격조종 데이터에서 저수준 제어 정책을 학습하는 계층적 모방 학습 프레임워크로, 장기 조작 작업의 데이터 효율성을 대폭 향상시킨다.

## Motivation

- **Known**: 모방 학습은 로봇 조작 기술 학습에 유망하지만 장기 작업을 위해 많은 시연 데이터가 필요하다. 계층적 모방 학습과 플레이 데이터 학습은 이를 해결하려는 기존 방향이다.
- **Gap**: 기존 계층적 방법들은 모두 비싼 로봇 원격조종 데이터로 고수준 계획과 저수준 제어를 학습해야 하며, 로봇 플레이 데이터 수집도 4.5~6시간으로 여전히 많은 시간이 소요된다.
- **Why**: 장기 조작 작업 학습은 로봇 산업에서 필수적이고, 데이터 수집 비용 감소는 실제 배포 가능성을 크게 높인다. 인간과 로봇의 형태 차이에도 불구하고 인간 행동 데이터에서 유용한 계획을 추출할 수 있다면 학습 효율이 급격히 개선된다.
- **Approach**: 3D-인식 latent plan space를 중간 표현으로 활용하여 인간과 로봇 간의 embodiment gap을 연결한다. 인간 플레이 데이터(10분)에서 goal-conditioned latent planner를 학습하고, 소량의 로봇 원격조종 데이터(30분 미만)에서 이 계획에 따르는 저수준 controller를 학습한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Evaluation of multi-task policy*

- **데이터 효율성**: 인간 플레이 데이터(10분) + 로봇 시연(30분 미만)으로 학습 가능하여 기존 4.5~6시간 플레이 데이터 수집 시간을 대폭 감소
- **우수한 성능**: 14개 실제 장기 조작 작업에서 state-of-the-art 모방 학습 방법들을 능가하는 작업 성공률 달성
- **일반화 능력**: 학습 중 보지 못한 새로운 작업에 대한 우수한 일반화 성능 및 외부 방해에 대한 강건성 입증
- **다중 인터페이스**: 인간 비디오를 로봇 조작 작업의 '프롬프트'로 직접 사용 가능한 통합 latent plan space 구축

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of MIMICPLAY. (a) Training Stage 1: using cheap human play data to train a*

- **Stage 1 - High-level Planner 학습**: 인간 플레이 데이터로부터 goal image가 주어졌을 때 미래 3D 인간 손 궤적을 예측하는 goal-conditioned latent planner를 학습
- **Stage 2 - Low-level Controller 학습**: 예측된 latent plan을 조건으로 하여 로봇 상태 정보를 통합해 최종 action을 생성하는 multi-task visuomotor controller를 소량의 원격조종 데이터로 학습
- **3D 표현 활용**: latent plan space를 3D-aware하게 설계하여 embodiment gap을 최소화하고 인간과 로봇 데이터 간 의미론적 연결 확보
- **다중 작업 학습**: 다양한 조작 작업을 단일 모델에서 학습하여 일반화 능력 강화

## Originality

- **데이터 원천의 분리**: 기존 계층적 학습에서 처음으로 고수준 계획과 저수준 제어를 서로 다른 데이터 타입(인간 vs 로봇)으로 학습하는 혁신적 패러다임 제시
- **3D latent plan space**: embodiment gap을 명시적으로 다루기 위해 3D-인식 중간 표현 도입으로, 인간과 로봇 간 의미 전달 가능하게 함
- **인간 플레이 데이터의 활용**: 기존 로봇 플레이 데이터 중심 연구에서 벗어나 저비용 인간 플레이 데이터의 가치를 체계적으로 입증
- **비디오 프롬프팅**: 학습된 latent space를 통해 인간 시연 비디오를 직접 로봇 조작 작업의 지령으로 사용 가능한 새로운 인터페이스 제안

## Limitation & Further Study

- **embodiment gap의 불완전한 해결**: 3D latent plan으로 일부 해소하지만 인간 손과 로봇 그리퍼의 근본적 차이로 인한 완전한 일반화는 여전히 어려움
- **데이터 선택 편향**: 인간이 자유롭게 수집한 플레이 데이터의 동작 범위가 특정 작업 영역으로 편향될 수 있음
- **multi-modal 행동 분포**: 동일 goal에 다양한 인간 행동이 존재할 때 단일 plan으로 충분한지 검증 필요
- **후속 연구 방향**: (1) 더 강력한 embodiment 맵핑 학습 방법 개발, (2) 도메인 적응 기법으로 다양한 환경 일반화 개선, (3) 인간 플레이와 로봇 능력의 한계를 명시적으로 모델링하는 메커니즘 추가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: MimicPlay는 데이터 수집 비용이라는 모방 학습의 근본적 문제를 창의적으로 해결하면서 실제 로봇 작업에서 우수한 성능을 입증한 의미있는 연구이다. 인간과 로봇 데이터의 상보적 활용이라는 새로운 패러다임은 로봇 학습의 확장성을 크게 향상시킬 수 있는 잠재력을 보여준다.

## Related Papers

- 🔄 다른 접근: [[papers/1453_Learning_Latent_Plans_from_Play/review]] — 둘 다 인간 플레이 데이터를 활용하지만 hierarchical imitation learning과 latent plan learning의 접근법 차이를 비교할 수 있다.
- 🔗 후속 연구: [[papers/1376_EgoScale_Scaling_Dexterous_Manipulation_with_Diverse_Egocent/review]] — diverse egocentric data를 hierarchical imitation learning과 결합하여 더 효율적인 장기 조작 학습을 달성할 수 있다.
- 🔄 다른 접근: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — 둘 다 long-horizon task learning을 다루지만 hierarchical imitation과 language model guided RL의 접근법 차이를 분석할 수 있다.
- 🔗 후속 연구: [[papers/1352_DemoDiffusion_One-Shot_Human_Imitation_using_pre-trained_Dif/review]] — 인간 시연을 통한 모방학습에서 장기간 작업에 대한 구체적 해결책을 제시합니다.
- 🔗 후속 연구: [[papers/1453_Learning_Latent_Plans_from_Play/review]] — 플레이 데이터에서의 학습을 long-horizon imitation learning으로 더 체계화하고 발전시켰다.
- 🔄 다른 접근: [[papers/1581_Structured_World_Models_from_Human_Videos/review]] — 인간의 행동 학습에서 SWIM은 비디오 기반 world model로, MimicPlay는 장기 모방 학습으로 서로 다른 접근법을 사용한다.
- 🔄 다른 접근: [[papers/1601_UniSkill_Imitating_Human_Videos_via_Cross-Embodiment_Skill_R/review]] — MimicPlay는 UniSkill과 같이 인간 비디오 모방을 통한 로봇 학습이지만 장기 수평선 작업에 특화된 다른 방법론이다.
- 🏛 기반 연구: [[papers/1634_ZeroMimic_Distilling_Robotic_Manipulation_Skills_from_Web_Vi/review]] — MimicPlay의 인간 비디오로부터 장기 모방 학습 방법론이 ZeroMimic의 웹 비디오 기반 스킬 학습에 이론적 기반을 제공한다
- 🏛 기반 연구: [[papers/1325_CALVIN_A_Benchmark_for_Language-Conditioned_Policy_Learning/review]] — MimicPlay의 장기간 모방 학습은 CALVIN의 언어 조건부 장기 작업 수행에 학습 방법론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1376_EgoScale_Scaling_Dexterous_Manipulation_with_Diverse_Egocent/review]] — MimicPlay의 human video를 통한 long-horizon imitation과 EgoScale의 egocentric video 기반 dexterous manipulation은 인간 비디오 활용에서 서로 다른 접근이다.
