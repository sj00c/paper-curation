---
title: "1464_Magma_A_Foundation_Model_for_Multimodal_AI_Agents"
authors:
  - "Jianwei Yang"
  - "Reuben Tan"
  - "Qianhui Wu"
  - "Ruijie Zheng"
  - "Baolin Peng"
date: "2025.02"
doi: ""
arxiv: ""
score: 4.0
essence: "Magma는 디지털 및 물리적 환경에서 UI 네비게이션부터 로봇 조작까지 다양한 에이전트 작업을 수행할 수 있는 멀티모달 기초 모델이다. Set-of-Mark(SoM)과 Trace-of-Mark(ToM) 기법을 통해 시공간 지능을 획득하여 언어 이해와 행동 예측을 동시에 수행한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yang et al._2025_Magma A Foundation Model for Multimodal AI Agents.pdf"
---

# Magma: A Foundation Model for Multimodal AI Agents

> **저자**: Jianwei Yang, Reuben Tan, Qianhui Wu, Ruijie Zheng, Baolin Peng, Yongyuan Liang, Yu Gu, Mu Cai, Seonghyeon Ye, Joel Jang, Yuquan Deng, Lars Liden, Jianfeng Gao | **날짜**: 2025-02-18 | **URL**: [https://arxiv.org/abs/2502.13130](https://arxiv.org/abs/2502.13130)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. We introduce Magma, the first foundation model that is capable of interpreting and grounding multimodal inputs*

Magma는 디지털 및 물리적 환경에서 UI 네비게이션부터 로봇 조작까지 다양한 에이전트 작업을 수행할 수 있는 멀티모달 기초 모델이다. Set-of-Mark(SoM)과 Trace-of-Mark(ToM) 기법을 통해 시공간 지능을 획득하여 언어 이해와 행동 예측을 동시에 수행한다.

## Motivation

- **Known**: Vision-Language(VL) 모델은 이미지와 텍스트를 이해하지만 공간-시간 행동 추론 능력이 부족하며, 기존 VLA 모델들은 특정 도메인(2D 디지털 또는 3D 물리)에 특화되어 있어 범용성이 낮다. 최근 UI 에이전트와 로봇 조작을 위한 별도의 모델들이 개발되었으나 멀티태스크 학습의 이점을 충분히 활용하지 못한다.
- **Gap**: 멀티모달 이해 능력을 유지하면서 동시에 디지털과 물리 환경 모두에서 공간-시간 행동 추론을 수행할 수 있는 통합된 기초 모델이 부재하다. 언어 기반 설명과 공간적 행동 좌표 간의 격차를 효과적으로 연결하는 방법이 필요하다.
- **Why**: 멀티모달 기초 모델은 다양한 환경과 작업에 대한 일반화 능력을 제공하며, 방대한 이미지-비디오 데이터를 활용하여 행동 기반 작업을 효율적으로 학습할 수 있다. 이는 AI 에이전트의 실용적 배포 비용을 크게 절감할 수 있다.
- **Approach**: SoM과 ToM이라는 두 가지 대리 작업을 도입하여 이미지의 상호작용 가능한 객체와 비디오의 객체 움직임을 표시함으로써 라벨이 없는 데이터를 VLA 데이터로 변환한다. UI, 로봇, 인스트럭셔널 비디오 등 이질적 데이터셋 39백만 샘플을 통합 학습하여 공간-시간 지능을 획득한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. We introduce Magma, the first foundation model that is capable of interpreting and grounding multimodal inputs*

- **UI 네비게이션 SOTA 달성**: Mind2Web, AITW 벤치마크에서 도메인 특화 모델을 능가하는 성능 달성
- **로봇 조작 SOTA 달성**: Bridge, LIBERO 로봇 조작 벤치마크에서 OpenVLA, RT-2 등 기존 모델 초과
- **멀티모달 이해 능력 유지**: GQA, VideoMME, BLINK 등 VL 벤치마크에서 훨씬 큰 데이터로 학습한 LMM과 비교 가능한 성능
- **SoM과 ToM의 상승 효과**: 두 기법의 조합이 공간-시간 지능 습득을 효과적으로 촉진함을 실증
- **모델 및 코드 공개**: 재현성을 위해 모델 가중치와 코드를 공개하여 커뮤니티 기여

## How

![Figure 4](figures/fig4.webp)

*Figure 4. Trace-of-Mark supervisions for robot manipulation (left) and human action (right). Same coordinate normalizati*

- **Set-of-Mark(SoM)**: 이미지의 상호작용 가능한 시각 객체(UI 버튼 등)에 번호 표시를 자동으로 추가하여 action grounding 학습 가능하게 변환
- **Trace-of-Mark(ToM)**: 비디오에서 인간 손이나 로봇 팔의 움직임 궤적을 자동 레이블링하여 action planning 학습
- **이질적 데이터셋 통합**: SeekClick(UI), OXE(로봇), Ego-4D(인스트럭셔널 비디오), 이미지-텍스트 쌍 등을 단일 모델로 동시 학습
- **아키텍처 설계**: Vision encoder로 시각 정보 추출, language model로 의미 이해, action decoder로 행동 예측 수행
- **Zero-shot 전이**: 단일 모델 파라미터로 다양한 다운스트림 작업에 직접 적용 가능

## Originality

- **첫 통합 멀티모달 에이전트 기초 모델**: 디지털/물리 환경 모두에서 멀티모달 이해와 행동 추론을 수행하는 단일 모델 제시
- **SoM과 ToM의 환경-불가지론 설계**: 두 기법이 도메인 특성에 무관하게 확장 가능하며 라벨 없는 대규모 데이터 활용 가능
- **멀티태스크 기초 모델 학습 패러다임**: 언어 이해와 공간 추론의 격차를 대리 작업으로 효과적으로 연결
- **39백만 샘플 규모의 이질적 데이터셋 구성**: 기존 작업별 벤치마크를 통합하는 새로운 데이터 큐레이션 접근

## Limitation & Further Study

- **도메인 간 전이 한계**: UI와 로봇 조작 간 직접적 지식 전이의 효과성이 명확히 분석되지 않음
- **SoM/ToM 자동 레이블링 정확도**: 복잡한 장면이나 부분적 폐색(occlusion) 상황에서의 자동 레이블링 오류 가능성 미검토
- **실시간 행동 실행 능력**: 모델이 행동 시퀀스를 예측하나, 실제 에이전트 시스템과의 통합과 폐쇄 루프 재계획 능력 평가 부족
- **후속 연구 방향**: 더 많은 물리 로봇 데이터로의 확장, 다중 모달 센서 입력(촉각, 음향) 통합, 동적 환경에서의 온라인 적응 학습

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Magma는 멀티모달 에이전트 연구에서 중요한 이정표를 제시하는 실질적인 기초 모델이며, SoM/ToM을 통한 데이터 변환 기법의 우아함과 실증적 성과(UI 및 로봇 SOTA)가 높은 임팩트를 시사한다. 공개 공개와 함께 추후 연구의 기반이 될 가능성이 크다.

## Related Papers

- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — OpenVLA와 동일한 멀티모달 VLA 접근법이지만 Magma는 SoM/ToM 기법으로 차별화된 시공간 지능을 구현한다.
- 🔗 후속 연구: [[papers/1344_CoT-VLA_Visual_Chain-of-Thought_Reasoning_for_Vision-Languag/review]] — CoT-VLA의 시각적 추론 체인을 확장하여 Set-of-Mark과 Trace-of-Mark로 더 정교한 시공간 추론을 가능하게 한다.
- 🔗 후속 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — PaLM-E의 멀티모달 embodied reasoning을 더 일반화된 AI 에이전트로 발전시킨 확장
- 🔄 다른 접근: [[papers/1385_EO-1_An_Open_Unified_Embodied_Foundation_Model_for_General_R/review]] — 통합된 embodied foundation model을 구축하는 다른 접근법
- ⚖️ 반론/비판: [[papers/1437_InternVLA-A1_Unifying_Understanding_Generation_and_Action_fo/review]] — 멀티모달 기초 모델의 이해-생성-행동 통합에서 다른 아키텍처 관점 제시
- 🔗 후속 연구: [[papers/1294_A_Generalist_Agent/review]] — Gato의 범용 정책 에이전트 개념은 Magma의 멀티모달 AI 에이전트로 확장된다.
- 🏛 기반 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — Magma가 발전시킨 multimodal foundation model의 기초가 되는 embodied multimodal LLM
