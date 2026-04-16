---
title: "1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M"
authors:
  - "Junjie Wen"
  - "Yichen Zhu"
  - "Jinming Li"
  - "Minjie Zhu"
  - "Kun Wu"
date: "2024.09"
doi: ""
arxiv: ""
score: 4.0
essence: "TinyVLA는 경량의 vision-language 모델과 diffusion policy decoder를 결합하여 대규모 로봇 데이터 사전학습 없이도 빠른 추론 속도와 높은 데이터 효율성을 달성하는 로봇 조작용 VLA 모델이다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_AI_Architectures"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wen et al._2024_TinyVLA Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation.pdf"
---

# TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation

> **저자**: Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, Jian Tang | **날짜**: 2024-09-19 | **URL**: [https://arxiv.org/abs/2409.12514](https://arxiv.org/abs/2409.12514)

---

## Essence


TinyVLA는 경량의 vision-language 모델과 diffusion policy decoder를 결합하여 대규모 로봇 데이터 사전학습 없이도 빠른 추론 속도와 높은 데이터 효율성을 달성하는 로봇 조작용 VLA 모델이다.

## Motivation

- **Known**: RT-2, OpenVLA와 같은 기존 VLA 모델들은 멀티태스크 학습과 일반화 성능이 우수하지만, 70억 개 이상의 매개변수로 인한 느린 추론 속도와 970K 샘플의 OpenX 데이터셋을 필요로 하는 대규모 사전학습이 필요하다는 문제가 있다.
- **Gap**: 기존 VLA 모델들은 빠른 추론 속도와 데이터 효율성을 동시에 달성하지 못했으며, 경량 모델로도 우수한 성능을 낼 수 있는 아키텍처 설계가 부족했다.
- **Why**: 로봇 제어에서 추론 속도는 사용자 경험과 로봇의 즉각적 반응성에 직접적 영향을 미치며, 대규모 로봇 데이터 수집의 어려움과 계산 비용을 고려할 때 데이터 효율성이 실제 배포에 필수적이다.
- **Approach**: 1.4억~14억 개 매개변수의 경량 VLM을 Pythia 언어 모델과 LLaVA 훈련 파이프라인으로 구축하고, LoRA를 이용한 매개변수 효율적 미세조정(5% 매개변수만 학습 가능)과 diffusion policy decoder를 통해 직접 로봇 액션을 출력한다.

## Achievement


- **추론 속도 향상**: TinyVLA-H가 OpenVLA 대비 20배 더 빠른 추론 지연시간 달성
- **성능 개선**: 실제 로봇 환경에서 OpenVLA 대비 25.7% 높은 성공률 달성 (매개변수는 5.5배 적음)
- **데이터 효율성**: OpenX 로봇 데이터셋에 대한 사전학습 없이도 높은 성능 유지
- **강력한 일반화**: 언어 지시 다양성, 신규 객체, 미숙련 위치, 객체 외형 변화, 배경 변화, 환경 변화 등 다양한 차원에서 OpenVLA와 동등하거나 우수한 일반화 성능
- **이중팔 로봇 작업 우수성**: 단일팔 데이터만으로 학습한 OpenVLA와 달리 이중팔 작업에서 OpenVLA를 크게 상회

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Model architecture. The left image illustrates the*

- 경량 VLM 구축: Pythia 언어 모델과 LLaVA 데이터셋을 활용하여 70M~1.4B 매개변수 규모의 컴팩트한 vision-language 모델 학습
- LoRA 기반 효율적 미세조정: 사전학습된 VLM의 가중치를 고정하고 LoRA를 통해 전체 매개변수의 5%만 학습 가능하도록 설정
- Policy decoder 통합: 사전학습된 multimodal 모델의 출력을 단순 선형 투영을 통해 diffusion policy decoder에 연결
- Diffusion 기반 액션 생성: 자동회귀 토큰 예측 대신 diffusion 모델을 이용한 직접 로봇 액션 출력으로 추론 속도 개선

## Originality

- 경량 VLM(1.4B 이하)과 diffusion policy의 결합이라는 새로운 VLA 아키텍처 설계로 추론 속도와 데이터 효율성 동시 달성
- LoRA를 활용한 5% 매개변수만 학습하는 초소형 조정 전략으로 계산 효율성 극대화
- 로봇 데이터 사전학습 없이도 vision-language 사전학습의 이점을 활용할 수 있음을 입증
- 자동회귀 토큰 예측에서 diffusion 모델 기반 직접 액션 예측으로의 패러다임 전환

## Limitation & Further Study

- 경량 VLM의 성능 한계: 70M 모델은 더 큰 모델 대비 언어 이해 능력이 제한될 수 있음
- Diffusion 모델의 추가 계산: Diffusion 디코더는 순회 단계로 인한 추가 계산 비용이 발생할 가능성
- 실험 범위 제한: 5가지 실제 로봇 작업으로 평가되었으나 더 다양한 조작 작업에 대한 검증 필요
- 후속 연구: 극도의 경량화(수십 M 매개변수) 모델에 대한 성능 특성 분석, 다양한 로봇 플랫폼과 조작 작업에 대한 확장성 검증, diffusion 단계 수 최적화를 통한 속도 더 개선

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: TinyVLA는 경량 VLM과 diffusion policy의 창의적 결합을 통해 추론 속도와 데이터 효율성이라는 실제 로봇 배포의 핵심 문제를 효과적으로 해결하며, 광범위한 시뮬레이션 및 실제 로봇 실험을 통해 우수한 성능을 입증한 우수한 연구이다.

## Related Papers

- 🔄 다른 접근: [[papers/1616_VLA-Adapter_An_Effective_Paradigm_for_Tiny-Scale_Vision-Lang/review]] — 둘 다 경량 백본을 사용한 효율적인 VLA 모델을 제안하지만 TinyVLA는 diffusion decoder를, VLA-Adapter는 Bridge Attention을 사용한다.
- 🔗 후속 연구: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — TinyVLA의 경량화 접근법을 더 극단적으로 추진하여 1-bit 양자화를 통해 VLA 모델의 효율성을 극대화한다.
- 🏛 기반 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 오픈소스 프레임워크와 데이터셋이 TinyVLA의 효율적인 VLA 모델 개발의 기반이 되었다.
- 🏛 기반 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-2의 vision-language-action 통합 아키텍처가 TinyVLA의 경량화된 VLA 모델 설계의 이론적 기반을 제공한다.
- 🧪 응용 사례: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — 실시간 속도에서의 VLA 실행이라는 실제 배포 문제를 다루어 TinyVLA의 빠른 추론 속도 장점을 실전에 적용합니다.
- 🏛 기반 연구: [[papers/1617_VLA-Cache_Efficient_Vision-Language-Action_Manipulation_via/review]] — VLA 모델의 추론 효율성 향상이라는 공통 목표를 가지며, 캐싱과 경량화라는 상호 보완적 접근을 보여준다.
- 🔄 다른 접근: [[papers/1392_FAST_Efficient_Action_Tokenization_for_Vision-Language-Actio/review]] — TinyVLA의 fast data-efficient approach와 FAST의 DCT-based tokenization은 VLA 모델 효율성을 서로 다른 방향에서 접근한다.
- 🔄 다른 접근: [[papers/1495_NORA_A_Small_Open-Sourced_Generalist_Vision_Language_Action/review]] — TinyVLA와 함께 경량화된 VLA 모델을 추구하지만 NORA는 3B 파라미터로 실시간 성능에, TinyVLA는 데이터 효율성에 집중한다.
- 🔗 후속 연구: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA의 대규모 모델을 TinyVLA의 효율적인 경량화 기법으로 압축하여 실제 배포 가능한 시스템을 구축할 수 있다.
- 🔄 다른 접근: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — 실시간 VLA 실행과 TinyVLA 모두 VLA의 효율성을 추구하지만 최적화와 경량화라는 다른 접근법을 사용합니다.
- 🔄 다른 접근: [[papers/1616_VLA-Adapter_An_Effective_Paradigm_for_Tiny-Scale_Vision-Lang/review]] — 둘 다 경량 VLA 모델을 제안하지만 VLA-Adapter는 Bridge Attention을, TinyVLA는 diffusion policy decoder를 핵심으로 사용한다.
- 🔗 후속 연구: [[papers/1617_VLA-Cache_Efficient_Vision-Language-Action_Manipulation_via/review]] — TinyVLA의 추론 효율성 향상을 KV 캐싱을 통한 추가적인 최적화로 확장하여 더 실용적인 시스템을 구축한다.
- 🔗 후속 연구: [[papers/1351_DeeR-VLA_Dynamic_Inference_of_Multimodal_Large_Language_Mode/review]] — 빠르고 데이터 효율적인 Vision-Language-Action 모델로서 동적 추론을 확장합니다.
- 🔄 다른 접근: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — 둘 다 VLA 모델의 효율성을 추구하지만 BitVLA는 1-bit 양자화로, TinyVLA는 모델 크기 축소로 접근합니다.
- 🏛 기반 연구: [[papers/1374_DynamicVLA_A_Vision-Language-Action_Model_for_Dynamic_Object/review]] — TinyVLA의 효율성 최적화 방법이 실시간 동적 객체 조작을 위한 기반이 됩니다.
