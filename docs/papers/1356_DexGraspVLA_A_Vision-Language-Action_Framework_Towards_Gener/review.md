---
title: "1356_DexGraspVLA_A_Vision-Language-Action_Framework_Towards_Gener"
authors:
  - "Yifan Zhong"
  - "Xuchuan Huang"
  - "Ruochong Li"
  - "Ceyao Zhang"
  - "Zhang Chen"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "DexGraspVLA는 Vision-Language model을 고수준 계획자로, diffusion 기반 저수준 행동 컨트롤러를 학습하는 계층적 VLA 프레임워크로, foundation model을 통해 언어·시각 입력을 도메인 불변 표현으로 변환하여 모방 학습의 일반화를 달성한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Multimodal_Instruction_Following"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhong et al._2025_DexGraspVLA A Vision-Language-Action Framework Towards General Dexterous Grasping.pdf"
---

# DexGraspVLA: A Vision-Language-Action Framework Towards General Dexterous Grasping

> **저자**: Yifan Zhong, Xuchuan Huang, Ruochong Li, Ceyao Zhang, Zhang Chen, Tianrui Guan, Fanlian Zeng, Ka Num Lui, Yuyao Ye, Yitao Liang, Yaodong Yang, Yuanpei Chen | **날짜**: 2025-02-28 | **URL**: [https://arxiv.org/abs/2502.20900](https://arxiv.org/abs/2502.20900)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of DexGraspVLA. A pre-trained VLM-based high-level planner (purple) decomposes prompts into object-*

DexGraspVLA는 Vision-Language model을 고수준 계획자로, diffusion 기반 저수준 행동 컨트롤러를 학습하는 계층적 VLA 프레임워크로, foundation model을 통해 언어·시각 입력을 도메인 불변 표현으로 변환하여 모방 학습의 일반화를 달성한다.

## Motivation

- **Known**: Dexterous grasping은 로봇 조작의 기본 과제이나, 기존 연구는 단일 객체 또는 제한된 환경 가정에 의존하며 일반화 성능이 제약적이다. Foundation model은 인터넷 규모 데이터로 학습되어 우수한 일반화 능력을 보유하지만, 로봇 정책에 직접 적용 시 대규모 시연 데이터를 요구하고 unseen scenario에서 성능 저하가 발생한다.
- **Gap**: Foundation model의 우수한 일반화 능력과 모방 학습의 제한된 데이터 활용성을 결합하여, 도메인 시프트 완화를 통해 폐루프 제어 정책의 강건한 일반화를 달성하는 방법이 부족하다. 특히 cluttered scenario에서의 장기 지평 다중 객체 grasping과 adversarial robustness를 동시에 달성하는 통합 프레임워크가 부재하다.
- **Why**: 실세계 로봇 응용은 다양한 객체 물리 특성, 환경 변동(조명, 배경), 방해 조건에서 견고한 grasping 능력을 요구하며, 제한된 전문가 데이터로부터 효과적인 일반화 달성은 실용적 배포의 핵심 과제이다.
- **Approach**: DexGraspVLA는 사전학습 VLM을 고수준 계획자로 활용하여 도메인 불변 affordance 신호를 생성하고, 저수준 컨트롤러는 vision foundation model로 multimodal 입력을 정제한 후 diffusion 기반 action head로 폐루프 행동을 생성하는 계층적 구조를 채택한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: We propose DexGraspVLA, a hierarchical VLA*

- **Unseen cluttered scenario 일반화**: 1,287개의 unseen object, 조명, 배경 조합에서 90.8%의 grasping 성공률 달성
- **단일 객체 성능**: 98.6% 성공률로 원본 시각 입력 학습 기준선 대비 48% 이상 성능 향상
- **장기 지평 명령 실행**: 자유형 long-horizon prompt에 대해 89.6% 성공률로 embodied reasoning 기반 다단계 task 완성
- **Robustness**: adversarial object, 인간 방해, 실패 복구 상황에서 견고한 성능 유지
- **일반성 확장**: Nonprehensile grasping으로 확장 적용 가능성 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of DexGraspVLA. A pre-trained VLM-based high-level planner (purple) decomposes prompts into object-*

- Pre-trained VLM을 high-level planner로 frozen 활용하여 prompt를 object 수준 grasping instruction과 bounding box로 분해
- Vision foundation model (예: SAM 등)로 target object mask 추출 및 RGB, mask, proprioception을 multimodal 입력으로 인코딩
- Diffusion-based action head (DiT model)를 imitation learning으로 학습하여 action chunk 예측
- Domain-invariant 표현 공간에서 모방 학습 적용으로 도메인 시프트 완화 및 일반화 향상
- High-level planner가 execution을 모니터링하며 갱신된 scene 기반 새로운 instruction 제시로 장기 task 관리

## Originality

- Foundation model의 domain-invariant 표현 능력과 imitation learning의 action modeling을 계층적으로 결합하는 novel architecture 제시
- Frozen VLM을 affordance 신호 생성에 활용하면서도 저수준 컨트롤러에서 diffusion 기반 폐루프 정책 학습 - 기존 end-to-end fine-tuning과 modular frozen 접근 간 중간 경로 개척
- Unseen cluttered scenario에서 90+% 성공률 달성 - 기존 imitation learning 기반 dexterous grasping 대비 획기적 성과
- Long-horizon prompt execution, adversarial robustness, failure recovery를 단일 프레임워크에서 동시 입증한 최초 사례

## Limitation & Further Study

- Foundation model의 affordance 인식 오류(예: 부정확한 mask 또는 object 분류 실패)가 저수준 컨트롤러 성능에 직접 영향 가능하나, 이에 대한 error propagation 분석 부족
- Diffusion model 기반 action head의 샘플링 과정으로 인한 inference 계산량 증가 및 실시간성 제약에 대한 언급 부재
- 모방 학습 데이터셋의 규모, 수집 프로토콜, 다양성 수준에 대한 상세 기술 부족 - 재현성 및 데이터 요구량 평가 어려움
- 단일 로봇 하드웨어 플랫폼에서만 검증되어 다양한 dexterous hand morphology에 대한 일반화 가능성 미확인
- 후속 연구: (1) Foundation model 오류에 대한 강건성 강화, (2) 효율적 inference 기법 개발, (3) 다중 로봇 플랫폼 확대 실험, (4) sim-to-real 적용 가능성 탐색

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: DexGraspVLA는 foundation model과 imitation learning의 상보적 강점을 계층적으로 통합하여 cluttered real-world scenario에서 unprecedented 90+% 일반화 성능을 달성한 의미 있는 기여이며, 장기 task, adversarial robustness, failure recovery를 동시 달성함으로써 실용적 dexterous grasping 로봇의 실현 가능성을 크게 높였다.

## Related Papers

- 🔄 다른 접근: [[papers/1522_RDT-1B_a_Diffusion_Foundation_Model_for_Bimanual_Manipulatio/review]] — diffusion 기반 bimanual manipulation과 VLA 프레임워크 기반 dexterous grasping은 서로 다른 접근법으로 복잡한 로봇 조작을 해결한다.
- 🔗 후속 연구: [[papers/1358_DexVLA_Vision-Language_Model_with_Plug-In_Diffusion_Expert_f/review]] — DexVLA의 plug-in diffusion expert와 DexGraspVLA의 diffusion 기반 저수준 컨트롤러는 모두 diffusion을 VLA에 통합하는 방향성을 공유한다.
- 🏛 기반 연구: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — Octo의 generalist robot policy 개념은 DexGraspVLA가 추구하는 일반적인 dexterous manipulation을 위한 기초 모델 아키텍처를 제공한다.
- 🏛 기반 연구: [[papers/1413_GraspVLA_a_Grasping_Foundation_Model_Pre-trained_on_Billion-/review]] — 대규모 그립 데이터로 사전학습된 foundation model이 손가락 그립 VLA의 기반이 됩니다.
- 🔗 후속 연구: [[papers/1356_DexGraspVLA_A_Vision-Language-Action_Framework_Towards_Gener/review]] — Vision-Language model을 활용한 계층적 그립 제어의 구체적 구현을 제시합니다.
- 🏛 기반 연구: [[papers/1511_PaLI-X_On_Scaling_up_a_Multilingual_Vision_and_Language_Mode/review]] — 다국어 비전-언어 모델이 도메인 불변 표현 학습의 이론적 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1413_GraspVLA_a_Grasping_Foundation_Model_Pre-trained_on_Billion-/review]] — 둘 다 grasping VLA 모델이지만 billion-scale synthetic data vs plug-in diffusion expert라는 다른 학습 전략을 사용한다.
- 🔄 다른 접근: [[papers/1574_SKT_Integrating_State-Aware_Keypoint_Trajectories_with_Visio/review]] — DexGraspVLA는 VLM과 keypoint 기반 접근법을 정교한 조작에 적용하는 유사하지만 다른 방법론을 제공한다.
