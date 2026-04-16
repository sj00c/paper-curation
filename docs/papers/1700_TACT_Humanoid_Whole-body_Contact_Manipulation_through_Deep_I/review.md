---
title: "1700_TACT_Humanoid_Whole-body_Contact_Manipulation_through_Deep_I"
authors:
  - "Masaki Murooka"
  - "Takahiro Hoshi"
  - "Kensuke Fukumitsu"
  - "Shimpei Masuda"
  - "Marwan Hamze"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "인간형 로봇이 촉각 센서를 활용한 모방 학습(imitation learning)을 통해 전신 접촉 조작을 수행할 수 있도록 하는 TACT(tactile-modality extended ACT) 제어 시스템을 제안하였다."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "sub/Tactile_Contact_Control"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Murooka et al._2025_TACT Humanoid Whole-body Contact Manipulation through Deep Imitation Learning with Tactile Modality.pdf"
---

# TACT: Humanoid Whole-body Contact Manipulation through Deep Imitation Learning with Tactile Modality

> **저자**: Masaki Murooka, Takahiro Hoshi, Kensuke Fukumitsu, Shimpei Masuda, Marwan Hamze, Tomoya Sasaki, Mitsuharu Morisawa, Eiichi Yoshida | **날짜**: 2025-06-18 | **URL**: [https://arxiv.org/abs/2506.15146](https://arxiv.org/abs/2506.15146)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2. Humanoid control system for whole-body contact manipulation with tactile feedback.*

인간형 로봇이 촉각 센서를 활용한 모방 학습(imitation learning)을 통해 전신 접촉 조작을 수행할 수 있도록 하는 TACT(tactile-modality extended ACT) 제어 시스템을 제안하였다.

## Motivation

- **Known**: 인간형 로봇의 대부분 조작 연구는 손과 발 같은 말단부 접촉만 다루며, 전신 접촉 조작을 위한 기존 모델 기반 방법들은 계산 비용이 높고 광범위 접촉 측정이 어렵다는 한계가 있다.
- **Gap**: 인간처럼 전신을 활용한 균형잡힌 접촉 조작을 수행하면서도 분산된 촉각 센서 정보를 효과적으로 활용하는 학습 기반 제어 방법이 부족하다.
- **Why**: 전신 접촉 조작은 안정성 향상과 부하 감소라는 장점이 있으며, 섬세한 접촉이 필요한 실생활 작업 수행을 위해 필수적이다.
- **Approach**: Transformer 기반 정책인 ACT를 촉각 모달리티로 확장하여 다중 센서(관절 위치, 시각, 촉각) 입력을 처리하고, 모방 학습으로 인간 텔레오퍼레이션 데이터로부터 학습하며, 이를 모델 기반 재타겟팅 및 보행 제어와 통합하였다.

## Achievement

![Figure 5](figures/fig5.webp)

*Fig. 5. Experiment in which a humanoid holds up a paper box.*

- **촉각 모달리티 통합**: ACT를 확장하여 처음으로 분산된 촉각 센서 데이터를 직접 Transformer 기반 정책에 입력할 수 있도록 구현
- **다층 제어 아키텍처**: 모델 기반 제어의 신뢰성과 학습 기반 제어의 유연성을 결합한 이층 구조 개발
- **전신 접촉 조작 실증**: 생활 규모의 인간형 로봇 RHP7 Kaleido가 균형을 유지하면서 보행과 동시에 섬세한 전신 접촉 조작 달성
- **센서 융합의 효과 검증**: 시각과 촉각 모달리티의 동시 입력이 광범위하고 섬세한 접촉 조작의 견고성을 향상시킴을 실험으로 증명

## How

![Figure 4](figures/fig4.webp)

*Fig. 4. Model structure of TACT (tactile-modality extended ACT).*

- 인간 텔레오퍼레이션 데이터 수집: 포즈 추적기를 착용한 인간의 자세를 로봇으로 재타겟팅하며 수집
- TACT 정책 아키텍처: 촉각 센서 격자의 공간 구조를 Transformer를 통해 암시적으로 학습
- 다중 센서 입력 처리: 관절 위치, 카메라 이미지, 분산 촉각 측정값을 일정 시간 호라이즌에 대해 처리
- 상위층 제어: 학습 기반 TACT 정책이 미래 동작 명령 생성
- 하위층 제어: 모델 기반 재타겟팅과 쌍족 모델 기반 보행 제어로 균형 유지
- 기하학적 캘리브레이션 제거: 그래프 신경망과 달리 사전 공간 맵 구축 없이 Transformer의 자기 주의 메커니즘으로 센서 셀 간 상관관계 학습

## Originality

- 촉각 센서 데이터의 직접 통합: 기존 ACT를 최초로 분산 촉각 센서 입력을 처리하도록 확장
- 생활 규모 로봇의 전신 접촉 조작: 학습 기반 정책으로 사전 정의되지 않은 접촉점에서의 전신 조작 달성
- 하이브리드 제어 구조: 신뢰성과 유연성을 모두 확보하는 모델 기반-학습 기반 통합 시스템
- 다중 모달리티 처리: 관절 위치, 시각, 촉각을 Transformer로 통합 처리하는 설계

## Limitation & Further Study

- 데이터 수집 의존성: 텔레오퍼레이션 기반 수집이므로 데이터 품질과 다양성에 의존
- 촉각 센서 배치 제약: 현재 상반신만 센서 장착으로 전신 접촉 감지 제한
- 일반화 능력 미검증: 학습 데이터와 다른 객체 또는 환경에서의 성능 한계 논의 부족
- 계산 복잡도: 후속 연구에서 실시간 처리를 위한 모델 경량화 필요
- 정량적 비교 부족: 시각/촉각 단독 입력 대비 성능 향상도를 더 상세히 분석할 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 연구는 촉각 센서를 Transformer 기반 모방 학습에 성공적으로 통합하여 생활 규모 인간형 로봇의 섬세한 전신 접촉 조작을 최초로 실증했으며, 모델 기반 제어와 학습 기반 제어의 창의적 결합으로 신뢰성과 유연성을 동시에 확보한 의미 있는 기여이다.

## Related Papers

- 🔄 다른 접근: [[papers/1853_Coordinated_Humanoid_Manipulation_with_Choice_Policies/review]] — TACT의 촉각 기반 모방학습과 Choice Policy의 다중 후보 행동 학습은 휴머노이드 조작의 서로 다른 센서 활용 방식
- 🔗 후속 연구: [[papers/1614_Physically_Consistent_Humanoid_Loco-Manipulation_using_Laten/review]] — 물리적 일관성 로코-조작이 TACT의 촉각 접촉 조작을 장기 계획과 결합한 확장 형태
- 🏛 기반 연구: [[papers/2130_OSMO_Open-Source_Tactile_Glove_for_Human-to-Robot_Skill_Tran/review]] — OSMO 촉각 글러브의 인간-로봇 스킬 전이가 TACT의 촉각 모방학습을 위한 직접적 데이터 수집 기반
- 🔄 다른 접근: [[papers/1616_PICO_Reconstructing_3D_People_In_Contact_with_Objects/review]] — 둘 다 접촉 중심 상호작용을 다루지만 TACT는 촉각 모방 학습에, PICO는 시각적 접촉 복원에 초점을 맞춘다
- 🔄 다른 접근: [[papers/1659_RUKA_Rethinking_the_Design_of_Humanoid_Hands_with_Learning/review]] — 둘 다 손 기반 조작을 다루지만 촉각 센서 활용 vs tendon-driven 메커니즘으로 접근이 다르다
- 🔗 후속 연구: [[papers/1659_RUKA_Rethinking_the_Design_of_Humanoid_Hands_with_Learning/review]] — RUKA의 learning-based control과 TACT의 촉각 모방 학습을 결합하면 더 정교한 접촉 조작이 가능하다
- 🏛 기반 연구: [[papers/1614_Physically_Consistent_Humanoid_Loco-Manipulation_using_Laten/review]] — TACT의 촉각 기반 모방학습이 물리적 일관성 있는 조작을 위한 접촉 정보 활용 측면에서 기반 기술
- 🔗 후속 연구: [[papers/1616_PICO_Reconstructing_3D_People_In_Contact_with_Objects/review]] — PICO의 접촉 정보 활용 3D 인간-물체 상호작용 복원 기술이 촉각 기반 전신 접촉 조작 학습에 데이터셋과 방법론을 제공한다
- 🔄 다른 접근: [[papers/1853_Coordinated_Humanoid_Manipulation_with_Choice_Policies/review]] — Choice Policy의 다중 후보 행동 학습과 TACT의 촉각 기반 모방학습은 휴머노이드 조작의 서로 다른 학습 방식
- 🏛 기반 연구: [[papers/1931_Flow_Matching_Imitation_Learning_for_Multi-Support_Manipulat/review]] — 전신 접촉 조작이 다중 지지점 조작 학습의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1980_HiWET_Hierarchical_World-Frame_End-Effector_Tracking_for_Lon/review]] — deep reinforcement learning을 통한 whole-body contact manipulation이 HiWET의 계층적 end-effector 추적의 기반 제어 기술입니다.
- 🔄 다른 접근: [[papers/1981_HMC_Learning_Heterogeneous_Meta-Control_for_Contact-Rich_Loc/review]] — 접촉 기반 조작을 HMC는 heterogeneous meta-control로, TACT는 깊은 RL 기반 접촉으로 접근한다.
- 🔄 다른 접근: [[papers/2106_MorphoGuard_A_Morphology-Based_Whole-Body_Interactive_Motion/review]] — MorphoGuard는 형태학적 표현 기반, TACT는 접촉 조작 기반으로 서로 다른 관점에서 휴머노이드 전신 접촉 제어 문제를 해결한다.
- 🏛 기반 연구: [[papers/2165_ULC_A_Unified_and_Fine-Grained_Controller_for_Humanoid_Loco-/review]] — 심층 강화학습을 통한 휴머노이드 전신 접촉 조작 기법이 상체-하체 통합 제어를 위한 단일 정책 프레임워크의 기반이 됩니다.
