# Whole-body Multi-contact Motion Control for Humanoid Robots Based on Distributed Tactile Sensors

> **저자**: Masaki Murooka, Kensuke Fukumitsu, Marwan Hamze, Mitsuharu Morisawa, Hiroshi Kaminaga, Fumio Kanehiro, Eiichi Yoshida | **날짜**: 2025-05-26 | **URL**: [https://arxiv.org/abs/2505.19580](https://arxiv.org/abs/2505.19580)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Control system for whole-body multi-contact motion in a humanoid robot.*

분산 촉각 센서를 장착한 휴머노이드 로봇의 팔꿈치, 무릎 등 중간 영역을 포함한 전신 다중 접촉 운동 제어 방법을 제시하고, 촉각 피드백 기반 안정화 제어로 외란에 대한 견고성을 향상시킨다.

## Motivation

- **Known**: 기존 다중 접촉 운동 제어는 손과 발의 극단부(extremities)에만 집중하였으며, force/torque 센서 장착 부위로 제한되어 있었다. 촉각 센서는 인간-로봇 상호작용이나 조작 작업에 활용되어 왔으나, 균형 제어에의 적용은 미미하였다.
- **Gap**: position-controlled 휴머노이드 로봇이 실시간 촉각 피드백을 통해 팔뚝(forearm) 같은 중간 영역 접촉으로 동적 운동을 수행한 사례가 없었다. 전신 접촉 시 실제 접촉 다각형 측정 및 이를 이용한 균형 제어 방법이 부재했다.
- **Why**: 폐쇄된 협소한 환경에서 로봇이 견고하게 작업하려면 전신 다중 접촉이 필수적이며, 의도적인 넓은 영역 접촉은 외란에 대한 안정성을 크게 향상시킨다.
- **Approach**: 기존 다중 접촉 운동 제어 프레임워크를 확장하여, 유연한 시트형 분산 촉각 센서로 실시간 접촉 다각형을 측정하고, centroidal motion control과 limb motion control에 촉각 데이터를 통합한 피드백 제어를 적용한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4. RHP Kaleido with distributed tactile sensors mounted on one forearm*

- **분산 촉각 센서 기반 접촉 감지**: 시트형 분산 촉각 센서를 로봇 사지 표면에 장착하여 로봇 체형 변형 없이 전신 접촉력 측정 가능
- **실시간 접촉 다각형 업데이트**: 예정 접촉 다각형과 측정값 간 유의미한 차이 시 접촉 영역 정점을 온라인 업데이트하여 불안정 제어 회피
- **촉각 피드백 기반 균형 제어**: MPC 기반 centroidal planning과 damping control에 촉각 정보를 통합하여 외란 및 환경 오차에 대한 견고성 향상
- **실제 로봇 실증**: RHP Kaleido 휴머노이드로 팔뚝 접촉 보행, 다리 접촉 앉은 자세 균형 등 동적 전신 다중 접촉 운동 달성

## How

![Figure 1](figures/fig1.webp)

*Fig. 1. Control system for whole-body multi-contact motion in a humanoid robot.*

- 분산 촉각 센서로부터 실제 접촉 영역(contact polygon)을 온라인 측정
- Equation (1)의 resultant wrench 정의식에서 촉각 측정값으로 접촉 다각형 정점 pi,j 실시간 업데이트
- Newton-Euler 방정식 (2)를 이산 시스템 (3)으로 변환하고, MPC (4)로 최적 제어 입력 λ 계산
- 분산 촉각 센서에서 측정한 접촉 force를 contact wrench로 변환 (Fig. 3 참조)
- 계산된 reference centroidal state를 역기구학(inverse kinematics)의 목표값으로 설정
- limb motion control에서 position control과 함께 촉각 센서 기반 damping control 적용

## Originality

- position-controlled 휴머노이드에서 중간 영역 접촉(forearm 등)을 이용한 최초의 동적 다중 접촉 운동 실증
- 분산 촉각 센서로 실시간 접촉 다각형을 감지하여 centroidal planning에 반영하는 통합 제어 고리 구현
- 기존 multi-contact motion controller를 촉각 센서 데이터 처리로 확장하는 modular한 설계
- 촉각 피드백을 균형 제어(balance control)에 명시적으로 적용한 첫 사례

## Limitation & Further Study

- 시뮬레이션 검증은 충실하지만, 실제 로봇 실험은 정성적 데모 수준이며 정량적 안정성 지표 부재
- 접촉 시퀀스(Cd)의 타이밍, 위치, 면적이 사전 수동 결정되거나 별도 global planner에 의존
- position-controlled 로봇 가정으로 torque-controlled 로봇에의 적용성 미지수
- 분산 촉각 센서의 캘리브레이션, 신뢰성, 내구성에 대한 상세 논의 부족
- Euler method 이산화로 인한 수치적 오차와 MPC 계산 부하에 대한 분석 미흡

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 분산 촉각 센서를 활용한 휴머노이드 로봇의 전신 다중 접촉 운동 제어는 새로운 차원의 운동 능력을 제시하며, centroidal motion 및 limb motion 제어의 통합이 체계적이다. 다만 실제 로봇 검증의 정량적 깊이와 일반화 가능성 분석이 보완되면 영향력이 더욱 클 것으로 판단된다.
