# Embracing Bulky Objects with Humanoid Robots: Whole-Body Manipulation with Reinforcement Learning

> **저자**: Chunxin Zheng, Kai Chen, Zhihai Bi, Yulin Li, Liang Pan, Jinni Zhou, Haoang Li, Jun Ma | **날짜**: 2025-09-16 | **DOI**: [10.48550/arXiv.2509.13534](https://doi.org/10.48550/arXiv.2509.13534)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1.*

본 논문은 인간의 동작 사전(human motion prior)과 neural signed distance field(NSDF)를 통합한 강화학습 프레임워크를 제안하여 휴머노이드 로봇이 팔과 몸통을 조율해 부피가 큰 물체를 전신으로 포용하고 운반할 수 있도록 하는 방법을 제시한다.

## Motivation

- **Known**: 휴머노이드 로봇의 전신 조작(WBM)은 다중 접촉 전략을 통해 부피가 큰 물체를 안정적으로 조작할 수 있으며, 강화학습과 행동 복제(behavior cloning)는 인간 모션 데이터를 활용해 자연스러운 로봇 제어를 가능하게 한다.
- **Gap**: 기존의 모델 기반 WBM 방법은 계산 비용이 높고 정확한 기하학적 인지에 실패하며, 학습 기반 방법들은 신중하게 설계된 보상에 의존하면서도 접촉이 많고 동적으로 불안정한 시나리오에서 강건한 행동을 생성하지 못한다.
- **Why**: 부피가 큰 물체의 전신 포용 작업은 오랜 지평선의 조율된 동작을 요구하며, 이를 성공적으로 수행하는 것은 산업 응용 및 가정 서비스 로봇의 배치에 필수적이다.
- **Approach**: Teacher-student 아키텍처를 통해 대규모 인간 모션 데이터(AMASS)에서 생물학적으로 타당한 운동학적 분포를 추출하고, NSDF를 이용해 정확한 기하학적 인지와 접촉 인식을 제공하며, 이 두 요소를 RL 정책 학습에 통합한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Fig. 1.*

- **첫 휴머노이드 WBM RL 프레임워크**: 휴머노이드 로봇이 팔과 몸통을 동시에 활용해 물체를 포용하는 최초의 강화학습 프레임워크 제안
- **수렴성 향상**: 인간 모션 사전을 도입해 다중 접촉 및 장기 지평선 작업에서 정책 학습의 수렴 속도를 가속화하고 인간형(anthropomorphic) 기술 습득 촉진
- **강건한 접촉 인지**: NSDF 표현으로 로봇-물체 상호작용을 정밀하게 인지하여 관찰 공간과 보상 함수 설계에 활용, 장시간 접촉 유지 강화
- **높은 적응성 및 현실 이전**: 다양한 형태와 크기의 물체에 우수한 적응성을 보이며 시뮬레이션에서 현실로의 전이(sim-to-real transfer) 성공 입증

## How

![Figure 2](figures/fig2.webp)

*Fig. 2.*

- AMASS 모션 캡처 데이터셋에서 시작하여 MaskedMimic을 사용해 운동학적 제약 위반(자기 충돌, 발 미끄러짐) 시퀀스 제거
- 필터링된 모션을 로봇 형태로 재표적화(retarget)하여 로봇 참조 궤적 수집
- Teacher-student 증류 아키텍처로 행동 복제 정책을 통해 모션 사전 학습
- Neural signed distance field 구성으로 로봇 신체의 정확한 기하학적 표현 생성
- 모션 사전과 NSDF 기반 관찰 및 보상을 활용한 RL 정책 학습
- 시뮬레이션 환경에서 정책 학습 후 실제 휴머노이드 로봇에 배포 및 검증

## Originality

- 휴머노이드 로봇의 전신 포용 조작을 위한 최초의 RL 프레임워크 제시
- 인간 모션 사전을 RL 정책에 통합하여 학습 안정성과 수렴성을 동시에 향상시키는 novel한 접근
- NSDF를 자기 모델링(self-modeling) 및 접촉 인식 향상에 직접 활용한 방법론 혁신
- Teacher-student 구조를 통한 모션 사전 추출로 기존 BC 기반 접근의 한계(환경 정보 부족) 극복

## Limitation & Further Study

- 논문에서는 특정 휴머노이드 로봇 플랫폼(구체적 명시 필요)에 대해서만 검증되어 다른 플랫폼으로의 일반화 가능성 불명확
- NSDF 계산 오버헤드 및 실시간 성능에 대한 상세 분석 부족
- 장시간 운반 작업에 대한 에너지 효율성 및 안정성 평가 미흡
- 다양한 환경(불균등한 바닥, 장애물이 많은 공간) 조건에서의 강건성 평가 필요
- 후속 연구로 다중 로봇 협력 전신 조작, 더욱 복잡한 기하학적 물체 처리, 동적 환경에서의 적응 능력 개선 기대

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 휴머노이드 로봇의 전신 물체 포용 조작을 위한 최초의 RL 프레임워크를 제시하며, 인간 모션 사전과 NSDF의 통합을 통해 학습 효율성과 접촉 강건성을 동시에 달성한 혁신적인 연구다. 시뮬레이션과 실제 로봇 실험을 통한 검증이 충분하고 실용적 가치가 높다.
