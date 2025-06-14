import requests
import json

# Flask 서버 주소 (필요 시 localhost 외 다른 주소로 수정)
URL = "http://localhost:5000/feat1"

# 예시 입력 데이터
input_data = {
    "LanguageHaveWorkedWith": ["C"],
    "DatabaseHaveWorkedWith": [],
    "PlatformHaveWorkedWith": [],
    "WebframeHaveWorkedWith": ["FastAPI"],
    "EmbeddedHaveWorkedWith": ["GNU GCC"],
    "MiscTechHaveWorkedWith": ["Torch/PyTorch"],
    "ToolsTechHaveWorkedWith": [],
    "ProfessionalTech": []
}

# POST 요청 전송
response = requests.post(URL, json=input_data)

# 응답 처리
if response.status_code == 200:
    result = response.json()
    print("✅ 기능1 API 테스트 성공!")
    print("입력 정보:")
    print(json.dumps(result["input"], ensure_ascii=False, indent=2))
    print("\n추천 결과:")
    for idx, row in enumerate(result["results"], 1):
        print(f"\n🔹 추천 {idx}")
        for key, value in row.items():
            print(f"  {key}: {value}")
else:
    print("❌ 오류 발생:", response.status_code)
    print(response.text)