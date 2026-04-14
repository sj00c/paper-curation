# Gait-Adaptive Perceptive Humanoid Locomotion with Real-Time Under-Base Terrain Reconstruction

> **저자**: Haolin Song, Hongbo Zhu, Tao Yu, Yan Liu, Mingqi Yuan, Wengang Zhou, Hua Chen, Houqiang Li | **날짜**: 2025-12-08 | **URL**: [https://arxiv.org/abs/2512.07464](https://arxiv.org/abs/2512.07464)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the proposed Successive Teacher–Student (S-TS) framework and deployment pipeline. A teacher–student*

인간형 로봇의 복잡한 지형 보행을 위해 하향식 깊이 카메라로 촬영한 영상을 U-Net으로 높이맵으로 재구성하고, 이를 통합 정책에 입력하여 관절 제어와 보행 주기를 동시에 적응시키는 지각 기반 보행 프레임워크를 제시한다.

## Motivation

- **Known**: 강화학습 기반 인간형 로봇 보행 제어가 평탄하거나 완만한 지형에서는 성과를 보이고 있으며, 전방 깊이 카메라와 LiDAR 기반 고도맵 방법들이 지형 인식 보행에 사용되어 왔다.
- **Gap**: 기존 전방향 카메라 방식은 로봇이 감속하거나 방향을 바꿀 때 발 아래 지형을 놓치고, LiDAR 방식은 추가 매핑 파이프라인의 복잡성과 지연을 야기하며, 보행 주기를 외부에서 지정하는 방식은 지형 인식과 보행 타이밍의 긴밀한 결합을 방해한다.
- **Why**: 계단 오르내림이나 넓은 갭 횡단 같은 복잡한 지형에서 한 발의 실수나 타이밍 오류만으로도 균형 상실로 이어질 수 있으므로, 실시간 지형 감지와 보행 적응이 통합된 제어가 필수적이다.
- **Approach**: 하향식 깊이 카메라 기반 단일 프레임 U-Net 높이맵 재구성과 지각·자체감각 정보를 입력으로 하는 통합 정책이 관절 명령과 보행 주기 신호를 동시에 생성하며, Successive Teacher–Student 학습으로 효율적으로 정책을 학습한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Full-sized humanoid robot Oli performing gait-*

- **실시간 높이맵 재구성**: 하향식 깊이 카메라로부터 50Hz에서 작동하는 compact U-Net을 통해 자아중심적 높이맵을 실시간으로 구성
- **통합 적응형 정책**: 지형 정보와 자체감각 정보를 처리하여 관절 목표값과 보행 주기 신호를 동시에 출력하며, 명령 동작과 국소 지형에 따라 보행 리듬 자동 조정
- **효율적 지식 전이**: 단일 단계 Successive Teacher–Student 프레임워크로 특권적 관찰에서 부분 관찰로의 안정적이고 데이터 효율적인 지식 이전 실현
- **실제 로봇 검증**: 31-DoF, 1.65m 인간형 로봇으로 계단 오르내림(전진/후진), 46cm 갭 횡단 등 다양한 복잡 지형에서 견고한 전방향 보행 시연

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Overview of the proposed Successive Teacher–Student (S-TS) framework and deployment pipeline. A teacher–student*

- 하향식 깊이 카메라를 로봇 베이스 아래에 장착하여 발 주변 지지 영역 촬영
- U-Net 기반 경량 신경망으로 각 깊이 프레임을 조밀한 자아중심적 높이맵으로 변환하여 신체 및 다리 자체폐색 문제 해결
- 지각 높이맵과 자체감각 관찰을 통합 정책 네트워크에 입력하여 관절 명령과 스칼라 보행 주기 신호를 동시 출력
- Successive Teacher–Student 학습에서 특권적 정보로 학습한 teacher 정책이 noisy 부분 관찰의 student 인코더를 감독하고, switch gate로 점진적 환경 상호작용 전이
- 제어 루프와 동일한 50Hz 주파수에서 높이맵 재구성과 정책 실행으로 지형 변화에 빠른 반응

## Originality

- 기존의 전방향 카메라 중심 접근에서 벗어나 하향식 깊이 카메라로 발 아래 핵심 영역에 집중하고, 단일 프레임 U-Net 재구성으로 다중 센서 융합 및 명시적 시간 맵핑 회피
- 보행 주기를 외부 신호로 취급하지 않고 관절 제어와 동일 정책에서 동시 학습하는 end-to-end 설계로, 지형 인식과 보행 적응의 긴밀한 결합 실현
- 단일 단계 Successive Teacher–Student 프레임워크로 특권적 관찰에서 부분 관찰로의 전이를 기존 다단계 방식보다 효율적으로 수행

## Limitation & Further Study

- 하향식 카메라는 로봇 앞의 먼 거리 지형을 감지할 수 없어 급격한 장애물이나 예기치 않은 지형 변화에 대응 어려움 가능
- 31-DoF 특정 로봇 구조에 대해 학습되었으므로 다른 형태의 인간형 로봇으로의 일반화 검증 필요
- 실제 계단/갭 환경에 대한 테스트 데이터가 제한적이므로 더 다양한 실제 지형 환경에서의 강건성 검증 필요
- U-Net의 깊이 이미지 노이즈, 반사 등에 대한 민감도 분석 및 개선 여지 존재
- 후속 연구에서는 전방향 카메라와의 결합, 더 복잡한 자연 지형 대응, 다양한 인간형 로봇 플랫폼으로의 전이 학습 추진 권장

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 인간형 로봇의 복잡 지형 보행이라는 중요한 문제를 하향식 깊이 카메라와 U-Net 기반 높이맵 재구성, 통합 적응형 정책의 조합으로 창의롭게 해결하였으며, 실제 로봇에서 계단 오르내림과 갭 횡단을 성공적으로 시연하여 높은 실용적 가치를 보인다.
