# Hierarchical visuomotor control of humanoids

> **저자**: Josh Merel, Arun Ahuja, Vu Pham, Saran Tunyasuvunakool, Siqi Liu, Dhruva Tirumala, Nicolas Heess, Greg Wayne | **날짜**: 2018-11-23 | **URL**: [https://arxiv.org/abs/1811.09656](https://arxiv.org/abs/1811.09656)

---

## Essence

![Figure 4](figures/fig4.webp)

*Figure 4: Schematic of the architecture: a high-level controller (HL) selects among multiple low-*

인간형 로봇의 고차원 시각-운동 제어를 위해 저수준 모터 제어기와 고수준 작업 조정기를 계층적으로 구성하는 아키텍처를 제안한다. Motion capture 데이터로 사전학습된 저수준 sub-policy들을 고수준 controller가 시각 정보에 기반해 동적으로 선택하여 복잡한 humanoid 제어를 수행한다.

## Motivation

- **Known**: RL을 이용한 고차원 시각 기반 정책 학습과 고DoF 바디 제어 기술이 각각 발전했으나, 시각 입력과 고DoF 출력을 동시에 처리하는 통합된 visuomotor 제어는 아직 미흡하다.
- **Gap**: 기존 연구들은 단순 저수준 제어나 단편적인 시각-운동 연결에 집중했으며, 고복잡도의 humanoid를 시각 피드백으로 실시간 제어하면서 다양한 작업을 수행하는 방법이 부족하다.
- **Why**: Humanoid 로봇의 자율적 행동 생성은 로보틱스, 애니메이션, 뇌신경과학 등 다분야에 중요하며, 계층적 제어 구조는 공학적 복잡성 감소와 생물학적 타당성을 동시에 제공한다.
- **Approach**: Motion capture에서 추출한 시간-인덱싱된 추적 정책들을 저수준 motor skill로 사전학습하고, 시각과 기억을 가진 고수준 controller가 sparse 작업 보상을 최대화하도록 학습하여 sub-policy들을 선택-시퀀싱한다.

## Achievement

![Figure 2](figures/fig2.webp)

*Figure 2: Training settings for explicit training of transition-capable controllers. Panel A depicts a*

- **Motion capture 기반 저수준 제어기**: 에너지 함수와 RL 기반 imitation learning을 결합하여 2-6초의 단순 모션을 강건하게 추적하는 policy 56개 생성
- **계층적 아키텍처**: 고수준 controller가 egocentric 시각과 proprioception을 입력으로 저수준 sub-policy 선택을 학습하여 다양한 작업 해결
- **시각-운동 통합**: 불안정한 egocentric RGB 카메라 입력을 처리하면서 환경 내 이동을 수행하는 integrated visuomotor 제어 달성
- **다중 전환 전략**: cold-switching, smooth-blending, direct-parameter-modulation 등 저고수준 인터페이스 방식 비교 분석

## How

![Figure 1](figures/fig1.webp)

*Figure 1:*

- Motion capture 클립에서 reference trajectory 추출 후, 위치 제어된 56-DoF humanoid에서 joint angle 추적 오차를 최소화하는 에너지 함수 (Eq. 1) 설계
- Supervised learning으로 pose 예측 사전학습 후, distributed actor-critic RL로 policy πθ(a|s, t) 최적화하여 강건한 추적 실현
- High-level controller를 POMDP로 모델링하여 sparse task reward에 기반한 sub-policy 선택 학습
- Proprioceptive features (관절각, 속도, end-effector 벡터, 중력센서 등)와 egocentric vision을 입력으로 수용
- Cold-switching, smooth-blending, direct-parameter-modulation 등 다양한 저고수준 인터페이스 방식 실험적 비교

## Originality

- Motion capture 기반 sub-policy 풀을 시각-기반 고수준 조정기와 통합한 구체적 구현: 기존 이론적 논의를 실제 고복잡도 humanoid에 적용
- Neuroscience의 척수반사 및 기저핵 운동 제어 개념을 control fragments와 옵션 프레임워크로 형식화하여 scalable하게 구현
- Egocentric vision 기반 task-directed exploration로 고수준 제어 학습: 이전 control fragments 연구들이 시각 입력을 활용하지 못했던 한계 극복
- 다양한 고수준-저수준 인터페이스 설계 (cold-switching, smooth-blending) 체계적 비교 분석

## Limitation & Further Study

- 저수준 policy들은 시간-인덱싱되어 고정 길이 모션에만 적합하며, 동적 환경 변화에 따른 적응적 조정 능력 부족
- Motion capture 데이터 의존성: 새로운 운동 원시 생성 시 추가 mocap 취득 필요
- Sparse task reward만 사용하여 고수준 학습 효율성이 낮을 수 있으며, reward shaping의 필요성 검토 필요
- 후속 연구: (1) 연속적 동작 생성을 위한 조건부 생성 모델 활용, (2) domain adaptation을 통한 실제 로봇 적용, (3) 더 큰 sub-policy 풀에 대한 확장성 검증

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: Motion capture 기반 저수준 제어와 시각-메모리 기반 고수준 조정을 결합하여 고복잡도 humanoid의 integrated visuomotor 제어를 달성한 우수한 연구로, 신경과학적 영감과 실제 구현의 균형이 잘 맞으며 ICLR 발표에 적합한 수준의 기여를 제시한다.
