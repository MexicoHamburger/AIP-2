# CareerPractice/main.py
import asyncio
import json
from dotenv import load_dotenv
from pathlib import Path

# services 패키지가 CareerPractice/ 내부에 있으므로 상대 import
from services.run_career_practice import CareerPracticeParams, run_career_practice

load_dotenv()

async def main():
    # dummy 2 (현재 사용중인 예시)
    params = CareerPracticeParams(
        user_history = ['Python', 'TensorFlow', 'Keras', 'AWS', 'CERT_DATA', 'TYPE_Intern|ROLE_AI', 'TYPE_Junior|ROLE_AI'],
        user_recommendation = ['TYPE_StartUp|ROLE_AI', 'TYPE_StartUp|ROLE_DEVOPS']
    )
    try:
        result = await run_career_practice(params)

        # 결과 출력
        print("===== Career Practice Result =====")
        print(f"Title: {result.title}\n")
        for step, item in result.practice_items.items():
            print(f"\nStep: {step}")
            print(f"  Category:   {item.category}")
            print(f"  Name:       {item.name}")
            print(f"  Reason:     {item.reason}")
            print(f"  Fields:     {item.fields}")
            print(f"  Skills:     {item.skills}")
            print(f"  Description:{item.description}")
            print(f"  Link:       {item.link}")
        print(f"\nTotal Reason: {result.total_reason}")

        # 결과를 JSON으로 저장
        output_path = Path("career_practice_result.json")
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(result.model_dump(), f, ensure_ascii=False, indent=2)

        print(f"\n결과가 {output_path} 에 저장되었습니다.")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    asyncio.run(main())
