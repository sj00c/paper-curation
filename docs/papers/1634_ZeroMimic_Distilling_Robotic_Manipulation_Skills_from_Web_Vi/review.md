---
title: "1634_ZeroMimic_Distilling_Robotic_Manipulation_Skills_from_Web_Vi"
authors:
  - "Junyao Shi"
  - "Zhuolun Zhao"
  - "Tianyou Wang"
  - "Ian Pedroza"
  - "Amy Luo"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "ZeroMimic은 EpicKitchens 데이터셋의 일반 인간 비디오로부터 로봇 조작 스킬을 직접 추출하여, 로봇별 데모나 탐색 없이 즉시 배포 가능한 이미지 목표 조건부 스킬 정책을 생성하는 첫 번째 시스템이다."
tags:
  - "cat/Foundation_Models_for_Robotics"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Multi-Task_Language_Benchmarks"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Shi et al._2025_ZeroMimic Distilling Robotic Manipulation Skills from Web Videos.pdf"
---

# ZeroMimic: Distilling Robotic Manipulation Skills from Web Videos

> **저자**: Junyao Shi, Zhuolun Zhao, Tianyou Wang, Ian Pedroza, Amy Luo, Jie Wang, Jason Ma, Dinesh Jayaraman | **날짜**: 2025-03-31 | **URL**: [https://arxiv.org/abs/2503.23877](https://arxiv.org/abs/2503.23877)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: ZeroMimic distills robotic manipulation skills from egocentric web videos for zero-shot deployment across divers*

ZeroMimic은 EpicKitchens 데이터셋의 일반 인간 비디오로부터 로봇 조작 스킬을 직접 추출하여, 로봇별 데모나 탐색 없이 즉시 배포 가능한 이미지 목표 조건부 스킬 정책을 생성하는 첫 번째 시스템이다.

## Motivation

- **Known**: 최근 로봇 조작 학습은 imitation learning에 크게 의존하고 있으며, 인간 비디오 데이터셋은 조작 스킬에 대한 풍부한 정보를 담고 있다. 또한 VLM, affordance 학습, 3D 비전 기술 등의 발전이 있었다.
- **Gap**: 기존 접근법들은 로봇별 데모 데이터의 의존성이 높거나, 인간 비디오로부터 직접 정책을 생성할 때 낮은 성능을 보인다. H2R을 제외한 선행 연구들은 로봇 데이터 없이 in-the-wild 비디오로부터 실용적 성능의 정책을 생성하지 못했다.
- **Why**: 로봇과 시나리오 특화 데모 수집은 확장성이 떨어지므로, 웹상의 다양한 인간 비디오로부터 스킬을 습득할 수 있다면 일반 목적 로봇 개발의 병목을 해소할 수 있다.
- **Approach**: ZeroMimic은 grasping phase(VRB를 통한 affordance 예측 + AnyGrasp를 통한 grasp 선택)와 post-grasp phase(HaMeR로 추출한 인간 손목 궤적을 3D 좌표계에 grounding하고 6D 궤적 정책 학습)로 구성된 두 단계 시스템을 제안한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Fig. 5: ZeroMimic Zero-Shot Performance Overview. ZeroMimic demonstrates strong generalization capabilities, achieving*

- **Zero-shot 성능**: 로봇별 학습 없이 실제 환경에서 71.0%, 시뮬레이션에서 73.8%의 성공률 달성
- **다중 스킬 지원**: opening, closing, pouring, pick&place, cutting, stirring 등 9가지 다른 스킬 평가
- **일반화 능력**: 데이터셋에 없는 새로운 물체에 대해 일반화하고, 다양한 로봇 embodiment에 배포 가능
- **시스템 공개**: 소프트웨어 및 정책 체크포인트 공개로 plug-and-play 재사용 가능

## How

![Figure 3](figures/fig3.webp)

*Fig. 3: ZeroMimic is composed of the grasping phase and the post-grasp phase. The grasping phase (top) leverages*

- EpicKitchens 데이터셋에서 ego-centric 인간 비디오 활용
- HaMeR를 이용한 인간 손목 궤적 추출 및 카메라 자세 재구성으로 3D grounding
- VRB(pre-trained on EpicKitchens)를 이용해 task 관련 affordance 예측
- AnyGrasp(robot 데이터 pre-trained)로 2-fingered gripper에 적합한 grasp 선택
- 추출된 인간 손목 궤적으로부터 6D end-effector 궤적 정책 학습
- 인간과 로봇의 embodiment 차이를 해결하기 위해 coarse action transfer 추상화 적용

## Originality

- In-the-wild 비디오로부터 **직접** 배포 가능한 로봇 정책을 생성하는 첫 번째 시스템으로, H2R과 달리 affordance 기반 grasping과 learned post-grasp 정책의 조합으로 더 높은 성능 달성
- 3D grounding, video activity understanding, grasp affordance 등 기존 기술들을 systematic하게 통합하여 in-the-wild 비디오의 다양성과 노이즈를 처리
- 다양한 물체, 환경, 로봇 embodiment에 대한 zero-shot 배포 가능성을 실증적으로 검증

## Limitation & Further Study

- 평가가 주로 주방 환경과 관련 작업에 제한되어 있으며, 다른 도메인으로의 일반화 미검증
- 2-fingered gripper에만 초점을 맞춰 다른 gripper 유형(예: parallel jaw, suction)에 대한 확장성 불명확
- 인간 손목 궤적 추출 시 HaMeR의 오류가 누적될 수 있으며, occlusion이나 out-of-frame 상황에서의 robust성 미평가
- post-grasp 정책의 실패 모드 분석 부재로, 어떤 task 특성에서 실패하는지 구체적 분석 부족
- 후속 연구로 다양한 embodiment(multi-fingered gripper, humanoid)에 대한 확장, 다른 도메인 비디오 활용, end-to-end 학습 가능성 탐색 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ZeroMimic은 in-the-wild 인간 비디오로부터 로봇 조작 스킬을 직접 추출하는 실질적이고 확장 가능한 접근법을 제시하며, 71%대의 현실적 성공률로 실용성을 입증한다. 로봇 학습의 데이터 병목을 해소하는 중요한 진전이지만, 평가 범위 확대와 실패 분석 강화가 향후 과제이다.

## Related Papers

- 🔄 다른 접근: [[papers/1515_Phantom_Training_Robots_Without_Robots_Using_Only_Human_Vide/review]] — Phantom과 함께 인간 비디오만으로 로봇을 훈련하는 접근법이지만, ZeroMimic은 일반 웹 비디오에서 직접 스킬을 추출하는 점이 다르다
- 🏛 기반 연구: [[papers/1425_Human2Robot_Learning_Robot_Actions_from_Paired_Human-Robot_V/review]] — Human2Robot의 인간-로봇 행동 매핑 방법론이 ZeroMimic의 인간 비디오에서 로봇 스킬 추출 과정의 기반 기술을 제공한다
- 🏛 기반 연구: [[papers/1476_MimicPlay_Long-Horizon_Imitation_Learning_by_Watching_Human/review]] — MimicPlay의 인간 비디오로부터 장기 모방 학습 방법론이 ZeroMimic의 웹 비디오 기반 스킬 학습에 이론적 기반을 제공한다
- 🏛 기반 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — 대규모 비디오 생성형 사전훈련 기술이 ZeroMimic의 웹 비디오 데이터 활용과 스킬 추출에 핵심적인 기반 기술을 제공한다
- 🔄 다른 접근: [[papers/1601_UniSkill_Imitating_Human_Videos_via_Cross-Embodiment_Skill_R/review]] — ZeroMimic은 UniSkill과 유사한 웹 비디오에서 로봇 조작 스킬을 추출하는 또 다른 접근법을 제시한다.
