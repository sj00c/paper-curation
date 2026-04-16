---
title: "1663_SafeHumanoid_VLM-RAG-driven_Control_of_Upper_Body_Impedance"
authors:
  - "Yara Mahmoud"
  - "Jeffrin Sam"
  - "Nguyen Khang"
  - "Marcelino Fernando"
  - "Issatay Tokmurziyev"
date: "2025.11"
doi: ""
arxiv: ""
score: 4.0
essence: "SafeHumanoid는 Vision Language Model(VLM)과 Retrieval-Augmented Generation(RAG)을 활용하여 휴머노이드 로봇의 임피던스와 속도를 동적으로 조정하는 시스템으로, 인간-로봇 상호작용 시 안전성과 작업 완료를 동시에 달성한다."
tags:
  - "cat/Robotic_Manipulation_and_Teleoperation"
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "sub/Dexterous_Hand_Trajectory_Datasets"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Mahmoud et al._2025_SafeHumanoid VLM-RAG-driven Control of Upper Body Impedance for Humanoid Robot.pdf"
---

# SafeHumanoid: VLM-RAG-driven Control of Upper Body Impedance for Humanoid Robot

> **저자**: Yara Mahmoud, Jeffrin Sam, Nguyen Khang, Marcelino Fernando, Issatay Tokmurziyev, Miguel Altamirano Cabrera, Muhammad Haris Khan, Artem Lykov, Dzmitry Tsetserukou | **날짜**: 2025-11-28 | **URL**: [https://arxiv.org/abs/2511.23300](https://arxiv.org/abs/2511.23300)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Egocentric perception and semantic-to-safety*

SafeHumanoid는 Vision Language Model(VLM)과 Retrieval-Augmented Generation(RAG)을 활용하여 휴머노이드 로봇의 임피던스와 속도를 동적으로 조정하는 시스템으로, 인간-로봇 상호작용 시 안전성과 작업 완료를 동시에 달성한다.

## Motivation

- **Known**: 임피던스 제어는 안전한 인간-로봇 상호작용을 위한 표준 도구이며, VLM은 로봇 작업 시퀀스 생성 및 궤적 생성에 활용되고 있다.
- **Gap**: 기존 VLM/VLA 파이프라인은 작업 완료와 위치 제어에 중점을 두며 임피던스 거동 변조를 고려하지 않으며, 의미론적 추론과 안전 임피던스 제어의 통합이 부족하다.
- **Why**: 로봇이 공유된 인간 환경에서 작동할 때 단순한 기하학적 안전장치로는 부족하며, 작업과 맥락을 이해하고 사전에 적절한 강성과 속도를 선택하는 것이 사용자 안전과 신뢰도를 향상시킨다.
- **Approach**: 자중심 비전으로 장면을 캡처하고 VLM 프롬프트로 의미론적 정보를 추출한 후, FAISS 기반 RAG를 통해 검증된 시나리오 데이터베이스에서 임피던스 파라미터(Kp, Kd, v)를 검색하고 역운동학으로 관절 명령으로 변환한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: SafeHumanoid pipeline architecture. The onboard PC streams egocentric frames and executes impedance control at*

- **VLM-RAG 제어 파이프라인**: 자중심 비전과 구조화된 VLM 프롬프트를 활용하여 실시간으로 맥락 인식 임피던스 및 속도 파라미터를 선택
- **실제 시스템 통합**: Unitree G1 휴머노이드 로봇에서 고수준 의미론적 추론과 저수준 상체 제어의 완전한 통합 달성
- **적응적 거동**: 테이블 닦이, 물체 인수인계, 액체 붓기 작업에서 고정 게인 기준선 대비 더 안전하고 맥락 인식적인 거동을 유지하면서 작업 성공률 보장
- **표준 준수**: ISO/TS 15066과 ISO 13855 같은 협력 로봇 안전 표준을 고려한 파라미터 선택

## How

![Figure 2](figures/fig2.webp)

*Figure 2: SafeHumanoid pipeline architecture. The onboard PC streams egocentric frames and executes impedance control at*

- 자중심 카메라에서 egocentric frames 획득
- 구조화된 VLM 프롬프트를 사용한 Molmo VLM으로 장면 의미론적 분석
- VLM 임베딩을 FAISS 검색 엔진으로 검증된 시나리오 데이터베이스와 매칭
- 검색된 파라미터(Kp, Kd, v)를 역운동학과 중력 보상을 통해 관절 명령{qref, q̇ref, τff, Kp, Kd}으로 변환
- 온보드 PC에서 50 Hz로 제어 실행, 오프보드 워크스테이션에서 VLM 및 RAG 처리

## Originality

- 의미론적 추론을 안전 임피던스 제어 계층과 직접 통합한 최초 시도
- 휴머노이드 HRI에서 VLM+RAG 파이프라인을 적용한 첫 번째 구체적 구현
- 작업과 인간 근접성 맥락에서 동적 스티프니스, 댐핑, 속도 조정의 새로운 접근
- 궤적 생성 방식과 무관하게 작동하는 범용 compliance layer 개발

## Limitation & Further Study

- 현재 추론 지연시간(최대 1.4초)으로 인해 매우 동적인 환경에서 즉각적 대응 제한
- 시나리오 데이터베이스의 규모와 다양성에 따른 성능 의존성
- 오프보드 처리 필요로 인한 실시간성 제약 및 통신 지연 위험
- 테이블탑 작업 중심의 평가로 전신 이동 작업에 대한 검증 부족
- 후속연구: 온디바이스 VLM 최적화로 지연시간 감소, 더 포괄적인 시나리오 데이터베이스 구축, 동적 환경에서의 실시간 적응 메커니즘 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: SafeHumanoid는 의미론적 추론과 임피던스 제어의 혁신적 결합으로 인간-로봇 협력의 안전성을 크게 향상시키는 제안이지만, 추론 지연시간과 실시간성은 실제 배포를 위해 해결해야 할 주요 과제이다.

## Related Papers

- 🔄 다른 접근: [[papers/2012_HumanoidVLM_Vision-Language-Guided_Impedance_Control_for_Con/review]] — 두 논문 모두 VLM을 활용한 휴머노이드 제어를 다루지만, 안전성 중심과 일반적인 임피던스 제어라는 다른 관점을 가진다.
- 🏛 기반 연구: [[papers/1847_Commanding_Humanoid_by_Free-form_Language_A_Large_Language_A/review]] — 자유형식 언어 명령을 통한 휴머노이드 제어의 기본 개념을 제공한다.
- 🔗 후속 연구: [[papers/1915_Endowing_GPT-4_with_a_Humanoid_Body_Building_the_Bridge_Betw/review]] — GPT-4와 휴머노이드 결합 연구를 VLM-RAG로 확장하여 더 안전하고 적응적인 상호작용을 실현한다.
- 🔗 후속 연구: [[papers/1671_SHIELD_Safety_on_Humanoids_via_CBFs_In_Expectation_on_Learne/review]] — SafeHumanoid의 VLM-RAG 기반 안전 제어가 SHIELD의 CBF 기반 안전성 보장과 결합되어 더 포괄적인 human-robot interaction 안전 시스템을 구축할 수 있다
- 🏛 기반 연구: [[papers/1802_An_Empirical_Evaluation_of_Four_Off-the-Shelf_Proprietary_Vi/review]] — SafeHumanoid의 VLM 활용 방식이 Empirical Evaluation of VLMs의 proprietary vision model 평가 결과를 기반으로 최적화될 수 있다
- 🔗 후속 연구: [[papers/1690_Stability-Aware_Retargeting_for_Humanoid_Multi-Contact_Teleo/review]] — SafeHumanoid의 VLM-RAG 기반 임피던스 조정과 다중 접촉 안정성 인식 retargeting을 결합하면 더 안전한 텔레오퍼레이션이 가능하다
- 🔄 다른 접근: [[papers/1686_SPARK_Safe_Protective_and_Assistive_Robot_Kit/review]] — 둘 다 휴머노이드 안전 제어를 다루지만 SafeHumanoid는 VLM-RAG 기반, SPARK는 CBF 기반 접근을 사용한다
- 🏛 기반 연구: [[papers/1686_SPARK_Safe_Protective_and_Assistive_Robot_Kit/review]] — SPARK의 모듈식 안전 제어 알고리즘이 SafeHumanoid의 VLM 기반 안전성 시스템에 기반 컨트롤러를 제공한다
- 🔄 다른 접근: [[papers/1690_Stability-Aware_Retargeting_for_Humanoid_Multi-Contact_Teleo/review]] — 둘 다 휴머노이드 안전성을 다루지만 물리적 안정성 기반 vs VLM-RAG 기반으로 접근 방식이 다르다
- 🔗 후속 연구: [[papers/1974_Hierarchical_Vision-Language_Planning_for_Multi-Step_Humanoi/review]] — SafeHumanoid의 VLM-RAG driven control이 hierarchical VLM planning을 안전성 측면에서 확장합니다.
- 🔄 다른 접근: [[papers/2012_HumanoidVLM_Vision-Language-Guided_Impedance_Control_for_Con/review]] — SafeHumanoid의 VLM-RAG driven control이 HumanoidVLM과 다른 방식으로 vision-language 기반 제어를 구현합니다.
