---
title: "1565_Scaling_Robot_Learning_with_Semantically_Imagined_Experience"
authors:
  - "Tianhe Yu"
  - "Ted Xiao"
  - "Austin Stone"
  - "Jonathan Tompson"
  - "Anthony Brohan"
date: "2023.02"
doi: ""
arxiv: ""
score: 4.0
essence: "ROSIE는 text-to-image diffusion 모델을 이용한 inpainting을 통해 기존 로봇 조작 데이터를 의미론적으로 증강하여, 새로운 물체와 환경에 대한 로봇의 일반화 능력을 향상시키는 방법을 제안한다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Yu et al._2023_Scaling Robot Learning with Semantically Imagined Experience.pdf"
---

# Scaling Robot Learning with Semantically Imagined Experience

> **저자**: Tianhe Yu, Ted Xiao, Austin Stone, Jonathan Tompson, Anthony Brohan, Su Wang, Jaspiar Singh, Clayton Tan, Dee M, Jodilyn Peralta, Brian Ichter, Karol Hausman, Fei Xia | **날짜**: 2023-02-22 | **URL**: [https://arxiv.org/abs/2302.11550](https://arxiv.org/abs/2302.11550)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: We propose using text-guided diffusion models for data augmentation within the sphere*

ROSIE는 text-to-image diffusion 모델을 이용한 inpainting을 통해 기존 로봇 조작 데이터를 의미론적으로 증강하여, 새로운 물체와 환경에 대한 로봇의 일반화 능력을 향상시키는 방법을 제안한다.

## Motivation

- **Known**: 로봇 학습의 성능 향상은 대규모 다양한 데이터에 의존하지만, 실제 로봇 데이터 수집은 인적 개입이나 복잡한 자동화 체계를 필요로 하므로 확장이 어렵다. 최근 DALL-E 2, Imagen, StableDiffusion 같은 text-to-image diffusion 모델들이 고품질의 합성 이미지 생성을 가능하게 했다.
- **Gap**: 기존 도메인 랜덤화나 시뮬레이션 기반 데이터 증강 방식은 로봇 작업의 의미론적 다양성을 충분히 제공하지 못한다. Internet-scale 학습된 생성 모델의 지식을 로봇 데이터 증강에 직접 적용하는 체계적 접근이 부재하다.
- **Why**: 로봇이 새로운 물체와 변화된 환경에서도 안정적으로 작동하도록 하려면 의미론적으로 다양한 학습 데이터가 필수적이다. Diffusion 모델 기반 증강은 실제 로봇 데이터 수집 비용을 크게 줄이면서도 의미론적 다양성을 제공할 수 있다.
- **Approach**: ROSIE는 자연어 지시문을 파싱하여 증강할 영상 영역을 자동으로 선정한 후, text-guided diffusion 모델의 inpainting 기능으로 해당 영역의 물체, 배경, 방해물을 의미론적으로 교체한다. 이를 통해 기존 RT-1 아키텍처를 이용한 정책 학습에 새로운 작업과 환경 변화에 대한 강건성을 부여한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Figure 4: Augmentations of in-hand objects during manipulation. We show examples where ROSIE*

- **새로운 물체 일반화**: Diffusion 모델로 증강된 데이터로 학습한 정책이 실제 로봇이 상호작용한 적 없는 완전히 새로운 물체를 조작하는 작업을 수행할 수 있음을 실증했다.
- **배경 및 방해물 강건성**: 의미론적 배경 변화와 새로운 방해물이 포함된 증강 데이터로 학습하여 분포 외(OOD) 시나리오에서의 강건성을 향상시켰다.
- **고수준 작업 개선**: Success detection 같은 고차원 로봇 학습 작업의 일반화 능력을 diffusion 기반 증강을 통해 향상시켰다.
- **자동화된 파이프라인**: 수동 마스킹이나 메시 정보 없이 텍스트 지시문만으로 자동으로 증강 영역을 선정하고 생성하는 완전 자동화 시스템을 구현했다.

## How

![Figure 2](figures/fig2.webp)

*Figure 2: The proposed architecture of ROSIE. First, we localize the augmentation region with open*

- 자연어 지시문에서 증강 대상(물체, 배경, 방해물)을 자동으로 파싱하여 식별
- 식별된 영역에 대해 diffusion 모델의 inpainting 기능을 적용하되, 로봇의 그리퍼 위치 등 의미론적으로 중요한 부분은 보존
- Text 프롬프트를 통해 diffusion 모델을 제어하여 원하는 의미론적 변화(예: 색상, 물체 종류, 배경) 유도
- 기존 RT-1 behavioral cloning 정책 학습에 augmented 데이터를 포함시켜 학습 및 평가
- 실제 로봇 환경에서 새로운 물체, 배경, 방해물에 대한 정책의 일반화 성능 검증

## Originality

- Internet-scale 학습된 text-to-image diffusion 모델을 로봇 데이터 증강에 처음으로 체계적으로 적용한 것으로, 기존 도메인 랜덤화나 시뮬레이션 기반 접근과 구분된다.
- Text 프롬프트 기반 자동 증강 영역 선정과 의미론적 보존을 결합하여, 수동 마스킹 없는 완전 자동화된 파이프라인을 구현했다.
- 기존 concurrent 작업(CACTI, GenAug)과 달리 깊이 정보나 메시 정보를 요구하지 않으면서도 의미론적 다양성을 달성했다.
- 로봇 조작뿐 아니라 success detection 같은 고수준 인식 작업의 강건성 향상도 시연했다.

## Limitation & Further Study

- **Diffusion 모델의 의미론적 편향**: Internet-scale 데이터로 학습된 생성 모델이 특정 물체나 장면에 대해 가진 고정된 표현이 로봇 학습의 다양성을 제한할 수 있다.
- **물리적 현실성 검증 부족**: 생성된 이미지가 시각적으로 그럴듯하더라도, 로봇 조작 시 물리적으로 불가능한 배치가 포함될 수 있으며, 이에 대한 체계적 필터링 메커니즘이 제시되지 않음.
- **인페인팅 정확도 의존성**: Text 프롬프트 해석과 증강 영역 선정의 정확성이 전체 성능에 크게 영향을 미치지만, 오류 케이스에 대한 분석이 제한적이다.
- **확장성 미검증**: 현재 RT-1 기반 실험에만 한정되어 있으며, 다양한 로봇 플랫폼이나 더 복잡한 multi-step 작업으로의 확장성이 확인되지 않았다.
- **후속 연구 방향**: (1) 물리 시뮬레이터를 이용한 생성 이미지의 현실성 검증, (2) 3D 장면 이해를 통한 더 정교한 의미론적 증강, (3) 로봇 피드백을 반영하는 적응형 증강 파이프라인 개발

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: ROSIE는 최신 text-to-image diffusion 모델을 로봇 학습에 창의적으로 적용하여 고비용의 실제 데이터 수집 없이 의미론적으로 다양한 학습 데이터를 생성하는 실용적인 방법을 제시했다. 광범위한 실험을 통해 새로운 물체 일반화, 배경/방해물 강건성, 고수준 작업 향상을 입증했으며, 로봇 학습 커뮤니티에 높은 영향을 미칠 가능성이 있다.

## Related Papers

- 🏛 기반 연구: [[papers/1407_Genie_Generative_Interactive_Environments/review]] — Genie의 생성형 인터랙티브 환경 개념이 ROSIE의 diffusion 모델을 이용한 로봇 데이터 의미론적 증강의 기초가 된다.
- 🔄 다른 접근: [[papers/1540_RoboGen_Towards_Unleashing_Infinite_Data_for_Automated_Robot/review]] — RoboGen이 완전히 새로운 데이터 생성에 중점을 두는 반면, ROSIE는 기존 데이터의 의미론적 변형을 통한 증강에 초점을 맞춘다.
- 🔗 후속 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — Unleashing Large-Scale Video Generation의 비디오 생성 기술을 로봇 조작 데이터의 의미론적 증강으로 특화하여 적용했다.
- 🏛 기반 연구: [[papers/1534_RoboAgent_Generalization_and_Efficiency_in_Robot_Manipulatio/review]] — 의미적으로 상상된 경험을 통한 로봇 학습 확장 기법이 RoboAgent의 semantic augmentation 방법론의 이론적 기초가 된다.
- 🔄 다른 접근: [[papers/1543_RoboPoint_A_Vision-Language_Model_for_Spatial_Affordance_Pre/review]] — ROSIE가 기존 데이터의 의미론적 증강에 중점을 두는 반면, RoboPoint는 완전히 합성된 데이터로부터 spatial affordance를 학습한다.
