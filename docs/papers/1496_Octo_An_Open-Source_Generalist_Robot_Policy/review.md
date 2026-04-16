---
title: "1496_Octo_An_Open-Source_Generalist_Robot_Policy"
authors:
  - "Octo Model Team"
  - "Dibya Ghosh"
  - "Homer Walke"
  - "Karl Pertsch"
  - "Kevin Black"
date: "2024.05"
doi: ""
arxiv: ""
score: 4.0
essence: "Open X-Embodiment 데이터셋의 800k 궤적으로 사전학습된 transformer 기반의 generalist robot policy인 Octo를 제안하며, 언어 명령이나 목표 이미지로 지시 가능하고 새로운 센서와 액션 공간으로 효율적으로 미세조정 가능하다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Team et al._2024_Octo An Open-Source Generalist Robot Policy.pdf"
---

# Octo: An Open-Source Generalist Robot Policy

> **저자**: Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, Sergey Levine | **날짜**: 2024-05-20 | **URL**: [https://arxiv.org/abs/2405.12213](https://arxiv.org/abs/2405.12213)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: We introduce Octo, an open-source, generalist policy for robotic manipulation. Octo is a transformer-based polic*

Open X-Embodiment 데이터셋의 800k 궤적으로 사전학습된 transformer 기반의 generalist robot policy인 Octo를 제안하며, 언어 명령이나 목표 이미지로 지시 가능하고 새로운 센서와 액션 공간으로 효율적으로 미세조정 가능하다.

## Motivation

- **Known**: RT-1, RoboCat 등 여러 robot embodiment을 다루는 generalist robot policy들이 제안되었으나, 대부분 사전정의된 센서와 액션 공간으로 제한되고 공개되지 않았다.
- **Gap**: 기존 generalist robot policy들은 새로운 관측과 액션 공간으로의 효율적인 미세조정을 지원하지 않으며, 다양한 로봇 플랫폼의 센서 설정 변화에 대응하기 어렵다.
- **Why**: 대규모 사전학습 정책의 공개는 로봇 커뮤니티의 접근성을 높이고, 효율적인 미세조정 능력은 새로운 로봇 설정에 빠르게 적응할 수 있게 하여 실제 응용을 가능케 한다.
- **Approach**: Tokenizer 기반 transformer 아키텍처로 임의의 입력(다양한 카메라, 센서)과 출력(다양한 액션 공간)을 처리하고, block-wise attention 구조로 새로운 관측 및 액션 헤드를 추가하여 미세조정한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1: We introduce Octo, an open-source, generalist policy for robotic manipulation. Octo is a transformer-based polic*

- **최대 규모 데이터셋 활용**: Open X-Embodiment의 800k 로봇 궤적으로 사전학습하여 이전 generalist robot policy보다 훨씬 큰 데이터에 노출
- **유연한 인터페이스**: 언어 명령 또는 목표 이미지로 지시 가능하며, 다양한 카메라 설정(워크스페이스, 손목 카메라)과 액션 공간(관절 제어, end-effector 제어)을 지원
- **효율적 미세조정**: 표준 consumer GPU에서 몇 시간 내에 새로운 센서와 액션 공간으로 미세조정 가능
- **9개 로봇 플랫폼 검증**: 4개 기관의 다양한 로봇(WidowX, UR5, RT-1 등)에서 우수한 성능 입증
- **완전 공개**: 모델 체크포인트(27M, 93M 파라미터), 사전학습 파이프라인, 미세조정 스크립트 등 전체 리소스 공개

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: Model architecture. Left: Octo tokenizes task descriptions (green) and input observations (blue) using a pretrai*

- Task tokens (언어 인코더로 처리) + Observation tokens (lightweight CNN으로 처리)를 생성
- Transformer backbone에서 block-wise attention으로 시퀀스 처리하여 readout tokens 생성
- Diffusion head를 통해 expressive action distribution 모델링
- Action chunks 예측으로 temporal consistency 향상
- 미세조정 시 새로운 observation/action head 추가 및 adapters 사용으로 기존 파라미터 보존
- 대규모 다양한 데이터 혼합으로 사전학습하여 generalization 극대화

## Originality

- Transformer, diffusion objectives, action chunks, block-wise attention 등 기존 기법들의 조합이 novel하며, 특히 cross-embodied generalist policy 맥락에서 처음 적용
- 새로운 관측 및 액션 공간으로의 적응을 위해 adapter 기반 미세조정 방식 도입
- Open X-Embodiment 데이터의 최대 규모 활용으로 이전 연구보다 훨씬 큰 다양성 확보
- 완전 공개형 generalist robot policy로서 선례적 기여

## Limitation & Further Study

- 논문에서 미세조정 성능의 상세한 정량 비교 부족 (새로운 도메인별 향상도 수치 제한적)
- 9개 로봇이 모두 조작(manipulation) 태스크에 한정되어 navigation 등 다른 도메인 일반화 능력 미검증
- Diffusion head의 계산 비용이 더 높은지 여부와 real-time 제어 가능성 불명확
- 후속 연구: 다른 로봇 도메인(navigation, quadruped 등)으로의 확장, 더 큰 규모 사전학습, 온라인 학습 능력 추가 연구 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Octo는 대규모 다양한 데이터와 유연한 아키텍처로 generalist robot policy의 실질적 발전을 이루었으며, 완전 공개를 통해 로봇 커뮤니티에 즉시적 기여를 제공한다. 미세조정 효율성과 다중 플랫폼 호환성은 실제 응용성을 크게 높인다.

## Related Papers

- 🏛 기반 연구: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Octo가 활용하는 Open X-Embodiment 데이터셋과 다중 로봇 플랫폼에서의 positive transfer 방법론의 기초를 제공한다.
- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — Octo와 유사한 generalist robot policy이지만 더 큰 7B 파라미터 규모와 오픈소스 접근법으로 차별화된다.
- 🔗 후속 연구: [[papers/1562_Scaling_Cross-Embodied_Learning_One_Policy_for_Manipulation/review]] — Octo의 cross-embodiment learning을 더욱 확장하여 single policy로 다양한 manipulation 작업을 처리하는 방법을 제시한다.
- 🔄 다른 접근: [[papers/1294_A_Generalist_Agent/review]] — Gato의 범용성 개념을 로봇 특화로 발전시켜 더 실용적인 오픈소스 정책 모델로 구현
- 🔄 다른 접근: [[papers/1484_MuJoCo_Playground/review]] — MuJoCo Playground와 Octo 모두 범용 로봇 정책 학습을 위한 프레임워크이지만 서로 다른 접근 방식을 사용합니다.
- 🏛 기반 연구: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Open X-Embodiment 데이터를 활용한 범용 로봇 정책 개발의 후속 연구에 해당한다.
- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — 오픈소스 generalist robot policy에서 VLA vs Octo의 다른 접근법
- 🔄 다른 접근: [[papers/1534_RoboAgent_Generalization_and_Efficiency_in_Robot_Manipulatio/review]] — 범용 로봇 조작 에이전트 구축에서 RoboAgent는 semantic augmentation을, Octo는 대규모 오픈소스 데이터를 활용한다.
- 🔄 다른 접근: [[papers/1537_RoboCat_A_Self-Improving_Generalist_Agent_for_Robotic_Manipu/review]] — Octo와 함께 범용 로봇 정책을 추구하지만 RoboCat는 자가 개선에, Octo는 오픈소스 일반화에 초점을 맞춘 서로 다른 접근이다.
- 🏛 기반 연구: [[papers/1546_Robot_Utility_Models_General_Policies_for_Zero-Shot_Deployme/review]] — Octo의 오픈소스 범용 로봇 정책 연구가 RUM의 다양한 환경에서 즉시 배포 가능한 정책 개발에 기술적 기초를 제공한다.
- 🔄 다른 접근: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — Octo는 RT-1과 같은 일반화 가능한 로봇 정책을 목표로 하지만 더 광범위한 embodiment를 지원하는 차별점이 있다.
- 🔗 후속 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-2의 VLM 기반 로봇 제어 개념을 Octo가 범용 정책으로 확장한다.
- 🔄 다른 접근: [[papers/1558_RVT-2_Learning_Precise_Manipulation_from_Few_Demonstrations/review]] — Octo와 RVT-2는 범용 로봇 정책 학습에서 서로 다른 모델 설계 철학을 보여줍니다.
- 🔗 후속 연구: [[papers/1620_VLA-RL_Towards_Masterful_and_General_Robotic_Manipulation_wi/review]] — Octo의 일반적인 로봇 정책을 강화학습으로 개선하여 분포 외 시나리오에서의 성능 향상을 달성한다.
- 🏛 기반 연구: [[papers/1627_What_Matters_in_Building_Vision-Language-Action_Models_for_G/review]] — Generalist robot policy의 기본 개념을 제공하여 VLA 모델 설계에서 고려해야 할 핵심 요소들의 이론적 근거를 마련한다.
- 🔄 다른 접근: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — Octo는 RoboFlamingo와 같은 일반화 가능한 로봇 정책이지만 더 광범위한 embodiment를 지원하는 차별점이 있다.
- 🏛 기반 연구: [[papers/1609_Vision-Language-Action_Models_for_Robotics_A_Review_Towards/review]] — Octo의 오픈소스 범용 로봇 정책이 VLA 모델의 실제 배포를 위한 실용적 프레임워크의 기반을 제공한다.
- 🏛 기반 연구: [[papers/1314_AutoEval_Autonomous_Evaluation_of_Generalist_Robot_Manipulat/review]] — 범용 로봇 정책의 기초적 구현인 Octo 모델 평가에 활용된다.
- 🧪 응용 사례: [[papers/1315_AutoRT_Embodied_Foundation_Models_for_Large_Scale_Orchestrat/review]] — Octo의 오픈소스 generalist 로봇 정책은 AutoRT의 대규모 데이터 수집을 활용한 실용적 응용 사례이다.
- 🧪 응용 사례: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — BridgeData V2가 Octo와 같은 generalist robot policy 모델의 훈련 데이터로 직접 활용됩니다.
- 🔄 다른 접근: [[papers/1374_DynamicVLA_A_Vision-Language-Action_Model_for_Dynamic_Object/review]] — 동적 객체에 특화된 compact VLA와 범용 generalist robot policy의 서로 다른 설계 철학을 보여줍니다.
- 🏛 기반 연구: [[papers/1356_DexGraspVLA_A_Vision-Language-Action_Framework_Towards_Gener/review]] — Octo의 generalist robot policy 개념은 DexGraspVLA가 추구하는 일반적인 dexterous manipulation을 위한 기초 모델 아키텍처를 제공한다.
