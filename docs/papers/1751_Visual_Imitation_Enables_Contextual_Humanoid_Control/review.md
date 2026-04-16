---
title: "1751_Visual_Imitation_Enables_Contextual_Humanoid_Control"
authors:
  - "Arthur Allshire"
  - "Hongsuk Choi"
  - "Junyi Zhang"
  - "David McAllister"
  - "Anthony Zhang"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "VIDEOMIMIC는 단순한 휴대폰 영상에서 인간-환경 4D 기하학을 공동 재구성하고, 이를 시뮬레이션에서 RL 정책으로 학습한 후 실제 휴머노이드 로봇에 배포하는 real-to-sim-to-real 파이프라인이다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Allshire et al._2025_Visual Imitation Enables Contextual Humanoid Control.pdf"
---

# Visual Imitation Enables Contextual Humanoid Control

> **저자**: Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, Angjoo Kanazawa | **날짜**: 2025-05-06 | **URL**: [https://arxiv.org/abs/2505.03729](https://arxiv.org/abs/2505.03729)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: VideoMimic Real-to-Sim. A casually captured phone video provides the only input. We first*

VIDEOMIMIC는 단순한 휴대폰 영상에서 인간-환경 4D 기하학을 공동 재구성하고, 이를 시뮬레이션에서 RL 정책으로 학습한 후 실제 휴머노이드 로봇에 배포하는 real-to-sim-to-real 파이프라인이다.

## Motivation

- **Known**: DeepMimic 등의 모방 학습 방식은 모션 캡처 데이터에 의존하고, 최근 legged robot 연구는 reward shaping 또는 MoCap 데이터를 통해 특정 행동을 학습해왔다.
- **Gap**: 기존 시각 기반 방법들은 인간만 또는 장면만 독립적으로 재구성하며, 환경-인식 전신 제어(contextual whole-body control)를 위한 물리적으로 일관성 있는 참조 동작을 제공하지 못했다.
- **Why**: 휴머노이드 로봇이 계단 오르기, 의자에 앉기 같은 다양한 환경 적응 행동을 단일 정책으로 수행할 수 있다면, 로봇 학습의 확장성을 크게 향상시킬 수 있다.
- **Approach**: 모노큘러 RGB 영상에서 VIMO, ViTPose, BSTRO, MegaSaM/MonST3R 등 사전학습 모델들로 인간 자세와 장면 포인트클라우드를 추출한 후, 메트릭 스케일과 joint 정렬을 위해 인간 높이 prior를 활용하여 공동 최적화하고, 최종적으로 retarget된 모션과 메시로 정책을 학습한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5: The policy performing various skills on the real robot: traversing complex terrain, standing, and*

- **실제 로봇 배포**: Unitree G1 휴머노이드에서 계단 등하강, 의자/벤치 앉기/일어나기 등 robust하고 반복 가능한 contextual control 달성
- **단일 통합 정책**: 환경(height-map)과 root direction으로 조건화된 단일 policy로 명시적 task labeling 없이 행동 선택 및 실행
- **Scalable 데이터 파이프라인**: 123개 모노큘러 RGB 영상 데이터셋으로 학습하여 MoCap 및 pre-scanned scene 불필요
- **Unseen environment 일반화**: 학습하지 않은 환경에서도 높이맵 정보만으로 적절한 행동 생성

## How

![Figure 2](figures/fig2.webp)

*Figure 2: VideoMimic Real-to-Sim. A casually captured phone video provides the only input. We first*

- **전처리**: Grounded SAM2로 인간 detection/association, VIMO로 SMPL 파라미터 추출, ViTPose로 2D keypoint 검출, BSTRO로 발 contact 회귀, MegaSaM/MonST3R로 장면 포인트클라우드 획득
- **Joint 최적화**: 인간의 global translation/orientation, local pose, 그리고 장면 스케일 α를 동시에 최적화하며, SMPL 인간 높이 prior를 메트릭 참조로 활용
- **Retargeting**: 최적화된 인간 궤적을 humanoid 로봇으로 kinematic retargeting하되, joint limits, contact, collision 제약 조건 준수
- **RL 정책 학습**: Mesh와 retarget 데이터로 goal-conditioned DeepMimic 스타일 RL 수행, mass/friction/latency/sensor noise randomization으로 robustness 확보
- **Policy 증류**: DAgger를 통해 추적(tracking) policy를 proprioception, 11×11 height-map patch, goal vector만 관찰하는 generalist controller로 증류하고 PPO fine-tuning 수행

## Originality

- **공동 4D 재구성의 물리 기반 활용**: 인간-장면을 메트릭하게 공동 재구성하고 이를 직접 physics simulator에 적용 가능한 형태로 변환한 점이 새로움
- **End-to-end real-to-sim-to-real 파이프라인**: 단순 모노큘러 영상에서 로봇 정책까지 일관된 파이프라인 구축으로, 기존 isolated reconstruction + reward engineering 접근과 구별
- **Context-aware generalist policy**: 명시적 task 분류 없이 height-map과 root command만으로 다양한 행동을 자동 선택하는 unified policy 설계
- **실제 로봇 검증**: Unitree G1에서 실제 배포 성공으로 sim-to-real transfer의 실질적 가능성 입증

## Limitation & Further Study

- **영상 품질 의존성**: 휴대폰 영상 기반이므로 occlusion, motion blur, low resolution 상황에서의 재구성 정확도 미검증
- **Embodiment gap**: 인간-로봇 체형 차이에 의한 dynamical mismatch 가능성; 현재 kinematic retargeting만으로는 contact dynamics를 완벽히 보장하지 못함
- **환경 복잡도 제한**: 학습된 policy는 height-map이라는 제한된 환경 표현에만 의존하므로, 복잡한 장애물, 동적 환경 대응 미흡 가능
- **영상 데이터 규모**: 123개 영상으로 학습하여, 더 광범위한 행동 다양성(던지기, 미세 조작 등)을 다루기 위해서는 데이터 확장 필요
- **후속 연구 방향**: (1) 다중 시점 또는 RGB-D 영상 활용으로 재구성 정확도 향상, (2) contact-aware RL 목적함수로 dynamics 정확화, (3) 대규모 웹 영상 데이터를 활용한 pre-training

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 일상 영상으로부터 휴머노이드 로봇의 문맥-인식 제어를 가능하게 하는 실용적이고 확장 가능한 파이프라인을 제시하며, 공동 4D 재구성과 RL 기반 정책 증류의 조합으로 높은 독창성을 보인다. 실제 로봇 배포 성공은 연구의 가치를 크게 높이나, 환경 표현의 제한성과 동역학 정확도 측면에서 개선 여지가 있다.

## Related Papers

- 🔄 다른 접근: [[papers/1753_VisualMimic_Visual_Humanoid_Loco-Manipulation_via_Motion_Tra/review]] — 둘 다 인간 영상에서 humanoid 제어를 학습하지만 VisualMimic은 hierarchical control에 더 중점을 둡니다.
- 🏛 기반 연구: [[papers/1903_EgoMimic_Scaling_Imitation_Learning_via_Egocentric_Video/review]] — EgoMimic의 egocentric video 모방 학습이 VIDEOMIMIC의 휴대폰 영상 처리 기술의 기반이 됩니다.
- 🔗 후속 연구: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — ResMimic의 일반적인 모션 추적이 VIDEOMIMIC의 4D 기하학 재구성 접근법을 보완합니다.
- 🔄 다른 접근: [[papers/1680_SLAC_Simulation-Pretrained_Latent_Action_Space_for_Whole-Bod/review]] — real-to-sim-to-real과 simulation-pretrained latent space라는 서로 다른 시뮬레이션-실제 연결 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1749_VIRAL_Visual_Sim-to-Real_at_Scale_for_Humanoid_Loco-Manipula/review]] — 휴머노이드 loco-manipulation에서 4D 기하학 재구성과 visual sim-to-real이라는 보완적 시각 처리 접근법을 다룬다.
- 🏛 기반 연구: [[papers/1857_CRISP_Contact-Guided_Real2Sim_from_Monocular_Video_with_Plan/review]] — monocular video에서 contact-guided real2sim과 4D 기하학 재구성이라는 관련된 실제-시뮬레이션 연결 방법론을 사용한다.
- 🔗 후속 연구: [[papers/1895_Efficient_and_Scalable_Monocular_Human-Object_Interaction_Mo/review]] — 효율적이고 확장 가능한 단안 인간-객체 상호작용 모델링을 휴머노이드 제어로 확장하여 단순한 휴대폰 영상에서 복잡한 맥락적 제어를 실현했다.
- 🔄 다른 접근: [[papers/2148_TokenHSI_Unified_Synthesis_of_Physical_Human-Scene_Interacti/review]] — 물리적 인간-장면 상호작용을 위해 서로 다른 접근(단순 영상 기반 모방 vs 통합된 토큰 기반 합성)을 통해 자연스러운 휴머노이드 행동을 생성한다.
- 🔄 다른 접근: [[papers/1680_SLAC_Simulation-Pretrained_Latent_Action_Space_for_Whole-Bod/review]] — 전신 조작 학습에서 잠재 행동 공간과 4D 기하학 재구성이라는 서로 다른 표현 학습 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1646_RoboMirror_Understand_Before_You_Imitate_for_Video_to_Humano/review]] — Visual Imitation Enables Contextual Control의 맥락적 휴머노이드 제어가 RoboMirror의 VLM 기반 의도 추출을 더욱 정교하게 확장함
- 🏛 기반 연구: [[papers/1749_VIRAL_Visual_Sim-to-Real_at_Scale_for_Humanoid_Loco-Manipula/review]] — visual sim-to-real 접근법에서 RGB 기반 정책과 4D 기하학 재구성이라는 보완적 시각 처리 방법을 사용한다.
- 🔄 다른 접근: [[papers/1753_VisualMimic_Visual_Humanoid_Loco-Manipulation_via_Motion_Tra/review]] — 둘 다 비전 기반 humanoid 제어지만 VIDEOMIMIC은 real-to-sim-to-real, VisualMimic은 hierarchical 접근법을 사용합니다.
- 🔗 후속 연구: [[papers/1885_DreamControl-v2_Simpler_and_Scalable_Autonomous_Humanoid_Ski/review]] — visual imitation을 통한 contextual humanoid control이 DreamControl-v2의 guided diffusion 접근법을 시각적 맥락으로 확장한다.
- 🔄 다른 접근: [[papers/1902_EgoMI_Learning_Active_Vision_and_Whole-Body_Manipulation_fro/review]] — Visual Imitation의 맥락적 휴머노이드 제어가 egocentric 데이터 없이도 시각 기반 제어를 가능하게 하는 다른 접근 방식을 제시한다.
- 🏛 기반 연구: [[papers/1969_HDMI_Learning_Interactive_Humanoid_Whole-Body_Control_from_H/review]] — visual imitation을 통한 contextual humanoid 제어가 HDMI의 모노큘러 비디오 기반 상호작용 학습의 기반 기술입니다.
- 🔄 다른 접근: [[papers/1975_Hierarchical_visuomotor_control_of_humanoids/review]] — 계층적 시각운동 제어와 시각적 모방 기반 문맥적 제어는 모두 시각 정보를 활용한 휴머노이드 제어이지만 접근법이 다르다.
- 🔄 다른 접근: [[papers/2022_In-N-On_Scaling_Egocentric_Manipulation_with_in-the-wild_and/review]] — 시각 기반 휴머노이드 제어에서 같은 문제를 다르지만 보완적인 접근으로 해결
