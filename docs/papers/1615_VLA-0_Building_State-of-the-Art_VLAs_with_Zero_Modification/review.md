---
title: "1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification"
authors:
  - "Ankit Goyal"
  - "Hugo Hadfield"
  - "Xuning Yang"
  - "Valts Blukis"
  - "Fabio Ramos"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "VLA-0는 Vision-Language Model의 구조 변경 없이 액션을 직접 텍스트로 표현하여 로봇 조작을 위한 최첨단 Vision-Language-Action 모델을 구축한다. 이 단순한 설계가 기존의 복잡한 방법들보다 우수한 성능을 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Visual_Language_Navigation"
  - "cat/Embodied_AI_Architectures"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Goyal et al._2025_VLA-0 Building State-of-the-Art VLAs with Zero Modification.pdf"
---

# VLA-0: Building State-of-the-Art VLAs with Zero Modification

> **저자**: Ankit Goyal, Hugo Hadfield, Xuning Yang, Valts Blukis, Fabio Ramos | **날짜**: 2025-10-15 | **URL**: [https://arxiv.org/abs/2510.13054](https://arxiv.org/abs/2510.13054)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Schematic representation of VLA-0. VLA-0 con-*

VLA-0는 Vision-Language Model의 구조 변경 없이 액션을 직접 텍스트로 표현하여 로봇 조작을 위한 최첨단 Vision-Language-Action 모델을 구축한다. 이 단순한 설계가 기존의 복잡한 방법들보다 우수한 성능을 달성한다.

## Motivation

- **Known**: 기존 VLA 방법들은 크게 세 가지로 분류되며, 대부분 VLM의 vocabulary 수정, action head 추가, 또는 맞춤형 아키텍처를 통해 액션을 예측한다. 이들은 각각 액션 해상도 제약, 언어 이해 저하, 복잡성 증가 등의 문제를 가진다.
- **Gap**: 액션을 직접 텍스트로 표현하는 가장 단순한 전략이 거의 탐구되지 않았다. 현존하는 LLARVA와 HAMSTER는 다단계 접근을 사용하여 최적의 설계를 찾지 못했다.
- **Why**: 단순한 설계는 구현이 용이하고 VLM의 사전학습된 능력을 보존하면서도 임의의 액션 해상도를 지원할 수 있어, 실제 로봇 시스템 배포에 중요하다.
- **Approach**: VLA-0는 액션(좌표, 관절각 등)을 space-separated integers의 텍스트로 표현하고, VLM의 네이티브 텍스트 생성 능력을 활용하여 액션을 예측한다. 최첨단 성능을 위해 학습 시 random masking과 테스트 시 prediction ensembling을 적용한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2: Families of methods for building VLAs. We categorize existing VLAs into three categories: Discrete Token VLAs,*

- **LIBERO 벤치마크 우수성**: 동일한 로봇 데이터로 학습한 모든 기존 방법(π0.5-KI, OpenVLA-OFT, SmolVLA)을 능가
- **대규모 사전학습 데이터 없이 경쟁성**: 대규모 로봇 데이터로 학습한 π0.5-KI, π0, GR00T-N1, MolmoAct를 초월
- **실세계 성능**: SmolVLA를 능가하며 실제 로봇 작업에서 우수한 성능 입증
- **구조 수정 없음**: VLM의 vocabulary, 아키텍처, 토크나이저에 어떠한 변경도 필요 없음

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Our proposed VLA-0. It creates a VLA without making any changes to the underlying VLM. It takes a system*

- VLM을 프롬프트하여 action을 텍스트로 직접 생성하도록 유도 (예: '4 12 98 3 0 0 13 5 ...')", '시스템 프롬프트, 언어 지시사항, 이미지를 입력으로 받아 space-separated integers 형태의 액션 출력
- 학습 시 action text에 random masking을 적용하여 모델의 견고성 향상
- 테스트 시 이전 예측값들을 ensemble하여 최종 액션 결정의 안정성 증대
- VLM의 cross-entropy loss를 그대로 사용하여 추가 신경망 불필요

## Originality

- 액션 예측에 있어 텍스트 기반 표현의 충분성을 처음으로 체계적으로 입증
- 기존 연구(LLARVA, HAMSTER)의 다단계 접근과 달리 end-to-end 직접 생성을 성공적으로 구현
- action token masking과 prediction ensembling이라는 critical한 학습/추론 기법 제시
- 단순성 대비 성능의 역설을 실제 벤치마크와 실세계 작업으로 입증

## Limitation & Further Study

- action text의 생성 품질이 VLM의 수치 예측 능력에 크게 의존하며, 이에 대한 심층 분석 부족
- random masking과 ensemble 기법이 필수적이나, 이들의 개별 기여도에 대한 ablation study 상세 분석 필요
- 실세계 평가가 4가지 작업만 포함되어 있어 더 광범위한 작업에 대한 일반화 검증 요구
- LIBERO의 시뮬레이션 환경이 실제 로봇의 복잡성을 완전히 반영하지 못할 가능성
- 후속연구로 액션 텍스트 생성의 해석성 향상, 더 효율적인 ensemble 기법 개발, 다양한 VLM 백본에 대한 성능 비교 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VLA-0는 예상을 뒤엎고 가장 단순한 설계가 최첨단 성능을 달성 가능함을 입증하여 VLA 분야에 중요한 통찰을 제공한다. 코드와 모델 공개를 통한 재현성과 실용성이 높으며, VLM 기반 로봇 제어 연구에 새로운 방향을 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — 둘 다 VLA 모델 구축의 핵심 요소를 분석하지만 VLA-0은 구조 변경 없는 단순함을, 후자는 체계적 설계 분석을 강조한다.
- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 오픈소스 vision-language-action 모델이 구조 변경 없이 액션을 텍스트로 표현하는 VLA-0의 설계 기반이다.
- 🔗 후속 연구: [[papers/1392_FAST_Efficient_Action_Tokenization_for_Vision-Language-Actio/review]] — 액션 토큰화 연구를 구조 변경 없이 액션을 직접 텍스트로 표현하는 더 단순한 방법으로 발전시켰다.
- 🏛 기반 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — RT-1의 실제 제어를 위한 Robotics Transformer가 VLA-0의 간단한 텍스트 기반 액션 표현의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — InternVLA의 understanding, generation, action 통합 방법론이 VLA-0의 단순한 텍스트 기반 action 표현의 이론적 토대를 제공한다.
- 🧪 응용 사례: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — BitVLA의 1-bit quantization 기술이 VLA-0의 단순한 구조와 결합되어 실제 로봇에서 더 효율적으로 실행될 수 있다.
- 🔄 다른 접근: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — 둘 다 VLA 통합을 추구하지만, VLA-0는 구조 변경 없는 단순함을, UniVLA는 discrete token 통합을 추구한다.
- 🏛 기반 연구: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — VLM 기반 로봇 정책의 기본 접근법을 제공하여 VLA-0의 zero modification 방법론의 이론적 근거를 마련한다.
- 🔄 다른 접근: [[papers/1616_VLA-Adapter_An_Effective_Paradigm_for_Tiny-Scale_Vision-Lang/review]] — 둘 다 효율적인 VLA 모델을 목표로 하지만, VLA-0는 구조 단순화를, VLA-Adapter는 경량 백본과 adapter를 사용한다.
- 🧪 응용 사례: [[papers/1518_Prismatic_VLMs_Investigating_the_Design_Space_of_Visually-Co/review]] — VLM 설계 최적화를 실제 VLA 구현에 적용한 zero-modification 접근법
- 🔗 후속 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 기본 구조를 zero modification으로 최적화한 VLA-0의 발전
- 🔄 다른 접근: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — 둘 다 VLA 통합을 추구하지만, UniVLA는 discrete token 통합을, VLA-0는 구조 변경 없는 텍스트 표현을 사용한다.
- 🔄 다른 접근: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — 둘 다 효과적인 VLA 모델 구축을 다루지만 이 논문은 체계적 분석을, VLA-0은 단순한 설계를 제안한다.
- 🔗 후속 연구: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — RoboFlamingo의 VLM 활용 접근을 zero modification으로 단순화하여 더 실용적이고 효율적인 방법론을 제시한다.
- 🏛 기반 연구: [[papers/1611_Visual_Instruction_Tuning/review]] — 다중모달 instruction following의 기본 개념을 제공하여 VLA-0의 텍스트 기반 액션 표현 방법론의 이론적 근거를 마련한다.
- 🔄 다른 접근: [[papers/1616_VLA-Adapter_An_Effective_Paradigm_for_Tiny-Scale_Vision-Lang/review]] — 둘 다 효율적인 VLA 구현을 목표로 하지만, VLA-Adapter는 adapter 기반을, VLA-0는 zero modification을 추구한다.
