from sae_core.sae_base import SAE
import torch

model_path = "/home/ubuntu/SAELens/sae_core/pretrained_models/qwen3_06B.blocks.14.hook_mlp_out.sae"

# Load the model with history
loaded_sae, history = SAE.load(model_path, device="cuda", load_history=True)

print(f"✓ Loaded SAE with {loaded_sae.cfg.d_sae} features")
print(f"✓ Input dimension: {loaded_sae.cfg.d_in}")

if history:
    print(f"\n✓ Training history available:")
    print(f"  - Final loss: {history['loss'][-1]:.4f}")
    print(f"  - Final sparsity: {history['sparsity'][-1]:.4f}")

# Test it
test_activation = torch.randn(1, loaded_sae.cfg.d_in, device="cuda")
reconstruction, features = loaded_sae(test_activation)

print(f"\n✓ Input shape: {test_activation.shape}")
print(f"✓ Reconstruction shape: {reconstruction.shape}")
print(f"✓ Features shape: {features.shape}")
print(f"✓ Active features: {(features > 0).sum().item()}/{features.shape[1]}")