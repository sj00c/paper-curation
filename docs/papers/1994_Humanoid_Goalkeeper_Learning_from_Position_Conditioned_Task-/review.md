---
title: "1994_Humanoid_Goalkeeper_Learning_from_Position_Conditioned_Task-"
authors:
  - "Junli Ren"
  - "Junfeng Long"
  - "Tao Huang"
  - "Huayi Wang"
  - "Zirui Wang"
date: "2026.03"
doi: "10.48550/arXiv.2510.18002"
arxiv: ""
score: 4.0
essence: "인간형 로봇의 골키퍼 역할을 위해 위치 조건부 task-motion constraints를 학습하는 end-to-end RL 프레임워크를 제시하며, 인간 모션 프라이어를 adversarial scheme으로 통합하여 자동화되고 인간다운 전신 동작을 생성한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Humanoid_Locomotion_and_Control"
  - "sub/Autonomous_Dribbling_Robots"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Ren et al._2026_Humanoid Goalkeeper Learning from Position Conditioned Task-Motion Constraints.pdf"
---

# Humanoid Goalkeeper: Learning from Position Conditioned Task-Motion Constraints

> **저자**: Junli Ren, Junfeng Long, Tao Huang, Huayi Wang, Zirui Wang, Feiyu Jia, Wentao Zhang, Jingbo Wang, Ping Luo, Jiangmiao Pang | **날짜**: 2026-03-14 | **DOI**: [10.48550/arXiv.2510.18002](https://doi.org/10.48550/arXiv.2510.18002)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Method framework: We train our policy using an end-to-end*

인간형 로봇의 골키퍼 역할을 위해 위치 조건부 task-motion constraints를 학습하는 end-to-end RL 프레임워크를 제시하며, 인간 모션 프라이어를 adversarial scheme으로 통합하여 자동화되고 인간다운 전신 동작을 생성한다.

## Motivation

- **Known**: 사족 로봇의 동적 객체 상호작용 능력과 imitation learning을 통한 인간 모션 스킬 전이가 시연되었으나, 인간형 로봇의 넓은 보호 범위 커버와 자연스러운 전신 동작 생성은 여전히 미해결 과제이다.
- **Gap**: 기존 방식들은 teleoperation이나 고정 motion tracking에 의존하거나 사전 정의된 motion primitives로 제한되어 있으며, 광범위한 interception 범위를 커버하면서 동시에 인간다운 움직임을 생성하는 단일 통합 정책이 부재하다.
- **Why**: 인간형 로봇의 골키퍼 능력은 지각, 의사결정, 민첩한 모터 제어를 통합해야 하며, 이는 로봇의 물리적 지능 평가를 위한 중요한 벤치마크이자 실시간 동적 상호작용 기술 발전을 위한 핵심이다.
- **Approach**: PPO 알고리즘과 IsaacGym 시뮬레이터를 사용하여 task 보상과 motion discriminator를 ball 착지 영역에 따라 조건화하고, adversarial training scheme으로 task 성공과 motion realism을 동시에 최적화하는 방식을 채택한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: We present Humanoid Goalkeeper, capable of performing goalkeeping tasks across various regions with a wide opera*

- **End-to-end RL 정책**: 별도의 최적화 단계 없이 task 성공과 motion realism을 jointly enforce하는 통합 프레임워크 달성
- **광범위한 operational coverage**: 위치 조건부 motion priors를 통해 넓은 보호 범위를 커버하면서 빠른 응답 시간 유지
- **실시간 자동 인터셉션**: 고속 비행 공의 민첩하고 자동화된 인간다운 인터셉션 성능 실증
- **일반화 능력**: 골키퍼 외에도 ball escaping, grabbing 등 관련 동적 상호작용 태스크로 접근법 확장 시연
- **실제 하드웨어 배포**: sim-to-real 갭 폐쇄를 위한 지각 노이즈, 궤적 추정, 멀티모달 센싱 통합으로 실제 인간형 로봇에서 성공적 배포

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Method framework: We train our policy using an end-to-end*

- Training environment을 k개 regions으로 분할하고 각 region에 대응하는 ball landing position을 샘플링
- Ball position (Oball)과 proprioceptive observations (Op)를 actor input으로 사용하며, 시간 정보 캡처를 위해 길이 T의 history 유지
- Position-conditioned task reward rt를 sigmoid 함수 기반으로 설계하여 end-effector가 동적 타겟 ptarget에 도달하도록 유도
- Ball 거리에 따라 예측된 착지점(pland)과 실제 ball position(pball) 간 switching을 통해 거리 기반 타겟팅 최적화
- Motion priors를 ball landing region R에 따라 조건화된 discriminator를 통해 adversarial training으로 통합
- Onboard camera 또는 MoCap 시스템 모두 호환 가능하도록 로컬 프레임 기반 관측 설계
- PPO 알고리즘으로 task reward와 motion discriminator 손실을 joint optimization

## Originality

- 기존의 고정 motion primitives나 pre-learned skills 선택 방식과 달리, 관측 조건화된 adversarial training을 통해 position-specific motion priors를 end-to-end 정책으로 통합하는 새로운 접근법
- Ball landing position을 기반으로 constraint space를 분할하는 position-conditioned task reward 설계로 광범위한 operational range 달성
- Humanoid 플랫폼에서 millisecond-level 동적 상호작용을 처음으로 시연하며, quadruped 기반의 선행 연구보다 복잡한 전신 제어 문제 해결
- Real-world feasibility를 위해 perception noise, trajectory estimation, multi-modal sensing을 training loop에 명시적으로 통합하는 실용적 접근법

## Limitation & Further Study

- 논문에서 실제 성공률, 실패 사례, 한계 상황(예: 극도로 빠른 공, 복잡한 궤적)에 대한 정량적 분석 부재
- Position-conditioned approach의 region 개수 k에 따른 성능 변화 및 최적 k 값 결정 기준이 명확하지 않음
- Adversarial training의 discriminator 손실 가중치와 task reward 간의 trade-off 분석 미흡
- 단일 로봇 플랫폼에서의 검증으로 다양한 humanoid 아키텍처에 대한 일반화 가능성 미검증
- Motion prior 데이터의 다양성과 품질이 최종 성능에 미치는 영향 분석 필요
- Sim-to-real 갭 폐쇄 과정에서 어떤 시뮬레이션 파라미터(마찰, 질량, 센서 지연 등)가 가장 중요한지에 대한 ablation study 부재

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 position-conditioned adversarial motion priors를 통해 humanoid 로봇의 자동화되고 인간다운 골키퍼 능력을 처음으로 시연한 의미 있는 연구이며, 실제 하드웨어 배포와 task 일반화를 통해 실용성을 입증했으나, 정량적 분석과 ablation study가 강화될 필요가 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1979_HITTER_A_HumanoId_Table_TEnnis_Robot_via_Hierarchical_Planni/review]] — 골키퍼와 탁구 로봇 모두 스포츠 특화 제어이지만 위치 조건부 vs 계층적 계획 접근법이 다르다.
- 🔗 후속 연구: [[papers/2003_Humanoid_Whole-Body_Badminton_via_Multi-Stage_Reinforcement/review]] — 골키퍼 기술이 배드민턴의 다단계 강화학습으로 확장되어 더 복잡한 스포츠 동작을 학습할 수 있다.
- 🔄 다른 접근: [[papers/1996_Humanoid_Locomotion_as_Next_Token_Prediction/review]] — next token prediction 방식과 달리 goalkeeper는 position-conditioned task-motion constraints 학습을 통한 특화된 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1648_RoboStriker_Hierarchical_Decision-Making_for_Autonomous_Huma/review]] — RoboStriker의 hierarchical decision-making이 humanoid goalkeeper의 골키퍼 역할을 축구 경기의 striker 측면으로 확장한 연구이다.
- 🏛 기반 연구: [[papers/1936_From_Motion_to_Behavior_Hierarchical_Modeling_of_Humanoid_Ge/review]] — hierarchical modeling of humanoid gait의 motion behavior 방법론이 goalkeeper의 task-motion constraints 학습 기초를 제공한다.
- 🏛 기반 연구: [[papers/1801_AMP_Adversarial_Motion_Priors_for_Stylized_Physics-Based_Cha/review]] — AMP의 적대적 모션 프라이어가 골키퍼의 자동화되고 인간다운 전신 동작 생성의 핵심 토대가 된다.
- 🔗 후속 연구: [[papers/1889_Dribble_Master_Learning_Agile_Humanoid_Dribbling_through_Leg/review]] — Dribble Master의 민첩한 드리블 학습을 골키퍼의 위치 조건부 방어 동작으로 확장한 발전된 형태다.
- 🔗 후속 연구: [[papers/1778_A_Hierarchical_Model-Based_System_for_High-Performance_Human/review]] — 축구 로봇의 골키퍼 태스크는 완전한 축구 시스템의 특화된 구성 요소로 전체 시스템 성능을 향상시킬 수 있다
