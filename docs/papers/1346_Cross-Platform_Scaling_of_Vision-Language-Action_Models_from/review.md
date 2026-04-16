---
title: "1346_Cross-Platform_Scaling_of_Vision-Language-Action_Models_from"
authors:
  - "Amir Taherin"
  - "Juyi Lin"
  - "Arash Akbari"
  - "Arman Akbari"
  - "Pu Zhao"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "Vision-Language-Action (VLA) 모델의 성능을 엣지 디바이스부터 데이터센터 GPU까지 다양한 하드웨어 플랫폼에서 체계적으로 평가하여, 아키텍처와 하드웨어 제약 조건에 따른 정확도, 레이턴시, 처리량, 메모리 사용량의 확장 추이를 밝혀낸다."
tags:
  - "cat/Embodied_AI_Architectures"
  - "sub/Vision-Language-Action_Architectures"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Taherin et al._2025_Cross-Platform Scaling of Vision-Language-Action Models from Edge to Cloud GPUs.pdf"
---

# Cross-Platform Scaling of Vision-Language-Action Models from Edge to Cloud GPUs

> **저자**: Amir Taherin, Juyi Lin, Arash Akbari, Arman Akbari, Pu Zhao, Weiwei Chen, David Kaeli, Yanzhi Wang | **날짜**: 2025-09-15 | **URL**: [https://arxiv.org/abs/2509.11480](https://arxiv.org/abs/2509.11480)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Peak VRAM usage for each evaluated VLA model*

Vision-Language-Action (VLA) 모델의 성능을 엣지 디바이스부터 데이터센터 GPU까지 다양한 하드웨어 플랫폼에서 체계적으로 평가하여, 아키텍처와 하드웨어 제약 조건에 따른 정확도, 레이턴시, 처리량, 메모리 사용량의 확장 추이를 밝혀낸다.

## Motivation

- **Known**: VLA 모델은 로봇 제어를 위한 강력한 일반화 정책으로 등장했으며, OpenVLA, SpatialVLA, VOTE 등 여러 기준선 모델이 개발되었다. 기존 연구는 주로 단일 하드웨어 플랫폼에서 고정된 자원 설정 하에서만 평가되었다.
- **Gap**: VLA 모델의 성능이 다양한 모델 아키텍처, 하드웨어 클래스, 전력 예산에 따라 어떻게 확장되는지에 대한 체계적인 이해가 부족하다. 엣지-클라우드 스펙트럼 전체에 걸친 정확도, 레이턴시, 처리량, 메모리 사용량의 트레이드오프가 명확하지 않다.
- **Why**: 실제 로봇 시스템은 다양한 하드웨어 자원, 레이턴시 요구 사항, 에너지 예산을 가지고 있으므로, 배포 시나리오에 맞는 최적의 모델 선택과 최적화를 위해 확장 추이를 이해하는 것이 필수적이다.
- **Approach**: LIBERO 벤치마크를 사용하여 5개의 대표적인 VLA 모델(OpenVLA, SpatialVLA, OpenVLA-OFT, QwenVLA, VOTE 포함 2개의 새로운 아키텍처)을 Jetson AGX Orin 엣지 디바이스(다양한 전력 모드)와 H100, A100, A6000, V100 데이터센터 GPU에서 평가한다. 정확도와 함께 레이턴시, 처리량, 피크 메모리 사용량 등 시스템 레벨 메트릭을 측정한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Peak VRAM usage for each evaluated VLA model*

- **아키텍처 영향**: Action tokenization과 모델 backbone 크기 같은 아키텍처 선택이 처리량과 메모리 풋프린트에 강하게 영향을 미침을 확인
- **엣지 디바이스의 비선형 성능 저하**: 전력 제약이 있는 엣지 디바이스에서 성능이 비선형적으로 저하되지만, 일부 구성이 구형 데이터센터 GPU와 동등하거나 초과하는 성능을 보임
- **정확도 손실 최소화**: 상당한 정확도 손실 없이 높은 처리량 변형이 달성 가능함을 입증
- **배포 의사결정 지침**: 다양한 배포 제약 조건에 따라 VLA 모델을 선택하고 최적화하기 위한 실행 가능한 통찰력 제공
- **통념 도전**: 로봇 추론에서 데이터센터 하드웨어의 우월성에 대한 현재의 가정에 의문을 제기

## How


- Jetson AGX Orin에서 15W, 30W, 50W, MAX 등 4가지 전력 모드에서 CPU/GPU 코어 수와 클록 주파수의 변화를 측정
- H100, A100, A6000, V100 등 4개의 데이터센터 GPU를 활용하여 다양한 아키텍처 세대와 성능 계층 평가
- OpenVLA, SpatialVLA, OpenVLA-OFT, QwenVLA, VOTE 5개 모델에 대해 LIBERO 벤치마크에서 정확도 평가
- 각 모델과 하드웨어 조합에서 피크 VRAM 사용량, 추론 레이턴시, 처리량을 측정
- 아키텍처 특성(LLM backbone 크기, action head 설계, 출력 tokenization)과 하드웨어 능력 간의 상호작용 분석

## Originality

- VLA 모델에 대한 최초의 포괄적인 크로스 플랫폼 성능 평가 연구로, 엣지부터 클라우드까지 스펙트럼을 체계적으로 분석
- 전력 제약이 있는 엣지 디바이스에서의 비선형 성능 저하 패턴을 처음으로 상세히 문서화
- 구형 데이터센터 GPU와 최신 엣지 디바이스의 성능 비교를 통해 하드웨어 우월성 가정에 실증적으로 도전
- 두 개의 새로운 VLA 아키텍처(QwenVLA, VOTE의 새로운 구성)를 제안하고 평가

## Limitation & Further Study

- 평가가 LIBERO 벤치마크로 제한되어 있어, 다른 로봇 작업 도메인이나 실제 환경에서의 성능 일반화 가능성 불명확
- 엣지 디바이스는 Jetson AGX Orin 하나만 평가되어, 다양한 엣지 플랫폼(다른 모바일 프로세서, IoT 디바이스)에서의 확장성 미지
- 전력 제약 하에서의 성능 저하 원인에 대한 심화 분석(메모리 대역폭, 캐시 미스, 연산 제약) 부족
- 실시간 로봇 제어에서의 지연 시간 누적 효과나 배치 처리와의 상호작용 미분석
- 후속 연구로는 다양한 엣지 플랫폼과 실제 로봇 환경에서의 검증, 전력 제약 하 성능 최적화 기법 개발, VLA 모델 압축(pruning, quantization) 기법의 영향 분석이 필요함

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 VLA 모델의 크로스 플랫폼 성능 확장을 체계적으로 분석한 중요한 벤치마크 연구로, 로봇 배포 시나리오에 맞는 하드웨어 선택과 모델 최적화를 위한 실용적인 통찰력을 제공한다. 엣지 디바이스의 경쟁력을 입증함으로써 로봇 시스템 설계에 대한 새로운 관점을 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1577_SpecPrune-VLA_Accelerating_Vision-Language-Action_Models_via/review]] — VLA 모델 가속화를 위한 다른 최적화 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1616_VLA-Adapter_An_Effective_Paradigm_for_Tiny-Scale_Vision-Lang/review]] — 소규모 VLA를 위한 어댑터 기반 효율적 패러다임으로 확장한다.
- 🏛 기반 연구: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — VLA 모델의 효율적 구현을 위한 1-bit 양자화 기초를 제공한다.
- 🔄 다른 접근: [[papers/1541_RoboMIND_Benchmark_on_Multi-embodiment_Intelligence_Normativ/review]] — RoboMIND와 cross-platform VLA scaling은 모두 다중 로봇 플랫폼을 다루지만 데이터셋과 모델 확장이라는 다른 관점에서 접근한다.
- 🏛 기반 연구: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — Cross-Platform Scaling 연구는 CrossFormer의 다중 embodiment 학습이 가능한 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1633_X-VLA_Soft-Prompted_Transformer_as_Scalable_Cross-Embodiment/review]] — cross-platform scaling을 soft-prompted transformer로 효율적으로 구현한 확장 연구입니다.
