---
title: "1634_Realistic_Lip_Motion_Generation_Based_on_3D_Dynamic_Viseme_a"
authors:
  - "| **날짜**: 2026-03-29"
date: "2026.03"
doi: ""
arxiv: ""
score: 4.0
essence: "인간-로봇 상호작용을 위해 3D 동적 비셈(viseme)과 공명음현상(coarticulation) 모델링 기반의 입술 운동 생성 프레임워크를 제안하며, 고차원 공간 입술 운동을 14-DOF 로봇 입술 구동 시스템으로 변환한다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Language-Guided_Robot_Motion_Planning"
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/Text-Conditioned_Motion_Generation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/2026_Realistic Lip Motion Generation Based on 3D Dynamic Viseme and Coarticulation Modeling for Human-Rob 1.pdf"
---

# Realistic Lip Motion Generation Based on 3D Dynamic Viseme and Coarticulation Modeling for Human-Robot Interaction

> **저자**:  | **날짜**: 2026-03-29 | **URL**: [https://arxiv.org/abs/2604.01756](https://arxiv.org/abs/2604.01756)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

인간-로봇 상호작용을 위해 3D 동적 비셈(viseme)과 공명음현상(coarticulation) 모델링 기반의 입술 운동 생성 프레임워크를 제안하며, 고차원 공간 입술 운동을 14-DOF 로봇 입술 구동 시스템으로 변환한다.

## Motivation

- **Known**: 기존 음소-비셈 매핑 기반 규칙 방식과 Wav2Lip, KMTalker 등 end-to-end 딥러닝 방식이 있으나, 전자는 정적 2D 모델링으로 동적 특성을 손실하고 중국어 공명음현상을 반영하지 못하며, 후자는 차원 격차와 실시간 성능 문제를 가진다.
- **Gap**: 중국어의 복잡한 음절과 공명음현상을 고려한 동적 3D 비셈 모델이 부족하고, 고차원 얼굴 특징을 저차원 로봇 구동계로 효율적으로 변환하는 경량 방법론이 없다.
- **Why**: 입술 동기화는 McGurk 효과를 통해 청각 인식을 향상시키고, 소음 환경에서 약 15 dB SNR 향상 효과를 제공하며, 청각장애인과 노인에게 이해도를 20-60% 개선시켜 자연스러운 인간-로봇 상호작용을 실현한다.
- **Approach**: ARKit 표준 52개 블렌드셰이프 중 27개 핵심 기저를 추출하여 3D 동적 비셈 라이브러리를 구성하고, 중국어 음성학의 초성-운모(Shengmu-Yunmu) 분리와 에너지 조절을 통해 공명음현상을 해결한 후, 운동 맵핑과 하이브리드 캘리브레이션으로 로봇 배포를 실현한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- **3D 동적 비셈 라이브러리**: 14개 범주의 3D 동적 비셈 시퀀스를 구성하여 기존 2D 정적 매핑의 한계를 극복하고 비선형 입술 궤적을 재현
- **초성-운모 분리 기반 공명음현상 모델**: 중국어의 독특한 음절 특성에 맞춘 融合 알고리즘으로 인접 음소 간 운동 충돌을 해결하고 자연스러운 동적 긴장감 구현
- **경량 배포 방법**: 고차원 얼굴 특징을 14-DOF 저차원 로봇 제어로 변환하는 차원 축소 및 하이브리드 캘리브레이션으로 실시간 로봇 구동 실현
- **정량적 검증**: Pearson Correlation Coefficient(PCC)와 Mean Absolute Jerk(MAJ) 메트릭을 이용한 절제 실험으로 효율성과 정확도 입증

## How

![Figure 3](figures/fig3.webp)

*Fig. 3.*

- ARKit 표준의 52개 얼굴 블렌드셰이프 중 jawOpen, mouthFunnel 등 입술 운동과 강한 상관성을 가진 27개 핵심 기저 추출
- 중국어 음성학 구조에 따라 21개 초성과 39개 운모로 구성된 60개 이상 병음 조합을 시각적 형태학적 특성에 기반하여 14개 비셈으로 차원 축소
- 깊이 센싱 기술로 연속 발음 중 입술 근육 운동 추적 및 주기적 입술 운동 데이터 수집
- 초성-운모 분리를 통해 인접 비셈 간 공명음 충돌 해결 및 에너지 조절로 자연스러운 궤적 생성
- 고차원 공간 입술 운동을 14-DOF 로봇 시스템으로 매핑하기 위한 역기구학(inverse kinematics) 기반 차원 축소 및 하이브리드 캘리브레이션 메커니즘 적용

## Originality

- 기존 정적 2D 비셈 모델에서 벗어나 ARKit 기반 3D 동적 비셈 라이브러리를 구성한 혁신적 접근
- 중국어의 초성-운모 분리 구조를 명시적으로 반영하여 공명음현상을 체계적으로 해결하는 언어학 기반 모델링
- 규칙 기반과 딥러닝 기반의 장점을 결합하여 경량, 해석 가능하면서도 고성능의 하이브리드 프레임워크 제안

## Limitation & Further Study

- 현재는 중국어만 지원하므로 다른 언어(영어, 일본어 등)로의 확장을 위한 추가 연구 필요
- ARKit 기반 데이터 수집이 특정 환경(조명, 각도)에 의존하므로 데이터 다양성 확대 필요
- 14-DOF 로봇 플랫폼 특정으로 개발되어 다른 로봇 형태로의 적응성 개선 필요
- 실시간 성능 검증이 제시되었으나 더 높은 주파수 프레임레이트(60+ fps)에서의 성능 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 연구는 3D 동적 비셈과 중국어 언어학적 특성을 결합하여 입술 동기화의 근본적 한계를 해결한 학제적 기여로, 경량하고 실용적인 로봇 배포 프레임워크를 통해 인간-로봇 상호작용의 자연성을 크게 향상시킨다.

## Related Papers

- 🏛 기반 연구: [[papers/1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f/review]] — 음성-제스처 생성 시스템이 입술 운동의 3D 동적 비셈 모델링을 포함한 종합적인 인간-로봇 상호작용 기반
- 🔗 후속 연구: [[papers/1672_SignBot_Learning_Human-to-Humanoid_Sign_Language_Interaction/review]] — SignBot의 수화 인식/생성이 입술 운동 생성을 포함한 다중 모달 소통 시스템으로 확장된 형태
- 🏛 기반 연구: [[papers/1962_H-Zero_Cross-Humanoid_Locomotion_Pretraining_Enables_Few-sho/review]] — H-RDT의 인간 시연 기반 조작 학습이 입술 운동의 coarticulation 모델링에 필요한 인간 발화 패턴 이해를 제공한다
- 🏛 기반 연구: [[papers/1912_EMOTION_Expressive_Motion_Sequence_Generation_for_Humanoid_R/review]] — EMOTION의 표현적 모션 생성 기술이 입술 운동의 감정적 표현력을 향상시키는 기반이 된다
- 🏛 기반 연구: [[papers/1669_Semantic_Co-Speech_Gesture_Synthesis_and_Real-Time_Control_f/review]] — 입술 운동 생성의 3D 동적 모델링이 음성 기반 제스처 생성의 다중 모달 표현 기반
- 🔗 후속 연구: [[papers/1672_SignBot_Learning_Human-to-Humanoid_Sign_Language_Interaction/review]] — 입술 운동 생성을 포함한 SignBot의 수화 시스템이 전체적인 인간-휴머노이드 소통으로 확장
