#CareerPractice/services/run_career_practice.py

import asyncio
import json
from pydantic import BaseModel, Field, TypeAdapter
from typing import List, Dict, Tuple
import os, sys
from dotenv import load_dotenv
load_dotenv() 

from langchain_openai import ChatOpenAI
from openai import OpenAI
from pinecone.grpc import PineconeGRPC as Pinecone
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from prompts.career_practice_prompts import CareerPracticePrompt

LLM_REASONING_MODEL = "o4-mini-2025-04-16"
EMBED_MODEL = "text-embedding-3-small"
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
_index = pc.Index("careerpractice-index")
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


class CareerPracticeParams(BaseModel):
    # 성능 저하 및 추천 모델 결과와의 충돌 발생으로 제외, 사용자의 경력을 llm에 넣기 때문에 필요 없다 판단.
    #user_prediction: str = Field(
    #    description="사용자의 커리어 경력 예측 내용 문자열입니다."
    #)
    user_history: List[str] = Field(description="사용자의 이력 토큰입니다.")
    user_recommendation: List[str] = Field(description="사용자의 이력 추천 토큰입니다.")


class PracticeItem(BaseModel):
    category: str = Field(description="커리어 활동의 구분입니다.")
    name: str = Field(..., description="커리어 활동의 이름입니다.")
    reason: str = Field(
        ..., description="커리어 활동을 추천한 이유를 2줄 내로 간략하게 제시합니다."
    )
    fields: List[str] = Field(
        description="커리어 활동과 관련한 분야들을 리스트 형식으로 작성합니다."
    )
    skills: List[str] = Field(
        description="커리어 활동과 관련한 스킬, 기술 스텍, 툴 들을 리스트 형식으로 작성합니다."
    )
    description: str = Field(
        description="커리어 활동에 대한 설명을 2줄 내로 간략하게 제시합니다."
    )
    link: str = Field(..., description="관련 활동의 URL")


class CareerPracticeResponse(BaseModel):
    title: str = Field(description="커리어 실천 전략 제목")
    practice_items: dict[str, PracticeItem] = Field(
        description="스텝 별 커리어 실천 활동들입니다.",
    )
    total_reason: str = Field(
        description="전체 커리어 활동의 요약 및 제안 사항을 2줄 내로 제시합니다."
    )


class PracticeQueryItem(BaseModel):
    step: str = Field(description="step + 숫자를 작성합니다. 예시) step1, step2, ...")
    category: str = Field(description="해당 경력의 카테고리를 작성합니다.")
    practice_query: str = Field(description="해당 step의 질의 쿼리를 작성합니다.")


class PracticeQueryGenerationResponse(BaseModel):
    success: bool
    queries: List[PracticeQueryItem]
    message: str | None = None

class ReasonResponse(BaseModel):
    title: str = Field(description="커리어 실천 제목을 작성합니다.")
    reason: str = Field(
        ..., description="커리어 실천 도우미로 실천 가이드라인을 제공하며 고려한 점을 작성합니다."
    )


async def _generate_practice_queries(
    params: CareerPracticeParams,
) -> PracticeQueryGenerationResponse:
    parser = JsonOutputParser(pydantic_object=PracticeQueryGenerationResponse)
    prompt = PromptTemplate(
        template=CareerPracticePrompt.MAKE_PRACTICE_QUERY_PROMPT.value,
        input_variables=["parts_summary", "user_prompt"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
        },
    )
    variables = {
        "user_history": params.user_history,
        "user_recommendation": params.user_recommendation,
    }
    chain = (
        prompt
        | ChatOpenAI(
            model=LLM_REASONING_MODEL,
            api_key=openai_api_key,
        )
        | parser
    )
    result = await chain.ainvoke(variables)

    return PracticeQueryGenerationResponse.model_validate(result)


def _retrieve_candidates(query: str, category: str) -> list[dict]:
    try:
        vec = client.embeddings.create(input=query, model=EMBED_MODEL, dimensions=512).data[0].embedding
        K = 3
        search_res = _index.query(
            vector=vec,
            top_k=K,
            include_metadata=True,
            filter={
                "category": category,
            },
        )
    except Exception as e:
        import traceback, sys
        traceback.print_exc()
        sys.exit(1)
    if not search_res["matches"]:
        return []
    return search_res["matches"]


# 후보 텍스트 중 필수만 변환
def _candidates_to_str_summary(matches: list[dict]) -> str:
    return "\n".join(
        [
            f"category: {m['metadata']['category']} | "
            f"name: {m['metadata']['name']} | "
            f"link: ₩{m['metadata']['link']} | "
            f"field: ₩{m['metadata']['field']} | "
            f"skills: ₩{m['metadata']['skills']} | "
            f"description: {m['metadata']['description']} | "
            for m in matches
        ]
    )

def serialize_selected_items(selected_items: Dict[str, PracticeItem]) -> str:
    # Pydantic 모델들을 dict로 변환
    serialized_dict = {key: item.model_dump() for key, item in selected_items.items()}
    # JSON 문자열로 변환 (indent 옵션은 보기 좋게 출력, 필요없으면 삭제)
    json_string = json.dumps(serialized_dict, ensure_ascii=False, indent=2)
    return json_string

async def _select_part(
    category: str, practice_query: str, candidates_str: str, selected_items: Dict[str, PracticeItem]
) -> PracticeItem:
    selected_items_str = serialize_selected_items(selected_items)
    parser = JsonOutputParser(pydantic_object=PracticeItem)
    llm = ChatOpenAI(
        model="gpt-4.1-2025-04-14",
        api_key=openai_api_key,
    )
    prompt = PromptTemplate(
        template=CareerPracticePrompt.RAG_PROMPT.value,
        input_variables=["practice_query", "candidates", "selected_items_str"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
        },
    )
    chain = prompt | llm | parser
    try:
        part_raw = await chain.ainvoke(
            {
                "practice_query": practice_query,
                "candidates": candidates_str,
                "selected_items_str": selected_items_str
            }
        )
    except Exception as e:
        print("llm search error")
        sys.exit(1)
    try:
        return PracticeItem.model_validate(part_raw)
    except Exception as e:
        sys.exit(1)


# 부품 업그레이드 과정 설명을 제작하는 함수
async def _generate_upgrade_reason(
    selected_items: Dict[str, PracticeItem],
    params: CareerPracticeParams,
) -> Tuple[str, str]:

    selected_items_str = serialize_selected_items(selected_items)
    parser = JsonOutputParser(pydantic_object=ReasonResponse)
    prompt = PromptTemplate(
        template=CareerPracticePrompt.REASON_PROMPT.value,
        input_variables=["user_history", "user_recommendation", "career_practice"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
        },
    )
    chain = (
        prompt
        | ChatOpenAI(
            model="gpt-4.1-2025-04-14",
            api_key=openai_api_key,
        )
        | parser
    )
    result = await chain.ainvoke(
        {
            "user_history": params.user_history,
            "user_recommendation": params.user_recommendation,
            "career_practice": selected_items_str,
        }
    )
    parsed_result = TypeAdapter(ReasonResponse).validate_python(result)
    return parsed_result.title, parsed_result.reason

async def _select_part_web_search(
    category: str, practice_query: str
) -> PracticeItem:
    parser = JsonOutputParser(pydantic_object=PracticeItem)
    llm = ChatOpenAI(
        model="gpt-4.1-2025-04-14",
        api_key=openai_api_key,
        model_kwargs={
            "tools": [{"type": "web_search"}],
            "tool_choice": {"type": "web_search"},
        },
    )
    prompt = PromptTemplate(
        template=CareerPracticePrompt.WEB_SEARCH_PROMPT.value,
        input_variables=["practice_query", "category"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
        },
    )
    chain = prompt | llm | parser
    try:
        part_raw = await chain.ainvoke(
            {
                "practice_query": practice_query,
                "category": category,
            }
        )
    except Exception as e:
        print("llm search error")
        sys.exit(1)
    try:
        return PracticeItem.model_validate(part_raw)
    except Exception as e:
        sys.exit(1)


# == main pipeline == #
async def run_career_practice(params: CareerPracticeParams) -> CareerPracticeResponse:
    # Step 1) 스텝 별 쿼리 생성
    query_resp = await _generate_practice_queries(params)
    if not query_resp.success:
        raise ValueError(query_resp.message or "쿼리 생성 실패")

    selected_items: Dict[str, PracticeItem] = {}

    # Step 2) 스텝 별 쿼리로 item fetch
    for query_item in query_resp.queries:
        category, practice_query, step = (
            query_item.category,
            query_item.practice_query,
            query_item.step,
        )
        print(category, practice_query)
        if category == "language" or category == "project" or category == "etc":
            part =  await _select_part_web_search(category, practice_query)
            selected_items[step] = part
            continue

        # 2-2) 벡터 검색 및 후보군 생성
        matches = _retrieve_candidates(
            practice_query,
            category,
        )

        candidates_str = _candidates_to_str_summary(matches)

        # 2-3. 단일 item 선택 (LLM 사용)
        part = await _select_part(category, practice_query, candidates_str, selected_items)
        if not part.name or str(part.name).strip().lower() in ["none", "null", ""]:
            print(f"[{category}] 선택된 아이템 없음.")
            selected_items[step] = PracticeItem(
                category=category,
                name="",
                reason="",
                fields=[""],
                skills=[""],
                description="",
                link="",
            )
            continue

        # 2-4) 기존 부품 덮어쓰기
        selected_items[step] = part

    # Step 3) 커리어 실천 제목과 이유 생성
    title, total_reason = await _generate_upgrade_reason(
        selected_items, params
    )

    return CareerPracticeResponse(
        title=title,
        practice_items=selected_items,
        total_reason=total_reason
    )