---
title: "2019_iCub3_Avatar_System_Enabling_Remote_Fully-Immersive_Embodime"
authors:
  - "Stefano Dafarra"
  - "Ugo Pattacini"
  - "Giulio Romualdi"
  - "Lorenzo Rapetti"
  - "Riccardo Grieco"
date: "2022.03"
doi: ""
arxiv: ""
score: 4.0
essence: "원격 위치에서 휴머노이드 로봇 iCub3을 구현화(embodiment)하는 완전한 아바타 시스템을 제시하며, 수백 km 떨어진 위치에서의 이동, 조작, 음성, 표정 제어와 시각, 청각, 촉각, 무게감 피드백을 통합한다."
tags:
  - "cat/Humanoid_Locomotion_and_Control"
  - "sub/Character_Motion_Policy_Transfer"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Dafarra et al._2022_iCub3 Avatar System Enabling Remote Fully-Immersive Embodiment of Humanoid Robots.pdf"
---

# iCub3 Avatar System: Enabling Remote Fully-Immersive Embodiment of Humanoid Robots

> **저자**: Stefano Dafarra, Ugo Pattacini, Giulio Romualdi, Lorenzo Rapetti, Riccardo Grieco, Kourosh Darvish, Gianluca Milani, Enrico Valli, Ines Sorrentino, Paolo Maria Viceconte, Alessandro Scalzo, Silvio Traversaro, Carlotta Sartore, Mohamed Elobaid, Nuno Guedelha, Connor Herron, Alexander Leonessa, Francesco Draicchio, Giorgio Metta, Marco Maggiali, Daniele Pucci | **날짜**: 2022-03-14 | **URL**: [https://arxiv.org/abs/2203.06972](https://arxiv.org/abs/2203.06972)

---

## Essence


원격 위치에서 휴머노이드 로봇 iCub3을 구현화(embodiment)하는 완전한 아바타 시스템을 제시하며, 수백 km 떨어진 위치에서의 이동, 조작, 음성, 표정 제어와 시각, 청각, 촉각, 무게감 피드백을 통합한다.

## Motivation

- **Known**: 텔레존재(telexistence) 기술과 휴머노이드 로봇이 원격 상호작용의 효율성을 높일 수 있으며, 바이페달 설계는 제한된 공간에서 복잡한 움직임을 수행할 수 있다는 것이 알려져 있다. ANA Avatar XPrize 경쟁은 아바타 시스템의 실질적인 검증 플랫폼이 되었다.
- **Gap**: 기존 휴머노이드 아바타 시스템은 주로 조작과 이동을 분리하거나 외골격(exoskeleton)을 통한 침습적 제어에 의존하며, 바이페달 이동성을 포함한 완전한 신체 제어와 다중 감각 피드백을 동시에 지원하는 통합 시스템이 부족하다.
- **Why**: COVID-19와 같은 생물학적 재해 상황에서 원격 신체 아바타 기술의 필요성이 증대되었으며, 사회적 현존감과 물리적 상호작용이 요구되는 응용 분야에서 휴머노이드 아바타의 인간 유사성과 안정성을 갖춘 시스템이 중요하다.
- **Approach**: 15년의 iCub 개발 축적을 바탕으로 개선된 iCub3과 iFeel 커스텀 웨어러블 기술을 결합하여 경량의 비침습적 오퍼레이터 장비를 구성하고, 로봇의 자율적 안정성 제어와 오퍼레이터의 고수준 의도 명령을 통합한다.

## Achievement


- **통합 신체 제어**: 이동, 조작, 음성, 표정을 포함한 휴머노이드 로봇의 완전한 신체 제어 시스템 구현
- **다중 감각 피드백**: 시각, 청각, 촉각, 무게감, 터치 모달리티를 포함한 포괄적 피드백 제공
- **원거리 실제 검증**: Biennale di Venezia(290 km), We Make Future(300 km)에서의 성공적인 원격 상호작용 실증
- **대규모 공중 참여**: 약 2000명의 관중 앞에서 페이로드 운반 작업 수행
- **경쟁 검증**: ANA Avatar XPrize 최종 단계에서 바이페달 이동을 활용한 유일한 팀의 성공

## How

![Figure 4](figures/fig4.webp)

*Figure 4(D) shows the CoM tracking of the balancing controller described in the Methods,*

- iFeel 웨어러블 장치를 통한 모션 및 힘 추적과 retargeting 알고리즘
- 로봇의 자율적 균형 제어를 통한 바이페달 이동 안정성 확보
- ROS/YARP 미들웨어를 이용한 지연 네트워크 환경에서의 통신 레이어 구현
- 터치 센서와 haptic 피드백을 통한 물리적 상호작용 감지 및 전달
- 얼굴 표정 제어 알고리즘을 통한 사회적 현존감 강화

## Originality

- 기존 아바타 시스템의 바이페달 이동성, 조작, 감정 표현을 통합한 첫 번째 완전한 휴머노이드 아바타 시스템
- 외골격 없이 경량 웨어러블만으로 안정적인 원격 바이페달 이동 제어 달성
- 수백 km 규모의 실제 환경에서 다중 감각 피드백과 대규모 공중 참여를 포함한 통합 검증
- 15년 iCub 개발의 누적 기술을 활용한 최신 휴머노이드 플랫폼 제시

## Limitation & Further Study

- 네트워크 지연에 따른 실시간 제어의 한계와 지연 보상 메커니즘의 구체적 성능 분석 부족
- 오퍼레이터의 embodiment 정도를 정량적으로 측정하는 심리학적 평가 지표 미제시
- 대규모 공중 환경에서의 시스템 안정성과 오류 복구 메커니즘에 대한 상세 논의 부족
- 여러 오퍼레이터의 동시 제어 또는 자율성과의 하이브리드 제어 모드에 대한 확장 가능성 미탐색
- 후속 연구로 신경 인터페이스 기반 제어, 강화학습 기반 자율 협력 모드, 다중 감각 피드백의 최적화 방안 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 휴머노이드 아바타의 완전한 신체 제어와 다중 감각 피드백을 통합하여 원격 현존감을 실현한 획기적인 시스템을 제시하며, 실제 환경에서의 대규모 검증을 통해 그 실용성을 입증했다. 네트워크 지연 처리와 embodiment 평가의 정량화 측면에서 개선의 여지가 있으나, 전체적으로 로보틱스와 텔레현존 분야에 중요한 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/2077_Learning_with_pyCub_A_Simulation_and_Exercise_Framework_for/review]] — pyCub 시뮬레이션 프레임워크가 iCub3 아바타 시스템의 교육 및 연구 기반을 제공한다.
- 🔗 후속 연구: [[papers/1814_Being-H0_Vision-Language-Action_Pretraining_from_Large-Scale/review]] — iCub3의 완전 구현화가 대규모 인간 데이터 기반 vision-language-action 사전 훈련으로 발전할 수 있다.
- 🏛 기반 연구: [[papers/1819_Beyond_Tools_and_Persons_Who_Are_They_Classifying_Robots_and/review]] — 원격 완전 몰입형 embodiment 시스템의 법적 윤리적 분류에 CPST 공간 이론의 기반 프레임워크를 적용할 수 있습니다.
- 🔗 후속 연구: [[papers/1933_FRAME_Floor-aligned_Representation_for_Avatar_Motion_from_Eg/review]] — FRAME의 일인칭 시점 자세 추정 기술을 iCub3 Avatar System의 fully-immersive embodiment와 결합하면 더 정확한 원격 제어가 가능하다.
- 🔄 다른 접근: [[papers/2044_Learning_Aerodynamics_for_the_Control_of_Flying_Humanoid_Rob/review]] — 둘 다 비행 휴머노이드이지만 Learning Aerodynamics는 공기역학 학습, iCub3 Avatar는 원격 몰입형 구현 중심
