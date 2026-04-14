# Hiking in the Wild: A Scalable Perceptive Parkour Framework for Humanoids

> **저자**: Shaoting Zhu, Ziwen Zhuang, Mengjie Zhao, Kun-Ying Lee, Hang Zhao | **날짜**: 2026-01-12 | **DOI**: [10.48550/arXiv.2601.07718](https://doi.org/10.48550/arXiv.2601.07718)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: System overview. Our framework trains an end-to-end policy using simulated depth and proprioception. To ensure*

이 논문은 깊이 카메라와 proprioception을 직접 joint actions으로 변환하는 end-to-end RL 프레임워크를 제시하여, 외부 상태 추정 없이 humanoid 로봇이 복잡한 비정형 지형에서 최대 2.5 m/s의 속도로 안전하게 이동할 수 있게 한다.

## Motivation

- **Known**: Blind locomotion은 proprioception만으로 견고한 성능을 보이지만 반응형이어서 큰 장애물 회피가 어렵다. LiDAR 기반 elevation map 방식은 상태 추정 드리프트와 모션 디스토션 문제가 있다.
- **Gap**: 기존 depth 기반 방법들은 낮은 속도와 단순 지형(평면, 계단)에만 적용되며 임의적 구성으로 인해 재현과 확장이 어렵다. 또한 foothold precision과 reward hacking 문제가 미해결되어 있다.
- **Why**: Humanoid 로봇이 실제 야외 환경에서 안전하고 신속하게 이동하려면 forward-looking perception이 필수적이며, 재현 가능하고 확장 가능한 통합 프레임워크가 필요하다.
- **Approach**: Single-stage RL을 통해 raw depth와 proprioception을 직접 joint actions에 매핑하되, Terrain Edge Detection + Foot Volume Points로 foothold safety를 보장하고, Flat Patch Sampling으로 reward hacking을 해결한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Hiking in the Wild. Our framework enables a humanoid robot to traverse diverse terrains in both indoor and outdo*

- **Zero-shot Sim-to-Real transfer**: 외부 localization이나 map reconstruction 없이 시뮬레이션 정책이 실제 로봇에서 바로 작동
- **High-speed robust traversal**: 계단, 갭, 경사지, 불규칙한 잔디 지형에서 최대 2.5 m/s 속도로 안전하게 주행
- **Scalable safety mechanism**: Terrain Edge Detection이 임의의 trimesh에 자동으로 적용되어 case-by-case 구현 불필요
- **Reward hacking 해결**: Flat Patch Sampling이 위치 기반 속도 명령을 생성하여 의미 있는 탐험 보장
- **Open-source 배포**: 최소한의 하드웨어 수정으로 실제 로봇에 배포 가능한 훈련/배포 코드 공개

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: System overview. Our framework trains an end-to-end policy using simulated depth and proprioception. To ensure*

- Mixture-of-Experts (MoE) 아키텍처를 활용한 깊이 인코더로 고차원 시각 데이터 처리
- Depth synthesis 모듈로 센서 노이즈와 artifacts를 모의하여 realistic training 구현
- Terrain Edge Detector가 trimesh에서 자동으로 엣지 추출, Volume Points로 침투 penalty 적용
- Flat Patch Sampling이 지형 메시에서 도달 가능한 평탄 영역 식별 후 그에 따른 velocity command 생성
- PPO 알고리즘으로 observation space (proprioception + 깊이 입력)에서 action space (joint actions)로의 매핑 최적화
- 60 Hz 깊이 센서에서 고주파 perception loop로 동적 장애물 회피 가능

## Originality

- **Scalable edge penalization**: 기존 edge penalization을 임의의 trimesh에 자동 적용 가능하도록 확장 (Terrain Edge Detection + Foot Volume Points)
- **Position-based velocity command**: Flat Patch Sampling으로 reward hacking을 근본적으로 해결하는 새로운 curriculum 전략
- **Realistic depth synthesis**: 훈련 중 센서 노이즈 모델링으로 zero-shot transfer 달성
- **High-frequency end-to-end policy**: 60 Hz depth input을 직접 처리하는 단일 단계 RL로 높은 동역학 성능 구현

## Limitation & Further Study

- 야외 환경의 다양한 조건(날씨, 조명, 계절 변화)에 대한 강건성 평가 부족
- Humanoid 로봇의 특정 형태(센서 위치, 체형)에 맞춘 설계로 다른 humanoid 플랫폼으로의 일반화 검증 필요
- 극한 지형(매우 높은 단차, 매우 가파른 경사)에서의 성능 한계 미명시
- 훈련 시간, 필요 데이터 규모, 수렴 안정성에 대한 상세 분석 부족
- 후속 연구로 multi-humanoid 플랫폼 검증, 실시간 환경 변화 대응, 팀 협력 주행 등 확대 가능

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 논문은 humanoid 로봇의 야외 주행을 위한 실용적이고 확장 가능한 end-to-end RL 프레임워크를 제시하며, Terrain Edge Detection, Foot Volume Points, Flat Patch Sampling 등 novel 메커니즘으로 safety와 reward hacking 문제를 효과적으로 해결한다. Open-source 배포와 실제 로봇 검증을 통해 높은 재현성과 실용성을 입증한 우수한 연구이다.
