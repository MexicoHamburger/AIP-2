import json
import re
from pathlib import Path

SKILL_TAIL = re.compile(r"\|SKILL_[^|]+$")

def strip_skill(token: str) -> str:
    """TYPE_* 토큰에서 |SKILL_?? 뒤를 잘라낸다."""
    if token.startswith("TYPE_"):
        return SKILL_TAIL.sub("", token)
    return token

def dedup_consecutive(tokens):
    """연속 중복을 제거한다(순서 유지·첫 항목 보존)."""
    cleaned = []
    prev = object()          # 절대 일치하지 않을 센티넬
    for tok in tokens:
        if tok != prev:
            cleaned.append(tok)
            prev = tok
    return cleaned

def process_file(src: str = "result.json", dst: str = "result_clean.json"):
    with open(src, encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        seq = entry.get("token_sequence", [])
        seq = [strip_skill(tok) for tok in seq]   # 1) SKILL 절단
        seq = dedup_consecutive(seq)              # 2) 연속 중복 제거
        entry["token_sequence"] = seq

    with open(dst, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    process_file()      # 기본: 같은 폴더의 result.json → result_clean.json
