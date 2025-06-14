# CareerPractice/main.py
import asyncio
from dotenv import load_dotenv

# services 패키지가 CareerPractice/ 내부에 있으므로 상대 import
from services.run_career_practice import CareerPracticeParams, run_career_practice

load_dotenv()

async def main():
    # dummy 1
    #params = CareerPracticeParams(
    #    user_prediction="",
    #    user_history=['Python', 'TYPE_Club|ROLE_BE', 'TYPE_Club|ROLE_DEVOPS'],
    #    user_recommendation=['TYPE_Club|ROLE_AI', 'TYPE_Hackathon|ROLE_AI']
    #)
    # dummy 2
    params = CareerPracticeParams(
        user_prediction="",
        user_history=['Python', 'TYPE_Club|ROLE_BE', 'TYPE_Club|ROLE_DEVOPS'],
        user_recommendation=['TYPE_Proj|ROLE_BE', 'TYPE_Intern|ROLE_AI']
    )
    try:
        result = await run_career_practice(params)
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
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    asyncio.run(main())
