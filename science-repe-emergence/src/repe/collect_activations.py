"""Phase 7 — Collect last-token hidden states for Source A + Source B and merge.

Source A — vgel-style: textbook suffixes from
data/repe_suffixes/science_suffix_bank.jsonl, persona swap is the only
varying part. Build pairs via make_dataset.make_dataset() with truncation
augmentation.

Source B — GPT-style: positive/negative texts from
data/processed/train.jsonl wrapped in the neutral_text template.

For each pair:
  - run forward pass with output_hidden_states=True under torch.no_grad()
  - grab the LAST-token hidden state at every layer
  - compute diff = h_pos[layer][-1] - h_neg[layer][-1]
  - tag every diff with source = "source_a_vgel" or "source_b_gpt"
  - save diffs by default (--save_raw to keep raw activations too)

Supports source ablations: Source A only, Source B only, Source A+B combined.

CLI:
  python -m src.repe.collect_activations \\
      --model Qwen/Qwen3-0.6B-Base \\
      --source_a_suffixes data/repe_suffixes/science_suffix_bank.jsonl \\
      --source_b_dataset data/processed/train.jsonl \\
      --output outputs/activations/qwen3_0.6b/train.pt \\
      --prompt_mode science_persona \\
      --truncation_levels 10
"""
