# Zero-Shot Whole-Body Humanoid Control via Behavioral Foundation Models

> **저자**: Andrea Tirinzoni, Ahmed Touati, Jesse Farebrother, Mateusz Guzek, Anssi Kanervisto, Yingchen Xu, Alessandro Lazaric, Matteo Pirotta | **날짜**: 2025-04-15 | **URL**: [https://arxiv.org/abs/2504.11054](https://arxiv.org/abs/2504.11054)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 META MOTIVO is the first behavioral foundation model for humanoid agents that can solve whole-body control task*

FB-CPR (Forward-Backward Representations with Conditional-Policy Regularization) 알고리즘을 통해 관찰-전용 모션캡처 데이터로 정규화된 unsupervised RL을 수행하여, 제로샷으로 모션추적, 목표도달, 보상최적화 등 다양한 전신 휴머노이드 제어 작업을 수행 가능한 첫 번째 behavioral foundation model인 Meta Motivo를 개발했다.

## Motivation

- **Known**: Foundation model은 대규모 unlabeled 데이터로 사전학습되어 다양한 downstream task를 프롬프트 기반으로 해결할 수 있다. 기존 unsupervised RL과 sequence model 기반 접근법은 복잡한 환경에서 또는 작업 범용성에서 제약이 있다.
- **Gap**: Zero-shot RL은 unsupervised 손실과 downstream task 간 상관성이 낮아 고차원 불안정 시스템에서 성능이 떨어지고, imitation 기반 방법은 dataset에 국한된 행동만 재현할 수 있으며, regularized policy 접근은 여전히 downstream task별 학습이 필요하다.
- **Why**: 휴머노이드 전신 제어는 높은 차원성과 고유한 불안정성으로 인해 오래되고 도전적인 문제이며, 범용적 행동 기초 모델을 확보하면 로봇공학, 가상 아바타, NPC 생성 등에 혁신적 가치를 제공할 수 있다.
- **Approach**: Forward-backward representation의 latent space에 unlabeled trajectory를 임베딩하고, latent-conditional discriminator를 통해 정책이 dataset의 상태를 커버하도록 유도하는 동시에 zero-shot 일반화 능력을 유지하도록 설계했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1 META MOTIVO is the first behavioral foundation model for humanoid agents that can solve whole-body control task*

- **FB-CPR 알고리즘 제안**: Forward-backward representation과 conditional policy regularization을 결합하여 unlabeled behavior dataset으로부터 학습하면서 zero-shot 일반화를 보존하는 novel unsupervised RL 방법 개발
- **Meta Motivo 구현**: AMASS 모션캡처 데이터로 학습된 SMPL 기반 휴머노이드 behavioral foundation model이 motion tracking, goal reaching, reward optimization을 제로샷으로 해결 가능
- **경쟁력 있는 성능**: task-specific 방법과 비교 가능한 성능을 달성하면서 state-of-the-art unsupervised RL 및 model-based baseline을 능가
- **인간다운 행동**: 학습된 모델이 human-like behavior를 표현하고 SMPL skeleton의 자연스러운 동역학을 활용
- **재현성 보장**: 환경, 코드, 사전학습 모델을 공개하여 재현성 및 후속 연구 지원

## How

![Figure 2](figures/fig2.webp)

*Figure 2 Illustration of the main components of FB-CPR: the discriminator is trained to estimate the ratio between the l*

- Successor measure M^π(X|s,a)를 저랭크 분해로 근사하는 Forward-Backward representation 활용: M^π(X|s,a) ≈ ∫_{s'∈X} F^π(s,a)^T B(s') ρ(ds')", 'Forward F와 backward B embedding을 temporal difference loss L_FB로 학습하여 Bellman residual 최소화
- Task encoding vector z를 통해 정책 π_z와 forward/backward embedding을 jointly 파라미터화
- Latent-conditional discriminator를 도입하여 policy가 unlabeled dataset의 상태 분포를 커버하도록 강제 정규화
- AMASS 모션캡처 데이터의 trajectory를 동일한 latent space에 임베딩하여 행동 기반 정보 활용
- Actor network를 통해 continuous action space에서 arg max를 근사: L_actor(π) = -E[F(s,a,z)^T z]
- SMPL skeleton 기반 휴머노이드에 대해 proprioceptive observation만으로 전신 제어 학습
- Zero-shot inference: 임의의 reward 함수 r에 대해 Q^π_r(s,a) = F(s,a,z)^T z로 정책 평가 및 최적화

## Originality

- **Unlabeled behavior dataset 활용의 혁신**: Observation-only 모션캡처 데이터를 unsupervised RL에 직접 통합하기 위해 forward-backward representation을 활용한 최초의 접근
- **Latent-conditional discriminator 설계**: 정책이 dataset 상태를 커버하도록 하면서도 zero-shot 일반화를 보존하는 새로운 정규화 메커니즘
- **Behavioral foundation model 개념의 구체화**: Language/vision foundation model의 패러다임을 embodied agent의 whole-body control로 확장한 첫 사례
- **Successor measure 기반 multitask learning**: 측도 기반 정책 표현으로 다양한 task (추적, 목표도달, 보상최적화)를 단일 모델에서 해결
- **AMASS와 SMPL의 통합**: 대규모 비정제 모션캡처 데이터와 인체 골격 모델을 활용하여 scale-up된 학습 달성

## Limitation & Further Study

- **Computational cost**: Online unsupervised RL + imitation 학습으로 인한 계산량 증가에 대한 명시적 비용 분석 부재
- **Dataset quality dependency**: AMASS 데이터셋의 bias나 coverage 제약이 학습된 행동에 미치는 영향에 대한 심도 있는 분석 부재
- **Task generalization 범위**: Bipedal walker, ant maze 외 다른 환경에서의 성능 및 확장성에 대한 평가 제한적
- **Discriminator 설계 선택사항**: Latent-conditional discriminator의 구체적 구조, 학습률, 손실 가중치 등에 대한 민감성 분석 부재
- **Real robot 검증 부재**: 모든 평가가 simulation 환경 내에서만 수행되어 실제 로봇 적용 가능성 미검증
- **후속 연구 방향**: (1) 다양한 morphology (사족보행, 손가락 제어)로의 확장, (2) 상이한 modality (RGB, tactile)의 통합, (3) Online interaction 환경에서의 adaptation 메커니즘

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 forward-backward representation을 unlabeled 행동 데이터와 결합하여 behavioral foundation model을 구현한 혁신적 작업으로, humanoid 제어의 zero-shot 일반화 문제를 실질적으로 해결했다. 기술적 견고성, 광범위한 실험 검증, 재현성 지원을 통해 embodied AI 분야에 중요한 기여를 제시하지만, 실로봇 검증과 확장성 분석에서 개선의 여지가 있다.
