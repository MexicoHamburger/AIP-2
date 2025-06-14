import requests
import json

# Flask 서버 주소 (포트 번호는 실제 실행 환경에 맞게 조정)
URL = "http://localhost:5000/feat3/practice"

# 예시 입력 데이터
payload = {
    "user_history": [
        "Python", "TensorFlow", "Keras", "AWS", "CERT_DATA",
        "TYPE_Intern|ROLE_AI", "TYPE_Junior|ROLE_AI"
    ],
    "user_recommendation": [
        "TYPE_StartUp|ROLE_AI", "TYPE_StartUp|ROLE_DEVOPS"
    ]
}

# API 요청
response = requests.post(URL, json=payload)

# 응답 출력
if response.status_code == 200:
    result = response.json()
    print("✅ 기능3 API 테스트 성공!")
    print(f"\n📌 Title: {result.get('title')}\n")
    for step, item in result.get("practice_items", {}).items():
        print(f"🔹 Step: {step}")
        print(f"  - Category   : {item.get('category')}")
        print(f"  - Name       : {item.get('name')}")
        print(f"  - Reason     : {item.get('reason')}")
        print(f"  - Fields     : {', '.join(item.get('fields', []))}")
        print(f"  - Skills     : {', '.join(item.get('skills', []))}")
        print(f"  - Description: {item.get('description')}")
        print(f"  - Link       : {item.get('link')}\n")
    print(f"📝 Total Reason: {result.get('total_reason')}")
else:
    print("❌ 기능3 API 요청 실패")
    print("상태코드:", response.status_code)
    print("응답내용:", response.text)
