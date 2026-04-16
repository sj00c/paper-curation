---
title: "1593_TrackVLA_Unleashing_Reasoning_and_Memory_Capabilities_in_VLA"
authors:
  - "Jiahang Liu"
  - "Yunpeng Qi"
  - "Jiazhao Zhang"
  - "Minghan Li"
  - "Shaoan Wang"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "TrackVLA++는 Vision-Language-Action 모델에 Polar-CoT 공간 추론과 Target Identification Memory(TIM)를 통합하여 장시간 추적과 폐색 상황에서의 강건한 embodied visual tracking을 실현한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Intelligent_Robot_Navigation_Planning"
  - "cat/Embodied_AI_Architectures"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Liu et al._2025_TrackVLA++ Unleashing Reasoning and Memory Capabilities in VLA Models for Embodied Visual Tracking.pdf"
---

# TrackVLA++: Unleashing Reasoning and Memory Capabilities in VLA Models for Embodied Visual Tracking

> **저자**: Jiahang Liu, Yunpeng Qi, Jiazhao Zhang, Minghan Li, Shaoan Wang, Kui Wu, Hanjing Ye, Hong Zhang, Zhibo Chen, Fangwei Zhong, Zhizheng Zhang, He Wang | **날짜**: 2025-10-08 | **URL**: [https://arxiv.org/abs/2510.07134](https://arxiv.org/abs/2510.07134)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: The pipeline of TrackVLA++. Given a video stream and a language instruction, TrackVLA++ predicts a tracking traj*

TrackVLA++는 Vision-Language-Action 모델에 Polar-CoT 공간 추론과 Target Identification Memory(TIM)를 통합하여 장시간 추적과 폐색 상황에서의 강건한 embodied visual tracking을 실현한다.

## Motivation

- **Known**: 최근 VLA 모델들(TrackVLA, LOVON)은 pre-trained VLM을 활용하여 자연어 기반 embodied visual tracking을 성공적으로 수행하고 있으나, 명시적 공간 추론과 장시간 목표 식별 메커니즘이 부족하다.
- **Gap**: 기존 방법들은 심각한 폐색이나 유사한 distractors가 있는 복잡한 장면에서 실패하며, CoT 기반 접근도 효율성 문제로 동적 추적 작업에 적합하지 않다.
- **Why**: Embodied visual tracking은 companion robots, guidance robots 등 실제 로봇 응용에 필수적이며, 폐색과 distractors를 견뎌내는 능력은 실환경 배포의 핵심 요구사항이다.
- **Approach**: Polar-CoT를 통해 목표의 상대 위치를 agent-centric 극좌표로 예측하고, 이를 기반으로 TIM이 confidence-aware gating 전략으로 장시간 메모리를 유지한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: Real-world demonstration of TrackVLA++. TrackVLA++ is a novel Vision-Language-Action model that incorporates spa*

- **State-of-the-art 성능**: EVT-Bench DT 스플릿에서 egocentric 설정에서 5.1%, multi-camera 설정에서 12% 이상 향상
- **효율적 추론**: Polar-CoT의 단일 reasoning token으로 높은 추론 속도 유지
- **강력한 일반화**: 시뮬레이션과 실환경에서 모두 우수한 성능 및 zero-shot 일반화 능력
- **다중 카메라 지원**: egocentric과 multi-camera 설정 모두에서 호환성 유지

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: The pipeline of TrackVLA++. Given a video stream and a language instruction, TrackVLA++ predicts a tracking traj*

- Vision encoder로 RGB 입력을 처리하고 grid pooling으로 시각 토큰 추출
- Polar-CoT를 통해 <θ, d, C> 형태의 극좌표 위치와 confidence 점수 예측
- TIM에서 가중치 w = C_new / (C_new + C_old)를 계산하여 메모리 업데이트 강도 결정
- Confidence 기반 gating으로 높은 신뢰도의 업데이트만 허용하여 폐색 중 메모리 보존
- Action head가 spatial prior와 메모리 정보로부터 tracking trajectory 생성

## Originality

- **Polar-CoT의 혁신**: 기존 CoT는 verbose한 중간 표현을 생성하나, Polar-CoT는 단일 극좌표 token으로 공간 추론을 효율화
- **TIM의 confidence-aware 설계**: 목표 존재 확신도에 따라 동적으로 메모리 업데이트 강도를 조절하는 새로운 접근
- **VLA 패러다임 확장**: 추론과 메모리를 결합한 통합 프레임워크로 EVT 작업에 특화된 설계
- **multi-view 자연스러운 확장**: 제안된 메커니즘이 단일/다중 카메라 설정 모두에 일관되게 적용 가능

## Limitation & Further Study

- **메모리 용량 제한**: 매우 장시간(수시간 이상) 추적에서 메모리 충돌 시 성능 저하 가능성
- **복잡한 distractors**: 여러 시간적으로 변화하는 유사 대상 간 식별 여전히 도전적
- **실시간성**: 다중 카메라 설정에서 계산 복잡도 증가로 frame rate 영향 가능
- **후속연구**: adaptive memory size 조절, hierarchical memory 구조, long-term object re-identification 모듈 통합 가능

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: TrackVLA++는 효율적인 spatial reasoning과 confidence-aware memory update로 embodied visual tracking의 실제 도전(폐색, distractors)을 우아하게 해결하며, 시뮬레이션과 실환경에서 모두 강력한 성능을 입증한 매우 우수한 연구이다.

## Related Papers

- 🏛 기반 연구: [[papers/1474_MEM_Multi-Scale_Embodied_Memory_for_Vision_Language_Action_M/review]] — multi-scale embodied memory가 visual tracking에서 Target Identification Memory의 기반이 됩니다.
- 🔄 다른 접근: [[papers/1592_TraceVLA_Visual_Trace_Prompting_Enhances_Spatial-Temporal_Aw/review]] — VLA에서 추적과 메모리를 위한 서로 다른 접근법 - target identification vs visual trace prompting입니다.
- 🔗 후속 연구: [[papers/1320_BitVLA_1-bit_Vision-Language-Action_Models_for_Robotics_Mani/review]] — 1-bit VLA의 효율성을 reasoning과 memory 기능과 결합하여 더 강건한 모델을 만들 수 있습니다.
- 🔄 다른 접근: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — 둘 다 VLA 모델에 메모리 기능을 추가하지만 TrackVLA++는 tracking 특화 TIM을, TriVLA는 에피소딕 월드 모델을 사용한다.
- 🏛 기반 연구: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — 3D-VLA의 3D 시각-언어-행동 생성 모델이 TrackVLA++의 공간적 추론 능력 개발의 기반이 되었다.
- 🏛 기반 연구: [[papers/1415_Grounding_DINO_Marrying_DINO_with_Grounded_Pre-Training_for/review]] — Grounding DINO의 시각적 grounding 기술이 TrackVLA++의 Target Identification Memory 구현에 핵심 기반을 제공한다.
- 🔗 후속 연구: [[papers/1592_TraceVLA_Visual_Trace_Prompting_Enhances_Spatial-Temporal_Aw/review]] — visual trace prompting을 기반으로 tracking과 memory 능력을 추가하여 TraceVLA의 spatial-temporal 인식을 더욱 발전시켰습니다.
- 🔄 다른 접근: [[papers/1596_TriVLA_A_Triple-System-Based_Unified_Vision-Language-Action/review]] — 둘 다 메모리와 추론을 VLA에 통합하지만 TriVLA는 에피소딕 메모리에, TrackVLA++는 tracking memory에 집중합니다.
- 🔗 후속 연구: [[papers/1322_BOSS_Benchmark_for_Observation_Space_Shift_in_Long-Horizon_T/review]] — 메모리와 추론 능력을 강화한 VLA로 장기 작업의 OSS 문제를 해결한다.
