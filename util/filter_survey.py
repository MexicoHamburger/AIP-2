import pandas as pd
from collections import Counter

# 파일명
csv_file = "test.csv"
output_csv = "test.csv"

# 허용할 DevType 목록
allowed_devtypes = [
    "Academic researcher", "Blockchain", "Cloud infrastructure engineer", "Data engineer",
    "Data scientist or machine learning specialist", "Developer, AI", "Developer, back-end",
    "Developer, embedded applications or devices", "Developer, front-end", "Developer, full-stack",
    "Developer, game or graphics", "Developer, mobile", "DevOps specialist", "Engineering manager",
    "Hardware Engineer", "Product manager", "Security professional"
]

# Industry 허용 목록
allowed_industries = [
    "Software Development", "Computer Systems Design and Services", "Internet, Telecomm or Information Services", 
    "Fintech", "Energy", "Government", "Banking/Financial Services", "Manufacturing", "Transportation, or Supply Chain", 
    "Healthcare", "Retail and Consumer Services", "Higher Education", "Media & Advertising Services", "Insurance", "Advertising Services", 
    "Business Consulting and Services", "Construction", "Financial Services", "Government Administration", 
    "Information Services, IT, Software Development, or other Technology", 
    "Legal Services", "Manufacturing, Transportation, or Supply Chain", "Non-profit Organizations", 
    "Oil & Gas", "Telecommunications, Media, and Entertainment", "Wholesale"]


# 원하는 컬럼 순서
ordered_columns = [
    "DevType", "Currency", "CompTotal",
    "LanguageHaveWorkedWith", "DatabaseHaveWorkedWith", "PlatformHaveWorkedWith",
    "WebframeHaveWorkedWith", "EmbeddedHaveWorkedWith", "MiscTechHaveWorkedWith", "Industry"
]

# ✅ 공통 다중 필드 필터링 함수 (주석 처리됨 - 사용 안함)
def filter_by_frequency(df, column_name, min_count=1000):
    all_values = df[column_name].dropna().str.split(";").sum()
    value_counts = Counter(v.strip() for v in all_values if v.strip() != "")
    allowed = {k for k, v in value_counts.items() if v >= min_count}
    def keep_only_frequent(value):
        if pd.isna(value):
            return ""
        parts = [v.strip() for v in value.split(";")]
        filtered = [v for v in parts if v in allowed]
        return ";".join(filtered)
    df[column_name] = df[column_name].apply(keep_only_frequent)
    return df

# 1️⃣ CSV 불러오기
df = pd.read_csv(csv_file)

# 2️⃣ DevType 필터링
df = df[df["DevType"].notna() & (df["DevType"].str.strip() != "")]
pattern = '|'.join([f"\\b{d}\\b" for d in allowed_devtypes])
df = df[df["DevType"].str.contains(pattern, case=False, na=False, regex=True)]

# 3️⃣ CompTotal, Currency 결측치 제거
df = df.dropna(subset=["CompTotal", "Currency"])

# 4️⃣ Currency 앞 3글자만 남기기
df["Currency"] = df["Currency"].str.replace(r'\s{2,}', ' ', regex=True)
df["Currency"] = df["Currency"].str.slice(0, 3)

# 5️⃣ 다중 필드 필터링 (주석 처리)
# multi_valued_columns = [
#     "LanguageHaveWorkedWith",
#     "DatabaseHaveWorkedWith",
#     "PlatformHaveWorkedWith",
#     "WebframeHaveWorkedWith",
#     "EmbeddedHaveWorkedWith",
#     "MiscTechHaveWorkedWith"
# ]
# for col in multi_valued_columns:
#     if col in df.columns:
#         df = filter_by_frequency(df, col, min_count=1000)

# 6️⃣ Industry 필터링
df["Industry"] = df["Industry"].apply(lambda x: x if x in allowed_industries else "")

# 7️⃣ 컬럼 순서 정렬 (없는 컬럼은 빈 값으로 추가)
for col in ordered_columns:
    if col not in df.columns:
        df[col] = ""
df = df[ordered_columns]

# 8️⃣ 저장
df.to_csv(output_csv, index=False)

print("byoooooooo")
print(f"✅ Industry 필터링 완료 → {output_csv}")
