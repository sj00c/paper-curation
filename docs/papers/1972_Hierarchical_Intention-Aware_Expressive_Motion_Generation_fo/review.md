---
title: "1972_Hierarchical_Intention-Aware_Expressive_Motion_Generation_fo"
authors:
  - "Lingfan Bao"
  - "Yan Pan"
  - "Tianhu Peng"
  - "Dimitrios Kanoulas"
  - "Chengxu Zhou"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 Vision Language Model의 의도 추론과 diffusion 기반 동작 생성을 결합한 계층적 프레임워크 HIAER을 제안하여, 인간의 사회적 의도와 감정 맥락을 파악하고 실시간으로 표현적인 로봇 동작을 생성한다."
tags:
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Adaptive_Locomotion_and_Control"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/LLM_Physical_Motion_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bao et al._2025_Hierarchical Intention-Aware Expressive Motion Generation for Humanoid Robots.pdf"
---

# Hierarchical Intention-Aware Expressive Motion Generation for Humanoid Robots

> **저자**: Lingfan Bao, Yan Pan, Tianhu Peng, Dimitrios Kanoulas, Chengxu Zhou | **날짜**: 2025-06-02 | **URL**: [https://arxiv.org/abs/2506.01563](https://arxiv.org/abs/2506.01563)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Overall framework of the proposed work. (a) The high-level system architecture. Multimodal inputs XI = (Vin, Lin*

본 논문은 Vision Language Model의 의도 추론과 diffusion 기반 동작 생성을 결합한 계층적 프레임워크 HIAER을 제안하여, 인간의 사회적 의도와 감정 맥락을 파악하고 실시간으로 표현적인 로봇 동작을 생성한다.

## Motivation

- **Known**: 최근 VLM은 고수준의 인간 의도 해석에 뛰어나며, diffusion model은 대규모 데이터셋 학습을 통해 다양한 표현적 동작 생성이 가능하다.
- **Gap**: 기존 접근법들은 기능적 목표 분해에 집중하여 명시적 과제 해석에만 머물며, 동적 사회 맥락의 암묵적 감정적 의도와 신체적 표현적 반응 사이의 폐쇄 루프를 형성하지 못한다.
- **Why**: 인간-로봇 상호작용에서 신뢰 구축, 협업 촉진, 사용자 참여 향상을 위해 사회적 맥락에 적응하는 표현적 동작이 필수적이다.
- **Approach**: VLM 기반의 의도 인식 모듈이 in-context learning과 Chain-of-Thought 프롬프팅으로 사회적 의도와 Valence-Arousal 감정 맥락을 추론하고, 이를 기반으로 DART text-to-motion diffusion model이 사회 적응적 제스처를 실시간으로 생성하며, RL 기반 whole-body controller가 물리 로봇에서 실행한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: Qualitative results across the six representative interaction scenarios. Each subfigure from (a) to (f) displays*

- **계층적 의도-감정 추론 프레임워크**: VLM이 사회적 의도뿐 아니라 Valence-Arousal 추정을 통해 감정 맥락을 파악하여 동작 선택을 조절하는 통합 구조를 제시
- **신뢰도 기반 적응형 응답**: 의도 추론에 신뢰도 점수를 도입하고 fallback 행동과 사회 맥락 인식을 통해 의도 정제 및 적응적 대응 가능
- **실시간 폐쇄 루프 상호작용**: 고수준 의도 해석에서 저수준 신체 제어까지 완전한 폐쇄 루프를 형성하여 기능적일 뿐 아니라 물리적, 사회적으로 표현적인 응답 생성
- **물리 로봇 실증**: 실제 인간로봇상호작용 시나리오에서 시스템을 구현하고 검증하여 저지연 맥락 적응적 제스처의 실현 가능성 증명

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Overall framework of the proposed work. (a) The high-level system architecture. Multimodal inputs XI = (Vin, Lin*

- 의도 인식 모듈 πi: 사전 프롬프트, few-shot 예시, 상호작용 이력 H_I/O를 활용한 VLM 에이전트로 multimodal 입력 (V_in, L_in)을 처리하여 구조화된 출력 [d, i, c, (V, A), <m>] 생성
- Valence-Arousal 모델: 5개 사분면(고arousal-음valence, 고arousal-양valence, 저arousal-양valence, 저arousal-음valence, neutral)으로 인간 감정 상태를 매개변수화
- 동작 생성: DART text-to-motion diffusion model이 VLM의 고수준 명령과 V-A 추정으로 조건화되어 시간적으로 일관성 있는 인간 동작 궤적 ŷ_t:t+n 합성
- 동작 재타겟팅: 인간 동작 궤적을 로봇의 특정 운동학으로 변환하여 원하는 궤적 y_t:t+n 생성
- 저수준 제어: RL 기반 whole-body controller πw가 로봇의 물리적 제약과 균형을 유지하면서 재타겟팅된 궤적 실행
- in-context learning과 CoT 프롬프팅: VLM이 구조화된 추론 과정을 통해 명시적이고 세밀한 의도 및 감정 맥락 분석

## Originality

- 사회적 의도 추론과 감정 맥락 파악(V-A)을 단일 VLM 추론 프로세스에 통합한 계층적 아키텍처의 창신성
- 기존의 template 기반이나 제한된 demonstration 중심 방식을 벗어나 대규모 인간 동작 데이터셋 기반의 diffusion model과 VLM 기반 고수준 추론을 결합한 점
- 신뢰도 점수, fallback 행동, 사회 맥락 인식 등 현실적 상호작용을 위한 실용적 메커니즘의 추가
- 완전한 폐쇄 루프(의도 추론→동작 생성→물리 실행)를 물리 humanoid 로봇에서 실증한 점

## Limitation & Further Study

- **계산 지연**: VLM 추론과 diffusion 기반 동작 생성이 실시간 요구사항을 만족하는지 정확한 지연 분석 부재
- **V-A 모델의 정확성**: Valence-Arousal 추정의 신뢰성과 검증 방법, 문화적 차이나 개인차에 대한 강건성 미흡
- **제한된 상호작용 시나리오**: 실험이 특정 representative 시나리오에 국한되어 다양한 사회 맥락에서의 일반화 가능성 미확인
- **동작 다양성과 물리 가능성**: diffusion model 기반 생성 동작의 물리적 가능성(관절 한계, 충돌 회피 등)에 대한 체계적 평가 부족
- **후속 연구 방향**: 경량화된 VLM이나 edge device 배포, 사용자 피드백을 통한 실시간 학습, 더 광범위한 감정-의도 매핑 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 VLM의 고수준 사회적 추론과 diffusion 기반 동작 생성을 의도적으로 결합하여 인간-로봇 상호작용의 폐쇄 루프를 완성한 점에서 높은 가치를 지니며, 물리 로봇 실증을 통해 실현 가능성을 보여준다.

## Related Papers

- 🔄 다른 접근: [[papers/1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f/review]] — 계층적 의도 인식 표현 생성과 의미적 공동 발화 제스처는 모두 사회적 상호작용을 위한 표현적 모션을 다룬다.
- 🔗 후속 연구: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — 실시간 텍스트 기반 제어가 계층적 의도 인식 모션 생성의 실시간 적용이다.
- 🏛 기반 연구: [[papers/1992_Humanoid_Agent_via_Embodied_Chain-of-Action_Reasoning_with_M/review]] — 체화된 행동 추론이 계층적 의도 인식의 기반 메커니즘이다.
- 🔄 다른 접근: [[papers/1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R/review]] — EMOTION의 expressive motion generation이 HIAER과 다른 방식으로 감정적 휴머노이드 동작을 생성합니다.
- 🏛 기반 연구: [[papers/1847_Commanding_Humanoid_by_Free-form_Language_A_Large_Language_A/review]] — Free-form language commanding이 HIAER의 의도 추론 및 표현적 동작 생성의 기반이 됩니다.
- 🔗 후속 연구: [[papers/1882_Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Aud/review]] — Do You Have Freestyle의 표현적 보행이 HIAER의 감정 맥락 기반 동작 생성을 확장합니다.
- 🔗 후속 연구: [[papers/1918_ExBody2_Advanced_Expressive_Humanoid_Whole-Body_Control/review]] — ExBody2의 표현적 휴머노이드 제어를 사회적 의도와 감정 맥락까지 확장한 HIAER의 발전된 형태다.
- 🏛 기반 연구: [[papers/1670_SENTINEL_A_Fully_End-to-End_Language-Action_Model_for_Humano/review]] — SENTINEL의 언어-행동 모델이 HIAER의 Vision Language Model 기반 의도 추론의 핵심 토대가 된다.
- 🔄 다른 접근: [[papers/1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f/review]] — 계층적 의도 인식 표현 생성과 LLM 기반 의미론적 제스처는 휴머노이드 표현의 서로 다른 접근법
- 🔄 다른 접근: [[papers/1672_SignBot_Learning_Human-to-Humanoid_Sign_Language_Interaction/review]] — 계층적 의도 인식 표현과 수화 언어 상호작용은 휴머노이드 소통의 서로 다른 표현 방식
- 🔄 다른 접근: [[papers/1865_Design_and_Control_of_a_Bipedal_Robotic_Character/review]] — 이족 로봇 캐릭터의 연극적 성능과 계층적 의도 인식 표현 동작 생성은 휴머노이드의 감정적 표현에서 서로 다른 제어 아키텍처를 사용한다.
- 🔄 다른 접근: [[papers/1936_From_Motion_to_Behavior_Hierarchical_Modeling_of_Humanoid_Ge/review]] — 둘 다 계층적 의도 기반 모션 생성을 다루지만 PHYLOMAN은 LLM 결합을, Hierarchical Intention-Aware는 expressive motion에 중점을 둔다.
- 🔗 후속 연구: [[papers/1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R/review]] — EMOTION의 표현적 모션 생성을 Hierarchical Intention-Aware 프레임워크와 결합하면 더 복잡한 의도 기반 휴머노이드 행동이 가능하다.
- 🏛 기반 연구: [[papers/1913_EMP_Executable_Motion_Prior_for_Humanoid_Robot_Standing_Uppe/review]] — 의도 인식 표현적 동작 생성 연구가 EMP의 인간 상체 동작 모방을 위한 동작 표현 및 의도 이해 기술적 기반을 제공한다.
