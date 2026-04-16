---
title: "1410_GR-3_Technical_Report"
authors:
  - "Chilam Cheang"
  - "Sijin Chen"
  - "Zhongren Cui"
  - "Yingdong Hu"
  - "Liqun Huang"
date: "2025.07"
doi: ""
arxiv: ""
score: 4.0
essence: "GR-3는 vision-language-action (VLA) 모델로, 웹 규모 vision-language 데이터와 로봇 궤적 데이터의 co-training을 통해 일반화 능력, 효율적 미세조정, 장기 지평 작업 수행 능력을 갖춘 범용 로봇 정책을 구현한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Semantic_Task_Generalization"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Cheang et al._2025_GR-3 Technical Report.pdf"
---

# GR-3 Technical Report

> **저자**: Chilam Cheang, Sijin Chen, Zhongren Cui, Yingdong Hu, Liqun Huang, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Xiao Ma, Hao Niu, Wenxuan Ou, Wanli Peng, Zeyu Ren, Haixin Shi, Jiawen Tian, Hongtao Wu, Xin Xiao, Yuyang Xiao, Jiafeng Xu, Yichu Yang | **날짜**: 2025-07-21 | **URL**: [https://arxiv.org/abs/2507.15493](https://arxiv.org/abs/2507.15493)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 Overview. GR-3 is able to learn from three types of data: vision-language data, robot trajectory data,*

GR-3는 vision-language-action (VLA) 모델로, 웹 규모 vision-language 데이터와 로봇 궤적 데이터의 co-training을 통해 일반화 능력, 효율적 미세조정, 장기 지평 작업 수행 능력을 갖춘 범용 로봇 정책을 구현한다.

## Motivation

- **Known**: Vision-language-action 모델은 사전학습된 VLM을 기반으로 자연언어 지시사항을 따르는 로봇 정책을 학습할 수 있다. 그러나 기존 VLA 모델은 미학습 개념 이해, 효율적 적응, 장기 작업의 견고성 측면에서 제한이 있다.
- **Gap**: 기존 VLA 모델은 로봇 궤적 데이터에 없는 추상적 개념을 이해하지 못하며, 새로운 환경 적응에 많은 데이터가 필요하고, 장기 지평 및 정교한 작업에서 누적 오류로 인한 견고성 문제를 겪는다.
- **Why**: 범용 로봇이 일상생활에서 인간을 보조하려면 다양한 객체, 환경, 추상 개념의 지시사항을 이해하고 적응해야 하며, 복잡한 조작 작업을 안정적으로 수행해야 한다.
- **Approach**: GR-3는 flow-matching을 이용한 action 예측, web-scale vision-language 데이터와의 co-training, task status auxiliary supervision, VR 기반 인간 궤적 데이터의 효율적 미세조정을 결합하며, ByteMini 양팔 모바일 로봇 플랫폼을 통해 실제 환경에서 검증한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2 Capabilities. GR-3 strictly follows instructions and is capable of understanding unseen instructions involving*

- **일반화 능력**: 미학습 객체, 환경, 추상 개념(크기, 공간관계, 상식)을 포함한 out-of-distribution 지시사항을 정확히 따른다.
- **효율적 적응**: 객체당 단 10개의 인간 궤적으로 신규 객체에 빠르고 비용 효율적으로 적응한다.
- **장기 작업 수행**: table bussing, cloth manipulation 등 복잡한 양팔 조작과 모바일 이동이 필요한 장기 지평 작업을 높은 견고성으로 수행한다.
- **우수한 성능**: 기존 SOTA 기준 π₀를 다양한 도전적 작업에서 일관되게 초과 달성한다.

## How

![Figure 3](figures/fig3.webp)

*Figure 3 The GR-3 Model. GR-3 is co-trained on both robot trajectories and vision-language data with a flow-matching*

- Pre-trained VLM (Qwen2.5-VL-3B-Instruct)을 backbone으로 하고 action diffusion transformer를 통해 k-length action chunk를 flow-matching으로 예측
- RMSNorm을 attention/FFN 선형층 이후에 적용하여 training 안정성 및 언어 추종 능력 향상
- Robot trajectory data에서 flow-matching loss로 action을 학습하고, vision-language data에서 next-token-prediction으로 VLM backbone만 학습하는 dual objective co-training
- Task status (Ongoing/Terminated/Invalid)를 auxiliary action dimension으로 추가하고 무효 지시사항으로 random replacement하여 언어 조건 주의력 강화
- Data collection scheduler를 통해 객체 조합, 배경, 수행 동작을 체계적으로 제어하여 데이터 다양성 최대화
- VR 기반 인간 궤적 수집으로 미세조정 데이터를 효율적으로 획득
- Bi-manual mobile robot (ByteMini) 플랫폼 개발으로 양팔 조작과 모바일 이동을 통합

## Originality

- Web-scale vision-language 데이터와 robot trajectory 데이터의 명시적 co-training으로 abstract concepts 이해를 추상화하는 혁신적 접근
- Task status auxiliary supervision을 통해 language attention 문제를 직접 해결하는 설계
- Flow-matching을 action 예측에 적용하여 diffusion 기반 generation의 안정성과 유연성 확보
- Data collection scheduler를 통한 체계적이고 다양한 로봇 궤적 수집의 효율화
- VR 기반 인간 궤적을 통한 few-shot 적응이라는 실용적 미세조정 방식 제시

## Limitation & Further Study

- 4B 파라미터 모델 크기로 인한 추론 계산 복잡도에 대한 평가 부족
- Vision-language 데이터와 robot trajectory 데이터의 co-training 비율, 혼합 방식에 대한 ablation 분석 제한적
- ByteMini 로봇의 물리적 제약(payload, dexterity 한계)에 따른 작업 범위의 근본적 제한
- 오직 3가지 작업(pick-and-place, table bussing, cloth manipulation)에 대한 평가로 범용성 검증 범위 제한
- 추상 개념 이해의 정량적 평가 부족—언어 지시사항 복잡도별 성능 분석 미흡
- 후속 연구: 모델 스케일링, 더 광범위한 다중 작업 벤치마크 개발, 현실 세계 배포 시 domain shift 대응 방안

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: GR-3는 co-training, auxiliary supervision, VR 기반 효율적 적응 등 여러 혁신 기법을 종합한 실질적으로 견고한 VLA 모델로서, 장기 지평과 정교한 조작 작업에서 SOTA를 달성했으나, 평가 범위의 제한과 부분적 ablation 분석으로 인해 완전한 기여 명확화에는 다소 미흡하다.

## Related Papers

- 🔄 다른 접근: [[papers/1510_OpenVLA_An_Open-Source_Vision-Language-Action_Model/review]] — 둘 다 오픈소스 VLA 모델이지만 GR-3는 co-training에, OpenVLA는 일반화 가능성에 중점을 둔다.
- 🏛 기반 연구: [[papers/1323_BridgeData_V2_A_Dataset_for_Robot_Learning_at_Scale/review]] — 대규모 로봇 데이터셋이 GR-3의 co-training을 위한 로봇 궤적 데이터의 기반을 제공한다.
- 🔗 후속 연구: [[papers/1560_SARA-RT_Scaling_up_Robotics_Transformers_with_Self-Adaptive/review]] — self-adaptive 로봇 트랜스포머가 GR-3의 VLA 모델 구조를 더 효율적으로 확장한 형태다.
- 🏛 기반 연구: [[papers/1409_GR-2_A_Generative_Video-Language-Action_Model_with_Web-Scale/review]] — GR-3의 이전 버전인 GR-2 모델의 기초 연구입니다.
- 🔗 후속 연구: [[papers/1411_GR-RL_Going_Dexterous_and_Precise_for_Long-Horizon_Robotic_M/review]] — 일반적인 VLA 정책에서 더 나아가 정밀한 장기 조작을 위한 전문화된 정책으로 발전시킨 연구입니다.
- 🔗 후속 연구: [[papers/1409_GR-2_A_Generative_Video-Language-Action_Model_with_Web-Scale/review]] — GR-2의 generative video-language-action 모델을 더욱 발전시킨 차세대 버전입니다.
- 🏛 기반 연구: [[papers/1411_GR-RL_Going_Dexterous_and_Precise_for_Long-Horizon_Robotic_M/review]] — GR-3 VLA 모델을 기반으로 하여 전문가 정책으로 변환하는 연구입니다.
