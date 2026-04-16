---
title: "1624_VQ-VLA_Improving_Vision-Language-Action_Models_via_Scaling_V"
authors:
  - "Yating Wang"
  - "Haoyi Zhu"
  - "Mingyu Liu"
  - "Jiange Yang"
  - "Hao-Shu Fang"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "100배 이상의 대규모 action trajectory 데이터셋을 활용하여 vector quantization 기반 action tokenizer를 학습하고, 이를 Vision-Language-Action 모델에 통합하여 추론 속도, 동작 부드러움, 장기 계획 능력을 향상시킨다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Broad_Task_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2025_VQ-VLA Improving Vision-Language-Action Models via Scaling Vector-Quantized Action Tokenizers.pdf"
---

# VQ-VLA: Improving Vision-Language-Action Models via Scaling Vector-Quantized Action Tokenizers

> **저자**: Yating Wang, Haoyi Zhu, Mingyu Liu, Jiange Yang, Hao-Shu Fang, Tong He | **날짜**: 2025-07-01 | **URL**: [https://arxiv.org/abs/2507.01016](https://arxiv.org/abs/2507.01016)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. The VQ-VLA pipeline, consisting of two main stages: (1) training a general convolutional residual VQ-VAE and (*

100배 이상의 대규모 action trajectory 데이터셋을 활용하여 vector quantization 기반 action tokenizer를 학습하고, 이를 Vision-Language-Action 모델에 통합하여 추론 속도, 동작 부드러움, 장기 계획 능력을 향상시킨다.

## Motivation

- **Known**: 최근 VLA 모델들은 discrete tokenization을 통해 robot action을 언어 모델과 호환 가능하도록 표현하고 있으며, VQ-VAE 기반 action tokenization이 유망한 가능성을 보여주고 있다.
- **Gap**: 기존 action tokenizer는 단일 task 데이터셋 기반으로 학습되어 일반화 능력이 제한적이며, synthetic과 real action trajectory 간 domain gap을 충분히 활용하지 못하고 있다.
- **Why**: 효율적인 action tokenization은 VLA 모델의 성능과 추론 속도를 동시에 향상시킬 수 있으며, 전체 모델 스케일링보다 비용 효율적이고 real-time embodied intelligence 시스템 구현에 필수적이다.
- **Approach**: convolutional residual VQ-VAE 기반의 일반화된 action tokenizer를 OpenX-Embodiment, LIBERO, ManiSkill 데이터셋에서 progressive training strategy로 학습하고, 이를 OpenVLA 모델의 action discretization 방식을 대체하여 적용한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3. Real-world experimental results: We compare the performance of Baseline, VQO, VQO+L, and VQO+L+M on both short*

- **확장 가능성**: 합성 데이터 량 증가에 따라 VQ-VAE tokenizer의 downstream task 성능이 선형적으로 향상됨을 입증
- **실제 성능 개선**: 실제 로봇 플랫폼에서 장기 계획 작업에 대해 최대 30% 높은 성공률 달성
- **효율성 증대**: VQ-VAE tokenizer 사용으로 VLA 모델의 추론 속도 가속화 및 동작 출력의 부드러움과 일관성 향상
- **Domain gap 최소화**: Synthetic과 real action trajectory 간 domain gap이 미미함을 발견, 대규모 합성 데이터 활용의 정당성 확보

## How

![Figure 1](figures/fig1.webp)

*Figure 1. The VQ-VLA pipeline, consisting of two main stages: (1) training a general convolutional residual VQ-VAE and (*

- 2D temporal convolutional layer 기반 encoder-decoder 구조로 구성된 residual VQ-VAE 설계
- Real-world 데이터(OpenX-Embodiment)에서 시작하여 점진적으로 synthetic 데이터(LIBERO, ManiSkill)를 통합하는 progressive training strategy 적용
- 100배 이상의 action trajectory 데이터를 활용하여 다양한 downstream task를 커버하는 일반화된 tokenizer 학습
- Reconstruction loss, VQ loss, commitment loss의 가중 조합으로 최적화
- 학습된 tokenizer를 frozen 상태로 유지하며 OpenVLA에 LoRA 기반 fine-tuning 적용

## Originality

- 기존 VQ-VAE 기반 action tokenization 연구를 100배 규모의 대규모 데이터셋으로 확장하는 novel scaling 접근법 제시
- Progressive training strategy를 통해 real-world 데이터의 노이즈를 점진적으로 synthetic 데이터의 smoothness로 대체하는 창의적 학습 전략
- Action domain에서 synthetic-real 간 minimal gap이 존재함을 실증적으로 증명하고 이를 체계적으로 활용
- MLP 대신 temporal convolutional layer를 사용하여 spatial-temporal 의존성을 더 효율적으로 포착하는 개선된 아키텍처

## Limitation & Further Study

- 실험이 주로 Franka Research 3 로봇과 LIBERO/ManiSkill 환경으로 제한되어 다양한 로봇 플랫폼 및 실제 환경에서의 일반화 검증 필요
- OpenVLA 7B 모델에만 적용되었으며, 다른 VLA 모델 아키텍처에 대한 호환성 및 성능 평가 부재
- Tokenizer의 reconstruction quality와 downstream task performance 간의 명확한 관계식 도출이 부족하고, optimal tokenization granularity에 대한 분석 미흡
- 합성 데이터의 domain gap이 작다는 결론이 특정 도메인(manipulation task)에 제한될 수 있으며, 다양한 task 영역으로의 확장 가능성 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 action tokenization을 대규모 데이터셋으로 확장하는 실용적이고 효과적인 방법론을 제시하며, synthetic-real 데이터 간 minimal domain gap이라는 중요한 발견을 통해 scalable embodied intelligence 시스템 구현의 길을 열었다. 실험 결과와 이론적 근거가 충분하고 VLA 모델의 성능과 효율성을 동시에 향상시키는 점에서 높은 실용성과 학술적 가치를 지닌다.

## Related Papers

- 🏛 기반 연구: [[papers/1392_FAST_Efficient_Action_Tokenization_for_Vision-Language-Actio/review]] — Action tokenization의 기본 개념을 제공하여 VQ-VLA의 vector quantization 기반 action tokenizer 설계에 핵심적인 이론적 토대를 마련한다.
- 🔄 다른 접근: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — 둘 다 action을 token으로 표현하지만, VQ-VLA는 vector quantization을, UniVLA는 discrete token 통합을 사용한다.
- 🏛 기반 연구: [[papers/1348_Data_Scaling_Laws_in_Imitation_Learning_for_Robotic_Manipula/review]] — 대규모 데이터에서의 학습 효과에 대한 이론적 근거를 제공하여 VQ-VLA의 100배 규모 데이터셋 활용 방법론을 뒷받침한다.
- 🔗 후속 연구: [[papers/1392_FAST_Efficient_Action_Tokenization_for_Vision-Language-Actio/review]] — VLA 모델의 action tokenization을 vector quantization 방법으로 확장한 연구입니다.
- 🏛 기반 연구: [[papers/1429_HybridVLA_Collaborative_Diffusion_and_Autoregression_in_a_Un/review]] — VQ-VLA의 다중 생성 패러다임 개념을 diffusion과 autoregressive의 collaborative training으로 구현했다.
- 🏛 기반 연구: [[papers/1366_Discrete_Diffusion_VLA_Bringing_Discrete_Diffusion_to_Action/review]] — vector quantization이 discrete diffusion VLA의 action token 표현에 핵심적인 기반 기술
