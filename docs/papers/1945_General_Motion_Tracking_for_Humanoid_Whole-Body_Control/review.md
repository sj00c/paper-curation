# General Motion Tracking for Humanoid Whole-Body Control

> **저자**:  | **날짜**:  | **URL**: [https://gmt-humanoid.github.io/](https://gmt-humanoid.github.io/)

---

## Essence

![Figure 2](figures/fig2.webp)

*Fig. 2: General Motion Retargeting (GMR) Pipeline.*

인간-휴머노이드 로봇 간 신체 구조 차이(embodiment gap)를 극복하기 위해 General Motion Retargeting (GMR)을 제안하고, 재타겟팅 품질이 모션 추적 정책 성능에 미치는 영향을 체계적으로 평가한 연구이다.

## Motivation

- **Known**: 휴머노이드 모션 추적은 텔레오퍼레이션과 계층적 제어의 핵심이며, 기존 PHC나 ProtoMotions 같은 재타겟팅 방법들이 존재한다. 현재 관행은 재타겟팅 후 RL을 통해 정책을 학습하지만 광범위한 보상 공학이 필요하다.
- **Gap**: 기존 재타겟팅 방법들은 발 관통(foot penetration), 자기 교차(self-intersection), 물리적으로 불가능한 모션 같은 인공물을 남기고 있지만, 이러한 재타겟팅 품질의 영향을 보상 튜닝 없이 체계적으로 평가한 연구가 부족하다.
- **Why**: 고품질의 재타겟팅은 실제 로봇 배포 시 별도의 보상 설계나 도메인 랜덤화 없이도 안정적인 모션 추적을 가능하게 하여, 휴머노이드 로봇의 실용화와 일반화를 촉진한다.
- **Approach**: 비균등 국소 스케일링(non-uniform local scaling)과 2단계 최적화를 결합한 GMR을 제안하며, BeyondMimic을 사용하여 재타겟팅 방법들을 공정하게 비교하고, LAFAN1 데이터셋의 다양한 21개 시퀀스에서 평가한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: User study (N = 20) results for comparing GMR to*

- **GMR 방법론**: 비균등 국소 스케일링과 2단계 최적화를 통해 기존 PHC와 ProtoMotions의 스케일링 관련 인공물을 해결하는 재타겟팅 기법 제안
- **체계적 성능 평가**: 재타겟팅 품질이 정책 성공률에 미치는 영향을 보상 튜닝 없이 실증적으로 증명
- **비교 분석**: GMR이 오픈소스 기준선 대비 추적 성능과 소스 모션 충실도에서 우수하며, 폐쇄소스 Unitree 데이터셋과 비슷한 성능 달성
- **문제 식별**: 발 관통, 자기 교차, 속도 스파이크 같은 주요 재타겟팅 인공물과 초기 프레임의 영향을 명확히 규명

## How

![Figure 2](figures/fig2.webp)

*Fig. 2: General Motion Retargeting (GMR) Pipeline.*

- SMPL 모델 기반의 비균등 국소 스케일링으로 신체 부위별 다른 스케일 적용
- 2단계 최적화: (1) 관절 공간에서 스케일된 참조를 따라 역운동학 해결, (2) 물리 제약 조건 만족
- BeyondMimic을 독립적으로 사용하여 재타겟팅 방법만 분리하여 평가
- LAFAN1 데이터셋의 다양한 모션(5초~2분)에서 단일 트래젝토리 정책 학습
- 센서 노이즈, 모델 파라미터 오류, 네트워크 지연을 포함한 조건에서 다중 평가 실시
- 사용자 연구(N=20)를 통한 지각적 충실도(perceptual fidelity) 검증

## Originality

- 재타겟팅 품질의 정량적 영향을 분리된 조건(고정된 RL 정책)에서 처음으로 체계적으로 분석
- 비균등 국소 스케일링과 2단계 최적화 조합으로 기존 방법들의 구체적 문제점 해결
- 폐쇄소스 고품질 데이터와의 비교를 통해 오픈소스 방법의 성능 격차 정량화
- 초기 프레임과 같은 간과된 요소들의 영향을 실증적으로 입증

## Limitation & Further Study

- 발 이외의 접촉이 있는 모션(손 접촉, 물체 상호작용)은 평가 범위에서 제외
- LAFAN1의 21개 제한된 시퀀스로만 평가했으므로 더 다양한 동작 유형에 대한 일반화 필요
- 폐쇄소스 Unitree 방법의 세부 기술 공개 불가로 직접 비교의 완전성 부족
- 실제 로봇에서의 zero-shot 배포 성능은 평가하지 않음 (시뮬레이션 기반 평가만 수행)
- 후속연구: 손 재타겟팅, 접촉 상호작용 포함 모션, 더 큰 규모 데이터셋에서의 평가 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 재타겟팅 품질의 정량적 영향을 처음으로 체계적으로 분석하고 GMR이라는 실용적인 해결책을 제시하여 휴머노이드 모션 추적의 실제 적용 가능성을 크게 향상시킨다.
