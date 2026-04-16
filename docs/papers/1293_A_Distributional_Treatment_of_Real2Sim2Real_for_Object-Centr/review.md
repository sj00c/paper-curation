---
title: "1293_A_Distributional_Treatment_of_Real2Sim2Real_for_Object-Centr"
authors:
  - "Georgios Kamaras"
  - "Subramanian Ramamoorthy"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "Deformable Linear Object(DLO) 조작을 위해 likelihood-free inference로 물리 파라미터의 사후분포를 추정하고, 이를 domain randomisation에 활용하여 시뮬레이션에서 학습한 정책을 실제 환경에 zero-shot으로 배포하는 end-to-end Real2Sim2Real 프레임워크를 제시한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Kamaras and Ramamoorthy_2025_A Distributional Treatment of Real2Sim2Real for Object-Centric Agent Adaptation in Vision-Driven Def.pdf"
---

# A Distributional Treatment of Real2Sim2Real for Object-Centric Agent Adaptation in Vision-Driven Deformable Linear Object Manipulation

> **저자**: Georgios Kamaras, Subramanian Ramamoorthy | **날짜**: 2025-02-25 | **URL**: [https://arxiv.org/abs/2502.18615](https://arxiv.org/abs/2502.18615)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

Deformable Linear Object(DLO) 조작을 위해 likelihood-free inference로 물리 파라미터의 사후분포를 추정하고, 이를 domain randomisation에 활용하여 시뮬레이션에서 학습한 정책을 실제 환경에 zero-shot으로 배포하는 end-to-end Real2Sim2Real 프레임워크를 제시한다.

## Motivation

- **Known**: Sim2Real 학습은 시뮬레이션에서의 다중 반복을 통해 정책을 강화하며, domain randomisation은 파라미터 변동에 대한 견고성을 제공한다. BayesSim과 같은 LFI 방법과 kernel mean embeddings는 물리 파라미터 추정에 효과적이다.
- **Gap**: 기존 연구는 Bayesian 추론의 표현력과 model-free RL의 유연성을 결합한 통합적인 Real2Sim2Real 시스템이 부족하며, 특히 시각 기반 DLO 조작에서 추정된 domain 분포가 정책 학습과 실제 성능에 미치는 영향을 체계적으로 연구하지 않았다.
- **Why**: 정밀한 DLO 조작(끈 묶기, 수술 봉합 등)은 강성, 길이 등 물리 파라미터에 민감하므로, 이러한 파라미터를 정확히 추정하고 그에 맞춰 정책을 적응시키는 것이 robustness 달성에 필수적이다.
- **Approach**: 실제 환경에서 수집한 visual trajectory에 대해 BayesSim으로 DLO 파라미터의 사후분포를 반복적으로 추정(Real2Sim)하고, 이 분포를 domain randomisation 프라이어로 사용하여 PPO 기반 정책을 시뮬레이션에서 학습한 후(Sim2Real), 추가 fine-tuning 없이 실제 환경에 배포한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **End-to-end Real2Sim2Real 프레임워크**: Bayesian inference의 표현력과 model-free RL의 유연성을 결합하여 vision-based DLO 조작을 위한 통합 시스템 구축
- **분포적 파라미터 추정**: RKHS 기반 keypoint trajectory embedding을 활용하여 BayesSim이 시각/proprioceptive 데이터만으로 parametric DLO 집합 내 미세한 물리 특성을 정밀하게 분류 가능함을 입증
- **Zero-shot deployment**: 추정된 사후분포를 domain randomisation에 활용한 정책이 실제 환경에서 추가 fine-tuning 없이 견고하게 작동함을 시연
- **Domain 분포의 영향 분석**: 서로 다른 randomisation domain이 model-free RL 학습과 실제 성능에 미치는 영향을 체계적으로 연구

## How

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- Likelihood-free inference (BayesSim)를 통해 real trajectory xr에 대한 파라미터 θ의 사후분포 p̂(θ|x=xr) 추정
- Kernel mean embeddings과 RKHS를 이용하여 고차원 keypoint trajectory를 저차원 분포 표현으로 임베딩
- Mixture density neural networks (MDNN)로 조건부 밀도함수 q_φ(θ|x) 학습
- 추정된 사후분포 p̂(θ)를 domain randomisation 프라이어로 사용하여 PPO 기반 정책 π_β 학습
- 시뮬레이션에서 학습한 정책을 DLO reaching task에서 실제 환경으로 zero-shot 배포 및 평가
- Algorithm 1에 따라 LFI 반복을 통해 reference prior를 점진적으로 갱신

## Originality

- Bayesian inverse problem 해결과 domain randomisation을 통합적으로 결합하여, 단순 균등 분포 대신 데이터 기반 사후분포로 RL 학습을 guide하는 novel 접근
- RKHS 기반 distributional embeddings을 BayesSim과 결합하여 visual servoing 노이즈에 robust한 파라미터 분류 달성
- Iterative LFI 프로세스(Algorithm 1)를 통해 reference prior를 점진적으로 정제하여 추론 정확도 향상
- Vision-centric DLO 조작에서 물리 파라미터 추정과 control policy 학습의 end-to-end 파이프라인 최초 제시

## Limitation & Further Study

- 실험이 단일 reaching task에 한정되어 있어, 더 복잡한 DLO 조작(끈 묶기, whipping 등)으로의 확장 검증 필요
- BayesSim의 분류 성능이 parameterization 범위의 크기에 의존할 수 있으므로, 더 광범위한 파라미터 공간에서의 scaling 검토 필요
- Zero-shot deployment의 성공이 시뮬레이터 정확도에 크게 의존하는데, 다양한 시뮬레이터와 DLO 재료에 대한 일반화 검증 부족
- Likelihood-free inference의 computational cost와 필요한 시뮬레이션 rollout 수에 대한 상세 분석 및 최적화 여지
- Real-to-sim 갭이 여전히 존재할 수 있으므로, domain gap을 더 명시적으로 모델링하는 방법 탐색 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 LFI 기반 파라미터 추정과 domain randomisation, model-free RL을 정교하게 통합하여 vision-based DLO 조작의 Real2Sim2Real 문제를 해결하는 novel하고 기술적으로 견고한 접근을 제시하며, zero-shot deployment의 실증을 통해 실용적 가치를 입증한다.

## Related Papers

- 🔄 다른 접근: [[papers/1527_Real2Render2Real_Scaling_Robot_Data_Without_Dynamics_Simulat/review]] — Real2Sim2Real에서 물리 파라미터 추정 방식과 동역학 시뮬레이션 없는 데이터 스케일링이 다른 접근법입니다.
- 🏛 기반 연구: [[papers/1309_An_Real-Sim-Real_RSR_Loop_Framework_for_Generalizable_Roboti/review]] — 일반화 가능한 로봇 제어를 위한 RSR 루프 프레임워크가 Real2Sim2Real의 이론적 기반을 제공합니다.
- 🧪 응용 사례: [[papers/1386_Evaluating_Real-World_Robot_Manipulation_Policies_in_Simulat/review]] — 시뮬레이션에서 실제 로봇 정책 평가 문제를 Real2Sim2Real 프레임워크로 해결할 수 있습니다.
- 🔗 후속 연구: [[papers/1431_Impact_of_Static_Friction_on_Sim2Real_in_Robotic_Reinforceme/review]] — 정적 마찰이 Sim2Real에 미치는 영향 연구를 deformable object에 대한 포괄적인 물리 파라미터 분포 추정으로 확장한 방법론입니다.
- 🔄 다른 접근: [[papers/1309_An_Real-Sim-Real_RSR_Loop_Framework_for_Generalizable_Roboti/review]] — 둘 다 Real2Sim2Real 프레임워크를 제안하지만 RSR Loop은 differentiable simulation에, Distributional Treatment는 물리 파라미터 분포 추정에 중점을 둡니다.
