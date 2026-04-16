---
title: "1620_VLA-RL_Towards_Masterful_and_General_Robotic_Manipulation_wi"
authors:
  - "Guanxing Lu"
  - "Wenkai Guo"
  - "Chubin Zhang"
  - "Yuheng Zhou"
  - "Haonan Jiang"
date: "2025.05"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 사전학습된 Vision-Language-Action(VLA) 모델을 강화학습(RL)으로 개선하여 로봇 조작 작업의 분포 외(OOD) 시나리오 대응력을 향상시키는 VLA-RL 프레임워크를 제시한다. 궤적 수준의 RL 공식화와 robotic process reward model을 통해 LIBERO 벤치마크에서 OpenVLA-7B의 성능을 4.5% 향상시킨다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Lu et al._2025_VLA-RL Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning.pdf"
---

# VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning

> **저자**: Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, Ziwei Wang | **날짜**: 2025-05-24 | **URL**: [https://arxiv.org/abs/2505.18719](https://arxiv.org/abs/2505.18719)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Previous VLAs focus on imitation learning that exploits the offline demonstrations, while VLA-RL ex-*

본 논문은 사전학습된 Vision-Language-Action(VLA) 모델을 강화학습(RL)으로 개선하여 로봇 조작 작업의 분포 외(OOD) 시나리오 대응력을 향상시키는 VLA-RL 프레임워크를 제시한다. 궤적 수준의 RL 공식화와 robotic process reward model을 통해 LIBERO 벤치마크에서 OpenVLA-7B의 성능을 4.5% 향상시킨다.

## Motivation

- **Known**: 최근 대규모 VLA 모델들은 인간 시연 모방을 통해 다양한 로봇 조작 작업에서 우수한 성능을 보였으나, 오프라인 데이터의 제한된 상태 방문으로 인해 테스트 시 OOD 시나리오에서 실패한다. LLM에 RL을 적용하는 것이 추론 성능 향상에 효과적임이 증명되었다.
- **Gap**: 기존 로봇 RL은 처음부터 학습하거나 간단한 도메인에만 적용되었으며, 대규모 기초 모델을 활용한 궤적 수준의 온라인 RL과 일반적인 멀티태스크 로봇 조작의 결합이 충분히 탐구되지 않았다.
- **Why**: 로봇 조작의 일반화 능력 향상은 실제 로봇 배포의 핵심 과제이며, LLM의 RL 성공을 로봇 도메인으로 확장하면 테스트 타임 스케일링과 추론 계산 이점을 얻을 수 있다.
- **Approach**: VLA-RL은 로봇 조작 궤적을 다중모달 다중턴 대화로 모델링하고, 자동 추출된 작업 세그먼트에서 생성된 의사 보상 레이블로 학습된 robotic process reward model을 통해 희소 보상 문제를 해결하며, 커리큘럼 선택, GPU 균형 환경, 배치 디코딩, critic warmup 등 구현 최적화를 적용한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Test-time Scaling Curve. We evaluate the fine-tuned OpenVLA-7B every 2500 training steps on the*

- **성능 향상**: OpenVLA-7B를 LIBERO의 40개 도전적인 로봇 조작 작업에서 76.3%에서 81.0%로 4.5% 개선하여 π0-FAST 같은 상용 모델 수준 달성
- **테스트 타임 스케일링**: 테스트 시 최적화 단계 증가에 따른 일관된 성능 향상(75%→85%)으로 로봇 도메인에서의 추론 스케일링 법칙 초기 증거 제시
- **일반화 프레임워크**: 다중모달 다중턴 대화 공식화를 통해 LLM RL 기법을 로봇 도메인에 체계적으로 적용하는 통일된 관점 제공
- **안정적 구현**: curriculum selection, GPU-balanced vectorized environments, batch decoding, critic warmup 등 실무적 개선사항으로 RL 훈련의 안정성 및 효율성 향상

## How

![Figure 2](figures/fig2.webp)

*Figure 2: The overall pipeline of VLA-RL, which is composed of a transformer-based policy, a homogeneous*

- auto-regressive VLA(OpenVLA-7B 기반)의 trajectory-level RL 공식화로 로봇 조작을 다중모달 다중턴 대화로 모델링
- vision-language model을 fine-tuning한 robotic process reward model(rPRM) 구축으로 자동 추출 작업 세그먼트의 의사 보상 라벨로 희소 보상 문제 해결
- PPO 기반 정책 최적화에 policy network와 value network를 LoRA 어댑터로 구현
- N개 병렬 환경에서 M 스텝 궤적 수집 후 GAE(Generalized Advantage Estimation)로 보상 계산
- curriculum selection 전략으로 훈련 데이터 선택 최적화
- GPU 워커 간 로드 밸런싱된 벡터화 환경으로 효율성 증대
- 배치 디코딩과 critic warmup으로 훈련 안정성 개선

## Originality

- 로봇 조작 궤적을 다중모달 다중턴 대화로 공식화한 혁신적 관점으로 LLM RL 기법의 로봇 적용 확장
- 일반적인 로봇 기초 모델의 온라인 RL fine-tuning 최초 체계적 탐구로 기존 단일 태스크나 단순 도메인 RL의 한계 돌파
- 자동 작업 세그먼트 추출 기반 의사 보상 라벨 생성 방식으로 비용이 많이 드는 보상 엔지니어링 회피
- 테스트 타임 계산 증가에 따른 성능 향상의 구체적 실증으로 로봇 도메인 추론 스케일링의 초기 증거 제시

## Limitation & Further Study

- LIBERO 시뮬레이션 환경에서만 평가되어 실물 로봇 환경으로의 일반화 가능성 미검증
- OpenVLA-7B에만 적용되어 다른 VLA 모델(Open X-Embodiment 등)에 대한 일반성 미확인
- rPRM의 의사 보상 라벨 자동 생성 과정의 정확도와 그에 따른 성능 상한에 대한 분석 부족
- 테스트 타임 스케일링의 계산 비용-성능 트레이드오프 분석 미흡
- 후속 연구: 실물 로봇 배포 실험, 다양한 VLA 모델 적용, rPRM 품질 개선 방법론 연구, 계산 효율성과 성능의 최적화 방안 탐색

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 LLM RL의 성공 사례를 로봇 도메인으로 창의적으로 확장하여 대규모 VLA 모델의 온라인 학습을 가능하게 하는 체계적인 프레임워크를 제시한다. LIBERO에서의 의미 있는 성능 향상과 테스트 타임 스케일링 증거는 로봇 학습의 새로운 방향을 제시하지만, 실물 로봇 검증이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1573_SimpleVLA-RL_Scaling_VLA_Training_via_Reinforcement_Learning/review]] — 둘 다 VLA와 RL의 결합을 다루지만 SimpleVLA-RL은 단순화된 접근에, VLA-RL은 궤적 수준 RL에 집중합니다.
- 🔗 후속 연구: [[papers/1338_ConRFT_A_Reinforced_Fine-tuning_Method_for_VLA_Models_via_Co/review]] — VLA 모델의 reinforced fine-tuning 개념을 scalable RL framework로 확장하여 더 체계적인 VLA-RL 접근법을 제시합니다.
- 🏛 기반 연구: [[papers/1516_Plan-Seq-Learn_Language_Model_Guided_RL_for_Solving_Long_Hor/review]] — language model guided RL의 기본 개념을 제공하여 VLA-RL의 언어 조건부 강화학습에 이론적 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1619_VLA-RFT_Vision-Language-Action_Reinforcement_Fine-tuning_wit/review]] — 둘 다 VLA 모델의 강화학습 개선을 다루지만, VLA-RL은 OOD 대응력을, VLA-RFT는 world model 효율성에 집중한다.
- 🏛 기반 연구: [[papers/1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen/review]] — VLA 모델의 강화학습 통합에 대한 통일된 프레임워크를 제공하여 VLA-RL의 방법론적 토대를 마련한다.
- 🔗 후속 연구: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — Octo의 일반적인 로봇 정책을 강화학습으로 개선하여 분포 외 시나리오에서의 성능 향상을 달성한다.
- 🔗 후속 연구: [[papers/1394_FLaRe_Achieving_Masterful_and_Adaptive_Robot_Policies_with_L/review]] — VLA-RL은 FLaRe의 BC-to-RL 파이프라인을 VLA 모델에 특화하여 발전시킨 연구입니다.
- 🔄 다른 접근: [[papers/1532_RLinf-VLA_A_Unified_and_Efficient_Framework_for_Reinforcemen/review]] — RLinf-VLA와 VLA-RL은 모두 VLA 모델의 강화학습 적용을 다루지만 훈련 효율성과 일반적 성능 향상이라는 다른 초점을 가진다.
- 🔗 후속 연구: [[papers/1619_VLA-RFT_Vision-Language-Action_Reinforcement_Fine-tuning_wit/review]] — VLA-RL이 VLA-RFT의 강화 학습 파인튜닝 아이디어를 더 일반적이고 숙련된 로봇 조작으로 확장한다.
- 🔄 다른 접근: [[papers/1338_ConRFT_A_Reinforced_Fine-tuning_Method_for_VLA_Models_via_Co/review]] — VLA-RL을 통한 숙련된 로봇 조작을 위한 다른 강화학습 접근법입니다.
- 🔄 다른 접근: [[papers/1411_GR-RL_Going_Dexterous_and_Precise_for_Long-Horizon_Robotic_M/review]] — VLA 모델의 RL 기반 미세조정에서 다른 방법론적 접근을 제시합니다.
