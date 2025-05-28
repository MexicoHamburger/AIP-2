import pandas as pd
from collections import Counter

# 파일명
csv_file = "source.csv"
output_csv = "dest.csv"

# 허용할 DevType 목록
allowed_devtypes = [
    "Academic researcher", "Blockchain", "Cloud infrastructure engineer", "Data engineer",
    "Data scientist or machine learning specialist", "Developer, AI", "Developer, back-end",
    "Developer, embedded applications or devices", "Developer, front-end", "Developer, full-stack",
    "Developer, game or graphics", "Developer, mobile", "DevOps specialist", "Engineering manager",
    "Hardware Engineer", "Product manager", "Security professional"
]

# 원하는 컬럼 순서
ordered_columns = [
    "DevType", "Currency", "CompTotal",
    "LanguageHaveWorkedWith", "DatabaseHaveWorkedWith", "PlatformHaveWorkedWith",
    "WebframeHaveWorkedWith", "EmbeddedHaveWorkedWith", "MiscTechHaveWorkedWith", "Industry"
]

allowed_industries = ["Software Development", "Computer Systems Design and Services", "Internet, Telecomm or Information Services", "Fintech", "Energy", "Government", "Banking/Financial Services", "Manufacturing", "Transportation, or Supply Chain", "Healthcare", "Retail and Consumer Services", "Higher Education", "Media & Advertising Services", "Insurance", "Advertising Services", "Business Consulting and Services", "Construction", "Financial Services", "Government Administration", "Information Services, IT, Software Development, or other Technology", "Legal Services", "Manufacturing, Transportation, or Supply Chain", "Non-profit Organizations", "Oil & Gas", "Telecommunications, Media, and Entertainment", "Wholesale"]

# ✅ 공통 다중 필드 필터링 함수 (빈도 기반)
def filter_by_frequency(df, column_name, min_count=1000):
    # 전체 항목 분해 후 개별 요소 카운트
    all_values = df[column_name].dropna().str.split(";").sum()
    value_counts = Counter(v.strip() for v in all_values if v.strip() != "")

    # 1000개 이상 등장한 값만 허용
    allowed = {k for k, v in value_counts.items() if v >= min_count}

    # 필터링 함수 정의
    def keep_only_frequent(value):
        if pd.isna(value):
            return ""
        parts = [v.strip() for v in value.split(";")]
        filtered = [v for v in parts if v in allowed]
        return ";".join(filtered)

    # 적용
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

# 5️⃣ 다중 필드 빈도 기반 필터링
multi_valued_columns = [
    "LanguageHaveWorkedWith",
    "DatabaseHaveWorkedWith",
    "PlatformHaveWorkedWith",
    "WebframeHaveWorkedWith",
    "EmbeddedHaveWorkedWith",
    "MiscTechHaveWorkedWith"
]

for col in multi_valued_columns:
    if col in df.columns:
        df = filter_by_frequency(df, col, min_count=1000)

# 6️⃣ 컬럼 순서 정렬 (없는 컬럼은 빈 값으로 추가)
for col in ordered_columns:
    if col not in df.columns:
        df[col] = ""
df = df[ordered_columns]

df["CompTotal"] = pd.to_numeric(df["CompTotal"], errors="coerce")

# 환율 테이블
exchange_rates = {
    "AED": 370.0,
    "AFN": 15.0,
    "ALL": 13.0,
    "AMD": 3.5,
    "ANG": 760.0,
    "AOA": 1.5,
    "ARS": 1.6,
    "AUD": 890.0,
    "AWG": 760.0,
    "AZN": 800.0,
    "BAM": 850.0,
    "BDT": 12.5,
    "BGN": 850.0,
    "BHD": 3600.0,
    "BIF": 0.7,
    "BND": 1000.0,
    "BOB": 200.0,
    "BRL": 270.0,
    "BSD": 1370.0,
    "BTN": 16.0,
    "BYN": 550.0,
    "BZD": 685.0,
    "CAD": 1000.0,
    "CDF": 0.7,
    "CHF": 1500.0,
    "CLP": 1.5,
    "CNY": 190.0,
    "COP": 0.35,
    "CRC": 2.5,
    "CUP": 55.0,
    "CVE": 14.0,
    "CZK": 60.0,
    "DKK": 220.0,
    "DOP": 24.0,
    "DZD": 10.0,
    "EGP": 45.0,
    "ETB": 25.0,
    "EUR": 1500.0,
    "FJD": 620.0,
    "GBP": 1700.0,
    "GEL": 500.0,
    "GGP": 1700.0,
    "GHS": 120.0,
    "GIP": 1700.0,
    "GTQ": 175.0,
    "GYD": 6.5,
    "HKD": 175.0,
    "HNL": 55.0,
    "HRK": 200.0,
    "HUF": 4.0,
    "IDR": 0.09,
    "ILS": 380.0,
    "IMP": 1700.0,
    "INR": 16.0,
    "IQD": 1.0,
    "IRR": 0.03,
    "ISK": 10.0,
    "JMD": 9.0,
    "JOD": 1930.0,
    "JPY": 9.6,
    "KES": 10.0,
    "KGS": 15.0,
    "KHR": 0.33,
    "KRW": 1.0,
    "KWD": 4500.0,
    "KZT": 3.0,
    "LBP": 0.09,
    "LKR": 4.5,
    "LSL": 75.0,
    "LYD": 280.0,
    "MAD": 150.0,
    "MDL": 80.0,
    "MGA": 0.3,
    "MKD": 24.0,
    "MMK": 0.65,
    "MNT": 0.4,
    "MOP": 170.0,
    "MRU": 36.0,
    "MUR": 30.0,
    "MVR": 90.0,
    "MWK": 1.0,
    "MXN": 80.0,
    "MYR": 310.0,
    "MZN": 22.0,
    "NAD": 75.0,
    "NGN": 1.5,
    "NIO": 38.0,
    "NOK": 130.0,
    "NPR": 10.0,
    "NZD": 830.0,
    "OMR": 3550.0,
    "PEN": 360.0,
    "PHP": 24.0,
    "PKR": 5.0,
    "PLN": 350.0,
    "PYG": 0.19,
    "QAR": 375.0,
    "RON": 300.0,
    "RSD": 13.0,
    "RUB": 15.0,
    "RWF": 1.2,
    "SAR": 365.0,
    "SEK": 130.0,
    "SGD": 1010.0,
    "SLL": 0.07,
    "SOS": 2.4,
    "SRD": 37.0,
    "SYP": 0.55,
    "SZL": 75.0,
    "THB": 38.0,
    "TJS": 125.0,
    "TMT": 390.0,
    "TND": 440.0,
    "TRY": 45.0,
    "TTD": 200.0,
    "TWD": 44.0,
    "TZS": 0.55,
    "UAH": 35.0,
    "UGX": 0.35,
    "USD": 1370.0,
    "UYU": 33.0,
    "UZS": 0.11,
    "VES": 0.04,
    "VND": 0.056,
    "WST": 500.0,
    "XAF": 2.3,
    "XDR": 1800.0,
    "XOF": 2.3,
    "XPF": 13.0,
    "YER": 5.5,
    "ZAR": 75.0,
    "ZMW": 80.0
}

# CompTotal을 KRW로 환산하여 저장
df["CompTotal"] = df.apply(
    lambda row: row["CompTotal"] * exchange_rates.get(row["Currency"], None)
    if pd.notnull(row["CompTotal"]) and row["Currency"] in exchange_rates
    else None,
    axis=1
)

df.drop(columns=["Currency"], inplace=True)

# 6️⃣ Industry 필터링: 허용된 값이 아니면 공백 처리 (행은 유지)
df["Industry"] = df["Industry"].apply(lambda x: x if x in allowed_industries else "")

# 7️⃣ 저장
df.to_csv(output_csv, index=False)

print("byoooooooo")
print(f"✅ 1000회 미만 항목 제거 포함 최종 전처리 완료 → {output_csv}")
