---
title: "1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th"
authors:
  - "Roya Firoozi"
  - "Johnathan Tucker"
  - "Stephen Tian"
  - "Anirudha Majumdar"
  - "Jiankai Sun"
date: "2023.12"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 로봇 자동화 스택의 지각, 의사결정, 제어 전반에 걸쳐 foundation model의 응용을 포괄적으로 조사하며, 로봇 도메인 적용 시 데이터 부족, 실시간 성능, 안전성 보장 등의 주요 과제를 제시한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Firoozi et al._2023_Foundation Models in Robotics Applications, Challenges, and the Future.pdf"
---

# Foundation Models in Robotics: Applications, Challenges, and the Future

> **저자**: Roya Firoozi, Johnathan Tucker, Stephen Tian, Anirudha Majumdar, Jiankai Sun, Weiyu Liu, Yuke Zhu, Shuran Song, Ashish Kapoor, Karol Hausman, Brian Ichter, Danny Driess, Jiajun Wu, Cewu Lu, Mac Schwager | **날짜**: 2023-12-13 | **URL**: [https://arxiv.org/abs/2312.07843](https://arxiv.org/abs/2312.07843)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Overview of Robotics Tasks Leveraging Foundation Models.*

본 논문은 로봇 자동화 스택의 지각, 의사결정, 제어 전반에 걸쳐 foundation model의 응용을 포괄적으로 조사하며, 로봇 도메인 적용 시 데이터 부족, 실시간 성능, 안전성 보장 등의 주요 과제를 제시한다.

## Motivation

- **Known**: Foundation model은 대규모 인터넷 데이터로 사전 학습되어 우수한 일반화 능력을 보이며, 기존 로봇 학습은 특정 작업별 소규모 데이터셋에 의존한다. VLM과 LLM이 시각-언어 이해와 상식 추론을 제공할 수 있다는 것이 알려져 있다.
- **Gap**: Foundation model의 로봇 분야 적용은 아직 초기 단계로, 로봇 관련 학습 데이터의 심각한 부족, 불확실성 정량화, 실시간 실행 가능성, 그리고 안전성 평가 방법론이 확립되지 않았다.
- **Why**: Foundation model은 제한된 데이터 환경에서의 로봇 학습 효율을 획기적으로 개선할 수 있으며, zero-shot 일반화 능력은 미지의 환경에서 로봇의 적응성을 크게 높일 수 있다.
- **Approach**: 본 논문은 perception, decision-making, control 영역에서 foundation model을 활용하는 최근 연구들을 체계적으로 분류 및 분석하고, 로봇 자동화 통합 시 직면하는 기술적, 안전성 관련 과제들을 상세히 논의한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Overview of Robotics Tasks Leveraging Foundation Models.*

- **Foundation Model 응용 분류**: Perception (open-vocabulary detection/segmentation, 3D 표현 학습), Decision-making (LLM 기반 태스크 플래닝, 언어 조건 모방 학습), Control (Transformer 기반 정책, in-context learning) 영역별로 체계화
- **주요 기술 동향 정리**: Language-grounded 3D scene understanding, code generation을 통한 태스크 플래닝, vision-language model의 affordance 학습 등 신흥 기법들의 성과 제시
- **핵심 과제 식별**: 데이터 부족(로봇 규모 학습 데이터 스케일링 방법 부재), 불확실성 정량화(instance/distribution 수준), 실시간 성능(inference latency), 안전성 평가(배포 전/중/후 검증) 등 5개 주요 분야의 구체적 문제 제시
- **해결 방안 제시**: 비구조화 플레이 데이터 활용, synthetic data 생성, VLM 기반 데이터 증강, 불확실성 정량화 프레임워크, 배포 전 안전 테스트 및 OOD detection 방안 제안

## How


- Foundation model의 유형별 분류: LLM, Vision Transformer, VLM(vision-language model), embodied multimodal LM, visual generative model 등의 특성과 로봇 적용 가능성 분석
- 로봇 응용 도메인별 체계적 리뷰: policy learning (language-conditioned imitation learning, language-assisted RL), task planning (language instruction, code generation), open-vocabulary navigation/manipulation, perception (object detection, semantic segmentation, 3D 표현)
- 데이터 스케일링 전략 검토: unlabeled video 및 human play data 활용, inpainting 기반 data augmentation, simulation을 통한 synthetic data 생성, VLM을 활용한 자동 라벨링
- 불확실성 및 안전성 평가 프레임워크: instance-level (언어 ambiguity, LLM hallucination), distribution-level uncertainty, distribution shift, calibration 관점의 분석
- 실시간 성능 개선 경로: 모델 경량화, inference acceleration, 구조화된 생성(structured generation)을 통한 latency 감소 방안 검토

## Originality

- 로봇 도메인의 foundation model 응용에 대한 최초의 포괄적 학술 조사(concurrent survey 제외)로, perception-decision making-control의 통합 관점 제시
- 기술적 성과뿐 아니라 실제 배포를 위한 안전성, 불확실성 정량화, 실시간 성능 등 실무적 과제를 동등한 비중으로 다룬 점
- 로봇 데이터 부족 문제를 다층적으로 접근하는 해결책(self-supervised learning, synthetic data, VLM 기반 augmentation 등)을 체계화

## Limitation & Further Study

- 조사 논문의 특성상 new empirical result나 novel algorithm 제시 부재
- Foundation model 자체의 근본적 한계(hallucination, OOD robustness 등)에 대한 깊이 있는 분석 부족
- 실제 로봇 플랫폼에서의 end-to-end 통합 사례 및 성능 비교 데이터 제한
- 후속 연구 방향: (1) 로봇 특화 foundation model 개발, (2) 엄격한 불확실성 정량화 방법론 수립, (3) closed-loop 배포 환경에서의 distribution shift 대응, (4) 안전성 검증 표준화, (5) 실시간 실행 가능한 경량 모델 개발

## Evaluation

- Novelty: 3/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 로봇 자동화에서 foundation model의 역할을 체계적으로 정리한 중요한 조사 논문으로, 기술적 성과뿐 아니라 안전성과 실시간 성능이라는 실무적 과제를 균형있게 다루어 해당 분야의 나침반 역할을 할 수 있다.

## Related Papers

- 🔗 후속 연구: [[papers/1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey/review]] — Foundation Models in Robotics와 Robot Learning in the Era of Foundation Models는 로봇틱스에서 foundation model 활용에 대한 상호 보완적인 종합 조사이다.
- 🔄 다른 접근: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — 로봇틱스 foundation model 응용과 foundation model 기반 범용 로봇은 동일한 기술의 현재 상태와 미래 비전을 다루는 서로 다른 관점이다.
- 🏛 기반 연구: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — Foundation Model Driven Robotics의 포괄적 리뷰는 로봇틱스 foundation model 응용 조사에 더 넓은 기술적 맥락과 기반을 제공한다.
- 🔗 후속 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — Pure Vision Language Action Models의 VLA 특화 조사가 Foundation Models in Robotics의 더 광범위한 foundation model 응용 연구로 확장된 관계이다.
- 🏛 기반 연구: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — Multimodal Fusion and Vision-Language Models 서베이가 Foundation Models in Robotics에서 다루는 multimodal foundation model의 로봇 응용에 기초적 이론을 제공한다.
- 🔄 다른 접근: [[papers/1397_Foundation_Model_Driven_Robotics_A_Comprehensive_Review/review]] — 둘 다 foundation model의 로봇공학 응용을 종합적으로 다루지만 LLM/VLM 중심 vs 전반적 foundation model로 범위가 다르다.
- 🔄 다른 접근: [[papers/1405_Generative_Artificial_Intelligence_in_Robotic_Manipulation_A/review]] — Foundation model의 로봇 적용을 다각도로 분석한 서베이와 생성형 AI 중심의 다른 관점을 제시한다.
- 🔗 후속 연구: [[papers/1388_Exploring_Embodied_Multimodal_Large_Models_Development_Datas/review]] — Foundation Models in Robotics가 EMLMs의 체계적 분석을 로봇 응용의 구체적인 도전과 기회로 확장합니다.
- 🔗 후속 연구: [[papers/1445_Large_Model_Empowered_Embodied_AI_A_Survey_on_Decision-Makin/review]] — 대규모 모델 기반 embodied AI 서베이가 Foundation Models in Robotics의 기초 연구를 의사결정과 학습 관점에서 심화 발전시킨다.
- 🏛 기반 연구: [[papers/1519_Pure_Vision_Language_Action_VLA_Models_A_Comprehensive_Surve/review]] — Foundation Models in Robotics의 전반적 분석이 VLA 모델 survey의 이론적 배경과 분류 체계를 제공한다.
- 🔄 다른 접근: [[papers/1545_Robot_Learning_in_the_Era_of_Foundation_Models_A_Survey/review]] — Foundation Models in Robotics와 함께 로봇 분야의 기초 모델을 조망하지만 이 연구는 LLM/multimodal 모델에, 다른 연구는 전반적 응용에 집중한다.
- 🔄 다른 접근: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — Foundation Models in Robotics는 동일한 로봇 foundation model 주제를 다루지만 응용과 도전 과제에 더 집중하는 다른 관점을 제공한다.
- 🔗 후속 연구: [[papers/1608_Vision-Language-Action_VLA_Models_Concepts_Progress_Applicat/review]] — 로봇공학에서 foundation model의 일반적 응용을 VLA 모델의 구체적 개념과 진전으로 확장하여 심화 분석한다.
- 🔗 후속 연구: [[papers/1300_A_Survey_on_Vision-Language-Action_Models_for_Autonomous_Dri/review]] — 자율주행용 VLA 모델 서베이는 로봇틱스 foundation model 종합 조사의 특정 도메인 확장판이다.
- 🔗 후속 연구: [[papers/1350_Deep_Reinforcement_Learning_for_Robotics_A_Survey_of_Real-Wo/review]] — Foundation model 시대의 로봇 공학에서 강화학습의 역할과 발전방향을 제시합니다.
- 🔗 후속 연구: [[papers/1357_Dexterous_Manipulation_through_Imitation_Learning_A_Survey/review]] — Foundation model 시대에 손가락 조작 모방학습의 새로운 방향성을 제시합니다.
- 🔄 다른 접근: [[papers/1361_Diffusion_Models_for_Robotic_Manipulation_A_Survey/review]] — 로봇 조작에서 diffusion model과 foundation model의 서로 다른 관점의 종합적 리뷰를 제공합니다.
