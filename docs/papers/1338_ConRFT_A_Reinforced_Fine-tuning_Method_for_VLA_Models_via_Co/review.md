---
title: "1338_ConRFT_A_Reinforced_Fine-tuning_Method_for_VLA_Models_via_Co"
authors:
  - "Yuhui Chen"
  - "Shuai Tian"
  - "Shugao Liu"
  - "Yingting Zhou"
  - "Haoran Li"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "ConRFT는 Vision-Language-Action 모델의 강화학습 기반 미세조정 방법으로, 오프라인 단계에서 행동 복제와 Q-러닝을 통합하고 온라인 단계에서 consistency policy를 통해 실제 로봇 조작 작업에서 높은 성공률을 달성한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Chen et al._2025_ConRFT A Reinforced Fine-tuning Method for VLA Models via Consistency Policy.pdf"
---

# ConRFT: A Reinforced Fine-tuning Method for VLA Models via Consistency Policy

> **저자**: Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou, Haoran Li, Dongbin Zhao | **날짜**: 2025-02-08 | **URL**: [https://arxiv.org/abs/2502.05450](https://arxiv.org/abs/2502.05450)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of ConRFT. This figure illustrates the architecture of our reinforced fine-tuning approach for a pre-tr*

ConRFT는 Vision-Language-Action 모델의 강화학습 기반 미세조정 방법으로, 오프라인 단계에서 행동 복제와 Q-러닝을 통합하고 온라인 단계에서 consistency policy를 통해 실제 로봇 조작 작업에서 높은 성공률을 달성한다.

## Motivation

- **Known**: VLA 모델은 대규모 모방 학습으로 강력한 표현을 학습하지만, 실제 환경에서는 제한적이고 불일치한 시연 데이터로 인해 감독 미세조정(SFT)의 성능이 떨어진다. LLM과 VLM에서 RL 기반 미세조정이 효과적임이 입증되었다.
- **Gap**: VLA 모델에 대한 RL 기반 미세조정은 실제 로봇의 안전성, 샘플 효율성, 접촉이 풍부한 환경에서의 위험 제약 때문에 직접 적용이 어렵다. 기존 RL 연구들은 데이터 증강이나 품질 개선에 중점을 두어 시연 데이터 분포 외의 상태 탐색이 제한된다.
- **Why**: 실제 로봇 조작은 비용이 높고 안전이 중요한 접촉 작업을 포함하므로, 제한된 데이터로도 높은 성공률을 달성하는 효율적인 미세조정 방법이 필요하다. 이는 현실의 로봇 응용에서 VLA 모델의 실용성을 크게 향상시킨다.
- **Approach**: ConRFT는 오프라인-온라인 두 단계 파이프라인으로, 오프라인 단계(Cal-ConRFT)에서는 consistency 기반 행동 복제와 Q-러닝을 통합하여 적은 시연으로 안정적인 정책과 가치함수를 학습하고, 온라인 단계(HIL-ConRFT)에서는 인간 개입을 통해 안전한 탐색 하에서 consistency policy로 미세조정한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Fig. 3: Learning curves during online training. This figure presents the success rates, intervention rates, and episode *

- **성공률 개선**: 8개 실제 로봇 작업에서 평균 96.3% 성공률 달성, 기존 감독 학습 방법 대비 144% 개선
- **샘플 효율성**: 45-90분의 온라인 미세조정만으로 높은 성능 달성
- **에피소드 길이 단축**: 기존 방법 대비 1.9배 짧은 에피소드 길이
- **통합 훈련 목표**: 오프라인과 온라인 단계 모두에서 일관된 consistency 기반 훈련 목표 사용
- **코드 공개**: 재현 가능성을 위해 프로젝트 웹사이트에서 코드와 영상 공개

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of ConRFT. This figure illustrates the architecture of our reinforced fine-tuning approach for a pre-tr*

- **오프라인 단계(Cal-ConRFT)**: 시연 데이터로부터 행동 복제(BC) 손실과 Q-러닝을 통합한 consistency 기반 목표로 정책과 가치함수 학습
- **온라인 단계(HIL-ConRFT)**: 오프라인 단계의 손실 구조를 유지하면서 CPQL을 기반으로 task-specific reward로 미세조정
- **Human-in-the-Loop 통합**: 온라인 탐색 중 인간 개입을 통해 안전성 보장 및 샘플 효율성 증대
- **Out-of-Distribution 처리**: 오프라인 단계에서 시연 분포 외 상태에 대한 OOD 처리로 안정적인 초기화
- **Pre-trained VLA 활용**: 기존의 대규모 사전학습된 VLA 모델을 기초로 하여 불필요한 탐색 감소

## Originality

- **Consistency 기반 통합 목표**: BC와 Q-러닝을 CPQL 인사이트로 통합하여 오프라인-온라인 모두에서 일관된 훈련 목표 제시
- **VLA-특화 오프라인-온라인 프레임워크**: 기존 일반적인 오프라인-온라인 RL과 달리, VLA 모델의 사전학습된 표현을 활용한 맞춤형 접근
- **HIL 기반 안전한 온라인 탐색**: 실제 로봇의 안전성과 비용 제약을 고려하여 인간 개입 메커니즘 설계
- **제한된 시연 데이터 활용**: 대규모 다양한 데이터셋 가정 없이 적은 수의 시연으로 효과적인 미세조정 달성

## Limitation & Further Study

- **인간 개입 의존성**: HIL-ConRFT의 온라인 단계가 인간의 개입을 필요로 하므로 완전한 자동화의 한계
- **Task-specific reward 필요**: 각 작업마다 reward 함수를 정의해야 하므로 일반화 가능성 제한
- **실험 범위**: 8개 작업으로 제한되어 더 다양한 도메인에서의 검증 필요
- **비교 연구**: 최신 오프라인-온라인 RL 방법들과의 직접 비교 부족
- **후속 연구**: (1) 인간 개입 없이 안전한 탐색을 위한 메커니즘 개발, (2) 다양한 로봇 플랫폼에서의 일반화, (3) reward 함수의 자동 학습 방법 탐구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ConRFT는 제한된 시연 데이터와 안전 제약이 있는 실제 로봇 환경에서 VLA 모델의 효율적인 미세조정을 위한 실용적이고 혁신적인 솔루션을 제시하며, 높은 성공률과 샘플 효율성으로 로봇 공학에 의미 있는 기여를 한다.

## Related Papers

- 🔗 후속 연구: [[papers/1619_VLA-RFT_Vision-Language-Action_Reinforcement_Fine-tuning_wit/review]] — VLA 모델의 강화학습 기반 파인튜닝에 대한 확장된 접근 방식을 제공합니다.
- 🔄 다른 접근: [[papers/1620_VLA-RL_Towards_Masterful_and_General_Robotic_Manipulation_wi/review]] — VLA-RL을 통한 숙련된 로봇 조작을 위한 다른 강화학습 접근법입니다.
- 🏛 기반 연구: [[papers/1339_Consistency_Policy_Accelerated_Visuomotor_Policies_via_Consi/review]] — ConRFT의 consistency policy 구성요소가 Consistency Policy 방법론을 기반으로 합니다.
- 🔗 후속 연구: [[papers/1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen/review]] — VLA 모델에 특화된 강화학습 미세조정 프레임워크의 구체적 구현을 보여줍니다.
- 🔄 다른 접근: [[papers/1394_FLaRe_Achieving_Masterful_and_Adaptive_Robot_Policies_with_L/review]] — VLA 모델의 강화학습 기반 미세조정에서 다른 consistency-based 접근법을 제시합니다.
- 🔄 다른 접근: [[papers/1513_Parallels_Between_VLA_Model_Post-Training_and_Human_Motor_Le/review]] — 운동 학습 이론 기반 접근과 ConRFT의 강화된 fine-tuning은 서로 다른 VLA 개선 방법론을 제시합니다.
- 🔄 다른 접근: [[papers/1573_SimpleVLA-RL_Scaling_VLA_Training_via_Reinforcement_Learning/review]] — ConRFT와 SimpleVLA-RL은 모두 VLA 모델의 강화학습 기반 fine-tuning을 다루지만 접근 방식이 다릅니다.
- 🔗 후속 연구: [[papers/1620_VLA-RL_Towards_Masterful_and_General_Robotic_Manipulation_wi/review]] — VLA 모델의 reinforced fine-tuning 개념을 scalable RL framework로 확장하여 더 체계적인 VLA-RL 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1619_VLA-RFT_Vision-Language-Action_Reinforcement_Fine-tuning_wit/review]] — contrastive reinforced fine-tuning이 VLA-RFT의 기반 방법론을 제공합니다.
- 🔗 후속 연구: [[papers/1373_DualVLA_Building_a_Generalizable_Embodied_Agent_via_Partial/review]] — ConRFT의 강화 미세조정 방법이 DualVLA의 이중 교사 적응형 증류 전략을 보완하여 action degeneration을 더 효과적으로 해결합니다.
