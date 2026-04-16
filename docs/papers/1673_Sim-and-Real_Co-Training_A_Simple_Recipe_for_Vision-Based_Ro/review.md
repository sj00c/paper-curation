---
title: "1673_Sim-and-Real_Co-Training_A_Simple_Recipe_for_Vision-Based_Ro"
authors:
  - "Abhiram Maddukuri"
  - "Zhenyu Jiang"
  - "Lawrence Yunliang Chen"
  - "Soroush Nasiriany"
  - "Yuqi Xie"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "시뮬레이션 데이터와 실제 로봇 데이터를 혼합하여 학습하는 sim-and-real co-training 전략을 체계적으로 연구하고, 비전 기반 로봇 조작 작업에서 실제 데이터만 사용하는 것 대비 평균 38% 성능 향상을 달성했다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Egocentric_Manipulation_Imitation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Maddukuri et al._2025_Sim-and-Real Co-Training A Simple Recipe for Vision-Based Robotic Manipulation.pdf"
---

# Sim-and-Real Co-Training: A Simple Recipe for Vision-Based Robotic Manipulation

> **저자**: Abhiram Maddukuri, Zhenyu Jiang, Lawrence Yunliang Chen, Soroush Nasiriany, Yuqi Xie, Yu Fang, Wenqi Huang, Zu Wang, Zhenjia Xu, Nikita Chernyadev, Scott Reed, Ken Goldberg, Ajay Mandlekar, Linxi Fan, Yuke Zhu | **날짜**: 2025-03-31 | **URL**: [https://arxiv.org/abs/2503.24361](https://arxiv.org/abs/2503.24361)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Sim-and-Real Co-Training. We show how co-training*

시뮬레이션 데이터와 실제 로봇 데이터를 혼합하여 학습하는 sim-and-real co-training 전략을 체계적으로 연구하고, 비전 기반 로봇 조작 작업에서 실제 데이터만 사용하는 것 대비 평균 38% 성능 향상을 달성했다.

## Motivation

- **Known**: Behavior cloning을 통한 로봇 정책 학습, domain randomization과 digital twin을 이용한 sim-to-real 전이, 최근 연구에서 시뮬레이션과 실제 데이터의 혼합 학습의 효과가 보여짐.
- **Gap**: 시뮬레이션과 실제 데이터를 혼합하여 학습하는 전략의 체계적 이해 부족, 어느 정도의 도메인 차이를 허용할 수 있는지, 최적의 데이터 구성이 무엇인지에 대한 명확한 가이드라인 부재.
- **Why**: 실제 로봇 데이터 수집은 시간과 자원이 많이 소비되는 반면, 생성형 AI와 자동화된 데이터 생성 도구로 대규모 시뮬레이션 데이터를 쉽게 생성할 수 있으므로, 두 데이터원의 효과적인 활용 방법을 이해하는 것이 중요하다.
- **Approach**: Task-aware 시뮬레이션(실제 작업에 맞춘 digital cousin)과 task-agnostic 시뮬레이션(다양한 사전 생성 시뮬레이션)의 두 가지 시뮬레이션 데이터 소스를 활용하여 로봇 팔과 휴머노이드 두 가지 로봇 형태에서 다양한 작업(pick-and-place, 관절 물체 조작, non-prehensile 조작 등)으로 광범위한 실험을 수행했다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4:*

- **체계적 연구 프레임워크**: 시뮬레이션과 실제 데이터의 co-training을 위한 실용적인 레시피 확립
- **성능 향상**: 두 로봇 도메인에 걸쳐 평균 38%의 성능 개선 달성
- **도메인 차이 허용도**: 시뮬레이션 데이터가 실제 데이터와 현저한 차이가 있어도 실질적인 이점 제공 가능함을 입증
- **다양성의 효과**: 다양한 시뮬레이션 데이터가 실제 환경의 미지 시나리오에 대한 일반화 향상에 기여함을 발견

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Method Overview. Our workflow consists of three components: (1) We start with a real-world target task in mind a*

- 두 가지 형태의 시뮬레이션 데이터 비교: task-aware 데이터(실제 작업과 느슨하게 정렬)와 task-agnostic 데이터(독립적으로 생성된 다양한 데이터)
- 데이터 구성 요소 분석: 작업 동일성, 장면 구성, 객체, 카메라 위치, 객체 배치 등이 co-training 효과에 미치는 영향 조사
- Synthetic data generation tools([9], [10])을 활용하여 다양한 시뮬레이션 데이터셋 구성 테스트
- Behavior cloning 기반의 정책 학습으로 co-training 비율 및 데이터 구성의 효과 측정
- 로봇 팔과 휴머노이드를 포함한 여러 로봇 형태와 다양한 조작 작업으로 일반화 검증

## Originality

- Sim-to-real 전이의 전통적 접근(domain randomization, system identification)과 달리, 완벽한 정렬 없이 co-training의 효과를 체계적으로 분석한 점
- Task-aware와 task-agnostic 시뮬레이션의 이분법적 분류 및 비교를 통해 어떤 형태의 시뮬레이션 데이터가 더 효과적인지 실증적으로 규명
- 데이터 구성의 세부 요소(객체, 장면, 카메라, 배치)별로 미치는 영향을 개별 분석하여 실무 가이드라인 제공

## Limitation & Further Study

- 현재 연구는 behavior cloning 기반의 imitation learning에 제한되어 있으므로, 다른 학습 패러다임(reinforcement learning, diffusion model 등)에서의 co-training 효과는 미검증
- 두 가지 로봇 형태(팔, 휴머노이드)와 제한된 작업 영역에서의 실험이므로, 다양한 로봇 플랫폼과 더 복잡한 작업에 대한 일반화 필요
- 시뮬레이션 데이터의 품질 차이나 비현실성 정도에 따른 성능 변화에 대한 더 세밀한 분석 부족
- 후속 연구: 동적 환경, 다중 에이전트 시나리오에서의 co-training 효과 검증; 자동적 데이터 구성 최적화 방법 개발; 다른 학습 알고리즘과의 결합 연구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 sim-and-real co-training의 실용성을 체계적으로 검증하여 실제 로봇 학습의 데이터 효율성 문제에 직접적인 해결책을 제시하며, 명확한 실험 설계와 실무적 가이드라인으로 로봇 커뮤니티에 높은 가치를 제공한다.

## Related Papers

- 🔄 다른 접근: [[papers/1644_RoboCasa_Large-Scale_Simulation_of_Everyday_Tasks_for_Genera/review]] — 두 논문 모두 시뮬레이션과 실제 환경의 혼합 학습을 다루지만, 일반적인 co-training과 대규모 일상 작업이라는 다른 규모를 다룬다.
- 🔗 후속 연구: [[papers/2103_MobileH2R_Learning_Generalizable_Human_to_Mobile_Robot_Hando/review]] — 인간-로봇 핸드오버의 일반화 학습을 시뮬레이션-실제 co-training으로 확장한다.
- 🏛 기반 연구: [[papers/1942_GaussGym_An_open-source_real-to-sim_framework_for_learning_l/review]] — 실제-시뮬레이션 프레임워크의 기본적인 개념과 방법론을 제공한다.
- 🔄 다른 접근: [[papers/1749_VIRAL_Visual_Sim-to-Real_at_Scale_for_Humanoid_Loco-Manipula/review]] — sim-to-real 전이에서 co-training과 teacher-student 구조라는 서로 다른 접근법을 사용하여 시뮬레이션-실제 간격을 해결한다.
- 🔗 후속 연구: [[papers/2125_Opening_the_Sim-to-Real_Door_for_Humanoid_Pixel-to-Action_Po/review]] — 시뮬레이션과 실제 데이터 혼합 학습 전략이 휴머노이드 pixel-to-action 정책의 sim-to-real 전이에 적용될 수 있다.
- 🏛 기반 연구: [[papers/1749_VIRAL_Visual_Sim-to-Real_at_Scale_for_Humanoid_Loco-Manipula/review]] — Sim-and-Real Co-Training의 방법론이 VIRAL의 teacher-student 구조 설계에 영향을 줍니다.
- 🏛 기반 연구: [[papers/1881_Distillation-PPO_A_Novel_Two-Stage_Reinforcement_Learning_Fr/review]] — sim-and-real co-training의 간단한 레시피가 D-PPO의 시뮬레이션과 실제 로봇 간 안정성 확보에 필요한 기초 방법론을 제공한다
- 🔗 후속 연구: [[papers/2107_MOSAIC_Bridging_the_Sim-to-Real_Gap_in_Generalist_Humanoid_M/review]] — Sim-and-Real Co-Training의 sim-to-real 방법론이 MOSAIC의 simulation-reality gap 해결로 더욱 발전된 것이다
- 🧪 응용 사례: [[papers/2155_Towards_bridging_the_gap_Systematic_sim-to-real_transfer_for/review]] — PMSM 기반 에너지 효율 모델링을 vision-based robotic learning의 sim-and-real co-training에 적용하여 더 현실적인 에너지 제약을 반영할 수 있습니다.
- 🔄 다른 접근: [[papers/2125_Opening_the_Sim-to-Real_Door_for_Humanoid_Pixel-to-Action_Po/review]] — 둘 다 sim-to-real 문제를 다루지만, Opening the Sim-to-Real Door는 포토리얼리스틱 시뮬레이션 기반 문열기에, Sim-and-Real Co-Training은 공동 훈련에 집중한다.
