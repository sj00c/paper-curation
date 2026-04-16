---
title: "1546_Robot_Utility_Models_General_Policies_for_Zero-Shot_Deployme"
authors:
  - "Haritheja Etukuru"
  - "Norihito Naka"
  - "Zijin Hu"
  - "Seungjae Lee"
  - "Julian Mehu"
date: "2024.09"
doi: ""
arxiv: ""
score: 4.0
essence: "Robot Utility Models (RUM)은 다양한 환경에서 수집한 대규모 데이터로 학습하여 새로운 환경에서 파인튜닝 없이 즉시 배포 가능한 로봇 정책 프레임워크이다. 90% 성공률로 미지의 환경과 객체에 대해 zero-shot 일반화를 달성한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Instruction-Following_Robot_Navigation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Etukuru et al._2024_Robot Utility Models General Policies for Zero-Shot Deployment in New Environments.pdf"
---

# Robot Utility Models: General Policies for Zero-Shot Deployment in New Environments

> **저자**: Haritheja Etukuru, Norihito Naka, Zijin Hu, Seungjae Lee, Julian Mehu, Aaron Edsinger, Chris Paxton, Soumith Chintala, Lerrel Pinto, Nur Muhammad Mahi Shafiullah | **날짜**: 2024-09-09 | **URL**: [https://arxiv.org/abs/2409.05865](https://arxiv.org/abs/2409.05865)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Robot Utility Models are trained on a diverse set of environments and objects, and then*

Robot Utility Models (RUM)은 다양한 환경에서 수집한 대규모 데이터로 학습하여 새로운 환경에서 파인튜닝 없이 즉시 배포 가능한 로봇 정책 프레임워크이다. 90% 성공률로 미지의 환경과 객체에 대해 zero-shot 일반화를 달성한다.

## Motivation

- **Known**: 대규모 데이터로 학습한 로봇 모델은 뛰어난 조작 및 네비게이션 능력을 보여주며, 동일 환경 내에서의 변동에 대한 일반화가 가능하다. 그러나 새로운 환경마다 파인튜닝이 필요하다는 점이 vision/language 모델의 zero-shot 배포와 대비된다.
- **Gap**: 기존 로봇 정책은 새로운 환경에 배포할 때마다 환경 특화 데이터를 수집하여 파인튜닝해야 하는데, vision 및 language 모델처럼 추가 학습 없이 open-world 문제에 zero-shot으로 배포 가능한 일반적인 로봇 정책이 부재하다.
- **Why**: 로봇의 상용화와 실제 배포 시 매번 새로운 환경에서 데이터를 수집하고 학습하는 것은 비용과 시간 면에서 매우 비효율적이므로, zero-shot 일반화 능력을 갖춘 유틸리티 정책은 로봇의 실용성을 크게 향상시킬 수 있다.
- **Approach**: Stick-v2라는 저비용 데이터 수집 도구로 다양한 환경에서 대규모 고품질 시연 데이터를 수집하고, multi-modal imitation learning으로 정책을 학습한 후, mLLM 기반 self-critique과 retrying을 통해 zero-shot 배포 성능을 향상시킨다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Robot Utility Models are trained on a diverse set of environments and objects, and then*

- **Zero-shot 배포 성능**: 25개의 미지 환경에서 평균 90% 성공률을 달성하여 파인튜닝 없이도 새로운 환경에 즉시 배포 가능함을 입증
- **다중 로봇 및 센서 호환성**: 다양한 로봇 암, 카메라 설정, 조명 조건에서 추가 데이터나 학습 없이 성공
- **데이터 효율성**: 약 1,000개 정도의 적당한 규모 데이터로도 일반적인 유틸리티 모델 개발 가능
- **실용적 파이프라인**: 5가지 manipulation 작업(문 열기, 서랍 열기, 냅킨 집기, 종이봉투 집기, 떨어진 객체 재배치)에 대해 실제 배포된 RUM 제공
- **자체 비판 시스템**: mLLM 기반 failure detection 및 retrying으로 성공률을 15.6% 추가 개선

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Stick-v2, our data collection tool (left: real photo, right: render), is built out of an iPhone*

- **Stick-v2 데이터 수집 도구**: iPhone Pro 기반의 $25 저비용 휴대용 도구로 RGB, depth, 6D pose를 60-100Hz로 수집
- **다양성 중심 데이터 전략**: 여러 지리적 위치(NYC, Jersey City, Pittsburgh)의 다양한 환경과 객체에서 데이터 수집하여 환경 다양성 극대화
- **Multi-modal imitation learning**: 고품질 시연 데이터를 다중 모달리티로 학습하는 최신 행동 모델링 알고리즘 활용
- **On-device 정책 배포**: Hello Robot Stretch 등 저비용 범용 로봇에 정책 탑재 및 실행
- **mLLM 기반 self-critique**: 독립적인 multimodal LLM을 활용한 failure detection 및 automated retrying 메커니즘
- **하드웨어 추상화**: 카메라 설정, 로봇 암 구성 변경에 robust한 정책 설계

## Originality

- 기존 pretrain-then-finetune 패러다임에서 벗어나 **zero-shot 로봇 정책 배포** 개념의 체계적 구현
- **Stick-v2 설계**: 휴대성, 정확도, 빠른 설정을 모두 충족하는 실용적 데이터 수집 도구 개발
- **데이터 다양성의 중요성 검증**: 데이터 양보다 다양성이 zero-shot 일반화에 더 중요함을 실증적으로 입증
- **mLLM 기반 로봇 introspection**: 언어 모델의 자체 비판 능력을 로봇 정책의 failure recovery에 적용한 창의적 접근
- **전체 스택 오픈소싱**: 코드, 데이터, 모델, 하드웨어 설계, 실험 영상 등을 공개하여 재현성과 커뮤니티 확장 가능성 제공

## Limitation & Further Study

- **작업 범위 제한**: 5가지 특정 manipulation 작업에 한정되어 있으며, 다른 복잡한 작업으로의 확장 가능성 미검증
- **실패 사례 분석 부족**: 90% 성공률의 10% 실패 케이스에 대한 상세한 분석 및 실패 원인 분류 부재
- **데이터 규모의 정확한 필요량**: 약 1,000개가 '적당한' 규모라고 제시하지만, 작업별 또는 환경 복잡도별 필요 데이터량의 정확한 특성화 부족", '**하드웨어 일반화의 한계**: 서로 다른 로봇 플랫폼에서의 테스트가 제한적이며, 대형 산업용 로봇이나 다완 로봇에서의 성능 미확인
- **실시간 성능 및 계산량**: on-device 배포 시 추론 속도, 메모리 요구사항, mLLM verifier의 실시간 성능에 대한 상세 분석 부족
- **후속 연구 방향**: 더 복잡한 멀티스텝 작업, 동적 환경 처리, 사용자 피드백 통합, 자동 데이터 샘플링 전략 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 로봇 정책의 zero-shot 일반화라는 중요한 문제를 체계적인 엔지니어링 접근으로 해결하며, 실용적인 데이터 수집 도구, 효과적인 학습 및 배포 파이프라인, 혁신적인 mLLM 기반 실패 복구 메커니즘을 제시한다. 2,950회의 실제 로봇 롤아웃과 오픈소싱된 리소스를 통해 강력한 실증적 기여를 이루었으나, 다양한 작업/로봇 플랫폼으로의 확장성과 상세한 실패 분석이 향후 과제로 남아있다.

## Related Papers

- 🔄 다른 접근: [[papers/1535_RoboArena_Distributed_Real-World_Evaluation_of_Generalist_Ro/review]] — RoboArena와 함께 범용 로봇 정책의 실제 평가를 다루지만 RUM은 제로샷 배포에, RoboArena는 분산 평가에 초점을 맞춘다.
- 🏛 기반 연구: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — Octo의 오픈소스 범용 로봇 정책 연구가 RUM의 다양한 환경에서 즉시 배포 가능한 정책 개발에 기술적 기초를 제공한다.
- 🔗 후속 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — RT-1의 로봇 제어 능력을 다양한 환경에서 수집한 대규모 데이터로 확장하여 zero-shot 일반화를 달성하는 발전된 형태이다.
- 🏛 기반 연구: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Open X-Embodiment의 대규모 로봇 데이터셋과 RT-X 모델이 Robot Utility Models의 zero-shot 배포 능력 개발에 핵심 기반을 제공한다.
- 🔄 다른 접근: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — 새로운 환경에서의 로봇 배포를 RUM은 zero-shot으로, Scaling Cross-Embodied Learning은 하나의 정책으로 해결하는 다른 접근법이다.
- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — RUM과 OpenVLA 모두 범용 로봇 정책을 다루지만 zero-shot 배포와 대규모 사전훈련이라는 다른 접근법을 사용합니다.
- 🧪 응용 사례: [[papers/1369_Do_As_I_Can_Not_As_I_Say_Grounding_Language_in_Robotic_Affor/review]] — Robot Utility Models의 제로샷 배포는 Do As I Can의 LLM affordance function grounding을 실제 로봇 정책으로 구현한다.
