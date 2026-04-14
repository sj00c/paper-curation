# ECHO: Edge-Cloud Humanoid Orchestration for Language-to-Motion Control

> **저자**: Haozhe Jia, Jianfei Song, Yuan Zhang, Honglei Jin, Youcheng Fan, Wenshuo Chen, Wei Zhang, Yutao Yue | **날짜**: 2026-03-17 | **URL**: [https://arxiv.org/abs/2603.16188](https://arxiv.org/abs/2603.16188)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

ECHO는 자연어 명령으로 휴머노이드 로봇을 제어하는 엣지-클라우드 프레임워크로, 클라우드의 diffusion 기반 text-to-motion 생성기와 엣지의 RL 트래커를 로봇 네이티브 38차원 표현으로 연결하여 실시간 폐루프 실행을 실현한다.

## Motivation

- **Known**: 최근 언어 조건부 휴머노이드 제어는 end-to-end 접근법 또는 human motion 기반 retargeting 파이프라인으로 진행되어 왔으나, 두 방식 모두 온보드 계산 한계 또는 retargeting 엔지니어링 오버헤드 문제를 안고 있다.
- **Gap**: 기존 방식들은 semantic 표현성, 실시간 제어, 엔지니어링 실용성 사이의 근본적 긴장을 해결하지 못하고 있으며, 특히 hardware 제약 준수와 배포 안정성을 평가하는 메트릭이 부족하다.
- **Why**: 휴머노이드 로봇의 실제 배포를 위해서는 high-frequency 제어와 semantic 복잡성을 동시에 충족하면서 안정적이고 modular한 아키텍처가 필수적이다.
- **Approach**: 생성(cloud diffusion 모델)과 실행(edge RL tracker)을 strictly 분리하고, robot-native 38D 운동 표현으로 두 모듈을 연결하여 inference-time retargeting을 제거하고 실시간 streaming 추적을 가능하게 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **Edge-Cloud 아키텍처**: 클라우드의 CLIP-conditioned 1D convolutional UNet diffusion 생성기가 ~1초 내 모션을 생성하고, 엣지의 teacher-student RL 트래커가 폐루프로 실시간 실행
- **Robot-Native 표현**: 38D velocity 기반 표현(joint angles 29D + root planar velocity 2D + root height 1D + 6D continuous root rotation)으로 retargeting 제거 및 PD 제어와 직접 호환
- **Sim-to-Real 전이**: Evidential Deep Regression adapter와 morphological symmetry 제약, domain randomization을 통해 teacher policy 지식을 student policy로 증류
- **실세계 배포**: Unitree G1 휴머노이드에서 zero hardware fine-tuning으로 다양한 text 명령의 안정적 실행 달성
- **평가 메트릭**: Motion Safety Score(MSS)와 Root Trajectory Consistency(RTC)라는 robot-centric 메트릭으로 hardware 제약 준수와 궤적 충실도 정량화

## How

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **Text-to-Motion 생성**: CLIP 인코더로 자연어를 임베딩하고, 1D convolutional UNet에 cross-attention으로 조건화하여 DDIM sampling(10 denoising steps)으로 50 FPS 모션 생성
- **Motion 표현**: 각 프레임을 38차원 벡터(관절각 + root 속도 + root 높이 + root 회전)로 인코딩하여 global 위치 제거로 drift 감소
- **RL 기반 트래킹**: Asymmetric Actor-Critic 구조에서 privileged teacher policy(PPO)를 student policy로 distill하고, evidential adaptation module로 uncertainty 처리
- **Fall Recovery**: IMU 기반 낙상 감지 및 pre-built motion library에서 recovery trajectory 검색
- **Training 데이터**: HumanML3D를 General Motion Retargeting(GMR)으로 robot skeleton으로 retarget하여 text-motion pairing 유지

## Originality

- **Strict modularity**: 생성과 실행의 완전한 분리로 robot platform 간 portability 및 기존 추적 스택과의 통합성 확보
- **Robot-native 표현**: inference-time retargeting을 완전히 제거하고 로봇 kinematics와 직접 호환되는 compact 38D 표현 제안
- **Edge-Cloud 분산 배포**: 클라우드의 semantic 처리와 엣지의 실시간 제어를 명확히 분리하여 hardware 제약과 semantic 복잡성의 trade-off 해결
- **Robot-centric 평가**: MSS와 RTC로 표준 text-to-motion 벤치마크에서 다루지 않는 hardware 안정성과 배포 안정성 정량화

## Limitation & Further Study

- **Cloud 지연**: 클라우드와의 WebSocket 통신 지연(~1초)이 동적 반응성이 필요한 실시간 상황에 제약
- **Motion library 의존성**: Fall recovery가 pre-built motion library에 의존하므로 예측되지 않은 상황에 대한 일반화 한계
- **Training 데이터 편향**: HumanML3D 기반 training으로 인한 human motion 분포 편향 및 로봇 특화 동작의 부족 가능성
- **후속연구**: 낮은 지연 클라우드-엣지 통신 최적화, 온보드 경량 diffusion 모델 탑재, multi-robot 플랫폼 호환성 확대, dynamic obstacle 회피 능력 강화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ECHO는 생성과 실행의 명확한 분리, robot-native 표현 설계, 실세계 배포 달성을 통해 언어-기반 휴머노이드 제어 분야에서 modularity와 deployability의 새로운 기준을 제시하는 의미 있는 연구이다.
