---
title: "1405_Generative_Artificial_Intelligence_in_Robotic_Manipulation_A"
authors:
  - "Kun Zhang"
  - "Peng Yun"
  - "Jun Cen"
  - "Junhao Cai"
  - "Didi Zhu"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "로봇 조작(robotic manipulation) 분야에서 생성형 AI 모델들(GAN, VAE, diffusion model 등)의 최근 발전을 종합적으로 검토하는 서베이로, 데이터 부족, 장기 태스크 계획, 다중 모드 추론이라는 세 가지 핵심 도전 과제를 해결하는 방법을 제시한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Zhang et al._2025_Generative Artificial Intelligence in Robotic Manipulation A Survey.pdf"
---

# Generative Artificial Intelligence in Robotic Manipulation: A Survey

> **저자**: Kun Zhang, Peng Yun, Jun Cen, Junhao Cai, Didi Zhu, Hangjie Yuan, Chao Zhao, Tao Feng, Michael Yu Wang, Qifeng Chen, Jia Pan, Wei Zhang, Bo Yang, Hua Chen | **날짜**: 2025-03-05 | **URL**: [https://arxiv.org/abs/2503.03464](https://arxiv.org/abs/2503.03464)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. Overview of this survey. Versatile generative models in robotic manipulation.*

로봇 조작(robotic manipulation) 분야에서 생성형 AI 모델들(GAN, VAE, diffusion model 등)의 최근 발전을 종합적으로 검토하는 서베이로, 데이터 부족, 장기 태스크 계획, 다중 모드 추론이라는 세 가지 핵심 도전 과제를 해결하는 방법을 제시한다.

## Motivation

- **Known**: 데이터 기반 로봇 조작 방법들(RL, IL)이 점진적으로 주류 방법론이 되고 있으며, generative model들이 이미지 생성, 보상 함수 생성, 행동 예측 등에서 우수한 성능을 보이고 있다.
- **Gap**: 개별 generative model 패러다임들(GAN, VAE, diffusion model 등)이 로봇 조작에 어떻게 응용되는지, 그리고 Foundation Layer에서 Policy Layer까지 어떻게 계층화되어 활용되는지에 대한 체계적인 분류와 종합 검토가 부족했다.
- **Why**: 로봇 조작은 산업 자동화부터 가정 내 보조 작업까지 실제 사회적 영향이 큰 분야이며, 데이터 부족과 복잡한 장기 계획이라는 근본적인 병목을 해결하기 위해서는 generative model들의 다양한 활용 방법을 체계적으로 이해할 필요가 있다.
- **Approach**: 이 서베이는 다섯 가지 주요 generative model 패러다임(GAN, VAE, diffusion model, probabilistic flow model, autoregressive model)을 식별하고, 이들을 Foundation Layer(데이터 및 보상 생성), Intermediate Layer(언어, 코드, 시각, 상태 생성), Policy Layer(그래스 및 궤적 생성)의 세 계층으로 분류하여 분석한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1. Overview of this survey. Versatile generative models in robotic manipulation.*

- **계층적 분류 체계**: generative model의 로봇 조작 응용을 Foundation, Intermediate, Policy 세 계층으로 체계화하여 각 계층의 역할과 상호작용을 명확히 함
- **도전 과제 연계**: 데이터 부족, 장기 태스크 계획, 다중 모드 추론이라는 세 가지 핵심 도전이 generative model들을 통해 어떻게 해결 가능한지 구체적으로 설명
- **다양한 모델 커버리지**: GAN, VAE, diffusion model, probabilistic flow model, autoregressive model 등 현재의 주요 generative 패러다임들의 강점과 한계를 함께 제시
- **State-of-the-art 작업 수집**: 각 분야에서 최신 성과를 낸 연구들을 종합하고, GitHub 리소스(AwesomeGAIManipulation)를 통해 커뮤니티에 공개

## How

![Figure 1](figures/fig1.webp)

*Fig. 1. Overview of this survey. Versatile generative models in robotic manipulation.*

- generative model 패러다임의 분류: 생성 방식에 따라 GAN, VAE, diffusion model, probabilistic flow model, autoregressive model로 구분
- Foundation Layer 분석: synthetic image 생성(Stable Diffusion 등)으로 데이터 부족 완화, 대규모 사전학습 언어 모델로 보상 신호 생성
- Intermediate Layer 분석: language generation과 code generation으로 Chain-of-Thought 기반 태스크 분해, visual generation으로 미래 상태 예측, state generation으로 동역학 학습
- Policy Layer 분석: diffusion model 기반 Diffusion Policy로 그래스 생성, trajectory generation으로 복잡한 조작 경로 계획
- 멀티모달 추론 처리: 하나의 상태에 대응하는 여러 valid action/outcome의 다양성을 생성 모델의 확률적 특성으로 포착

## Originality

- 로봇 조작에 특화된 generative model 서베이로, 기존의 일반적인 generative model 리뷰보다 도메인 특화적인 분석 제공
- 세 계층 구조(Foundation-Intermediate-Policy)라는 새로운 분류 체계를 제안하여 generative model들의 역할을 위계적으로 정리
- 데이터 부족, 장기 계획, 다중 모드 추론이라는 로봇 조작의 구체적 도전 과제와 generative model 솔루션을 명시적으로 연결
- 여러 모델 패러다임(GAN, VAE, diffusion, flow, autoregressive)을 동일 프레임워크 내에서 비교 분석

## Limitation & Further Study

- 현장 실험 데이터 부족: 대부분의 분석이 논문 기반 문헌 검토이므로, 실제 로봇 시스템에서의 성능 비교 데이터 부족
- 계산 효율성 논의 미흡: generative model들의 추론 속도, 메모리 사용량 등 실시간 로봇 제어에 필요한 실용적 고려사항에 대한 상세한 분석 부재
- 크로스 모달 통합 미성숙: 여러 모드(vision, language, code, tactile, depth)의 효과적 통합 방법론이 아직 확립되지 않은 상태
- 일반화 보증 부족: 합성 데이터와 실제 환경 간 domain gap, 새로운 객체나 환경에 대한 일반화 성능 보장이 아직 충분하지 않음
- 후속 연구 방향: (1) 데이터 효율성 개선을 위한 few-shot learning 기법 개발, (2) long-horizon task의 계획-실행 피드백 루프 강화, (3) 다양한 로봇 플랫폼과 환경에서의 검증 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 이 서베이는 로봇 조작이라는 중요한 응용 분야에서 generative model들의 역할을 체계적으로 종합한 포괄적 리뷰로, 세 계층 분류 체계와 도전 과제 연계를 통해 해당 분야의 종사자들에게 명확한 로드맵을 제공하며, 그래프와 자료를 통해 고도의 명확성을 갖춘다. 다만 실제 시스템 구현과 성능 비교, 계산 효율성 등 실용적 측면에 대한 깊이 있는 논의가 보충되면 더욱 가치 있을 것으로 예상된다.

## Related Papers

- 🏛 기반 연구: [[papers/1361_Diffusion_Models_for_Robotic_Manipulation_A_Survey/review]] — 로봇 조작에서 diffusion model 사용에 대한 기초적인 서베이를 제공하여 생성형 AI 전반의 이해를 돕는다.
- 🔗 후속 연구: [[papers/1445_Large_Model_Empowered_Embodied_AI_A_Survey_on_Decision-Makin/review]] — 생성형 AI 모델들의 로봇 조작 활용을 구체적으로 다루며, 대규모 모델 기반 embodied AI 서베이와 상호 보완적이다.
- 🔄 다른 접근: [[papers/1398_Foundation_Models_in_Robotics_Applications_Challenges_and_th/review]] — Foundation model의 로봇 적용을 다각도로 분석한 서베이와 생성형 AI 중심의 다른 관점을 제시한다.
- 🔗 후속 연구: [[papers/1485_Multimodal_Fusion_and_Vision-Language_Models_A_Survey_for_Ro/review]] — Multimodal Fusion and Vision-Language Models 서베이는 생성형 AI를 멀티모달 로봇 학습으로 확장한 포괄적 검토임
- 🔗 후속 연구: [[papers/1357_Dexterous_Manipulation_through_Imitation_Learning_A_Survey/review]] — dexterous manipulation의 imitation learning을 생성형 AI 관점에서 확장한 포괄적 조사입니다.
