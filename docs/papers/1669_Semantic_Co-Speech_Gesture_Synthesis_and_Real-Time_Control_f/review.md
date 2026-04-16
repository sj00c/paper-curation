---
title: "1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f"
authors:
  - "Gang Zhang"
date: "2025.12"
doi: "10.48550/arXiv.2512.17183"
arxiv: ""
score: 4.0
essence: "이 연구는 음성 입력으로부터 의미론적으로 적절한 제스처를 생성하고 실시간으로 휴머노이드 로봇에 배포하는 end-to-end 프레임워크를 제시한다. LLM과 Motion-GPT를 활용한 제스처 생성과 imitation learning 기반의 MotionTracker 제어 정책을 통합하여 의미 있는 비언어적 소통을 실현한다."
tags:
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/LLM_Physical_Motion_Planning"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang_2025_Semantic Co-Speech Gesture Synthesis and Real-Time Control for Humanoid Robots.pdf"
---

# Semantic Co-Speech Gesture Synthesis and Real-Time Control for Humanoid Robots

> **저자**: Gang Zhang | **날짜**: 2025-12-19 | **DOI**: [10.48550/arXiv.2512.17183](https://doi.org/10.48550/arXiv.2512.17183)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: System Overview: Training and Inference Pipeline.*

이 연구는 음성 입력으로부터 의미론적으로 적절한 제스처를 생성하고 실시간으로 휴머노이드 로봇에 배포하는 end-to-end 프레임워크를 제시한다. LLM과 Motion-GPT를 활용한 제스처 생성과 imitation learning 기반의 MotionTracker 제어 정책을 통합하여 의미 있는 비언어적 소통을 실현한다.

## Motivation

- **Known**: 음성 동기화 제스처 생성은 주로 beat gesture에 집중해왔으며, 의미 있는 제스처는 데이터 희소성으로 인해 생성이 어렵다. 휴머노이드 로봇 제어는 embodiment gap과 물리적 제약으로 인해 복잡한 인간 동작 추적이 어렵다.
- **Gap**: 기존 시스템들은 의미론적 제스처 생성 또는 로봇 제어 중 하나에 집중하며, 실시간 배포 가능한 완전한 end-to-end 파이프라인이 부족하다. 특히 인간 동작 데이터를 실제 로봇에 적응시키는 robust 방법론이 필요하다.
- **Why**: 자연스럽고 표현력 있는 로봇 소통은 human-robot interaction의 핵심이며, 의미론적으로 정확하고 실시간으로 배포 가능한 제스처 생성은 로봇의 실제 활용성을 크게 높인다.
- **Approach**: General Motion Retargeting (GMR)으로 human motion을 로봇에 맞추고, Residual VQ-VAE와 Motion-GPT를 통해 의미론적 제스처를 생성한 후, imitation learning 기반의 MotionTracker로 실시간 추적 제어를 수행한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Comparison of Original vs. Reconstructed G1 Mo-*

- **완전한 end-to-end 파이프라인**: 음성 입력부터 실제 로봇 배포까지 의미론적 co-speech gesture 생성을 자동화하고 실시간 동기화 실행
- **GMR 기반 motion retargeting**: 인간 skeleton에서 로봇 morphology로 고충실도 동작 변환을 통해 embodiment gap 해결
- **hierarchical RVQ-VAE 구조**: 신체와 손을 분리하여 모델링하고 residual quantization으로 복잡한 제스처 표현 능력 향상
- **MotionTracker 제어 정책**: imitation learning 기반으로 diverse하고 dynamic한 제스처를 정확하게 추적하면서 균형 유지
- **의미론적 정확성 입증**: LLM 기반 retrieval mechanism과 Motion-GPT의 조합으로 의미론적으로 적절하고 리듬감 있는 제스처 생성 확인

## How

![Figure 1](figures/fig1.webp)

*Figure 1: System Overview: Training and Inference Pipeline.*

- Motion Retargeting: key body matching, non-uniform local scaling, 두 단계의 differential IK optimization으로 BVH motion을 Unitree G1의 29 DoF에 맞춤
- Motion Codebook Training: Residual VQ-VAE로 motion sequence를 hierarchical discrete latent space로 인코딩하여 motion token 생성
- Gesture Generation: GPT-2 기반 Motion-GPT 모델을 이전 motion token과 synchronized audio feature에 조건으로 설계하여 미래 gesture token을 autoregressive하게 예측
- Control Training: 목표 로봇용 retargeted motion을 reference trajectory로 사용하여 reinforcement learning 기반의 π_motion 정책 학습
- Real-Time Inference: Text-to-Speech로 생성된 음성을 Audio-Encoder로 처리 → Motion-GPT로 gesture token 생성 → decoding으로 Ref-Motion 변환 → π_motion이 실시간 action 생성

## Originality

- 음성 기반 의미론적 제스처 생성과 로봇 실시간 배포를 통합하는 첫 번째 완전한 파이프라인 제시
- LLM의 semantic understanding과 Motion-GPT의 생성 능력을 결합한 novel gesture synthesis approach
- Residual VQ-VAE의 hierarchical 구조로 body와 hand를 독립적으로 모델링하여 표현 능력 극대화
- General Motion Retargeting 방법론을 통해 embodiment gap을 체계적으로 해결하며 high-fidelity reference motion 생성
- Imitation learning 기반 MotionTracker로 diverse gesture 추적과 balance maintenance를 동시에 달성

## Limitation & Further Study

- 음성 입력의 semantic ambiguity에 대한 robustness 평가 부족 — LLM retrieval이 항상 적절한 gesture candidate를 찾지 못할 수 있음
- 실제 환경의 동적 변화(external disturbance, terrain variation)에 대한 online adaptation 능력이 제한적 — Any2Track의 AnyAdapter 같은 advanced dynamics adaptation 미통합
- 평가가 제한적 — 의미론적 정확성의 정량적 지표 부재, 사용자 연구를 통한 자연스러움 평가 미실시
- Unitree G1 특화 설계로 다른 로봇 플랫폼으로의 일반화 가능성 미검증
- Motion 데이터셋의 규모와 semantic gesture 샘플 비율 불명시 — sparse semantic gesture 문제의 완전한 해결 여부 불명확

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 음성 기반 의미론적 제스처 생성과 실시간 로봇 배포를 통합한 의미 있는 연구로, LLM, Motion-GPT, imitation learning을 창의적으로 결합하여 완전한 end-to-end 파이프라인을 실현했다. 다만 평가의 정량성 강화와 다양한 환경에서의 robustness 검증이 필요하다.

## Related Papers

- 🔗 후속 연구: [[papers/1672_SignBot_Learning_Human-to-Humanoid_Sign_Language_Interaction/review]] — SignBot의 수화 상호작용이 음성-제스처 생성을 시각적 언어로 확장한 포괄적 소통 시스템
- 🏛 기반 연구: [[papers/1634_Realistic_Lip_Motion_Generation_Based_on_3D_Dynamic_Viseme_a/review]] — 입술 운동 생성의 3D 동적 모델링이 음성 기반 제스처 생성의 다중 모달 표현 기반
- 🔄 다른 접근: [[papers/1972_Hierarchical_Intention-Aware_Expressive_Motion_Generation_fo/review]] — 계층적 의도 인식 표현 생성과 LLM 기반 의미론적 제스처는 휴머노이드 표현의 서로 다른 접근법
- 🔄 다른 접근: [[papers/1670_SENTINEL_A_Fully_End-to-End_Language-Action_Model_for_Humano/review]] — LLM을 활용한 언어-행동 모델링에서 제스처 생성과 전신 제어라는 서로 다른 응용 영역을 다룬다.
- 🏛 기반 연구: [[papers/1708_TextOp_Real-time_Interactive_Text-Driven_Humanoid_Robot_Moti/review]] — 실시간 언어-모션 변환이라는 공통 과제를 다루며, TextOp의 상호작용적 접근법이 Semantic Co-Speech의 실시간 제어에 기여할 수 있다.
- 🏛 기반 연구: [[papers/1968_Harmon_Whole-Body_Motion_Generation_of_Humanoid_Robots_from/review]] — Harmon의 전신 모션 생성 기술이 제스처와 조화된 휴머노이드 전체 움직임 생성에 필요한 기반이다
- 🏛 기반 연구: [[papers/1672_SignBot_Learning_Human-to-Humanoid_Sign_Language_Interaction/review]] — 음성-제스처 생성의 다중 모달 프레임워크가 SignBot의 수화 인식/생성을 위한 기본 상호작용 구조
- 🔗 후속 연구: [[papers/1646_RoboMirror_Understand_Before_You_Imitate_for_Video_to_Humano/review]] — Visual motion intent를 semantic gesture synthesis로 확장한 응용 연구
- 🔄 다른 접근: [[papers/1624_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_A/review]] — PRIMAL의 generative motion model과 제스처 생성의 LLM+Motion-GPT는 서로 다른 인간형 실시간 애니메이션 접근법
- 🏛 기반 연구: [[papers/1634_Realistic_Lip_Motion_Generation_Based_on_3D_Dynamic_Viseme_a/review]] — 음성-제스처 생성 시스템이 입술 운동의 3D 동적 비셈 모델링을 포함한 종합적인 인간-로봇 상호작용 기반
- 🏛 기반 연구: [[papers/1882_Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Aud/review]] — semantic co-speech gesture synthesis가 audio-controlled humanoid locomotion의 음성-동작 매핑에 대한 기본 원리를 제공한다.
- 🔄 다른 접근: [[papers/1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R/review]] — LLM 기반 표현적 모션 생성과 의미적 공동 발화 제스처 합성은 모두 자연스러운 인간형 표현을 목표로 한다.
- 🔄 다른 접근: [[papers/1972_Hierarchical_Intention-Aware_Expressive_Motion_Generation_fo/review]] — 계층적 의도 인식 표현 생성과 의미적 공동 발화 제스처는 모두 사회적 상호작용을 위한 표현적 모션을 다룬다.
