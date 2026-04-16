---
title: "1470_MapNav_A_Novel_Memory_Representation_via_Annotated_Semantic"
authors:
  - "Lingfeng Zhang"
  - "Xiaoshuai Hao"
  - "Qinwen Xu"
  - "Qiang Zhang"
  - "Xinyao Zhang"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "MapNav는 Vision-and-Language Navigation에서 Annotated Semantic Map(ASM)을 메모리 표현으로 사용하여 기존의 과거 프레임 저장의 비효율성을 해결하는 end-to-end VLM 기반 모델이다. ASM은 top-down 시멘틱 맵에 텍스트 라벨을 추가하여 구조화된 내비게이션 정보를 제공한다."
tags:
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Visual_Language_Navigation"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Semantic_Navigation_Exploration"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_MapNav A Novel Memory Representation via Annotated Semantic Maps for Vision-and-Language Navigation.pdf"
---

# MapNav: A Novel Memory Representation via Annotated Semantic Maps for Vision-and-Language Navigation

> **저자**: Lingfeng Zhang, Xiaoshuai Hao, Qinwen Xu, Qiang Zhang, Xinyao Zhang, Pengwei Wang, Jing Zhang, Zhongyuan Wang, Shanghang Zhang, Renjing Xu | **날짜**: 2025-02-19 | **URL**: [https://arxiv.org/abs/2502.13451](https://arxiv.org/abs/2502.13451)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Illustration of our Annotated Semantic*

MapNav는 Vision-and-Language Navigation에서 Annotated Semantic Map(ASM)을 메모리 표현으로 사용하여 기존의 과거 프레임 저장의 비효율성을 해결하는 end-to-end VLM 기반 모델이다. ASM은 top-down 시멘틱 맵에 텍스트 라벨을 추가하여 구조화된 내비게이션 정보를 제공한다.

## Motivation

- **Known**: Vision-and-Language Navigation은 자연어 명령을 따르며 미지의 환경을 네비게이션하는 embodied AI 핵심 과제이다. 기존 방법들은 historical frames을 메모리로 사용하여 높은 저장 용량과 계산 오버헤드를 초래한다.
- **Gap**: 연속 환경 내비게이션(VLN-CE) 방법들이 과거 관찰 데이터에 의존하면서 저장 요구사항이 증가하고 과거 궤적에 대한 구조화된 이해가 부족하다. semantic maps이 존재하지만 VLM이 직접 해석할 수 있는 형태로 표현되지 못하고 있다.
- **Why**: 효율적인 메모리 표현은 VLN 모델의 실제 배포 가능성을 높이고, 구조화된 공간 이해는 네비게이션 성능과 실시간 의사결정을 개선할 수 있기 때문이다.
- **Approach**: RGB-D와 pose 데이터를 포인트 클라우드로 변환하여 top-down 시멘틱 맵을 생성하고, 시맨틱 세그멘테이션을 정렬하여 기본 맵을 구성한 뒤, 주요 영역에 대한 명시적 텍스트 주석을 추가하여 ASM을 생성한다. 이 ASM을 입력으로 하는 end-to-end VLM 기반 agent를 설계한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: An overview of MapNav framework. We present a top-down Annotated Semantic Map (ASM), updated*

- **ASM 메모리 표현**: 물리적 장애물, 탐색 영역, 에이전트 위치, 궤적, 시멘틱 객체 정보를 포함하는 구조화된 top-down 맵을 동적으로 업데이트
- **SOTA 성능**: 시뮬레이션(Habitat) 및 실제 환경(현실 세계) 벤치마크에서 기존 방법들을 초과하는 성능 달성
- **효율성 개선**: 과거 프레임 저장 대신 ASM을 사용하여 저장 용량 및 계산 오버헤드 감소
- **재현성 기여**: 1 Million step-wise 샘플, ASM 생성 코드, 데이터셋 공개 약속

## How

![Figure 3](figures/fig3.webp)

*Figure 3: ASM Generation Process. Semantic map generation starts with episode initialization. At each timestep,*

- RGB-D 이미지와 depth 정보를 3D point cloud로 변환
- Semantic segmentation을 point cloud와 정렬하여 객체 마스킹 수행
- 마스킹된 객체 정보를 기반으로 top-down semantic map 생성 및 각 timestep에서 업데이트
- 핵심 영역과 추상적 시멘틱 개념에 명시적 텍스트 라벨 추가하여 ASM 생성
- 현재 RGB observation, ASM, 사용자 instruction을 frozen VLM의 multi-modal projector를 통해 입력
- VLM의 end-to-end 능력을 활용하여 move forward, turn left, turn right, stop 등의 navigation actions 생성

## Originality

- 기존 semantic maps과 달리 VLM이 직접 해석 가능하도록 명시적 텍스트 주석을 통합한 ASM 개념의 창안
- VLN에서 historical frames을 완전히 대체하는 새로운 메모리 표현 패러다임 제시
- ASM 생성 파이프라인과 1 Million step-wise 데이터셋의 공개를 통해 필드에 대한 체계적 기여
- top-down 시각과 텍스트 라벨의 조합으로 VLM의 공간 추론 능력을 향상시키는 멀티모달 통합 방식

## Limitation & Further Study

- ASM 생성 과정에서 semantic segmentation 모델의 정확도에 의존하므로, 세그멘테이션 오류가 누적될 수 있음
- 텍스트 라벨 생성 과정의 자동화 정도와 라벨 품질이 명확히 설명되지 않음
- 실제 환경 테스트에서의 구체적 결과값과 시뮬레이션 환경과의 성능 격차 비교 부족
- 다양한 VLM 백본(GPT-4V, LLaVA 등)에 대한 평가 및 비교 결과가 제한적
- 후속 연구: ASM 생성의 자동화 및 오류 복원력 개선, 동적 환경에 대한 실시간 업데이트 메커니즘 강화, cross-domain 일반화 능력 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: MapNav는 Annotated Semantic Map이라는 혁신적 메모리 표현을 통해 VLN의 효율성과 구조화된 공간 이해를 동시에 달성한 견고한 연구이다. SOTA 성능 달성과 데이터셋 공개 약속으로 임체AI 커뮤니티에 실질적인 기여를 제시하며, VLN 분야의 새로운 방향을 제안한다.

## Related Papers

- 🔄 다른 접근: [[papers/1612_Visual_Language_Maps_for_Robot_Navigation/review]] — Vision-Language Navigation에서 메모리 표현 방법으로 Annotated Semantic Map vs Visual Language Map이라는 서로 다른 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1342_CorrectNav_Self-Correction_Flywheel_Empowers_Vision-Language/review]] — VLN에서의 구조화된 메모리 표현을 자기 교정 메커니즘과 결합하여 더 강력한 네비게이션 시스템 구축 가능성을 보여준다.
- 🏛 기반 연구: [[papers/1595_TRAVEL_Training-Free_Retrieval_and_Alignment_for_Vision-and-/review]] — training-free VLN 접근법의 기초 연구로서 MapNav의 효율적인 메모리 표현 설계에 이론적 토대를 제공한다.
- 🔄 다른 접근: [[papers/1489_NaVid_Video-based_VLM_Plans_the_Next_Step_for_Vision-and-Lan/review]] — VLN에서 annotated semantic map vs video 기반 예측의 다른 메모리 표현 방식
- 🔗 후속 연구: [[papers/1340_Context-Aware_Entity_Grounding_with_Open-Vocabulary_3D_Scene/review]] — open-vocabulary 3D scene grounding을 structured navigation으로 확장한 응용
- 🔄 다른 접근: [[papers/1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M/review]] — 둘 다 VLN에서 메모리 표현을 다루지만 MapNav는 2D semantic map을, MEM은 multi-scale embodied memory를 사용하는 다른 접근법입니다.
- 🔗 후속 연구: [[papers/1592_TraceVLA_Visual_Trace_Prompting_Enhances_Spatial-Temporal_Aw/review]] — MapNav의 구조화된 맵 표현이 TraceVLA의 visual trace prompting에서 공간적 추적 정보를 더 효과적으로 활용할 수 있게 합니다.
- 🔄 다른 접근: [[papers/1319_BeliefMapNav_3D_Voxel-Based_Belief_Map_for_Zero-Shot_Object/review]] — 3D voxel belief map 대신 annotated semantic map을 활용한 다른 메모리 기반 네비게이션 접근법
- 🔄 다른 접근: [[papers/1402_GC-VLN_Instruction_as_Graph_Constraints_for_Training-free_Vi/review]] — 둘 다 VLN에서 메모리 표현을 다루지만 GC-VLN은 그래프 제약 최적화를, MapNav는 Annotated Semantic Map을 사용하는 다른 접근법입니다.
- 🔄 다른 접근: [[papers/1595_TRAVEL_Training-Free_Retrieval_and_Alignment_for_Vision-and-/review]] — MapNav는 TRAVEL의 topological map 기반 접근법과 유사하게 주석이 달린 의미론적 지도를 활용한 네비게이션을 제시한다.
