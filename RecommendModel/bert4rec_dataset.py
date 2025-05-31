import json, random
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import pandas as pd
import os

class BERT4RecDataset(Dataset):
    def __init__(self, sequences, token2id, max_len=20, mask_ratio=0.2, val=False):
        self.sequences     = sequences
        self.token2id      = token2id
        self.max_len       = max_len
        self.mask_ratio    = mask_ratio
        self.val           = val
        self.mask_token_id = token2id['[MASK]']

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        seq = self.sequences[idx]
        # 1) 토큰→ID, truncate, left-pad
        ids = [self.token2id[t] for t in seq if t in self.token2id]
        ids = ids[-self.max_len:]
        pad = [0] * (self.max_len - len(ids))
        input_ids = pad + ids

        labels     = [-100] * self.max_len
        masked_ids = input_ids.copy()

        if self.val:
            # validation/Test: 마지막 non-pad 토큰만 마스크
            last_pos = max(i for i, x in enumerate(input_ids) if x != 0)
            labels[last_pos]     = input_ids[last_pos]
            masked_ids[last_pos] = self.mask_token_id
        else:
            # train: 랜덤 마스크 + 최소 1개 보장
            for i in range(self.max_len):
                if masked_ids[i] != 0 and random.random() < self.mask_ratio:
                    labels[i]       = masked_ids[i]
                    masked_ids[i]   = self.mask_token_id
            if all(l == -100 for l in labels):
                # 만약 모든 위치에서 마스킹이 일어나지 않았다면, 거듭 확인하여 
                # 마지막 non-pad 위치는 무조건 한 번 마스킹 처리
                last_pos = max(i for i,x in enumerate(input_ids) if x != 0)
                labels[last_pos]     = input_ids[last_pos]
                masked_ids[last_pos] = self.mask_token_id

        return (
            torch.tensor(masked_ids, dtype=torch.long),
            torch.tensor(labels,     dtype=torch.long),
        )
        
        
def create_dataloader(train_seqs, val_seqs, test_seqs, token2id, config, batch_size):
    train_ds = BERT4RecDataset(
        train_seqs,
        token2id,
        max_len=config['max_seq_length'],
        mask_ratio=config['mask_ratio'],  # train 단계: 랜덤 마스크
        val=False
    )
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)

    # ─ Validation DataLoader ─
    val_ds = BERT4RecDataset(
        val_seqs,
        token2id,
        max_len=config['max_seq_length'],
        mask_ratio=0.0,  # val 단계: mask_ratio=0.0으로 설정
        val=True         # val=True → 마지막 non-pad 위치(=원본 seq의 penultimate)를 마스킹
    )
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    # ─ Test DataLoader ─
    test_ds = BERT4RecDataset(
        test_seqs,
        token2id,
        max_len=config['max_seq_length'],
        mask_ratio=0.0,  # test 단계: mask_ratio=0.0
        val=True         # val=True → 마지막 non-pad 위치(=원본 seq의 마지막)를 마스킹
    )
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
    
    return train_loader, val_loader, test_loader


