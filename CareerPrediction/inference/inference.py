# inference.py ─────────────────────────────────────────────
import os, pickle, joblib
import numpy as np, pandas as pd, torch
from typing import Dict, List

# ───────────────── 1. 하이퍼파라미터 & 경로 ────────────────
DEVICE   = "cuda" if torch.cuda.is_available() else "cpu"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 기준 경로

PT_PATH        = os.path.join(BASE_DIR, "best_model_silvery-sweep-1.pt")
RAW_PATH       = os.path.join(BASE_DIR, "raw.pkl")
TOK_HAVE_PATH  = os.path.join(BASE_DIR, "tokenizer_have.pkl")
TOK_WANT_PATH  = os.path.join(BASE_DIR, "tokenizer_want.pkl")
SCALER_PATH    = os.path.join(BASE_DIR, "scaler.pkl")

EMBED_DIM = 128
DEPTH     = 8
DROPOUT   = 0.3
TOP_K     = 3
THRESHOLD = 2

# ───────────────── 2. 모델 아키텍처 정의 ──────────────────
import torch.nn as nn
class TabTransformer(nn.Module):
    def __init__(self, input_dim, embed_dim, depth, heads=8, dropout=0.3):
        super().__init__()
        self.embedding = nn.Linear(input_dim, embed_dim)
        enc_layer = nn.TransformerEncoderLayer(embed_dim, heads, embed_dim*4,
                                               dropout=dropout, batch_first=True)
        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=depth)
        self.dropout = nn.Dropout(dropout)
    def forward(self, x):
        x = self.embedding(x).unsqueeze(1)
        x = self.encoder(x)
        return self.dropout(x.mean(1))

class ResidualAdapter(nn.Module):
    def __init__(self, dim, bottleneck=128):
        super().__init__()
        self.adapter = nn.Sequential(
            nn.Linear(dim, bottleneck), nn.ReLU(), nn.Linear(bottleneck, dim))
    def forward(self, x): return x + self.adapter(x)

class MultiTaskTab(nn.Module):
    def __init__(self, in_dim_have, n_role, n_ind, n_want,
                 embed_dim=256, depth=6, dropout=0.3):
        super().__init__()
        self.backbone = TabTransformer(in_dim_have, embed_dim, depth, dropout=dropout)
        def head(out_dim, act=None):
            m = [nn.LayerNorm(embed_dim), nn.Linear(embed_dim, out_dim)]
            if act=='sigmoid': m.append(nn.Sigmoid())
            return nn.Sequential(*m)
        self.role_proj = ResidualAdapter(embed_dim)
        self.ind_proj  = ResidualAdapter(embed_dim)
        self.sal_proj  = ResidualAdapter(embed_dim)
        self.sat_proj  = ResidualAdapter(embed_dim)
        self.want_proj = ResidualAdapter(embed_dim)

        self.role_head = head(n_role, 'sigmoid')
        self.ind_head  = head(n_ind,  'sigmoid')
        self.want_head = head(n_want, 'sigmoid')
        self.sal_head  = head(n_role)
        self.sat_head  = head(n_role)

    def forward(self, x):
        f = self.backbone(x)
        return (
            self.role_head(self.role_proj(f)),
            self.ind_head (self.ind_proj (f)),
            self.sal_head (self.sal_proj (f)),
            self.sat_head (self.sat_proj (f)),
            self.want_head(self.want_proj(f)),
        )

# ───────────────── 3. 유틸 함수 ──────────────────────────
@torch.no_grad()
def predict_with_upskill(model, x_np, tok_have, tok_want, top_k=3, device="cpu"):
    x = torch.tensor(x_np, dtype=torch.float32).to(device)
    r,i,s,t,w = model(x); r,i,s,t,w = (a.cpu().numpy()[0] for a in (r,i,s,t,w))
    have_indices = np.where(x_np[0]==1)[0]
    have_tokens  = set(tok_have.classes_[have_indices])
    mask_w = np.isin(tok_want.classes_, list(have_tokens)).astype(np.float32)
    w_filtered = w*(1-mask_w)
    top_idx = w_filtered.argsort()[-top_k:][::-1]
    return {"role_prob":r,"industry_prob":i, "salary":s,"satisfaction": t,"topk_stack_idx":top_idx}

# ───────────────── 4. 로딩 (토크나이저 / 스케일러 / raw) ─
with open(RAW_PATH, 'rb') as f:
    raw = pickle.load(f)
tokenizer_have  = pickle.load(open(TOK_HAVE_PATH,  'rb'))
tokenizer_want  = pickle.load(open(TOK_WANT_PATH,  'rb'))
scaler          = joblib.load(SCALER_PATH)

have_cols  = [c for c in raw.columns if c.endswith("HaveWorkedWith")]
want_cols  = [c for c in raw.columns if c.endswith("WantToWorkWith")]
other_multi= ["ProfessionalTech"]

n_role = raw["DevType"].str.get_dummies(";").shape[1]
n_ind  = raw["Industry"].str.get_dummies(";").shape[1]
n_want = len(tokenizer_want.classes_)
INPUT_DIM = len(tokenizer_have.classes_)

# ───────────────── 5. 모델 로드 ──────────────────────────
model = MultiTaskTab(INPUT_DIM, n_role, n_ind, n_want,
                     embed_dim=EMBED_DIM, depth=DEPTH, dropout=DROPOUT).to(DEVICE)
model.load_state_dict(torch.load(PT_PATH, map_location=DEVICE))
model.eval()

# ───────────────── 6. 핵심 inference 함수 ───────────────
def run_inference(dummy_input: Dict[str, List[str]],
                  threshold:int=THRESHOLD, top_k:int=TOP_K)->pd.DataFrame:

    dummy_have_tokens = sum([dummy_input.get(c, []) for c in have_cols+other_multi], [])
    x0  = tokenizer_have.transform([dummy_have_tokens]).astype("float32")
    out = predict_with_upskill(model, x0, tokenizer_have, tokenizer_want,
                               top_k=top_k, device=DEVICE)

    role_cols = raw["DevType"].str.get_dummies(";").columns
    top_role_idx = out["role_prob"].argsort()[-top_k:][::-1]
    top_roles    = role_cols[top_role_idx]
    top_stacks   = tokenizer_want.classes_[out["topk_stack_idx"]]

    role_avg = {}
    dummy_set = set(dummy_have_tokens)
    #for role in role_cols:
    #    mask_role = raw["DevType"].str.contains(role, na=False)
    #    common_cnt = raw.loc[mask_role, have_cols+other_multi].apply(
    #        lambda row: len(dummy_set & set(sum(row, []))), axis=1)
    #    similar_mask = common_cnt >= threshold
    #    vals = raw.loc[mask_role & similar_mask, "CompTotal"].dropna()
    #    role_avg[role] = vals.mean() if len(vals) else np.nan
    for role in role_cols:
        mask_role = raw["DevType"].str.contains(role, na=False)
        vals = raw.loc[mask_role, "CompTotal"].dropna()
        role_avg[role] = vals.mean() if len(vals) else np.nan
    ind_cols = raw["Industry"].fillna("Unknown").str.get_dummies(";").columns
    top_ind_idx = out["industry_prob"].argsort()[-top_k:][::-1]
    top_inds    = ind_cols[top_ind_idx]
    rows=[]
    for r_idx,r_name in zip(top_role_idx, top_roles):
        sal_before = scaler.inverse_transform(out["salary"][r_idx].reshape(1,-1))[0,0]
        ds_mean    = role_avg.get(r_name, np.nan)
        sat_before = out["satisfaction"][r_idx]
        after=[]
        for s_tok in top_stacks:
            new_have=set(dummy_have_tokens)|{s_tok}
            x_new = tokenizer_have.transform([list(new_have)]).astype("float32")
            nw_out=predict_with_upskill(model,x_new,tokenizer_have,tokenizer_want,
                                        top_k=0,device=DEVICE)
            sal_after=scaler.inverse_transform(nw_out["salary"][r_idx].reshape(1,-1))[0,0]
            after.append(f"{sal_after:,.0f}")
        rows.append({
            "추천 직무":r_name,
            "추천 산업군": ", ".join(map(str, top_inds.tolist())),
            "예상 연봉(현재)":f"{sal_before:,.0f}",
            "예상 만족도": f"{sat_before:.2f}",
            "직무 평균 (DB)":f"{ds_mean:,.0f}",
            "추천 스택":", ".join(top_stacks),
            "보완 후 연봉": " / ".join(after)+" 원"
        })
    return pd.DataFrame(rows)

# ───────────────── 7. 예시 실행 ─────────────────────────
if __name__ == "__main__":
    dummy = {
        "LanguageHaveWorkedWith": ["Python", "C"],
        "DatabaseHaveWorkedWith": ["SQLite"],
        "PlatformHaveWorkedWith": ["AWS"],
        "WebframeHaveWorkedWith": ["FastAPI", "React", "Flack"],
        "EmbeddedHaveWorkedWith": ["GNU GCC"],
        "MiscTechHaveWorkedWith": ["Docker", "Numpy", "PyTorch"],
        "ToolsTechHaveWorkedWith": ["Docker"],
        "ProfessionalTech": ["AI-assisted Tech. Tool"],
    }
    df = run_inference(dummy)
    print(df.to_markdown(index=False))
