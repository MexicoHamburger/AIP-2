from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import List
from pydantic import BaseModel, Field
from prompts.make_sequence_prompt import MakeSequencePrompt
from settings import settings

class MakeSequenceParam(BaseModel):
    input_resume: str


class MakeSequenceResponse(BaseModel):
    token_sequence: List[str] = Field(
        description="토큰화된 이력 시퀀스를 JSON 배열(List[str]) 형식으로 출력합니다."
    )


async def run_general_search(param: MakeSequenceParam) -> dict:
    input_resume = param.input_resume


    parser = JsonOutputParser(pydantic_object=MakeSequenceResponse)

    prompt = PromptTemplate(
        template=MakeSequencePrompt.DEFAULT_PROMPT.value,
        input_variables=["user_prompt", "additional_instructions"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
        },
    )

    llm = ChatOpenAI(
        model="o4-mini",
        api_key=settings.openai_api_key,
        temperature=1
    )

    chain = prompt | llm | parser
    return await chain.ainvoke(
        {
            "input_resume": input_resume,
        }
    )
# main.py (또는 현재 파일 하단에 추가)

import asyncio, os, json

async def main():
    input_resume = """
**[이력서]**  
- 이름: 홍민수  
- 생년월일 (나이 만 26세)  
- 전화번호: 010-****-1234  
- 이메일: minsu_hong@xxmail.com  

**학력:**  
- OO초등학교 졸업  
- OO중학교 졸업  
- OO고등학교 졸업  
- YY대학교 컴퓨터공학과 (졸업)

**경력 및 경험:**  
- YY대학교 졸업 프로젝트: "E-commerce Platform Development"  
  - Next.js를 활용한 웹 애플리케이션 개발  
  - React Query로 API 데이터 통신 및 상태 관리 구현  
  - Tailwind CSS를 사용하여 반응형 디자인 및 UI 개발  
  - Git을 통한 버전 관리 경험  

- 인턴 경험: ZZ회사 (2023년 6월 - 2023년 8월)  
  - Agile 환경에서 웹 애플리케이션의 UI/UX 최적화 작업 수행  
  - Git을 활용한 팀 프로젝트에서의 버전 관리 및 협업 경험  

**기술 및 역량:**  
- HTML, CSS, JavaScript: 숙련  
- React.js: 프로젝트 경험 보유  
- Next.js: 프로젝트 경험 보유  
- Git: 능숙하게 사용 가능  
- Tailwind CSS: 경험 보유  
- Zustand: 사용 경험 (학교 프로젝트 상황에서)  
- Figma: 디자인 협업 경험

**기타:**  
- 자격증: 정보처리기사 (2023)  
- 교육이수: "React.js 실무 과정" 수료 (2022년)  
- Hackathon 참여: "최고의 사용자 경험을 위한 UI/UX 디지털 솔루션" 대회 수상 (2023년)
"""

    param = MakeSequenceParam(input_resume=input_resume)
    try:
        result = await run_general_search(param)
        print("\n결과:")
        print(result)

        # JSON 파일에 append
        filepath = "result.json"
        new_entry = result

        # 파일이 존재하면 기존 내용 불러오기
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = [data]
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # 새 항목 추가 후 저장
        data.append(new_entry)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\nresult.json에 저장 완료 (총 {len(data)}건)")
    except Exception as e:
        print(f"\n오류 발생: {e}")

if __name__ == "__main__":
    asyncio.run(main())
