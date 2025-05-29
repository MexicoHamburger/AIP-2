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
import pandas as pd

CSV_PATH = "~/aip/jobpost_resume_only.csv"   # ← 필요하면 경로 수정
RESULT_PATH = "result.json"                      # 결과 저장 파일

# --- 유틸 함수 ---------------------------------------------------------- #
async def process_single_resume(resume_text: str) -> dict:
    """단일 이력서를 LLM 체인에 넘겨 결과를 반환."""
    param = MakeSequenceParam(input_resume=resume_text)
    return await run_general_search(param)


async def load_existing_results(path: str) -> list:
    """기존 JSON 결과가 있으면 불러오고, 없으면 빈 리스트 반환."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else [data]
        except json.JSONDecodeError:
            pass
    return []


async def main():
    # 1) CSV 파일에서 resume 컬럼 읽어오기
    df = pd.read_csv(CSV_PATH)

    # ────────────────────────────────────────────────────────────────
    # ▶ ① 행 번호 범위로 자르기 (예: 0번째~99번째 총 100개만)
    df_subset = df.iloc[100:1000]          # <- 원하는 범위로 수정: iloc[start:end]

    # ▶ ② 특정 인덱스(리스트)만 선택 (예: 0, 3, 7, 10번째 행만)
    # wanted_idx = [0, 3, 7, 10]
    # df_subset = df.loc[wanted_idx]

    # ▶ ③ 임의로 N개 샘플링 (예: 무작위 500개)
    # df_subset = df.sample(n=500, random_state=42)
    # ────────────────────────────────────────────────────────────────
    resumes: list[str] = df_subset["resume"].dropna().tolist()
    print(f"총 {len(resumes):,}개의 이력서를 처리합니다.")

    # 2) 기존 결과 불러오기
    aggregated: list = await load_existing_results(RESULT_PATH)

    # 3) LLM 호출 (동시에 너무 많이 호출하면 rate-limit가 걸릴 수 있으니 주의)
    #    → 필요 시 semaphore 로 동시 호출 수 제한 가능
    sem = asyncio.Semaphore(5)           # 동시 5개 호출 예시 (원하면 조정)

    async def safe_process(res_text):
        async with sem:
            return await process_single_resume(res_text)

    tasks = [safe_process(r) for r in resumes]

    for coro in asyncio.as_completed(tasks):
        try:
            result = await coro
            aggregated.append(result)
        except Exception as e:
            print("⚠️  처리 실패:", e)

    # 4) JSON 파일로 저장
    with open(RESULT_PATH, "w", encoding="utf-8") as f:
        json.dump(aggregated, f, indent=2, ensure_ascii=False)

    print(f"\n완료! result.json에 총 {len(aggregated):,}건이 저장되었습니다.")

# 스크립트 진입점
if __name__ == "__main__":
    asyncio.run(main())