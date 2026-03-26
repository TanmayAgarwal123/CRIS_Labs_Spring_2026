from sae_core.full_analysis import SAEAnalyzer
from transformer_lens import HookedTransformer
from sae_core.data_processing.textbook_process import load_processed_data
import torch

def get_compute_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"

MODEL_NAME = "qwen3-0.6b"
SAE_PATH = 'Qwen_Qwen3-0.6B.blocks.9.hook_resid_post.btop128sae.all_science.exp4'
DEVICE = get_compute_device()
TORCH_DTYPE = torch.float16 if DEVICE in {"cuda", "mps"} else torch.float32
DTYPE_STR = str(TORCH_DTYPE).replace("torch.", "")
NUM_DEVICES = torch.cuda.device_count() if DEVICE == "cuda" else 1

FROM_PRETRAINED_KWARGS = {
    "trust_remote_code": True,
    "torch_dtype": TORCH_DTYPE,
}
if NUM_DEVICES > 1:
    FROM_PRETRAINED_KWARGS["device_map"] = "auto"


model = HookedTransformer.from_pretrained(
        MODEL_NAME,
        device=DEVICE,
        dtype=DTYPE_STR,
        n_devices=max(1, NUM_DEVICES),
        **FROM_PRETRAINED_KWARGS,
    )

texts = load_processed_data("sae_core/data/processed_data/processed_textbooks_all.json")
analyzer = SAEAnalyzer(model, sae_path=SAE_PATH, layer=9, hook_name="hook_resid_post", dataset=texts)

sparsity_metrics, feature_freq = analyzer.compute_sparsity_metrics(batch_size=16)
dead_feature_stats = analyzer.find_dead_features(feature_freq)
ablation_metrics = analyzer.ablation_study(batch_size=4)
