---
title: "1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani"
authors:
  - "Hongyu Wang"
  - "Chuyan Xiong"
  - "Ruiping Wang"
  - "Xilin Chen"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇 조작을 위한 완전한 1-bit Vision-Language-Action 모델인 BitVLA를 제안하여 11.0배의 메모리 감소와 4.4배의 지연 시간 단축을 달성하면서도 full-precision 기준 모델과 비슷한 성능을 유지한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wang et al._2025_BitVLA 1-bit Vision-Language-Action Models for Robotics Manipulation.pdf"
---

# BitVLA: 1-bit Vision-Language-Action Models for Robotics Manipulation

> **저자**: Hongyu Wang, Chuyan Xiong, Ruiping Wang, Xilin Chen | **날짜**: 2025-06-09 | **URL**: [https://arxiv.org/abs/2506.07530](https://arxiv.org/abs/2506.07530)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: We introduce BitVLA, the first fully native 1-bit vision-language-action (VLA) model for robotic manipulation, i*

로봇 조작을 위한 완전한 1-bit Vision-Language-Action 모델인 BitVLA를 제안하여 11.0배의 메모리 감소와 4.4배의 지연 시간 단축을 달성하면서도 full-precision 기준 모델과 비슷한 성능을 유지한다.

## Motivation

- **Known**: Vision-Language-Action (VLA) 모델은 로봇 조작을 위한 유망한 패러다임이지만, 기존 VLA 모델들은 대규모 full-precision 파라미터로 인해 엣지 로봇 플랫폼에 배포하기 어렵다는 문제가 있다.
- **Gap**: 극도로 낮은 비트의 모델링(1-bit LLM)이 언어 영역에서 성과를 보였으나, 다중모달 인식과 로봇 제어로의 확장은 여전히 미흡한 상태이며, post-hoc 압축만으로는 정확도 손실을 초래한다.
- **Why**: 메모리 제약이 있는 엣지 로봇 플랫폼에서 경쟁력 있는 조작 능력을 실현하기 위해 training-time에 양자화와 학습을 통합한 co-design이 필요하며, 이는 로봇 공학 분야의 실제 배포 가능성을 크게 향상시킬 수 있다.
- **Approach**: BitNet b1.58 2B4T 1-bit LLM 백본과 full-precision vision encoder를 초기에 학습한 후, Quantize-then-Distill이라는 양자화 인식 학습 전략으로 vision encoder를 1.58-bit 가중치로 압축하면서 teacher 모델의 지도로 표현 정렬을 유지하고, 대규모 로봇 궤적에 대한 사전학습을 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: We introduce BitVLA, the first fully native 1-bit vision-language-action (VLA) model for robotic manipulation, i*

- **완전한 1-bit VLA 모델**: 모든 파라미터가 ternary {-1, 0, 1}인 첫 번째 fully native 1-bit Vision-Language-Action 모델을 구축했다.
- **극적인 효율성 개선**: 모델 메모리를 11.0배 감소(1.4GB)시키고 end-to-end 지연 시간을 4.4배 단축하면서도 성능 저하 최소화
- **경쟁력 있는 성능 유지**: OpenVLA-OFT baseline과 비교하여 LIBERO 벤치마크 및 실제 로봇 실험에서 유사한 조작 성공률 달성
- **Quantize-then-Distill 전략**: Vision encoder를 1.58-bit 가중치로 압축하는 경량 양자화 인식 훈련 방법 제시로 표현 정렬 유지

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the three-stage training pipeline in BitVLA. We first perform multimodal training with a 1-bit LLM*

- BitNet b1.58 2B4T를 1-bit LLM 백본으로 사용하고 SigLIP-L을 224×224 해상도의 vision encoder로 채택
- LLaVA 훈련 패러다임을 따라 1-bit LLM과 full-precision vision encoder를 페어링하여 multimodal 훈련 수행
- Quantize-then-Distill 단계에서 full-precision vision encoder를 teacher로 사용하여 MSE와 Cross-Entropy 손실로 1.58-bit INT8 vision encoder 훈련
- OpenVLA 패러다임을 따라 약 1M개의 실제 로봇 궤적으로 로봇 조작 사전학습 수행
- Linear transformation에서 ternary 가중치와 INT8 활성화를 사용하여 부동소수점 연산량을 1/10 이상 감소

## Originality

- 다중모달 perception과 로봇 제어 영역에 native 1-bit 모델링을 처음 적용
- 양자화를 훈련 후 압축이 아닌 훈련 과정의 일부로 통합하는 Quantize-then-Distill 방법론 개발
- Vision-Language-Action 학습의 복잡한 상호작용 속에서 극단적인 저비트 양자화의 실현 가능성 입증
- 엣지 로봇 플랫폼의 메모리-성능 trade-off를 해결하는 training-time co-design 패러다임 제시

## Limitation & Further Study

- 현재 SigLIP-L vision encoder 기반이므로 더 큰 vision 모델의 1.58-bit 양자화 가능성 미검증
- Quantize-then-Distill에서 teacher 모델이 여전히 full-precision이므로 배포 시 추가 메모리 요구
- LIBERO 시뮬레이션과 특정 실제 로봇 작업에 한정된 평가로 일반화 가능성에 대한 추가 검증 필요
- 후속 연구에서 더 극단적인 양자화(binary 가중치) 가능성, 더 큰 기본 VLM과의 결합, 그리고 1-bit VLA 특화 가속기 설계 탐색 권장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: BitVLA는 로봇 조작용 VLA 모델의 극단적 양자화의 첫 성공적 사례로, Quantize-then-Distill이라는 혁신적 훈련 전략을 통해 11배 메모리 감소와 4.4배 속도 향상을 달성하면서도 성능을 유지하여 엣지 로봇 배포의 실질적 경로를 제시한다.

## Related Papers

- 🔄 다른 접근: [[papers/1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M/review]] — 둘 다 VLA 모델의 효율성을 추구하지만 BitVLA는 1-bit 양자화로, TinyVLA는 모델 크기 축소로 접근합니다.
- 🔗 후속 연구: [[papers/1617_VLA-Cache_Efficient_Vision-Language-Action_Manipulation_via/review]] — VLA-Cache의 효율적 추론 개념을 1-bit 양자화로 더 극단적으로 발전시킨 메모리 최적화 연구입니다.
- 🧪 응용 사례: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA와 같은 오픈소스 VLA 모델에 BitVLA의 1-bit 양자화 기법을 적용할 수 있는 실용적 연관성이 있습니다.
- 🔄 다른 접근: [[papers/1327_CEED-VLA_Consistency_Vision-Language-Action_Model_with_Early/review]] — 둘 다 VLA 모델의 효율성 향상을 다루지만 BitVLA는 1-bit quantization에, CEED-VLA는 consistency distillation에 중점을 둡니다.
- 🔗 후속 연구: [[papers/1577_SpecPrune-VLA_Accelerating_Vision-Language-Action_Models_via/review]] — SpecPrune-VLA의 VLA 모델 가속화 개념을 더 극단적인 1-bit quantization으로 발전시켜 11배 메모리 감소와 4.4배 지연 단축을 달성한 연구입니다.
- 🔗 후속 연구: [[papers/1495_NORA_A_Small_Open-Sourced_Generalist_Vision_Language_Action/review]] — BitVLA의 1-bit 양자화 기법을 더 실용적인 3B 파라미터 모델로 확장하여 실시간 로봇 제어의 실용성을 높였다.
- 🔗 후속 연구: [[papers/1533_RLRC_Reinforcement_Learning-based_Recovery_for_Compressed_Vi/review]] — BitVLA의 1-bit quantization이 RLRC의 structured pruning과 quantization을 더 극단적인 압축으로 발전시킨다.
- 🔄 다른 접근: [[papers/1564_Scaling_Proprioceptive-Visual_Learning_with_Heterogeneous_Pr/review]] — BitVLA가 단일 embodiment에서의 효율화에 중점을 두는 반면, HPT는 다중 이종 embodiment에서의 표현 학습에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1560_SARA-RT_Scaling_up_Robotics_Transformers_with_Self-Adaptive/review]] — BitVLA의 VLA 모델 경량화 개념을 linear attention을 통한 효율화로 확장하여 on-robot 배포에 최적화했다.
- 🔄 다른 접근: [[papers/1577_SpecPrune-VLA_Accelerating_Vision-Language-Action_Models_via/review]] — BitVLA가 모델 quantization을 통한 경량화에 중점을 두는 반면, SpecPrune-VLA는 동적 토큰 프루닝을 통한 추론 가속화에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M/review]] — TinyVLA의 경량화 접근법을 더 극단적으로 추진하여 1-bit 양자화를 통해 VLA 모델의 효율성을 극대화한다.
- 🔗 후속 연구: [[papers/1593_TrackVLA_Unleashing_Reasoning_and_Memory_Capabilities_in_VLA/review]] — 1-bit VLA의 효율성을 reasoning과 memory 기능과 결합하여 더 강건한 모델을 만들 수 있습니다.
- 🧪 응용 사례: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — BitVLA의 1-bit quantization 기술이 VLA-0의 단순한 구조와 결합되어 실제 로봇에서 더 효율적으로 실행될 수 있다.
- 🔗 후속 연구: [[papers/1616_VLA-Adapter_An_Effective_Paradigm_for_Tiny-Scale_Vision-Lang/review]] — 경량 VLA 모델의 효율성을 1-bit 양자화로 더 극한까지 추진하여 tiny-scale 모델의 발전 방향을 제시한다.
- 🏛 기반 연구: [[papers/1346_Cross-Platform_Scaling_of_Vision-Language-Action_Models_from/review]] — VLA 모델의 효율적 구현을 위한 1-bit 양자화 기초를 제공한다.
- 🔄 다른 접근: [[papers/1327_CEED-VLA_Consistency_Vision-Language-Action_Model_with_Early/review]] — 둘 다 VLA 모델 추론 가속화를 다루지만 CEED-VLA는 consistency distillation과 early-exit에, BitVLA는 1-bit quantization에 중점을 둡니다.
- 🔗 후속 연구: [[papers/1500_OmniVLA_Physically-Grounded_Multimodal_VLA_with_Unified_Mult/review]] — 다중 센서 정보는 BitVLA의 1-bit 양자화된 VLA 모델에서도 활용 가능한 보완적 접근입니다.
