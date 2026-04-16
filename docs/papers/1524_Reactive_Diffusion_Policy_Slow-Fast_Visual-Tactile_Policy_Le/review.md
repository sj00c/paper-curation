---
title: "1524_Reactive_Diffusion_Policy_Slow-Fast_Visual-Tactile_Policy_Le"
authors:
  - "Han Xue"
  - "Jieji Ren"
  - "Wendi Chen"
  - "Gu Zhang"
  - "Yuan Fang"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 접촉 기반 조작 작업을 위해 AR 기반 촉각 피드백 텔레작동 시스템 TactAR과 slow-fast 계층 구조의 Reactive Diffusion Policy (RDP) 알고리즘을 제안하여, 고주파 촉각 피드백 기반 폐루프 제어와 복잡한 궤적 모델링을 통합한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Diffusion_Policy_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xue et al._2025_Reactive Diffusion Policy Slow-Fast Visual-Tactile Policy Learning for Contact-Rich Manipulation.pdf"
---

# Reactive Diffusion Policy: Slow-Fast Visual-Tactile Policy Learning for Contact-Rich Manipulation

> **저자**: Han Xue, Jieji Ren, Wendi Chen, Gu Zhang, Yuan Fang, Guoying Gu, Huazhe Xu, Cewu Lu | **날짜**: 2025-03-04 | **URL**: [https://arxiv.org/abs/2503.02881](https://arxiv.org/abs/2503.02881)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: TactAR is a low-cost and versatile teleoperation system which can provide real-time tactile / force feedback via*

본 논문은 접촉 기반 조작 작업을 위해 AR 기반 촉각 피드백 텔레작동 시스템 TactAR과 slow-fast 계층 구조의 Reactive Diffusion Policy (RDP) 알고리즘을 제안하여, 고주파 촉각 피드백 기반 폐루프 제어와 복잡한 궤적 모델링을 통합한다.

## Motivation

- **Known**: 시각 기반 모방 학습(IL) 방법들은 action chunking을 통해 장시간 수열의 누적 오차를 완화하고 복잡한 비-마르코프 행동을 모델링할 수 있으나, 청크 실행 중 환경 변화에 즉각 대응하지 못하고 촉각 입력이 부재하여 정밀한 접촉 작업에 제한된다.
- **Gap**: 기존 시각-촉각 모방 학습은 관측 수준에서만 촉각 입력을 활용하며 action chunking에 의존하여 고주파 촉각 피드백 기반의 빠른 반응 제어가 불가능하고, 대부분의 텔레작동 시스템은 미세한 촉각/힘 피드백 수집의 어려움이 있다.
- **Why**: 접촉 기반 정밀 작업(채소 깎기 등)은 인간의 예측 행동과 감각 피드백 기반 폐루프 미조정 두 제어 메커니즘이 필요하며, 이를 로봇에서 구현할 수 있다면 제조, 의료 등 다양한 실제 응용 분야를 확장할 수 있다.
- **Approach**: 두 가지 핵심 제안으로 구성된다: (1) Meta Quest3를 이용한 AR 기반 실시간 촉각/힘 피드백 텔레작동 시스템 TactAR으로 고품질 데이터 수집, (2) latent diffusion policy(느린 네트워크, 1-2 Hz)로 고수준 action chunk를 예측하고 asymmetric tokenizer(빠른 네트워크, 20-30 Hz)로 고주파 촉각 피드백 기반 폐루프 제어를 수행하는 slow-fast 계층 구조의 RDP 알고리즘.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: TactAR is a low-cost and versatile teleoperation system which can provide real-time tactile / force feedback via*

- **TactAR 텔레작동 시스템**: Meta Quest3 기반 저비용($500) AR 시스템으로 GelSight Mini, MCTac, 관절 토크 센서 등 다양한 센서를 지원하며 3D deformation field를 통합 표현으로 실시간 촉각/힘 피드백 제공
- **RDP 알고리즘**: slow-fast 계층 구조로 action chunking의 복잡 궤적 모델링 능력과 고주파 촉각 피드백 폐루프 제어를 통합하여 접촉 기반 작업에서 기존 방법 대비 35% 이상 성능 향상
- **교차 센서 적용성**: 서로 다른 촉각/힘 센서(GelSight Mini, MCTac, 토크 센서)에 대해 RDP의 일반화 능력을 실증적으로 검증
- **복합 능력 평가**: 정밀도, 정밀한 적응 힘 제어, 외란에 대한 빠른 반응, 양팔 협동 등을 포함한 3개 도전적 접촉 작업으로 광범위 평가

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of TactAR teleoperation system. It can provide real-time tactile / force feedback via Augmented Reality*

- **TactAR 구성**: Meta Quest3 VR 헤드셋과 컨트롤러로 end-effector 포즈 제어, 촉각 센서와 RGB 카메라 스트림 통합, 3D deformation field를 AR에서 로봇 end-effector에 부착하여 시각화
- **3D Deformation Field 표현**: 광학 촉각 센서(GelSight Mini, MCTac)의 젤 표면 변형과 힘/토크 센서의 정규화된 출력을 통일된 3D 변형장으로 표현하여 센서 종류에 무관하게 적용
- **시간 동기화 및 스트림 처리**: 촉각(25-30 Hz), 힘/토크(120 Hz), 이미지(30 Hz), 액션 명령(90 Hz) 등 다양한 주파수의 센서 신호를 TCP 포즈 추적(120 Hz) 기준으로 동기화
- **Slow 정책(LDP)**: latent diffusion model 기반으로 시각 관측으로부터 latent space에서 고수준 action chunk를 1-2 Hz 저주파에서 예측하여 복잡하고 비-마르코프 행동 모델링
- **Fast 정책(Asymmetric Tokenizer)**: 예측된 latent action chunk를 고주파(20-30 Hz) 촉각 피드백에 기반하여 폐루프로 미조정하는 learnable impedance controller 역할로 정밀한 힘 제어와 빠른 반응 달성
- **Latent Action Chunk Correction**: latent space에서 fast policy의 수정 신호를 누적하여 slow policy의 예측 chunk를 보정하는 메커니즘

## Originality

- **AR 기반 촉각 피드백 텔레작동의 혁신**: 기존 텔레작동의 촉각 피드백 한계를 극복하기 위해 Meta Quest3의 AR 공간에 3D deformation field를 렌더링하는 신개념의 저비용 시스템 제시
- **3D Deformation Field의 통합 표현**: 광학 및 전기식 촉각 센서, 힘/토크 센서를 포함한 이질적 센서들을 단일 3D 변형장으로 표현하는 통일된 접근으로 센서 독립적 호환성 달성
- **Slow-Fast 계층 구조의 창의적 설계**: 인간 신경과학의 feedforward 예측과 폐루프 미조정 이분 제어 구조에서 영감을 얻어 action chunking과 고주파 피드백 제어를 first principles 수준에서 통합
- **Asymmetric Tokenizer의 고주파 폐루프 제어**: 기존 action chunking 기반 IL 방법들이 청크 실행 중 피드백에 응답 불가능한 제약을 극복하기 위해 latent space에서의 동적 수정 메커니즘 제안
- **교차 센서 일반화성**: 서로 다른 물리적 특성의 센서(광학 vs. 전기식, 접촉 vs. 힘)에 대해 RDP의 유효성을 실증적으로 증명하여 실제 로봇 시스템 적용 가능성 입증

## Limitation & Further Study

- **TactAR의 AR 카메라 해상도**: Meta Quest3의 카메라 해상도가 제한적이어서 미세한 환경 시각 특성을 캡처하기 어려울 수 있으며, 실외 환경이나 밝은 조명에서 AR 렌더링 성능 저하 가능
- **RDP의 느린 정책-빠른 정책 동기화**: 두 네트워크 간의 잠재 공간 수정 신호 전달이 지연될 수 있고, latent action chunk correction의 최적 설계에 대한 이론적 근거 부족
- **데이터 수집 규모의 제한**: 세 가지 접촉 작업에만 평가하였으며, 더 넓은 범위의 복잡한 다중 접촉 상호작용 작업에 대한 성능 미검증
- **센서 간의 특성 차이 처리**: 광학 센서와 힘/토크 센서 간의 측정 신호의 노이즈 특성과 주파수 응답이 상이한데, 3D deformation field 표현만으로는 이러한 차이를 완전히 표준화하지 못할 가능성
- **후속 연구 방향**: (1) 실시간 시각-촉각 센서 융합을 위한 더 효율적인 멀티모달 인코더 개발, (2) sim-to-real 전이 학습으로 데이터 수집 비용 감소, (3) 동적 환경과 미지의 객체에 대한 RDP의 적응성 연구, (4) 이족 이족 로봇 등 더 복잡한 플랫폼으로의 확장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 AR 기반 저비용 촉각 피드백 텔레작동 시스템과 slow-fast 계층 구조의 반응형 확산 정책을 제시하여 접촉 기반 조작에서 실시간 촉각 피드백 폐루프 제어와 복잡한 궤적 모델링을 효과적으로 통합하였으며, 광범위한 실험과 교차 센서 검증을 통해 로봇 조작 학습의 중요한 진전을 이루었다.

## Related Papers

- 🏛 기반 연구: [[papers/1362_Diffusion_Policy_Visuomotor_Policy_Learning_via_Action_Diffu/review]] — diffusion policy의 기본 이론과 visuomotor learning 방법론을 제공하여 RDP의 slow-fast hierarchical diffusion policy 설계에 필수적인 기술적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1423_Hierarchical_Diffusion_Policy_manipulation_trajectory_genera/review]] — hierarchical diffusion policy의 개념을 visual-tactile feedback과 결합하여 접촉 기반 조작 작업에서의 계층적 제어를 구현한다.
- 🧪 응용 사례: [[papers/1525_Real-Time_Execution_of_Action_Chunking_Flow_Policies/review]] — real-time action chunking 기법을 reactive diffusion policy에 적용하여 고주파 촉각 피드백과 복잡한 궤적 모델링의 실시간 통합을 달성한다.
- 🔄 다른 접근: [[papers/1572_Sim-to-Real_Reinforcement_Learning_for_Vision-Based_Dexterou/review]] — RDP의 visual-tactile policy와 달리 vision-based dexterous manipulation을 위한 sim-to-real 강화학습 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1564_Scaling_Proprioceptive-Visual_Learning_with_Heterogeneous_Pr/review]] — RDP의 tactile feedback을 heterogeneous pre-training과 결합하여 proprioceptive-visual-tactile learning을 통합한 더 강력한 policy를 개발할 수 있다.
- 🔄 다른 접근: [[papers/1558_RVT-2_Learning_Precise_Manipulation_from_Few_Demonstrations/review]] — Reactive Diffusion Policy가 slow-fast 시각-촉각 학습에 중점을 두는 반면, RVT-2는 순수 시각 기반의 고정밀 조작 학습에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1374_DynamicVLA_A_Vision-Language-Action_Model_for_Dynamic_Object/review]] — Reactive Diffusion Policy의 slow-fast visual-tactile learning이 DynamicVLA의 perception-action latency 해결에 대한 확장된 접근 방식을 제시한다.
