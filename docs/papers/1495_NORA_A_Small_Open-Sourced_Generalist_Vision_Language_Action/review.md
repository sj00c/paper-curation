---
title: "1495_NORA_A_Small_Open-Sourced_Generalist_Vision_Language_Action"
authors:
  - "Chia-Yu Hung"
  - "Qi Sun"
  - "Pengfei Hong"
  - "Amir Zadeh"
  - "Chuan Li"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "NORA는 3B 파라미터의 경량 Vision-Language-Action 모델로, 기존 7B 이상의 대규모 VLA 모델보다 계산 효율을 크게 개선하면서도 실시간 로봇 제어 성능을 유지한다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Deep_Reinforcement_Learning_Applications"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Hung et al._2025_NORA A Small Open-Sourced Generalist Vision Language Action Model for Embodied Tasks.pdf"
---

# NORA: A Small Open-Sourced Generalist Vision Language Action Model for Embodied Tasks

> **저자**: Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U-Xuan Tan, Navonil Majumder, Soujanya Poria | **날짜**: 2025-04-28 | **URL**: [https://arxiv.org/abs/2504.19854](https://arxiv.org/abs/2504.19854)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: The overall architecture and inference flow of NORA.*

NORA는 3B 파라미터의 경량 Vision-Language-Action 모델로, 기존 7B 이상의 대규모 VLA 모델보다 계산 효율을 크게 개선하면서도 실시간 로봇 제어 성능을 유지한다.

## Motivation

- **Known**: 기존 VLA 모델들은 뛰어난 추론 및 작업 계획 능력을 보여주지만 높은 계산 오버헤드로 인해 실시간 로봇 환경에서의 실용성이 제한된다. Vision-Language Model을 backbone으로 사용하는 것이 효과적임이 알려져 있다.
- **Gap**: 기존의 대규모 VLA 모델들은 7B 이상의 파라미터로 인해 소비자급 GPU에서 미세조정이 어렵고, 시각 인코딩의 한계로 인한 그래스핑 실패 문제가 존재한다.
- **Why**: 로봇 시스템의 실제 배포에서는 속도와 효율성이 중요하며, 소비자급 GPU에서 미세조정 가능한 경량 모델의 필요성이 크다.
- **Approach**: Qwen-2.5-VL-3B를 backbone으로 하는 3B 파라미터 모델을 제안하고, FAST+ tokenizer를 통해 효율적인 action sequence 생성을 구현하며, 970k의 실제 로봇 시연 데이터로 학습한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Experimental results on different categories of real-world robot tasks.*

- **모델 크기 감소**: 7B 이상의 기존 모델 대비 3B 파라미터로 60% 이상 축소
- **성능 유지/향상**: 계산 오버헤드 감소에도 불구하고 기존 대규모 VLA 모델 대비 우수한 작업 성능 달성
- **메모리 효율성**: 추론 시 약 8.3GB GPU 메모리로 실시간 로봇 제어 가능
- **오픈 소스 공개**: 모델 체크포인트, 학습 전략, 평가 프로토콜 전체 공개로 재현성과 후속 연구 촉진

## How

![Figure 2](figures/fig2.webp)

*Figure 2: (a) Training Loss Curve; (b) Gradient Norm Curve.*

- Qwen-2.5-VL-3B를 backbone으로 채택하여 우수한 시각-의미 이해 활용
- FAST+ tokenizer를 통해 DCT(Discrete Cosine Transform)와 BPE(Byte-Pair Encoding)로 action token 압축
- Open X-Embodiment 데이터셋의 970k 실제 로봇 시연으로 학습
- Single-step과 chunked action prediction의 비교 분석을 통한 효율적 action 생성 전략 수립
- 실제 로봇 환경과 LIBERO 시뮬레이션 벤치마크에서 광범위한 실험 수행

## Originality

- 경량 VLA 모델 설계에 최신 Qwen-2.5-VL-3B VLM을 처음 적용
- FAST+ tokenizer의 DCT 기반 action 압축을 VLA에 적용하여 token 효율성 개선
- 단순한 아키텍처로 SpatialVLA의 복잡한 공간 임베딩 없이도 우수한 성능 달성
- 3B 파라미터로 대규모 모델 대비 우수 성능을 달성하여 새로운 효율성-성능 트레이드오프 제시

## Limitation & Further Study

- LIBERO 시뮬레이션 벤치마크와 실제 로봇 환경에서의 성능이 완전히 동등하지 않을 수 있으며, 더 다양한 로봇 형태(이족 로봇, 휴머노이드 등)에 대한 평가 필요
- 시각 인코딩 한계 문제가 완전히 해결되었는지 명확하지 않으며, 복잡한 폐색(occlusion) 상황에서의 성능 평가 부족
- 계산 효율성과 성능의 최적 균형점에 대한 더 깊은 분석 필요
- 후속 연구로 더 소형 모델(1-2B)로의 확장 가능성 탐색 및 다양한 VLM backbone의 비교 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: NORA는 경량 VLA 모델의 실용적 필요성을 잘 해결한 의미 있는 기여로, 3B 파라미터로 대규모 모델 대비 우수한 성능을 달성하면서 실시간 로봇 제어를 가능하게 한다. 오픈 소스 공개로 후속 연구를 촉진할 것으로 예상된다.

## Related Papers

- 🔄 다른 접근: [[papers/1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M/review]] — TinyVLA와 함께 경량화된 VLA 모델을 추구하지만 NORA는 3B 파라미터로 실시간 성능에, TinyVLA는 데이터 효율성에 집중한다.
- 🔗 후속 연구: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — BitVLA의 1-bit 양자화 기법을 더 실용적인 3B 파라미터 모델로 확장하여 실시간 로봇 제어의 실용성을 높였다.
- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — 둘 다 일반화된 VLA 모델이지만, NORA는 소형 효율성을, OpenVLA는 오픈소스 범용성에 초점을 둔다.
- 🔗 후속 연구: [[papers/1296_A_Pragmatic_VLA_Foundation_Model/review]] — NORA의 소규모 오픈소스 VLA 모델 개념을 실제 20,000시간 데이터로 학습한 더 실용적인 기초 모델로 발전시킨 연구입니다.
