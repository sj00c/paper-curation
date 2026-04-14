# Learning Adaptive Neural Teleoperation for Humanoid Robots: From Inverse Kinematics to End-to-End Control

> **저자**: Sanjar Atamuradov | **날짜**: 2025-11-15 | **URL**: [https://arxiv.org/abs/2511.12390](https://arxiv.org/abs/2511.12390)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Neural teleoperation policy architecture. The network takes VR controller poses (14-dim), joint states (28-*

VR 텔레오퍼레이션 시스템에서 기존의 IK+PD 파이프라인을 reinforcement learning으로 학습한 신경망 정책으로 대체하여, 외력 적응, 부드러운 궤적 생성, 사용자 선호도 적응을 달성한다.

## Motivation

- **Known**: VR 텔레오퍼레이션은 인간형 로봇의 복잡한 조작 작업 제어에 유망한 접근법이며, 기존 시스템은 IK 솔버와 hand-tuned PD 컨트롤러를 사용한다.
- **Gap**: 전통적인 IK+PD 방식은 외력을 처리하지 못하고, 사용자 적응이 불가능하며, 특이점 근처에서 실패하고 비자연스러운 움직임을 생성한다는 근본적 한계가 있다.
- **Why**: 자동 보상 및 적응형 제어를 통해 텔레오퍼레이션 시스템의 자연스러움과 강건성을 크게 향상시킬 수 있으며, 이는 창고 물류, 제조, 재난 대응 등 실제 응용 분야의 성능 개선으로 이어진다.
- **Approach**: IK 시연으로부터의 행동 복제(behavioral cloning)로 초기화한 후, PPO를 사용하여 추적(tracking), 부드러움(smoothness), 에너지 정규화 보상과 함께 미세 조정하고, force curriculum을 적용하여 외력 강건성을 학습시킨다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3 provides a detailed breakdown of performance*

- **추적 오차 감소**: IK 기준선 대비 34% 낮은 tracking error 달성
- **동작 부드러움 개선**: 45% 더 부드러운 궤적 생성
- **외력 적응 우수성**: 외력 적응 측면에서 IK 기준선을 상회
- **실시간 성능 유지**: 50Hz 제어 주파수로 실시간 성능 확보
- **다양한 작업 검증**: pick-and-place, 문열기, bimanual coordination 등에서 성공적 수행

## How

![Figure 1](figures/fig1.webp)

*Figure 1: Neural teleoperation policy architecture. The network takes VR controller poses (14-dim), joint states (28-*

- VR 입력 인코더: 초기 그립 자세 대비 상대 변환을 인코딩하여 VR 좌표계 독립성 확보
- Proprioception 인코더: 관절 위치, 속도, 이전 액션의 5-timestep 히스토리를 MLP로 처리
- LSTM 정책 헤드: 인코딩된 VR 입력과 proprioception을 결합하여 시간적 일관성과 smooth trajectory 생성
- 3단계 학습: (1) IK 시연에서 behavioral cloning으로 초기화, (2) PPO로 smoothness/tracking/energy 보상 미세조정, (3) curriculum-based force randomization으로 외력 강건성 강화
- Domain randomization: 동역학 특성(링크 질량 ±10% 등) 및 sensor noise 무작위화로 sim-to-real 전이 개선

## Originality

- 기존 IK+PD 텔레오퍼레이션 파이프라인을 end-to-end 학습된 신경망 정책으로 완전히 대체하는 첫 시도
- Proprioceptive feedback을 통한 암묵적 외력 보상 메커니즘 제시 - 기존 IK 솔버의 '힘 맹목성(force blindness)' 문제 해결", 'Relative transformation 인코딩으로 VR 좌표계 독립성 달성하는 새로운 설계 선택
- Force curriculum을 통한 점진적 외력 강건성 학습 전략
- Human-in-the-loop 실시간 텔레오퍼레이션을 위한 특화된 학습 설계 (FALCON 등 자율 제어 기반 선행연구와 차별화)

## Limitation & Further Study

- sim-to-real gap: 시뮬레이션 환경과 실제 로봇 환경의 불일치로 인한 성능 저하 가능성
- 일반화 범위: 단일 로봇 플랫폼(Unitree G1)에서만 검증, 다른 인간형 로봇으로의 전이 가능성 미검증
- 사용자 다양성: 제한된 사용자 샘플에서만 사용자 적응 특성 입증, 광범위한 사용자 그룹에서의 성능 미검증
- 외력 보상의 한계: Curriculum 기반 학습이므로 훈련 중 제시된 외력 범위를 벗어난 극단적 상황에서 성능 저하 가능
- **후속연구**: (1) 다중 로봇 플랫폼으로 확장, (2) 메타러닝을 통한 빠른 사용자 적응, (3) 모드 적응형(task-dependent) 정책 학습

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 기존 IK+PD 파이프라인의 근본적 한계를 end-to-end 학습으로 우아하게 해결하며, 강력한 실증 결과와 명확한 성과 지표를 제시한 견실한 연구이다. 다만 단일 플랫폼 검증과 제한된 사용자 다양성은 일반화 가능성에 대한 의문을 남긴다.
