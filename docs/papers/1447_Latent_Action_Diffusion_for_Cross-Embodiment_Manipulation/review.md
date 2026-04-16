---
title: "1447_Latent_Action_Diffusion_for_Cross-Embodiment_Manipulation"
authors:
  - "Erik Bauer"
  - "Elvis Nava"
  - "Robert K. Katzschmann"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇의 다양한 end-effector 간 action space 이질성을 극복하기 위해 contrastive learning으로 학습된 shared latent action space에서 diffusion policy를 학습하여 cross-embodiment 조작을 실현한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Dexterous_Spatial_Grasping"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bauer et al._2025_Latent Action Diffusion for Cross-Embodiment Manipulation.pdf"
---

# Latent Action Diffusion for Cross-Embodiment Manipulation

> **저자**: Erik Bauer, Elvis Nava, Robert K. Katzschmann | **날짜**: 2025-06-17 | **URL**: [https://arxiv.org/abs/2506.14608](https://arxiv.org/abs/2506.14608)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview of our approach. Left: We construct a semantically aligned latent action space by training modality-spe*

로봇의 다양한 end-effector 간 action space 이질성을 극복하기 위해 contrastive learning으로 학습된 shared latent action space에서 diffusion policy를 학습하여 cross-embodiment 조작을 실현한다.

## Motivation

- **Known**: 최근 cross-embodiment 학습 연구들은 공유 action space를 사용하거나 human-to-robot retargeting에 의존하고 있으나, 이러한 접근은 다양한 end-effector의 복잡한 action space를 효과적으로 활용하지 못하고 있다.
- **Gap**: dexterous hand와 parallel gripper 같은 이질적인 end-effector들의 action space를 통일하면서도 각 embodiment 특성을 보존하여 단일 정책으로 다중 로봇을 제어하고 skill transfer를 달성하는 방법이 부재하다.
- **Why**: 로봇 학습의 데이터 부족 문제를 해결하기 위해 heterogeneous embodiment 간 데이터 공유가 필수적이며, 이를 통해 새로운 로봇 morphology 추가 시 요구되는 데이터 수집과 재학습 비용을 대폭 감소시킬 수 있다.
- **Approach**: Retargeting으로 생성된 aligned action pair를 contrastive loss로 학습된 embodiment-specific encoder들을 통해 공유 latent space로 투영하고, 이 latent space에서 embodiment-agnostic diffusion policy를 훈련한 후 embodiment-specific decoder로 디코딩한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: Success rates for three different tasks comparing single-embodiment diffusion policies to cross-embodied latent*

- **Semantically aligned latent action space 학습**: Contrastive learning을 이용하여 anthropomorphic robotic hand, human hand, parallel jaw gripper의 action을 단일 latent space로 통합
- **Cross-embodiment 정책 학습**: Latent diffusion policy 기반으로 단일 정책이 다양한 embodiment을 제어 가능하도록 구현
- **성능 향상**: Co-training을 통해 단일 embodiment 정책 대비 최대 25.3% (평균 13.4%) 조작 성공률 개선 달성
- **실용적 확장성**: 새로운 로봇 morphology 추가 시 광범위한 데이터 수집 불필요, embodiment 간 generalization 가속화

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: The three-stage process for learning the cross-embodiment latent action space. Stage 1: Aligned end-effector (EE*

- **Aligned action pair 생성**: Human hand pose를 retargeting 휴리스틱과 energy-based 방법으로 다양한 robot end-effector pose로 변환
- **Stage 1 - Encoder 훈련**: Contrastive loss를 통해 embodiment-specific encoder를 학습하여 paired action을 shared latent space로 매핑
- **Stage 2 - Decoder 훈련**: L2 reconstruction loss로 decoder를 훈련하여 latent 표현에서 원래 action 복원 가능하게 구현
- **Stage 3 - Fine-tuning**: Encoder를 reconstruction 품질 개선을 위해 미세조정
- **Diffusion policy 학습**: 학습된 latent space에서 embodiment-agnostic diffusion policy를 co-training으로 학습
- **Multi-robot control**: 훈련된 policy와 각 embodiment별 decoder 조합으로 단일 policy로 여러 로봇 제어

## Originality

- **Multimodal representation learning 프레임워크 적용**: Robot action space 정렬 문제를 multimodal alignment 문제로 재정의하여 contrastive learning 활용
- **Retargeting 기반 alignment prior**: 기존 retargeting 방법을 alignment의 initialization으로 활용하되, learned latent space에서의 semantic alignment 달성
- **Any-to-any reconstruction**: 일방향 human-to-robot retargeting과 달리 latent space에서 임의의 embodiment 간 action 변환 가능
- **Factorized policy 아키텍처**: Embodiment-agnostic policy와 embodiment-specific decoder 분리로 확장성과 재사용성 향상

## Limitation & Further Study

- **제한된 embodiment 범위**: 실험이 single-arm robot with different end-effector로 제한되어, multi-arm이나 완전히 다른 morphology(예: 다리를 가진 로봇)로의 확장 검증 부재
- **Retargeting 품질 의존성**: Latent space alignment 초기화가 retargeting 품질에 의존하므로, retargeting이 부정확한 경우 성능 저하 가능성
- **Semantic alignment 검증 부족**: Learned latent space의 semantic alignment가 충분한지에 대한 정량적 평가 및 시각화 자료 제한적
- **Cross-embodiment skill transfer의 한계 분석 부재**: 25.3% 성능 향상이 embodiment 간 차이의 크기에 따라 어떻게 변하는지 체계적 분석 부족
- **Real-world 배포 고려사항 부재**: Latent space의 안정성, 노이즈 로버스트성, sim-to-real transfer에 대한 논의 미흡
- **후속 연구 방향**: (1) 더 이질적인 embodiment(예: 인간형 vs 이족 로봇) 간 transfer 검증, (2) Retargeting 불가능한 embodiment에 대한 alignment 방법 개발, (3) Unsupervised alignment 방식 탐색

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Cross-embodiment 로봇 학습의 action space 이질성 문제를 learned latent representation으로 우아하게 해결하고, contrastive learning과 diffusion policy를 조합하여 실제 성능 향상을 입증한 가치있는 연구이다. 다만 embodiment 다양성 범위 확대와 alignment 메커니즘의 더 깊은 분석이 후속 과제이다.

## Related Papers

- 🔄 다른 접근: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — 둘 다 cross-embodiment 학습이지만 Latent Action Diffusion은 latent space에, Scaling 논문은 정책 통합에 집중한다.
- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — diffusion policy의 기본 아이디어가 latent action space에서의 cross-embodiment 정책 학습에 적용되었다.
- 🔗 후속 연구: [[papers/1601_UniSkill_Imitating_Human_Videos_via_Cross-Embodiment_Skill_R/review]] — cross-embodiment skill 학습을 latent diffusion으로 더 정교하게 구현한 발전된 형태다.
- 🏛 기반 연구: [[papers/1331_CLASS_Contrastive_Learning_via_Action_Sequence_Supervision_f/review]] — contrastive learning을 통한 행동 표현 학습의 기본 원리를 cross-embodiment manipulation에 적용하는 토대를 제공한다.
- 🔄 다른 접근: [[papers/1475_MetaMorph_Learning_Universal_Controllers_with_Transformers/review]] — 둘 다 다양한 로봇 형태에 대한 일반화를 다루지만 latent action space와 universal controller의 접근법 차이를 비교할 수 있다.
- 🔄 다른 접근: [[papers/1475_MetaMorph_Learning_Universal_Controllers_with_Transformers/review]] — 둘 다 cross-embodiment learning을 다루지만 universal controller와 latent action diffusion의 접근법 차이를 비교할 수 있다.
- 🏛 기반 연구: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — cross-embodiment manipulation의 이론적 기반이 CrossFormer의 다중 로봇 제어에 적용된다.
- 🔄 다른 접근: [[papers/1633_X-VLA_Soft-Prompted_Transformer_as_Scalable_Cross-Embodiment/review]] — Cross-embodiment manipulation을 latent action diffusion으로 해결하는 다른 접근법이다.
- 🏛 기반 연구: [[papers/1328_Chain-of-Action_Trajectory_Autoregressive_Modeling_for_Robot/review]] — latent action diffusion의 궤적 표현 개념이 chain-of-action의 역방향 모델링 설계 기반
- 🏛 기반 연구: [[papers/1330_CLAM_Continuous_Latent_Action_Models_for_Robot_Learning_from/review]] — Latent Action Diffusion의 latent action space 개념을 continuous space에서 unlabeled observation data로부터의 학습으로 확장한 방법론입니다.
