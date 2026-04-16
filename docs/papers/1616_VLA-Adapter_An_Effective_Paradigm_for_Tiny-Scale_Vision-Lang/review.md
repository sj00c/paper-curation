---
title: "1616_VLA-Adapter_An_Effective_Paradigm_for_Tiny-Scale_Vision-Lang"
authors:
  - "Yihao Wang"
  - "Pengxiang Ding"
  - "Lingxiao Li"
  - "Can Cui"
  - "Zirui Ge"
date: "2025.09"
doi: ""
arxiv: ""
score: 4.0
essence: "VLA-Adapter는 경량 백본(0.5B 파라미터)을 사용하여 로봇 데이터 사전학습 없이 최첨단 Vision-Language-Action 모델을 학습할 수 있는 새로운 패러다임을 제시한다. Bridge Attention을 통해 비전-언어 표현을 행동 공간에 효과적으로 연결한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Embodied_AI_Architectures"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2025_VLA-Adapter An Effective Paradigm for Tiny-Scale Vision-Language-Action Model.pdf"
---

# VLA-Adapter: An Effective Paradigm for Tiny-Scale Vision-Language-Action Model

> **저자**: Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, Siteng Huang, Yifan Tang, Wenhui Wang, Ru Zhang, Jianyi Liu, Donglin Wang | **날짜**: 2025-09-11 | **URL**: [https://arxiv.org/abs/2509.09372](https://arxiv.org/abs/2509.09372)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Characteristics of VLA-Adapter. “↓” is that smaller*

VLA-Adapter는 경량 백본(0.5B 파라미터)을 사용하여 로봇 데이터 사전학습 없이 최첨단 Vision-Language-Action 모델을 학습할 수 있는 새로운 패러다임을 제시한다. Bridge Attention을 통해 비전-언어 표현을 행동 공간에 효과적으로 연결한다.

## Motivation

- **Known**: 기존 VLA 모델들은 대규모 VLM을 로봇 데이터로 사전학습한 후 Policy 네트워크와 연결하여 행동 생성을 수행하고 있다. 비전-언어-행동 간의 다양한 연결 패러다임(raw features, additional queries 등)이 존재한다.
- **Gap**: 기존 방법들의 상대적 효과성이 명확하지 않으며, 어느 조건(condition)이 행동 생성에 본질적으로 중요한지 체계적으로 분석되지 않았다. 또한 VLA 모델의 높은 계산 비용과 GPU 메모리 소비가 배포 장벽이 되고 있다.
- **Why**: 경량 VLA 모델의 개발은 로봇 공학의 접근성을 크게 향상시킬 수 있으며, VL에서 A로의 효과적인 연결 메커니즘 규명은 VLA 설계의 핵심이다.
- **Approach**: 먼저 다양한 VL 조건이 행동 생성에 미치는 영향을 체계적으로 분석하고, Bridge Attention을 갖춘 경량 Policy 모듈을 제안하여 최적 조건을 자동으로 주입한다. 이를 통해 사전학습 없이도 고성능을 달성한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Characteristics of VLA-Adapter. “↓” is that smaller*

- **체계적 분석**: VL에서 A로의 다양한 브릿징 패러다임에 대한 첫 번째 체계적 분석 수행
- **경량 모델**: 0.5B 파라미터 백본으로 기존 7B 모델(OpenVLA-OFT) 수준의 성능(LIBERO 97.3%) 달성
- **빠른 학습**: 단일 소비자급 GPU에서 8시간 내 강력한 VLA 모델 학습 가능 (학습 VRAM 24.7GB, 1/14배 감소)
- **높은 추론 속도**: 219.2Hz 처리량으로 기존 71.4Hz 대비 3배 향상
- **배포 접근성**: 로봇 데이터 사전학습 없이도 실제 및 시뮬레이션 로봇 벤치마크에서 최첨단 성능 달성

## How

![Figure 3](figures/fig3.webp)

*Figure 3: The proposed VLA framework. The key components are the effective condition explo-*

- Prismatic-VLM 아키텍처 기반 VLM 구축 (DINOv2, SigLIP 시각 특성 추출)
- 다양한 조건 비교 실험: (1) 단일 계층 Raw features, (2) 단일 계층 ActionQuery features, (3) 전체 계층 Raw features, (4) 전체 계층 ActionQuery features
- Bridge Attention 메커니즘 설계로 조건 정보를 행동 공간에 효율적으로 주입
- Policy 네트워크가 최적 조건을 자동으로 선택하도록 학습하는 구조
- 0.5B Qwen2.5 백본으로 기본 설정, 7B LLaMA2 및 OpenVLA-7B와의 비교 실험 수행

## Originality

- VL-A 브릿징 패러다임의 효과를 처음으로 체계적으로 비교 분석
- Bridge Attention이라는 새로운 주의 메커니즘으로 다중 조건을 효율적으로 통합
- 로봇 데이터 사전학습 없이도 높은 성능을 달성하는 새로운 VLA 설계 철학 제시
- ActionQuery를 중심으로 한 새로운 브릿징 인터페이스 탐색

## Limitation & Further Study

- 현재 단일 로봇 환경(manipulation tasks)에서 주로 평가되었으며, 다양한 로봇 플랫폼(navigation, mobile manipulation 등)에 대한 일반화 검증 필요
- 0.5B 백본이 고도로 복잡한 추론을 요구하는 작업에서의 성능 한계 가능성
- Bridge Attention의 계산 복잡도와 메모리 오버헤드에 대한 상세 분석 부재
- 후속 연구: (1) 더 다양한 로봇 작업으로 확장, (2) 모듈식 구조로의 발전, (3) 다중 모드 입력 처리 능력 강화, (4) 도메인 적응 메커니즘 추가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: VLA-Adapter는 경량 백본으로도 최첨단 성능을 달성할 수 있음을 보여주며, VL-A 브릿징의 본질에 대한 체계적 분석을 통해 VLA 설계의 실질적 지침을 제공한다. 빠른 학습 시간과 낮은 계산 비용으로 로봇 공학의 접근성을 크게 높이는 중요한 기여이다.

## Related Papers

- 🔄 다른 접근: [[papers/1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M/review]] — 둘 다 경량 VLA 모델을 제안하지만 VLA-Adapter는 Bridge Attention을, TinyVLA는 diffusion policy decoder를 핵심으로 사용한다.
- 🔗 후속 연구: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — 경량 VLA 모델의 효율성을 1-bit 양자화로 더 극한까지 추진하여 tiny-scale 모델의 발전 방향을 제시한다.
- 🏛 기반 연구: [[papers/1503_OneTwoVLA_A_Unified_Vision-Language-Action_Model_with_Adapti/review]] — OneTwoVLA의 적응형 아키텍처 설계가 VLA-Adapter의 Bridge Attention 기반 연결 방법론의 이론적 기반을 제공한다.
- 🏛 기반 연구: [[papers/1514_Perceiver-Actor_A_Multi-Task_Transformer_for_Robotic_Manipul/review]] — Perceiver-Actor의 multi-task transformer 아키텍처가 VLA-Adapter의 경량 백본 설계에 구조적 영감을 제공했다.
- 🧪 응용 사례: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — 경량 VLA 모델의 실시간 실행 가능성을 실증하여 VLA-Adapter의 효율성 장점을 실제 배포 환경에서 검증합니다.
- 🔄 다른 접근: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — 둘 다 효율적인 VLA 구현을 목표로 하지만, VLA-Adapter는 adapter 기반을, VLA-0는 zero modification을 추구한다.
- 🔄 다른 접근: [[papers/1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M/review]] — 둘 다 경량 백본을 사용한 효율적인 VLA 모델을 제안하지만 TinyVLA는 diffusion decoder를, VLA-Adapter는 Bridge Attention을 사용한다.
- 🔄 다른 접근: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — 둘 다 효율적인 VLA 모델을 목표로 하지만, VLA-0는 구조 단순화를, VLA-Adapter는 경량 백본과 adapter를 사용한다.
- 🔗 후속 연구: [[papers/1346_Cross-Platform_Scaling_of_Vision-Language-Action_Models_from/review]] — 소규모 VLA를 위한 어댑터 기반 효율적 패러다임으로 확장한다.
- 🏛 기반 연구: [[papers/1351_DeeR-VLA_Dynamic_Inference_of_Multimodal_Large_Language_Mode/review]] — VLA-Adapter의 효율적인 파라미터 조정 기법이 DeeR-VLA의 동적 크기 조절 아이디어의 기반을 제공합니다.
