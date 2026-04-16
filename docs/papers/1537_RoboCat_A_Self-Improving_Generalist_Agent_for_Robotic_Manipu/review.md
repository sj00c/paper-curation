---
title: "1537_RoboCat_A_Self-Improving_Generalist_Agent_for_Robotic_Manipu"
authors:
  - "Konstantinos Bousmalis"
  - "Giulia Vezzani"
  - "Dushyant Rao"
  - "Coline Devin"
  - "Alex X. Lee"
date: "2023.06"
doi: ""
arxiv: ""
score: 4.0
essence: "RoboCat는 서로 다른 로봇과 작업 경험을 활용하여 다중 embodiment과 다중 작업을 처리할 수 있는 시각 기반 goal-conditioned decision transformer 기반의 자가 개선 로봇 조작 에이전트이다. 100-1000개의 예제만으로 새로운 작업과 로봇에 적응하며, 자체 생성 데이터를 이용한 반복적 개선이 가능하다."
tags:
  - "cat/Multimodal_Robot_Learning_Systems"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Large-Scale_Robot_Learning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Bousmalis et al._2023_RoboCat A Self-Improving Generalist Agent for Robotic Manipulation.pdf"
---

# RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation

> **저자**: Konstantinos Bousmalis, Giulia Vezzani, Dushyant Rao, Coline Devin, Alex X. Lee, Maria Bauza, Todor Davchev, Yuxiang Zhou, Agrim Gupta, Akhil Raju, Antoine Laurens, Claudio Fantacci, Valentin Dalibard, Martina Zambelli, Murilo Martins, Rugile Pevceviciute, Michiel Blokzijl, Misha Denil, Nathan Batchelor, Thomas Lampe, Emilio Parisotto, Konrad Żołna, Scott Reed, Sergio Gómez Colmenarejo, Jon Scholz, Abbas Abdolmaleki, Oliver Groth, Jean-Baptiste Regli, Oleg Sushkov, Tom Rothörl, José Enrique Chen, Yusuf Aytar, Dave Barker, Joy Ortiz, Martin Riedmiller, Jost Tobias Springenberg, Raia Hadsell, Francesco Nori, Nicolas Heess | **날짜**: 2023-06-20 | **URL**: [https://arxiv.org/abs/2306.11706](https://arxiv.org/abs/2306.11706)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1: The self-improvement process. RoboCat is a multi-task, multi-embodiment visual goal-conditioned*

RoboCat는 서로 다른 로봇과 작업 경험을 활용하여 다중 embodiment과 다중 작업을 처리할 수 있는 시각 기반 goal-conditioned decision transformer 기반의 자가 개선 로봇 조작 에이전트이다. 100-1000개의 예제만으로 새로운 작업과 로봇에 적응하며, 자체 생성 데이터를 이용한 반복적 개선이 가능하다.

## Motivation

- **Known**: 최근 vision과 language 분야의 foundation model 발전으로 multi-task learning이 성공하였으며, transformer 기반 모델이 Gato처럼 다양한 도메인 작업을 수행할 수 있음이 입증되었다. 그러나 기존 로봇 연구는 일반적으로 단일 task 중심이거나 동일한 관측 및 action space를 가정했다.
- **Gap**: 이질적인 로봇 데이터를 대규모로 활용하여 서로 다른 embodiment(자유도, 관측, action space 상이)과 작업에 대한 일반화 능력을 갖춘 generalist agent의 부재가 있다. 또한 자동으로 개선되는 self-improvement loop를 갖춘 로봇 조작 시스템의 실증이 부족하다.
- **Why**: 로봇 학습의 높은 데이터 수집 비용을 감소시키고, 새로운 embodiment과 작업에 빠르게 적응할 수 있으면 로봇 학습을 근본적으로 변화시킬 수 있기 때문이다. 자가 개선 loop는 인간 개입 최소화로 지속적 개선을 가능하게 한다.
- **Approach**: VQ-GAN 인코더를 사용하여 이미지를 토큰화하고, visual goal-conditioning을 통해 다양한 관측/action 차원을 다루며, autoregressive transformer 기반으로 π(at|ot, gt)를 학습한다. Hindsight goal을 활용하여 데이터 효율성을 높이고, fine-tuning 후 생성된 데이터를 다시 학습 데이터에 추가하는 반복 과정을 통해 자가 개선한다.

## Achievement

![Figure 5](figures/fig5.webp)

*Figure 5: RoboCat compared to VFM baselines on training tasks. RoboCat performs better on the vast*

- **다중 embodiment과 작업의 처리**: 서로 다른 자유도, 관측, action space를 가진 실제 로봇 embodiment 3개 이상에서 다양한 조작 작업을 성공적으로 수행
- **효율적 적응**: 목표 작업에 대해 단 100-1000개의 시연만으로 zero-shot 및 fine-tuning 기반 적응 가능
- **자가 개선 루프 실증**: fine-tuned agent가 생성한 데이터를 학습 데이터에 추가하여 다음 iteration의 성능 향상을 증명
- **cross-task transfer**: 학습 데이터 확장 및 다양화에 따라 작업 간 전이 학습 성능과 새로운 작업 적응 효율이 개선됨을 입증

## How

![Figure 1](figures/fig1.webp)

*Figure 1: The self-improvement process. RoboCat is a multi-task, multi-embodiment visual goal-conditioned*

- VQ-GAN을 사용한 이미지 토큰화로 빠른 학습 가능
- Visual goal-conditioning 방식으로 임의의 trajectory 마지막 이미지를 goal로 활용
- Hindsight goal 기법으로 추가 인간 감독 없이 기존 데이터로부터 goal 자동 추출
- Autoregressive transformer에서 variable-length sequence를 context에 따라 처리하여 heterogeneous embodiment 수용
- Tokenized trajectory representation [x, I, g, a]로 다양한 차원의 proprioceptive observation과 action을 통합
- 초기 다양한 작업/robot 데이터로 generalist agent 학습
- 새로운 작업에 대해 소규모 demonstration dataset으로 fine-tuning
- Fine-tuned agent를 실제 환경에 배치하여 on-policy 데이터 자동 수집
- 수집된 데이터를 원본 dataset에 추가하여 다음 iteration 학습

## Originality

- 처음으로 대규모 transformer sequence model이 이질적 embodiment(서로 다른 자유도, 관측, action space)을 가진 실제 로봇에서 다양한 조작 작업을 수행함을 입증
- Visual goal-conditioning과 hindsight goal을 활용하여 데이터 효율성과 자동 데이터 활용을 혁신적으로 개선
- 실제 로봇에서 self-improvement loop가 작동함을 최초로 실증하여 autonomous improvement의 가능성 제시
- Foundation model 패러다임을 로봇 조작에 체계적으로 적용한 첫 번째 대규모 실증 사례

## Limitation & Further Study

- 테이블톱 object manipulation 중심으로 제한되어 있으며, 더 복잡한 환경이나 전신 움직임 작업으로의 일반화 미검증
- Self-improvement loop의 단 한 번의 iteration만 입증되었으므로, 장기적 scaling과 performance saturation에 대한 분석 부족
- Fine-tuning 시 100-1000개 시연이 필요하다는 것은 여전히 상당한 데이터 수집 비용이므로, 더 낮은 샘플 복잡도 달성 가능성 미불명
- 다양한 실세계 변동(조명, 카메라 각도, 객체 특성 등)에 대한 견고성 평가가 충분하지 않음
- 후속 연구: 더 긴 horizon task, multi-step planning, 언어 조건화 등과의 통합 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 3/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: RoboCat는 foundation model 패러다임을 로봇 조작에 성공적으로 적용하여 이질적 embodiment 처리, 효율적 적응, 자가 개선을 동시에 달성한 획기적 연구이다. 광범위한 실험 검증과 명확한 presentation이 강점이나, 복잡도 증가와 장기 scaling에 대한 분석이 향후 과제이다.

## Related Papers

- 🔄 다른 접근: [[papers/1496_Octo_An_Open-Source_Generalist_Robot_Policy/review]] — Octo와 함께 범용 로봇 정책을 추구하지만 RoboCat는 자가 개선에, Octo는 오픈소스 일반화에 초점을 맞춘 서로 다른 접근이다.
- 🔗 후속 연구: [[papers/1504_Open_X-Embodiment_Robotic_Learning_Datasets_and_RT-X_Models/review]] — Open X-Embodiment의 다중 embodiment 데이터를 활용하여 RoboCat의 크로스 로봇 학습 능력을 더욱 체계화했다.
- 🏛 기반 연구: [[papers/1316_Behavior_Transformers_Cloning_k_modes_with_one_stone/review]] — RoboCat의 self-improving agent를 위한 기본적인 behavior cloning과 multi-modal learning 방법론을 제공한다.
- 🔗 후속 연구: [[papers/1542_RoboMonkey_Scaling_Test-Time_Sampling_and_Verification_for_V/review]] — RoboCat의 self-improvement를 RoboMonkey의 test-time sampling과 verification으로 확장하여 더 신뢰성 있는 로봇 학습을 달성할 수 있다.
- 🔄 다른 접근: [[papers/1294_A_Generalist_Agent/review]] — RoboCat의 robot-specific generalist agent와 달리 일반적인 multi-domain generalist agent 접근법을 제시한다.
- 🔗 후속 연구: [[papers/1294_A_Generalist_Agent/review]] — RoboCat은 Gato의 범용 에이전트 개념을 로봇 조작에 특화하여 발전시킨 후속 연구입니다.
- 🏛 기반 연구: [[papers/1554_RT-1_Robotics_Transformer_for_Real-World_Control_at_Scale/review]] — RoboCat의 self-improving agent 개념이 RT-1의 대규모 학습과 일반화 능력 개발의 이론적 기반이다.
- 🔗 후속 연구: [[papers/1606_Vision-Language_Foundation_Models_as_Effective_Robot_Imitato/review]] — self-improving generalist agent 개념을 VLM 기반 imitation learning으로 확장하여 더 효율적인 로봇 학습을 제시합니다.
