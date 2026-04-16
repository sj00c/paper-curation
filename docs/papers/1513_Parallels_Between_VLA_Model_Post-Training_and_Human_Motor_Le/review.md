---
title: "1513_Parallels_Between_VLA_Model_Post-Training_and_Human_Motor_Le"
authors:
  - "Tian-Yu Xiang"
  - "Ao-Qun Jin"
  - "Xiao-Hu Zhou"
  - "Mei-Jiang Gui"
  - "Xiao-Liang Xie"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "본 논문은 Vision-Language-Action (VLA) 모델의 post-training 방법을 인간의 운동 학습 이론(Newell의 제약 주도 이론)의 관점에서 종합적으로 분석하고, 환경 지각, 신체 인식, 작업 이해, 다중 요소 통합의 4가지 범주로 체계화한 설문 논문이다."
tags:
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Embodied_AI_Architectures"
  - "cat/Embodied_Visual_Reasoning"
  - "sub/Embodied_Language_Models"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xiang et al._2025_Parallels Between VLA Model Post-Training and Human Motor Learning Progress, Challenges, and Trends.pdf"
---

# Parallels Between VLA Model Post-Training and Human Motor Learning: Progress, Challenges, and Trends

> **저자**: Tian-Yu Xiang, Ao-Qun Jin, Xiao-Hu Zhou, Mei-Jiang Gui, Xiao-Liang Xie, Shi-Qi Liu, Shuang-Yi Wang, Sheng-Bin Duan, Fu-Chao Xie, Wen-Kai Wang, Si-Cheng Wang, Ling-Yun Li, Tian Tu, Zeng-Guang Hou | **날짜**: 2025-06-26 | **URL**: [https://arxiv.org/abs/2506.20966](https://arxiv.org/abs/2506.20966)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

본 논문은 Vision-Language-Action (VLA) 모델의 post-training 방법을 인간의 운동 학습 이론(Newell의 제약 주도 이론)의 관점에서 종합적으로 분석하고, 환경 지각, 신체 인식, 작업 이해, 다중 요소 통합의 4가지 범주로 체계화한 설문 논문이다.

## Motivation

- **Known**: VLA 모델은 VLM의 시각 지각 및 명령어 이해 능력을 활용하여 다양한 조작 작업에서 우수한 일반화 성능을 보인다. 그러나 높은 정확도가 요구되는 응용에서는 사전 학습된 모델의 추가 적응 없이는 성능 격차가 발생한다.
- **Gap**: VLA 모델 적응에 대한 관심이 증가하고 있음에도 불구하고, VLA model post-training 기법에 대한 포괄적인 리뷰가 부족하다. 특히 인간의 운동 학습 이론과 연결하여 체계적으로 분석한 연구가 제한적이다.
- **Why**: VLA 모델은 NLP/CV의 foundation model에 비해 out-of-the-box 성능이 낮으며, 제한된 데이터셋, 이질적인 신체 구조, 복잡한 추상 규칙으로 인해 실제 배포 전 post-training이 필수적이다. 이는 인간의 운동 기술 획득 과정과 유사하여 신경과학과 로봇공학을 연결하는 NeuroAI 관점에서 중요하다.
- **Approach**: 본 논문은 Newell의 제약 주도 이론을 적용하여 VLA post-training 방법을 4가지 범주로 분류하고, 각 범주별 기존 연구들을 종합하며 표준 벤치마크에서의 실험 결과를 비교 분석한다. 또한 인간의 운동 학습 전략으로부터의 통찰을 VLA post-training의 향후 방법으로 제시한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4. Taxonomy of post-training VLA models proposed in this study.*

- **포괄적인 VLA post-training 리뷰**: 인간의 운동 학습 관점에서 VLA model adaptation의 현황을 체계적으로 정리한 첫 번째 종합 설문 논문
- **신경과학과 로봇공학의 통합 관점**: Newell의 제약 주도 이론을 기반으로 환경, 신체, 작업의 3가지 핵심 요소와 이들의 다중 요소 통합을 통한 post-training 방법론 체계화
- **실용적 가이드라인 제공**: 표준 벤치마크 실험 결과 종합을 통해 VLA model 개발을 위한 actionable insights 도출
- **미래 연구 방향 제시**: 현재의 열린 과제(open challenges)와 emerging trends를 명시하며 후속 연구의 방향성 제시

## How


- VLA 모델의 pre-training과 post-training 단계를 인간의 선천적 운동 프로그램과 운동 기술 학습 과정에 병렬화
- Open X-Embodiment 데이터셋을 포함한 로봇 조작 데이터셋의 규모 변화 추적으로 VLA 모델 발전의 데이터 기반 분석
- VLA 모델 아키텍처 비교: 별도 인코더 방식(a)과 LLM 기반 토큰화 방식(b) 검토
- Post-training 방법을 4가지 범주로 구조화: (i) 환경 지각 강화 (ii) 신체 인식 개선 (iii) 작업 이해 심화 (iv) 다중 요소 통합
- 표준 벤치마크에서의 비교 실험 결과 종합 및 분석

## Originality

- **Newell 이론의 로봇공학 적용**: 인간 운동 학습의 제약 주도 이론을 VLA post-training 체계화에 처음 적용한 novel perspective
- **NeuroAI 관점의 통합**: 신경과학과 로봇공학의 접점을 명시적으로 연결하여 foundation model 적응의 생물학적 근거 제시
- **체계적 분류 프레임워크**: 기존의 산발적인 post-training 방법들을 환경-신체-작업의 3가지 제약 조건에 따라 최초로 통합 분류
- **인간 학습 전략의 역이용**: 인간이 운동 기술을 습득하는 방식으로부터 VLA post-training의 향후 방법론 도출

## Limitation & Further Study

- **데이터 격차 미해결**: 로봇 조작 데이터가 여전히 NLP 대비 매우 부족하며, 이에 대한 근본적인 해결책이 제시되지 않음
- **이질적 신체 구조의 일반화**: 다양한 로봇 플랫폼 간의 동력학 차이를 극복하는 범용적 post-training 방법이 미개발 상태
- **복잡한 추상 규칙의 표현**: 조작 작업의 고수준 추상 규칙을 언어로 명확히 표현하고 학습하는 방법이 여전히 미완성
- **벤치마크의 제한성**: 실제 현장의 노이즈, 불확실성, 동적 환경을 충분히 반영하지 못하는 표준 벤치마크의 한계
- **후속 연구 방향**: (1) 합성 데이터와 시뮬레이션 활용을 통한 데이터 부족 문제 해결, (2) 도메인 적응(domain adaptation) 기법의 강화, (3) meta-learning을 통한 빠른 적응, (4) human-in-the-loop 학습 방식의 체계화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 VLA model post-training을 인간의 운동 학습 이론으로 통합 분석한 창의적인 설문 논문으로, NeuroAI 패러다임의 중요성을 강조하며 로봇공학 커뮤니티에 명확한 가이드라인을 제공한다. 다만 이론적 프레임워크 제시 중심이므로 각 범주의 구체적 기술 발전과 미해결 문제에 대한 심화 분석이 추가되면 더욱 실무적 가치가 높아질 것이다.

## Related Papers

- 🧪 응용 사례: [[papers/1573_SimpleVLA-RL_Scaling_VLA_Training_via_Reinforcement_Learning/review]] — 인간 운동학습 이론의 관점에서 분석한 VLA post-training 방법들이 SimpleVLA-RL의 강화학습 기반 훈련에 실제 적용될 수 있다.
- 🏛 기반 연구: [[papers/1493_Neural_Scaling_Laws_in_Robotics/review]] — Neural Scaling Laws가 VLA 모델의 post-training 효과를 정량적으로 이해하는 이론적 기반을 제공한다.
- 🔗 후속 연구: [[papers/1425_Human2Robot_Learning_Robot_Actions_from_Paired_Human-Robot_V/review]] — Human2Robot의 인간-로봇 학습 패러다임이 Newell의 제약 주도 이론을 실제 로봇 학습으로 확장한 구체적 사례다.
- 🏛 기반 연구: [[papers/1426_HumanPlus_Humanoid_Shadowing_and_Imitation_from_Humans/review]] — VLA post-training 분석이 참조하는 인간 운동 학습의 실제 적용 사례인 humanoid imitation
- 🔗 후속 연구: [[papers/1619_VLA-RFT_Vision-Language-Action_Reinforcement_Fine-tuning_wit/review]] — 인간 운동 학습 관점의 VLA post-training을 reinforcement fine-tuning으로 실제 구현
- 🔄 다른 접근: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — VLA 모델 구축에서 human motor learning vs engineering optimization의 다른 관점
- 🏛 기반 연구: [[papers/1609_Vision-Language-Action_Models_for_Robotics_A_Review_Towards/review]] — VLA 모델 post-training 방법론은 VLA 모델 전반의 개념과 응용을 이해하는 데 필수적입니다.
- 🔄 다른 접근: [[papers/1338_ConRFT_A_Reinforced_Fine-tuning_Method_for_VLA_Models_via_Co/review]] — 운동 학습 이론 기반 접근과 ConRFT의 강화된 fine-tuning은 서로 다른 VLA 개선 방법론을 제시합니다.
- 🏛 기반 연구: [[papers/1573_SimpleVLA-RL_Scaling_VLA_Training_via_Reinforcement_Learning/review]] — VLA 모델의 강화학습 확장이 인간 운동학습 이론에서 분석된 post-training 방법들을 실제 구현으로 발전시킨다.
