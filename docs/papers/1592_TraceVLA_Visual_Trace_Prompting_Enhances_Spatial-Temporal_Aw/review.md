---
title: "1592_TraceVLA_Visual_Trace_Prompting_Enhances_Spatial-Temporal_Aw"
authors:
  - "Ruijie Zheng"
  - "Yongyuan Liang"
  - "Shuaiyi Huang"
  - "Jianfeng Gao"
  - "Hal Daumé"
date: "2024.12"
doi: ""
arxiv: ""
score: 4.0
essence: "Visual trace prompting 기법을 통해 VLA 모델의 spatial-temporal 인식을 향상시켜 로봇 조작 작업의 성능을 개선한 연구이다. 150K 로봇 조작 궤적 데이터셋을 수집하고 TraceVLA 모델을 개발하여 시뮬레이션과 실제 로봇 환경에서 우수한 성능을 입증했다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Semantic_Task_Generalization"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zheng et al._2024_TraceVLA Visual Trace Prompting Enhances Spatial-Temporal Awareness for Generalist Robotic Policies.pdf"
---

# TraceVLA: Visual Trace Prompting Enhances Spatial-Temporal Awareness for Generalist Robotic Policies

> **저자**: Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daumé, Andrey Kolobov, Furong Huang, Jianwei Yang | **날짜**: 2024-12-13 | **URL**: [https://arxiv.org/abs/2412.10345](https://arxiv.org/abs/2412.10345)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: An illustration of our method. The first image shows the original robot’s observation, while the second*

Visual trace prompting 기법을 통해 VLA 모델의 spatial-temporal 인식을 향상시켜 로봇 조작 작업의 성능을 개선한 연구이다. 150K 로봇 조작 궤적 데이터셋을 수집하고 TraceVLA 모델을 개발하여 시뮬레이션과 실제 로봇 환경에서 우수한 성능을 입증했다.

## Motivation

- **Known**: 대규모 로봇 데이터셋으로 사전학습된 VLA 모델은 다양한 조작 작업에 대해 일반화된 정책을 제공할 수 있다. 그러나 이들 모델은 현재 입력에만 반응하고 과거 움직임에 대한 인식이 부족하여 복잡한 조작 작업에서 효과적이지 못하다.
- **Gap**: VLA 모델이 시간적 동역학(temporal dynamics)과 공간적 동역학(spatial dynamics)을 충분히 이해하지 못하여 복잡한 조작 작업에서 성능이 제한된다. 과거 프레임을 단순히 연결하는 방식은 정보 중복성으로 인해 모델의 주의 집중을 방해한다.
- **Why**: 일반화된 로봇 정책 개발은 로봇이 다양한 환경과 작업에 적응할 수 있게 하므로 로봇 조작의 실용성을 크게 향상시킨다. 공간-시간 정보의 명시적 인코딩은 모델이 동적 환경에서 더 정확한 액션 예측을 수행하도록 돕는다.
- **Approach**: Co-Tracker를 사용하여 역사적 이미지 시퀀스에서 밀집 포인트 궤적을 추출하고, 이를 원본 관찰 이미지에 시각적으로 오버레이하여 visual trace를 생성한다. 이 visual trace와 원본 이미지를 separator token으로 구분하여 VLA 모델의 입력으로 제공한다.

## Achievement

![Figure 3](figures/fig3.webp)

*Figure 3: (Left): 7B TraceVLA vs. 7B OpenVLA. (Right): 4B TraceVLA-Phi3 vs. 4B OpenVLA-Phi3.*

- **SimplerEnv 성능**: OpenVLA 대비 10% 향상된 성능을 137개 환경 설정에서 달성
- **실제 로봇 성능**: WidowX 로봇 4가지 작업에서 OpenVLA 대비 3.5배 우수한 성능 입증
- **효율성**: 4B Phi-3-Vision 기반 TraceVLA-Phi3 모델이 7B OpenVLA 수준의 성능을 달성하면서 추론 효율성을 크게 개선
- **일반화 능력**: 다양한 로봇 구체화(embodiment)와 시나리오에서 견고한 일반화 성능 시연
- **데이터셋**: 150K 로봇 조작 궤적 데이터셋 구성 및 공개

## How

![Figure 2](figures/fig2.webp)

*Figure 2: An illustration of visual trace generation. Given a sequence of historical image observations, we first*

- Co-Tracker 알고리즘으로 시간 윈도우 N 범위 내의 역사적 이미지 시퀀스에서 K×K 그리드 기반 밀집 포인트 궤적 추출
- 유의미한 움직임을 보이는 활성 포인트 궤적(active point trajectories)을 필터링하여 선택
- 활성 궤적을 시각적 선/점으로 오버레이하여 원본 이미지 위에 visual trace 생성
- 원본 이미지와 visual trace 오버레이 이미지 두 개를 separator token으로 구분하여 연결
- 텍스트 명령어 토큰과 함께 VLA 모델의 vision tokenizer 및 text tokenizer에 입력
- OpenVLA 및 Phi-3-Vision 백본 모델 위에서 end-to-end fine-tuning 수행
- SimplerEnv 시뮬레이터와 물리적 WidowX 로봇에서 다양한 작업으로 평가

## Originality

- **Visual trace prompting의 단순성과 효과성**: 기존의 프레임 연결 방식을 대체하는 우아한 대안으로, 2D 이미지만 사용하면서도 공간-시간 정보를 효과적으로 전달
- **Co-Tracker 활용**: 사전학습된 밀집 포인트 추적 모델을 VLA 학습에 창의적으로 통합하여 추가 감독 신호 없이 시간 정보 인코딩
- **다양한 모델 스케일 검증**: 7B OpenVLA와 4B Phi-3-Vision 두 가지 아키텍처에서 방법의 일반성과 확장성 입증
- **대규모 데이터셋 구성**: 150K 로봇 조작 궤적으로 구성된 전담 시각 추적 프롬프팅 데이터셋 구축

## Limitation & Further Study

- Visual trace 생성에 별도의 Co-Tracker 모델이 필요하여 계산 오버헤드가 발생하며, 추적 실패 시 성능 저하 가능성
- 2D 포인트 궤적만 사용하므로 3D 공간 정보의 깊이(depth) 손실로 인한 제약
- SimplerEnv와 WidowX 로봇에 대한 평가이므로 다른 로봇 플랫폼(팔, 휴머노이드 등)에 대한 일반화 정도 미지수
- Visual trace의 최적 추적 시간 윈도우 N과 그리드 크기 K에 대한 체계적 분석 부족
- **후속연구**: 적응적 trace 생성, 3D 포인트 클라우드 기반 확장, 다양한 로봇 형태에 대한 평가, visual trace 품질 자동 평가 메커니즘 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Visual trace prompting은 직관적이면서도 효과적인 기법으로, VLA 모델의 공간-시간 인식을 실질적으로 개선하며 광범위한 실험(시뮬레이션 및 실제 로봇)을 통해 우수한 성능을 일관되게 입증했다. ICLR 2025 게재 논문으로서 로봇 조작 분야의 실질적 기여도가 높다.

## Related Papers

- 🔗 후속 연구: [[papers/1593_TrackVLA_Unleashing_Reasoning_and_Memory_Capabilities_in_VLA/review]] — visual trace prompting을 기반으로 tracking과 memory 능력을 추가하여 TraceVLA의 spatial-temporal 인식을 더욱 발전시켰습니다.
- 🔄 다른 접근: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — 둘 다 VLA 모델의 추론 능력 향상을 목표로 하지만 CoT-VLA는 Chain-of-Thought에, TraceVLA는 visual trace에 집중합니다.
- 🏛 기반 연구: [[papers/1574_SKT_Integrating_State-Aware_Keypoint_Trajectories_with_Visio/review]] — keypoint trajectory를 VLA와 통합하는 기본 개념을 제공하여 TraceVLA의 시공간 추적 메커니즘에 이론적 기반을 제공합니다.
- 🔄 다른 접근: [[papers/1599_Unified_Vision-Language-Action_Model/review]] — 둘 다 VLA 모델의 spatial-temporal 처리를 개선하지만, TraceVLA는 visual trace를, UniVLA는 통합된 토큰화를 사용한다.
- 🔗 후속 연구: [[papers/1470_MapNav_A_Novel_Memory_Representation_via_Annotated_Semantic/review]] — MapNav의 구조화된 맵 표현이 TraceVLA의 visual trace prompting에서 공간적 추적 정보를 더 효과적으로 활용할 수 있게 합니다.
- 🏛 기반 연구: [[papers/1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M/review]] — MEM의 시공간 메모리 개념이 TraceVLA의 시공간 인식 향상 방법론과 유사한 이론적 기반을 공유한다.
- 🔄 다른 접근: [[papers/1593_TrackVLA_Unleashing_Reasoning_and_Memory_Capabilities_in_VLA/review]] — VLA에서 추적과 메모리를 위한 서로 다른 접근법 - target identification vs visual trace prompting입니다.
