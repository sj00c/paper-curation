---
title: "1404_Gemini_Robotics_Bringing_AI_into_the_Physical_World"
authors:
  - "Gemini Robotics Team"
  - "Saminda Abeyruwan"
  - "Joshua Ainslie"
  - "Jean-Baptiste Alayrac"
  - "Montserrat Gonzalez Arenas"
date: "2025.03"
doi: ""
arxiv: ""
score: 4.0
essence: "Gemini 2.0 기반의 Vision-Language-Action 모델인 Gemini Robotics를 제시하여, 대규모 멀티모달 모델의 embodied reasoning 능력을 로봇 제어에 직접 활용하고 복잡한 조작 작업을 수행할 수 있도록 한다."
tags:
  - "cat/Embodied_Visual_Reasoning"
  - "cat/Robotic_Manipulation_and_Simulation"
  - "cat/Foundation_Models_for_Robotics"
  - "sub/Embodied_Visual_Reasoning"
  - "topic/physical-ai"
pdf: "C:/Users/jehyu/GoogleDrive/Zotero/Team et al._2025_Gemini Robotics Bringing AI into the Physical World.pdf"
---

# Gemini Robotics: Bringing AI into the Physical World

> **저자**: Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, Steven Bohez, Konstantinos Bousmalis, Anthony Brohan, Thomas Buschmann, Arunkumar Byravan, Serkan Cabi, Ken Caluwaerts, Federico Casarini, Oscar Chang, Jose Enrique Chen, Xi Chen, Hao-Tien Lewis Chiang, Krzysztof Choromanski, David D'Ambrosio, Sudeep Dasari, Todor Davchev, Coline Devin, Norman Di Palo, Tianli Ding, Adil Dostmohamed, Danny Driess, Yilun Du, Debidatta Dwibedi, Michael Elabd, Claudio Fantacci, Cody Fong, Erik Frey, Chuyuan Fu, Marissa Giustina, Keerthana Gopalakrishnan, Laura Graesser, Leonard Hasenclever, Nicolas Heess, Brandon Hernaez, Alexander Herzog, R. Alex Hofer, Jan Humplik, Atil Iscen, Mithun George Jacob, Deepali Jain, Ryan Julian, Dmitry Kalashnikov, M. Emre Karagozler, Stefani Karp, Chase Kew, Jerad Kirkland, Sean Kirmani, Yuheng Kuang, Thomas Lampe, Antoine Laurens, Isabel Leal, Alex X. Lee, Tsang-Wei Edward Lee, Jacky Liang, Yixin Lin, Sharath Maddineni, Anirudha Majumdar, Assaf Hurwitz Michaely, Robert Moreno, Michael Neunert, Francesco Nori, Carolina Parada, Emilio Parisotto, Peter Pastor, Acorn Pooley, Kanishka Rao, Krista Reymann, Dorsa Sadigh, Stefano Saliceti, Pannag Sanketi, Pierre Sermanet, Dhruv Shah, Mohit Sharma, Kathryn Shea, Charles Shu, Vikas Sindhwani, Sumeet Singh, Radu Soricut, Jost Tobias Springenberg, Rachel Sterneck, Razvan Surdulescu, Jie Tan, Jonathan Tompson, Vincent Vanhoucke, Jake Varley, Grace Vesom, Giulia Vezzani, Oriol Vinyals, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Fei Xia, Ted Xiao, Annie Xie, Jinyu Xie, Peng Xu, Sichun Xu, Ying Xu, Zhuo Xu, Yuxiang Yang, Rui Yao, Sergey Yaroshenko, Wenhao Yu, Wentao Yuan, Jingwei Zhang, Tingnan Zhang, Allan Zhou, Yuxiang Zhou | **날짜**: 2025-03-25 | **URL**: [https://arxiv.org/abs/2503.20020](https://arxiv.org/abs/2503.20020)

---

## Essence

![Figure 1](figures/fig1.webp)

*Figure 1 | Overview of the Gemini Robotics family of embodied AI models. Gemini 2.0 already exhibits*

Gemini 2.0 기반의 Vision-Language-Action 모델인 Gemini Robotics를 제시하여, 대규모 멀티모달 모델의 embodied reasoning 능력을 로봇 제어에 직접 활용하고 복잡한 조작 작업을 수행할 수 있도록 한다.

## Motivation

- **Known**: 대규모 멀티모달 모델은 디지털 도메인에서 뛰어난 일반화 능력을 보이고 있으나, 이를 로봇과 같은 물리적 에이전트로 전환하는 것은 여전히 어려운 문제이다.
- **Gap**: 기존 VLM들은 2D 인식에 중점을 두고 있으며, 물리적 세계의 3D 구조, 시공간적 추론, 접촉 물리학 등 embodied reasoning 능력이 부족하다. 또한 로봇 제어에 필요한 low-level action grounding이 미흡하다.
- **Why**: 일반 목적의 로봇이 실세계에서 안전하고 효과적으로 작동하려면 강력한 embodied reasoning과 정확한 물리적 상호작용 이해가 필수적이며, 이는 인공지능이 물리적 세계에서 잠재력을 발휘하는 데 핵심이다.
- **Approach**: Gemini 2.0의 멀티모달 이해 능력을 기반으로 embodied reasoning 능력을 강화한 Gemini Robotics-ER 모델을 먼저 개발한 후, 이를 로봇 행동 데이터로 fine-tuning하여 직접 로봇 제어가 가능한 Vision-Language-Action 모델 Gemini Robotics를 구축한다.

## Achievement

![Figure 1](figures/fig1.webp)

*Figure 1 | Overview of the Gemini Robotics family of embodied AI models. Gemini 2.0 already exhibits*

- **ERQA 벤치마크 개발**: Embodied reasoning 능력을 평가하기 위한 오픈소스 벤치마크를 구축하여 2D/3D 객체 감지, pointing, trajectory 예측, state estimation 등 다양한 공간적 추론 능력을 측정
- **Gemini Robotics-ER 모델**: 강화된 spatial 및 temporal understanding을 통해 object detection, 3D bounding box prediction, multi-view correspondence, grasp prediction 등 로봇에 필수적인 embodied reasoning 능력을 달성
- **Gemini Robotics VLA 모델**: 다양한 복잡한 조작 작업(origami 접기, 카드 게임 등)을 수행하고, 100개의 데모로 새로운 short-horizon task 학습, 새로운 로봇 embodiment(bi-arm platform, humanoid)로의 빠른 적응 능력 입증
- **일반화 및 강건성**: 다양한 객체 종류, 위치 변화, unseen 환경에 대한 강건성을 보이며, open vocabulary instruction을 따르고, zero-shot 및 few-shot 학습이 가능
- **안전 고려사항**: 대규모 로봇 foundation model의 안전 함의를 논의하고 responsible development 지침을 제시

## How

![Figure 1](figures/fig1.webp)

*Figure 1 | Overview of the Gemini Robotics family of embodied AI models. Gemini 2.0 already exhibits*

- Gemini 2.0의 multimodal foundation model을 출발점으로 하여 embodied reasoning 능력의 기초 검증
- 로봇 관련 대규모 dataset(diverse robot actions, dexterous tasks, new embodiments, embodied reasoning dataset)으로 robotics-specific training 수행
- Gemini Robotics-ER에서 향상된 spatial-temporal understanding을 통해 3D perception, trajectory/grasp prediction 등의 능력을 먼저 확보
- 로봇 행동 데이터(action data)를 통합하여 low-level control을 가능하게 하는 Vision-Language-Action 모델 개발
- optional specialization stage를 통해 극도의 dexterity, 어려운 generalization setting에서의 고급 추론, 완전히 새로운 embodiment으로의 적응 지원
- ERQA 벤치마크로 embodied reasoning 능력을 체계적으로 평가(spatial reasoning 84개, action reasoning 72개 등의 문제 카테고리)

## Originality

- Gemini 2.0이라는 state-of-the-art VLM을 로봇 도메인으로 확장하여 embodied AI를 구현한 첫 시도
- embodied reasoning capability를 명확하게 정의하고 이를 평가하기 위한 전용 벤치마크 ERQA를 새로이 개발
- Vision-Language-Action 통합 모델을 통해 인식(perception)과 행동(action)을 직접 연결하는 end-to-end 접근
- 새로운 embodiment으로의 빠른 적응과 극도의 dexterity를 위한 specialization 전략 제시
- Responsible development와 safety considerations를 체계적으로 논의하며 foundation model의 사회적 영향 검토

## Limitation & Further Study

- 논문은 주로 기술 성과에 초점을 맞추고 있으며, 정량적인 비교 평가 결과와 기존 로봇 제어 방식과의 성능 비교가 제한적
- 실제 물리적 상호작용의 복잡성(마찰, 변형, 예상 밖의 동역학 등)에 대한 로버스트성 평가가 추가로 필요
- 후속 연구에서는 더 광범위한 embodiment에 대한 generalization 능력 검증과 장시간 deployment에서의 안정성 평가가 필수
- AI 모델의 의도하지 않은 오류나 dangerous action 생성에 대한 위험성 평가 및 mitigation strategy의 실제 효과 입증이 필요

## Evaluation

- Novelty: 4/5
- Technical Soundness: 4/5
- Significance: 4/5
- Clarity: 4/5
- Overall: 4/5

**총평**: 본 논문은 state-of-the-art VLM인 Gemini 2.0을 로봇 제어에 성공적으로 적용하여 embodied reasoning과 action grounding을 통합한 Vision-Language-Action 모델을 제시함으로써, 일반 목적의 로봇 개발 분야에 획기적인 기여를 한다. ERQA 벤치마크 개발, Gemini Robotics-ER과 Gemini Robotics 모델의 우수한 성능, 그리고 responsible development 논의는 로봇 AI의 실용화와 안전성을 동시에 고려한 종합적인 접근을 보여준다.

## Related Papers

- 🏛 기반 연구: [[papers/1403_Gemini_Robotics_15_Pushing_the_Frontier_of_Generalist_Robots/review]] — Gemini Robotics 1.5의 기본이 되는 초기 Vision-Language-Action 모델 버전이다.
- 🔄 다른 접근: [[papers/1512_PaLM-E_An_Embodied_Multimodal_Language_Model/review]] — 둘 다 대규모 멀티모달 모델의 embodied 적용이지만 Gemini는 로봇 제어에, PaLM-E는 언어 모델에 집중한다.
- 🔗 후속 연구: [[papers/1555_RT-2_Vision-Language-Action_Models_Transfer_Web_Knowledge_to/review]] — RT-2의 웹 지식 전이 접근법을 Gemini 2.0 기반으로 더 발전시켜 embodied reasoning을 강화했다.
- 🔗 후속 연구: [[papers/1436_InstructVLA_Vision-Language-Action_Instruction_Tuning_from_U/review]] — Gemini 2.0의 추론 능력을 활용한 VLA 접근법으로 InstructVLA의 instruction tuning 개념과 상호 보완적이다.
- 🔄 다른 접근: [[papers/1369_Do_As_I_Can_Not_As_I_Say_Grounding_Language_in_Robotic_Affor/review]] — SayCan과 Gemini Robotics 모두 LLM을 로봇 제어에 활용하지만 affordance grounding vs 직접 제어의 차이가 있음
- 🧪 응용 사례: [[papers/1590_Toward_General-Purpose_Robots_via_Foundation_Models_A_Survey/review]] — 범용 로봇을 위한 foundation model 서베이는 Gemini Robotics가 제시한 AI의 물리 세계 적용 비전을 체계화함
- 🔗 후속 연구: [[papers/1403_Gemini_Robotics_15_Pushing_the_Frontier_of_Generalist_Robots/review]] — Gemini Robotics의 기본 모델을 Motion Transfer와 embodied thinking으로 발전시킨 개선된 버전이다.
