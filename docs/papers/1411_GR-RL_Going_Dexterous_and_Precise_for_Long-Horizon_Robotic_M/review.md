---
title: "1411_GR-RL_Going_Dexterous_and_Precise_for_Long-Horizon_Robotic_M"
authors:
  - "Yunfei Li"
  - "Xiao Ma"
  - "Jiafeng Xu"
  - "Yu Cui"
  - "Zhongren Cui"
date: "2025.12"
doi: ""
arxiv: ""
score: 4.0
essence: "GR-RL은 일반적인 vision-language-action (VLA) 정책을 다단계 학습 파이프라인(데이터 필터링, 형태 대칭 증강, 온라인 RL)을 통해 장기 복잡 조작을 위한 고정밀 전문가 정책으로 변환하는 로봇 학습 프레임워크이다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Li et al._2025_GR-RL Going Dexterous and Precise for Long-Horizon Robotic Manipulation.pdf"
---

# GR-RL: Going Dexterous and Precise for Long-Horizon Robotic Manipulation

> **저자**: Yunfei Li, Xiao Ma, Jiafeng Xu, Yu Cui, Zhongren Cui, Zhigang Han, Liqun Huang, Tao Kong, Yuxiao Liu, Hao Niu, Wanli Peng, Jingchao Qiao, Zeyu Ren, Haixin Shi, Zhi Su, Jiawen Tian, Yuyang Xiao, Shenyu Zhang, Liwei Zheng, Hang Li, Yonghui Wu | **날짜**: 2025-12-01 | **URL**: [https://arxiv.org/abs/2512.01801](https://arxiv.org/abs/2512.01801)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 GR-RL performs long-horizon, dexterous, and high-precision manipulation, in the task of shoe lacing, by*

GR-RL은 일반적인 vision-language-action (VLA) 정책을 다단계 학습 파이프라인(데이터 필터링, 형태 대칭 증강, 온라인 RL)을 통해 장기 복잡 조작을 위한 고정밀 전문가 정책으로 변환하는 로봇 학습 프레임워크이다.

## Motivation

- **Known**: VLA 정책은 다양한 작업에서 뛰어난 일반화를 보였으나, 밀리미터 단위 정밀도와 장기 강건성이 필요한 복잡한 조작 작업에서는 부족하다.
- **Gap**: 기존 VLA 정책은 인간 시연의 최적성을 가정하나, 고정밀 조작에서 인간 시연은 잡음이 많고 부분최적이며, 학습과 배포 간 불일치가 존재한다.
- **Why**: 신발끈 꿰기와 같은 실제 과제는 장기 추론, 밀리미터 정밀도, 유연한 물체 상호작용을 모두 요구하여 로봇의 신뢰할 수 있는 자동화가 중요하다.
- **Approach**: GR-RL은 offline RL을 통해 학습된 task progress 함수로 부분최적 시연을 필터링하고, 양방향 로봇의 형태 대칭성을 이용한 행동 증강, 그리고 latent space noise predictor를 학습하는 온라인 RL을 결합한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5 Left: the success rate of our multi-stage training recipe. Data filtering, mirror augmentation, and online*

- **신발끈 꿰기 자동화**: 83.3% 성공률로 신발끈을 여러 개의 고리를 통해 꿰는 최초의 학습 기반 정책 달성
- **데이터 필터링 효과**: 부분최적 인간 시연을 식별하여 제거함으로써 정책 성능 향상
- **형태 대칭 증강**: 양방향 로봇의 좌우 대칭성을 활용한 데이터 증강으로 일반화 및 성공률 크게 개선
- **학습-배포 불일치 해소**: 온라인 RL을 통해 시스템 최적화와의 불일치 완화 및 고정밀 제어 성능 개선

## How

![Figure 2](figures/fig2.webp)

*Figure 2*

- Offline RL (TD3+BC)로 sparse reward를 사용하여 distributional critic 학습
- 예측된 Q-값의 평균값을 task progress ρ로 계산하여 모든 시연 전이(transition) 평가
- 양성 진행에 기여하는 전이만 유지하고 나머지는 필터링
- Binary-flip morphological symmetry augmentation으로 양방향 로봇의 좌우 관측 및 행동을 미러링하여 증강
- 온라인 RL에서 latent space noise predictor 학습으로 denoising 프로세스를 고수익 영역으로 조향
- Mixture-of-Transformer (MoT) 아키텍처로 VLA 정책과 distributional critic 동시 학습

## Originality

- Offline RL Q-값을 직접 task progress 함수로 활용한 새로운 데이터 필터링 방법론
- 양방향 로봇의 형태 대칭성을 체계적으로 활용한 행동 증강 기법
- VLA 정책의 학습-배포 불일치를 온라인 RL과 latent space noise predictor로 해결하는 접근법
- 분포적 강화학습(distributional RL)을 offline sparse reward 환경에서 robust progress evaluator로 적용

## Limitation & Further Study

- 신발 끈 꿰기 과제에 특화된 시연이 필요하며, 다른 정밀 조작 작업으로의 일반화 검증 부족
- 형태 대칭 증강은 양방향 구조를 가진 로봇에만 적용 가능하여 범용성 제한
- 온라인 RL 단계에서 실제 로봇 환경에서의 탐색 비용과 안전 문제에 대한 논의 부족
- 후속 연구에서는 다양한 조작 과제로의 확장, 단일 팔 로봇 또는 비대칭 로봇 구조에서의 적용 방법 개발이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: GR-RL은 인간 시연의 부분최적성과 학습-배포 불일치라는 실질적 문제를 체계적으로 해결하는 실용적인 다단계 파이프라인을 제시하며, 신발끈 꿰기와 같은 극도로 정밀한 조작 과제를 성공시킴으로써 로봇 기초 모델의 전문화 방향을 제시하는 중요한 기여를 한다.

## Related Papers

- 🏛 기반 연구: [[papers/1410_GR-3_Technical_Report/review]] — GR-3 VLA 모델을 기반으로 하여 전문가 정책으로 변환하는 연구입니다.
- 🔄 다른 접근: [[papers/1620_VLA-RL_Towards_Masterful_and_General_Robotic_Manipulation_wi/review]] — VLA 모델의 RL 기반 미세조정에서 다른 방법론적 접근을 제시합니다.
- 🔗 후속 연구: [[papers/1394_FLaRe_Achieving_Masterful_and_Adaptive_Robot_Policies_with_L/review]] — 대규모 사전학습된 로봇 정책을 RL로 미세조정하는 방법론을 더욱 정교한 전문가 정책으로 발전시킨 연구입니다.
- 🔗 후속 연구: [[papers/1619_VLA-RFT_Vision-Language-Action_Reinforcement_Fine-tuning_wit/review]] — long-horizon robotic task를 reinforcement fine-tuning으로 해결하는 확장 연구입니다.
- 🔗 후속 연구: [[papers/1410_GR-3_Technical_Report/review]] — 일반적인 VLA 정책에서 더 나아가 정밀한 장기 조작을 위한 전문화된 정책으로 발전시킨 연구입니다.
