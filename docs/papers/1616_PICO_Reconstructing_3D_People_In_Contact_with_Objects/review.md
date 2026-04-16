---
title: "1616_PICO_Reconstructing_3D_People_In_Contact_with_Objects"
authors:
  - "Alpár Cseke"
  - "Shashank Tripathi"
  - "Sai Kumar Dwivedi"
  - "Arjun Lakshmipathy"
  - "Agniv Chatterjee"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "단일 이미지에서 신체-물체 접촉 정보를 활용하여 3D 인간-물체 상호작용을 복원하는 PICO 프레임워크를 제시하며, 이를 위해 신체와 물체 모두에 밀집된 3D 접촉 주석이 있는 PICO-db 데이터셋을 수집했다."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Dexterous_Hand_Trajectory_Datasets"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Cseke et al._2025_PICO Reconstructing 3D People In Contact with Objects.pdf"
---

# PICO: Reconstructing 3D People In Contact with Objects

> **저자**: Alpár Cseke, Shashank Tripathi, Sai Kumar Dwivedi, Arjun Lakshmipathy, Agniv Chatterjee, Michael J. Black, Dimitrios Tzionas | **날짜**: 2025-04-24 | **URL**: [https://arxiv.org/abs/2504.17695](https://arxiv.org/abs/2504.17695)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. We present PICO, a novel framework for joint human-object reconstruction in 3D. PICO includes PICO-db, a uniqu*

단일 이미지에서 신체-물체 접촉 정보를 활용하여 3D 인간-물체 상호작용을 복원하는 PICO 프레임워크를 제시하며, 이를 위해 신체와 물체 모두에 밀집된 3D 접촉 주석이 있는 PICO-db 데이터셋을 수집했다.

## Motivation

- **Known**: 기존 연구들은 알려진 물체 형태나 제한된 물체 클래스에서만 3D HOI를 다루었으며, DAMON 데이터셋은 신체 접촉 주석만 제공한다.
- **Gap**: 현재 방법들은 임의의 물체 클래스에 대한 일반화가 어렵고, 신체와 물체 양쪽에서 3D 접촉을 함께 추론하는 데이터와 방법이 부족하다.
- **Why**: 자연 이미지에서 다양한 물체와의 상호작용을 이해하는 것은 스마트홈, 혼합현실, 로봇 보조 등 실제 응용에 필수적이며, 이를 통해 HOI 이해를 현실로 확장할 수 있다.
- **Approach**: 신체 접촉 패치를 물체에 투영하기 위해 vision foundation model(OpenShape)을 활용한 물체 검색과 최소 인력(2 클릭)을 조합하여 PICO-db를 구축하고, render-and-compare 최적화 기반의 PICO-fit 방법으로 접촉 정보를 통해 3D 신체-물체 메시를 반복적으로 적합시킨다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2. PICO-db dataset annotations. Left to right: Color im-*

- **PICO-db 데이터셋**: 신체와 물체 양쪽의 3D 접촉 주석을 가진 첫 번째 자연 이미지 데이터셋으로, 이원 신체-물체 접촉 대응점을 포함한다.
- **일반화 능력**: 이전에 다루지 못한 여러 물체 클래스(소파, 바나나, 프리스비 등)에 대해 작동하는 확장 가능한 방법을 제시한다.
- **정성적/정량적 개선**: PHOSA, HDM, CONTHO 등 기존 방법 대비 지각 연구에서 훨씬 더 현실적인 복원 결과를 보인다.
- **최소 주석 비용**: 2 클릭만으로 신체 접촉을 물체에 투영하는 효율적인 주석 방법을 개발했다.

## How

![Figure 4](figures/fig4.webp)

*Figure 4. Overview of PICO-fit, a novel method for fitting interacting 3D body and object meshes to an image. It initial*

- DAMON 데이터셋의 신체 접촉 패치를 시작점으로 PCA를 통해 자동 축 생성
- OpenShape foundation model을 활용하여 이미지에서 가장 유사한 3D 물체 메시를 Objaverse에서 검색
- ContactEdit 개념을 확장하여 2 클릭으로 신체 접촉 패치를 물체에 투영
- OSX를 통해 초기 신체 형태/자세 추론
- DECO를 사용하여 신체 접촉 추론, SAM으로 물체 클래스 인식
- PICO-db에서 가장 가까운 이웃 신체-물체 접촉 대응점 검색
- render-and-compare 최적화를 통해 접촉 제약을 사용하여 신체와 물체 메시를 반복적으로 적합

## Originality

- 신체와 물체 양쪽의 3D 접촉 주석을 포함한 첫 번째 자연 이미지 데이터셋 수집
- 최소 인력(2 클릭)으로 신체 접촉을 물체에 투영하는 새로운 방법 제시
- Vision foundation model(OpenShape)을 활용한 임의의 물체 클래스에 대한 메시 검색 및 일반화
- 접촉 정보를 활용하여 신체-물체 상호작용의 3D 포즈 추정을 가능하게 하는 render-and-compare 최적화 기반 방법
- 신체-물체 이원 접촉 대응점을 통한 풍부한 기하학적 제약 활용

## Limitation & Further Study

- Foundation model(OpenShape)의 물체 검색에 의존하므로 메시 데이터베이스 품질과 범위에 제한적
- 복잡한 다중 물체 상호작용이나 동적 상호작용에 대한 평가 부재
- 접촉 추론(DECO)이 실패하는 경우에 대한 강건성 분석 필요
- 정량적 평가가 제한적이며 대부분 정성적 결과와 지각 연구에 의존
- 후속 연구: 동영상 시퀀스 기반 시간적 일관성 개선, 더 복잡한 물체 위상 구조 처리, 자기-조절 학습을 통한 주석 비용 추가 감소

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 신체-물체 접촉이라는 새로운 관점에서 3D HOI 문제를 체계적으로 다루며, PICO-db라는 고가치 데이터셋과 확장 가능한 PICO-fit 방법을 통해 현실의 다양한 물체 클래스에 일반화되는 실용적인 해결책을 제시한다.

## Related Papers

- 🔗 후속 연구: [[papers/2148_TokenHSI_Unified_Synthesis_of_Physical_Human-Scene_Interacti/review]] — PICO의 3D 접촉 정보 복원 기술이 TokenHSI의 물리적 human-scene interaction 합성에서 더 정확한 접촉 모델링을 제공할 수 있다
- 🏛 기반 연구: [[papers/1758_WHOLE_World-Grounded_Hand-Object_Lifted_from_Egocentric_Vide/review]] — PICO-db 데이터셋의 밀집된 3D 접촉 주석이 WHOLE의 egocentric hand-object interaction 학습에 필수적인 ground truth를 제공한다
- 🧪 응용 사례: [[papers/1869_DexMimicGen_Automated_Data_Generation_for_Bimanual_Dexterous/review]] — PICO의 신체-물체 접촉 정보가 DexMimicGen의 bimanual manipulation 데이터 생성에서 물리적으로 타당한 접촉 제약을 제공할 수 있다
- 🔗 후속 연구: [[papers/1700_TACT_Humanoid_Whole-body_Contact_Manipulation_through_Deep_I/review]] — PICO의 접촉 정보 활용 3D 인간-물체 상호작용 복원 기술이 촉각 기반 전신 접촉 조작 학습에 데이터셋과 방법론을 제공한다
- 🔄 다른 접근: [[papers/1779_A_Humanoid_Visual-Tactile-Action_Dataset_for_Contact-Rich_Ma/review]] — 둘 다 접촉 중심의 데이터셋을 제공하지만 PICO는 단일 이미지에서, HATD는 시각-촉각-행동 통합에 초점을 맞춘다
- 🏛 기반 연구: [[papers/2115_OKAMI_Teaching_Humanoid_Robots_Manipulation_Skills_through_S/review]] — OKAMI의 인간 모션 데이터 활용 조작 학습에 PICO의 3D 접촉 주석 데이터셋이 중요한 입력 자료가 된다
- 🔄 다른 접근: [[papers/1700_TACT_Humanoid_Whole-body_Contact_Manipulation_through_Deep_I/review]] — 둘 다 접촉 중심 상호작용을 다루지만 TACT는 촉각 모방 학습에, PICO는 시각적 접촉 복원에 초점을 맞춘다
- 🔄 다른 접근: [[papers/1252_ActiveUMI_Robotic_Manipulation_with_Active_Perception_from_R/review]] — 두 논문 모두 3D 공간에서 물체-환경 상호작용을 추론하지만 ActiveUMI는 조작에, PICO는 인간-물체 접촉에 초점을 맞춘다
- 🔗 후속 연구: [[papers/1837_Climber_Force_and_Motion_Estimation_from_Video/review]] — PICO의 물체와 접촉하는 3D 인간 복원 기술이 등반자와 암벽 간의 상호작용을 더 정확하게 모델링하는 데 활용될 수 있다.
- 🏛 기반 연구: [[papers/1857_CRISP_Contact-Guided_Real2Sim_from_Monocular_Video_with_Plan/review]] — 인간-객체 접촉 재구성이 실제-시뮬레이션 변환의 기초가 됩니다.
- 🏛 기반 연구: [[papers/1907_EmbodMocap_In-the-Wild_4D_Human-Scene_Reconstruction_for_Emb/review]] — PICO의 3D 인간-객체 접촉 재구성 기술이 EmbodMocap의 메트릭 스케일 재구성의 이론적 기반입니다.
- 🔗 후속 연구: [[papers/1910_Embracing_Evolution_A_Call_for_Body-Control_Co-Design_in_Emb/review]] — 신체 구조와 제어의 co-design이 물리 기반 모션 모방의 확장된 형태로 구현될 수 있다.
- 🔗 후속 연구: [[papers/2120_OmniRetarget_Interaction-Preserving_Data_Generation_for_Huma/review]] — PICO의 3D people-object contact reconstruction이 OmniRetarget의 interaction 보존 retargeting을 실제 3D 접촉 데이터로 확장한 형태입니다.
