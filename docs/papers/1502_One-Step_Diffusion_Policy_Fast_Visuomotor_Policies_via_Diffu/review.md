---
title: "1502_One-Step_Diffusion_Policy_Fast_Visuomotor_Policies_via_Diffu"
authors:
  - "Zhendong Wang"
  - "Zhaoshuo Li"
  - "Ajay Mandlekar"
  - "Zhenjia Xu"
  - "Jiaojiao Fan"
date: "2024.10"
doi: ""
arxiv: ""
score: 4.0
essence: "One-Step Diffusion Policy (OneDP)는 사전 학습된 diffusion policy의 지식을 단일 단계 action generator로 distill하여 로봇 제어의 추론 속도를 42배 향상시킨다. KL divergence 최소화를 통해 원본 policy 분포와의 정렬을 보장하면서도 2%-10%의 추가 학습 비용만 필요하다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2024_One-Step Diffusion Policy Fast Visuomotor Policies via Diffusion Distillation.pdf"
---

# One-Step Diffusion Policy: Fast Visuomotor Policies via Diffusion Distillation

> **저자**: Zhendong Wang, Zhaoshuo Li, Ajay Mandlekar, Zhenjia Xu, Jiaojiao Fan, Yashraj Narang, Linxi Fan, Yuke Zhu, Yogesh Balaji, Mingyuan Zhou, Ming-Yu Liu, Yu Zeng | **날짜**: 2024-10-28 | **URL**: [https://arxiv.org/abs/2410.21257](https://arxiv.org/abs/2410.21257)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Comparison of Diffusion Policy and One-Step Diffusion Policy (OneDP). We demon-*

One-Step Diffusion Policy (OneDP)는 사전 학습된 diffusion policy의 지식을 단일 단계 action generator로 distill하여 로봇 제어의 추론 속도를 42배 향상시킨다. KL divergence 최소화를 통해 원본 policy 분포와의 정렬을 보장하면서도 2%-10%의 추가 학습 비용만 필요하다.

## Motivation

- **Known**: Diffusion model은 생성 AI에서 뛰어난 성능을 보이며 로봇 제어의 behavior cloning에도 적용되고 있다. 그러나 iterative denoising step으로 인한 느린 추론 속도(1.49 Hz)는 실시간 로봇 애플리케이션에 부적합하다.
- **Gap**: 기존 diffusion policy 가속화 연구는 ODE solver 또는 몇 단계의 sampling에 의존하며, Consistency Policy도 여전히 여러 반복이 필요하다. 진정한 단일 단계 distillation으로 robotic control을 가속화하는 연구는 부족하다.
- **Why**: 동적 환경과 자원 제약 로봇에서는 빠른 응답이 필수적이며, 환경 변화에 신속하게 대응할 수 없으면 task 실패로 이어진다. 단계 inference로 실시간 제어를 가능하게 하는 것이 중요하다.
- **Approach**: 사전 학습된 diffusion policy의 score network와 새로운 one-step generator의 score network 간 KL divergence를 최소화하는 distillation 방법을 제안한다. Generator와 generator score network를 원본 모델로 초기화하여 효율적인 학습을 달성한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Comparison of Diffusion Policy and One-Step Diffusion Policy (OneDP). We demon-*

- **추론 속도 대폭 개선**: 1.49 Hz에서 62.5 Hz로 42배 향상 (real-world 로봇 실험)
- **최고 수준의 성능**: Robomimic 벤치마크 6개 과제에서 state-of-the-art 성공률 달성
- **효율적 학습**: Distillation 수렴에 필요한 추가 학습 비용이 원본 학습의 2%-10%에 불과
- **빠른 task 완료**: 실제 task 완료 시간 36.36초에서 25.81초로 단축
- **동적 환경 대응**: 환경 변화(object perturbation)에 대한 신속한 반응으로 높은 성공률 유지

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Diffusion Distillation Pipeline. a) Our one-step action generator processes image-based*

- One-step implicit action generator Gθ 설계: 노이즈 z와 observation O를 입력받아 single-step action 생성
- Generator score network πψ 도입: Generator가 생성한 actions의 score 추정
- KL divergence 최소화: 사전 학습된 diffusion policy의 score network πϕ와 generator score network πψ의 차이를 손실 함수로 정의
- Score difference loss 활용: KL divergence의 gradient를 score difference로 표현하여 효율적 학습
- 초기화 전략: Generator와 generator score network를 원본 diffusion model로 초기화하여 빠른 수렴 달성
- Forward diffusion chain 활용: Generated actions에 diffusion process를 적용하여 다양한 noise level에서 policy 정렬

## Originality

- Robotic control을 위한 최초의 진정한 one-step diffusion distillation 방법 제시 (Consistency Policy는 여전히 여러 단계 필요)
- SDS/VSD의 성공을 robot policy 영역으로 처음 적용한 policy-matching distillation 방법론
- Action distribution의 KL divergence를 diffusion chain 전체에 걸쳐 최소화하는 novel loss formulation
- Initialization 전략으로 2%-10% 추가 학습만으로 수렴 가능하게 한 효율적 설계

## Limitation & Further Study

- 평가가 6개 simulation task와 4개 real-world task로 제한적이며, 더 다양한 task 범위의 검증 필요
- Diffusion chain 전체에 대한 KL divergence 계산으로 인한 메모리 오버헤드 미분석
- Generator score network의 수렴성과 안정성에 대한 이론적 분석 부재
- One-step generator의 generalization 능력 및 새로운 환경에 대한 transfer learning 성능 미평가
- Offline RL 설정에서의 성능을 다루지 않으며, online learning 시나리오에서의 적용 가능성 미탐색

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: One-Step Diffusion Policy는 diffusion 기반 로봇 제어의 추론 속도 문제를 우아하게 해결하는 혁신적 접근법이다. 실험 결과가 강력하고 방법론이 명확하며 실제 로봇 애플리케이션의 가능성을 크게 확대한 중요한 연구다.

## Related Papers

- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — Diffusion Policy의 핵심 개념을 OneDP가 단일 단계로 압축하여 효율성을 극대화한다.
- 🔄 다른 접근: [[papers/1339_Consistency_Policy_Accelerated_Visuomotor_Policies_via_Consi/review]] — 두 논문 모두 diffusion 기반 정책의 추론 속도 개선을 목표로 하지만 distillation과 consistency model로 접근법이 다르다.
- 🔗 후속 연구: [[papers/1560_SARA-RT_Scaling_up_Robotics_Transformers_with_Self-Adaptive/review]] — SARA-RT의 모델 효율화 연구를 OneDP가 추론 시간 최적화 관점에서 보완한다.
- 🔄 다른 접근: [[papers/1525_Real-Time_Execution_of_Action_Chunking_Flow_Policies/review]] — OneDP의 single-step distillation과 달리 real-time chunking을 통해 inference 지연 문제를 해결하는 다른 접근법이다.
- 🏛 기반 연구: [[papers/1580_Streaming_Flow_Policy_Simplifying_diffusionflow-matching_pol/review]] — OneDP가 개선하고자 하는 기존 diffusion/flow-matching policy의 streaming 방법론과 성능 한계를 제시한다.
- 🔄 다른 접근: [[papers/1395_FlowPolicy_Enabling_Fast_and_Robust_3D_Flow-based_Policy_via/review]] — 둘 다 빠른 정책 추론을 목표로 하지만 Consistency Flow Matching vs One-Step Diffusion이라는 다른 가속화 기법을 사용한다.
- 🔄 다른 접근: [[papers/1465_ManiFlow_A_General_Robot_Manipulation_Policy_via_Consistency/review]] — 고품질 visuomotor policy 생성에서 consistency training vs diffusion의 다른 접근
- 🏛 기반 연구: [[papers/1525_Real-Time_Execution_of_Action_Chunking_Flow_Policies/review]] — one-step diffusion policy의 기본 이론을 제공하여 RTC의 비동기적 action chunk 생성과 실행에 필요한 빠른 inference 기법의 토대를 제공한다.
- 🔗 후속 연구: [[papers/1533_RLRC_Reinforcement_Learning-based_Recovery_for_Compressed_Vi/review]] — OneDP의 추론 속도 개선과 RLRC의 모델 압축이 상호 보완적인 효율화 방법이다.
- 🔄 다른 접근: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — One-Step Diffusion Policy는 VLA 실시간 실행과 유사한 목표로 diffusion 정책의 추론 속도를 획기적으로 개선한다.
- 🏛 기반 연구: [[papers/1560_SARA-RT_Scaling_up_Robotics_Transformers_with_Self-Adaptive/review]] — 모델 효율화의 맥락에서 SARA-RT와 OneDP가 상호 보완적인 최적화 방법이다.
- 🔄 다른 접근: [[papers/1613_VITA_Vision-to-Action_Flow_Matching_Policy/review]] — One-Step Diffusion Policy는 VITA와 유사하게 추론 속도와 효율성을 획기적으로 개선하지만 diffusion 기반 접근법을 사용한다.
- 🔗 후속 연구: [[papers/1617_VLA-Cache_Efficient_Vision-Language-Action_Manipulation_via/review]] — one-step diffusion을 KV 캐싱과 결합하여 더 빠른 visuomotor policy를 구현할 수 있습니다.
- 🔄 다른 접근: [[papers/1327_CEED-VLA_Consistency_Vision-Language-Action_Model_with_Early/review]] — 단일 스텝 diffusion 기반 VLA 가속화에 대한 다른 접근 방식을 제시합니다.
- 🔄 다른 접근: [[papers/1339_Consistency_Policy_Accelerated_Visuomotor_Policies_via_Consi/review]] — Diffusion policy의 속도 개선을 위한 또 다른 one-step 접근방식을 제시합니다.
- 🔄 다른 접근: [[papers/1366_Discrete_Diffusion_VLA_Bringing_Discrete_Diffusion_to_Action/review]] — One-Step Diffusion Policy의 빠른 추론과 Discrete Diffusion VLA의 adaptive action decoding은 diffusion 기반 정책에서 효율성을 다르게 접근한다.
- 🔄 다른 접근: [[papers/1374_DynamicVLA_A_Vision-Language-Action_Model_for_Dynamic_Object/review]] — dynamic object manipulation을 위한 continuous inference 대신 one-step diffusion을 통한 빠른 정책 실행
