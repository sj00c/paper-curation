---
title: "1633_X-VLA_Soft-Prompted_Transformer_as_Scalable_Cross-Embodiment"
authors:
  - "Jinliang Zheng"
  - "Jianxiong Li"
  - "Zhihao Wang"
  - "Dongxiu Liu"
  - "Xirui Kang"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "X-VLA는 소프트 프롬프트(Soft Prompt) 기법을 도입하여 이질적인 로봇 플랫폼 간 cross-embodiment 학습을 효과적으로 처리하는 scalable Vision-Language-Action 모델이다. 0.9B 파라미터 규모로 6개 시뮬레이션 벤치마크와 3개 실로봇에서 SOTA 성능을 달성한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zheng et al._2025_X-VLA Soft-Prompted Transformer as Scalable Cross-Embodiment Vision-Language-Action Model.pdf"
---

# X-VLA: Soft-Prompted Transformer as Scalable Cross-Embodiment Vision-Language-Action Model

> **저자**: Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, Ya-Qin Zhang, Jiangmiao Pang, Jingjing Liu, Tai Wang, Xianyuan Zhan | **날짜**: 2025-10-11 | **URL**: [https://arxiv.org/abs/2510.10274](https://arxiv.org/abs/2510.10274)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 | X-VLA employs distinctive learnable embeddings, referred to as soft prompt, to effectively*

X-VLA는 소프트 프롬프트(Soft Prompt) 기법을 도입하여 이질적인 로봇 플랫폼 간 cross-embodiment 학습을 효과적으로 처리하는 scalable Vision-Language-Action 모델이다. 0.9B 파라미터 규모로 6개 시뮬레이션 벤치마크와 3개 실로봇에서 SOTA 성능을 달성한다.

## Motivation

- **Known**: VLA 모델은 LLM과 VLM의 성공을 로보틱스에 적용하여 자연어 지시를 따르고 복잡한 조작을 수행할 수 있는 generalist 모델로 주목받고 있다. 대규모 cross-embodiment 데이터셋으로 사전학습하면 다양한 환경과 구체에 대한 일반화 성능이 향상된다.
- **Gap**: 기존 VLA 방법은 embodiment별 action space 이질성만 처리하며, 카메라 설정, 시각 영역, 작업 분포 등 다른 이질성 차원의 distributional shift와 semantic misalignment 문제를 해결하지 못한다. 표준화되지 않은 데이터 수집 프로토콜과 하드웨어 불일치로 인한 proprioceptive-aware reasoning이 미흡하다.
- **Why**: Heterogeneous 로봇 데이터의 효과적인 통합은 VLA의 cross-embodiment 적응 능력과 일반화 성능을 크게 향상시킬 수 있으며, 소형 모델로도 대규모 모델 수준의 성능을 달성하여 실제 배포의 효율성을 높일 수 있다.
- **Approach**: 데이터 소스별로 구별되는 learnable embedding 세트를 Soft Prompt로 도입하여 embodiment-specific 특성을 조기 단계부터 인코딩한다. Flow-matching 기반 VLA 아키텍처에 표준 Transformer encoder를 stack하여 multimodal 특성 융합과 action 생성을 수행한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1 | X-VLA employs distinctive learnable embeddings, referred to as soft prompt, to effectively*

- **Cross-embodiment SOTA 달성**: 6개 시뮬레이션 벤치마크(Libero, Calvin, VLABench, Robotwin2 등)와 3개 실로봇(Agibot-3, Agilex, Franka, UR5 등)에서 동시에 최고 성능 달성
- **효율적 파라미터 튜닝**: 1% 파라미터(9M)만 조정하여 Libero에서 93%, Simpler-WidowX에서 54% 성공률 달성, π0(300배 더 많은 파라미터)과 비등한 성능
- **Dexterous 작업 성능**: 1,200개 시연만으로 천 접기 작업에서 2분 이내에 1개 완성하는 throughput 달성
- **안정적 학습 동역학**: Soft Prompt 활용 시 예측 오류가 낮고 안정적인 학습 곡선 유지
- **확장 가능성**: 모델 크기, 데이터 소스 수, 데이터 량 증가에 따른 성능 향상 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2 | Comparison among four methods in handling heterogeneity in cross-embodiment training.*

- **Soft Prompt 메커니즘**: 각 데이터 소스마다 구별되는 learnable embedding 세트를 도입하여 embodiment-specific 특성을 인코딩
- **Flow-matching 기반 VLA**: Optimal transport 경로를 따르는 velocity field를 학습하여 noise에서 action chunk로 변환
- **Two-phase 학습**: Phase I에서 290K 에피소드(Droid, Robomind, Agibot)로 7개 플랫폼 cross-embodiment 사전학습, Phase II에서 새로운 도메인용 soft prompt 최적화 및 백본 고정 상태로 파인튜닝
- **Multimodal 입력 처리**: Multi-view 이미지, 언어 프롬프트, proprioceptive 특성을 ViT와 Transformer로 통합 처리
- **LoRA 활용**: Pretrained VLM에 LoRA를 적용하여 효율적인 파라미터 업데이트
- **Prefix tuning enhancement**: Cross-task/environment/robot 적응 시 파라미터 효율성 강화

## Originality

- **Meta-learning 관점의 재해석**: Hardware 설정과 데이터 타입을 task-specific 특성으로 재정의하여 prompt-learning 기법 적용
- **Minimal parameter 추가**: 전체 모델의 1% 파라미터만으로 cross-embodiment 이질성 처리로 기존 방식 대비 혁신적 효율성
- **Unified soft prompt framework**: Domain-specific action projection과 HPT-style projection 대비 더 간단하고 확장 가능한 단일 프레임워크 제시
- **Flow-matching과의 결합**: Diffusion 기반이 아닌 flow-matching을 VLA에 적용하여 안정적이고 효율적인 action 생성
- **실증적 검증의 광범위성**: 시뮬레이션과 실로봇 통합 평가, 다양한 이질성 차원(embodiment, environment, task)의 체계적 검증

## Limitation & Further Study

- **데이터 규모 제한**: 290K 에피소드로 사전학습하였으나 더 대규모 데이터셋과의 비교 분석 부재
- **Soft prompt 용량 분석 미흡**: Learnable embedding 차원 수와 성능의 관계에 대한 상세한 ablation study 부족
- **새 embodiment 발견성**: 완전히 새로운 하드웨어 구성에 대한 zero-shot adaptation 성능 평가 미흡, 항상 new soft prompt 학습 필요
- **계산 복잡도 분석**: Inference 시간과 메모리 오버헤드에 대한 정량적 분석 부재
- **다중 로봇 동시 제어**: 단일 모델에서 여러 embodiment을 동시에 제어하는 시나리오에 대한 평가 부족
- **후속 연구 방향**: (1) Soft prompt 구조의 자동 발견 메커니즘 개발, (2) Zero-shot embodiment transfer를 위한 메타러닝 통합, (3) 대규모 멀티모달 로봇 데이터셋 구축, (4) Real-to-sim transfer 능력 강화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: X-VLA는 soft prompt를 통한 우아하고 효율적인 cross-embodiment 처리 방식으로 VLA 분야의 중요한 진전을 이룬다. 파라미터 효율성과 광범위한 실증 평가를 통해 실제 로봇 응용 분야에서의 높은 실용성을 입증하며, flow-matching 기반 아키텍처의 안정성과 확장성은 향후 generalist 로봇 모델 개발의 주요 방향을 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — cross-embodiment learning의 기반이 되는 open x-embodiment dataset과 모델입니다.
- 🔗 후속 연구: [[papers/1346_Cross-Platform_Scaling_of_Vision-Language-Action_Models_from/review]] — cross-platform scaling을 soft-prompted transformer로 효율적으로 구현한 확장 연구입니다.
- 🔄 다른 접근: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — cross-embodiment learning에서 서로 다른 접근법 - soft prompt vs unified policy입니다.
- 🏛 기반 연구: [[papers/1306_All_Robots_in_One_A_New_Standard_and_Unified_Dataset_for_Ver/review]] — Cross-embodiment learning을 위한 통합 데이터셋과 표준화 방법론의 기본 토대를 제공한다.
- 🔄 다른 접근: [[papers/1447_Latent_Action_Diffusion_for_Cross-Embodiment_Manipulation/review]] — Cross-embodiment manipulation을 latent action diffusion으로 해결하는 다른 접근법이다.
