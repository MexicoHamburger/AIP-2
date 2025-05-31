import json
import re
from glob import glob
from pathlib import Path

def natural_key(path: str):
    """
    'result10.json' 같은 이름이 사전식이 아닌
    숫자 기반 '자연 정렬'이 되도록 키를 반환합니다.
    """
    filename = Path(path).name
    # 'result', '10', '.json' 처럼 분리 → 숫자는 int로 변환
    return [int(tok) if tok.isdigit() else tok.lower()
            for tok in re.split(r'(\d+)', filename)]

def merge_results(pattern: str = "result*.json",
                  dst: str = "result.json"):
    """
    `pattern`에 맞는 모든 JSON 파일을 자연 정렬한 뒤 합쳐
    `dst` 파일로 저장합니다.
    """
    files = sorted(glob(pattern), key=natural_key)
    if not files:
        raise FileNotFoundError(f"No files match pattern '{pattern}'")

    merged = []
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            data = json.load(f)

        # 각 파일이 리스트인지(권장)·단일 dict인지 모두 지원
        if isinstance(data, list):
            merged.extend(data)
        else:
            merged.append(data)

    with open(dst, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"Merged {len(files)} files → '{dst}' "
          f"({len(merged)} total records)")

if __name__ == "__main__":
    # 기본값: 현재 폴더의 result*.json → result.json
    merge_results()
