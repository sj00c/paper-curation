---
title: "2148_TokenHSI_Unified_Synthesis_of_Physical_Human-Scene_Interacti"
authors:
  - "Liang Pan"
  - "Zeshi Yang"
  - "Zhiyang Dou"
  - "Wenjia Wang"
  - "Buzhen Huang"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "TokenHSI는 transformer 기반의 통합 정책으로 humanoid 고유감각을 공유 토큰으로 모델링하고 task 토큰과 masking mechanism으로 결합하여 다양한 인간-장면 상호작용(HSI) 기술을 단일 네트워크에서 통합한다."
tags:
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Motion_Learning_from_Demonstration"
  - "sub/Adaptive_Locomotion_Recovery"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Pan et al._2025_TokenHSI Unified Synthesis of Physical Human-Scene Interactions through Task Tokenization.pdf"
---

# TokenHSI: Unified Synthesis of Physical Human-Scene Interactions through Task Tokenization

> **저자**: Liang Pan, Zeshi Yang, Zhiyang Dou, Wenjia Wang, Buzhen Huang, Bo Dai, Taku Komura, Jingbo Wang | **날짜**: 2025-03-25 | **URL**: [https://arxiv.org/abs/2503.19901](https://arxiv.org/abs/2503.19901)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Introducing TokenHSI, a unified model that enables physics-based characters to perform diverse human-scene int*

TokenHSI는 transformer 기반의 통합 정책으로 humanoid 고유감각을 공유 토큰으로 모델링하고 task 토큰과 masking mechanism으로 결합하여 다양한 인간-장면 상호작용(HSI) 기술을 단일 네트워크에서 통합한다.

## Motivation

- **Known**: 기존 연구들은 특정 상호작용 작업마다 별도의 컨트롤러를 개발했으며, 일부 통합 컨트롤러도 정적 장면 상호작용과 제한된 일반화 능력에만 집중했다.
- **Gap**: 현재 방법들은 복합 작업(예: 물건을 들고 앉기)을 처리하거나 새로운 시나리오로의 유연한 적응이 부족하며, 여러 기술의 통합과 효율적인 정책 적응을 동시에 달성하지 못한다.
- **Why**: 현실에서 인간은 다양한 상호작용을 수행하고 새로운 환경에 적응하는 범용 에이전트이므로, 컴퓨터 애니메이션과 embodied AI 분야에서 이러한 다재다능성과 적응성을 구현하는 것이 중요하다.
- **Approach**: proprioception tokenizer를 통해 캐릭터 상태를 공유 토큰으로 모델링하고, 다양한 task tokenizer들과 transformer의 masking mechanism으로 결합하여 다중 기술을 학습한 후, 변수 길이 입력을 지원하는 아키텍처로 새로운 작업에 효율적으로 적응한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Introducing TokenHSI, a unified model that enables physics-based characters to perform diverse human-scene int*

- **다중 기술 통합**: following, sitting, climbing, carrying 등 4가지 대표적 HSI 기술을 단일 transformer 네트워크에서 동시 학습
- **효율적 정책 적응**: 기초 기술 학습 후 task tokenizer와 adapter layer만 추가하여 새로운 작업에 빠르게 적응 가능
- **포괄적 일반화**: 기술 합성, 물체/지형 형태 변화, 장기 작업 완성 등 다양한 HSI 벤치마크에서 기존 방법 대비 성능 향상

## How

![Figure 2](figures/fig2.webp)

*Figure 2. TokenHSI consists of two stages: (left) foundational skill learning and (right) policy adaptation. Through mul*

- **Proprioception tokenizer**: 캐릭터 상태를 독립적인 공유 토큰으로 인코딩하여 모든 작업에서 재사용
- **Task tokenizer**: 각 작업의 관찰값을 표준화된 길이로 변환
- **Masking mechanism**: transformer encoder에서 proprioception 토큰과 task 토큰을 선택적으로 결합
- **Variable length input 지원**: 새로운 task tokenizer를 추가하여 정책 재훈련 없이 적응
- **Multi-task training**: 공유 proprioception tokenizer가 다양한 캐릭터 상태에 일반화되도록 함
- **Adapter layer**: MLP 기반 action head에 부분 미세조정 가능하게 함

## Originality

- **독립적 proprioception tokenizer**: 기존의 joint character-goal 상태 공간과 달리 proprioception을 분리하여 더 효과적인 지식 공유 실현
- **Masking mechanism의 다차원 활용**: task 토큰 결합뿐만 아니라 정책 적응과 기술 합성까지 확장
- **효율적 적응 전략**: 전체 정책 미세조정 대신 새로운 tokenizer와 adapter layer만 학습하는 parameter-efficient 접근

## Limitation & Further Study

- **동시성 제한**: 현재 4가지 기본 기술만 다루며, 더 많은 기술의 통합 시 scalability 미검증
- **물리 시뮬레이션 의존성**: physics engine에 의존하므로 실제 로봇 배포 시 sim-to-real gap 해결 필요
- **복합 작업의 제한**: 기술 합성이 기존 기술의 조합에만 한정되며, 완전히 새로운 합성 기술 학습 능력 미검증
- **후속연구**: (1) 더 많은 HSI 기술의 통합 시 성능 유지 방안 (2) 실제 로봇 환경에서의 검증 (3) 사용자 의도 입력 메커니즘 강화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: TokenHSI는 독립적 proprioception tokenizer와 masking mechanism을 통해 다중 HSI 기술을 단일 네트워크에서 효과적으로 통합하고, 변수 길이 입력을 활용한 효율적 정책 적응까지 실현한 혁신적인 접근법으로, 컴퓨터 애니메이션과 embodied AI 분야에서 실질적인 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1676_SimGenHOI_Physically_Realistic_Whole-Body_Humanoid-Object_In/review]] — 물리적으로 현실적인 전신 인간-객체 상호작용 생성의 기본 기술이 TokenHSI의 통합 정책 설계에 적용된다.
- 🔄 다른 접근: [[papers/2170_Unified_Human-Scene_Interaction_via_Prompted_Chain-of-Contac/review]] — transformer 기반 통합 정책 대신 LLM을 활용한 Chain of Contacts 방식으로 인간-장면 상호작용을 처리한다.
- 🧪 응용 사례: [[papers/1613_PhysHSI_Towards_a_Real-World_Generalizable_and_Natural_Human/review]] — 통합된 HSI 기술이 실제 세계에서 일반화 가능하고 자연스러운 인간-휴머노이드 상호작용 구현에 적용된다.
- 🏛 기반 연구: [[papers/1968_Harmon_Whole-Body_Motion_Generation_of_Humanoid_Robots_from/review]] — Harmon의 language-conditioned motion generation이 TokenHSI의 transformer 기반 통합 정책에서 다양한 HSI 작업의 토큰 기반 모델링의 기술적 토대를 제공합니다.
- 🔗 후속 연구: [[papers/1947_Generalizable_Humanoid_Manipulation_with_3D_Diffusion_Polici/review]] — Generalizable humanoid manipulation with 3D diffusion이 TokenHSI의 unified HSI policy를 3D diffusion을 통한 일반화 가능한 manipulation으로 확장한 형태입니다.
- 🔗 후속 연구: [[papers/1676_SimGenHOI_Physically_Realistic_Whole-Body_Humanoid-Object_In/review]] — 인간-장면-객체 상호작용을 다루며, 물리적 현실성과 토큰화된 표현이라는 보완적 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1616_PICO_Reconstructing_3D_People_In_Contact_with_Objects/review]] — PICO의 3D 접촉 정보 복원 기술이 TokenHSI의 물리적 human-scene interaction 합성에서 더 정확한 접촉 모델링을 제공할 수 있다
- 🔄 다른 접근: [[papers/1751_Visual_Imitation_Enables_Contextual_Humanoid_Control/review]] — 물리적 인간-장면 상호작용을 위해 서로 다른 접근(단순 영상 기반 모방 vs 통합된 토큰 기반 합성)을 통해 자연스러운 휴머노이드 행동을 생성한다.
- 🔗 후속 연구: [[papers/1857_CRISP_Contact-Guided_Real2Sim_from_Monocular_Video_with_Plan/review]] — 토큰화된 인간-장면 상호작용 합성으로 발전됩니다.
- 🔗 후속 연구: [[papers/1895_Efficient_and_Scalable_Monocular_Human-Object_Interaction_Mo/review]] — 4DHOISolver의 시공간적 일관성 재구성이 TokenHSI의 unified human-scene interaction synthesis로 발전하여 더 포괄적인 상호작용 모델링을 제공한다.
- 🔄 다른 접근: [[papers/2015_HUMOTO_A_4D_Dataset_of_Mocap_Human_Object_Interactions/review]] — HUMOTO의 모션캡처 기반 접근법과 TokenHSI의 unified synthesis는 human-scene interaction을 위한 서로 다른 데이터 수집과 합성 방법론입니다.
- 🔄 다른 접근: [[papers/2030_It_Takes_Two_Learning_Interactive_Whole-Body_Control_Between/review]] — 둘 다 다중 에이전트 상호작용이지만 Harmanoid는 로봇-로봇, TokenHSI는 인간-장면 상호작용 중심
- 🔄 다른 접근: [[papers/2170_Unified_Human-Scene_Interaction_via_Prompted_Chain-of-Contac/review]] — LLM 기반 Chain of Contacts 대신 transformer 기반 통합 정책으로 인간-장면 상호작용을 처리한다.
