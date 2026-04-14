# High-Speed and Impact Resilient Teleoperation of Humanoid Robots

> **저자**: Sylvain Bertrand, Luigi Penco, Dexton Anderson, Duncan Calvert, Valentine Roy, Stephen McCrory, Khizar Mohammed, Sebastian Sanchez, Will Griffith, Steve Morfey, Alexis Maslyczyk, Achintya Mohan, Cody Castello, Bingyin Ma, Kartik Suryavanshi, Patrick Dills, Jerry Pratt, Victor Ragusila, Brandon Shrewsbury, Robert Griffin | **날짜**: 2024-09-06 | **URL**: [https://arxiv.org/abs/2409.04639](https://arxiv.org/abs/2409.04639)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

본 논문은 7개의 IMU 기반 캘리브레이션 무료 모션 캡처, low-latency kinematics streaming toolbox, 고대역폭 cycloidal actuator를 통합하여 휴머노이드 로봇의 고속 및 충격 강건 텔레오퍼레이션을 실현한다.

## Motivation

- **Known**: 텔레오퍼레이션 시스템은 높은 투명성(high transparency)과 실시간 제어를 위해 정교한 하드웨어 및 소프트웨어 솔루션이 필요하다. 기존 연구는 모션 예측, 양방향 제어, 또는 비전 기반 shadow 방식을 제안했으나 고속 동작 시나리오에서의 검증이 부족하다.
- **Gap**: 기존 방법들은 네트워크 지연에 민감하거나, 사용자 측 장비가 복잡하거나, 고속 동작에서의 유효성이 입증되지 않았다. 고속 충격 내성과 실시간 제어를 동시에 달성하는 통합 솔루션이 부재한다.
- **Why**: 휴머노이드 로봇의 텔레오퍼레이션은 위험한 환경에서의 인간 의사결정 활용, 직관적 제어, 그리고 고속 동적 작업 수행이 중요하며, 이는 재해 대응, 산업 응용 등 실제 환경에서 필수적이다.
- **Approach**: 본 논문은 최소한의 센서(7 IMU) 기반 칼리브레이션 무료 모션 리타게팅, 60Hz 입력을 1kHz 제어 대역폭으로 확장하는 filtering/estimation/prediction 기반 streaming 기법, 그리고 고대역폭 cycloidal actuator 통합을 통해 문제를 해결한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **최소 모션 캡처**: 7개 IMU(VR headset 1개, 컨트롤러 2개, 추적기 4개)만 사용하여 full-body reference 생성 가능하며, 사전 캘리브레이션이나 신체 계측 불필요
- **저지연 kinematics streaming**: filtering, state estimation, prediction을 통합한 KST로 60Hz 입력을 1kHz 제어 대역폭으로 실시간 처리
- **충격 강건성**: cycloidal actuator 통합으로 100lbs 펀칭백을 인간 속도로 타격 가능한 고속 임팩트 내성 달성
- **통합 프레임워크**: motion retargeting, KST, whole-body controller, visual feedback(digital twin + stereo vision)을 통합하여 unprecedented 성능 시연

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- **Pelvis retargeting**: 사용자 waist tracker의 z축 움직임을 로봇 pelvis 높이 비율로 스케일링하고, 초기 대비 변위를 적용하여 pelvis pose 업데이트(식 1-3)
- **Hand retargeting**: 헤드셋과 chest tracker 위치로부터 shoulder 위치 추정(식 4-5), 팔 길이 비율 스케일링(식 6), 사용자 손 움직임의 스케일된 리플렉션을 적용(식 7)
- **Footstep streaming**: 사용자 발 움직임을 연속 추적하여 로봇의 새로운 footstep pose 생성
- **KST filtering & safety**: 입력 명령에 대한 filtering 및 안전 제한 적용
- **State estimation & prediction**: 지연 보상 및 미래 상태 예측으로 매끄럽고 지속적인 동작 유지
- **Inverse kinematics**: 원하는 rigid body 위치 및 방향을 달성하기 위한 필요한 joint 움직임 계산
- **Whole-body controller**: 로봇의 balance를 유지하면서 명령 추적 및 실행

## Originality

- **최소 센서 모션 캡처**: 기하학적 관계(예: 머리 길이와 chest-headset 거리의 1.5배 관계, 식 4)를 활용하여 7 IMU만으로 shoulder/hand pose 추정하는 캘리브레이션 무료 방식은 기존 marker-based/RGB 기반 방식과 차별화
- **저지연 streaming 프레임워크**: 60Hz 사용자 입력을 filtering, prediction, estimation으로 1kHz 제어로 업샘플링하는 명시적 기법은 네트워크 지연 보상에 새로운 접근
- **실제 고속 동작 검증**: motion anticipation/bilateral control의 이론적 제안과 달리, 100lbs 펀칭백 타격을 통한 고속 임팩트 시나리오에서의 실제 검증은 이 분야에서 새로운 벤치마크 제시

## Limitation & Further Study

- **시각 피드백 분석 부족**: 논문은 visual feedback이 기존 기술을 따른다고 명시하였으나, digital twin과 stereo vision의 지연, 품질, 사용자 경험에 대한 정량적 분석 부재
- **로봇 특화성**: Nadia 휴머노이드 로봇 특화 설계로 다른 로봇 플랫폼에의 일반화 가능성 미검증
- **신체 다양성**: 사용자와 로봇 간 신체 비율 스케일링이 단순 선형 비율 기반이므로, 극단적으로 다른 신체 형태에서의 성능 미평가
- **환경 상호작용**: 펀칭백 외 다양한 환경과의 상호작용(미끄러운 표면, 복잡한 장애물, 유연한 물체) 에서의 강건성 미검증
- **후속 연구**: (1) 다중 로봇 플랫폼 및 극단적 신체 크기에 대한 일반화, (2) 네트워크 지연이 있는 원격 환경에서의 성능 평가, (3) 복합 조작 작업(정교한 조립, 민감한 물체 처리)에서의 안정성 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 최소 센서 기반 모션 캡처, low-latency streaming, cycloidal actuator를 통합하여 휴머노이드 로봇의 고속 충격 강건 텔레오퍼레이션을 처음으로 실제 구현 및 검증했으며, 간단하면서도 효과적인 설계로 실용적 가치가 높다. 다만 플랫폼 특화성과 환경 다양성 평가 부재가 한계이다.
