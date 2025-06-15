from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import sys, os
import json
import asyncio
import pandas as pd

# RecommendModel 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'CareerPractice')))
from CareerPrediction.inference.inference import run_inference # 기능 1
from RecommendModel.bert4rec import BERT4Rec # 기능 2
from CareerPractice.services.run_career_practice import CareerPracticeParams, run_career_practice # 기능 3

app = Flask(__name__)
CORS(app)  # 모든 요청 허용

# 기능 2 모델 로드
MODEL_DIR = "../checkpoint_best"

config_path = os.path.join(MODEL_DIR, "config.json")
token2id_path = os.path.join(MODEL_DIR, "token2id.json")
id2token_path = os.path.join(MODEL_DIR, "id2token.json")
model_path = os.path.join(MODEL_DIR, "bert4rec.pt")

for p in (config_path, token2id_path, id2token_path, model_path):
    if not os.path.exists(p):
        raise FileNotFoundError(f"필요한 파일이 없습니다: {p}")

with open(config_path, encoding='utf-8') as f:
    config = json.load(f)
with open(token2id_path, encoding='utf-8') as f:
    token2id = json.load(f)
with open(id2token_path, encoding='utf-8') as f:
    id2token = json.load(f)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_bert = BERT4Rec(config)
model_bert.load_state_dict(torch.load(model_path, map_location=device))
model_bert.to(device)
model_bert.eval()

# 홈 API
@app.route('/')
def home():
    return '''
    <h1>AIP-2 Backend</h1>
    <p>Team2의 백엔드 서버입니다.</p>
    <a href="http://localhost:5173/">NextDev 홈페이지 바로가기</a>
    '''

# 기능1: 커리어 예측 API
@app.route("/feat1", methods=["POST"])
def feature1_inference():
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"error": "입력은 JSON 딕셔너리 형식이어야 합니다."}), 400

        # 추론 실행
        df_result = run_inference(data['tokens'])

        # DataFrame을 JSON으로 변환
        result_json = df_result.to_dict(orient="records")

        return jsonify({
            "input": data,
            "results": result_json
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 기능2: 추천 API
@app.route("/feat2/rec", methods=["POST"])
def recommend_tree():
    try:
        data = request.get_json()
        seq = data.get("sequence", [])
        if not isinstance(seq, list):
            return jsonify({"error": "sequence는 리스트 형식이어야 합니다."}), 400

        def get_top_k(seq_tokens, top_k):
            token_ids = [token2id[t] for t in seq_tokens if t in token2id]
            token_ids = token_ids[-(config["max_seq_length"] - 1):]
            masked_ids = token_ids + [token2id["[MASK]"]]
            pad = [0] * (config["max_seq_length"] - len(masked_ids))
            input_ids = pad + masked_ids
            input_tensor = torch.tensor([input_ids], dtype=torch.long, device=device)

            with torch.no_grad():
                logits = model_bert(input_tensor)
                last_logits = logits[0, config["max_seq_length"] - 1].clone()
                for t_id in set(input_ids):
                    if t_id != 0:
                        last_logits[t_id] = float('-inf')

                topk_ids = torch.topk(last_logits, k=top_k).indices.tolist()
                topk_tokens = [
                    id2token[str(i)] if isinstance(id2token, dict) and isinstance(next(iter(id2token.keys())), str)
                    else id2token[i]
                    for i in topk_ids
                ]
            return topk_tokens

        # 1차 추천 → Top-5 중 Top-3 사용
        top3 = get_top_k(seq, top_k=5)[:3]

        tree = []
        for token in top3:
            new_seq = seq + [token]
            child_tokens = get_top_k(new_seq, top_k=2)
            tree.append({
                "token": token,
                "children": child_tokens
            })

        return jsonify({
            "input_sequence": seq,
            "tree": tree
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 기능 3 : 가이드라인 제시 API
@app.route("/feat3/practice", methods=["POST"])
def feature3_practice():
    try:
        data = request.get_json()
        user_history = data.get("user_history", [])
        user_recommendation = data.get("user_recommendation", [])

        if not isinstance(user_history, list) or not isinstance(user_recommendation, list):
            return jsonify({"error": "user_history와 user_recommendation은 리스트여야 합니다."}), 400

        # 파라미터 준비
        params = CareerPracticeParams(
            user_history=user_history,
            user_recommendation=user_recommendation
        )

        # 비동기 실행
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_career_practice(params))

        return jsonify(result.model_dump())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)