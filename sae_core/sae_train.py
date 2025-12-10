import torch
from torch.utils.data import DataLoader, Dataset
from transformer_lens import HookedTransformer
from typing import List, Optional
from pathlib import Path

from sae_core.sae_base import SAE
from sae_core.sae_config import SAEConfig
from sae_core.training import train_sae
from sae_core.train_config import TrainingConfig


class WindowedTextDataset(Dataset):
    """Streams token windows from raw texts instead of pre-tokenizing everything."""

    def __init__(
        self,
        texts: List[str],
        tokenizer,
        max_length: int,
        prepend_bos: bool = False,
    ):
        self.texts = [t for t in texts if t and t.strip()]
        if len(self.texts) == 0:
            raise ValueError("No non-empty texts provided for training")
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.prepend_bos = prepend_bos
        self.bos_token_id = tokenizer.bos_token_id or tokenizer.eos_token_id
        self.windows = self._build_windows()
        if len(self.windows) == 0:
            raise ValueError("No valid token windows produced from provided texts")

    def __len__(self) -> int:
        return len(self.windows)

    def _tokenize(self, text: str) -> torch.Tensor:
        encoded = self.tokenizer(
            text,
            return_tensors="pt",
            padding=False,
            truncation=False,
            add_special_tokens=False,
        )["input_ids"][0]
        if self.prepend_bos and self.bos_token_id is not None:
            bos = torch.tensor([self.bos_token_id], dtype=torch.long)
            encoded = torch.cat([bos, encoded], dim=0)
        return encoded.long()

    def _build_windows(self) -> List[torch.Tensor]:
        """Tokenize once and split into fixed windows to avoid repeated work."""
        windows: List[torch.Tensor] = []
        for text in self.texts:
            tokens = self._tokenize(text)
            if tokens.numel() == 0:
                continue
            if tokens.shape[0] <= self.max_length:
                windows.append(tokens.clone())
                continue
            start = 0
            while start < tokens.shape[0]:
                end = min(start + self.max_length, tokens.shape[0])
                windows.append(tokens[start:end].clone())
                start = end
        return windows

    def __getitem__(self, idx: int) -> torch.Tensor:
        return self.windows[idx]


def pad_collate(batch: List[torch.Tensor], pad_token_id: int) -> torch.Tensor:
    """Pads a list of 1D token tensors into a batch."""
    max_len = max(t.size(0) for t in batch) # get max sequence length within the batch
    padded = torch.full((len(batch), max_len), pad_token_id, dtype=torch.long)
    for i, tokens in enumerate(batch):
        padded[i, : tokens.size(0)] = tokens
    return padded


class SAETrainer:    
    def __init__(
        self,
        model: HookedTransformer,
        sae_class: SAE,
        sae_config: SAEConfig,
        train_config: TrainingConfig,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.model = model
        self.hook_spec = sae_config.hook_spec
        self.device = device

        self.sae_cfg = sae_config
        self.train_cfg = train_config
        
        self.sae = sae_class(self.sae_cfg)
        
    def train(
            self, 
            texts: List[str],
            checkpoint_dir: Optional[str] = None,
            checkpoint_freq: int = 5,
            save_best: bool = True,
            val_texts: Optional[List[str]] = None,
        ):
        pad_token_id = self.model.tokenizer.pad_token_id
        if pad_token_id is None:
            pad_token_id = self.model.tokenizer.eos_token_id
        if pad_token_id is None:
            raise ValueError("Tokenizer must supply a pad_token_id or eos_token_id for batching")

        dataset = WindowedTextDataset(
            texts=texts,
            tokenizer=self.model.tokenizer,
            max_length=self.train_cfg.max_text_length,
            prepend_bos=True,
        )

        sample_tokens = dataset[0]
        print(f"Token dtype: {sample_tokens.dtype}")
        print(f"Sample tokens: {sample_tokens[:10]}")

        persistent_workers = (
            self.train_cfg.persistent_workers and self.train_cfg.num_dataloader_workers > 0
        )

        loader = DataLoader(
            dataset,
            batch_size=self.train_cfg.batch_size,
            shuffle=True,
            collate_fn=lambda batch: pad_collate(batch, pad_token_id),
            num_workers=self.train_cfg.num_dataloader_workers,
            pin_memory=self.train_cfg.pin_memory,
            persistent_workers=persistent_workers,
        )

        val_loader = None
        if val_texts is not None and len(val_texts) > 0:
            val_dataset = WindowedTextDataset(
                texts=val_texts,
                tokenizer=self.model.tokenizer,
                max_length=self.train_cfg.max_text_length,
                prepend_bos=True,
            )
            val_loader = DataLoader(
                val_dataset,
                batch_size=self.train_cfg.batch_size,
                shuffle=False,
                collate_fn=lambda batch: pad_collate(batch, pad_token_id),
                num_workers=self.train_cfg.num_dataloader_workers,
                pin_memory=self.train_cfg.pin_memory,
                persistent_workers=False,
            )

        checkpoint_path = Path(checkpoint_dir) if checkpoint_dir is not None else None

        return train_sae(
            self.sae, 
            self.model, 
            loader, 
            self.train_cfg,
            checkpoint_dir=checkpoint_path,
            checkpoint_freq=checkpoint_freq,
            save_best=save_best,
            val_loader=val_loader,
        )
    
print("all the way through")
