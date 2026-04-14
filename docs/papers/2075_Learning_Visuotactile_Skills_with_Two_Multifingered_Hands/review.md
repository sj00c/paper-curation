# Learning Visuotactile Skills with Two Multifingered Hands

> **저자**: Toru Lin, Yu Zhang, Qiyang Li, Haozhi Qi, Brent Yi, Sergey Levine, Jitendra Malik | **날짜**: 2024-04-25 | **URL**: [https://arxiv.org/abs/2404.16823](https://arxiv.org/abs/2404.16823)

---

## Essence

![Figure 1](figures/fig1.webp)

*Fig. 1. An overview of our system setup and learned visuotactile skills on four tasks. (a) Our hardware and teleoperatio*

VR 기반 저가형 텔레오퍼레이션 시스템 HATO와 촉각 센서가 장착된 의족 손을 활용하여 양손 다중지 조작 로봇이 시각-촉각 데이터로부터 인간 수준의 민첩한 조작 기술을 학습하는 시스템을 제시한다.

## Motivation

- **Known**: 기존 양손 조작 시스템은 단순성 때문에 병렬 그리퍼를 사용하며, imitation learning을 통한 조작 학습이 활발히 연구되고 있다. 그러나 촉각 센싱이 있는 다중지 손을 갖춘 양손 시스템은 매우 드물다.
- **Gap**: 양손 다중지 조작에 적합한 저가형 텔레오퍼레이션 시스템이 없고, 촉각 센싱을 갖춘 다중지 손 하드웨어도 부족하다. 또한 양손 다중지 조작과 visuotactile learning의 교집합 연구가 없다.
- **Why**: 인간 수준의 민첩함(dexterity)을 달성하려면 양손 협력, 적응적 파악, 도구 사용 등이 필수적이며, 촉각 피드백은 미끄러운 물체 조작이나 고정밀 작업에서 중요하다.
- **Approach**: 의료용 의족 손(Psyonic Ability Hand)을 연구용으로 재목적화하고, VR 컨트롤러(Meta Quest 2) 기반의 직관적 매핑을 통해 HATO 시스템을 개발했으며, 멀티모달 데이터 처리와 end-to-end 정책 학습을 수행했다.

## Achievement

![Figure 2](figures/fig2.webp)

*Fig. 2. Illustration of learned skills on four different tasks. Our learned policies complete long-horizon and high-prec*

- **저가형 텔레오퍼레이션 시스템**: Meta Quest 2의 VR 컨트롤러를 활용한 HATO로 30분~2시간의 데이터로 효과적인 정책 학습 가능
- **하드웨어 혁신**: 촉각 센서 장착 의족 손을 로봇 연구용으로 재목적화하여 6개의 손가락 DoF와 6개의 fingertip 촉각 센서 제공
- **복잡한 작업 성공**: 손가락 협력 필요(미끄러운 물체 전달, 블록 스택), 대형 물체 조작(와인 붓기), 도구 사용(스테이크 서빙) 등 4개 작업 수행
- **ablation study**: 촉각과 시각이 정책 성공률과 견고성을 크게 향상시키며, 수백 개의 시연만으로 효과적 학습 가능함을 입증

## How

![Figure 3](figures/fig3.webp)

*Fig. 3. Fingertip Tactile Sensor Layout. There are six tactile*

- Meta Quest 2 컨트롤러 pose → UR5e 팔의 end-effector pose 매핑
- grip button → 4개 손가락 파워 그래스 제어, thumbstick → 엄지 2-DoF 관절 위치 제어
- 3개 RGB-D 카메라(손목 2개, 제3관점 1개) + 각 fingertip 6개 촉각 센서 + proprioception 수집
- Multimodal data processing 파이프라인으로 시각, 촉각, proprioception 정렬 및 처리
- End-to-end behavior cloning으로 vision + tactile input으로부터 정책 학습

## Originality

- **처음의 교집합**: 양손 다중지 조작 + imitation learning + visuotactile sensing의 조합이 기존에 없음
- **의족 재목적화**: 의료용 prosthetic hand를 로봇 연구용으로 전환한 창의적 하드웨어 활용
- **직관적 텔레오퍼레이션**: 기존 retargeting 기반 접근과 달리 그리퍼/엄지 분리 제어로 낮은 지연시간과 사용성 개선
- **체계적 ablation**: dataset size, sensing modality, visual preprocessing의 영향을 종합적으로 분석

## Limitation & Further Study

- 데이터 수집이 여전히 수동 텔레오퍼레이션에 의존하므로 확장성 제한
- 4개 작업만 평가되었으며, 더 다양한 장기 지평 작업에 대한 검증 필요
- 촉각 센서의 temporal dynamics 활용이 제한적이며, 더 정교한 tactile representation 학습 필요
- 단일 정책이 모든 작업을 해결하지는 못하며, 작업별 독립적 정책 학습 필요
- Sim-to-real transfer나 domain adaptation 기법 미적용으로 실제 배포 견고성 평가 부족

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 양손 다중지 조작 분야에서 하드웨어 혁신(의족 재목적화)과 접근성 높은 텔레오퍼레이션 시스템(HATO)을 통해 visuotactile learning의 새로운 경계를 개척했다. 촉각 센싱의 중요성을 실증적으로 보여주고 효율적 데이터 수집 및 정책 학습을 달성하여 로봇 조작 분야에 상당한 기여를 한다.
