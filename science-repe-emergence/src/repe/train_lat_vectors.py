"""Phase 8 — Train per-layer LAT vectors via PCA on diff activations.

For each (model, dataset, source_setting, layer):
  - load positive-minus-negative diff vectors
  - PCA(n_components=1)
  - normalize the principal component
  - sign-flip if validation accuracy points negative; record which layers flipped
  - save vector, explained variance, pair count, skipped pairs, mean diff norm

Saves a .pt file per dataset of the form:
  {
    "model_name": str,
    "dataset": str,
    "source_setting": "source_a" | "source_b" | "combined",
    "layers": list[int],
    "vectors": Tensor[num_layers, hidden_dim],
    "pca_explained_variance": list[float],
    "flipped_layers": list[int],
    "metadata": dict,
  }

CLI:
  python -m src.repe.train_lat_vectors \\
      --activations outputs/activations/qwen3_0.6b/train.pt \\
      --output outputs/vectors/qwen3_0.6b
"""
