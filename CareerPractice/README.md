# 커리어 실천 도우미 AI

## 📌 개요

- 사용자의 경력 이력을 기반으로, AI가 실천 가능한 커리어 액션 아이템을 추천합니다.
- Pinecone 기반의 벡터 검색과 OpenAI LLM 기반 reasoning을 결합한 커리어 추천 파이프라인.

---

## 📦 디렉토리 구조
```bash
CareerPractice/
│
├── data/ # 원본 raw data 폴더
│
├── database/ # Pinecone vector DB 업서트 스크립트
│ ├── result1.json # 업서트 대상 데이터
│ └── upsert.py # Pinecone 인덱스 생성 및 데이터 삽입
│
├── prompts/ # 모든 LLM용 프롬프트 템플릿 정의
│ ├── init.py
│ └── career_practice_prompts.py
│
├── services/ # 비즈니스 로직 및 파이프라인 코드
│ ├── init.py
│ └── run_career_practice.py # 핵심 파이프라인 및 스키마 정의 (Pydantic 모델 포함)
│
├── .env # API 키 환경변수 (Pinecone, OpenAI)
├── main.py # 실행 진입점 (테스트 및 실행용)
└── README.md
```

---

## 🚀 실행 방법

```bash
python3 main.py
```
※ 실행 전 .env 파일에 API 키를 입력해야 합니다.
OPENAI_API_KEY="your_openai_key_here"
PINECONE_API_KEY="your_pinecone_key_here"
