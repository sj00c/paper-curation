---
title: "1422_Hi_Robot_Open-Ended_Instruction_Following_with_Hierarchical"
authors:
  - "Lucy Xiaoyang Shi"
  - "Brian Ichter"
  - "Michael Equi"
  - "Liyiming Ke"
  - "Karl Pertsch"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "Hi Robot는 계층적 vision-language model 구조를 통해 로봇이 복잡한 자연어 지시사항과 실시간 피드백을 처리하여 개방형 과제를 수행할 수 있도록 하는 시스템이다. 고수준 VLM이 복잡한 프롬프트를 해석하여 원자적 명령어를 생성하고, VLA 정책이 이를 실행하는 두 단계 계층 구조를 제안한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shi et al._2025_Hi Robot Open-Ended Instruction Following with Hierarchical Vision-Language-Action Models.pdf"
---

# Hi Robot: Open-Ended Instruction Following with Hierarchical Vision-Language-Action Models

> **저자**: Lucy Xiaoyang Shi, Brian Ichter, Michael Equi, Liyiming Ke, Karl Pertsch, Quan Vuong, James Tanner, Anna Walling, Haohuan Wang, Niccolo Fusai, Adrian Li-Bell, Danny Driess, Lachy Groom, Sergey Levine, Chelsea Finn | **날짜**: 2025-02-26 | **URL**: [https://arxiv.org/abs/2502.19417](https://arxiv.org/abs/2502.19417)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Open-ended instruction following. Hi Robot enables robots to follow multi-stage instructions, adapt to real-ti*

Hi Robot는 계층적 vision-language model 구조를 통해 로봇이 복잡한 자연어 지시사항과 실시간 피드백을 처리하여 개방형 과제를 수행할 수 있도록 하는 시스템이다. 고수준 VLM이 복잡한 프롬프트를 해석하여 원자적 명령어를 생성하고, VLA 정책이 이를 실행하는 두 단계 계층 구조를 제안한다.

## Motivation

- **Known**: VLA 모델들은 단순한 원자적 지시사항('컵을 들어')을 따를 수 있으며, 일부 LLM/VLM 기반 방법들은 다단계 과제를 분해할 수 있다. 그러나 기존 방법들은 복잡한 프롬프트와 실시간 피드백을 동시에 처리하는 능력이 제한적이다.
- **Gap**: 현재 지시 따르기 방법들은 주로 System 1 수준의 단순 명령 실행에 집중하며, System 2 수준의 고수준 추론이 필요한 '야채 샌드위치를 만들되 토마토는 빼달라'와 같은 복잡한 프롬프트와 실시간 수정('그건 쓰레기가 아니야')을 통합하는 능력이 부족하다.
- **Why**: 개방형 인간-중심 환경에서 로봇의 유연성과 적응성은 필수적이며, 복잡한 자연어 상호작용을 처리할 수 있는 능력은 사용자가 로봇을 새로운 과제로 안내하고 실시간으로 수정할 수 있게 함으로써 로봇의 실용성을 획기적으로 향상시킨다.
- **Approach**: 높은 수준의 VLM과 낮은 수준의 VLA 정책으로 구성된 계층적 구조를 설계하고, 기존 로봇 데이터셋에 대해 VLM을 사용하여 합성적으로 생성한 복잡한 프롬프트와 인간의 개입 예시를 추가하여 고수준 정책을 학습시킨다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5: Comparisons to Prior Methods. Hi Robot outperforms GPT-4o and flat VLA on Table Bussing, Sandwich Making, and*

- **다양한 로봇 플랫폼에서의 검증**: 단팔, 양팔, 양팔 모바일 로봇 3가지 플랫폼에서 테이블 정리, 샌드위치 만들기, 식료품 쇼핑 등 다양한 과제를 성공적으로 수행
- **복잡한 프롬프트 처리**: 기존 VLA 정책보다 훨씬 복잡한 다단계 지시사항, 조건부 명령, 사용자 제약을 이해하고 실행
- **실시간 피드백 통합**: 과제 실행 중 사용자의 수정 사항('더 높게!
- 그건 쓰레기가 아니야')을 동적으로 반영하여 행동 수정", '**GPT-4o 및 평면 VLA 정책 초과**: 비교 실험에서 API 기반 VLM과 평면 VLA 모델을 능가하는 인간 의도 정렬 및 과제 성공률 달성

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Overview of hierarchical VLA. The policy consists*

- 고수준 VLM을 통해 현재 시각 관찰과 사용자 발화를 입력으로 받아 적절한 원자적 명령어(예: 'grasp the cup')와 언어 응답 생성", '저수준 VLA 정책은 생성된 원자적 명령어를 받아 실제 로봇 제어 신호(관절 각도, 그리퍼 명령 등)로 변환하여 실행
- 합성 데이터 생성 방식: 기존 로봇 시연 데이터(관찰-행동 쌍)에 대해 VLM에게 그 행동을 유도했을 법한 복잡한 프롬프트와 인간의 개입을 역생성하도록 지시
- 생성된 합성 데이터(상황에 맞는 복잡한 프롬프트-명령어 쌍)를 고수준 VLM 정책의 학습 데이터로 활용하여 다양한 프롬프트와 피드백에 대한 일반화 능력 확보
- 계층적 구조를 통해 고수준 추론과 저수준 제어를 분리하되, 둘 다 VLM/VLA 기반으로 구현하여 시각 관찰에 대한 풍부한 상황 인식 유지

## Originality

- **계층적 VLM-VLA 결합**: 고수준 복잡 추론과 저수준 정확한 제어를 통합한 새로운 아키텍처로, 기존 end-to-end VLA나 순차적 LLM-기반 방법과 차별화
- **합성 프롬프트 생성**: 기존 로봇 데이터에 VLM을 사용해 상황에 맞는 복잡한 프롬프트와 인간의 개입을 역생성하는 창의적인 데이터 확장 기법
- **실시간 피드백 통합**: 과제 수행 중 사용자의 언어적 수정을 동적으로 처리하는 메커니즘으로, 기존 방법들의 제한을 극복
- **다양한 로봇 플랫폼 검증**: 단일 팔, 양팔, 모바일 로봇에 걸쳐 일관되게 동작하는 범용 시스템 제시

## Limitation & Further Study

- **합성 데이터의 품질 의존성**: 생성된 프롬프트와 개입의 현실성과 다양성이 VLM의 능력에 크게 의존하며, 오류가 학습에 악영향을 미칠 수 있음
- **저수준 VLA 정책의 한계**: 원자적 명령어가 충분히 제어 가능하고 정확해야 하므로, VLA 정책의 성능이 전체 시스템 성능을 제한할 수 있음
- **평가 범위의 제약**: 주로 정리, 음식 준비, 쇼핑 등 특정 도메인 과제에만 테스트되었으며, 더 광범위한 일반화 능력은 미검증
- **계산 비용**: 고수준 VLM을 매 단계마다 실행해야 하므로 실시간성과 에너지 효율성 측면에서 개선 필요
- **후속 연구 방향**: (1) 합성 데이터 생성 과정의 자동화 및 품질 보증, (2) 저수준 VLA의 정확도 향상, (3) 실시간 성능 최적화, (4) 더 복잡한 멀티턴 인간-로봇 대화 처리

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Hi Robot은 계층적 VLM-VLA 구조와 합성 프롬프트 생성을 통해 로봇의 복잡한 지시 따르기와 실시간 피드백 통합 능력을 크게 향상시킨 중요한 기여이다. 다양한 플랫폼에서의 실험 검증과 기존 방법 대비 우수한 성능을 보여주지만, 합성 데이터의 품질, 저수준 정책의 한계, 계산 비용 등에 대한 개선이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1579_Statler_State-Maintaining_Language_Models_for_Embodied_Reaso/review]] — 둘 다 계층적 instruction following을 다루지만 VLM + VLA vs state-maintaining language model이라는 다른 아키텍처를 사용한다.
- 🏛 기반 연구: [[papers/1435_Instruct2Act_Mapping_Multi-modality_Instructions_to_Robotic/review]] — Instruct2Act의 multi-modal instruction mapping을 계층적 VLM 구조로 발전시킨 확장 연구이다.
- 🔗 후속 연구: [[papers/1585_ThinkBot_Embodied_Instruction_Following_with_Thought_Chain_R/review]] — ThinkBot의 thought chain을 계층적 vision-language 구조로 더욱 체계화하여 개방형 과제 수행을 개선했다.
- 🔗 후속 연구: [[papers/1434_Inner_Monologue_Embodied_Reasoning_through_Planning_with_Lan/review]] — Inner Monologue의 LLM 기반 추론을 계층적 VLM 구조로 발전시켜 더 체계적인 개방형 과제 수행을 가능하게 한다.
- 🔄 다른 접근: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — PaLM-E의 단일 모델 접근법과 다르게 고수준 VLM과 VLA 정책을 분리한 계층적 구조를 제안한다.
- 🔄 다른 접근: [[papers/1556_RT-H_Action_Hierarchies_Using_Language/review]] — 로봇의 계층적 제어에서 RT-H는 언어 기반 행동 계층으로, Hi Robot은 오픈엔드 instruction following으로 접근한다.
