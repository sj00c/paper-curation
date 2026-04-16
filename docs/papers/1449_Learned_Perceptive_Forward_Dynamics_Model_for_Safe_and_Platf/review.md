---
title: "1449_Learned_Perceptive_Forward_Dynamics_Model_for_Safe_and_Platf"
authors:
  - "Pascal Roth"
  - "Jonas Frey"
  - "Cesar Cadena"
  - "Marco Hutter"
date: "2025.04"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 시뮬레이션과 실세계 데이터로 학습한 지각형 Forward Dynamics Model (FDM)을 제안하여, 복잡한 지형에서 사족 로봇의 안전한 네비게이션을 실현한다. 이 FDM을 MPPI 플래닝 프레임워크에 통합하여 복잡한 비용 함수 튜닝 없이 안전한 경로 계획을 가능하게 한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Roth et al._2025_Learned Perceptive Forward Dynamics Model for Safe and Platform-aware Robotic Navigation.pdf"
---

# Learned Perceptive Forward Dynamics Model for Safe and Platform-aware Robotic Navigation

> **저자**: Pascal Roth, Jonas Frey, Cesar Cadena, Marco Hutter | **날짜**: 2025-04-27 | **URL**: [https://arxiv.org/abs/2504.19322](https://arxiv.org/abs/2504.19322)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Demonstration of the proposed perceptive Forward Dynamics Model for robust navigation in complex environments. T*

본 논문은 시뮬레이션과 실세계 데이터로 학습한 지각형 Forward Dynamics Model (FDM)을 제안하여, 복잡한 지형에서 사족 로봇의 안전한 네비게이션을 실현한다. 이 FDM을 MPPI 플래닝 프레임워크에 통합하여 복잡한 비용 함수 튜닝 없이 안전한 경로 계획을 가능하게 한다.

## Motivation

- **Known**: Forward Dynamics Model은 로봇의 미래 상태를 예측하는 데 사용되며, 기존 물리 기반 모델은 접촉이 많은 시나리오에서 정확성이 떨어진다. 데이터 기반 접근법은 신경망을 사용하여 복잡한 역학을 근사할 수 있으나 대량의 실세계 데이터가 필요하다.
- **Gap**: 기존 연구는 2D 환경이나 단기 예측에만 집중했으며, 거친 지형에서의 3D 지각을 포함한 FDM과 안정적인 sim-to-real 전이가 부족했다. 또한 MPPI 기반 플래닝은 환경별로 비용 함수를 광범위하게 조정해야 한다는 문제가 있다.
- **Why**: 로봇이 복잡한 환경에서 안전하게 자율 네비게이션을 수행하려면 정확한 동역학 예측과 지형 통과성 평가가 필수적이다. 수동 비용 함수 조정을 제거하면 새로운 환경으로의 빠른 적응이 가능해지므로 실용성이 크게 향상된다.
- **Approach**: 본 논문은 합성 데이터로 사전 학습한 후 실세계 데이터로 미세 조정하는 하이브리드 전략을 사용한다. 지각형 FDM이 높이 스캔과 고유감각 측정값의 역사를 입력으로 받아 미래 상태와 실패 확률을 예측하며, 이를 MPPI 기반 플래닝과 통합하여 간단한 보상 함수로 최적 행동을 선택한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Fig. 5: Comparison of the position error at the final prediction step in different environments for the presented FDM*

- **위치 추정 개선**: ANYmal 사족 로봇에서 위치 추정을 기존 방법 대비 평균 41% 개선했다.
- **네비게이션 성공률 향상**: 거친 시뮬레이션 환경에서 네비게이션 성공률이 27% 증가했다.
- **Sim-to-Real 전이 달성**: 실세계 데이터를 통합하여 안정적인 현실 세계 배포를 입증했다.
- **영점 적응**: 추가 학습 없이 환경별 비용 항 조정만으로 새 환경에 적응 가능함을 보였다.
- **공개 구현**: 코드와 모델을 공개 저장소에서 제공하여 재현성과 확장성을 지원한다.

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the FDM training. Data is collected in a parallelized simulation setting and from real-world experim*

- 사전학습: 상태 기반 시뮬레이터에서 수년의 네비게이션 경험과 고위험 기동을 포함한 합성 데이터로 FDM을 사전 학습한다.
- 미세 조정: 실세계 상호작용 데이터를 수집하여 FDM을 미세 조정하여 미모델링 효과를 보정한다.
- 다중 입력 처리: 높이 맵 스캔(3D 지각), 고유감각 측정값의 역사, 과거 상태를 신경망 인코더에 입력한다.
- n-step 예측: Forward Integration을 통해 연쇄적으로 미래 상태와 실패 확률을 예측한다.
- MPPI 통합: 학습된 동역학 모델을 Model Predictive Path Integral 샘플링 플래너와 연결하여 간단한 보상 함수로 경로를 최적화한다.
- Receding Horizon 계획: 현재 위치에서 실행 가능한 행동을 샘플링하고, 가장 높은 보상을 받는 경로를 선택한 후 다음 시간 단계로 이동한다.

## Originality

- 거친 지형에서의 첫 번째 사족 로봇 FDM: 높이 스캔을 활용한 3D 환경 인식을 포함한 거친 지형 네비게이션 모델의 첫 구현이다.
- 하이브리드 학습 전략: 시뮬레이션과 실세계 데이터를 결합한 효과적인 sim-to-real 전이 방법론을 제시한다.
- 지각형 동역학 모델: 고유감각 정보와 환경 기하학을 통합하여 플랫폼별 특성을 포함한 동역학 예측을 실현한다.
- 비용 함수 단순화: FDM이 내재적으로 통과성을 학습하므로 MPPI의 복잡한 비용 함수 튜닝을 제거할 수 있다.
- 영점 적응성: 추가 학습 없이 새 환경으로 즉시 적응 가능한 메커니즘을 개발했다.

## Limitation & Further Study

- **데이터 요구량**: 실세계 데이터의 양이 많을수록 성능이 향상되므로, 충분한 실제 데이터 수집이 필수적이다.
- **계산 복잡도**: MPPI 샘플링 기반 접근법은 경로 샘플링을 위한 계산량이 적지 않으며, 실시간 성능 분석이 부족하다.
- **일반화 범위**: 특정 로봇(ANYmal) 플랫폼 중심으로 평가되었으므로 다른 사족 또는 바퀴형 로봇으로의 일반화 정도가 불명확하다.
- **환경 편의성**: 거친 지형 평가는 주로 시뮬레이션 환경에 기반했으며, 실세계 검증이 제한적이다.
- **후속 연구**: (1) 보다 다양한 로봇 플랫폼에 대한 적응 가능성 평가, (2) 온라인 학습 또는 적응 메커니즘 개발, (3) 장시간 자율 네비게이션 시나리오 검증이 필요하다.

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 거친 지형에서 사족 로봇의 안전한 네비게이션을 위해 지각형 FDM을 제안한 의미 있는 연구로, 하이브리드 학습 전략과 MPPI 통합을 통해 비용 함수 튜닝을 제거하고 영점 적응성을 제공한다. 실측 개선(41% 위치 추정, 27% 성공률)과 공개 구현이 큰 강점이나, 실세계 검증 범위 확대와 다양한 플랫폼 적용 가능성 입증이 향후 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1526_Real-World_Humanoid_Locomotion_with_Reinforcement_Learning/review]] — 둘 다 사족 로봇의 복잡한 지형 네비게이션을 다루지만 perceptive FDM + MPPI vs pure RL이라는 다른 접근법을 사용한다.
- 🏛 기반 연구: [[papers/1431_Impact_of_Static_Friction_on_Sim2Real_in_Robotic_Reinforceme/review]] — sim2real에서 friction의 영향 분석을 Forward Dynamics Model 학습에 적용한 실용적 확장이다.
- 🔗 후속 연구: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — real-world robotics의 DRL 응용을 learned dynamics model과 결합하여 안전한 네비게이션으로 발전시켰다.
- 🔄 다른 접근: [[papers/1484_MuJoCo_Playground/review]] — 둘 다 사족 로봇을 위한 시뮬레이션 기반 접근법이지만 forward dynamics model과 MuJoCo 기반 학습의 차이점을 비교할 수 있다.
- 🔄 다른 접근: [[papers/1488_NavDP_Learning_Sim-to-Real_Navigation_Diffusion_Policy_with/review]] — 둘 다 sim-to-real navigation을 다루지만 forward dynamics model과 diffusion policy의 접근법 차이를 분석할 수 있다.
- 🔄 다른 접근: [[papers/1484_MuJoCo_Playground/review]] — 둘 다 사족 로봇 시뮬레이션을 다루지만 MuJoCo playground와 forward dynamics model의 접근법 차이를 비교할 수 있다.
- 🔄 다른 접근: [[papers/1488_NavDP_Learning_Sim-to-Real_Navigation_Diffusion_Policy_with/review]] — 둘 다 sim-to-real navigation을 다루지만 diffusion policy와 forward dynamics model의 접근법 차이를 비교할 수 있다.
