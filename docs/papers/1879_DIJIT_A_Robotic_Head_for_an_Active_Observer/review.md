---
title: "1879_DIJIT_A_Robotic_Head_for_an_Active_Observer"
authors:
  - "Mostafa Kamali Tabrizi"
  - "Mingshi Chi"
  - "Bir Bikram Dey"
  - "Yu Qing Yuan"
  - "Markus D. Solbach"
date: "2025.12"
doi: ""
arxiv: ""
score: 4.0
essence: "인간의 시각 체계를 모방한 생체모방 쌍안 로봇 헤드 DIJIT를 제시하며, 9개의 기계적 자유도와 4개의 광학적 자유도를 통해 능동적 시각 연구와 인간 시각의 안구-머리 운동을 탐구한다."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "sub/Laparoscopic_Teleoperation_Systems"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Tabrizi et al._2025_DIJIT A Robotic Head for an Active Observer.pdf"
---

# DIJIT: A Robotic Head for an Active Observer

> **저자**: Mostafa Kamali Tabrizi, Mingshi Chi, Bir Bikram Dey, Yu Qing Yuan, Markus D. Solbach, Yiqian Liu, Michael Jenkin, John K. Tsotsos | **날짜**: 2025-12-08 | **URL**: [https://arxiv.org/abs/2512.07998](https://arxiv.org/abs/2512.07998)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

인간의 시각 체계를 모방한 생체모방 쌍안 로봇 헤드 DIJIT를 제시하며, 9개의 기계적 자유도와 4개의 광학적 자유도를 통해 능동적 시각 연구와 인간 시각의 안구-머리 운동을 탐구한다.

## Motivation

- **Known**: 로봇 시각 시스템은 고정된 쌍안 스테레오 카메라나 pan-tilt 구조에 제한되어 있으며, 기존 생체모방 로봇 헤드들은 무게, 크기, 자유도 측면에서 인간 시각계를 완전히 구현하지 못했다.
- **Gap**: 기존 로봇 헤드는 인간과 유사한 기준선(baseline), 기계적 자유도, 광학적 자유도를 모두 갖추면서도 saccade 성능을 정량적으로 보고한 시스템이 부족했다.
- **Why**: 인간 시각과 컴퓨터 시각의 차이를 탐구하기 위해 능동 시각 연구가 중요하며, 인간 수준의 빠른 안구 운동(saccade)은 생물학적 능동 시각의 필수 요소이다.
- **Approach**: 인간의 안구 운동 범위와 속도에 맞춘 9개 자유도의 기계적 설계와 homography 기반의 saccade 제어 방법을 개발하여 카메라 방향과 모터 값 간의 직접적 관계를 수립했다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **완전한 자유도 구현**: 각 카메라마다 pan, tilt, roll의 3개 자유도와 neck에 3개의 자유도(pan, side-bending, flexion/extension)를 추가로 4개의 광학적 자유도를 제공하여 총 13개 자유도 확보
- **인간 수준의 성능**: saccade 피크 속도가 인간 성능의 85% 이상을 달성하며 정확도는 인간과 비교 가능한 수준 달성
- **컴팩트 설계**: 헤드 크기 22cm×18cm×12cm(목 제외), 전체 크기 22cm×22cm×26cm으로 모바일 플랫폼 탑재에 적합
- **인간과 유사한 기준선**: 115mm의 inter-camera baseline으로 인간(45-80mm)과 유사한 수준의 스테레오 기하학 구현
- **새로운 saccade 제어 방법**: 광범위한 학습이나 동적/운동학 모델링 없이 homography를 이용한 효율적인 saccade 실행 방법 제시

## How


- 9개의 기계적 자유도: neck에 3DOF(pan, side-bending, flexion/extension), 각 카메라에 3DOF(pan, tilt, roll)를 독립적으로 구현
- 4개의 광학적 자유도: 각 카메라 마다 초점 거리, 초점 위치, 조리개, 렌즈 선택으로 구성
- Homography 기반 saccade 제어: 카메라 방향 변화를 모터 값으로 직접 매핑하여 복잡한 동역학 모델링 회피
- vergence, version, cyclotorsion 운동 범위 포함: 수렴 스테레오 시각에 필요한 모든 안구 운동 구현
- 온라인 학습 대신 calibration 기반 접근: 사전 학습 데이터 수집의 부담을 제거한 효율적인 calibration 방식 적용

## Originality

- **최초 달성**: 인간 수준의 기준선과 자유도(각 눈 3DOF, 목 3DOF)를 모두 갖춘 동시에 4개의 광학적 자유도를 포함하고 saccade 성능을 정량화한 최초 로봇 헤드
- **Homography 기반 사카드 제어**: COG의 온라인 학습 방식(90분 calibration)을 개선하여 사전 정의된 homography를 이용한 신속하고 효율적인 방법 제시
- **체계적 비교**: 기존 24개 로봇 헤드와의 상세 비교표(Table I)를 통해 DIJIT의 위치 명확히 제시
- **Open-source 공개**: 3D 모델, 부품 목록, 소프트웨어 코드를 MIT 라이센스로 완전 공개

## Limitation & Further Study

- **Primary saccade 중심**: 인간의 다단계 saccade 전략 중 corrective saccade는 부분적으로만 다루어짐
- **정확도 85% 수준**: 피크 속도가 인간의 85% 수준이므로 고속 추적 작업에서의 성능 제약 가능성
- **광학 수차 미논의**: 4개의 광학적 자유도가 정의되었으나 초점 거리, 조리개 등의 상호작용과 광학 수차 특성 분석 부재
- **실제 능동 시각 작업 평가 미흡**: 논문은 saccade 운동 성능 평가에 집중하며 SLAM, 객체 인식 등 실제 시각 작업에서의 이점 검증 부족
- **후속 연구**: 능동 시각 연구와 human-machine vision 비교 연구가 진행 중이며, cyclotorsion, vergence 등 추가 자유도의 유용성 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: DIJIT은 인간 시각의 핵심 특성을 종합적으로 구현한 최초의 로봇 헤드로, 생체모방 설계와 실제 saccade 성능 평가를 통해 능동 시각 연구의 새로운 플랫폼을 제공한다. 완전 공개된 설계와 체계적인 비교 분석은 후속 로봇 시각 연구에 중요한 기여를 할 수 있다.

## Related Papers

- 🧪 응용 사례: [[papers/1713_Thinking_in_360_Humanoid_Visual_Search_in_the_Wild/review]] — DIJIT의 생체모방 쌍안 로봇 헤드 기술이 실제 환경에서 360도 시각 탐색을 수행하는 구체적 응용사례입니다.
- 🏛 기반 연구: [[papers/1750_Vision_in_Action_Learning_Active_Perception_from_Human_Demon/review]] — 인간 시연으로부터 능동 지각을 학습하는 방법론이 DIJIT의 능동적 시각 연구 기반이 됩니다.
- 🔄 다른 접근: [[papers/2070_Learning_to_Look_Around_Enhancing_Teleoperation_and_Learning/review]] — Learning to Look Around은 텔레오퍼레이션용 능동 목 제어, DIJIT은 일반적인 능동 관찰자용 로봇 헤드로 서로 다른 응용 목적을 가진다.
