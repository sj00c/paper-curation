---
title: "2147_TeleGate_Whole-Body_Humanoid_Teleoperation_via_Gated_Expert"
authors:
  - "Jie Li"
  - "Bing Tang"
  - "Feng Wu"
  - "Rongyun Cao"
date: "2026.02"
doi: ""
arxiv: ""
score: 4.0
essence: "TeleGate는 가벼운 gating network를 통해 multiple domain-specific expert policies를 동적으로 선택하여 humanoid robot의 real-time whole-body teleoperation을 수행하며, VAE 기반 motion prior를 도입하여 미래 정보 없이도 점프나 일어서기 같은 동적 동작을 예측적으로 제어한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2026_TeleGate Whole-Body Humanoid Teleoperation via Gated Expert Selection with Motion Prior.pdf"
---

# TeleGate: Whole-Body Humanoid Teleoperation via Gated Expert Selection with Motion Prior

> **저자**: Jie Li, Bing Tang, Feng Wu, Rongyun Cao | **날짜**: 2026-02-10 | **URL**: [https://arxiv.org/abs/2602.09628](https://arxiv.org/abs/2602.09628)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

TeleGate는 가벼운 gating network를 통해 multiple domain-specific expert policies를 동적으로 선택하여 humanoid robot의 real-time whole-body teleoperation을 수행하며, VAE 기반 motion prior를 도입하여 미래 정보 없이도 점프나 일어서기 같은 동적 동작을 예측적으로 제어한다.

## Motivation

- **Known**: RL 기반 whole-body control은 단일 과제에서 우수하지만, multiple motion categories에 대해 학습하면 catastrophic forgetting이 발생한다. 기존 distillation 기반 접근법은 여러 expert를 하나의 정책으로 압축하면서 성능 저하를 초래한다.
- **Gap**: Real-time teleoperation에서 미래 reference trajectory가 없는 상황에서 다양한 동적 움직임을 고정밀도로 추적하면서도 knowledge distillation의 성능 손실을 피하고 제한된 학습 데이터로 효율적으로 수행할 수 있는 통합 프레임워크가 부재하다.
- **Why**: Humanoid robot의 재난 구조, 산업 검사 등 비정형 환경에서의 안정적인 실시간 제어와 고품질 학습 데이터 수집이 중요하며, 2.5시간의 적은 데이터로 높은 정밀도를 달성하면 실제 배포 비용을 크게 절감할 수 있다.
- **Approach**: TeleGate는 domain similarity에 따라 독립적으로 학습된 multiple expert policies를 고정하고, proprioceptive states와 reference trajectories를 기반으로 runtime에 동적으로 expert를 활성화하는 lightweight gating network를 학습한다. 또한 VAE 기반 motion prior 모듈로 역사적 관찰에서 암묵적 미래 동작 의도를 추출하여 anticipatory control을 가능하게 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **Data Efficiency**: 단 2.5시간의 motion capture 데이터만으로 running, fall recovery, jumping 등 다양한 동적 움직임의 고정밀도 real-time teleoperation 달성, 기존 SONIC(700h)에 비해 280배 효율적
- **Performance Preservation**: Knowledge distillation의 성능 저하를 회피하면서 expert-level의 추적 정확도를 유지하여 baseline 방법들 대비 tracking accuracy와 success rate에서 유의미한 우월성 입증
- **Anticipatory Control**: VAE 기반 motion prior로 미래 정보 부재 상황에서 점프, 일어서기 같은 예측 필요 동작에 대한 anticipatory control 능력 확보
- **Real-world Deployment**: Unitree G1 humanoid robot에서 완전한 physical deployment validation 수행하여 sim-to-real transfer 효과와 out-of-distribution 동작 일반화 능력 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- Dynamic similarity를 기준으로 motion capture 데이터를 clustering하여 각 cluster별로 독립적인 domain expert policy를 RL로 학습
- Learned expert policies의 파라미터를 고정하고, proprioceptive states(로봇의 현재 상태)와 reference trajectories를 입력으로 받아 각 expert에 대한 활성화 가중치를 출력하는 lightweight gating network 학습
- Runtime에 gating network의 출력을 통해 experts를 동적으로 선택하여 seamless policy switching 구현
- VAE를 사용하여 historical motion observations에서 latent representation을 학습하고, 이를 policy에 입력하여 미래 동작 의도 예측
- Inertial motion capture 장비를 사용하여 teleoperation을 위한 motion capture 데이터 수집 및 학습
- Simulation 환경에서 systematic comparison 수행 후, Unitree G1 humanoid robot에서 physical validation

## Originality

- **Gated Expert Selection Architecture**: Knowledge distillation의 lossy compression 문제를 회피하고 expert policies의 전체 capability를 보존하면서 dynamic routing하는 새로운 구조
- **VAE-based Motion Prior for Real-time Control**: 미래 정보 부재 상황에서 historical observations로부터 implicit future motion intent를 추출하는 novel approach, 기존 adversarial motion priors와 다른 방식의 motion modeling
- **Inertial MoCap Device Selection**: VR, exoskeleton, optical motion capture 등 기존 방식 대비 휴대성과 정확도의 균형을 새롭게 고려한 입력 모달리티 선택
- **Limited Data, High Precision Paradigm**: 기존 data scaling 전략(SONIC 700h)과 달리, 제한된 데이터(2.5h)로 높은 정밀도 달성의 새로운 paradigm 제시

## Limitation & Further Study

- Gating network의 동적 expert 선택이 smooth하게 이루어지지 않을 경우 policy switching 순간 tracking quality 저하 가능성 — 향후 더 정교한 blending mechanism 필요
- VAE 기반 motion prior의 예측 horizon이 제한적일 수 있어 매우 긴 선행 시간이 필요한 동작에 대한 한계 가능성 — recurrent 구조나 attention mechanism 도입 검토
- Domain clustering에 사용된 dynamic similarity metric의 정의가 명확하지 않으며, 새로운 motion category 추가 시 기존 experts와의 상호작용 영향 미분석
- Real-world 실험이 Unitree G1 단일 로봇에 국한되어 다른 humanoid platforms로의 generalization 검증 필요
- Inertial motion capture의 누적 오류(drift) 문제와 실제 teleoperation 환경에서의 latency 영향에 대한 분석 부족

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: TeleGate는 gated expert selection과 VAE 기반 motion prior를 결합하여 제한된 데이터로도 높은 정밀도의 real-time whole-body humanoid teleoperation을 실현하는 혁신적인 프레임워크이며, Unitree G1에서의 성공적인 physical deployment로 실제 적용 가능성을 입증했다.

## Related Papers

- 🔄 다른 접근: [[papers/1983_HOMIE_Humanoid_Loco-Manipulation_with_Isomorphic_Exoskeleton/review]] — TeleGate는 expert selection을 통한 텔레오퍼레이션을 제안하고 HOMIE는 isomorphic exoskeleton을 사용하는 서로 다른 전신 제어 접근법입니다.
- 🏛 기반 연구: [[papers/2124_Open-TeleVision_Teleoperation_with_Immersive_Active_Visual_F/review]] — Open-TeleVision의 immersive 시각 텔레오퍼레이션 기술이 TeleGate의 실시간 전신 텔레오퍼레이션을 위한 핵심 기반이 됩니다.
- 🔗 후속 연구: [[papers/2164_TWIST2_Scalable_Portable_and_Holistic_Humanoid_Data_Collecti/review]] — TeleGate의 gated expert selection을 TWIST2의 확장 가능한 데이터 수집 시스템과 결합하면 더 효율적인 휴머노이드 학습이 가능합니다.
- 🔄 다른 접근: [[papers/1756_Whole-Body_Bilateral_Teleoperation_with_Multi-Stage_Object_P/review]] — gated expert selection 대신 다단계 객체 인식을 통한 전신 양손 원격조종 접근법을 제시한다.
- 🏛 기반 연구: [[papers/1963_H2-COMPACT_Human-Humanoid_Co-Manipulation_via_Adaptive_Conta/review]] — 인간-휴머노이드 협력적 제어의 기본 원리가 TeleGate의 expert policy 선택 메커니즘에 적용된다.
- 🔗 후속 연구: [[papers/2168_UniAct_Unified_Motion_Generation_and_Action_Streaming_for_Hu/review]] — 실시간 전신 원격조종 기술을 다양한 multimodal 명령 스트리밍으로 확장한 발전된 형태이다.
- 🔄 다른 접근: [[papers/1839_CLONE_Closed-Loop_Whole-Body_Humanoid_Teleoperation_for_Long/review]] — CLONE의 closed-loop teleoperation이 TeleGate의 gated expert selection과 다른 continuous control 접근법으로 real-time whole-body teleoperation을 달성합니다.
- 🏛 기반 연구: [[papers/1924_FARM_Frame-Accelerated_Augmentation_and_Residual_Mixture-of-/review]] — FARM의 residual mixture-of-experts가 TeleGate의 multiple expert policies 동적 선택에서 전문가 네트워크 구조의 기술적 토대를 제공합니다.
- 🔗 후속 연구: [[papers/2163_TWIST_Teleoperated_Whole-Body_Imitation_System/review]] — TWIST의 teleoperated whole-body imitation이 TeleGate의 gated expert selection을 더 포괄적인 imitation learning으로 확장한 형태입니다.
- 🏛 기반 연구: [[papers/1690_Stability-Aware_Retargeting_for_Humanoid_Multi-Contact_Teleo/review]] — TeleGate의 전신 휴머노이드 텔레오퍼레이션에 안정성 인식 retargeting이 필수적인 안전 기술을 제공한다
- 🔄 다른 접근: [[papers/1707_Teleoperation_of_Humanoid_Robots_A_Survey/review]] — 포괄적 서베이와 구체적인 TeleGate 시스템이 휴머노이드 텔레오퍼레이션의 이론과 실제를 상호 보완한다
- 🔄 다른 접근: [[papers/1835_CHILD_Controller_for_Humanoid_Imitation_and_Live_Demonstrati/review]] — CHILD의 직접 관절 매핑 방식과 TeleGate의 게이트 전문가 기반 접근법은 휴머노이드 텔레오퍼레이션에 대한 서로 다른 제어 패러다임을 제시한다.
- 🔄 다른 접근: [[papers/1839_CLONE_Closed-Loop_Whole-Body_Humanoid_Teleoperation_for_Long/review]] — CLONE의 MoE 기반 폐루프 제어와 TeleGate의 게이트 전문가 방식은 휴머노이드 전신 텔레오퍼레이션에 대한 서로 다른 제어 아키텍처를 제시한다.
- 🔗 후속 연구: [[papers/1970_Heavy_lifting_tasks_via_haptic_teleoperation_of_a_wheeled_hu/review]] — TeleGate의 gated expert 기반 전신 텔레오퍼레이션이 햅틱 피드백 방식을 발전시킵니다.
- 🔄 다른 접근: [[papers/2163_TWIST_Teleoperated_Whole-Body_Imitation_System/review]] — TeleGate의 gated expert 접근법과 TWIST의 통합 신경망 접근법은 휴머노이드 텔레오퍼레이션의 상이한 아키텍처를 비교할 수 있음
- 🏛 기반 연구: [[papers/2168_UniAct_Unified_Motion_Generation_and_Action_Streaming_for_Hu/review]] — 실시간 전신 원격조종의 기본 기술이 다양한 multimodal 명령의 통합 스트리밍 실행으로 확장된다.
