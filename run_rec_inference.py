import os
import json
import argparse
import torch
from RecommendModel.bert4rec import BERT4Rec

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_dir",
        type=str,
        required=True,
        help="model directory"
    )

    args = parser.parse_args()
    model_dir = args.model_dir
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    config_path   = os.path.join(model_dir, "config.json")
    token2id_path = os.path.join(model_dir, "token2id.json")
    id2token_path = os.path.join(model_dir, "id2token.json")
    model_path    = os.path.join(model_dir, "bert4rec.pt")


    for p in (config_path, token2id_path, id2token_path, model_path):
        if not os.path.exists(p):
            raise FileNotFoundError(f"필요한 파일이 없습니다: {p}")

    config   = load_json(config_path)
    token2id = load_json(token2id_path)
    id2token = load_json(id2token_path)

    model_bert = BERT4Rec(config)
    model_bert.to(device)

    state_dict = torch.load(model_path, map_location=device)

    model_bert.load_state_dict(state_dict)
    model_bert.eval()

    max_len       = config["max_seq_length"]
    mask_token_id = token2id["[MASK]"]

    # 예시 시퀀스 몇 개 (길이가 0인 경우도 있음)
    random_seqs = [
        ['Python', 'PyTorch', 'CERT_AI', 'CERT_IPE', 'CERT_DATA', 'TensorFlow', 'AWS'],
        ['HTMLCSS'],
        ['HTMLCSS', 'JS', 'CERT_IPE', 'Git', 'React', 'Redux'],
        ['HTMLCSS', 'JS', 'TYPE_Proj|ROLE_FE', 'TYPE_Club|ROLE_FE', 'TYPE_Junior|ROLE_FE', 'TYPE_Intern|ROLE_FE', 'TYPE_Proj|ROLE_UXUI'],
        []
    ]

    with torch.no_grad():
        for idx, seq in enumerate(random_seqs, 1):

            ids = [token2id[t] for t in seq]


            ids = ids[-(max_len - 1):]              # 최대 (max_len - 1) 개만 사용용
            masked_ids = ids + [mask_token_id]      # 마지막 인덱스를 [MASK]

            pad = [0] * (max_len - len(masked_ids))
            input_ids = pad + masked_ids            # 길이 = max_len

            inp = torch.tensor([input_ids], dtype=torch.long, device=device)  # shape=(1, max_len)


            logits = model_bert(inp)  # → shape = (1, max_len, V)

            last_logits = logits[0, max_len - 1].clone() 

            for t_id in set(input_ids):
                if t_id != 0:           
                    last_logits[t_id] = float("-inf")

            topk_ids = torch.topk(last_logits, k=5).indices.tolist()
            topk_tokens = [id2token[str(i)] if isinstance(id2token, dict) and isinstance(next(iter(id2token.keys())), str)
                           else id2token[i]
                           for i in topk_ids]

            print(f"\nTest#{idx}  입력시퀀스: {seq}")
            print(f"추천 Top-5 (중복 제외): {topk_tokens}")
