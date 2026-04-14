# Do You Have Freestyle? Expressive Humanoid Locomotion via Audio Control

> **저자**: Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Tao Huang, Zhenguo Sun, Yibo Peng, Pengwei Wang, Zhongyuan Wang, Fangzhou Liu, Chang Xu, Shanghang Zhang | **날짜**: 2025-12-29 | **URL**: [https://arxiv.org/abs/2512.23650](https://arxiv.org/abs/2512.23650)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1.*

RoboPerform은 오디오를 직접 제어 신호로 사용하여 음악에 맞춰 춤을 추거나 음성에 맞춰 제스처를 생성하는 휴머노이드 로봇 제어 프레임워크로, 명시적 모션 재구성을 제거하여 저지연 및 고충실도를 달성한다.

## Motivation

- **Known**: 기존 휴머노이드 로봇은 사전 정의된 모션이나 희소한 텍스트 명령으로만 제어되며, 오디오-모션 생성 후 retargeting 파이프라인은 cascaded error, 높은 지연시간, 느슨한 음향-구동 매핑을 야기한다.
- **Gap**: 오디오를 implicit style 신호로 직접 활용하여 통합된 모션 생성을 하는 unified framework이 없으며, retargeting 없이 실시간 오디오-모션 정렬을 달성하는 방법이 부족하다.
- **Why**: 휴머노이드 로봇이 음악 및 음성과 같은 리치한 오디오 신호에 반응하는 표현력 있는 성능을 수행할 수 있다면 인간-로봇 상호작용의 자연스러움과 몰입감이 크게 향상될 수 있다.
- **Approach**: motion = content + style 원칙으로 오디오를 implicit style signal로 인코딩하고, ΔMoE teacher policy와 diffusion-based student policy를 통해 content latent와 audio-driven style latent를 분리하여 직접 모션을 생성한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of RoboPerform. We propose a two-stage approach: train an adaptor to inject kinematic information int*

- **First unified audio-to-locomotion framework**: 오디오를 암시적 제어 신호로 활용하는 첫 번째 통합 프레임워크로, 음악-춤과 음성-제스처 양쪽 작업을 지원한다.
- **ΔMoE 교사 정책**: Residual mixture-of-experts 아키텍처로 다양한 모션 패턴을 특화된 전문가들이 처리하며, 동적 가중치 조정을 통해 견고한 모션 추적을 실현한다.
- **Retargeting-free 설계**: 명시적 모션 재구성을 제거하여 cascaded error를 제거하고, 지연시간을 크게 감소시키며, 실시간 성능을 달성한다.
- **물리적 타당성과 오디오 정렬**: 광범위한 실험을 통해 물리적으로 그럴듯한 모션과 높은 오디오 시간 정렬을 동시에 달성함을 입증한다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2. Overview of RoboPerform. We propose a two-stage approach: train an adaptor to inject kinematic information int*

- Audio-motion alignment: InfoNCE loss를 사용하여 temporal attention augmented adaptor로 raw audio latents를 motion latents와 정렬
- ΔMoE teacher policy: 3D conditional inputs를 4개의 nested subspaces로 분할하고 gating network로 residual fusion을 통해 동적 가중치 조정
- Content-style decomposition: Text-to-motion model에서 추출한 high-level content latent와 audio-driven style latent를 분리
- Diffusion-based student policy: Content latent와 temporally-aligned style latent로 guided denoising을 통해 executable actions 생성
- Knowledge distillation: Teacher policy의 지식을 student policy에 증류하여 효율성과 성능 균형

## Originality

- 오디오를 첫 번째 implicit control modality로 활용하는 novel perspective로, 기존 language-guided나 motion-replay 패러다임에서 벗어남
- Motion decomposition (content + style)을 통한 새로운 latent-driven framework로, retargeting-free 설계를 처음으로 audio-driven locomotion에 적용
- ΔMoE의 residual fusion 구조로 기존 orthogonal MoE와 차별화되는 전문가 혼합 방식 제안
- InfoNCE-optimized audio-motion alignment module을 통해 kinematic priors를 audio에 직접 임베딩

## Limitation & Further Study

- 실제 로봇 배포 실험이 논문에 명확히 제시되지 않아 sim-to-real 갭에 대한 검증 필요
- Content와 style의 분리 정도에 따른 성능 변화에 대한 상세 분석 부족
- 복잡한 다중 오디오 신호(음악 + 음성 동시) 처리에 대한 확장성 미검증
- 후속연구: 실제 로봇 플랫폼에서의 제어 안정성 및 일반화 성능 평가, 더 다양한 장르/언어의 오디오에 대한 적응성 강화, visual feedback을 포함한 closed-loop 제어 시스템 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RoboPerform은 오디오 제어 신호를 휴머노이드 로봇 모션에 직접 통합하는 novel한 접근으로, retargeting-free 설계와 content-style decomposition을 통해 저지연 고충실도 실시간 성능을 달성한 의미 있는 기여이다. 다만 실제 로봇 배포 및 sim-to-real 검증이 추가되면 실용성이 더욱 강화될 것이다.
