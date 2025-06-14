import requests

# Flask 서버 주소 (포트는 실제 서버 실행 상태에 따라 수정)
URL = "http://localhost:5000/feat2/rec"

# 테스트할 입력 시퀀스
input_sequence = ["HTMLCSS", "JS", "CERT_IPE", "Git", "React", "Redux"]

# 요청 본문 데이터
payload = {
    "sequence": input_sequence
}

# POST 요청
response = requests.post(URL, json=payload)

# 결과 출력
if response.status_code == 200:
    result = response.json()
    print("✅ 추천 트리 결과:")
    print("입력 시퀀스:", result["input_sequence"])
    for i, node in enumerate(result["tree"], 1):
        print(f"  추천{i}: {node['token']} → {node['children']}")
else:
    print("❌ 에러 발생:", response.status_code, response.text)