---
title: "1308_An_Embodied_Generalist_Agent_in_3D_World"
authors:
  - "Jiangyong Huang"
  - "Silong Yong"
  - "Xiaojian Ma"
  - "Xiongkun Linghu"
  - "Puhao Li"
date: "2023.11"
doi: ""
arxiv: ""
score: 4.0
essence: "LEO는 egocentric 2D 이미지, 3D point cloud, 텍스트를 입력으로 받아 3D 환경에서 인식, grounding, 추론, 계획, 행동을 수행할 수 있는 최초의 embodied generalist agent이다. 통일된 모델 아키텍처와 학습 목표로 3D vision-language alignment와 3D vision-language-action instruction tuning의 두 단계로 학습된다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Embodied_Spatial_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Huang et al._2023_An Embodied Generalist Agent in 3D World.pdf"
---

# An Embodied Generalist Agent in 3D World

> **저자**: Jiangyong Huang, Silong Yong, Xiaojian Ma, Xiongkun Linghu, Puhao Li, Yan Wang, Qing Li, Song-Chun Zhu, Baoxiong Jia, Siyuan Huang | **날짜**: 2023-11-18 | **URL**: [https://arxiv.org/abs/2311.12871](https://arxiv.org/abs/2311.12871)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: The proposed embodied generalist agent LEO. It takes egocentric 2D images, 3D point clouds, and texts as input*

LEO는 egocentric 2D 이미지, 3D point cloud, 텍스트를 입력으로 받아 3D 환경에서 인식, grounding, 추론, 계획, 행동을 수행할 수 있는 최초의 embodied generalist agent이다. 통일된 모델 아키텍처와 학습 목표로 3D vision-language alignment와 3D vision-language-action instruction tuning의 두 단계로 학습된다.

## Motivation

- **Known**: 최근 LLM 기반 generalist 모델들이 컴퓨터 비전과 로봇공학 등 다양한 도메인에서 성과를 보였다. 하지만 대부분의 모델들은 2D 이미지에 의존하며 3D 입력 처리 능력이 제한적이고, 3D grounding, embodied reasoning, acting 같은 3D 세계에 내재된 작업을 거의 탐색하지 않았다.
- **Gap**: 기존의 3D vision-language 모델들은 대규모 통일된 pretraining과 효율적인 fine-tuning을 충분히 탐색하지 않았으며, embodied 작업(navigation, manipulation)에서는 성능이 떨어진다. 또한 3D 데이터 수집의 높은 비용으로 인해 대규모 3D dataset이 부족하다.
- **Why**: 현실 세계의 작업은 3D 환경에서 이루어지므로, 3D 세계를 이해하고 상호작용할 수 있는 generalist agent의 개발은 일반 인공지능에 접근하기 위해 필수적이다.
- **Approach**: object-centric 3D representation과 LLM을 연결하는 통일된 프레임워크를 제시하고, LLM-assisted pipeline으로 고품질 3D vision-language 데이터를 생성한다. 모든 modality를 token 시퀀스로 변환하여 GPT-style autoregressive language modeling으로 학습한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: The proposed embodied generalist agent LEO. It takes egocentric 2D images, 3D point clouds, and texts as input*

- **통일된 embodied generalist agent**: 단일 모델으로 3D captioning, question answering, embodied reasoning, navigation, manipulation을 포함한 다양한 작업을 처리하며 대부분의 작업에서 task-specific 모델을 능가한다.
- **효율적인 3D vision-language 데이터 생성**: scene graph와 Object-centric Chain-of-Thought(O-CoT) 방법을 활용한 LLM-assisted pipeline으로 대규모 고품질 3D VL 데이터를 생성하고, 정규 표현식 매칭과 scene graph retrieval을 통해 LLM hallucination을 완화한다.
- **강력한 일반화 능력**: scene-grounded dialogue와 planning에서 유연하고 coherent한 응답을 생성하며, navigation과 manipulation 작업에서 task-specific 모델과 견줄 수 있는 성능을 달성한다.
- **확장성 검증**: 모델 크기 증가에 따른 성능 개선을 보여주며 scaling law를 입증한다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2: Our proposed LLM-assisted 3D-language data generation pipeline and data examples.. (Top-left) Messages with 3D*

- 2단계 학습 스킴: (1) 3D vision-language alignment - 대규모 3D captioning 데이터로 visual-language 연결 학습, (2) 3D vision-language-action instruction tuning - action 토큰을 포함한 instruction tuning
- Multi-modal tokenization: egocentric 2D 이미지 토큰, object-centric 3D point cloud 토큰, 텍스트 토큰을 통합 시퀀스로 변환하여 LLM에 입력
- Dual encoder 구조: egocentric 2D encoder로 embodied 시점을 인식하고 3D point cloud encoder로 third-person 전역 시점을 처리
- LLM-assisted 데이터 생성 파이프라인: scene graph를 LLM에 입력하고 O-CoT 방법으로 고품질 captioning 생성, 정규 표현식과 scene graph retrieval로 후처리
- 통합 목표 함수: 모든 작업을 sequence prediction으로 공식화하여 동일한 autoregressive 학습 목표 적용
- LoRA 기반 효율적 fine-tuning: 사전학습된 LLM의 가중치를 고정하고 LoRA를 통해 적응

## Originality

- **최초의 embodied generalist agent**: egocentric 2D, 3D global, 텍스트 입력을 통일 아키텍처로 처리하면서 동시에 text response와 embodied action을 생성하는 첫 시도
- **Object-centric 3D 표현과 LLM의 효율적 연결**: point cloud의 object-centric 특성을 활용하여 3D 이해와 LLM의 추론 능력을 자연스럽게 결합
- **LLM-assisted 3D VL 데이터 생성 파이프라인**: scene graph 기반 구조화된 prompt와 O-CoT 방법으로 대규모 고품질 3D 주석을 생성하는 실용적 솔루션
- **포괄적 3D 작업 벤치마크**: object-level과 scene-level의 다양한 3D 작업을 통일된 framework로 평가하고 상세한 ablation study 제시

## Limitation & Further Study

- **3D 데이터 규모**: 여전히 대규모 3D 데이터 수집은 2D에 비해 비용이 높으며, 제시된 데이터셋의 규모가 2D foundation model 수준에 미치지 못함
- **실제 로봇 환경 검증 부족**: 대부분의 평가가 시뮬레이션 환경(3D scene benchmark)에서 이루어졌으며 실제 로봇 플랫폼에서의 성능 검증이 제한적
- **Action 토큰의 표현력**: 로봇 조작 작업의 precise control(위치, 회전 좌표)을 위해 action tokenization 방식의 추가 개선 필요
- **Scene understanding의 동적 환경 대응**: 정적 3D scene 이해에 최적화되어 있으며 동적 환경 변화에 대한 적응 능력은 미탐색
- **후속 연구 방향**: (1) 더 대규모 3D 데이터 수집 및 합성 데이터 활용, (2) 실제 embodied 환경에서의 closed-loop 평가, (3) 다양한 3D encoder 아키텍처 탐색, (4) few-shot adaptation 능력 강화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: LEO는 3D 환경에서의 embodied generalist agent 개발에 중요한 이정표를 제시하며, 통일된 아키텍처로 다양한 3D 작업을 처리할 수 있음을 입증했다. LLM-assisted 데이터 생성 파이프라인은 3D 데이터 수집의 실질적 문제를 해결하는 실용적 기여이며, 광범위한 실험과 ablation study가 연구의 신뢰성을 높인다.

## Related Papers

- 🔄 다른 접근: [[papers/1403_Gemini_Robotics_15_Pushing_the_Frontier_of_Generalist_Robots/review]] — 둘 다 generalist robotics agent이지만 LEO는 3D 환경에, Gemini Robotics는 범용 로봇 지능에 더 중점을 둡니다.
- 🏛 기반 연구: [[papers/1589_TopV-Nav_Unlocking_the_Top-View_Spatial_Reasoning_Potential/review]] — TopV-Nav의 top-view spatial reasoning이 LEO의 3D 환경에서의 공간 인식과 계획 능력의 기초가 됩니다.
- 🔗 후속 연구: [[papers/1291_3D-VLA_A_3D_Vision-Language-Action_Generative_World_Model/review]] — 3D-VLA는 LEO의 3D embodied agent 개념을 generative world model로 발전시킨 후속 연구입니다.
- 🔄 다른 접근: [[papers/1294_A_Generalist_Agent/review]] — 둘 다 generalist agent를 지향하지만 LEO는 3D 환경에서의 embodied 능력에 더 특화되어 있습니다.
