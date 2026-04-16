---
title: "1330_CLAM_Continuous_Latent_Action_Models_for_Robot_Learning_from"
authors:
  - "Anthony Liang"
  - "Pavel Czempin"
  - "Matthew Hong"
  - "Yutai Zhou"
  - "Erdem Biyik"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "CLAM은 라벨이 없는 관찰 데이터로부터 로봇 정책을 학습하기 위해 continuous latent action space를 사용하며, action decoder를 jointly training하여 실제 환경 액션으로의 grounding을 보장하는 방법을 제안한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liang et al._2025_CLAM Continuous Latent Action Models for Robot Learning from Unlabeled Demonstrations.pdf"
---

# CLAM: Continuous Latent Action Models for Robot Learning from Unlabeled Demonstrations

> **저자**: Anthony Liang, Pavel Czempin, Matthew Hong, Yutai Zhou, Erdem Biyik, Stephen Tu | **날짜**: 2025-05-08 | **URL**: [https://arxiv.org/abs/2505.04999](https://arxiv.org/abs/2505.04999)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of CLAM. CLAM consists of a latent inverse dynamics model, fϕ, which in-*

CLAM은 라벨이 없는 관찰 데이터로부터 로봇 정책을 학습하기 위해 continuous latent action space를 사용하며, action decoder를 jointly training하여 실제 환경 액션으로의 grounding을 보장하는 방법을 제안한다.

## Motivation

- **Known**: Imitation learning은 대규모의 비용이 많이 드는 action-labeled expert demonstrations을 요구하며, self-supervised inverse dynamics models를 통해 observation-only 데이터에서 latent action labels를 학습하는 접근이 제안되어왔다.
- **Gap**: 기존 방법들은 discrete action representations을 사용하거나 action decoder를 독립적으로 학습하여 continuous control tasks에서 세밀한 동작이 필요한 복잡한 로봇 작업에 대응하기 어렵다.
- **Why**: 로봇 정책 학습을 위한 비용이 많이 드는 expert demonstrations 수집의 병목을 해결하고, 인터넷 규모의 대량 unlabeled video 데이터를 효과적으로 활용하기 위해 중요하다.
- **Approach**: CLAM은 latent inverse/forward dynamics models를 self-supervised objective로 pretrain하고, continuous latent action space를 유지하면서 action decoder를 jointly training하여 non-expert play data만으로도 latent actions을 실제 액션으로 grounding할 수 있게 한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: MetaWorld Image-Based Experiments. Task success rate over 50 evaluation rollouts*

- **Continuous latent actions**: discrete representations 대신 continuous latent action space 사용으로 fine-grained robot control tasks에서 우월한 성능 달성
- **Joint training**: latent action model과 action decoder의 joint training으로 downstream policy 성능이 2-3배 향상
- **Non-expert grounding data**: expert demonstrations 없이 random 또는 play data만으로 학습 가능하여 데이터 수집 비용 대폭 감소
- **Comprehensive evaluation**: DMControl, MetaWorld 벤치마크 및 실제 WidowX robot arm에서 prior state-of-the-art methods 대비 2-3배 task success rate 향상

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of CLAM. CLAM consists of a latent inverse dynamics model, fϕ, which in-*

- Stage 1: Latent Action Model (LAM) pretraining - latent IDM과 latent FDM을 future observation reconstruction loss (L_recon)로 jointly train
- Information bottleneck을 통한 meaningful action representation 학습 - encoder/decoder 아키텍처로 shortcut solutions 방지
- Continuous latent action space 유지 - Vector Quantization 대신 learned continuous action space 사용
- Joint action decoder training - unlabeled data의 reconstruction loss (L_recon)와 labeled data의 action decoder loss (L_action-decoder)를 번갈아 최적화하여 latent space regularity 보장
- Stage 2: Latent action policy training - pretrained latent IDM으로 unlabeled expert data에 pseudo-action labels 할당 후, latent action policy π_θ를 imitation learning으로 학습
- Feature reuse - pretrained IDM의 image encoder features를 policy training에 활용

## Originality

- 기존 discrete latent action 방식에서 continuous 방식으로의 근본적 전환으로 continuous control tasks의 fine-grained motion 표현 가능
- Latent action model과 action decoder의 joint training 패러다임 도입 - 독립적 training의 한계를 극복하는 새로운 정규화 기법
- Expert 데이터 없이 random/play data만으로 grounding 가능한 scalable framework 제시 - 데이터 수집의 현실적 제약 해결
- Self-supervised latent space learning과 supervised action decoding의 효과적 결합으로 unlabeled 데이터의 가치 극대화

## Limitation & Further Study

- Single-task, single-embodiment 설정으로 제한되어 있으며, 실제 in-the-wild YouTube 영상과 같은 다양한 소스의 영상 활용은 미래 과제로 남음
- Latent action space 학습에 필수적으로 일부 expert 데이터 (D_unlabeled-expert)가 포함되어야 하므로 완전한 unlabeled 설정은 아님
- Action decoder training을 위해 별도의 labeled data (D_labeled)가 필요하며, 이 데이터의 최소 규모 및 최적 수집 방식에 대한 상세 분석 부족
- Context window H 등 여러 하이퍼파라미터의 민감도 분석 및 자동 선택 방법 제시 필요
- Cross-task, cross-embodiment 전이 학습(transfer learning) 가능성에 대한 검토 부재 - 기초 모델 관점에서의 확장성 제한

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: CLAM은 continuous latent action space와 joint decoder training이라는 명확한 기술적 혁신으로 unlabeled 데이터 기반 로봇 정책 학습의 실질적 성능을 획기적으로 향상시키며, 비용이 많이 드는 expert 데이터 수집의 필요성을 크게 감소시키는 highly significant contribution을 제시한다.

## Related Papers

- 🏛 기반 연구: [[papers/1447_Latent_Action_Diffusion_for_Cross-Embodiment_Manipulation/review]] — Latent Action Diffusion의 latent action space 개념을 continuous space에서 unlabeled observation data로부터의 학습으로 확장한 방법론입니다.
- 🔗 후속 연구: [[papers/1453_Learning_Latent_Plans_from_Play/review]] — Learning Latent Plans from Play의 라벨 없는 학습 개념을 continuous latent action space와 joint training을 통한 실제 환경 grounding으로 발전시킨 연구입니다.
- 🔄 다른 접근: [[papers/1480_Moto_Latent_Motion_Token_as_the_Bridging_Language_for_Learni/review]] — 둘 다 latent action modeling을 다루지만 CLAM은 continuous latent space에, Moto는 latent motion token에 중점을 둡니다.
- 🔄 다른 접근: [[papers/1453_Learning_Latent_Plans_from_Play/review]] — 둘 다 연속적인 행동 학습이지만 Play-LMP는 잠재 계획에, CLAM은 연속 잠재 행동에 집중한다.
- 🏛 기반 연구: [[papers/1354_Dex1B_Learning_with_1B_Demonstrations_for_Dexterous_Manipula/review]] — 연속 잠재 행동 모델 CLAM이 Dex1B의 생성 모델 기반 시연 생성에 이론적 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1316_Behavior_Transformers_Cloning_k_modes_with_one_stone/review]] — 연속 잠재 행동 모델 CLAM이 BeT의 action discretization에 이론적 기반을 제공합니다.
