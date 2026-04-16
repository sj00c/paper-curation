---
title: "1347_D2E_Scaling_Vision-Action_Pretraining_on_Desktop_Data_for_Tr"
authors:
  - "Suhwan Choi"
  - "Jaeyoon Jung"
  - "Haebin Seong"
  - "Minchan Kim"
  - "Minyeong Kim"
date: "2025.10"
doi: ""
arxiv: ""
score: 4.0
essence: "D2E는 데스크톱 환경(게임 등)에서 수집한 대규모 비전-액션 데이터를 사전학습 자료로 사용하여 로봇 조작 및 네비게이션 같은 구체화된 AI 작업으로 전이 학습하는 프레임워크를 제시한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Choi et al._2025_D2E Scaling Vision-Action Pretraining on Desktop Data for Transfer to Embodied AI.pdf"
---

# D2E: Scaling Vision-Action Pretraining on Desktop Data for Transfer to Embodied AI

> **저자**: Suhwan Choi, Jaeyoon Jung, Haebin Seong, Minchan Kim, Minyeong Kim, Yongjun Cho, Yoonshik Kim, Yubeen Park, Youngjae Yu, Yunsung Lee | **날짜**: 2025-10-07 | **URL**: [https://arxiv.org/abs/2510.05684](https://arxiv.org/abs/2510.05684)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of D2E framework. (1) The OWA Toolkit captures 335.6 hours of rich desktop demon-*

D2E는 데스크톱 환경(게임 등)에서 수집한 대규모 비전-액션 데이터를 사전학습 자료로 사용하여 로봇 조작 및 네비게이션 같은 구체화된 AI 작업으로 전이 학습하는 프레임워크를 제시한다.

## Motivation

- **Known**: LLM은 인터넷 규모의 텍스트 데이터로 학습되어 강한 성능을 보이고 있으나, 구체화된 AI(embodied AI)는 물리적 궤적 수집의 높은 비용으로 인해 데이터 규모의 한계를 겪고 있다. VPT나 SIMA 같은 선행 연구들이 데스크톱 상호작용의 가능성을 보였으나 도메인 특정적이거나 데이터가 비공개였다.
- **Gap**: 데스크톱 데이터가 로봇 작업으로 실질적으로 전이될 수 있음을 입증하는 완전한 파이프라인과 공개 자료가 부재했으며, 다중 게임에 걸친 일반화 가능한 역동역학 모델(generalist IDM)도 없었다.
- **Why**: 데스크톱 환경은 물리 로봇 데이터보다 저비용으로 수십억 시간의 대규모 데이터를 수집할 수 있으며, 감각 운동 원시 패턴이 실제 로봇 작업으로 전이될 수 있음을 보이면 구체화 AI의 데이터 확장성 문제를 획기적으로 해결할 수 있다.
- **Approach**: 데스크톱 데이터 수집을 위한 OWA Toolkit, 다중 게임 일반화를 위한 timestamp 기반 NEP-τ를 사용하는 Generalist-IDM, 그리고 데스크톱 표현을 로봇 작업으로 전이하는 VAPT 세 가지 핵심 요소로 구성된 통합 파이프라임을 제안한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1: Overview of D2E framework. (1) The OWA Toolkit captures 335.6 hours of rich desktop demon-*

- **OWA Toolkit**: 31개 게임에서 335시간의 동기화된 멀티모달 데이터(화면, 키보드, 마우스)를 수집하고, OWAMcap 형식으로 152배 압축을 달성하여 기존 형식 대비 효율성을 대폭 향상.
- **Generalist-IDM**: timestamp 기반 이벤트 예측(NEP-τ)으로 미학습 게임에 강한 영점 사격 일반화를 달성하여 1,000시간 이상의 YouTube 게임플레이 영상의 자동 의사 레이블링 가능.
- **VAPT 기초 모델**: 1.3K시간의 데스크톱 데이터로 사전학습된 10억 매개변수 모델이 LIBERO 조작 96.6% 성공률, CANVAS 네비게이션 83.3% 성공률을 달성하여 3.3B, 7B 모델을 능가.

## How

![Figure 2](figures/fig2.webp)

*Figure 2: OWA Toolkit’s recording and storage architecture. (Left) ocap recorder captures perfectly*

- **OWA Toolkit의 ocap 레코더**: Windows API와 GStreamer 기반으로 화면(60 Hz FHD/QHD), 키보드, 마우스 이벤트를 나노초 정밀도로 동기화하여 멀티모달 스트림 기록
- **OWAMcap 포맷**: MCAP 표준 컨테이너에 H.265 코덱 기반 비디오(217배 압축), PNG/JPEG 스크린샷, 메타데이터를 통합하여 저장소 효율성 극대화
- **Generalist-IDM의 NEP-τ 아키텍처**: 고정된 tick 기반 예측 대신 다음 이벤트와 그 발생 timestamp를 함께 예측하여 sparse 이벤트 환경에서 효율적인 in-context 적응(예: 마우스 스케일 보정) 가능
- **VAPT 전이 학습**: OWA 수집 데이터(259시간 인간 데모)와 Generalist-IDM 의사 레이블(1,000시간+)을 결합하여 vision-action 사전학습을 수행한 후 LIBERO, CANVAS 벤치마크에 미세조정

## Originality

- **첫 완전한 파이프라인**: 데스크톱 데이터 수집(OWA)부터 인터넷 규모 의사 레이블링(Generalist-IDM), 로봇 전이(VAPT)까지 전체 프로세스를 공개 자료로 제시한 최초의 연구.
- **Generalist-IDM의 혁신**: 기존의 domain-specific Specialist IDM(VPT 스타일)을 넘어 다중 게임 범주에서 작동하는 일반화된 역동역학 모델을 도입하고, timestamp 기반 NEP-τ로 sparse 이벤트 예측 효율화.
- **데이터 압축 및 스토리지 최적화**: 기존 포맷 대비 152배 압축과 TorchCodec 대비 41배 낮은 디스크 읽기 속도를 달성하여 대규모 데이터 처리의 실질적 병목 해결.
- **데스크톱-로봇 전이 검증**: 데스크톱 상호작용의 감각 운동 원시 패턴이 물리 로봇 조작, 네비게이션으로 직접 전이 가능함을 벤치마크로 최초 실증.

## Limitation & Further Study

- **게임 다양성 제한**: 31개 게임은 여전히 전체 데스크톱 애플리케이션 공간의 극히 작은 부분이며, 제시된 게임들이 특정 장르(액션/전략)에 편향될 가능성.
- **Generalist-IDM의 의사 레이블 품질**: YouTube 데이터의 자동 레이블링이 human-annotated 데이터보다 노이즈가 많을 수 있으며, 이것이 최종 모델 성능에 미치는 정확한 영향 분석 부족.
- **로봇 전이의 제한된 도메인**: LIBERO와 CANVAS만으로 전이 성능을 검증했으며, 다른 유형의 로봇 작업(manipulation 외 작업) 또는 실제 로봇 하드웨어 다양성에 대한 검증 필요.
- **컴퓨트 비용 분석 부재**: Generalist-IDM 학습에 192 H100-hours(약 $800)가 소요된다고 언급했으나, 전체 D2E 파이프라인의 학습 비용과 산업 적용 가능성에 대한 상세 분석 부족.
- **후속 연구 방향**: (1) 웹 스케일 데스크톱 데이터로의 확장, (2) 다양한 로봇 형태 및 환경으로의 전이 성능 검증, (3) human-in-the-loop 의사 레이블링 품질 개선 전략.

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: D2E는 데스크톱 환경을 구체화 AI의 실질적 사전학습 자료로 확립하는 종합 프레임워크를 제시하며, 공개 자료와 효율적 도구(OWA, Generalist-IDM, VAPT)를 통해 재현성과 실용성을 담보한다. 데이터 수집 비용 대비 로봇 성능의 우수한 달성은 AI 구체화 연구의 확장성 문제에 획기적 해결책을 제공한다.

## Related Papers

- 🔗 후속 연구: [[papers/1632_World_Simulation_with_Video_Foundation_Models_for_Physical_A/review]] — Video Foundation Models의 물리적 세계 시뮬레이션 능력이 D2E의 데스크톱-로봇 전이 학습에 중요한 표현 기반을 제공합니다.
- 🏛 기반 연구: [[papers/1602_Unleashing_Large-Scale_Video_Generative_Pre-training_for_Vis/review]] — 대규모 비디오 생성 사전학습의 표현 학습이 D2E의 vision-action 사전학습 방법론의 이론적 토대가 됩니다.
- 🔄 다른 접근: [[papers/1448_Latent_Action_Pretraining_from_Videos/review]] — 둘 다 비디오에서 action 학습을 다루지만 D2E는 데스크톱 데이터를, Latent Action Pretraining은 일반 비디오를 활용합니다.
- 🔗 후속 연구: [[papers/1348_Data_Scaling_Laws_in_Imitation_Learning_for_Robotic_Manipula/review]] — 로봇 조작 모방 학습의 데이터 스케일링 법칙을 D2E의 대규모 사전훈련으로 확장할 수 있습니다.
- 🔄 다른 접근: [[papers/1515_Phantom_Training_Robots_Without_Robots_Using_Only_Human_Vide/review]] — 인간 비디오만을 사용한 로봇 훈련과 데스크톱 환경 전이 학습이 다른 데이터 활용 접근법을 제시합니다.
- 🔄 다른 접근: [[papers/1355_DreamDojo_A_Generalist_Robot_World_Model_from_Large-Scale_Hu/review]] — 대규모 비전-액션 데이터를 데스크톱 환경과 인간 동영상에서 각각 수집하는 서로 다른 접근법입니다.
- 🔗 후속 연구: [[papers/1347_D2E_Scaling_Vision-Action_Pretraining_on_Desktop_Data_for_Tr/review]] — 게임 환경에서 로봇 작업으로의 전이학습을 위한 구체적 방법론을 제시합니다.
- 🔄 다른 접근: [[papers/1400_GAIA-1_A_Generative_World_Model_for_Autonomous_Driving/review]] — 게임과 자율주행이라는 서로 다른 시뮬레이션 환경에서 실세계로의 전이학습 접근을 비교할 수 있습니다.
