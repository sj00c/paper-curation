---
title: "1327_CEED-VLA_Consistency_Vision-Language-Action_Model_with_Early"
authors:
  - "Wenxuan Song"
  - "Jiayi Chen"
  - "Pengxiang Ding"
  - "Yuxin Huang"
  - "Han Zhao"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-Language-Action (VLA) 모델의 추론 속도를 향상시키기 위해 consistency distillation과 early-exit decoding을 결합한 CEED-VLA를 제안하며, 4배 이상의 가속화를 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "sub/Vision-Language-Action_Distillation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Song et al._2025_CEED-VLA Consistency Vision-Language-Action Model with Early-Exit Decoding.pdf"
---

# CEED-VLA: Consistency Vision-Language-Action Model with Early-Exit Decoding

> **저자**: Wenxuan Song, Jiayi Chen, Pengxiang Ding, Yuxin Huang, Han Zhao, Donglin Wang, Haoang Li | **날짜**: 2025-06-16 | **URL**: [https://arxiv.org/abs/2506.13725](https://arxiv.org/abs/2506.13725)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Acceleration effect of CEED-VLA on OpenVLA and LLaVA-VLA. Left: Comparison*

Vision-Language-Action (VLA) 모델의 추론 속도를 향상시키기 위해 consistency distillation과 early-exit decoding을 결합한 CEED-VLA를 제안하며, 4배 이상의 가속화를 달성한다.

## Motivation

- **Known**: Jacobi decoding은 autoregressive decoding을 병렬화하여 이론적으로 더 빠른 추론을 가능하게 하지만, 표준 VLA에서는 실제로 1.28배 정도의 제한된 가속화만 제공한다.
- **Gap**: VLA가 AR 학습으로 인해 잘못된 prefix에 대한 robust한 예측 능력이 부족하여 Jacobi decoding에서 각 반복마다 한 토큰만 정확하게 예측하며, 비효율적인 반복이 병목이 된다.
- **Why**: 고주파수 및 정밀한 조작 작업을 요구하는 로봇 배포에서 실시간 추론 속도는 실질적인 성능 제약이므로 효율적인 가속화 기법이 중요하다.
- **Approach**: consistency distillation을 통해 학생 모델이 각 반복에서 여러 토큰을 예측하도록 학습하고, mixed-label supervision으로 오류 누적을 완화하며, early-exit decoding으로 비효율적인 반복을 제거한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Acceleration effect of CEED-VLA on OpenVLA and LLaVA-VLA. Left: Comparison*

- **4배 이상 추론 가속화**: OpenVLA에서 3.6배, LLaVA-VLA에서 2.0배 이상의 speedup을 달성하면서 조작 성능 유지
- **높은 작업 성공률**: 시뮬레이션 및 실제 로봇 작업에서 comparable 또는 improved success rates 달성
- **실시간 배포 가능**: 실제 로봇 팔 배포에서 4배 주파수 향상과 고주파 정밀 작업에서 성능 개선
- **범용적 가속 패러다임**: 서로 다른 VLA baseline에 적용 가능한 일반적인 방법론 제시

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of our proposed CEED-VLA. Our proposed framework first runs the pretrained*

- **Consistency distillation**: teacher 모델의 Jacobi trajectory 상의 임의 지점을 fixed point로 직접 매핑하도록 학생 모델 학습
- **Auxiliary AR loss**: 학생 모델의 native autoregressive 능력 보존을 위해 teacher의 next-token 분포와의 alignment 유지
- **Mixed-label supervision**: teacher 모델의 action accuracy가 학습된 threshold를 초과하면 teacher 출력을, 아니면 ground-truth를 supervision signal로 사용
- **Early-exit decoding**: Jacobi decoding의 엄격한 convergence 조건을 완화하여 비효율적 반복 제거 및 평균 추론 속도 개선

## Originality

- 처음으로 consistency training 기법을 VLA의 빠른 추론에 적용하여 intermediate Jacobi trajectory 상태를 fixed point로 매핑
- mixed-label supervision을 통한 적응적 오류 누적 완화 메커니즘 설계로 distillation 과정에서의 supervision 신뢰도 향상
- early-exit decoding으로 Jacobi decoding의 strict convergence 조건을 완화하면서도 성능 유지 가능함을 이론적·경험적으로 입증

## Limitation & Further Study

- mixed-label supervision의 threshold 학습 메커니즘에 대한 상세한 분석 및 민감도 분석 부족
- early-exit decoding 시 convergence 완화의 정확한 조건과 task 특성에 따른 최적 exit point 선택 기준이 명확하지 않음
- 다양한 로봇 환경과 작업 유형에 대한 광범위한 일반화 검증 필요
- 후속 연구: early-exit 조건의 자동 학습, 다양한 VLA 아키텍처에 대한 확장성 검증, 더 복잡한 sequential decision-making 작업으로의 적용

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: CEED-VLA는 consistency distillation과 early-exit decoding을 결합하여 VLA 추론을 획기적으로 가속화하며, 실제 로봇 배포에서 4배 이상의 속도 개선을 달성하면서도 조작 성능을 유지하는 실용적이고 일반화 가능한 해결책을 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1502_One-Step_Diffusion_Policy_Fast_Visuomotor_Policies_via_Diffu/review]] — 단일 스텝 diffusion 기반 VLA 가속화에 대한 다른 접근 방식을 제시합니다.
- 🧪 응용 사례: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — 실시간 속도로 VLA 실행하는 구체적인 적용 방법을 보여줍니다.
- 🔄 다른 접근: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — 둘 다 VLA 모델 추론 가속화를 다루지만 CEED-VLA는 consistency distillation과 early-exit에, BitVLA는 1-bit quantization에 중점을 둡니다.
- 🏛 기반 연구: [[papers/1568_Search-TTA_A_Multimodal_Test-Time_Adaptation_Framework_for_V/review]] — CEED-VLA의 consistency vision-language-action 모델이 Search-TTA의 멀티모달 테스트타임 적응을 위한 기반 VLM 아키텍처를 제공한다.
- 🔄 다른 접근: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — 둘 다 VLA 모델의 효율성 향상을 다루지만 BitVLA는 1-bit quantization에, CEED-VLA는 consistency distillation에 중점을 둡니다.
- 🔄 다른 접근: [[papers/1373_DualVLA_Building_a_Generalizable_Embodied_Agent_via_Partial/review]] — CEED-VLA의 early exit mechanism과 DualVLA의 partial decoupling은 VLA 모델의 효율성과 성능을 다른 방식으로 최적화하는 접근법이다.
