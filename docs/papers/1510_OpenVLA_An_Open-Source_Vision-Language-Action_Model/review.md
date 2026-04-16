---
title: "1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model"
authors:
  - "Moo Jin Kim"
  - "Karl Pertsch"
  - "Siddharth Karamcheti"
  - "Ted Xiao"
  - "Ashwin Balakrishna"
date: "2024.06"
doi: ""
arxiv: ""
score: 4.0
essence: "OpenVLA는 970k개의 로봇 시연 데이터로 학습된 7B 파라미터의 오픈소스 Vision-Language-Action 모델로, 폐쇄형 모델들보다 우수한 성능을 보이면서 효율적인 미세조정과 배포를 지원한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kim et al._2024_OpenVLA An Open-Source Vision-Language-Action Model.pdf"
---

# OpenVLA: An Open-Source Vision-Language-Action Model

> **저자**: Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, Chelsea Finn | **날짜**: 2024-06-13 | **URL**: [https://arxiv.org/abs/2406.09246](https://arxiv.org/abs/2406.09246)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: We present OpenVLA, a 7B-parameter open-source vision-language-action model (VLA), trained*

OpenVLA는 970k개의 로봇 시연 데이터로 학습된 7B 파라미터의 오픈소스 Vision-Language-Action 모델로, 폐쇄형 모델들보다 우수한 성능을 보이면서 효율적인 미세조정과 배포를 지원한다.

## Motivation

- **Known**: VLM 기반의 robot policy 학습이 가능하며, RT-2와 같은 폐쇄형 VLA 모델들이 좋은 일반화 성능을 보인다. 하지만 기존 VLA들은 폐쇄적이고 효율적인 미세조정 방법이 부재하다.
- **Gap**: 기존의 VLA 모델들은 대부분 폐쇄적이고 접근 불가능하며, 새로운 작업에 대한 효율적인 미세조정 방법과 실제 배포 전략이 탐색되지 않았다.
- **Why**: 오픈소스 VLA와 효율적인 미세조정 방법은 로봇 커뮤니티의 광범위한 채택을 촉진하고, 소비자 수준의 하드웨어에서도 로봇 정책을 적응시킬 수 있게 함으로써 로봇 분야 발전을 가속화한다.
- **Approach**: Llama 2 언어 모델과 DINOv2, SigLIP의 시각 인코더를 결합한 VLM 백본을 Open X-Embodiment 데이터셋의 다양한 로봇 시연 데이터로 미세조정하고, LoRA와 quantization을 활용한 효율적 적응 방법을 제시한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: BridgeData V2 WidowX robot evaluation tasks and results. We evaluate OpenVLA and prior*

- **성능 우수성**: RT-2-X(55B)를 7배 적은 파라미터로 16.5% 절대 성공률 향상을 29개 작업에서 달성
- **일반화 능력**: 다중 객체를 포함한 멀티태스크 환경에서 강력한 일반화 성능과 언어 기반 제어 능력 입증
- **미세조정 효율성**: Diffusion Policy 대비 20.4% 성능 향상을 달성하면서 효율적 미세조정 가능 입증
- **계산 효율성**: LoRA와 quantization을 통해 소비자 GPU에서 성능 손실 없이 미세조정 및 배포 가능
- **오픈소스 공개**: 모델 체크포인트, 미세조정 노트북, PyTorch 학습 파이프라인 전체를 공개

## How

![Figure 2](figures/fig2.webp)

*Figure 2: OpenVLA model architecture. Given an image observation and a language instruction, the model*

- Llama 2 7B 언어 모델을 기반으로 하며, DINOv2(저수준 공간 정보)와 SigLIP(고수준 의미론)의 다중 해상도 시각 특징을 융합
- 로봇 액션을 언어 모델 어휘로 취급하여 end-to-end VLM 미세조정을 수행
- Open X-Embodiment 데이터셋의 970k 에피소드로 학습하여 다양한 로봇 구현, 작업, 장면 포함
- LoRA(Low-Rank Adaptation)를 사용한 파라미터 효율적 미세조정 방법 적용
- Model quantization을 통한 효율적 배포 실현
- 다양한 로봇 구현에 대한 즉시 제어 및 새로운 로봇 도메인으로의 빠른 적응 지원

## Originality

- VLM의 단순한 patch-as-token 아키텍처를 로봇 제어에 직접 적용하여 확장성과 성능의 균형 달성
- DINOv2와 SigLIP 특징의 명시적 융합을 통해 다중 입도의 시각 정보 활용
- 로봇 분야에서 처음으로 LoRA와 quantization 같은 현대적 효율성 기법의 효과를 체계적으로 입증
- 폐쇄형 모델보다 적은 파라미터로 우수한 성능을 달성하는 새로운 벤치마크 제시
- 완전한 오픈소스 생태계 제공으로 재현성과 커뮤니티 기여 가능성 극대화

## Limitation & Further Study

- 학습 데이터 규모(970k 에피소드)는 인터넷 규모 비전-언어 데이터에 비해 여전히 제한적이며, 로봇 도메인의 데이터 부족 문제 해결 부분적
- 평가는 주로 WidowX와 Google Robot 두 가지 로봇 구현에 제한되어 다양한 로봇 형태로의 일반화 능력 검증 필요
- 실시간 제어와 고주파 행동 생성이 필요한 복잡한 조작 작업에 대한 성능 평가 부재
- 언어 명령의 다양한 표현 방식(paraphrasing)에 대한 강건성 검증 필요
- 후속 연구로 더 큰 규모의 로봇 데이터셋 확보, 다양한 센서 모달리티 통합, 동적 환경에서의 적응 능력 향상 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: OpenVLA는 폐쇄형 대규모 VLA 모델을 능가하는 성능을 더 작은 파라미터로 달성하면서 완전한 오픈소스 공개와 효율적 미세조정 방법을 제시하여 로봇 분야의 파운데이션 모델 생태계 구축에 중요한 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1499_OmniVLA_An_Omni-Modal_Vision-Language-Action_Model_for_Robot/review]] — OmniVLA가 확장한 OpenVLA의 기본 오픈소스 VLA 모델 기반
- 🔄 다른 접근: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — 오픈소스 generalist robot policy에서 VLA vs Octo의 다른 접근법
- 🔗 후속 연구: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — OpenVLA의 기본 구조를 zero modification으로 최적화한 VLA-0의 발전
- 🔗 후속 연구: [[papers/1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M/review]] — OpenVLA의 대규모 모델을 TinyVLA의 효율적인 경량화 기법으로 압축하여 실제 배포 가능한 시스템을 구축할 수 있다.
- 🧪 응용 사례: [[papers/1621_VLABench_A_Large-Scale_Benchmark_for_Language-Conditioned_Ro/review]] — OpenVLA의 성능을 VLABench의 포괄적인 language-conditioned robotics benchmark에서 평가하고 비교할 수 있다.
- 🔄 다른 접근: [[papers/1286_π_05_a_Vision-Language-Action_Model_with_Open-World_Generali/review]] — 둘 다 오픈소스 Vision-Language-Action 모델이지만 π0.5는 heterogeneous 데이터 co-training에 특화되어 있습니다.
- 🏛 기반 연구: [[papers/1287_π_0_A_Vision-Language-Action_Flow_Model_for_General_Robot_Co/review]] — OpenVLA의 오픈소스 VLA 모델은 π0의 vision-language-action 정책 설계에 기초 프레임워크를 제공한다.
- 🔄 다른 접근: [[papers/1403_Gemini_Robotics_15_Pushing_the_Frontier_of_Generalist_Robots/review]] — 대규모 멀티모달 로봇 제어에서 OpenVLA와 다른 접근방식으로 다중 플랫폼 통합을 제안한다.
- 🔗 후속 연구: [[papers/1424_HiMoE-VLA_Hierarchical_Mixture-of-Experts_for_Generalist_Vis/review]] — OpenVLA의 일반화 능력을 이질적 로봇 데이터 처리에 특화된 MoE 구조로 발전시킨다.
- 🔄 다른 접근: [[papers/1429_HybridVLA_Collaborative_Diffusion_and_Autoregression_in_a_Un/review]] — 둘 다 unified VLA 모델이지만 diffusion + autoregressive hybrid vs pure open-source 접근이라는 다른 전략을 사용한다.
- 🔄 다른 접근: [[papers/1413_GraspVLA_a_Grasping_Foundation_Model_Pre-trained_on_Billion-/review]] — OpenVLA와 다르게 합성 데이터 사전학습에 특화된 VLA 모델로 실세계 일반화에 대한 다른 접근법을 제시한다.
- 🔄 다른 접근: [[papers/1464_Magma_A_Foundation_Model_for_Multimodal_AI_Agents/review]] — OpenVLA와 동일한 멀티모달 VLA 접근법이지만 Magma는 SoM/ToM 기법으로 차별화된 시공간 지능을 구현한다.
- 🏛 기반 연구: [[papers/1466_ManipBench_Benchmarking_Vision-Language_Models_for_Low-Level/review]] — OpenVLA 같은 기존 VLM들의 조작 추론 한계를 체계적으로 분석하여 향후 VLA 모델 개발의 기초 지식을 제공한다.
- 🔄 다른 접근: [[papers/1436_InstructVLA_Vision-Language-Action_Instruction_Tuning_from_U/review]] — OpenVLA와 다르게 VLM의 추론 능력을 보존하면서 로봇 조작 성능을 달성하는 instruction tuning 방식을 제안한다.
- 🔄 다른 접근: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — 둘 다 통합된 VLA 모델을 제시하지만, InternVLA-A1은 Mixture-of-Transformers 아키텍처를, OpenVLA는 일반화된 오픈소스 접근법을 택한다.
- 🔗 후속 연구: [[papers/1438_InternVLA-M1_A_Spatially_Guided_Vision-Language-Action_Frame/review]] — OpenVLA의 기본 구조에 공간 그라운딩을 핵심으로 한 확장 가능한 일반 지능 프레임워크를 구축한다.
- 🏛 기반 연구: [[papers/1484_MuJoCo_Playground/review]] — MJX 기반의 GPU 가속 학습은 OpenVLA와 같은 대규모 VLA 모델의 효율적인 훈련을 가능하게 합니다.
- 🔄 다른 접근: [[papers/1495_NORA_A_Small_Open-Sourced_Generalist_Vision_Language_Action/review]] — 둘 다 일반화된 VLA 모델이지만, NORA는 소형 효율성을, OpenVLA는 오픈소스 범용성에 초점을 둔다.
- 🔄 다른 접근: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — Octo와 유사한 generalist robot policy이지만 더 큰 7B 파라미터 규모와 오픈소스 접근법으로 차별화된다.
- 🔗 후속 연구: [[papers/1499_OmniVLA_An_Omni-Modal_Vision-Language-Action_Model_for_Robot/review]] — OmniVLA의 다중 플랫폼 학습이 OpenVLA의 일반화된 아키텍처를 다양한 로봇 플랫폼에서 검증하고 확장한 연구이다.
- 🔗 후속 연구: [[papers/1573_SimpleVLA-RL_Scaling_VLA_Training_via_Reinforcement_Learning/review]] — OpenVLA의 오픈소스 기반을 확장하여 SimpleVLA-RL이 효율적인 강화학습 훈련 방법론을 제시합니다.
- 🔄 다른 접근: [[papers/1546_Robot_Utility_Models_General_Policies_for_Zero-Shot_Deployme/review]] — RUM과 OpenVLA 모두 범용 로봇 정책을 다루지만 zero-shot 배포와 대규모 사전훈련이라는 다른 접근법을 사용합니다.
- 🔗 후속 연구: [[papers/1547_Robotic_Control_via_Embodied_Chain-of-Thought_Reasoning/review]] — OpenVLA의 기본 VLA 구조를 확장하여 embodied chain-of-thought 추론 능력을 추가함으로써 성능을 크게 향상시켰다.
- 🔄 다른 접근: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — OpenVLA는 RT-1과 유사한 대규모 로봇 데이터 학습 접근법을 취하지만 오픈소스 형태로 제공되는 차별점이 있다.
- 🔗 후속 연구: [[papers/1557_Running_VLAs_at_Real-time_Speed/review]] — 실시간 VLA 최적화는 OpenVLA와 같은 대규모 VLA 모델을 실제 로봇 제어에 적용 가능하게 만드는 핵심 기술입니다.
- 🏛 기반 연구: [[papers/1588_TinyVLA_Towards_Fast_Data-Efficient_Vision-Language-Action_M/review]] — OpenVLA의 오픈소스 프레임워크와 데이터셋이 TinyVLA의 효율적인 VLA 모델 개발의 기반이 되었다.
- 🏛 기반 연구: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — open-source vision-language-action model의 기반이 되는 통합 모델링 접근법입니다.
- 🏛 기반 연구: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — OpenVLA의 오픈소스 프레임워크가 범용 VLA 모델 개발 시 고려해야 할 핵심 요소들의 실험적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1605_VIMA_General_Robot_Manipulation_with_Multimodal_Prompts/review]] — OpenVLA가 VIMA의 멀티모달 프롬프트 아이디어를 대규모 오픈소스 VLA 모델로 확장 발전시켰다.
- 🔄 다른 접근: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — OpenVLA는 RoboFlamingo와 유사한 VLM 기반 로봇 정책이지만 오픈소스이며 더 광범위한 데이터셋을 활용한다.
- 🏛 기반 연구: [[papers/1615_VLA-0_Building_State-of-the-Art_VLAs_with_Zero_Modification/review]] — OpenVLA의 오픈소스 vision-language-action 모델이 구조 변경 없이 액션을 텍스트로 표현하는 VLA-0의 설계 기반이다.
- 🏛 기반 연구: [[papers/1385_EO-1_An_Open_Unified_Embodied_Foundation_Model_for_General_R/review]] — OpenVLA의 오픈소스 VLA 프레임워크가 EO-1의 unified embodied foundation model 설계의 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1410_GR-3_Technical_Report/review]] — 둘 다 오픈소스 VLA 모델이지만 GR-3는 co-training에, OpenVLA는 일반화 가능성에 중점을 둔다.
- 🧪 응용 사례: [[papers/1372_DROID_A_Large-Scale_In-The-Wild_Robot_Manipulation_Dataset/review]] — OpenVLA는 DROID와 같은 대규모 다양한 데이터셋을 활용한 범용 VLA 모델의 실제 구현 사례임
- 🧪 응용 사례: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — OpenVLA와 같은 오픈소스 VLA 모델에 BitVLA의 1-bit 양자화 기법을 적용할 수 있는 실용적 연관성이 있습니다.
- 🏛 기반 연구: [[papers/1336_CogACT_A_Foundational_Vision-Language-Action_Model_for_Syner/review]] — OpenVLA의 오픈소스 VLA 모델이 CogACT의 특화된 cognition-action 분리 설계의 기반 모델
- 🏛 기반 연구: [[papers/1358_DexVLA_Vision-Language_Model_with_Plug-In_Diffusion_Expert_f/review]] — OpenVLA의 오픈소스 VLA 아키텍처와 학습 방법론이 DexVLA의 billion 규모 diffusion expert 통합의 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1363_Diffusion_Transformer_Policy/review]] — 오픈소스 generalist robot policy의 기본 구조와 원리를 제공합니다.
- 🔗 후속 연구: [[papers/1366_Discrete_Diffusion_VLA_Bringing_Discrete_Diffusion_to_Action/review]] — 오픈소스 VLA의 action decoding을 discrete diffusion으로 개선하는 구체적 방법을 제시합니다.
- 🏛 기반 연구: [[papers/1373_DualVLA_Building_a_Generalizable_Embodied_Agent_via_Partial/review]] — OpenVLA는 DualVLA가 해결하려는 Vision-Language-Action 모델의 기본 아키텍처를 제공합니다.
- 🔄 다른 접근: [[papers/1500_OmniVLA_Physically-Grounded_Multimodal_VLA_with_Unified_Mult/review]] — OmniVLA와 OpenVLA 모두 비전-언어-액션 모델이지만 물리적 센서 정보 통합 여부에서 차별화됩니다.
- 🔄 다른 접근: [[papers/1296_A_Pragmatic_VLA_Foundation_Model/review]] — 오픈소스 VLA 모델로서 LingBot-VLA와 다른 접근 방식의 기초 모델을 제시합니다.
