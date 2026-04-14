# Generative World Modelling for Humanoids: 1X World Model Challenge Technical Report

> **저자**: Riccardo Mereu, Aidan Scannell, Yuxin Hou, Yi Zhao, Aditya Jitta, Antonio Dominguez, Luigi Acerbi, Amos Storkey, Paul Chang | **날짜**: 2025-10-08 | **URL**: [https://arxiv.org/abs/2510.07092](https://arxiv.org/abs/2510.07092)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Overview of the 1X World Model Challenges Left de-*

1X World Model Challenge에서 humanoid 로봇의 미래 상태 예측을 위해 Wan 2.2 TI2V-5B를 video-state-conditioned 프레임 예측으로 적응시키고, Spatio-Temporal Transformer를 압축 트랙용으로 훈련하여 두 트랙 모두에서 1위를 달성했다.

## Motivation

- **Known**: World model은 AI와 로봇공학에서 에이전트가 시각적 관찰이나 compact latent state를 예측함으로써 미래를 추론할 수 있게 한다. 최근 generative model의 발전은 autoregressive transformer와 diffusion-based 접근법을 활용한 강력한 foundation model을 만들었다.
- **Gap**: 실제 humanoid 로봇 상호작용 데이터에 대한 world model의 성능이 충분히 벤치마크되지 않았으며, pixel space 예측과 discrete latent space 예측 사이의 trade-off를 체계적으로 비교한 연구가 부족하다.
- **Why**: World model은 로봇이 직접 상호작용 없이 계획을 수립하고 결과를 예상할 수 있게 하므로, 실제 humanoid 로봇 제어 시스템의 효율성과 안전성을 크게 향상시킬 수 있다.
- **Approach**: Sampling 트랙에서는 Wan 2.2 TI2V-5B의 masking을 수정하여 video-state-conditioned 예측을 구현하고 AdaLN-Zero와 LoRA를 적용했으며, Compression 트랙에서는 discrete token 예측을 위해 Spatio-Temporal Transformer를 처음부터 훈련했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. Overview of the 1X World Model Challenges Left de-*

- **Sampling 트랙 1위**: 23.0 dB PSNR으로 미래 프레임 예측에서 우수한 성능 달성
- **Compression 트랙 1위**: Top-500 CE 6.6386으로 discrete latent code 예측에서 최고 성능 달성
- **Ensemble 기법**: 다중 샘플 예측으로 Gaussian blur보다 우수한 성능 획득
- **Architecture 적응**: Text-image-to-video 모델을 video-state-conditioned 설정으로 효과적으로 재설계

## How

![Figure 2](figures/fig2.webp)

*Figure 2. State conditioning of DiT-Block. Wan2.2 TI2V-5B*

- Sampling 트랙: Wan 2.2 TI2V-5B의 입력 latent masking을 확장하여 여러 프레임을 고정하는 video-to-video 조건화 구현
- State 조건화: 연속 각도와 속도 상태를 sinusoidal feature로 augment한 후 MLP로 projection하고, 1D convolution으로 temporal compression
- AdaLN-Zero: Robot state 특징을 flow matching timestep embedding과 결합하여 DiT block의 30개 계층에서 modulation 적용
- LoRA fine-tuning: Rank 32의 LoRA를 Wan 2.2 DiT backbone에 적용하여 효율적인 적응
- Ensemble inference: 예측 불확실성을 활용하여 최대 100개의 샘플을 평균화하여 PSNR 개선
- Compression 트랙: Cosmos 8×8×8 tokenizer로 인코딩된 discrete latent code의 top-500 cross-entropy 최소화를 위한 Spatio-Temporal Transformer 훈련

## Originality

- Text-image-to-video 모델을 robot state 조건화가 가능한 video-state-conditioned 예측 모델로 창의적으로 변환
- AdaLN-Zero 메커니즘을 robot state 특징과 flow matching timestep embedding의 결합으로 확장하여 시간-공간적 modulation 실현
- Gaussian blur 기반 post-processing보다 ensemble 기반 불확실성 활용이 우수함을 실증적으로 입증
- Pixel space와 discrete latent space 두 가지 상이한 예측 패러다임을 동시에 해결하는 통합적 접근

## Limitation & Further Study

- Ensemble 기반 추론은 단일 샘플 추론보다 계산 비용이 높아 실시간 로봇 제어 응용에 제약 가능성
- PSNR 메트릭의 한계로 인해 blur 효과가 선호되는 경향이 있으며, 실제 로봇 제어 성능과의 correlation이 명확하지 않음
- State 조건화의 temporal compression이 robot state의 동적 정보를 어느 정도 손실할 수 있음
- 후속 연구: 실시간성과 성능의 trade-off를 최적화하는 경량 ensemble 기법 개발, 로봇 제어 태스크에서의 world model 성능 검증, 더 긴 예측 horizon에 대한 성능 평가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 대규모 foundation model을 robot state 조건화로 효과적으로 적응시키고, pixel space와 discrete latent space에서 모두 최고 성능을 달성함으로써 실제 humanoid 로봇 world modeling의 새로운 벤치마크를 제시했다. 방법론의 명확한 설명과 포괄적인 ablation study는 향후 world model 연구에 큰 기여가 될 것으로 예상된다.
