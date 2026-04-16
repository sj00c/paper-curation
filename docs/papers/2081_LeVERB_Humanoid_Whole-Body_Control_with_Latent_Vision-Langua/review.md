---
title: "2081_LeVERB_Humanoid_Whole-Body_Control_with_Latent_Vision-Langua"
authors:
  - "Haoru Xue"
  - "Xiaoyu Huang"
  - "Dantong Niu"
  - "Qiayuan Liao"
  - "Thomas Kragerud"
date: "2025.06"
doi: ""
arxiv: ""
score: 4.0
essence: "LeVERB는 humanoid 로봇의 전신 제어를 위해 vision-language 입력을 latent action 공간으로 인코딩하는 계층적 프레임워크를 제안하며, 150개 이상의 task로 구성된 첫 번째 sim-to-real 준비 벤치마크를 제시한다."
tags:
  - "cat/Motion_Learning_from_Demonstration"
  - "cat/Diffusion-Based_Motion_Generation"
  - "cat/Adaptive_Locomotion_and_Control"
  - "sub/Egocentric_Manipulation_Imitation"
  - "topic/humanoid"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Xue et al._2025_LeVERB Humanoid Whole-Body Control with Latent Vision-Language Instruction.pdf"
---

# LeVERB: Humanoid Whole-Body Control with Latent Vision-Language Instruction

> **저자**: Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, Guanya Shi, Trevor Darrell, Koushil Sreenath, Shankar Sastry | **날짜**: 2025-06-16 | **URL**: [https://arxiv.org/abs/2506.13751](https://arxiv.org/abs/2506.13751)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of our contributions. Top: we create a photorealistic and dynamically accurate*

LeVERB는 humanoid 로봇의 전신 제어를 위해 vision-language 입력을 latent action 공간으로 인코딩하는 계층적 프레임워크를 제안하며, 150개 이상의 task로 구성된 첫 번째 sim-to-real 준비 벤치마크를 제시한다.

## Motivation

- **Known**: Vision-Language-Action(VLA) 모델은 강력한 의미 이해와 zero-shot 일반화를 보여주었으나, 대부분의 기존 시스템은 end-effector pose나 root velocity 같은 hand-crafted action 'vocabulary'를 가정하여 quasi-static task에만 국한된다.
- **Gap**: humanoid whole-body control(WBC)을 위한 agile한 전신 동작을 지원하는 vision-language 시스템의 부재, 그리고 photorealistic rendering을 포함한 WBC 벤치마크의 부족이 존재한다.
- **Why**: Humanoid 로봇이 복잡한 장면을 인지하고 언어 명령을 해석하며 전신 동작을 실행하도록 하는 것은 로봇공학의 중요한 목표이며, 이는 고차원 비선형 동역학 시스템의 제어를 요구한다.
- **Approach**: CVAE 기반 architecture를 통해 vision-language 정책이 synthetic kinematic demonstration에서 latent action vocabulary를 학습하고, 강화학습 기반 WBC 정책이 이러한 latent verb를 dynamics-level command로 변환하는 이중 과정(System 2-System 1) 구조를 제안한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of our contributions. Top: we create a photorealistic and dynamically accurate*

- **LeVERB-Bench 구축**: 10개 카테고리 150개 이상의 task로 구성된 photorealistic, sim-to-real 준비 벤치마크 개발
- **성능 달성**: 단순 navigation task에서 80% success rate, 전체적으로 58.5% success rate 달성하며 naive hierarchical VLA보다 7.8배 우수
- **Zero-shot 실제 배포**: synthetic data로만 학습되어 실제 humanoid 로봇에 zero-shot 배포 가능함을 입증
- **Latent instruction interface**: 손으로 설계한 action vocabulary 대신 structured latent space를 통해 표현력 있는 전신 동작 및 장면 상호작용 지원

## How

![Figure 3](figures/fig3.webp)

*Figure 3: Details of our data collection and training pipeline. Step 1: we collect a synthetic,*

- Human motion capture 데이터를 humanoid 로봇으로 retargeting한 후 photorealistic rendering으로 합성 데이터 생성
- Diverse scene context에서 randomized visual rendering 수행
- VLM을 사용한 semantic language annotation을 통해 robot-specific video-language pair 데이터 구성
- CVAE 기반 high-level vision-language policy로 structured latent space 학습
- Kinematics reconstruction으로 visual과 motion semantics 정렬
- Frozen latent space에서 proprioception-only controller 학습을 통해 robot dynamics 마스터링
- High-frequency(50Hz) low-level WBC와 low-frequency(10Hz) vision-language processing의 분리
- Closed-loop evaluation을 위한 dynamic simulation environment 구성

## Originality

- Humanoid WBC를 위한 latent vision-language interface 설계의 첫 사례
- Photorealistic rendering과 physics-based simulation을 모두 포함한 최초의 WBC 벤치마크 제시
- Human-inspired dual-process architecture(System 1-System 2)를 humanoid 로봇 제어에 체계적으로 적용
- Synthetic data만을 사용한 zero-shot sim-to-real transfer 달성
- CVAE를 활용한 structured latent space 학습으로 vision-language-action distribution 통합

## Limitation & Further Study

- 전체 success rate 58.5%는 복잡한 task의 어려움을 시사하며, 특히 seated interactions이나 복합 동작에서의 성능 개선 필요
- 합성 데이터의 domain gap이 여전히 존재할 수 있으며, 더 다양한 실제 환경에서의 검증 필요
- 고주파 WBC 정책의 계산 복잡도 및 실시간 성능에 대한 상세한 분석 부족
- Language instruction의 다양성과 robust성에 대한 광범위한 평가 필요
- 후속 연구로는 실제 데이터 수집을 통한 fine-tuning, 더 복잡한 multi-agent scenario 확대, 그리고 transfer learning 기법의 적용이 필요함

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: LeVERB는 humanoid WBC를 위한 vision-language 제어에서 중요한 진전을 이루었으며, 첫 latent instruction-following framework와 comprehensive sim-to-real 벤치마크를 제시하여 이 분야의 기초를 다졌다. 다만 실제 배포 성능의 추가 개선과 더 광범위한 task 평가를 통한 검증이 필요하다.

## Related Papers

- 🔄 다른 접근: [[papers/1937_FRoM-W1_Towards_General_Humanoid_Whole-Body_Control_with_Lan/review]] — 언어 기반 일반 휴머노이드 전신 제어와 시각-언어 지시사항 통합이라는 다른 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1670_SENTINEL_A_Fully_End-to-End_Language-Action_Model_for_Humano/review]] — 완전한 종단간 언어-행동 모델의 확장된 구현을 보여준다.
- 🏛 기반 연구: [[papers/1847_Commanding_Humanoid_by_Free-form_Language_A_Large_Language_A/review]] — 자유 형식 언어를 통한 휴머노이드 명령의 이론적 기반을 제공한다.
- 🔄 다른 접근: [[papers/1901_EgoHumanoid_Unlocking_In-the-Wild_Loco-Manipulation_with_Rob/review]] — 둘 다 egocentric video를 활용한 humanoid 조작 학습이지만 LeVERB는 vision-language instruction에 중점을 둔 차이가 있다
- 🏛 기반 연구: [[papers/1886_DreamControl_Human-Inspired_Whole-Body_Humanoid_Control_for/review]] — DreamControl의 whole-body humanoid control 기법이 LeVERB의 계층적 전신 제어 프레임워크 설계에 기반이 되었다
- 🔄 다른 접근: [[papers/2093_Masquerade_Learning_from_In-the-wild_Human_Videos_using_Data/review]] — 인간 비디오로부터 로봇 조작 정책을 학습하는 다른 접근법으로, 데이터 편집과 latent 인코딩의 차이점을 비교할 수 있다.
- 🔗 후속 연구: [[papers/1937_FRoM-W1_Towards_General_Humanoid_Whole-Body_Control_with_Lan/review]] — LeVERB의 latent vision-language embedding을 실제 언어 지시문 처리와 안정적인 로봇 실행이 결합된 완전한 시스템으로 발전시켰습니다.
- 🔗 후속 연구: [[papers/2166_ULTRA_Unified_Multimodal_Control_for_Autonomous_Humanoid_Who/review]] — LeVERB의 latent vision-language control에 ULTRA의 egocentric 시각 인지를 통합하면 더 자연스러운 whole-body control 가능
