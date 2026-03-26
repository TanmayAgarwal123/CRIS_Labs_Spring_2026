import argparse
import gc
import os
import random
from pathlib import Path
from typing import List, Optional, Tuple

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
from sae_core.sae_base import SAE, BatchTopKSAE
from sae_core.sae_config import SAEConfig
from sae_core.sae_train import SAETrainer
from sae_core.train_config import TrainingConfig


def get_compute_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def resolve_device(device_arg: str) -> str:
    if device_arg == "auto":
        return get_compute_device()
    return device_arg


def resolve_dtype(dtype_arg: str, device: str) -> torch.dtype:
    if dtype_arg == "auto":
        if device in {"cuda", "mps"}:
            return torch.float16
        return torch.float32
    return getattr(torch, dtype_arg)


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


def resolve_hook_layer(
    n_layers: int,
    requested_hook_layer: Optional[int],
    middle_layer_strategy: str,
) -> int:
    if requested_hook_layer is not None:
        if requested_hook_layer < 0 or requested_hook_layer >= n_layers:
            raise ValueError(
                f"hook_layer={requested_hook_layer} out of range for model with {n_layers} layers"
            )
        return requested_hook_layer
    return select_middle_layer(n_layers, middle_layer_strategy)


def clear_device_cache(device: str) -> None:
    gc.collect()
    if device == "cuda":
        torch.cuda.empty_cache()
    if device == "mps" and hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
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


def parse_args() -> argparse.Namespace:
    default_data_path = Path(__file__).resolve().parents[2] / "sae_core/data/processed_data/processed_textbooks_all.json"
    parser = argparse.ArgumentParser(
        description="Train a single SAE on one model, with configurable hook layer and hyperparameters."
    )

    # Model + data
    parser.add_argument("--model-name", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--data-path", type=Path, default=default_data_path)
    parser.add_argument("--output-root", type=Path, default=Path("sae_core/pretrained_models"))
    parser.add_argument("--checkpoint-root", type=Path, default=Path("sae_core/checkpoints"))
    parser.add_argument(
        "--run-name",
        default=None,
        help="Optional custom run name. If omitted, a descriptive name is generated automatically.",
    )
    parser.add_argument("--val-fraction", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=420)

    # Device + model load
    parser.add_argument("--device", choices=["auto", "cuda", "mps", "cpu"], default="auto")
    parser.add_argument(
        "--model-dtype",
        choices=["auto", "float16", "bfloat16", "float32"],
        default="auto",
        help="Dtype used when loading the model.",
    )
    parser.add_argument("--load-in-4bit", action="store_true")
    parser.add_argument(
        "--trust-remote-code",
        action=argparse.BooleanOptionalAction,
        default=True,
    )

    # Hook selection
    parser.add_argument("--hook-layer", type=int, default=None)
    parser.add_argument("--middle-layer-strategy", choices=["lower", "upper"], default="lower")
    parser.add_argument("--hook-name", default="hook_resid_post")

    # SAE config
    parser.add_argument("--sae-type", choices=["batch_topk", "standard"], default="batch_topk")
    parser.add_argument("--sae-expansion", type=int, default=4)
    parser.add_argument("--sae-dtype", default="float32")
    parser.add_argument("--sparsity-penalty", type=float, default=0.0)
    parser.add_argument("--topk", type=int, default=128)
    parser.add_argument("--topk-aux", type=int, default=None)
    parser.add_argument("--n-batches-to-dead", type=int, default=200)
    parser.add_argument("--aux-penalty", type=float, default=(1.0 / 32.0))

    # Training config
    parser.add_argument("--num-epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--activation-batch-size", type=int, default=16)
    parser.add_argument("--max-text-length", type=int, default=512)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--recon-weight", type=float, default=1.0)
    parser.add_argument("--use-end-to-end", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--use-block-mse", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--block-mse-weight", type=float, default=1e-3)
    parser.add_argument("--use-logit-kl", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--logit-kl-weight", type=float, default=1e-2)
    parser.add_argument("--log-freq", type=int, default=100)
    parser.add_argument("--checkpoint-freq", type=int, default=2)
    parser.add_argument("--early-stopping-patience", type=int, default=2)
    parser.add_argument("--early-stopping-min-delta", type=float, default=0.0)

    # HF upload
    parser.add_argument("--upload-to-hf", action="store_true")
    parser.add_argument(
        "--hf-repo-id",
        default=os.getenv("SAE_HF_REPO_ID"),
        help="HF model repo id, e.g. username/Qwen3_SAEs. Defaults to SAE_HF_REPO_ID env var.",
    )
    parser.add_argument("--hf-private", action="store_true")

    # W&B logging
    parser.add_argument("--wandb", action="store_true", help="Log epoch metrics to Weights & Biases.")
    parser.add_argument("--wandb-project", default=os.getenv("WANDB_PROJECT", "sae-training"))
    parser.add_argument("--wandb-entity", default=os.getenv("WANDB_ENTITY"))
    parser.add_argument(
        "--wandb-mode",
        choices=["online", "offline", "disabled"],
        default=None,
        help="Optional W&B mode override. Defaults to WANDB_MODE env var / wandb default.",
    )
    parser.add_argument("--wandb-group", default=None)
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

    if args.use_end_to_end and not (args.use_block_mse or args.use_logit_kl):
        raise ValueError(
            "Invalid config: with --use-end-to-end enabled, at least one of "
            "--use-block-mse or --use-logit-kl must be enabled."
        )

    if args.sae_type == "batch_topk" and args.topk <= 0:
        raise ValueError("--topk must be > 0 for batch_topk SAE")

    device = resolve_device(args.device)
    torch_dtype = resolve_dtype(args.model_dtype, device)
    dtype_str = str(torch_dtype).replace("torch.", "")
    n_devices = torch.cuda.device_count() if device == "cuda" else 1

    from_pretrained_kwargs = {
        "trust_remote_code": args.trust_remote_code,
        "torch_dtype": torch_dtype,
        "load_in_4bit": args.load_in_4bit,
    }
    if n_devices > 1:
        from_pretrained_kwargs["device_map"] = "auto"

    args.output_root.mkdir(parents=True, exist_ok=True)
    args.checkpoint_root.mkdir(parents=True, exist_ok=True)

    print(f"Loading dataset: {args.data_path}")
    text_list = load_processed_data(args.data_path)
    train_texts, val_texts = split_texts(text_list, val_fraction=args.val_fraction, seed=args.seed)
    print(
        f"Loaded {len(train_texts)} training texts and {len(val_texts)} validation texts "
        f"(seed={args.seed}, val_fraction={args.val_fraction})"
    )

    print(
        f"Loading model: {args.model_name} "
        f"(device={device}, dtype={dtype_str}, n_devices={max(1, n_devices)})"
    )
    model = HookedTransformer.from_pretrained(
        args.model_name,
        device=device,
        dtype=dtype_str,
        n_devices=max(1, n_devices),
        **from_pretrained_kwargs,
    )
    model.eval()

    hook_layer_int = resolve_hook_layer(
        n_layers=model.cfg.n_layers,
        requested_hook_layer=args.hook_layer,
        middle_layer_strategy=args.middle_layer_strategy,
    )
    hook_layer = str(hook_layer_int)
    hook_spec = f"blocks.{hook_layer}.{args.hook_name}"

    sae_class = BatchTopKSAE if args.sae_type == "batch_topk" else SAE
    top_k = args.topk if args.sae_type == "batch_topk" else None
    top_k_aux = args.topk_aux if args.sae_type == "batch_topk" else None

    sae_config = SAEConfig(
        d_in=model.cfg.d_model,
        d_sae=args.sae_expansion * model.cfg.d_model,
        l1_coefficient=args.sparsity_penalty,
        dtype=args.sae_dtype,
        device=device,
        hook_layer=hook_layer,
        hook_name=args.hook_name,
        hook_spec=hook_spec,
        top_k=top_k,
        top_k_aux=top_k_aux,
        n_batches_to_dead=args.n_batches_to_dead,
        aux_penalty=args.aux_penalty,
    )

    train_config = TrainingConfig(
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        l1_coefficient=sae_config.l1_coefficient,
        use_end_to_end=args.use_end_to_end,
        reconstruction_loss_weight=args.recon_weight,
        use_block_mse=args.use_block_mse,
        block_mse_weight=args.block_mse_weight,
        use_logit_kl=args.use_logit_kl,
        logit_kl_weight=args.logit_kl_weight,
        log_freq=args.log_freq,
        early_stopping_patience=args.early_stopping_patience,
        early_stopping_min_delta=args.early_stopping_min_delta,
        activation_batch_size=args.activation_batch_size,
        max_text_length=args.max_text_length,
    )

    print(
        "Training setup:"
        f" hook={hook_spec}, sae_type={args.sae_type}, "
        f"d_in={sae_config.d_in}, d_sae={sae_config.d_sae}"
    )
    print(
        "Training config:"
        f" epochs={train_config.num_epochs}, batch_size={train_config.batch_size}, "
        f"activation_batch_size={train_config.activation_batch_size}, "
        f"max_text_length={train_config.max_text_length}"
    )

    model_id = args.model_name.replace("/", "_")
    sae_tag = f"btop{args.topk}sae" if args.sae_type == "batch_topk" else "sae"
    default_run_name = f"{model_id}.{hook_spec}.{sae_tag}.exp{args.sae_expansion}"
    run_name = args.run_name or default_run_name
    checkpoint_dir = args.checkpoint_root / run_name
    model_path = args.output_root / run_name

    wandb_tags = list(args.wandb_tags or [])
    wandb_tags.extend([args.sae_type, f"layer{hook_layer_int}", args.model_name.split("/")[-1]])
    wandb_run = maybe_init_wandb_run(
        enabled=args.wandb,
        project=args.wandb_project,
        entity=args.wandb_entity,
        name=run_name,
        job_type="single_sae_training",
        group=args.wandb_group,
        notes=args.wandb_notes,
        mode=args.wandb_mode,
        tags=wandb_tags,
        config={
            "cli_args": vars(args),
            "resolved": {
                "device": device,
                "model_dtype": dtype_str,
                "n_devices": max(1, n_devices),
                "hook_layer": hook_layer_int,
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
                "n_layers": int(model.cfg.n_layers),
                "d_model": int(model.cfg.d_model),
            },
        },
    )

    trainer = SAETrainer(
        model,
        sae_class=sae_class,
        sae_config=sae_config,
        train_config=train_config,
        device=sae_config.device,
    )
    try:
        print("Starting SAE training")
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

        trainer.sae.save(str(model_path), history=history)

        if args.upload_to_hf:
            print(f"Uploading {model_path.name} to Hugging Face repo {args.hf_repo_id}")
            maybe_upload_to_hf(
                local_model_path=model_path,
                hf_repo_id=args.hf_repo_id,
                hf_private=args.hf_private,
            )

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
                "hf/uploaded": bool(args.upload_to_hf),
                "hf/repo_id": args.hf_repo_id if args.upload_to_hf else None,
            },
        )
        if args.wandb_log_final_artifact:
            maybe_log_final_artifact(
                wandb_run,
                model_dir=model_path,
                artifact_name=f"{run_name.replace('/', '_')}-final",
                metadata={
                    "run_name": run_name,
                    "model_name": args.model_name,
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

    print("\n" + "=" * 80)
    print("Run complete")
    print(f"Model: {args.model_name}")
    print(f"Saved SAE: {model_path}")
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
    del model
    clear_device_cache(device)


if __name__ == "__main__":
    main()
