---
title: "1681_SMAP_Self-supervised_Motion_Adaptation_for_Physically_Plausi"
authors:
  - "Haoyu Zhao"
  - "Sixu Lin"
  - "Qingwei Ben"
  - "Minyue Dai"
  - "Hao Fei"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 인간 모션과 휴머노이드 로봇의 이질적 행동 공간 간 차이를 해결하기 위해 Vector-Quantized Periodic Autoencoder 기반의 Humanoid-Adapter를 제안하여 인간 모션을 물리적으로 타당한 로봇 모션으로 적응시키고, Teacher-Student 증류 학습을 통해 안정적인 전신 제어 정책을 학습한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Compliant_Motion_Tracking"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhao et al._2025_SMAP Self-supervised Motion Adaptation for Physically Plausible Humanoid Whole-body Control.pdf"
---

# SMAP: Self-supervised Motion Adaptation for Physically Plausible Humanoid Whole-body Control

> **저자**: Haoyu Zhao, Sixu Lin, Qingwei Ben, Minyue Dai, Hao Fei, Jingbo Wang, Hua Zou, Junting Dong | **날짜**: 2025-05-26 | **URL**: [https://arxiv.org/abs/2505.19463](https://arxiv.org/abs/2505.19463)

---

## Essence

![Figure 3](figures/fig3.webp)

*Figure 3: Pipeline of SMAP*

본 논문은 인간 모션과 휴머노이드 로봇의 이질적 행동 공간 간 차이를 해결하기 위해 Vector-Quantized Periodic Autoencoder 기반의 Humanoid-Adapter를 제안하여 인간 모션을 물리적으로 타당한 로봇 모션으로 적응시키고, Teacher-Student 증류 학습을 통해 안정적인 전신 제어 정책을 학습한다.

## Motivation

- **Known**: 기존 연구들은 대규모 인간 모션 캡처 데이터를 RL을 통해 직접 모방하도록 학습하여 휴머노이드 로봇의 전신 제어를 수행해왔다. 그러나 인간과 로봇의 모션 특성 차이로 인해 학습 효율성과 안정성이 저하된다.
- **Gap**: 기존 방법들은 이질적인 재타겟팅된 인간 모션 공간에서 직접 정책을 학습하여 훈련 수렴이 느리고 동적 환경에서 불안정하다. 인간 모션을 로봇의 물리적으로 타당한 행동 공간으로 효율적으로 변환하는 메커니즘이 부재하다.
- **Why**: 안정적이고 효율적인 전신 제어는 휴머노이드 로봇이 일상의 다양한 작업을 수행하기 위한 필수 요소이며, 인간 데이터의 활용을 통한 학습 효율성 향상은 실제 로봇 배포의 실용성을 크게 높인다.
- **Approach**: Humanoid-Adapter라는 Vector-Quantized Periodic Autoencoder를 사용하여 공유 코드북에 인간 모션을 인코딩하고 로봇 행동 공간으로 디코딩함으로써 원자적 행동 단위를 학습한다. 이어 Privileged Teacher 정책으로부터 Student 정책으로 지식을 증류하며, 상체와 하체를 분리하는 디커플된 보상을 제안한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5: Qualitative results on the H1 robot in simulation.*

- **Humanoid-Adapter 설계**: Vector-Quantized Periodic Autoencoder를 기반으로 인간과 휴머노이드 로봇 모션의 공유 위상 다양체(phase manifold)를 학습하고, 의미론적으로 유사한 행동들을 자동으로 군집화한다.
- **물리적 타당성 확보**: 적응된 모션을 모방 목표로 사용함으로써 학습 수렴 속도를 가속화하고 새로운/도전적 모션 처리 시 안정성을 향상시킨다.
- **교사-학생 증류 학습**: Privileged information(지면 접촉, 목표 상태 등)을 활용한 교사 정책에서 학생 정책으로 정확한 모방 기술을 전달한다.
- **디커플된 보상 함수**: 상체와 하체 동역학을 분리하여 최적화함으로써 전신 추적 정확도와 속도 추적 성능을 동시에 개선한다.
- **실제 로봇 검증**: Unitree H1 로봇의 시뮬레이션 및 실제 환경 실험에서 SOTA 방법 대비 우수한 안정성과 성능을 입증한다.

## How

![Figure 4](figures/fig4.webp)

*Figure 4: Humanoid-Adapter. To align heterogeneous*

- Periodic Autoencoder 아키텍처를 기반으로 위상 정렬(phase alignment)을 수행하여 주기적 모션의 구조를 캡처한다.
- Vector Quantization을 통해 인간과 로봇 모션을 공유 코드북으로 매핑하여 이산적 의미 단위를 학습한다.
- 공유 코드북으로 인코딩된 원자적 행동을 로봇의 행동 공간으로 디코딩하여 물리적으로 타당한 모션을 생성한다.
- 적응된 모션을 목표 상태(goal state) sg_t로 제공하여 Goal-Conditioned RL 프레임워크에서 정책을 학습한다.
- Privileged Teacher 정책은 접촉 정보, 목표 상태 등 추가 정보를 활용하여 학생 정책을 지도한다.
- 상체(팔) 및 하체(다리) 관절 추적에 대한 보상을 분리하여 각각을 최적화하는 디커플된 보상을 설계한다.
- PPO 알고리즘을 사용하여 정책 π를 최적화하고, Sim2Real 기법을 통해 시뮬레이션에서 학습한 정책을 실제 로봇으로 전이한다.

## Originality

- Vector-Quantized Periodic Autoencoder를 휴머노이드 제어 도메인에 처음 적용하여 인간-로봇 이질성 해결을 위한 자동 모션 적응 메커니즘을 제시한다.
- 공유 코드북 기반 모션 적응은 unpaired 데이터로도 학습 가능하게 함으로써 기존 페어링 데이터 기반 방법들과 차별화된다.
- 상체-하체 분리 보상 함수 설계는 전신 로봇의 이질적 동역학 특성을 고려한 새로운 보상 설계 패러다임을 제안한다.
- Privileged Teacher-Student 증류 학습에서 제안된 디커플된 보상이 증류 과정에 통합되어 지식 전달 효율성을 향상시킨다.

## Limitation & Further Study

- Humanoid-Adapter의 사전 학습 데이터셋 크기와 다양성에 따른 성능 변화에 대한 분석이 부재하다.
- 제안 방법은 Unitree H1 로봇에만 검증되었으며, 다른 형태의 휴머노이드 로봇(예: Atlas, Boston Dynamics)으로의 일반화 가능성이 미지수이다.
- 벡터 양자화 코드북 크기 선택 기준과 위상 정렬 성능 간의 관계에 대한 상세 분석이 부족하다.
- 실제 환경에서의 외부 교란(바람, 충돌 등)에 대한 강건성 평가가 제한적이다.
- 후속 연구로는 다양한 로봇 형태와 환경에 대한 일반화, 온라인 적응 학습 메커니즘, 그리고 모션 적응 과정의 해석가능성(interpretability) 향상이 필요하다.

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 인간-로봇 모션 이질성이라는 실질적 문제를 Vector-Quantized Periodic Autoencoder와 디커플된 보상을 통해 체계적으로 해결하며, 시뮬레이션과 실제 로봇 실험을 통해 방법의 효과성을 충분히 입증한다. 다만 특정 로봇 플랫폼에 한정된 검증과 일반화 가능성에 대한 추가 분석이 있으면 더욱 강력한 논문이 될 것으로 예상된다.

## Related Papers

- 🔄 다른 접근: [[papers/1640_ResMimic_From_General_Motion_Tracking_to_Humanoid_Whole-body/review]] — 두 논문 모두 인간 모션을 휴머노이드 로봇으로 적응시키는 문제를 다루지만, 자기지도 학습과 일반적인 추적이라는 다른 방법을 사용한다.
- 🏛 기반 연구: [[papers/2088_Make_Tracking_Easy_Neural_Motion_Retargeting_for_Humanoid_Wh/review]] — 휴머노이드 전신 제어를 위한 신경망 모션 리타게팅의 기초 방법론을 제공한다.
- 🔗 후속 연구: [[papers/2137_PhysDiff_Physics-Guided_Human_Motion_Diffusion_Model/review]] — 물리 기반 인간 모션 diffusion을 자기지도 학습으로 휴머노이드에 적응시키는 방향으로 확장한다.
- 🔄 다른 접근: [[papers/1753_VisualMimic_Visual_Humanoid_Loco-Manipulation_via_Motion_Tra/review]] — 인간 모션을 휴머노이드로 적응시키는 과제에서 자기지도 적응과 시각적 모방이라는 서로 다른 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1615_Physics-Based_Motion_Imitation_with_Adversarial_Differential/review]] — 물리 기반 모션 모방에서 adversarial differential과 self-supervised adaptation이라는 관련된 학습 패러다임을 사용한다.
- 🔄 다른 접근: [[papers/1660_RuN_Residual_Policy_for_Natural_Humanoid_Locomotion/review]] — human motion adaptation vs residual policy라는 서로 다른 방식의 자연스러운 휴머노이드 제어 접근법입니다.
- 🏛 기반 연구: [[papers/2000_Humanoid_Policy__Human_Policy/review]] — 인간 모션의 물리적 타당성 확보가 humanoid-human policy alignment의 기초입니다.
- 🔄 다른 접근: [[papers/1660_RuN_Residual_Policy_for_Natural_Humanoid_Locomotion/review]] — 자연스러운 보행을 위해 residual learning vs motion adaptation이라는 서로 다른 decoupling 방식을 사용합니다.
- 🔄 다른 접근: [[papers/1753_VisualMimic_Visual_Humanoid_Loco-Manipulation_via_Motion_Tra/review]] — 인간 모션을 휴머노이드로 적용하는 과제에서 시각적 모방과 자기지도 적응이라는 서로 다른 접근법을 사용한다.
