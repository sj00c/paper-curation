# ARMADA: Augmented Reality for Robot Manipulation and Robot-Free Data Acquisition

> **저자**: Nataliya Nechyporenko, Ryan Hoque, Christopher Webb, Mouli Sivapurapu, Jian Zhang | **날짜**: 2024-12-14 | **URL**: [https://arxiv.org/abs/2412.10631](https://arxiv.org/abs/2412.10631)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview. (A) Human demonstrators wearing Apple Vision Pro can*

Apple Vision Pro의 AR을 활용하여 물리적 로봇 없이 로봇 조작 데이터를 수집하는 ARMADA 시스템을 제시하며, 실시간 로봇 피드백이 데이터 품질을 1.3%에서 71.1%로 향상시킨다.

## Motivation

- **Known**: 모방 학습(imitation learning)은 로봇 조작을 위한 주요 접근법이지만, 전문 하드웨어를 통한 원격 조종 데이터 수집은 하드웨어 가용성에 의해 병목된다.
- **Gap**: 인간과 로봇 간의 embodiment gap을 극복하면서도 물리적 로봇 없이 확장 가능한 데이터 수집 방법이 부재하다.
- **Why**: 인터넷 규모의 로봇 조작 데이터셋이 존재하지 않아 대규모 모방 학습이 불가능하며, AR을 통한 스케일링 가능한 데이터 수집은 로봇 학습의 일반화를 크게 향상시킬 수 있다.
- **Approach**: Apple Vision Pro에서 손 뼈대 추적(skeleton tracking)을 통해 인간의 행동을 감지하고, 실시간 kinematic 시뮬레이션된 로봇 디지털 트윈을 AR로 오버레이하여 사용자에게 로봇 운동학, 동역학, 속도 피드백을 제공한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Overview. (A) Human demonstrators wearing Apple Vision Pro can*

- **스케일러블 데이터 수집**: 15명의 참여자로부터 3개 작업에 대해 675개의 로봇 없는 데모를 수집
- **성능 향상**: 실시간 AR 피드백을 통해 직접 재현(replay) 성공률이 1.3%에서 71.1%로 증가
- **하드웨어 독립성**: 물리적 로봇 접근 없이도 로봇 호환 데이터 수집 가능
- **사용성**: Vision Pro만 필요한 착용 불편 요소 없는 맨손(barehanded) 데이터 수집 가능

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the system architecture described in Section III-A. Human skeletal data is sent over websockets to a*

- ARKit을 통해 손가락과 손목 위치를 추적하여 로봇 제어 명령으로 변환
- ROS와 websocket을 결합한 아키텍처로 Vision Pro와 외부 compute device 간 30Hz 루프 통신
- QR 코드 기준으로 로봇 기저를 배치하고 각 링크를 상대 프레임으로 추가하여 AR 시각화
- singularity, speed, workspace 위반 등의 constraint 정보를 실시간으로 계산하여 시각적 피드백 제공
- 이미지 프레임과 인간 뼈대 데이터를 캡처하여 proprioceptive data와 함께 저장

## Originality

- Apple Vision Pro의 egocentric passthrough 카메라와 고급 손 추적을 활용한 최초의 실시간 로봇 디지털 트윈 AR 시스템
- 물리적 로봇 하드웨어 없이도 embodiment gap을 고려한 데이터 수집이 가능함을 실증
- AR2-D2와 달리 실시간 피드백을 제공하며, ARCap 대비 간편한 맨손 인터페이스 제시
- plug-and-play 아키텍처로 다양한 로봇 플랫폼(Franka, UR5 등)에 호환 가능

## Limitation & Further Study

- 15명의 소규모 사용자 연구로 대규모 데이터 수집 가능성을 충분히 검증하지 못함
- Apple Vision Pro의 높은 비용으로 인한 보편적 접근성 제한
- 복잡한 손-물체 접촉 모델링이 필요한 과제에서의 성능 미검증
- 시스템의 지연시간(latency)과 추적 정확도에 대한 상세한 분석 부족
- 후속 연구: 더 많은 참여자와 다양한 과제에 대한 대규모 검증, 시뮬레이션-실제 로봇 간 성능 격차 분석, 손 접촉 감각 피드백 추가

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ARMADA는 AR 기술을 창의적으로 활용하여 로봇 데이터 수집의 실제적 병목을 해결하는 혁신적 시스템을 제시하며, 실시간 피드백의 극적인 효과를 실증함으로써 대규모 로봇 학습의 새로운 가능성을 열었다.
