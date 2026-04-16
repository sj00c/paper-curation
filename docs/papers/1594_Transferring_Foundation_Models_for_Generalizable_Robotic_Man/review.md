---
title: "1594_Transferring_Foundation_Models_for_Generalizable_Robotic_Man"
authors:
  - "Jiange Yang"
  - "Wenhui Tan"
  - "Chuhao Jin"
  - "Keling Yao"
  - "Bei Liu"
date: "2023.06"
doi: ""
arxiv: ""
score: 4.0
essence: "인터넷 규모의 기초 모델(foundation models)에서 생성된 언어-추론 기반 분할 마스크를 활용하여 로봇 조작 작업을 조건화함으로써 샘플 효율적인 일반화를 달성하는 패러다임을 제안한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yang et al._2023_Transferring Foundation Models for Generalizable Robotic Manipulation.pdf"
---

# Transferring Foundation Models for Generalizable Robotic Manipulation

> **저자**: Jiange Yang, Wenhui Tan, Chuhao Jin, Keling Yao, Bei Liu, Jianlong Fu, Ruihua Song, Gangshan Wu, Limin Wang | **날짜**: 2023-06-09 | **URL**: [https://arxiv.org/abs/2306.05716](https://arxiv.org/abs/2306.05716)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2. Our model comprises four components: (1) GPT-4 reasons target objects based on human demands. (2) A multi-moda*

인터넷 규모의 기초 모델(foundation models)에서 생성된 언어-추론 기반 분할 마스크를 활용하여 로봇 조작 작업을 조건화함으로써 샘플 효율적인 일반화를 달성하는 패러다임을 제안한다.

## Motivation

- **Known**: RT-1 같은 기존 접근법은 대규모 로봇 데이터 수집에 의존하지만 데이터 다양성 부족으로 새로운 객체와 환경에서의 일반화 능력이 제한된다.
- **Gap**: 기존 로봇 조작 방법은 비용이 많이 드는 대규모 데이터 수집이 필요하고 충분한 데이터 다양성을 갖지 못해 미지의 객체와 환경에서 성능 저하가 발생한다.
- **Why**: 실제 환경에서 작동 가능한 범용 로봇 에이전트를 개발하는 것은 로봇공학의 오랜 과제이며, 기초 모델의 지식을 활용하면 데이터 효율성을 크게 개선할 수 있다.
- **Approach**: GPT-4로 언어 명령을 해석하여 객체 프롬프트 생성, SAM을 통해 언어-추론 분할 마스크 생성, 그리고 이 마스크를 활용하는 two-stream 정책 모델(TPM)을 설계하여 로봇 행동을 예측한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. A demonstration of our task. Receiving human instruction “I want to take a shower”, our model can reason out t*

- **기초 모델 활용 패러다임**: 인터넷 규모 비전 기초 모델의 의미론적, 기하학적, 시간적 상관 정보를 로봇 조작에 통합하는 새로운 접근법을 제시
- **Two-stream 정책 모델**: 전역 RGB 정보를 처리하는 깊은 분지와 지역 객체 관련 RGB-M 정보를 처리하는 얕은 분지로 구성되어 robust 3D 지각을 실현
- **샘플 효율적 일반화**: 1000개 시연(40개 객체)으로 훈련하여 미지의 객체, 의미론적 카테고리, 예상하지 못한 배경에서 효과적으로 일반화
- **다중 로봇 플랫폼 검증**: Franka Emika 로봇과 저비용 이족 로봇에서 실증하여 여러 조작 기술(drawer 열기, picking-placing, stacking 등)에 확장 가능함을 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Our model comprises four components: (1) GPT-4 reasons target objects based on human demands. (2) A multi-moda*

- **언어-추론 마스크 생성**: GPT-4를 활용해 자연어 명령에서 목표 객체 프롬프트 추출
- **객체 탐지 및 추적**: open-vocabulary detection과 tracking 모델로 원하는 객체 식별 및 위치 파악
- **분할 마스크 생성**: SAM(Segment Anything Model) 기초 모델을 활용하여 목표 객체의 고정밀 분할 마스크 생성
- **Two-stream 정책 모델 아키텍처**: 깊은 분지(전역 RGB)와 얕은 분지(지역 RGB-M)로 구성하고 attention mechanism으로 multi-view 특성과 로봇 proprioception 상태 융합
- **Imitation learning 기반 훈련**: end-to-end 방식으로 마스크 조건화 정책을 학습하여 depth 캘리브레이션 불필요
- **폐루프 행동 예측**: 원시 이미지 입력으로부터 연속 로봇 행동을 동적으로 출력하는 closed-loop 방식 채택

## Originality

- **기초 모델 통합의 새로운 방식**: 기존의 prompt 기반 분할과 점구름 구성 방식 대신, 정교한 detection-tracking-segmentation 파이프라인으로 더 정밀한 객체 표현 제공
- **언어-추론 마스크 모달리티**: SAM으로 생성된 분할 마스크를 직접 정책 조건으로 활용하여 언어의 모호성을 완화하고 기하학적 정보를 명시적으로 제공
- **Local-global 이중 지각 구조**: 단순 RGB 인코딩이 아닌 전역-지역 정보를 동시에 처리하는 two-stream 아키텍처로 공간 관계 이해 강화
- **실제 환경에서의 scalable 시스템**: 깊이 정보 불필요, 완벽한 객체 마스크 불요구, 폐루프 방식으로 현실적 제약 극복

## Limitation & Further Study

- **훈련 데이터 규모**: 1000개 시연으로 훈련하여 더 복잡한 다중 객체 상호작용이나 동역학적 제약이 강한 작업의 일반화 능력 미검증
- **기초 모델 성능 의존성**: SAM, open-vocabulary detection 등 기초 모델의 오류가 누적되어 최종 성능 한계 발생 가능
- **작업 범위 제한**: pick-and-place 계열 작업에 중점으로 더 복잡한 조작(섬세한 그래스핑, 힘 제어 필요 작업) 미평가
- **비교 평가 제한**: RT-1 등 최신 baseline과의 직접 정량적 비교 부족, 주로 ablation 중심의 평가
- **후속 연구**: (1) 더 큰 규모 다양한 실제 환경 데이터로 일반화 강화, (2) 정책 모델의 생성 모델링 탐색, (3) reinforcement learning 결합으로 학습 효율성 증대

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 기초 모델의 지식을 체계적으로 로봇 조작에 통합하는 실질적인 패러다임을 제시하였으며, 언어-추론 마스크라는 새로운 조건화 모달리티와 two-stream 정책 모델로 샘플 효율적 일반화를 달성한 의미 있는 기여를 했다.

## Related Papers

- 🔄 다른 접근: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — 둘 다 foundation model을 로봇 조작에 전이하지만 RoboFlamingo는 VLM 기반 정책 구축에 집중하는 다른 접근법을 제시합니다.
- 🔗 후속 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — 언어 모델을 로봇 제어에 활용하는 Code as Policies의 개념을 foundation model 전이 학습으로 확장한 연구입니다.
- 🏛 기반 연구: [[papers/1578_SPRINT_Scalable_Policy_Pre-Training_via_Language_Instruction/review]] — 언어 명령을 통한 정책 사전학습의 확장 가능한 방법론을 제공하여 foundation model 전이의 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1506_Open-World_Object_Manipulation_using_Pre-trained_Vision-Lang/review]] — Open-World Object Manipulation은 기초 모델을 활용한 일반화 가능한 로봇 조작의 이론적 배경을 제시합니다.
- 🔗 후속 연구: [[papers/1315_AutoRT_Embodied_Foundation_Models_for_Large_Scale_Orchestrat/review]] — AutoRT는 기초 모델의 대규모 로봇 학습 오케스트레이션을 통해 일반화 가능한 조작을 실현하는 확장된 접근법입니다.
- 🏛 기반 연구: [[papers/1454_Learning_Transferable_Visual_Models_From_Natural_Language_Su/review]] — Learning Transferable Visual Models은 기초 모델에서 로봇 조작으로의 전이 학습을 위한 시각 표현 학습 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — Foundation model을 로봇 제어에 적용하는 선구적 연구로서 transfer learning 접근법의 이론적 근거를 제공한다.
- 🔗 후속 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-1의 foundation model 활용을 언어-추론 기반 분할로 더 정교하게 발전시켜 일반화 성능을 향상시킨다.
- 🔄 다른 접근: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — 둘 다 foundation model을 로봇 조작에 활용하지만 1594는 분할 마스크 기반, RoboFlamingo는 VLM 기반 접근법을 제시합니다.
- 🔗 후속 연구: [[papers/1302_Adapt3R_Adaptive_3D_Scene_Representation_for_Domain_Transfer/review]] — 일반화 가능한 로봇 조작을 위한 foundation model 전이와 3D 장면 표현 적응이 상호 보완적입니다.
- 🔗 후속 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — Diffusion Policy를 foundation model로 확장하여 일반화 가능한 로봇 조작으로 발전시킵니다.
