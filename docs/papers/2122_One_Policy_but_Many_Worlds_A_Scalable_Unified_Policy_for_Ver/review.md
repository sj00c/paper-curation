# One Policy but Many Worlds: A Scalable Unified Policy for Versatile Humanoid Locomotion

> **저자**: Yahao Fan, Tianxiang Gui, Kaiyang Ji, Shutong Ding, Chixuan Zhang, Jiayuan Gu, Jingyi Yu, Jingya Wang, Ye Shi | **날짜**: 2025-05-24 | **URL**: [https://arxiv.org/abs/2505.18780](https://arxiv.org/abs/2505.18780)

---

## Essence

![Figure 2](figures/fig2.webp)

*Figure 2: Framework of DreamPolicy. The system is decomposed into two parts: (1) Terrain-aware*

DreamPolicy는 Humanoid Motion Imagery (HMI)를 생성하는 terrain-aware autoregressive diffusion planner와 HMI-conditioned RL policy를 결합하여, 단일 정책으로 다양한 지형에서 humanoid 로봇의 이동을 학습하고 미지의 시나리오로 zero-shot 일반화를 달성하는 통합 프레임워크이다.

## Motivation

- **Known**: 기존 humanoid 이동 제어는 task-specific reward 설계에 의존하며 특정 training 조건에 overfitting되는 경향이 있고, policy distillation 방식도 구성 전문가의 brittleness를 상속받는다.
- **Gap**: 전통적인 RL은 증가하는 데이터셋을 효과적으로 활용하지 못하고, 다양한 지형과 external disturbance에 대한 견고한 일반화 능력이 부족하며, 수동 reward engineering의 필요성이 있다.
- **Why**: Humanoid 로봇이 다양한 환경에서 robust하고 자연스러운 이동을 수행해야 하는데, 확장 가능하면서도 reward engineering을 제거한 통합 정책이 필요하다.
- **Approach**: 전문화된 RL 정책들로부터 수집한 offline humanoid kinematic 데이터로 autoregressive diffusion planner를 학습하여 terrain-adaptive 궤적을 생성하고, 이를 dynamic objective로 삼아 HMI-conditioned RL 정책을 최적화한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Comparison in Single terrain*

- **Cross-Terrain 일반화**: 단 6개의 single-terrain에서만 학습했음에도 training 환경에서 평균 90% 성공률, 미지의 지형에서는 기존 방법 대비 평균 20% 높은 성공률 달성
- **Scalable 데이터 활용**: Dataset이 확대될수록 diffusion prior가 더 풍부한 이동 기술을 학습하여 정책이 retraining 없이 새로운 지형 습득 가능
- **Manual Reward Engineering 제거**: HMI를 implicit, terrain-adaptive reward signal로 사용하여 복잡한 reward 설계 필요 없음
- **Robustness**: Perturbed 및 composite scenario에서 기존 방법이 실패할 때도 강건한 성능 유지

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Framework of DreamPolicy. The system is decomposed into two parts: (1) Terrain-aware*

- **Stage 1 - Primitive Skills Collection**: 6개의 구별되는 지형에서 전문화된 RL 정책 학습 및 대규모 시뮬레이션을 통한 diverse humanoid kinematic dataset 수집
- **Stage 2 - Diffusion Planner 학습**: Collected dataset에서 autoregressive diffusion model을 학습하여 cross-scenario state-action distribution을 모델링하고 물리적으로 타당한 궤적 합성 가능
- **Stage 3 - HMI-Conditioned RL 정책 최적화**: Diffusion planner의 예측을 dynamic objective로 사용하여 physics-constrained RL 정책을 학습, 궤적 추적 정확도와 물리적 현실성 균형
- **Decoupled Architecture**: Motion synthesis와 policy optimization을 분리하여 dataset 확장을 통한 지속적인 개선 가능

## Originality

- **Native Humanoid Kinematics**: Human motion dataset 재targeting 대신 humanoid-native kinematic을 직접 수집하여 terrain-specific physical constraint를 자연스럽게 인코딩
- **Terrain-aware Autoregressive Diffusion Planner**: 단순 trajectory generation을 넘어 terrain 정보를 조건으로 하는 autoregressive diffusion을 통해 adaptive motion imagery 생성
- **Implicit Reward Signaling via HMI**: Diffusion 기반 미래 상태 예측을 implicit reward로 활용하여 explicit reward engineering 제거
- **Scalability Paradigm**: 기존 RL의 data scaling 한계를 diffusion prior의 capability growth로 해결하는 새로운 접근

## Limitation & Further Study

- **Training Data 의존성**: 6개 지형의 offline data에만 의존하며, 더 다양한 지형에서의 성능 영향 미분석
- **Sim-to-Real Gap**: 시뮬레이션 기반 평가만 제시되어 실제 humanoid 로봇에서의 실현 가능성 미검증
- **Computational Overhead**: Diffusion model의 inference cost와 전체 시스템의 computational 요구사항에 대한 상세 분석 부족
- **Generalization Limits**: Zero-shot generalization이 데이터셋 distribution과 얼마나 멀어질 수 있는지에 대한 명확한 경계 미제시
- **후속연구**: (1) 실제 humanoid 로봇에서의 실시간 적용 검증, (2) 더 광범위한 terrain type과 external disturbance 조건 연구, (3) Diffusion model의 효율성 개선 및 경량화, (4) Transfer learning을 통한 다른 humanoid 형태로의 일반화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: DreamPolicy는 offline data와 diffusion-based trajectory synthesis를 통합하여 humanoid 이동의 확장성 문제를 창의적으로 해결하고, 실제 로봇 응용에 실질적 가치를 제공하는 강력한 프레임워크이다. 다만 sim-to-real 검증과 computational 효율성 분석이 보완되면 더욱 견고한 기여가 될 것이다.
