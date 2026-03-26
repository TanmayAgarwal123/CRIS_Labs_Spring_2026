import bisect
import torch
from torch.utils.data import DataLoader, Dataset
from transformer_lens import HookedTransformer
from typing import Any, List, Optional
from pathlib import Path

from sae_core.sae_base import SAE
from sae_core.sae_config import SAEConfig
from sae_core.training import train_sae
from sae_core.train_config import TrainingConfig


class _TokenizedTextDataset(Dataset):
    """Shared tokenizer/cache logic for text datasets used by SAE training."""

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
        self.tokenized_texts = self._tokenize_all_texts()
        if len(self.tokenized_texts) == 0:
            raise ValueError("No valid token sequences produced from provided texts")

    def _tokenize_all_texts(self) -> List[torch.Tensor]:
        tokenized: List[torch.Tensor] = []
        for text in self.texts:
            tokens = self._tokenize(text)
            if tokens.numel() > 0:
                tokenized.append(tokens)
        return tokenized

    def __len__(self) -> int:
        raise NotImplementedError

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


class WindowedTextDataset(_TokenizedTextDataset):
    """Deterministic non-overlapping windows (used for validation/eval)."""

    def __init__(
        self,
        texts: List[str],
        tokenizer,
        max_length: int,
        prepend_bos: bool = False,
    ):
        super().__init__(
            texts=texts,
            tokenizer=tokenizer,
            max_length=max_length,
            prepend_bos=prepend_bos,
        )
        self.windows = self._build_windows()
        if len(self.windows) == 0:
            raise ValueError("No valid token windows produced from provided texts")

    def __len__(self) -> int:
        return len(self.windows)

    def _build_windows(self) -> List[torch.Tensor]:
        """Split cached tokenized texts into deterministic non-overlapping windows."""
        windows: List[torch.Tensor] = []
        for tokens in self.tokenized_texts:
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


class RandomCropWindowedTextDataset(_TokenizedTextDataset):
    """
    Randomly samples a crop from cached tokenized texts on each __getitem__.

    This reduces persistent alignment artifacts (e.g., "position-0" features)
    caused by deterministic window boundaries while keeping validation deterministic.
    """

    def __init__(
        self,
        texts: List[str],
        tokenizer,
        max_length: int,
        prepend_bos: bool = False,
        windows_per_epoch: Optional[int] = None,
    ):
        super().__init__(
            texts=texts,
            tokenizer=tokenizer,
            max_length=max_length,
            prepend_bos=prepend_bos,
        )

        # Approximate old epoch semantics by defaulting to the number of
        # non-overlapping windows the deterministic dataset would have produced.
        if windows_per_epoch is None:
            windows_per_epoch = sum(
                max(1, (tokens.shape[0] + self.max_length - 1) // self.max_length)
                for tokens in self.tokenized_texts
            )
        if windows_per_epoch <= 0:
            raise ValueError("windows_per_epoch must be > 0")
        self.windows_per_epoch = int(windows_per_epoch)

        # Weight text sampling by number of possible crops, which better
        # approximates uniform sampling over window starts than uniform-text sampling.
        self._crop_start_counts = [
            max(1, int(tokens.shape[0]) - self.max_length + 1)
            for tokens in self.tokenized_texts
        ]
        self._cumulative_crop_weights: List[int] = []
        total = 0
        for count in self._crop_start_counts:
            total += count
            self._cumulative_crop_weights.append(total)
        self._total_crop_weight = total

    def __len__(self) -> int:
        return self.windows_per_epoch

    def _sample_text_index(self) -> int:
        draw = int(torch.randint(self._total_crop_weight, (1,)).item())
        return bisect.bisect_right(self._cumulative_crop_weights, draw)

    def __getitem__(self, idx: int) -> torch.Tensor:
        del idx  # sampling is randomized each call
        text_idx = self._sample_text_index()
        tokens = self.tokenized_texts[text_idx]
        if tokens.shape[0] <= self.max_length:
            return tokens.clone()

        max_start = int(tokens.shape[0]) - self.max_length
        start = int(torch.randint(max_start + 1, (1,)).item())
        end = start + self.max_length
        return tokens[start:end].clone()


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
            wandb_run: Optional[Any] = None,
        ):
        pad_token_id = self.model.tokenizer.pad_token_id
        if pad_token_id is None:
            pad_token_id = self.model.tokenizer.eos_token_id
        if pad_token_id is None:
            raise ValueError("Tokenizer must supply a pad_token_id or eos_token_id for batching")

        dataset = RandomCropWindowedTextDataset(
            texts=texts,
            tokenizer=self.model.tokenizer,
            max_length=self.train_cfg.max_text_length,
            prepend_bos=False,
        )

        sample_tokens = dataset[0]
        print(f"Token dtype: {sample_tokens.dtype}")
        print(f"Sample tokens: {sample_tokens[:10]}")
        print(f"Training dataset mode: random-crop windows ({len(dataset)} samples/epoch)")

        persistent_workers = (
            self.train_cfg.persistent_workers and self.train_cfg.num_dataloader_workers > 0
        )

        loader = DataLoader(
            dataset,
            batch_size=self.train_cfg.batch_size,
            # Dataset sampling is already randomized per __getitem__.
            shuffle=False,
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
                prepend_bos=False,
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
            print(f"Validation dataset mode: deterministic windows ({len(val_dataset)} total)")

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
            wandb_run=wandb_run,
        )
    
print("all the way through")
