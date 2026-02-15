import random
import torch
from transformer_lens import HookedTransformer
from pathlib import Path

from sae_core.sae_base import SAE, BatchTopKSAE
from sae_core.sae_config import SAEConfig
from sae_core.pretrained import load_pretrained
from sae_core.sae_train import SAETrainer
from sae_core.train_config import TrainingConfig

from sae_core.data_processing.textbook_process import load_processed_data


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

from_pretrained_kwargs = {
    "trust_remote_code": True,
    "torch_dtype": TORCH_DTYPE,
}
if NUM_DEVICES > 1:
    from_pretrained_kwargs["device_map"] = "auto"

# Model + load configuration 
MODEL_NAME = "Qwen/Qwen3-0.6B"
MODEL_ID = MODEL_NAME.replace("/", "_")
MODEL_LOAD_CONFIG = {
    "device": DEVICE,
    "dtype": DTYPE_STR,
    "n_devices": max(1, NUM_DEVICES),
    "from_pretrained_kwargs": {
        "load_in_4bit": False,
        **from_pretrained_kwargs,
    },
}

sae_expansion = 4
sparsity_penalty = 0.0  # Set to 0 when doing BatchTopK
recon_weight = 1.0
mse_penalty = 0.001
kl_penalty = 1e-2
topk=128

def split_texts(texts, val_fraction=0.1, seed=0):
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


def main():
    data_path = Path(__file__).resolve().parents[2] / "sae_core/data/processed_data/processed_textbooks_all.json"
    text_list = load_processed_data(data_path)
    train_texts, val_texts = split_texts(text_list, val_fraction=0.1, seed=420)
    print(f"Loaded {len(train_texts)} training texts and {len(val_texts)} validation texts")

    # Qwen3 Models: 0.6B, 1.7B, 4B, 8B, 14B, 32B
    qwen3_model = HookedTransformer.from_pretrained(
        MODEL_NAME,
        device=MODEL_LOAD_CONFIG.get("device"),
        dtype=MODEL_LOAD_CONFIG.get("dtype", "float32"),
        n_devices=MODEL_LOAD_CONFIG.get("n_devices", 1),
        **MODEL_LOAD_CONFIG.get("from_pretrained_kwargs", {}),
    )
    qwen3_model.eval()

    hook_layer = '9'
    hook_name = 'hook_resid_post'
    hook_spec = f'blocks.{hook_layer}.{hook_name}'

    QWEN3_SAE_Config = SAEConfig(
        d_in = qwen3_model.cfg.d_model,
        d_sae = sae_expansion * qwen3_model.cfg.d_model,
        l1_coefficient = sparsity_penalty,
        dtype="float32",
        device = MODEL_LOAD_CONFIG["device"],
        hook_layer = hook_layer,
        hook_name = hook_name,
        hook_spec = hook_spec,
        top_k=topk
    )
    print(f'Model dim: {QWEN3_SAE_Config.d_in}, SAE dim: {QWEN3_SAE_Config.d_sae}')

    QWEN3_SAE_TRAIN_Config = TrainingConfig(
        num_epochs=10,
        batch_size=8,
        lr=1e-3,
        l1_coefficient=QWEN3_SAE_Config.l1_coefficient,
        use_end_to_end=True,
        reconstruction_loss_weight=recon_weight,
        use_block_mse=False, # Makes things worse actually
        block_mse_weight=mse_penalty,
        use_logit_kl= True,
        logit_kl_weight=kl_penalty,
        log_freq=100,
        early_stopping_patience=2,
        early_stopping_min_delta=0.0,
        activation_batch_size=16,
        max_text_length=512
    )

    QWEN3_SAE_Trainer = SAETrainer(
        qwen3_model,
        sae_class=BatchTopKSAE,
        sae_config=QWEN3_SAE_Config,
        train_config=QWEN3_SAE_TRAIN_Config,
        device=QWEN3_SAE_Config.device
    )

    print("Starting SAE training:")

    checkpoint_dir = Path('sae_core/checkpoints') / f'qwen3_06B_layer{hook_layer}_exp{sae_expansion}'

    history = QWEN3_SAE_Trainer.train(
        texts=train_texts,
        checkpoint_dir=str(checkpoint_dir),
        checkpoint_freq=2,
        save_best=True,
        val_texts=val_texts if len(val_texts) > 0 else None,
    )

    best_model_path = checkpoint_dir / "best_model.pt"
    if best_model_path.exists():
        print(f"Loading best checkpoint from {best_model_path}")
        QWEN3_SAE_Trainer.sae = load_pretrained(
            str(best_model_path),
            device=QWEN3_SAE_Config.device,
        )
    else:
        print("Best checkpoint not found; exporting last-epoch weights.")

    QWEN3_SAE = QWEN3_SAE_Trainer.sae

    # Save model:
    model_path = f'sae_core/pretrained_models/{MODEL_ID}.{QWEN3_SAE_Trainer.hook_spec}.btop{topk}sae.all_science.exp{sae_expansion}'
    # model_path = f'sae_core/smoke_test_early_stopping'

    QWEN3_SAE_Trainer.sae.save(model_path, history=history)

    print("Training Complete!")

    print("\n=== Final Statistics ===")
    print(f"Final Loss: {history['loss'][-1]:.4f}")
    print(f"Final Reconstruction Loss: {history['recon_loss'][-1]:.4f}")
    print(f"Final Sparsity: {history['sparsity'][-1]:.4f}")
    if 'val_loss' in history:
        print(f"Final Val Loss: {history['val_loss'][-1]:.4f}")
        print(f"Final Val Reconstruction Loss: {history['val_recon_loss'][-1]:.4f}")
        print(f"Final Val Sparsity: {history['val_sparsity'][-1]:.4f}")
    print(f"Final Dead Features: {history['dead_features'][-1]} ({history['dead_feature_percentage'][-1]:.2f}%)")

    print("\n=== Dead Feature Trends ===")
    print("Epoch | Dead Features | Percentage")
    for epoch, (dead_count, dead_pct) in enumerate(zip(history['dead_features'], history['dead_feature_percentage']), 1):
        print(f"{epoch:5d} | {dead_count:13d} | {dead_pct:9.2f}%")

    print("\n=== Saved Files ===")
    print(f"Final model: {model_path}")
    print(f"Checkpoints: {checkpoint_dir}")
    if checkpoint_dir.exists():
        checkpoints = sorted(checkpoint_dir.glob("*.pt"))
        for ckpt in checkpoints:
            print(f"  - {ckpt.name}")

if __name__ == "__main__":
    main()
