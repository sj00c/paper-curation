# UniDex: A Robot Foundation Suite for Universal Dexterous Hand Control from Egocentric Human Videos

> **저자**: Gu Zhang, Qicheng Xu, Haozhe Zhang, Jianhan Ma, Long He, Yiming Bao, Zeyu Ping, Zhecheng Yuan, Chenhao Lu, Chengbo Yuan, Tianhai Liang, Xiaoyu Tian, Maanping Shao, Feihong Zhang, Mingyu Ding, Yang Gao, Hao Zhao, Hang Zhao, Huazhe Xu | **날짜**: 2026-03-23 | **URL**: [https://arxiv.org/abs/2603.22264](https://arxiv.org/abs/2603.22264)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1. We introduce UniDex, a robot foundation suite for heterogeneous dexterous hand embodiments. We first curate Un*

인간 자기중심 비디오에서 50K+ 궤적을 수집한 UniDex-Dataset과 Function–Actuator–Aligned Space (FAAS) 통합 액션 공간을 활용하여 8종 로봇 핸드에 대한 범용 손재주 제어가 가능한 VLA 파운데이션 모델을 제시한다.

## Motivation

- **Known**: Gripper 중심의 로봇 파운데이션 모델들이 대규모 데이터셋으로 학습되고 있으며, 인간 비디오에서 로봇 데이터로의 변환 기술들이 존재한다. 그러나 손재주 조작(dexterous manipulation) 분야는 데이터 부족, 손 형태의 이질성, 높은 차원의 제어 문제를 겪고 있다.
- **Gap**: 손재주 로봇 핸드의 대규모 통합 데이터셋이 부재하고, 서로 다른 DoF와 형태를 가진 여러 손들 간의 효과적인 skill transfer를 위한 통합 액션 공간이 없으며, 로봇 원격조작 데이터 수집의 높은 비용을 해결할 방안이 제시되지 않았다.
- **Why**: 손재주 조작은 일상의 도구 사용 작업에 필수적이며, 파운데이션 모델의 확보는 손재주 로봇의 실용화와 다양한 응용 분야 확대를 가능하게 한다. 이는 현재 gripper 중심의 기술을 넘어 더 복잡한 조작 능력을 요구하는 실제 작업 해결의 열쇠다.
- **Approach**: 인간 자기중심 비디오를 human-in-the-loop retargeting으로 로봇 궤적으로 변환하여 UniDex-Dataset을 구축하고, 기능적으로 유사한 액추에이터를 공유 좌표로 매핑하는 FAAS를 정의하며, 이를 기반으로 3D pointcloud 입력을 사용하는 UniDex-VLA를 학습한다. 추가로 portable한 UniDex-Cap 캡처 장치를 통해 인간-로봇 co-training을 가능하게 한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1. We introduce UniDex, a robot foundation suite for heterogeneous dexterous hand embodiments. We first curate Un*

- **UniDex-Dataset**: 8종 로봇 핸드(6-24 DoFs)에 걸친 50K+ 궤적과 9M paired image-pointcloud-action 프레임으로 구성된 최초의 대규모 통합 손재주 데이터셋 구축
- **FAAS & UniDex-VLA**: 함수 중심의 통합 액션 공간 설계 및 이를 활용한 3D VLA 모델로 도구 사용 작업에서 81% 평균 진행률(task progress) 달성, π0 모델 대비 2배 이상 성능 우위
- **Generalization 능력**: spatial, object, zero-shot cross-hand generalization 모두에서 강력한 성능 입증
- **Human-Robot Co-training**: UniDex-Cap을 통해 변환된 인간 데이터가 로봇 원격조작 데이터를 부분적으로 대체 가능함을 정량적으로 입증

## How

![Figure 2](figures/fig2.webp)

*Figure 2. The figure illustrates the complete human–robot trans-*

- Egocentric RGB-D human manipulation 비디오를 시작점으로 하되, fingertip 기반 inverse kinematics와 interactive adjustment를 결합한 human-in-the-loop retargeting으로 인간 궤적을 로봇 실행 가능한 궤적으로 변환
- 변환 과정에서 human hand를 visual stream에서 마스킹하고 retargeted robot hand를 scene pointcloud에 삽입하여 시각적 도메인 갭 축소
- Function–Actuator–Aligned Space (FAAS) 정의: 기능적으로 유사한 액추에이터들(예: 각 손의 검지손가락)을 공유 좌표계로 매핑하여 cross-hand transfer 가능성 확보
- 3D VLA 모델 아키텍처: single-view color + pointcloud 입력을 처리하는 encoder, language instruction을 처리하는 component, FAAS 기반 action space로의 decoder로 구성
- Two-stage learning: UniDex-Dataset에서 대규모 pretraining 후 task-specific demonstration으로 fine-tuning
- UniDex-Cap: 동기화된 RGB-D 스트림과 human hand pose 기록 → 동일 변환 파이프라인으로 로봇 궤적 생성하여 co-training 데이터 수집

## Originality

- **최초의 대규모 통합 손재주 데이터셋**: 8종 이질적인 로봇 핸드를 아우르는 50K+ 궤적 규모의 dataset은 이 분야에서 전례 없음
- **Function-centric unified action space (FAAS)**: 기존 left-aligned나 latent action space와 달리 기능적 유사성을 기준으로 액추에이터를 통합하는 혁신적 설계로 post-processing 불필요
- **Human-in-the-loop retargeting의 체계적 적용**: 단순 자동화가 아닌 human-in-the-loop 접근으로 kinematic gap을 효과적으로 폐쇄하고, visual masking으로 domain gap 완화
- **Practical human-robot co-training pipeline**: UniDex-Cap이라는 portable 캡처 장치를 통해 인간 비디오의 경제성과 로봇 실행성을 동시에 확보

## Limitation & Further Study

- **Retargeting 절차의 수작업 의존성**: human-in-the-loop retargeting이 필요하여 완전 자동화가 아니며, 이는 대규모 확장 시 병목이 될 가능성
- **평가 대상의 제한성**: 5개 도구 사용 작업과 2종 로봇 핸드에만 실평가했으며, 더 다양한 작업 유형(재배치, 조작 등)에 대한 검증 부재
- **Sim-to-real gap 미분석**: 실제 robustness와 장기간 운영 안정성에 대한 논의 부족, 실패 케이스 분석 미흡
- **FAAS의 일반성**: 아직 새로운 손 형태에 FAAS를 적용하는 protocol이 명확하지 않으며, 매우 이질적인 형태의 손에 대한 transfer 가능성 미검증
- **후속 연구 방향**: (1) Retargeting 과정의 자동화 수준 향상, (2) 더 많은 도구 및 일상 작업으로의 확대, (3) Real-world deployment 시 안정성 강화, (4) FAAS의 이론적 기반 및 일반화 가능성 분석

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: UniDex는 손재주 로봇 조작 분야의 파운데이션 모델 구축을 위해 필요한 대규모 통합 데이터셋, 혁신적 액션 공간, 실용적 co-training 파이프라인을 체계적으로 제시한 종합적 연구로, 높은 실제 성능과 함께 cross-hand generalization 능력을 입증하여 이 분야의 실질적 발전을 견인할 것으로 기대된다.
