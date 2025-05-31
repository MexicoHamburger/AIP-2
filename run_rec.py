import json, random
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import pandas as pd
import os
from RecommendModel.bert4rec import BERT4Rec
from RecommendModel.bert4rec_dataset import BERT4RecDataset, create_dataloader
from RecommendModel.evaluate import evaluate_simple_metrics
import argparse

import wandb


# Set random seed for reproducibility
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def load_json(file_path):
    with open('./util/result_clean.json','r') as f:
        raw_data = json.load(f)

    rows = []
    for uid, user in enumerate(raw_data):
        for ts, token in enumerate(user['token_sequence']):
            rows.append([uid, token, ts])
    df = pd.DataFrame(rows, columns=["user_id","item_id","timestamp"])
    user_seqs = df.groupby("user_id")["item_id"].apply(list).tolist()

    unique_items = sorted(df["item_id"].unique().tolist())
    token2id = {t:i+1 for i,t in enumerate(unique_items)}
    token2id['[MASK]'] = len(token2id) + 1
    id2token = {v:k for k,v in token2id.items()}
    
    return user_seqs, token2id, id2token


def train_bert4rec(args, model_bert, train_loader, val_loader, 
                   device, opt, criterion, EPOCHS=100, SAVE_DIR='./checkpoints'):
    
    best_epoch    = -1
    best_val_loss = float('inf')
    for epoch in tqdm(range(1, 1 + EPOCHS)):
        # --- (1) Train ---
        model_bert.train()
        total_loss = 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            logits = model_bert(x)              # (B, L, V)
            B, L, V = logits.shape
            loss = criterion(logits.view(-1, V), y.view(-1))
            opt.zero_grad()
            loss.backward()
            opt.step()
            total_loss += loss.item()
        train_loss = total_loss / len(train_loader)

        # --- (2) Validation ---
        model_bert.eval()
        val_loss = 0
        all_scores, all_labels = [], []

        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                logits = model_bert(x)           # (B, L, V)
                B, L, V = logits.shape
                val_loss += criterion(logits.view(-1, V), y.view(-1)).item()

                # Predict last item
                for b in range(B):
                    pos = (y[b] != -100).nonzero(as_tuple=True)[0].item()
                    scores = logits[b, pos, :].clone()

                    # exclude already seen items (input_ids)
                    input_token_ids = set(x[b].tolist())
                    for t_id in input_token_ids:
                        if t_id != 0:
                            scores[t_id] = float('-inf')

                    all_scores.append(scores.cpu().numpy())
                    all_labels.append(y[b, pos].item())

        val_loss /= len(val_loader)
        val_metrics = {}
        val_metrics = evaluate_simple_metrics(np.stack(all_scores), np.array(all_labels))

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_epoch    = epoch
            save_path = os.path.join(SAVE_DIR, "bert4rec.pt")
            torch.save(model_bert.state_dict(), save_path)
        
            result_text = f"Epoch {best_epoch}/{EPOCHS} - " \
                        f"Train Loss: {train_loss:.4f}, " \
                        f"Val Loss: {val_loss:.4f}, " \
                        f"HR@1: {val_metrics['HR@1']:.4f}, " \
                        f"HR@5: {val_metrics['HR@5']:.4f}, " \
                        f"HR@10: {val_metrics['HR@10']:.4f}, " \
                        f"NDCG@5: {val_metrics['NDCG@5']:.4f}, " \
                        f"NDCG@10: {val_metrics['NDCG@10']:.4f}, " \
                        f"MRR: {val_metrics['MRR']:.4f}"
            with open(os.path.join(SAVE_DIR, "result_val.txt"), 'w') as f:
                f.write(result_text + '\n')

        if args.wandb:
            wandb.log({
                "epoch": epoch,
                "train_loss": train_loss,
                "val_loss": val_loss,
                "val_HR@1": val_metrics['HR@1'],
                "val_HR@5": val_metrics['HR@5'],
                "val_HR@10": val_metrics['HR@10'],
                "val_NDCG@5": val_metrics['NDCG@5'],
                "val_NDCG@10": val_metrics['NDCG@10'],
                "val_MRR": val_metrics['MRR']
            })

    return save_path


def test_bert4rec(model_bert, test_loader, device, criterion, save_path, args):
    model_bert.load_state_dict(torch.load(save_path))
    model_bert.eval()

    test_loss = 0
    all_scores, all_labels = [], []

    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            logits = model_bert(x)           # (B, L, V)
            B, L, V = logits.shape
            test_loss += criterion(logits.view(-1, V), y.view(-1)).item()

            for b in range(B):
                pos = (y[b] != -100).nonzero(as_tuple=True)[0].item()
                scores = logits[b, pos, :].clone()  # (V,)

                # exclude already seen items (input_ids)
                input_token_ids = set(x[b].tolist())
                for t_id in input_token_ids:
                    if t_id != 0:
                        scores[t_id] = float('-inf')

                all_scores.append(scores.cpu().numpy())
                all_labels.append(y[b, pos].item())

    test_loss /= len(test_loader)

    # (3) Evaluate metrics
    all_scores_np = np.stack(all_scores)
    all_labels_np = np.array(all_labels, dtype=int)
    test_metrics = evaluate_simple_metrics(all_scores_np, all_labels_np)
    result_text = f"Test Loss: {test_loss:.4f}, " \
                  f"HR@1: {test_metrics['HR@1']:.4f}, " \
                  f"HR@5: {test_metrics['HR@5']:.4f}, " \
                  f"HR@10: {test_metrics['HR@10']:.4f}, " \
                  f"NDCG@5: {test_metrics['NDCG@5']:.4f}, " \
                  f"NDCG@10: {test_metrics['NDCG@10']:.4f}, " \
                  f"MRR: {test_metrics['MRR']:.4f}"
    with open(os.path.join(os.path.dirname(save_path), "result_test.txt"), 'w') as f:
        f.write(result_text + '\n')

    if args.wandb:
        wandb.log({
            "test_loss": test_loss,
            "HR@1 (TEST)": test_metrics['HR@1'],
            "HR@5 (TEST)": test_metrics['HR@5'],
            "HR@10 (TEST)": test_metrics['HR@10'],
            "NDCG@5 (TEST)": test_metrics['NDCG@5'],
            "NDCG@10 (TEST)": test_metrics['NDCG@10'],
            "MRR (TEST)": test_metrics['MRR']
        })

def run_rec(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    user_seqs, token2id, id2token = load_json(args.input_path)
    model_name = f'head_{args.n_heads}_layers_{args.n_layers}_batch_{args.batch_size}_seed_{args.seed}'
    
    output_path = args.output_dir + '/' + model_name
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    config = {
        "n_layers": args.n_layers,
        "n_heads": args.n_heads,
        "hidden_size": args.hidden_size,
        "inner_size": args.inner_size,
        "hidden_dropout_prob": args.hidden_dropout_prob,
        "attn_dropout_prob": args.attn_dropout_prob,
        "hidden_act": args.hidden_act,
        "layer_norm_eps": args.layer_norm_eps,
        "initializer_range": args.initializer_range,
        "mask_ratio": args.mask_ratio,
        "max_seq_length": args.max_seq_length,
        "n_items": len(token2id)
    }
    
    
    # Store token2id, id2token, and config 
    with open(os.path.join(output_path, "token2id.json"), 'w') as f:
        json.dump(token2id, f, indent=4)
    with open(os.path.join(output_path, "id2token.json"), 'w') as f:
        json.dump(id2token, f, indent=4)
    with open(os.path.join(output_path, "config.json"), 'w') as f:
        json.dump(config, f, indent=4)


    train_seqs = []
    val_seqs   = []
    test_seqs  = []

    for seq in user_seqs:
        if len(seq) < 3:
            continue
        train_seqs.append(seq[:-2])
        val_seqs.append(seq[:-1])
        test_seqs.append(seq)
        
    if args.wandb:
        wandb.init(
            project="seq_rec",
            entity="ai_project_team2",
            name=model_name,
            config=config
        )
    
    train_dataloaer, val_dataloader, test_dataloader = create_dataloader(
        train_seqs, val_seqs, test_seqs, token2id, config, args.batch_size
    )

    model = BERT4Rec(config).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    criterion = nn.CrossEntropyLoss(ignore_index=-100)
    
    # --- Train/Valid ---
    model_path = train_bert4rec(
        args, model, train_dataloaer, val_dataloader, 
        device, optimizer, criterion, EPOCHS=args.epochs, SAVE_DIR=output_path
    )
    
    # --- Test ---
    test_bert4rec(
        model, test_dataloader, device, criterion, 
        model_path, args
    )
    
    if args.wandb:
        wandb.finish()
    
    
    
    

def get_args():
    parser = argparse.ArgumentParser(description="Model and training configuration")
    
    parser.add_argument(
        '--seed', 
        type=int,
        default=0,
        help='Random seed for reproducibility'
    )

    # 모델 구조 관련 파라미터
    parser.add_argument(
        "--n_layers",
        type=int,
        default=4,
        help="Number of transformer layers"
    )
    parser.add_argument(
        "--n_heads",
        type=int,
        default=4,
        help="Number of attention heads per layer"
    )
    parser.add_argument(
        "--hidden_size",
        type=int,
        default=64,
        help="Hidden size (d_model) of each transformer layer"
    )
    parser.add_argument(
        "--inner_size",
        type=int,
        default=256,
        help="Inner (feed-forward) layer size"
    )
    parser.add_argument(
        "--hidden_act",
        type=str,
        default="gelu",
        help="Activation function in hidden layers (e.g., gelu, relu)"
    )
    parser.add_argument(
        "--layer_norm_eps",
        type=float,
        default=1e-12,
        help="Epsilon value for layer normalization"
    )
    parser.add_argument(
        "--initializer_range",
        type=float,
        default=0.02,
        help="Standard deviation of the truncated_normal_initializer for initializing all weight matrices"
    )
    # 드롭아웃 확률
    parser.add_argument(
        "--hidden_dropout_prob",
        type=float,
        default=0.2,
        help="Dropout probability for all fully connected layers in the embeddings and pooler"
    )
    parser.add_argument(
        "--attn_dropout_prob",
        type=float,
        default=0.2,
        help="Dropout probability for attention probabilities"
    )

    parser.add_argument(
        "--mask_ratio",
        type=float,
        default=0.2,
        help="Ratio of tokens to mask for masked language modeling"
    )
    
    parser.add_argument(
        "--max_seq_length",
        type=int,
        default=20,
        help="Maximum sequence length for inputs"
    )

    # 추가 학습 설정
    parser.add_argument(
        "--epochs",
        type=int,
        default=500,
        help="Number of training epochs"
    )
    
    parser.add_argument(
        "--batch_size",
        type=int,
        default=128,
        help="Batch size for training"
    )
    
    parser.add_argument(
        '--input_path',
            type=str,
            default='../util/result_clean.json',
        )
    parser.add_argument(
        '--output_dir',
        type=str,
        default='./checkpoints/bert4rec',
        help='Directory to save the model and results'
    )
    parser.add_argument(
        '--lr',
        type=float,
        default=1e-3,
        help='Learning rate for the optimizer'
    )
    
    parser.add_argument(
        '--wandb',
        action='store_true',
        help='Whether to use Weights & Biases for logging'
    )
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    set_seed(args.seed)
    run_rec(args)

    