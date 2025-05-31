import json, random
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
import pandas as pd
import os

class BERT4Rec(nn.Module):
    def __init__(self, cfg):
        super().__init__()

        self.hidden_size = cfg['hidden_size']
        self.max_len     = cfg['max_seq_length']
        self.n_items     = cfg['n_items']

        # +2: padding(0), mask 토큰
        self.item_emb = nn.Embedding(self.n_items+2, self.hidden_size, padding_idx=0)
        self.pos_emb  = nn.Embedding(self.max_len, self.hidden_size)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.hidden_size, nhead=cfg['n_heads'],
            dim_feedforward=cfg['inner_size'], dropout=cfg['hidden_dropout_prob'],
            activation="gelu", layer_norm_eps=cfg['layer_norm_eps'],
            batch_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=cfg['n_layers'])
        self.norm    = nn.LayerNorm(self.hidden_size, eps=cfg['layer_norm_eps'])
        self.drop    = nn.Dropout(cfg['hidden_dropout_prob'])
        self.out     = nn.Linear(self.hidden_size, self.n_items+1)
        self._init_weights(cfg['initializer_range'])

    def _init_weights(self, std):
        for n,p in self.named_parameters():
            if 'weight' in n:
                nn.init.normal_(p, 0, std)
            elif 'bias' in n:
                nn.init.constant_(p, 0)

    def forward(self, input_ids):
        pos = torch.arange(self.max_len, device=input_ids.device).unsqueeze(0).expand_as(input_ids)
        x = self.item_emb(input_ids) + self.pos_emb(pos)
        x = self.norm(x)
        x = self.drop(x)

        pad_mask = (input_ids == 0)
        h = self.encoder(x, src_key_padding_mask=pad_mask)
        return self.out(h)
