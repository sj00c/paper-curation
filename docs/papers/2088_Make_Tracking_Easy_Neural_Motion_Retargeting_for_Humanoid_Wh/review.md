---
title: "2088_Make_Tracking_Easy_Neural_Motion_Retargeting_for_Humanoid_Wh"
authors:
  - "Qingrui Zhao"
  - "Kaiyue Yang"
  - "Xiyu Wang"
  - "Shiqi Zhao"
  - "Yi Lu"
date: "2026.03"
doi: ""
arxiv: ""
score: 4.0
essence: "기존 최적화 기반 모션 리타겟팅의 비볼록 문제를 해결하기 위해 Neural Motion Retargeting (NMR) 프레임워크를 제안하며, VAE 기반 클러스터링과 RL 전문가를 활용한 Clustered-Expert Physics Refinement (CEPR) 파이프라인으로 인간 동작을 휴머노이드 로봇의 실행 가능한 동작으로 변환한다."
tags:
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Humanoid_Diffusion_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhao et al._2026_Make Tracking Easy Neural Motion Retargeting for Humanoid Whole-body Control.pdf"
---

# Make Tracking Easy: Neural Motion Retargeting for Humanoid Whole-body Control

> **저자**: Qingrui Zhao, Kaiyue Yang, Xiyu Wang, Shiqi Zhao, Yi Lu, Xinfang Zhang, Wei Yin, Qiu Shen, Xiao-Xiao Long, Xun Cao | **날짜**: 2026-03-23 | **URL**: [https://arxiv.org/abs/2603.22201](https://arxiv.org/abs/2603.22201)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Data Construction Pipeline. We obtain high-quality human–humanoid motion pairs through three processing stages.*

기존 최적화 기반 모션 리타겟팅의 비볼록 문제를 해결하기 위해 Neural Motion Retargeting (NMR) 프레임워크를 제안하며, VAE 기반 클러스터링과 RL 전문가를 활용한 Clustered-Expert Physics Refinement (CEPR) 파이프라인으로 인간 동작을 휴머노이드 로봇의 실행 가능한 동작으로 변환한다.

## Motivation

- **Known**: 기존 inverse kinematics (IK) 기반 방법들과 GMR, PHC 등의 최적화 기반 리타겟팅 접근법이 존재하지만, 이들은 프레임별 기하학적 최적화에 초점을 맞춰 지역 최적값, 관절 점프, 자기 관통 등의 문제를 야기한다.
- **Gap**: 최적화 기반 방법의 수학적 비볼록성으로 인한 초기화 민감도와 지역 최적값 문제, 그리고 소스 데이터의 노이즈 전파 문제가 해결되지 않고 있다.
- **Why**: 휴머노이드 로봇이 복잡한 인간 환경에서 다양한 운동 기술을 습득하려면 인간-로봇 구현(embodiment) 간격을 효과적으로 해소하고 물리적으로 실현 가능한 고품질 동작 데이터가 필수적이다.
- **Approach**: 모션 리타겟팅 문제를 단일 프레임 최적화에서 모션 분포 학습으로 재정의하고, VAE 기반 클러스터링으로 이질적 동작을 분류한 후 병렬 RL 전문가들이 물리 시뮬레이터에서 동작을 추적 및 정제하여 고품질 학습 데이터를 자동으로 생성한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Visualization of NMR retargeting results with and without CEPR data fine-tuning*

- **NMR 프레임워크**: 최적화 기반 방법의 지역 최적값, 관절 불연속성, 자기 충돌 문제를 완화하는 신경망 기반 리타겟팅 접근법 제시
- **CEPR 데이터 파이프라인**: 모션 클러스터링, 병렬 RL 전문가 정책, 물리 기반 정제를 통해 약 30,000개의 물리적으로 일관성 있는 인간-로봇 동작 쌍 자동 생성
- **Transformer 기반 아키텍처**: CNN-Transformer 비자기귀귀(non-autoregressive) 설계로 글로벌 시간 문맥을 고려하여 재구성 노이즈 억제 및 기하학적 함정 우회
- **실험 성과**: Unitree G1 휴머노이드에서 다양한 동적 작업(격투기, 춤 등) 실험 결과 관절 점프와 자기 충돌이 현저히 감소하고 다운스트림 전신 제어 정책의 수렴 가속화

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Data Construction Pipeline. We obtain high-quality human–humanoid motion pairs through three processing stages.*

- VAE를 사용한 모션 특징 추출 및 이질적 인간 동작 데이터의 계층적 클러스터링
- 병렬 RL 전문가 정책들을 훈련하여 물리 시뮬레이터에서 클러스터링된 동작 추적 및 물리적 결함 자동 수정
- CNN-Transformer 하이브리드 아키텍처를 활용한 시간 의존성 모델링으로 SMPL 시퀀스를 로봇 동작으로 직접 매핑
- 상세 품질과 물리적 충실성을 모두 보장하는 2단계 훈련 전략(Detail to physical 스킴) 적용

## Originality

- 모션 리타겟팅 문제를 프레임별 최적화에서 분포 매핑으로 재정의하는 개념적 전환
- VAE 기반 클러스터링과 병렬 RL 전문가를 결합한 계층적 CEPR 파이프라인의 창의적 설계
- 비자기귀귀 CNN-Transformer 아키텍처를 모션 리타겟팅에 적용하여 글로벌 시간 문맥을 활용한 노이즈 억제
- Hessian 분석을 통한 기존 최적화 기반 방법의 비볼록성 이론적 검증

## Limitation & Further Study

- 약 30,000개의 동작 쌍 데이터셋 규모가 더 대규모 다양성을 요구하는 추가 응용에 제한적일 수 있음
- Unitree G1에 특화된 검증으로 다른 휴머노이드 플랫폼(예: Boston Dynamics Atlas, TESLA Optimus)으로의 일반화 가능성 미검증
- VAE 클러스터링의 최적 개수 결정 및 RL 전문가 훈련의 수렴 보장에 대한 이론적 분석 부재
- 후속 연구에서는 더 대규모 다양한 동작 데이터 수집, 다양한 로봇 형태 및 역학계에 대한 적응 메커니즘, 전이 학습 전략 개발이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 최적화 기반 모션 리타겟팅의 근본적 수학적 한계를 명확히 지적하고, 신경망 기반의 창의적인 대안을 제시하며 물리 기반 데이터 생성 파이프라인으로 실용성을 확보한 매우 우수한 연구이다.

## Related Papers

- 🏛 기반 연구: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — 일반 동작 추적에서 휴머노이드 전신 제어로의 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1655_Robust_and_Generalized_Humanoid_Motion_Tracking/review]] — 강건하고 일반화된 휴머노이드 동작 추적과 신경 동작 리타겟팅이라는 다른 접근법을 제시한다.
- 🔗 후속 연구: [[papers/2021_Implicit_Kinodynamic_Motion_Retargeting_for_Human-to-humanoi/review]] — 인간-휴머노이드 운동학적 동작 리타겟팅의 확장된 구현을 보여준다.
- 🏛 기반 연구: [[papers/1917_Example-based_Motion_Synthesis_via_Generative_Motion_Matchin/review]] — Example-based Motion Synthesis의 생성형 모션 매칭이 NMR의 클러스터링 기반 모션 리타겟팅의 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/2156_Towards_Motion_Turing_Test_Evaluating_Human-Likeness_in_Huma/review]] — 모션 리타겟팅의 품질을 Human-Likeness 평가 기준으로 확장하여 더 자연스러운 휴머노이드 동작을 달성할 수 있다.
- 🏛 기반 연구: [[papers/1681_SMAP_Self-supervised_Motion_Adaptation_for_Physically_Plausi/review]] — 휴머노이드 전신 제어를 위한 신경망 모션 리타게팅의 기초 방법론을 제공한다.
- 🏛 기반 연구: [[papers/1785_A_Whole-Body_Motion_Imitation_Framework_from_Human_Data_for/review]] — 신경망 기반 모션 리타겟팅 기술이 contact-aware 전신 모션 리타겟팅의 이론적 기반을 제공합니다.
- 🧪 응용 사례: [[papers/1858_cuRoboV2_Dynamics-Aware_Motion_Generation_with_Depth-Fused_D/review]] — cuRoboV2의 B-spline 궤적 최적화와 TSDF 파이프라인이 humanoid motion retargeting의 동적 실행 가능성 보장에 직접 활용될 수 있다.
- 🏛 기반 연구: [[papers/1891_DynaRetarget_Dynamically-Feasible_Retargeting_using_Sampling/review]] — neural motion retargeting이 DynaRetarget의 인간 동작을 humanoid 실행 가능한 행동으로 변환하는 기본 원리를 제공한다.
- 🏛 기반 연구: [[papers/1935_From_Language_to_Locomotion_Retargeting-free_Humanoid_Contro/review]] — 신경망 모션 리타겟팅이 retargeting-free 접근법의 대조되는 기반 기술이다.
- 🔄 다른 접근: [[papers/2021_Implicit_Kinodynamic_Motion_Retargeting_for_Human-to-humanoi/review]] — 인간 모션을 휴머노이드로 변환하는 문제에서 implicit kinodynamic 방식 대신 neural retargeting 접근법을 제시한다.
- 🔄 다른 접근: [[papers/2120_OmniRetarget_Interaction-Preserving_Data_Generation_for_Huma/review]] — Make Tracking Easy의 neural retargeting이 OmniRetarget의 optimization-based retargeting과 다른 neural network 접근법으로 유사한 motion retargeting 문제를 해결합니다.
- 🏛 기반 연구: [[papers/2136_PHUMA_Physically-Grounded_Humanoid_Locomotion_Dataset/review]] — neural motion retargeting 기술이 PHUMA의 physics-constrained retargeting의 핵심 기술적 토대가 됨
