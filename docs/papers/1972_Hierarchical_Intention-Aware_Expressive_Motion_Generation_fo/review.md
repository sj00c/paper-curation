# Hierarchical Intention-Aware Expressive Motion Generation for Humanoid Robots

> **저자**: Lingfan Bao, Yan Pan, Tianhu Peng, Dimitrios Kanoulas, Chengxu Zhou | **날짜**: 2025-06-02 | **URL**: [https://arxiv.org/abs/2506.01563](https://arxiv.org/abs/2506.01563)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1: Overall framework of the proposed work. (a) The high-level system architecture. Multimodal inputs XI = (Vin, Lin*

본 논문은 비전-언어 모델(VLM)의 의도 추론과 diffusion 기반 모션 생성을 계층적으로 결합하여, 휴머노이드 로봇이 인간의 사회적 의도와 정서 맥락을 이해하고 실시간으로 표현력 있는 제스처를 생성하는 HIAER 프레임워크를 제안한다.

## Motivation

- **Known**: 최근 VLM은 높은 수준의 의도 해석에서 우수한 성능을 보였고, diffusion 모델(예: DART)은 대규모 모션 데이터셋(AMASS, HumanML3D)을 활용하여 다양한 모션 생성이 가능하다. 또한 RL 기반 whole-body controller는 로봇의 강건한 실행을 가능하게 한다.
- **Gap**: 기존 접근법들은 기능적 목표 분해에 집중하여 명시적 의도는 잘 파악하지만, 동적 사회 환경에 내재된 암묵적 정서 의도와 맥락을 고려하지 못한다. 또한 규칙 기반이나 템플릿 기반 방법은 실제 상황의 유동적 특성에 적응하지 못한다.
- **Why**: 효과적인 인간-로봇 상호작용은 상대방의 의도를 정확히 추론하고 비언어적 응답을 생성하는 긴밀한 결합이 필수적이며, 이는 신뢰 구축, 협업 촉진, 사용자 참여 증대에 중요하다.
- **Approach**: VLM을 이용한 in-context learning과 Chain-of-Thought 프롬팅으로 사회적 의도와 valence-arousal(V-A) 정서 맥락을 추론한 후, DART diffusion 모델에 조건부 텍스트 프롬프트를 제공하여 사회적으로 적절한 모션을 실시간 생성하고, RL 기반 whole-body controller로 물리 로봇에서 실행한다.

## Achievement

![Figure 4](figures/fig4.webp)

*Fig. 4: Qualitative results across the six representative interaction scenarios. Each subfigure from (a) to (f) displays*

- **계층적 의도-인식 프레임워크**: VLM의 정교한 추론을 사회적 의도와 정서 맥락(V-A 모델)에 통합하여 휴머노이드 로봇이 맥락 인식 모션 생성 가능
- **V-A 파라미터화**: 복잡한 사회적 의도를 valence와 arousal로 파라미터화하여 actionable parameter로 변환하고 표현력 있는 모션 선택 가이드
- **VLM 기반 의도 추론 모듈**: ICL과 CoT 프롬팅을 활용한 구조화된 출력 생성으로 신뢰도 점수, V-A 추정, 모션 원시(motion primitive) 도출
- **실제 로봇 검증**: 물리 휴머노이드 플랫폼에서 실제 HRI 시나리오에서 저지연 맥락 적절 제스처 생성 능력 입증 및 사회적 지능성 평가 우수

## How

![Figure 1](figures/fig1.webp)

*Fig. 1: Overall framework of the proposed work. (a) The high-level system architecture. Multimodal inputs XI = (Vin, Lin*

- 입력 모달리티(비전 Vin, 언어 Lin)와 대화 이력 HI/O를 VLM 에이전트 πi에 입력
- 사전 프롬프트 Lpre와 CoT 프롬팅 전략으로 장면 설명(d), 의도(i), 신뢰도(c), V-A 추정, 모션 원시(⟨m⟩) 포함한 구조화된 출력 O 생성
- 출력 O로 조건화된 text-to-motion diffusion 모델 DART을 이용하여 시간적으로 일관성 있는 인간 모션 궤적 ŷt:t+n 합성
- 생성된 궤적을 로봇의 운동학에 맞게 재타겟하여 원하는 궤적 yt:t+n 획득
- 최종적으로 RL 기반 whole-body controller πw에 전달하여 물리 로봇에서 실행

## Originality

- 기존의 기능적 목표 분해를 넘어 **암묵적 정서 의도**를 valence-arousal 모델로 명시적으로 모델링하여 사회적 맥락 인식 실현
- **의도-모션 폐루프의 완성**: VLM의 고수준 추론과 diffusion 모델의 저수준 실행을 계층적으로 통합하는 end-to-end 프레임워크 제시
- **신뢰도 기반 적응형 선택**: 의도 추론의 신뢰도 점수를 구조화된 출력에 포함시켜 fallback behavior와 적응형 응답 가능
- **대규모 데이터 기반 일반화**: AMASS, HumanML3D 같은 대규모 모션 데이터셋을 활용하여 템플릿 의존성 제거 및 다양한 모션 합성

## Limitation & Further Study

- VLM의 의도 추론이 시각적 모호성이나 복잡한 사회적 신호에서 정확도 제한 가능
- Valence-Arousal 모델이 2차원으로 복잡한 인간 정서를 완전히 표현하지 못할 수 있음
- 실시간 성능은 VLM 추론 지연과 diffusion 모델 denoising 단계의 계산 비용에 의존
- 물리 로봇 검증이 특정 휴머노이드 플랫폼에 제한되어 다른 로봇 형태로의 일반화 미지수
- **후속 연구**: 더 정교한 정서 모델 탐색, 크로스 모달 정보 통합, 장시간 상호작용에서의 의도 추적 개선, 다양한 로봇 형태에 대한 일반화

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 VLM의 고수준 사회적 추론과 diffusion 기반 모션 생성을 계층적으로 연결하여 의도-인식 표현력 있는 로봇 행동의 폐루프를 실현한 중요한 기여이다. 물리 로봇 검증과 실제 HRI 시나리오에서의 평가로 실용성을 입증했으나, VLM 추론의 정확도와 계산 효율성 측면에서 추가 개선이 필요하다.
