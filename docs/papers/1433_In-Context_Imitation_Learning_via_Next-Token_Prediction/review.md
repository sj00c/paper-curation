---
title: "1433_In-Context_Imitation_Learning_via_Next-Token_Prediction"
authors:
  - "Letian Fu"
  - "Huang Huang"
  - "Gaurav Datta"
  - "Lawrence Yunliang Chen"
  - "William Chung-Ho Panitch"
date: "2024.08"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇이 새로운 작업을 수행할 때 정책 파라미터 업데이트 없이 입력 단계에서 제공된 문맥 정보를 해석하는 In-Context Robot Transformer (ICRT)를 제안한다. ICRT는 감각-운동 궤적에 대한 자동회귀 다음-토큰 예측을 통해 훈련 없이 새로운 작업을 유연하게 실행할 수 있다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Semantic_Task_Generalization"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Fu et al._2024_In-Context Imitation Learning via Next-Token Prediction.pdf"
---

# In-Context Imitation Learning via Next-Token Prediction

> **저자**: Letian Fu, Huang Huang, Gaurav Datta, Lawrence Yunliang Chen, William Chung-Ho Panitch, Fangchen Liu, Hui Li, Ken Goldberg | **날짜**: 2024-08-28 | **URL**: [https://arxiv.org/abs/2408.15980](https://arxiv.org/abs/2408.15980)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: In-Context Robot Transformer (ICRT): A robot foundation model with in-context imitation learning capabilities. I*

로봇이 새로운 작업을 수행할 때 정책 파라미터 업데이트 없이 입력 단계에서 제공된 문맥 정보를 해석하는 In-Context Robot Transformer (ICRT)를 제안한다. ICRT는 감각-운동 궤적에 대한 자동회귀 다음-토큰 예측을 통해 훈련 없이 새로운 작업을 유연하게 실행할 수 있다.

## Motivation

- **Known**: LLM과 LVM이 다음-토큰 예측으로 문맥 내 학습 능력을 보여주었으며, 최근 로봇 학습도 이를 차용하여 다중 작업 정책을 개발하고 있다. 하지만 기존 로봇 모델은 새로운 환경의 미지 작업 수행을 위해 추가 훈련이나 미세 조정이 필요하다.
- **Gap**: 다음-토큰 예측 모델의 문맥 내 학습 능력이 비전과 언어 도메인에 국한되어 있으며, 실제 로봇이 소수의 시연만으로 새로운 작업을 수행할 수 있는 방법이 명확하지 않다. 또한 기존 접근법들은 복잡한 손실 함수, 키포인트 식별, 또는 보상 함수가 필요하다.
- **Why**: 로봇이 미세 조정 없이 몇 가지 시연으로 새로운 작업을 즉시 수행할 수 있으면 실제 환경에서의 적용 복잡도가 크게 감소한다. 이는 로봇 기초 모델의 실용성과 확장성을 획기적으로 향상시킨다.
- **Approach**: ICRT는 긴 문맥 윈도우를 가진 인과 transformer를 사용하여 이미지 관찰, 로봇 상태, 액션으로 구성된 감각-운동 궤적에 대해 직접 다음-토큰 예측을 수행한다. 훈련 시간에 다중 작업 데이터셋과 동일한 초기 관찰에서 다양한 작업이 가능한 데이터 구성을 활용하여 문맥 내 학습을 유도한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: Example inference pipeline of ICRT on the task of picking*

- **ICRT 모델 제안**: 긴 문맥 윈도우와 간단한 다음-토큰 예측 손실만을 사용하여 실제 로봇에서 미세 조정 없는 문맥 내 학습을 달성
- **다중 작업 데이터셋 및 훈련 패러다임**: 문맥 내 능력을 지원하는 새로운 로봇 데이터셋과 훈련 방법론 제공
- **일반화 성능**: 프롬프트와 훈련 데이터와 다른 환경 구성에서도 미지 작업을 수행 가능하며, 다중 작업 환경에서 기존 최첨단 다음-토큰 예측 모델 (Octo, OpenVLA)을 크게 능가

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: Method Overview: (Left) We encode camera observations with a pre-trained vision transformer. Additionally, we en*

- Pre-trained vision model (예: CLIP 또는 유사 모델)을 이용한 카메라 관찰 인코딩
- 인코딩된 이미지, 로봇 고유 상태(proprioceptive state), 액션을 토큰화하여 sequence 구성
- Causal transformer 기반 자동회귀 모델로 다음 토큰(액션 또는 상태) 예측
- 추론 시점에 새 작업의 인간 원격 조작 시연 궤적을 프롬프트로 제공
- 모델이 프롬프트 패턴을 추출하여 현재 환경에서 유사한 액션 시퀀스 생성
- 장기 문맥 윈도우를 통해 여러 궤적으로부터 작업 의미론 학습

## Originality

- 기존 Few-shot imitation learning과 달리 keypoint/keyframe 식별, 복잡한 손실 함수, 추가 인지 모듈 불필요
- One-Shot Imitation Learning, Prompting Decision Transformer와 다르게 완전한 상태 정보나 보상 함수 미필요, 긴 문맥 윈도우 지원, 실제 로봇에서 이미지 관찰 기반 시연
- 동일한 초기 관찰에서 다양한 작업이 가능한 데이터셋 특성을 명시적으로 활용하여 문맥 내 학습 유도하는 점이 혁신적
- 언어나 보상 함수 없이 순수 감각-운동 궤적만으로 문맥 내 학습 달성

## Limitation & Further Study

- 미지 작업이 훈련 중 사용된 모션 primitive의 조합만 가능 (완전히 새로운 작업 타입은 불가)
- 현재 실험이 특정 환경(Franka Emika, 특정 객체 세트)에 제한되어 다양한 로봇 플랫폼으로의 일반화 검증 부족
- 프롬프트 궤적의 품질과 양에 대한 민감도 분석 부재 (몇 개의 시연이 최적인지 불명확)
- 계산 효율성 및 실시간 성능에 대한 상세한 분석 미제시
- 후속 연구: (1) 완전히 새로운 motion primitive 학습 능력 추가, (2) 다양한 로봇 플랫폼 및 환경 규모 확대, (3) 프롬프트 설계 최적화 연구

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ICRT는 실제 로봇에서 처음으로 효과적인 문맥 내 학습을 보여주며, 간단한 다음-토큰 예측 프레임워크로 복잡한 시연 기반 학습을 가능하게 한다. 로봇 기초 모델의 실용성을 크게 향상시키는 의미 있는 기여이나, 일반화 범위와 기술적 깊이 면에서 추가 검증이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1316_Behavior_Transformers_Cloning_k_modes_with_one_stone/review]] — 멀티모달 행동 생성을 위한 Transformer 기반 접근법으로 in-context learning과 behavior cloning의 차이점을 비교할 수 있다.
- 🔗 후속 연구: [[papers/1328_Chain-of-Action_Trajectory_Autoregressive_Modeling_for_Robot/review]] — trajectory autoregressive modeling을 in-context learning에 적용하여 더 긴 시퀀스의 맥락 정보 활용 가능성을 탐구할 수 있다.
- 🏛 기반 연구: [[papers/1294_A_Generalist_Agent/review]] — generalist agent의 기본 개념과 next-token prediction을 통한 일반화 능력의 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1578_SPRINT_Scalable_Policy_Pre-Training_via_Language_Instruction/review]] — In-Context Imitation Learning은 SPRINT의 cross-trajectory 학습과 유사한 효율성을 next-token prediction으로 달성한다.
- 🔄 다른 접근: [[papers/1349_DataMIL_Selecting_Data_for_Robot_Imitation_Learning_with_Dat/review]] — next-token prediction을 통한 다른 모방학습 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1316_Behavior_Transformers_Cloning_k_modes_with_one_stone/review]] — 다음 토큰 예측을 통한 맥락 내 모방 학습과 Behavior Transformer의 multi-modal 행동 학습을 결합할 수 있습니다.
