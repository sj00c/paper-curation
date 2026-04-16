---
title: "1488_NavDP_Learning_Sim-to-Real_Navigation_Diffusion_Policy_with"
authors:
  - "Wenzhe Cai"
  - "Jiaqi Peng"
  - "Yuqiang Yang"
  - "Yujian Zhang"
  - "Meng Wei"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "NavDP는 시뮬레이션에서만 학습한 unified transformer 기반 diffusion policy로, privileged information을 활용한 trajectory generation과 critic value prediction을 통해 zero-shot sim-to-real transfer를 달성한다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Trajectory-Conditioned_Robot_Simulation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Cai et al._2025_NavDP Learning Sim-to-Real Navigation Diffusion Policy with Privileged Information Guidance.pdf"
---

# NavDP: Learning Sim-to-Real Navigation Diffusion Policy with Privileged Information Guidance

> **저자**: Wenzhe Cai, Jiaqi Peng, Yuqiang Yang, Yujian Zhang, Meng Wei, Hanqing Wang, Yilun Chen, Tai Wang, Jiangmiao Pang | **날짜**: 2025-05-13 | **URL**: [https://arxiv.org/abs/2505.08712](https://arxiv.org/abs/2505.08712)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: NavDP is solely trained with simulation data but can achieve zero-shot sim-to-real transfer to different types o*

NavDP는 시뮬레이션에서만 학습한 unified transformer 기반 diffusion policy로, privileged information을 활용한 trajectory generation과 critic value prediction을 통해 zero-shot sim-to-real transfer를 달성한다.

## Motivation

- **Known**: Diffusion policy는 로봇 조작 작업에서 multimodal distribution 학습에 효과적이며, end-to-end visual navigation은 cross-embodiment 적응성을 보여주고 있다.
- **Gap**: 기존 학습 기반 방법들은 실제 데이터 수집의 비용과 복잡성으로 인한 제약이 있으며, modular 접근법은 hyperparameter 튜닝과 cascading error의 문제가 있다.
- **Why**: 동적이고 복잡한 개방 환경에서의 자율로봇 네비게이션은 구체화된 지능형 로봇 개발의 핵심이며, 시뮬레이션 기반 대규모 학습은 실용적인 확장성을 제공한다.
- **Approach**: RGB-D 입력만으로 조건화된 unified transformer 네트워크가 trajectory generation과 evaluation을 동시에 학습하며, 시뮬레이션의 privileged information(ESDF, global planner)으로부터 감독 신호를 얻어 안전성을 강화한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: Visualization of comparison among navigation approaches. Two common failure mode of baselines are displayed:*

- **대규모 데이터셋 구축**: 3,000개 장면에서 1백만 미터 이상의 네비게이션 경험을 포함한 200K 궤적 데이터셋 (실시간 데이터 수집 대비 20배 효율)
- **우수한 성능**: 시뮬레이션 및 실제 환경 모두에서 기존 state-of-the-art 방법을 상당한 차이로 능가
- **Zero-shot 일반화**: 학습되지 않은 다양한 환경과 로봇 embodiment에 대한 sim-to-real transfer 달성
- **통합 아키텍처**: trajectory generation과 evaluation을 하나의 transformer 네트워크로 통합하여 효율성 증대

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the network architecture. NavDP is con-*

- Embodiment-aware planning: 로봇 높이 hb를 (0.25m, 1.25m) 범위에서 무작위화하고 camera pitch angle을 동적으로 조정
- ESDF 기반 궤적 생성: voxel map을 0.05m 해상도로 변환 후 0.2m으로 downsampling하여 A* 경로 계획
- Waypoint refinement: 원본 ESDF map에서 greedy search로 장애물로부터의 거리 최대화
- Cubic spline interpolation으로 smooth한 연속 궤적 생성
- Domain randomization: light condition, view, texture 무작위화로 데이터 다양성 증대
- Contrastive trajectory samples에 대한 critic value 예측으로 안전성 학습
- BlenderProc를 사용한 photorealistic RGB-D rendering
- Multi-modal encoder로 RGB와 depth 정보 fusion

## Originality

- Imitation learning의 효율성과 RL의 counterfactual reasoning을 diffusion policy로 결합한 새로운 프레임워크
- Privileged information (global ESDF, global planner)을 trajectory generation과 critic function 학습에 이중으로 활용하는 감독 전략
- 시뮬레이션에서만 학습하여 실제 로봇에 zero-shot transfer가 가능한 embodiment-aware 설계
- 2,500 trajectories/GPU/day의 매우 효율적인 데이터 생성 엔진 개발
- 200K 궤적, 1M+ 미터의 대규모 공개 네비게이션 데이터셋

## Limitation & Further Study

- Cylinder 기반 로봇 모델 단순화로 인해 실제 로봇의 복잡한 형태를 완전히 반영하지 못할 가능성
- 시뮬레이션-현실 갭은 여전히 존재하며, 극단적인 현실 환경에서의 성능 저하 가능성
- Critic function이 시뮬레이션의 전역 ESDF에 의존하므로, 예측 불가능한 동적 장애물에 대한 대응 능력 제한
- Local RGB-D만 사용하므로 전역 경로 계획이 필요한 매우 복잡한 시나리오에서 최적성 보장 불가
- 후속 연구: 실제 시각적 변동성 더 추가, 동적 환경에서의 실시간 계획 강화, 시각-언어 모델(VLM) 통합 확대

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: NavDP는 시뮬레이션의 privileged information을 효과적으로 활용하는 unified transformer 아키텍처와 대규모 효율적 데이터 엔진으로 navigation 분야에서 significant advance를 달성했으며, zero-shot sim-to-real transfer와 cross-embodiment 일반화 측면에서 강력한 empirical 결과를 보여준다.

## Related Papers

- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — diffusion policy의 기본 이론과 visuomotor policy learning 방법론을 제공하여 NavDP의 trajectory generation 메커니즘 설계에 핵심적인 기반을 제공한다.
- 🔗 후속 연구: [[papers/1572_Sim-to-Real_Reinforcement_Learning_for_Vision-Based_Dexterou/review]] — sim-to-real transfer의 기본 개념을 navigation diffusion policy와 privileged information을 활용한 zero-shot transfer로 확장한다.
- 🧪 응용 사례: [[papers/1525_Real-Time_Execution_of_Action_Chunking_Flow_Policies/review]] — diffusion policy의 real-time execution 기법을 navigation 도메인에 적용하여 NavDP의 실시간 궤적 생성 성능을 향상시킨다.
- 🔄 다른 접근: [[papers/1449_Learned_Perceptive_Forward_Dynamics_Model_for_Safe_and_Platf/review]] — 둘 다 sim-to-real navigation을 다루지만 diffusion policy와 forward dynamics model의 접근법 차이를 비교할 수 있다.
- 🏛 기반 연구: [[papers/1363_Diffusion_Transformer_Policy/review]] — diffusion transformer의 기본 아키텍처를 navigation diffusion policy에 적용하는 이론적 토대를 제공한다.
- 🔗 후속 연구: [[papers/1378_Embodied_Navigation_Foundation_Model/review]] — embodied navigation foundation model을 diffusion policy와 결합하여 더 일반적인 navigation 능력을 달성할 수 있다.
- 🔗 후속 연구: [[papers/1396_ForesightNav_Learning_Scene_Imagination_for_Efficient_Explor/review]] — NavDP의 sim-to-real navigation diffusion이 ForesightNav에서 상상력 기반 장기 네비게이션 목표 선택으로 더욱 발전한 형태이다.
- 🔗 후속 연구: [[papers/1414_Ground_Slow_Move_Fast_A_Dual-System_Foundation_Model_for_Gen/review]] — NavDP의 diffusion policy가 DualVLN의 Diffusion Transformer 기반 policy를 sim-to-real navigation으로 확장합니다.
- 🔄 다른 접근: [[papers/1449_Learned_Perceptive_Forward_Dynamics_Model_for_Safe_and_Platf/review]] — 둘 다 sim-to-real navigation을 다루지만 forward dynamics model과 diffusion policy의 접근법 차이를 분석할 수 있다.
