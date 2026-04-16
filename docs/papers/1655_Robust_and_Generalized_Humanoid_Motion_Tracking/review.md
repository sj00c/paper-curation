---
title: "1655_Robust_and_Generalized_Humanoid_Motion_Tracking"
authors:
  - "Yubiao Ma"
  - "Han Yu"
  - "Jiayin Xie"
  - "Changtai Lv"
  - "Qiang Luo"
date: "2026.01"
doi: "10.48550/arXiv.2601.23080"
arxiv: ""
score: 4.0
essence: "휴머노이드 로봇의 일반적인 전신 제어를 위해 dynamics-conditioned command aggregation 프레임워크를 제안하며, 인과적 temporal encoder와 multi-head cross-attention을 결합하여 노이즈가 있는 참조 동작에 강건하게 대응한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Ma et al._2026_Robust and Generalized Humanoid Motion Tracking.pdf"
---

# Robust and Generalized Humanoid Motion Tracking

> **저자**: Yubiao Ma, Han Yu, Jiayin Xie, Changtai Lv, Qiang Luo, Chi Zhang, Yunpeng Yin, Boyang Xing, Xuemei Ren, Dongdong Zheng | **날짜**: 2026-01-30 | **DOI**: [10.48550/arXiv.2601.23080](https://doi.org/10.48550/arXiv.2601.23080)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the proposed whole-body control pipeline. A history encoder extracts a dynamics embedding from*

휴머노이드 로봇의 일반적인 전신 제어를 위해 dynamics-conditioned command aggregation 프레임워크를 제안하며, 인과적 temporal encoder와 multi-head cross-attention을 결합하여 노이즈가 있는 참조 동작에 강건하게 대응한다.

## Motivation

- **Known**: 기존 humanoid motion tracking 연구는 단일 동작이나 소규모 동작 집합에 대해 학습되어 일반화 능력이 제한되며, 동적 동작과 접촉 전환 시 추적 정확도와 폐루프 안정성이 최적이 아니다.
- **Gap**: 대규모 데이터(700시간 이상)와 계산 리소스에 의존하지 않으면서도 일반화된 전신 제어기를 학습하고, 낙하 회복을 통합하여 단일 정책으로 폐루프 안정성과 견고성을 동시에 달성하는 방법의 부재.
- **Why**: 휴머노이드 로봇이 다양한 환경과 작업에 적응하려면 여러 동작을 아우르는 강건한 단일 정책이 필수적이며, 이를 통해 연구 접근성을 높이고 실제 배포 안전성을 향상시킬 수 있다.
- **Approach**: 최근 proprioception 히스토리로부터 동역학 표현을 추출하는 causal temporal encoder와 현재 동역학에 기반하여 contextual command window를 선택적으로 집계하는 multi-head cross-attention command encoder를 결합하며, 불안정한 초기화와 annealed assistance force를 통한 낙하 회복 커리큘럼을 통합한다.

## Achievement


- **효율적인 학습**: 약 3.5시간의 컴팩트 모션 데이터셋으로 distillation 없는 단일 단계 end-to-end 학습 달성
- **강건한 일반화**: mocap, 비디오 기반 포즈 추정, 실시간 VR 텔레오퍼레이션 등 다양한 참조 소스에 대해 일반화
- **제로샷 전이**: 학습하지 않은 동작에 대해 제로샷 전이 능력 입증
- **통합된 견고성**: 낙하 회복을 메인 정책에 통합하여 동적 동작과 접촉이 풍부한 시나리오에서 뛰어난 견고성과 외란 거부 능력 확보
- **실제 로봇 배포**: Unitree G1 휴머노이드 로봇에서 안정적인 장기간 추적 및 다운스트림 애플리케이션(조이스틱 구동 로코모션) 성공

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the proposed whole-body control pipeline. A history encoder extracts a dynamics embedding from*

- Causal temporal encoder를 이용하여 recent proprioception ([gravity direction, angular velocity, joint positions/velocities, previous action])에서 compact dynamics embedding 추출
- Multi-head cross-attention 메커니즘으로 현재 dynamics embedding을 query로 하여 command window의 contextual reference targets을 동적으로 집계
- Command observation으로 reference base velocities, reference gravity direction, reference joint positions 제공
- Asymmetric actor-critic 구조: actor는 noisy observation 입력, critic은 privileged observation (reference height, link poses, base velocity) 추가 입력
- 잔차 제어 공식화 (residual joint position offset at을 reference joint configuration qref에 더함)로 PD setpoint 설정
- 밀도 있는 보상 함수: keypoint alignment, relative pose consistency, keypoint velocity consistency 추적 + action smoothness, joint limit, non-target contact penalization
- 낙하 회복 커리큘럼: randomized unstable initialization과 annealed upward assistance force를 결합하여 로봇을 더 넓은 state distribution으로 노출
- Motion dataset quality control: LAFAN1과 AMASS의 선택된 부분을 General Motion Retargeting으로 재타겟팅하되, 낮은 품질 및 불가능한 동작 제거

## Originality

- Dynamics-conditioned command aggregation 설계의 창의성: 단순히 reference를 그대로 따르기보다, 현재 동역학 상태에 기반하여 참조 신호의 신뢰도를 적응적으로 판단하고 집계
- Causal temporal encoder와 multi-head cross-attention의 조합: 기존 RL 기반 motion tracking에서 rarely seen되는 아키텍처로, 노이즈가 있는 참조에 대한 새로운 대응 방식
- 통합된 낙fall recovery: 별도 정책이 아닌 단일 정책에 낙하 회복을 직접 포함시켜 학습 효율성과 실제 안전성을 동시에 향상
- 컴팩트 데이터셋의 효율적 활용: quality-driven construction과 dynamics-conditioned aggregation의 결합으로 기존 대규모 데이터 의존성 극복

## Limitation & Further Study

- 현재 방법은 약 3.5시간의 고품질 motion data 선별에 의존하며, 이 quality control 프로세스의 자동화 방안 부재
- Dynamics-conditioned command aggregation이 어떤 종류의 노이즈 패턴(periodic vs. transient vs. structural artifacts)에 특히 강건한지에 대한 세부 분석 부족
- Transfer learning 측면에서 타 humanoid 플랫폼 (예: Boston Dynamics Atlas, Tesla Optimus)으로의 일반화 가능성 미검증
- Long-horizon task (예: 복합 조작, 환경 상호작용)에서의 성능 평가 부재 — 현재는 주로 motion tracking과 locomotion에 한정
- Temporal receptive field와 attention window size 선택에 대한 민감도 분석 및 ablation study 확대 필요
- Sim-to-real transfer 중 domain randomization 및 identification 전략의 세부 사항 미기술

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 dynamics-conditioned command aggregation이라는 우아한 설계를 통해 컴팩트한 데이터셋으로도 강건한 일반화 휴머노이드 전신 제어를 달성하며, 낙하 회복의 통합과 실제 로봇 배포 검증으로 높은 실용성을 보여준다.

## Related Papers

- 🔄 다른 접근: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — 두 논문 모두 인간 모션을 휴머노이드 로봇이 추적하는 문제를 다루지만, 다른 네트워크 아키텍처를 사용한다.
- 🔗 후속 연구: [[papers/1955_GMT_General_Motion_Tracking_for_Humanoid_Whole-Body_Control/review]] — GMT의 일반적인 모션 추적 방법론을 dynamics-conditioned aggregation으로 확장하여 노이즈에 더 강건하게 만든다.
- 🏛 기반 연구: [[papers/1685_SONIC_Supersizing_Motion_Tracking_for_Natural_Humanoid_Whole/review]] — SONIC의 대규모 motion tracking 접근법이 본 논문의 강건한 모션 추적 프레임워크의 기반이 된다.
- 🔗 후속 연구: [[papers/1665_Scalable_and_General_Whole-Body_Control_for_Cross-Humanoid_L/review]] — 단일 로봇의 robust motion tracking을 여러 휴머노이드 형태로 확장하는 cross-humanoid 일반화입니다.
- 🔄 다른 접근: [[papers/1667_SCDP_Learning_Humanoid_Locomotion_from_Partial_Observations/review]] — 전역 정보 기반 motion tracking vs 부분 관측만으로 하는 locomotion이라는 다른 접근 방식입니다.
- 🏛 기반 연구: [[papers/1665_Scalable_and_General_Whole-Body_Control_for_Cross-Humanoid_L/review]] — 단일 로봇의 robust control이 여러 휴머노이드로의 일반화를 위한 기본 전제입니다.
- ⚖️ 반론/비판: [[papers/1667_SCDP_Learning_Humanoid_Locomotion_from_Partial_Observations/review]] — privileged information 없는 제한적 센서 vs robust한 전역 정보 활용이라는 대조적 관점입니다.
- 🏛 기반 연구: [[papers/1685_SONIC_Supersizing_Motion_Tracking_for_Natural_Humanoid_Whole/review]] — 강건하고 일반화된 휴머노이드 모션 추적의 기초적인 방법론을 제공한다.
- 🏛 기반 연구: [[papers/1660_RuN_Residual_Policy_for_Natural_Humanoid_Locomotion/review]] — motion prior 기반 자연스러운 보행이 robust motion tracking의 기초 methodology가 됩니다.
- 🔗 후속 연구: [[papers/1758_Whole-body_Humanoid_Robot_Locomotion_with_Human_Reference/review]] — Robust and Generalized Motion Tracking이 Adam의 인간 수준 보행을 더 다양한 환경으로 확장합니다.
- 🏛 기반 연구: [[papers/1826_Biomechanical_Comparisons_Reveal_Divergence_of_Human_and_Hum/review]] — Robust and Generalized Humanoid Motion Tracking의 견고한 동작 추적 기술이 GDAF의 정확한 보행 분석을 위한 기술적 기반이 된다.
- 🔄 다른 접근: [[papers/2088_Make_Tracking_Easy_Neural_Motion_Retargeting_for_Humanoid_Wh/review]] — 강건하고 일반화된 휴머노이드 동작 추적과 신경 동작 리타겟팅이라는 다른 접근법을 제시한다.
- 🔄 다른 접근: [[papers/2158_Track_Any_Motions_under_Any_Disturbances/review]] — Any2Track은 교란 적응에 특화된 두 단계 학습을 제안하고 Robust and Generalized Motion Tracking은 일반화된 강건성을 추구하는 서로 다른 접근법입니다.
