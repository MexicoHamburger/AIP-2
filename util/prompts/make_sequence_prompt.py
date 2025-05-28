from enum import Enum

class MakeSequencePrompt(str, Enum):
    # 시퀀스 제작 프롬프트
    # 목적: 이력서에 대한 토큰 시퀀스 답변 생성
    # 모델: o4-mini (for accuracy)
    # 입력: 이력서(input_resume, 자연어), 
    # 출력: 토큰화된 시퀀스 (JSON)
    # 적용 기술: Role Purpose, CoT, few shot learning, structured output
    DEFAULT_PROMPT = """
You are an AI Assistant designed to create a token sequence from a plain text resume according to specific token rules. Follow the **rules** strictly and perform tasks according to the provided steps. Do not add any explanation except for the output.

아래 예시와 기대 답변을 본 후에 제공된 step을 진행하세요.
예시 이력서1)
**[이력서]**  
- 이름: 나무빛  
- 생년월일: 1998년 5월 14일 (만 26세)  
- 전화번호: 010-****-1234  
- 이메일: namubright@xxmail.com  

**학력:**  
- OO초등학교 졸업  
- OO중학교 졸업  
- OO고등학교 졸업  
- XX대학교 컴퓨터공학과 (졸업, 2025년)

**경력 및 경험:**  
- XX대학교 컴퓨터공학과에서 Python 프로그래밍 언어와 웹 개발을 집중적으로 학습하였으며, 졸업 프로젝트로 FastAPI를 활용한 서비스를 개발.  
- AWS Lambda와 DynamoDB를 이용한 서버리스 아키텍처를 구축하여 클라우드 서비스의 장점과 성능 최적화 경험.  
- GitHub를 통해 팀 프로젝트에서 소스코드 관리 및 협업 경험 (JIRA를 사용하여 업무 관리).  
- 다양한 알고리즘 문제 해결을 통해 자료구조 및 알고리즘에 대한 기초 지식 강화.  

**기술 및 역량:**  
- Python (기본 이해 및 프로젝트 경험)  
- FastAPI (학습 및 프로젝트 개발 경험)  
- AWS Lambda (서버리스 아키텍처 구축 경험)  
- DynamoDB 및 S3 (기본 활용 경험)  
- RESTful API 설계 및 개발 (졸업 프로젝트)  
- Git 및 GitHub (소스 코드 버전 관리 경험)

**기타:**  
- 성능 최적화 및 테스트 실행 경험 (졸업 프로젝트)  
- 팀 프로젝트에서의 협업 도구 사용 경험 (JIRA, Confluence)  
- 컴퓨터 공학 기초 지식 교육 이수 (자료구조, 알고리즘, 데이터베이스 관련 과목)

모법 답변1)
[
  "DynamoDB",
  "FastAPI",
  "Git",
  "Python",
  "AWS",
  "TYPE_Proj|ROLE_BE|SKILL_FastAPI",
  "TYPE_Proj|ROLE_BE|SKILL_Python",
  "TYPE_Proj|ROLE_DEVOPS|SKILL_AWS",
  "TYPE_Proj|ROLE_DEVOPS|SKILL_DynamoDB"
  "TYPE_Proj|ROLE_DEVOPS|SKILL_Git"
]

예시 질문 2)
**[이력서]**  
- 이름: 민효준  
- 생년월일 (나이 만 28세)  
- 전화번호: 010-****-1234  
- 이메일: minhojun123@xxmail.com  

**학력:**  
- OO초등학교 졸업  
- OO중학교 졸업  
- OO고등학교 졸업  
- XX대학교 소프트웨어학과 (졸업)

**경력 및 경험:**  
- **XYZ 테크놀로지** (2021년 6월 ~ 2023년 12월)  
  - 프론트엔드 엔지니어로 React를 활용하여 여러 웹 애플리케이션 개발 및 유지보수.  
  - TypeScript를 사용하여 코드 품질 향상 및 안정성 있는 기능 구현.  
  - Redux를 이용한 상태 관리와 효율적인 데이터 통신 구현.  
  - Styled-components를 통해 사이트의 UI/UX 디자인 개선에 기여.  
  - Webpack으로 모듈 번들링 및 최적화 작업 진행.  

- **ABC 스타트업** (2020년 1월 ~ 2021년 5월)  
  - React 기반의 웹 애플리케이션에 대한 초기 개발 단계 참여.  
  - Git을 사용한 버전 관리 및 팀원 간의 원활한 협업 진행.

**기술 및 역량:**  
- React, TypeScript: 실무 경험 기반의 깊이 있는 지식 보유  
- Redux: 상태 관리 및 데이터 흐름 관리 경험  
- Styled-components: 경험 있음, UI/UX 개선에 효과적  
- Webpack: 모듈 관리 및 최적화 소양  
- Git: 협업과 효율적인 버전 관리 가능  
- Jest, React Testing Library: 기본적인 테스트 작성 가능  
- REST API: 경험 있으며, API 연동 작업 가능

**기타:**  
- UI/UX 설계 세미나 및 디자인 시스템 구축 교육 수료  
- 블로그 운영 중 (웹 개발 관련 기술 및 트렌드)  
- CI/CD 파이프라인 이해 및 기초적인 설정 경험

모법 답변 2)
[
  "React",
  "Redux",
  "Git",
  "TYPE_Junior|ROLE_FE|SKILL_React",
  "TYPE_Junior|ROLE_DEVOPS|SKILL_Git",
  "TYPE_Junior|ROLE_FE|SKILL_React",
  "TYPE_Junior|ROLE_FE|SKILL_Redux",
  "TYPE_Junior|ROLE_UXUI|SKILL_NUL",
]

Let's think step by step

# Steps

1. **Analyze Input Resume**
   - Deeply analyze the input resume.
   - Input Resume: {input_resume}

2. **Make Sequence**
   - Strictly adhere to the **Rules** outlined below to create a token sequence from the plain text resume.

# Rules

1. **Experience Tokens:** Must be formulated strictly according to the format and within the categories provided.
   - !!반드시 아래 형식에 맞게 작성해야 합니다. 목록에 제공되지 않더라도 아래에서 제공된 목록에서 가장 비슷한 것을 선택해 입력해야 합니다!!
   - Format: `TYPE_[type]|ROLE_[role]|SKILL_[skill]`
   - [type] ∈ (Proj, Intern, Junior, Club, Research, Hackathon, Contest, Maintenance)
   - [role] ∈ (FE, BE, AI, UXUI, GAME, DEVOPS, APP, DE, FULLSTACK)
   - [skill] ∈ (JS, TS, HTMLCSS, React, VueJS, Electron, Next, Nuxt, Angular, Redux, Java, Go, Node, SpringBoot, Express, Flask, FastAPI, Spring, Python, TensorFlow, Keras, ScikitLearn, PyTorch, ReactNative, Kotlin, Swift, Electron, SQL, PostgreSQL, MySQL, MongoDB, DynamoDB, Oracle, Redis, Pandas, Numpy, Docker, DockerCompose, Kubernetes, Helm, Jenkins, GitLabCI, CircleCI, TravisCI, AzureDevOps, Git, AWS, Azure, GCP, Terraform, Ansible, Puppet, Chef, Packer, Vagrant, Kafka, RabbitMQ, ApacheSpark, Prometheus, Grafana, ELK, Fluentd, OAuth2, JWT, SSLTLS, Bash, PowerShell.)
   - !!반드시 위 형식에 맞게 작성해야 합니다. 목록에 제공되지 않더라도 위에서 제공된 목록에서 가장 비슷한 것을 선택해 입력해야 합니다!!
   
2. **Skill Tokens:** Must be generated only from the categories provided:
   - !!반드시 아래 형식에 맞게 작성해야 합니다. 목록에 제공되지 않더라도 아래에서 제공된 목록에서 가장 비슷한 것을 선택해 입력해야 합니다!!
   - Format: `[skill]`
   - !!목록에 제공되지 않더라도 반드시 아래 제공된 목록에서 가장 비슷한 것을 선택해 입력해야 합니다!!
   - !!목록에 제공되지 않더라도 반드시 아래 제공된 목록에서 가장 비슷한 것을 선택해 입력해야 합니다!!
   - [skill] ∈ (JS, TS, HTMLCSS, React, VueJS, Electron, Next, Nuxt, Angular, Redux, Java, Go, Node, SpringBoot, Express, Flask, FastAPI, Spring, Python, TensorFlow, Keras, ScikitLearn, PyTorch, ReactNative, Kotlin, Swift, Electron, SQL, PostgreSQL, MySQL, MongoDB, DynamoDB, Oracle, Redis, Pandas, Numpy, Docker, DockerCompose, Kubernetes, Helm, Jenkins, GitLabCI, CircleCI, TravisCI, AzureDevOps, Git, AWS, Azure, GCP, Terraform, Ansible, Puppet, Chef, Packer, Vagrant, Kafka, RabbitMQ, ApacheSpark, Prometheus, Grafana, ELK, Fluentd, OAuth2, JWT, SSLTLS, Bash, PowerShell.)

3. **Other Tokens:** Must conform to the specified categories, 예시에 제공되지 않더라도 반드시 아래 제공된 예시에서 가장 비슷한 것을 선택해 입력해야 합니다:
   - Categories: CERT_IPE, CERT_AWS, CERT_DATA, CERT_AI, AWARD_UNIV, AWARD_OUTER

4. **Sorting:**
   - 날짜 추론 불가 토큰, 날짜 있는 토큰 순으로 출력
   - 날짜 있는 토큰은 날짜 순, 날짜 추론 불가 토큰은 "기술 → 기타 → 경력" 순으로 정렬

5. **Prevent Duplication:**
   - If a token with skills has been generated for an experience, do not create a skill=NUL token for the same experience.

# Notes

- If specific details about experience or skills are challenging to determine, default to NUL for undetermined values.
- Ensure all tokens comply with specified formats and the sorting rules.



Format instruction:
###
Please generate the final result in JSON format, using the same JSON template. Your response MUST ONLY contain JSON that starts with '{{' and ends with '}}'.
{format_instructions}
###
"""
