---
title: "1506_Open-World_Object_Manipulation_using_Pre-trained_Vision-Lang"
authors:
  - "Austin Stone"
  - "Ted Xiao"
  - "Yao Lu"
  - "Keerthana Gopalakrishnan"
  - "Kuang-Huei Lee"
date: "2023.03"
doi: ""
arxiv: ""
score: 4.0
essence: "Pre-trained vision-language model(VLM)을 로봇 정책과 인터페이싱하여 로봇이 직접 경험하지 못한 새로운 물체 카테고리에 대한 지시를 따를 수 있도록 하는 MOO(Manipulation of Open-World Objects) 방법을 제안한다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robot_Policy_Learning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Instruction-Following_Robot_Navigation"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Stone et al._2023_Open-World Object Manipulation using Pre-trained Vision-Language Models.pdf"
---

# Open-World Object Manipulation using Pre-trained Vision-Language Models

> **저자**: Austin Stone, Ted Xiao, Yao Lu, Keerthana Gopalakrishnan, Kuang-Huei Lee, Quan Vuong, Paul Wohlhart, Sean Kirmani, Brianna Zitkovich, Fei Xia, Chelsea Finn, Karol Hausman | **날짜**: 2023-03-02 | **URL**: [https://arxiv.org/abs/2303.00905](https://arxiv.org/abs/2303.00905)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of MOO. We train a language-conditioned policy conditioned on object locations from a*

Pre-trained vision-language model(VLM)을 로봇 정책과 인터페이싱하여 로봇이 직접 경험하지 못한 새로운 물체 카테고리에 대한 지시를 따를 수 있도록 하는 MOO(Manipulation of Open-World Objects) 방법을 제안한다.

## Motivation

- **Known**: 로봇은 첫 경험 데이터로부터 다양한 행동을 학습할 수 있지만, 인간의 풍부한 의미론적 어휘를 모두 다루기는 불가능하다. VLM과 같은 pre-trained 모델은 인터넷의 방대한 정적 데이터에서 풍부한 의미론적 정보를 캡처한다.
- **Gap**: 기존 pipelined 접근법은 다양한 물체 카테고리에 일반화할 수 있지만 불안정하고, vanilla pre-training을 사용한 정책은 안정적이지만 미경험 의미론적 개념으로 일반화하지 못한다.
- **Why**: 로봇이 인간의 자연어 지시를 따르려면 보지 못한 물체를 이해하고 조작할 수 있어야 하며, 이는 의미론적 접지(semantic grounding)와 실제 제어의 결합을 통해 실현될 수 있다.
- **Approach**: Frozen VLM을 사용하여 언어 지시에서 물체를 지역화하고, 이 물체 위치 정보와 이미지, 지시를 결합하여 조작 정책을 조건화함으로써 end-to-end 학습 정책이 의미론적 정보를 활용하도록 한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5: Main Results. While baseline methods perform competitively on in-distribution combinations of*

- **Zero-shot 일반화**: 훈련에서 본 106개 물체를 넘어 다양한 미경험 물체 카테고리와 환경에 걸쳐 zero-shot 일반화 달성
- **실제 로봇 평가**: 실제 모바일 조작기에서 1,472번의 평가를 통해 최근 로봇 학습 방법을 유의미하게 초과
- **다중 모달리티 지원**: 자연어뿐 아니라 손가락 포인팅, 참조 이미지, GUI 등 다양한 입력 모달리티로 확장 가능
- **모바일 조작 통합**: Clip-on-Wheels(CoW)와 통합하여 미경험 물체에 대한 모바일 조작 작업 완성 가능

## How

![Figure 2](figures/fig2.webp)

*Figure 2: MOO architecture: We extract object location (represented as the center of the bounding box) on*

- OWL-ViT를 사용한 개방형 어휘 물체 검출로 언어 지시의 물체명 추출 및 2D 좌표 지역화
- 지역화된 물체의 2D 중심 좌표를 정책 입력으로 포함시켜 명시적 물체-지시 연결
- 106개 훈련 물체의 59,000개 데모로 언어-조건 정책 학습
- Frozen VLM과 훈련된 정책의 결합으로 구성된 end-to-end 시스템으로 파이프라인 brittleness 회피
- 다양한 입력 모달리티(포인팅, 참조 이미지)에서 물체 위치 추출을 위한 VLM 활용

## Originality

- Vision-language model과 로봇 정책의 새로운 결합 방식으로, VLM을 정확한 상태 추정이 아닌 물체 지역화 목적으로만 사용
- Frozen VLM과 함께 훈련된 정책으로 brittleness 문제 해결
- 단순한 2D 좌표 기반 표현을 통해 확장성과 안정성을 동시에 달성
- 자연어 이상의 다양한 모달리티(포인팅, 이미지, GUI)로의 일반화 시연

## Limitation & Further Study

- VLM의 물체 검출 정확도에 의존하므로 VLM이 실패하면 정책도 실패 가능
- 실험은 단일 로봇 플랫폼(모바일 조작기)에서만 수행되어 다른 로봇에 대한 일반화는 미확인
- 훈련 데이터는 여전히 106개 물체로 제한되어 있으며, 더 다양한 물체와 작업에 대한 평가 필요
- 복잡한 공간 추론이나 다중 물체 상호작용이 필요한 작업에 대한 성능은 미평가
- 후속연구: VLM 성능 향상, 다양한 로봇 플랫폼 적용, 3D 정보 활용, 동적 환경 적응 등

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 pre-trained VLM을 로봇 조작에 실질적으로 통합하여 의미론적 일반화를 달성한 중요한 기여이며, 실제 로봇 실험과 다중 모달리티 확장을 통해 실용성을 입증했다.

## Related Papers

- 🏛 기반 연구: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — Vision-Language Foundation Models의 로봇 모방 학습 활용 연구가 MOO의 pre-trained VLM 기반 객체 조작 방법론의 기초가 된다.
- 🔄 다른 접근: [[papers/1467_Manipulate-Anything_Automating_Real-World_Robots_using_Visio/review]] — Manipulate-Anything과 동일하게 개방형 객체 조작을 다루지만 MOO는 VLM 인터페이싱에, 다른 연구는 자동화에 집중한다.
- 🔄 다른 접근: [[papers/1548_Robotic_Skill_Acquisition_via_Instruction_Augmentation_with/review]] — 두 논문 모두 VLM을 활용한 instruction-following 로봇 제어를 다루지만 물체 조작과 기술 습득의 관점이 다르다.
- 🏛 기반 연구: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — PaLM-E의 embodied multimodal language model 개념을 구체적인 물체 조작 작업에 적용한다.
- 🔗 후속 연구: [[papers/1334_Code_as_Policies_Language_Model_Programs_for_Embodied_Contro/review]] — Code as Policies의 언어 기반 제어 개념을 pre-trained VLM과 결합하여 발전시킨다.
- 🏛 기반 연구: [[papers/1415_Grounding_DINO_Marrying_DINO_with_Grounded_Pre-Training_for/review]] — MOO가 활용하는 open-vocabulary object detection과 grounding 기능의 기반이 되는 vision-language model을 제공한다.
- 🔄 다른 접근: [[papers/1340_Context-Aware_Entity_Grounding_with_Open-Vocabulary_3D_Scene/review]] — MOO의 open-world object manipulation과 달리 entity grounding을 통한 3D scene understanding 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1597_UniAff_A_Unified_Representation_of_Affordances_for_Tool_Usag/review]] — MOO의 open-world object manipulation을 tool usage와 affordance understanding으로 확장하여 더 복잡한 조작 작업을 수행할 수 있다.
- 🔄 다른 접근: [[papers/1399_From_Seeing_to_Doing_Bridging_Reasoning_and_Decision_for_Rob/review]] — Open-World Object Manipulation의 pre-trained vision-language 활용과 FSD의 spatial relationship reasoning은 zero-shot 로봇 조작에서 서로 다른 접근 방식이다.
- 🏛 기반 연구: [[papers/1462_LOTUS_Continual_Imitation_Learning_for_Robot_Manipulation_Th/review]] — open-vocabulary vision model을 활용한 객체 조작이 LOTUS의 기술 발견에 기반을 제공한다.
- 🏛 기반 연구: [[papers/1467_Manipulate-Anything_Automating_Real-World_Robots_using_Visio/review]] — Open-World Object Manipulation의 사전 훈련된 VLM 활용 방법론이 Manipulate-Anything의 기술적 기반임
- 🏛 기반 연구: [[papers/1435_Instruct2Act_Mapping_Multi-modality_Instructions_to_Robotic/review]] — Open-World Object Manipulation의 기본 개념을 LLM과 foundation model API로 구현하는 구체적 프레임워크를 제시한다.
- 🔄 다른 접근: [[papers/1548_Robotic_Skill_Acquisition_via_Instruction_Augmentation_with/review]] — 두 논문 모두 VLM을 활용한 instruction-following을 다루지만 데이터 증강과 실시간 적용의 접근법이 다르다.
- 🏛 기반 연구: [[papers/1594_Transferring_Foundation_Models_for_Generalizable_Robotic_Man/review]] — Open-World Object Manipulation은 기초 모델을 활용한 일반화 가능한 로봇 조작의 이론적 배경을 제시합니다.
