"""Phase 3 — Source A prompt preview (debug/inspection).

For each Source A dataset (concept_correct_vs_misconception,
mechanistic_explanation_vs_surface, counterfactual_reasoning), wrap each
selected suffix from the suffix bank in BOTH the positive- and
negative-persona templates and write one JSONL row per pair. Verifies
suffix exact-string equality and sets suffix_identical=true only after
verification.

Also writes a markdown report summarizing raw chunk counts, kept suffix
counts by domain, average suffix length, preview-pair counts, and three
inspected positive/negative prompt pairs.

Do NOT precompute the full truncation-augmented dataset here — that lives
in Phase 7 (collect_activations).

Output JSONL row:
  {pair_id, source="vgel_textbook_suffix", dataset, domain, suffix_id,
   positive_persona, negative_persona, positive_prompt, negative_prompt,
   suffix, suffix_identical}

CLI:
  python -m src.data.build_source_a_prompt_preview \\
      --suffix_bank data/repe_suffixes/science_suffix_bank.jsonl \\
      --output data/repe_suffixes/source_a_vgel_pairs_preview.jsonl \\
      --report outputs/reports/source_a_dataset_report.md \\
      --examples_per_dataset 30
"""
