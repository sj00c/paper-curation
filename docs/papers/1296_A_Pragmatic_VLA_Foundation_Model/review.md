---
title: "1296_A_Pragmatic_VLA_Foundation_Model"
authors:
  - "Wei Wu"
  - "Fan Lu"
  - "Yunnan Wang"
  - "Shuai Yang"
  - "Shi Liu"
date: "2026.01"
doi: ""
arxiv: ""
score: 4.0
essence: "LingBot-VLA는 약 20,000시간의 실제 로봇 데이터로 학습한 Vision-Language-Action 기초 모델로, 효율적인 학습과 다중 플랫폼 일반화 능력을 갖춘다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robot_Policy_Learning"
  - "sub/Broad_Task_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Wu et al._2026_A Pragmatic VLA Foundation Model.pdf"
---

# A Pragmatic VLA Foundation Model

> **저자**: Wei Wu, Fan Lu, Yunnan Wang, Shuai Yang, Shi Liu, Fangjing Wang, Qian Zhu, He Sun, Yong Wang, Shuailei Ma, Yiyu Ren, Kejia Zhang, Hui Yu, Jingmei Zhao, Shuai Zhou, Zhenqi Qiu, Houlong Xiong, Ziyu Wang, Zechen Wang, Ran Cheng, Yong-Lu Li, Yongtao Huang, Xing Zhu, Yujun Shen, Kecheng Zheng | **날짜**: 2026-01-26 | **URL**: [https://arxiv.org/abs/2601.18692](https://arxiv.org/abs/2601.18692)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. Overview of LingBot-VLA. We scale dual-arm robot data collected in the real world for pre-training. LingBot-VL*

LingBot-VLA는 약 20,000시간의 실제 로봇 데이터로 학습한 Vision-Language-Action 기초 모델로, 효율적인 학습과 다중 플랫폼 일반화 능력을 갖춘다.

## Motivation

- **Known**: Vision-Language-Action 기초 모델은 대규모 사전학습을 통해 자연어 지시로 다양한 로봇 조작 작업을 수행할 수 있으며, 최근 VLA 모델들이 diffusion 기반 action head와 사전학습된 vision-language 모델을 활용하고 있다.
- **Gap**: 기존 연구는 실제 로봇 데이터의 규모에 따른 성능 스케일링 거동을 체계적으로 조사하지 않았으며, 대규모 데이터로 효율적인 학습을 지원하는 최적화된 코드베이스가 부족하다.
- **Why**: VLA 모델의 스케일링 거동을 이해하는 것은 향후 모델 개발과 데이터 수집 전략 수립에 필수적이며, 실제 배포를 위해서는 높은 계산 효율성과 실제 환경에서의 신뢰할 수 있는 평가가 필요하다.
- **Approach**: 3,000시간에서 20,000시간으로 데이터를 확장하여 스케일링 거동을 조사하고, 3개 로봇 플랫폼에서 각각 100개 작업을 130 에피소드씩 수행하는 체계적인 벤치마킹을 실시하며, 최적화된 코드베이스로 훈련 처리량을 1.5~2.8배 향상시킨다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2. Visualization of pre-training dataset used by LingBot-VLA.*

- **스케일링 증거**: 20,000시간까지 포화 현상 없이 데이터 증가에 따라 지속적이고 상당한 성공률 개선을 달성하여 실제 로봇 학습의 우호적 스케일링 특성을 처음으로 실증적 증거를 제공
- **다중 플랫폼 성능**: 9개 로봇 구성에서 수집한 대규모 다양한 데이터로 학습한 LingBot-VLA가 3개 평가 플랫폼에서 경쟁 모델 대비 명확한 우월성과 강한 일반화 능력을 입증
- **계산 효율성**: 8-GPU 훈련 설정에서 초당 261 샘플의 처리량을 달성하여 기존 VLA 코드베이스 대비 1.5~2.8배 속도 향상으로 훈련 사이클 단축과 계산 오버헤드 감소
- **평가 표준**: GM-100 벤치마크를 활용한 체계적 평가 프레임워크로 작업 다양성과 다중 플랫폼 일관성을 강조하여 VLA 벤치마킹의 새로운 기준 제시
- **오픈 소스 기여**: 코드, 기초 모델, 벤치마크 데이터에 대한 공개 접근을 제공하여 커뮤니티 발전 촉진

## How

![Figure 1](figures/fig1.webp)

*Figure 1. Overview of LingBot-VLA. We scale dual-arm robot data collected in the real world for pre-training. LingBot-VL*

- 9개 서로 다른 dual-arm 로봇 구성(AgiBot G1, AgileX, Galaxea R1Lite, Galaxea R1Pro, Realman Rs-02, Leju KUAVO 4 Pro, Qinglong, ARX Lift2, Bimanual Franka)에서 원격 조종(VR 기반 및 isomorphic arms)으로 대규모 실제 데이터 수집
- 자동 주석 처리와 인간 개선을 결합한 다층 데이터 라벨링: 영상 세그먼트 분해, atomic action 정의, 자연어 지시 생성
- 사전학습된 vision-language 모델을 의미론적 백본으로 활용하고 diffusion 기반 action head를 결합한 VLA 아키텍처
- 데이터 로딩, 분산 훈련 전략, 연산자 수준 가속화의 체계적 최적화를 통한 고성능 코드베이스 개발
- GM-100 벤치마크의 100개 작업에 대해 각 플랫폼당 130 에피소드 수행하는 표준화된 다중 플랫폼 평가 프로토콜

## Originality

- 기존 VLA 모델 대비 약 2배 규모인 ~20,000시간의 실제 로봇 데이터를 9개 서로 다른 dual-arm 로봇 구성에서 수집하여 전례 없는 규모와 다양성의 데이터셋 제공
- 실제 환경에서 3,000~20,000시간 범위에서 데이터 스케일에 따른 VLA 모델의 성능 스케일링 거동을 처음으로 체계적이고 실증적으로 조사
- 300개 작업 × 3 플랫폼의 대규모 실제 로봇 벤치마킹으로 기존의 제한적 비교 평가를 넘어선 포괄적 평가 프레임워크 제시
- 데이터 I/O 병목과 통신 오버헤드를 해결한 최적화된 VLA 훈련 코드베이스로 1.5~2.8배 처리량 향상 달성

## Limitation & Further Study

- 평가가 3개 플랫폼(GM-100 벤치마크 기반)으로 제한되어 있으며, 데이터 수집에 사용된 9개 플랫폼과의 직접적 평가 비교 부재
- 약 20,000시간에서 포화가 없다는 것이 입증되었지만, 더 큰 규모 데이터(30,000+ 시간)에서의 스케일링 거동 검증 부족
- depth 정보의 선택적 활용에 대한 상세한 공간 추론 개선 메커니즘 분석 필요
- 후속 연구로 더 도전적인 조작 작업, 단일 팔 로봇 및 이족 로봇 등 다양한 로봇 형태로의 확장, 그리고 few-shot 적응 능력 강화 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: LingBot-VLA는 실제 로봇 학습의 스케일링 거동을 최초로 실증하고 대규모 다양한 데이터와 효율적 훈련 인프라를 통해 실용적이고 일반화 가능한 VLA 기초 모델을 제시하며, 오픈 소스 공개로 로봇 학습 커뮤니티에 현저한 기여를 한다.

## Related Papers

- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — 오픈소스 VLA 모델로서 LingBot-VLA와 다른 접근 방식의 기초 모델을 제시합니다.
- 🏛 기반 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — 웹 지식을 로봇 제어에 전이하는 Vision-Language-Action 모델의 선구적 연구입니다.
- 🏛 기반 연구: [[papers/1318_Being-H05_Scaling_Human-Centric_Robot_Learning_for_Cross-Emb/review]] — Being-H0.5의 멀티플랫폼 일반화 개념을 실용적인 규모로 축소하여 효율적인 학습에 중점을 둔 pragmatic한 접근법입니다.
- 🔗 후속 연구: [[papers/1495_NORA_A_Small_Open-Sourced_Generalist_Vision_Language_Action/review]] — NORA의 소규모 오픈소스 VLA 모델 개념을 실제 20,000시간 데이터로 학습한 더 실용적인 기초 모델로 발전시킨 연구입니다.
