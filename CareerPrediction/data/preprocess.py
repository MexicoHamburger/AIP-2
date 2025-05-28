import pandas as pd
from collections import Counter

# 파일명
csv_file = "survey_results_public_2024.csv"
output_csv = "SODC_2024.csv"
summary_txt = "field_summary.txt"

# 허용할 DevType 목록
allowed_devtypes = [
    "Academic researcher", "Blockchain", "Cloud infrastructure engineer", "Data engineer",
    "Data scientist or machine learning specialist", "Developer, AI", "Developer, back-end",
    "Developer, embedded applications or devices", "Developer, front-end", "Developer, full-stack",
    "Developer, game or graphics", "Developer, mobile", "DevOps specialist", "Engineering manager",
    "Hardware Engineer", "Product manager", "Security professional"
]

# 다중 필드 목록
multi_valued_columns = [
    "LanguageHaveWorkedWith", "LanguageWantToWorkWith",
    "DatabaseHaveWorkedWith", "DatabaseWantToWorkWith",
    "PlatformHaveWorkedWith", "PlatformWantToWorkWith",
    "WebframeHaveWorkedWith", "WebframeWantToWorkWith",
    "EmbeddedHaveWorkedWith", "EmbeddedWantToWorkWith",
    "MiscTechHaveWorkedWith", "MiscTechWantToWorkWith",
    "ToolsTechHaveWorkedWith", "ToolsTechWantToWorkWith",
    "AISearchDevHaveWorkedWith", "AISearchDevWantToWorkWith",
    "ProfessionalTech", "ProfessionalCloud"
]

# 출력 순서
ordered_columns = [
    "DevType", "Currency", "CompTotal",
    "LanguageHaveWorkedWith", "LanguageWantToWorkWith",
    "DatabaseHaveWorkedWith", "DatabaseWantToWorkWith",
    "PlatformHaveWorkedWith", "PlatformWantToWorkWith",
    "WebframeHaveWorkedWith", "WebframeWantToWorkWith", 
    "EmbeddedHaveWorkedWith", "EmbeddedWantToWorkWith",
    "MiscTechHaveWorkedWith", "MiscTechWantToWorkWith",
    "ToolsTechHaveWorkedWith", "ToolsTechWantToWorkWith",
    "AISearchDevHaveWorkedWith", "AISearchDevWantToWorkWith",
    "ProfessionalTech", "ProfessionalCloud", "ProfessionalQuestion",
    "Industry", "JobSat"
]

# 필터링된 산업군
allowed_industries = [
    "Software Development", "Computer Systems Design and Services", "Internet, Telecomm or Information Services", "Fintech", "Energy", "Government",
    "Banking/Financial Services", "Manufacturing", "Transportation, or Supply Chain", "Healthcare", "Retail and Consumer Services", "Higher Education",
    "Media & Advertising Services", "Insurance", "Advertising Services", "Business Consulting and Services", "Construction", "Financial Services",
    "Government Administration", "Information Services, IT, Software Development, or other Technology", "Legal Services",
    "Manufacturing, Transportation, or Supply Chain", "Non-profit Organizations", "Oil & Gas", "Telecommunications, Media, and Entertainment", "Wholesale"
]

# 환율 테이블 (생략 가능)
exchange_rates = {"USD": 1370.0, "KRW": 1.0, "EUR": 1500.0, "JPY": 9.6, "GBP": 1700.0, "INR": 16.0, "CNY": 190.0}  # 예시 환율만 남김

# ✅ 다중 필드 필터링 함수 (빈도 기반 + 허용 항목 반환)
def filter_by_frequency(df, column_name, min_count=1000, log_file=None):
    # 전체 항목 분해 후 개별 요소 카운트
    all_values = df[column_name].dropna().str.split(";").sum()
    value_counts = Counter(v.strip() for v in all_values if v.strip() != "")

    # 포함/제거 기준 적용
    allowed = {k for k, v in value_counts.items() if v >= min_count}
    removed = {k for k in value_counts if k not in allowed}

    # 필터링 함수 정의
    def keep_only_frequent(value):
        if pd.isna(value):
            return ""
        parts = [v.strip() for v in value.split(";")]
        filtered = [v for v in parts if v in allowed]
        return ";".join(filtered)

    # 적용
    df[column_name] = df[column_name].apply(keep_only_frequent)

    # 로그 작성
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[📌 Column: {column_name}]\n")
            f.write(f"✅ 포함된 값 ({len(allowed)}개):\n")
            f.write(", ".join(sorted(allowed)) + "\n")
            f.write(f"❌ 제거된 값 ({len(removed)}개):\n")
            f.write(", ".join(sorted(removed)) + "\n\n")

    return df, allowed


# ✅ 데이터 전처리 시작
df = pd.read_csv(csv_file)

# DevType 필터링
df = df[df["DevType"].notna() & (df["DevType"].str.strip() != "")]
pattern = '|'.join([f"\\b{d}\\b" for d in allowed_devtypes])
df = df[df["DevType"].str.contains(pattern, case=False, na=False, regex=True)]

# 결측 제거
df = df.dropna(subset=["CompTotal", "Currency", "JobSat"])

# Currency 앞 3자리
df["Currency"] = df["Currency"].str.replace(r'\s{2,}', ' ', regex=True)
df["Currency"] = df["Currency"].str.slice(0, 3)

# 필드 필터링 및 allowed 항목 저장
with open(summary_txt, "w", encoding="utf-8") as f:
    for col in multi_valued_columns:
        if col in df.columns:
            df, allowed = filter_by_frequency(df, col, min_count=1000)
            f.write(f"[{col}]\n")
            for item in sorted(allowed):
                f.write(f"- {item}\n")
            f.write("\n")

# 컬럼 순서 정리
for col in ordered_columns:
    if col not in df.columns:
        df[col] = ""
df = df[ordered_columns]

# 환산
df["CompTotal"] = pd.to_numeric(df["CompTotal"], errors="coerce")
df["CompTotal"] = df.apply(
    lambda row: row["CompTotal"] * exchange_rates.get(row["Currency"], None)
    if pd.notnull(row["CompTotal"]) and row["Currency"] in exchange_rates
    else None,
    axis=1
)
df.drop(columns=["Currency"], inplace=True)

# 산업군 정리
df["Industry"] = df["Industry"].apply(lambda x: x if x in allowed_industries else "")
df["ProfessionalQuestion"] = df["ProfessionalQuestion"].fillna("")

# 저장
df.to_csv(output_csv, index=False)
print("✅ 전처리 완료 →", output_csv)
print("📄 필터된 항목 리스트 저장 →", summary_txt)
