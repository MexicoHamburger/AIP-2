import pandas as pd

# 파일명 설정
input_csv = "survey_2023.csv"
output_csv = "filtered_results.csv"

# 최종적으로 남기고 싶은 컬럼 목록
columns_to_keep = [
    "LanguageHaveWorkedWith",
    "DatabaseHaveWorkedWith",
    "PlatformHaveWorkedWith",
    "WebframeHaveWorkedWith",
    "EmbeddedHaveWorkedWith",  # 이 컬럼이 없어도 빈 값으로 추가될 예정
    "MiscTechHaveWorkedWith",
    "DevType",
    "Currency",
    "CompTotal",
    "Industry"
]

# 실제 CSV에서 존재하는 컬럼만 선택
df = pd.read_csv(input_csv)

# 누락된 컬럼 파악
missing_columns = [col for col in columns_to_keep if col not in df.columns]

# 누락된 컬럼은 빈 값으로 추가
for col in missing_columns:
    df[col] = ""

# 컬럼 순서 맞춰서 재정렬 (원하는 순서대로 저장)
df = df[columns_to_keep]

# 저장
df.to_csv(output_csv, index=False)

print(f"✅ 누락 컬럼은 빈 값으로 추가하고, 원하는 컬럼만 저장 완료: {output_csv}")
