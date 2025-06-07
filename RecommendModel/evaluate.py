import json, random
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import pandas as pd
import os

def evaluate_simple_metrics(all_scores: np.ndarray, all_labels: np.ndarray):
    N, V = all_scores.shape
    rank = np.argsort(-all_scores, axis=1)

    hits1  = np.array([1 if all_labels[i] in rank[i, :1] else 0 for i in range(N)])
    hits5  = np.array([1 if all_labels[i] in rank[i, :5] else 0 for i in range(N)])
    hits10 = np.array([1 if all_labels[i] in rank[i, :10] else 0 for i in range(N)])
    HR1  = hits1.mean()
    HR5  = hits5.mean()
    HR10 = hits10.mean()

    def compute_ndcg_at_k(k):
        dcg_list = np.zeros(N, dtype=np.float32)
        for i in range(N):
            true_item = all_labels[i]
            topk_items = rank[i, :k]
            if true_item in topk_items:
                r = int(np.where(topk_items == true_item)[0][0])
                dcg_list[i] = 1.0 / np.log2(r + 2.0)
            else:
                dcg_list[i] = 0.0
        return float(dcg_list.mean())

    NDCG5  = compute_ndcg_at_k(5)
    NDCG10 = compute_ndcg_at_k(10)

    rr_list = np.zeros(N, dtype=np.float32)
    for i in range(N):
        true_item = all_labels[i]
        r_full = int(np.where(rank[i] == true_item)[0][0])
        rr_list[i] = 1.0 / (r_full + 1.0)
    MRR = float(rr_list.mean())

    return {
        "HR@1":   HR1,
        "HR@5":   HR5,
        "HR@10":  HR10,
        "NDCG@5":  NDCG5,
        "NDCG@10": NDCG10,
        "MRR":    MRR
    }