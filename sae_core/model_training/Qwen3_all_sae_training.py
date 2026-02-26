import argparse
import gc
import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
from huggingface_hub import HfApi
from transformer_lens import HookedTransformer

from sae_core.data_processing.textbook_process import load_processed_data
from sae_core.model_training.wandb_utils import (
    finish_wandb_run,
    maybe_init_wandb_run,
    maybe_log_final_artifact,
    maybe_update_wandb_summary,
)
from sae_core.pretrained import load_pretrained
from sae_core.sae_base import BatchTopKSAE
from sae_core.sae_config import SAEConfig
from sae_core.sae_train import SAETrainer
from sae_core.train_config import TrainingConfig


QWEN3_MODELS = [
    "Qwen/Qwen3-0.6B",
    "Qwen/Qwen3-1.7B",
    "Qwen/Qwen3-4B",
    "Qwen/Qwen3-8B",
    "Qwen/Qwen3-14B",
    "Qwen/Qwen3-32B",
]

# Conservative defaults to reduce OOM risk as models scale up.
MODEL_TRAINING_OVERRIDES: Dict[str, Dict[str, int]] = {
    "Qwen/Qwen3-0.6B": {"batch_size": 8, "activation_batch_size": 16, "max_text_length": 512},
    "Qwen/Qwen3-1.7B": {"batch_size": 4, "activation_batch_size": 16, "max_text_length": 512},
    "Qwen/Qwen3-4B": {"batch_size": 2, "activation_batch_size": 8, "max_text_length": 384},
    "Qwen/Qwen3-8B": {"batch_size": 1, "activation_batch_size": 8, "max_text_length": 256},
    "Qwen/Qwen3-14B": {"batch_size": 1, "activation_batch_size": 4, "max_text_length": 192},
    "Qwen/Qwen3-32B": {"batch_size": 1, "activation_batch_size": 2, "max_text_length": 128},
}


def get_compute_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


DEVICE = get_compute_device()
TORCH_DTYPE = torch.float16 if DEVICE in {"cuda", "mps"} else torch.float32
DTYPE_STR = str(TORCH_DTYPE).replace("torch.", "")
NUM_DEVICES = torch.cuda.device_count() if DEVICE == "cuda" else 1


def build_model_load_config(load_in_4bit: bool) -> Dict[str, object]:
    from_pretrained_kwargs = {
        "trust_remote_code": True,
        "torch_dtype": TORCH_DTYPE,
        "load_in_4bit": load_in_4bit,
    }
    if NUM_DEVICES > 1:
        from_pretrained_kwargs["device_map"] = "auto"

    return {
        "device": DEVICE,
        "dtype": DTYPE_STR,
        "n_devices": max(1, NUM_DEVICES),
        "from_pretrained_kwargs": from_pretrained_kwargs,
    }


def split_texts(texts: List[str], val_fraction: float = 0.1, seed: int = 0) -> Tuple[List[str], List[str]]:
    if not texts:
        raise ValueError("No texts provided for training/validation split")
    rng = random.Random(seed)
    indices = list(range(len(texts)))
    rng.shuffle(indices)
    val_count = int(len(texts) * val_fraction)
    if val_count == 0 and len(texts) > 1:
        val_count = 1
    val_count = min(val_count, max(len(texts) - 1, 0))
    val_indices = set(indices[:val_count])
    train_texts = [text for idx, text in enumerate(texts) if idx not in val_indices]
    val_texts = [text for idx, text in enumerate(texts) if idx in val_indices]
    return train_texts, val_texts


def select_middle_layer(n_layers: int, strategy: str) -> int:
    if n_layers <= 0:
        raise ValueError(f"Invalid layer count: {n_layers}")
    if strategy == "upper":
        return n_layers // 2
    return (n_layers - 1) // 2


def clear_device_cache() -> None:
    gc.collect()
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    if DEVICE == "mps" and hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
        torch.mps.empty_cache()


def maybe_upload_to_hf(local_model_path: Path, hf_repo_id: Optional[str], hf_private: bool) -> None:
    if hf_repo_id is None:
        raise ValueError(
            "Upload requested but no HF repo was provided. "
            "Set --hf-repo-id or SAE_HF_REPO_ID."
        )
    api = HfApi()
    api.create_repo(repo_id=hf_repo_id, repo_type="model", private=hf_private, exist_ok=True)
    api.upload_folder(
        repo_id=hf_repo_id,
        repo_type="model",
        folder_path=str(local_model_path),
        path_in_repo=local_model_path.name,
        commit_message=f"Add {local_model_path.name}",
    )


def make_training_config(model_name: str, args: argparse.Namespace, l1_coefficient: float) -> TrainingConfig:
    overrides = MODEL_TRAINING_OVERRIDES.get(model_name, {})
    batch_size = overrides.get("batch_size", args.batch_size)
    activation_batch_size = overrides.get("activation_batch_size", args.activation_batch_size)
    max_text_length = overrides.get("max_text_length", args.max_text_length)

    return TrainingConfig(
        num_epochs=args.num_epochs,
        batch_size=batch_size,
        lr=args.lr,
        l1_coefficient=l1_coefficient,
        use_end_to_end=True,
        reconstruction_loss_weight=args.recon_weight,
        use_block_mse=False,
        block_mse_weight=args.mse_penalty,
        use_logit_kl=True,
        logit_kl_weight=args.kl_penalty,
        log_freq=args.log_freq,
        early_stopping_patience=args.early_stopping_patience,
        early_stopping_min_delta=args.early_stopping_min_delta,
        activation_batch_size=activation_batch_size,
        max_text_length=max_text_length,
    )


def train_single_model(
    model_name: str,
    train_texts: List[str],
    val_texts: List[str],
    args: argparse.Namespace,
) -> Tuple[Path, Path]:
    model_load_config = build_model_load_config(load_in_4bit=args.load_in_4bit)
    model_id = model_name.replace("/", "_")

    print("\n" + "=" * 80)
    print(f"Loading model: {model_name}")
    qwen3_model = HookedTransformer.from_pretrained(
        model_name,
        device=model_load_config.get("device"),
        dtype=model_load_config.get("dtype", "float32"),
        n_devices=model_load_config.get("n_devices", 1),
        **model_load_config.get("from_pretrained_kwargs", {}),
    )
    qwen3_model.eval()

    middle_layer = select_middle_layer(qwen3_model.cfg.n_layers, args.middle_layer_strategy)
    hook_layer = str(middle_layer)
    hook_name = args.hook_name
    hook_spec = f"blocks.{hook_layer}.{hook_name}"

    sae_config = SAEConfig(
        d_in=qwen3_model.cfg.d_model,
        d_sae=args.sae_expansion * qwen3_model.cfg.d_model,
        l1_coefficient=args.sparsity_penalty,
        dtype="float32",
        device=model_load_config["device"],
        hook_layer=hook_layer,
        hook_name=hook_name,
        hook_spec=hook_spec,
        top_k=args.topk,
    )
    print(
        "SAE config:"
        f" d_in={sae_config.d_in}, d_sae={sae_config.d_sae},"
        f" n_layers={qwen3_model.cfg.n_layers}, selected_middle_layer={middle_layer}"
    )

    train_config = make_training_config(model_name, args, l1_coefficient=sae_config.l1_coefficient)
    print(
        "Training config:"
        f" batch_size={train_config.batch_size},"
        f" activation_batch_size={train_config.activation_batch_size},"
        f" max_text_length={train_config.max_text_length}"
    )

    trainer = SAETrainer(
        qwen3_model,
        sae_class=BatchTopKSAE,
        sae_config=sae_config,
        train_config=train_config,
        device=sae_config.device,
    )

    checkpoint_dir = args.checkpoint_root / f"{model_id}_layer{hook_layer}_exp{args.sae_expansion}"
    run_name = f"{model_id}.{hook_spec}.btop{args.topk}sae.middle.exp{args.sae_expansion}"
    wandb_tags = list(args.wandb_tags or [])
    wandb_tags.extend(["batch_topk", "qwen3", f"layer{middle_layer}", model_name.split("/")[-1]])
    wandb_run = maybe_init_wandb_run(
        enabled=args.wandb,
        project=args.wandb_project,
        entity=args.wandb_entity,
        name=run_name,
        job_type="qwen3_sae_training",
        group=args.wandb_group or "qwen3_all_sae_training",
        notes=args.wandb_notes,
        mode=args.wandb_mode,
        tags=wandb_tags,
        config={
            "cli_args": vars(args),
            "resolved": {
                "device": model_load_config["device"],
                "model_dtype": model_load_config["dtype"],
                "n_devices": model_load_config["n_devices"],
                "hook_layer": middle_layer,
                "hook_spec": hook_spec,
                "run_name": run_name,
            },
            "sae_config": sae_config.to_dict(),
            "train_config": vars(train_config),
            "dataset": {
                "train_texts": len(train_texts),
                "val_texts": len(val_texts),
            },
            "model_cfg": {
                "n_layers": int(qwen3_model.cfg.n_layers),
                "d_model": int(qwen3_model.cfg.d_model),
            },
        },
    )

    print("Starting SAE training")
    try:
        history = trainer.train(
            texts=train_texts,
            checkpoint_dir=str(checkpoint_dir),
            checkpoint_freq=args.checkpoint_freq,
            save_best=True,
            val_texts=val_texts if len(val_texts) > 0 else None,
            wandb_run=wandb_run,
        )

        best_model_path = checkpoint_dir / "best_model.pt"
        if best_model_path.exists():
            print(f"Loading best checkpoint from {best_model_path}")
            trainer.sae = load_pretrained(
                str(best_model_path),
                device=sae_config.device,
            )
        else:
            print("Best checkpoint not found; exporting last-epoch weights.")

        model_path = args.output_root / run_name
        trainer.sae.save(str(model_path), history=history)

        maybe_update_wandb_summary(
            wandb_run,
            {
                "status": "completed",
                "saved_model_path": str(model_path),
                "checkpoint_dir": str(checkpoint_dir),
                "final/loss": history["loss"][-1],
                "final/val_loss": history["val_loss"][-1] if "val_loss" in history else None,
                "final/dead_features": history["dead_features"][-1],
                "final/dead_feature_percentage": history["dead_feature_percentage"][-1],
            },
        )
        if args.wandb_log_final_artifact:
            maybe_log_final_artifact(
                wandb_run,
                model_dir=model_path,
                artifact_name=f"{run_name.replace('/', '_')}-final",
                metadata={
                    "run_name": run_name,
                    "model_name": model_name,
                    "hook_spec": hook_spec,
                    "checkpoint_artifacts_uploaded": False,
                },
            )
    except Exception as exc:
        maybe_update_wandb_summary(
            wandb_run,
            {
                "status": "failed",
                "error": str(exc),
            },
        )
        raise
    finally:
        finish_wandb_run(wandb_run)

    print("Training complete")
    print(f"Final model: {model_path}")
    print(f"Checkpoints: {checkpoint_dir}")
    print(f"Final loss: {history['loss'][-1]:.4f}")
    if "val_loss" in history:
        print(f"Final val_loss: {history['val_loss'][-1]:.4f}")
    print(
        "Final dead features:"
        f" {history['dead_features'][-1]}"
        f" ({history['dead_feature_percentage'][-1]:.2f}%)"
    )

    del trainer
    del qwen3_model
    clear_device_cache()
    return model_path, checkpoint_dir


def parse_args() -> argparse.Namespace:
    default_data_path = Path(__file__).resolve().parents[2] / "sae_core/data/processed_data/processed_textbooks_all.json"
    parser = argparse.ArgumentParser(
        description="Train one BatchTopK SAE at the middle layer for each selected Qwen3 model."
    )
    parser.add_argument("--models", nargs="+", default=QWEN3_MODELS, help="Model IDs to train.")
    parser.add_argument("--data-path", type=Path, default=default_data_path, help="Path to processed text JSON.")
    parser.add_argument("--output-root", type=Path, default=Path("sae_core/pretrained_models"))
    parser.add_argument("--checkpoint-root", type=Path, default=Path("sae_core/checkpoints"))
    parser.add_argument("--val-fraction", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=420)
    parser.add_argument("--middle-layer-strategy", choices=["lower", "upper"], default="lower")
    parser.add_argument("--hook-name", default="hook_resid_post")

    parser.add_argument("--sae-expansion", type=int, default=4)
    parser.add_argument("--topk", type=int, default=128)
    parser.add_argument("--sparsity-penalty", type=float, default=0.0)
    parser.add_argument("--num-epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--activation-batch-size", type=int, default=16)
    parser.add_argument("--max-text-length", type=int, default=512)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--recon-weight", type=float, default=1.0)
    parser.add_argument("--mse-penalty", type=float, default=1e-3)
    parser.add_argument("--kl-penalty", type=float, default=1e-2)
    parser.add_argument("--log-freq", type=int, default=100)
    parser.add_argument("--checkpoint-freq", type=int, default=2)
    parser.add_argument("--early-stopping-patience", type=int, default=2)
    parser.add_argument("--early-stopping-min-delta", type=float, default=0.0)
    parser.add_argument("--load-in-4bit", action="store_true", help="Enable 4-bit model loading.")

    parser.add_argument("--upload-to-hf", action="store_true", help="Upload each trained SAE after saving.")
    parser.add_argument(
        "--hf-repo-id",
        default=os.getenv("SAE_HF_REPO_ID"),
        help="HF model repo id, e.g. username/Qwen3_SAEs. Defaults to SAE_HF_REPO_ID env var.",
    )
    parser.add_argument("--hf-private", action="store_true", help="Used only when creating a missing HF repo.")

    parser.add_argument("--wandb", action="store_true", help="Log epoch metrics to Weights & Biases.")
    parser.add_argument("--wandb-project", default=os.getenv("WANDB_PROJECT", "sae-training"))
    parser.add_argument("--wandb-entity", default=os.getenv("WANDB_ENTITY"))
    parser.add_argument(
        "--wandb-mode",
        choices=["online", "offline", "disabled"],
        default=None,
        help="Optional W&B mode override. Defaults to WANDB_MODE env var / wandb default.",
    )
    parser.add_argument("--wandb-group", default=None, help="Optional W&B group for all model runs.")
    parser.add_argument("--wandb-notes", default=None)
    parser.add_argument("--wandb-tags", nargs="*", default=None)
    parser.add_argument(
        "--wandb-log-final-artifact",
        action="store_true",
        help="Upload only the final exported SAE directory to W&B Artifacts (never checkpoints).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_root.mkdir(parents=True, exist_ok=True)
    args.checkpoint_root.mkdir(parents=True, exist_ok=True)

    text_list = load_processed_data(args.data_path)
    train_texts, val_texts = split_texts(text_list, val_fraction=args.val_fraction, seed=args.seed)
    print(
        f"Loaded {len(train_texts)} training texts and {len(val_texts)} validation texts "
        f"from {args.data_path}"
    )
    print(f"Device={DEVICE}, dtype={DTYPE_STR}, n_devices={max(1, NUM_DEVICES)}")
    print(f"Models to train: {args.models}")

    successes: List[Tuple[str, Path]] = []
    failures: List[Tuple[str, str]] = []

    for model_name in args.models:
        try:
            model_path, _ = train_single_model(
                model_name=model_name,
                train_texts=train_texts,
                val_texts=val_texts,
                args=args,
            )
            if args.upload_to_hf:
                print(f"Uploading {model_path.name} to Hugging Face repo {args.hf_repo_id}")
                maybe_upload_to_hf(
                    local_model_path=model_path,
                    hf_repo_id=args.hf_repo_id,
                    hf_private=args.hf_private,
                )
            successes.append((model_name, model_path))
        except Exception as exc:
            failures.append((model_name, str(exc)))
            print(f"Failed model {model_name}: {exc}")
            clear_device_cache()

    print("\n" + "=" * 80)
    print("Run summary")
    print(f"Successful: {len(successes)}")
    for model_name, model_path in successes:
        print(f"  - {model_name}: {model_path}")
    print(f"Failed: {len(failures)}")
    for model_name, error_msg in failures:
        print(f"  - {model_name}: {error_msg}")

    if failures:
        raise RuntimeError("Some models failed during training. See summary above.")


if __name__ == "__main__":
    main()
