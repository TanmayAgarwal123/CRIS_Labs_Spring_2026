"""Score a held-out test set against per-layer LAT vectors.

For each pair:
  score_pos = dot(h_pos_layer, v_layer)
  score_neg = dot(h_neg_layer, v_layer)
  correct  = score_pos > score_neg

Reports per-layer pairwise accuracy, AUC, mean +/- scores, margin, best layer.
Writes JSON to --output. Also supports cross-dataset and paraphrase-test eval
(point --dataset at the relevant JSONL).

CLI:
  python -m src.repe.evaluate_reading_vectors \\
      --model Qwen/Qwen3-0.6B \\
      --vectors outputs/vectors/qwen3_0.6b/concept_correct_vs_misconception_lat.pt \\
      --dataset data/processed/test.jsonl \\
      --output outputs/evaluations/qwen3_0.6b_concept_test.json
"""
