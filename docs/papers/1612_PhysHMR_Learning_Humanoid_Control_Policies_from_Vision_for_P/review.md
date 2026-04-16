---
title: "1612_PhysHMR_Learning_Humanoid_Control_Policies_from_Vision_for_P"
authors:
  - "Qiao Feng"
  - "Yiming Huang"
  - "Yufu Wang"
  - "Jiatao Gu"
  - "Lingjie Liu"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "PhysHMR은 모노큘러 비디오로부터 물리적으로 타당한 인간 동작 재구성을 위해 비전-기반 휴머노이드 제어 정책을 직접 학습하는 통합 프레임워크이다. 기존의 두 단계 방식(운동학 기반 추정 + 물리 후처리)과 달리, 시각 정보와 물리 제약을 단일 정책 네트워크에서 함께 추론한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Feng et al._2025_PhysHMR Learning Humanoid Control Policies from Vision for Physically Plausible Human Motion Recons.pdf"
---

# PhysHMR: Learning Humanoid Control Policies from Vision for Physically Plausible Human Motion Reconstruction

> **저자**: Qiao Feng, Yiming Huang, Yufu Wang, Jiatao Gu, Lingjie Liu | **날짜**: 2025-10-02 | **URL**: [https://arxiv.org/abs/2510.02566](https://arxiv.org/abs/2510.02566)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Given a monocular video (a), (b) kinematic-based methods (e.g., GVHMR [Shen et al. 2024]) often cannot produce p*

PhysHMR은 모노큘러 비디오로부터 물리적으로 타당한 인간 동작 재구성을 위해 비전-기반 휴머노이드 제어 정책을 직접 학습하는 통합 프레임워크이다. 기존의 두 단계 방식(운동학 기반 추정 + 물리 후처리)과 달리, 시각 정보와 물리 제약을 단일 정책 네트워크에서 함께 추론한다.

## Motivation

- **Known**: 기존 HMR 방법들은 운동학 기반 자세 추정에 집중하여 발 슬라이딩, 지면 침투, 불일관한 접촉 동작 등의 비물리적 인공물을 생성한다. 사후 물리 기반 보정을 통해 개선하려는 시도들도 있으나, 두 단계 설계로 인해 오류 누적이 발생한다.
- **Gap**: 모노큘러 비디오는 본질적으로 모호성을 가지며, 같은 시각 관찰을 설명할 수 있는 여러 물리적 동작이 존재한다. 재구성 단계에서 단일 해를 선택하면 다운스트림 물리 모듈이 전체 관찰 맥락에 접근할 수 없어 최적이 아닌 보정이 발생한다.
- **Why**: 물리적으로 타당한 동작 재구성은 시뮬레이션, 애니메이션, 로봇 등 다운스트림 응용에 필수적이며, 통합 접근법은 시각 증거와 물리 제약 간의 충돌을 근본적으로 해결할 수 있다.
- **Approach**: PhysHMR은 물리 기반 시뮬레이터 내에서 모노큘러 비디오로부터 직접 제어 신호를 예측하는 시각-대-행동 정책을 학습한다. mocap 학습된 모방 전문가로부터의 distillation과 물리 기반 강화학습 보상을 통해 효율적으로 정책을 훈련한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Given a monocular video (a), (b) kinematic-based methods (e.g., GVHMR [Shen et al. 2024]) often cannot produce p*

- **통합 프레임워크**: 기존의 분리된 재구성-보정 파이프라인을 단일 정책 네트워크로 통합하여 오류 누적 제거
- **Soft Global Grounding**: 2D 키포인트를 3D spatial ray로 변환하여 노이즈 있는 3D 루트 예측 회피 및 강건한 전역 자세 안내 제공
- **Distillation 기반 훈련**: mocap 학습된 모방 전문가로부터의 지식 이전으로 강화학습의 샘플 비효율성 극복
- **평가 및 성과**: Human3.6M, AIST++, EMDB2에서 기존 운동학 기반 방법과 비교 가능한 정확도 유지하면서 물리적 타당성 대폭 향상

## How

![Figure 2](figures/fig2.webp)

*Fig. 2 provides an overview of our method. Given a monocular*

- pretrained visual encoder로부터 각 프레임의 특징 추출하여 로컬 자세 참조 제공
- 2D keypoint 검출 후 3D spatial ray로 변환하여 글로벌 공간에서 소프트 제약 조건으로 사용
- mocap 데이터로 학습된 모방 전문가 정책의 행동 감독으로 시각-기반 정책 distillation
- Motion imitation, adversarial motion prior, physical smoothness를 균형잡은 composite reward로 강화학습 정제
- 물리 시뮬레이터(Isaac Gym)에서 정책 실행하여 접촉, 관절 제한, 운동량 보존 등 물리 제약 자동 시행

## Originality

- 시각 기반 휴머노이드 제어와 모션 재구성을 처음으로 통합하는 end-to-end 프레임워크 제시
- 2D keypoint를 3D ray로 변환하는 pixel-as-ray 전략으로 3D 루트 예측의 노이즈 문제 혁신적 해결
- mocap 학습 모방 정책으로부터의 지식 distillation을 강화학습과 결합한 하이브리드 훈련 기법
- 단순 자세 추정을 넘어 물리 동역학을 직접 학습하는 패러다임 전환

## Limitation & Further Study

- 물리 시뮬레이터의 카메라 모델과 실제 비디오 카메라 간 sim-to-real 격차 미해결
- 극단적 동작이나 비상황적 움직임에 대한 일반화 성능 미평가
- 계산 비용: 시뮬레이터 기반 훈련의 온라인 비용이 순수 운동학 방법보다 높음
- mocap 데이터 의존성: 고품질 mocap 데이터 없는 시나리오에서 distillation 효과 미실증
- 후속 연구: (1) 다양한 신체 형태 및 의상 처리, (2) 실시간 처리 최적화, (3) 비표준 활동(악기 연주, 도구 사용)에 대한 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: PhysHMR은 시각-기반 제어와 물리 추론을 통합하는 창의적 접근으로 모노큘러 비디오 기반 인간 동작 재구성의 근본적 문제를 해결한다. 우수한 물리적 타당성 개선과 실질적 응용 가치로 컴퓨터 비전과 그래픽스 분야에 의미 있는 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1862_DeepMimic_Example-Guided_Deep_Reinforcement_Learning_of_Phys/review]] — PhysHMR의 비전-기반 물리적 제어 정책 학습이 DeepMimic의 example-guided 강화학습 방법론을 확장한 것이다
- 🔄 다른 접근: [[papers/2137_PhysDiff_Physics-Guided_Human_Motion_Diffusion_Model/review]] — 두 논문 모두 물리적으로 타당한 인간 동작 생성을 다루지만 PhysHMR은 비전-제어 통합에, PhysDiff는 확산 모델에 집중한다
- 🔗 후속 연구: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — PhysHMR의 통합 프레임워크가 ResMimic의 잔차 학습과 결합되어 더 정밀한 전신 제어를 실현할 수 있다
- 🔄 다른 접근: [[papers/1753_VisualMimic_Visual_Humanoid_Loco-Manipulation_via_Motion_Tra/review]] — 같은 비전 기반 humanoid motion imitation 문제를 motion tracking 접근법으로 해결
- 🔗 후속 연구: [[papers/1809_ASE_Large-Scale_Reusable_Adversarial_Skill_Embeddings_for_Ph/review]] — ASE의 adversarial skill embedding이 PhysHMR의 비전 기반 제어 정책으로 확장되어 시각적 입력에서 직접 스킬을 학습할 수 있다
- 🏛 기반 연구: [[papers/1975_Hierarchical_visuomotor_control_of_humanoids/review]] — PhysHMR의 vision-based humanoid control이 hierarchical visuomotor control의 시각 정보 처리 부분을 위한 기초 방법론을 제공한다.
