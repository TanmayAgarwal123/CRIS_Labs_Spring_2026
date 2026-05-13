# CLAUDE.md — RepE Science Emergence

Persistent project memory. Update as steps complete.

## Project objective

Test whether natural-science reasoning representations become more linearly
readable, robust, and behaviorally controllable across Qwen3 model scale,
via Representation Engineering (LAT-style reading + control vectors). No
fine-tuning of Qwen3.

Three claims:
1. **Reading** — a linear direction separates correct/mechanistic from
   flawed/surface scientific reasoning.
2. **Control** — adding/subtracting that direction during generation changes
   scientific-explanation behavior.
3. **Scaling** — readability/control behavior changes across Qwen3 sizes.

Framing for the report: representations associated with scientific reasoning
become more linearly decodable, robust to paraphrase, and steerable across
scale. Never claim the model "understands" science.

## 40-Hour Sprint Scope (ACTIVE — read first)

```text
TEXTBOOK INPUTS (the only source for the MVP):
  data/preprocessed/processed_textbook_physics.json
  data/preprocessed/processed_textbook_chemistry.json
  data/preprocessed/processed_textbook_biology.json

DATASETS:
  Source A — vgel/repeng-style textbook suffix pairs
    - identical suffix in positive/negative; only persona phrase changes
    - primary RepE/LAT training signal
  Source B — GPT-generated contrast pairs (~165 total)
    - concept_correct_vs_misconception     (~55)
    - mechanistic_explanation_vs_surface   (~55)
    - counterfactual_reasoning             (~55)

SKIP:
  math_formal_reasoning, transfer_application,
  cross_domain_scientific_reasoning, notebooks (until script pipeline runs).

MODELS (in order, stop when out of time/memory):
  1. Qwen/Qwen3-0.6B-Base   (required first run)
  2. Qwen/Qwen3-1.7B-Base   (required second run)
  3. Qwen/Qwen3-4B-Base     (strong target, time/memory permitting)
  4. Qwen/Qwen3-8B-Base     (optional, >=24GB)
  5. Qwen/Qwen3-14B-Base    (optional, >=40GB)

CONTROL GENERATION:
  - One model only (1.7B or 4B).
  - 10 prompts x 5 coefficients = 50 generations.
    (3 physics + 3 chemistry + 2 biology + 2 math; user override keeps math
     even though new AGENTS.md says phys/chem/bio only.)

SAE BRIDGE (REQUIRED):
  - Existing 1.7B SAEs at CRISMechInterp/Qwen3_SAEs (btop128 + btop256,
    hook_resid_post middle layer, expansion 4).
  - Cosine of LAT vector vs every SAE decoder row; top-k features (k=20)
    + alignment-spectrum plot; btop128-vs-btop256 split analysis.
```

## Phase map (target order)

```
Phase 1  extract_textbook_text         (3 JSON inputs -> textbook_text.json)
Phase 2  build_repe_suffix_bank        (curate ~300-360 high-quality suffixes)
Phase 3  build_source_a_prompt_preview (debug/inspection JSONL + report)
Phase 4  extract_textbook_concepts     (~25 concepts/domain via GPT)
Phase 5  generate_contrast_pairs       (3 Source B JSONLs)
Phase 6  validate_dataset + split_dataset
Phase 7  collect_activations           (Source A + Source B merged)
Phase 8  train_lat_vectors             (PCA per layer)
Phase 9  evaluate_reading_vectors      (acc / AUC / margin / paraphrase / cross)
Phase 10 run_control_generation        (coefficient sweep)
Phase 11 evaluate_generations          (LLM-judge rubric)
Phase 12 sae_alignment                 (REQUIRED — SAE bridge)
Phase 13 plot_scaling_trends           (bootstrap CIs)
Phase 14 build_report
```

## Directory structure (target)

```
science-repe-emergence/
  README.md  AGENTS.md  CLAUDE.md  requirements.txt  .env.example  .env(gitignored)

  data/
    preprocessed/                      # 3 processed_textbook_*.json
    extracted/                         # textbook_text.json, textbook_concepts.json
    repe_suffixes/                     # science_suffix_bank.jsonl,
                                       # source_a_vgel_pairs_preview.jsonl
    generated/                         # 3 Source B contrast-pair JSONLs
    processed/                         # all_pairs.jsonl, train/val/test/paraphrase

  src/
    data/    extract_textbook_text  build_repe_suffix_bank
             build_source_a_prompt_preview  extract_textbook_concepts
             generate_contrast_pairs  validate_dataset  split_dataset
    repe/    model_loader  prompt_templates  make_dataset
             collect_activations  train_lat_vectors
             evaluate_reading_vectors  control_model  run_control_generation
    analysis/ evaluate_generations  plot_layer_scores  plot_scaling_trends
              compare_vector_alignment  sae_alignment  build_report
    utils/   io  logging  openai_client  seed

  configs/  models.yaml dataset_generation.yaml repe.yaml control_prompts.yaml
  outputs/  activations vectors generations evaluations plots sae_alignment
            reports runs
```

## Schemas (single source of truth)

**Source A pair (data/repe_suffixes/source_a_vgel_pairs_preview.jsonl)**:
```
pair_id, source="vgel_textbook_suffix", dataset, domain, suffix_id,
positive_persona, negative_persona, positive_prompt, negative_prompt,
suffix, suffix_identical (true)
```

**Source B pair (data/generated/*.jsonl)**:
```
pair_id, source="gpt_generated_contrast", dataset, domain,
textbook=<domain>, chapter_or_section, concept,
positive, negative, positive_label=1, negative_label=0,
reasoning_type, difficulty, shared_anchors, notes
```
(no `split` at this stage — assigned in Phase 6)

**Suffix bank entry (data/repe_suffixes/science_suffix_bank.jsonl)**:
```
suffix_id, domain, source_chunk_id, chapter_or_section, text,
approx_token_count, quality_score, why_selected
```

**Textbook chunk (data/extracted/textbook_text.json)**:
```
chunk_id, domain, source_file, chapter_or_section, text,
char_count, approx_token_count
```

## Prompt templates / persona labels

```python
TEMPLATES = {
  "science_persona":     "Consider the following scientific text, interpreted by someone with {persona}.\n\n{suffix}",
  "mechanistic_persona": "The following scientific text is being interpreted by someone with {persona}.\n\n{suffix}",
  "neutral_text":        "Consider the following scientific statement:\n\n{text}\n\nAnalysis:",
}
PERSONA_LABELS["concept_correct_vs_misconception"] uses science_persona.
PERSONA_LABELS["mechanistic_explanation_vs_surface"] uses mechanistic_persona.
PERSONA_LABELS["counterfactual_reasoning"]         uses mechanistic_persona.
```

## Key invariants / do-not-do

- Never fine-tune Qwen3.
- Source A: positive suffix == negative suffix (verify exact string equality).
- Source B: never copy or closely paraphrase textbook sentences.
- Activation collection: torch.no_grad, model.eval, output_hidden_states=True,
  collect last-token hidden state per layer, save diffs by default.
- Default control layers: [0.45L, 0.55L, 0.65L, 0.75L].
- Never compare dense LAT vectors across model sizes (Qwen3 hidden dims
  differ across scale). Use SAE-feature matching for cross-size.
- Bootstrap CIs (N_boot=1000) on every accuracy / AUC / margin in the report.
- Math IS in scope (user override): math control prompts kept; future Source B
  math contrast datasets to be generated WITHOUT a math textbook input
  (use built-in concept seeds, same generator path as the other Source B sets).
- Do not start large model downloads before Source A and Source B dataset
  reports exist.

## Status / progress log

- 2026-05-12: Read original AGENTS.md. Wrote first CLAUDE.md, scaffolded full
  repo, verified OpenAI key, generated initial 50-pair dataset (old schema).
- 2026-05-13: AGENTS.md updated (1223 lines, was 2273). Major changes:
  three JSON-only textbook inputs; new repe_suffixes/ folder + 2 new scripts
  (build_repe_suffix_bank, build_source_a_prompt_preview); Source B rows now
  carry a `source` field and drop `split` at generation; control prompts are
  phys/chem/bio only. CLAUDE.md and configs updated to match.
- 2026-05-13: Re-scaffolded — added new stubs, updated configs and templates,
  removed math prompts from control_prompts.yaml.
- 2026-05-13: Re-verified OpenAI key (cheap gpt-4.1-mini call, 5 max_tokens).
- 2026-05-13: Regenerated 50 concept_correct_vs_misconception pairs to the
  new schema (added `source`, `textbook=<domain>`, dropped `split`).
- 2026-05-13: Refactored generate_contrast_pairs.py into a 4-dataset registry
  (concept_correct, mechanistic, counterfactual, math) with --dataset CLI
  flag and --skip-if-exists default. SCIENCE_CONCEPTS shared by the first 3;
  MATH_CONCEPTS (15 entries) drives math_formal_reasoning. Per-dataset
  positive/negative descriptions + few-shot examples (catalysts for
  mechanistic, osmosis for counterfactual) baked into the prompt.
- 2026-05-13: Generated 3 missing Source B datasets at n=55 each (parallel
  background jobs). All hit target.
    mechanistic_explanation_vs_surface  55 kept / 27 dropped
    counterfactual_reasoning            55 kept /  4 dropped
    math_formal_reasoning               55 kept / 25 dropped
  Source B totals so far: 50 + 55 + 55 + 55 = 215 pairs across 4 datasets.
  concept_correct_vs_misconception is still 50 (kept per user); could be
  topped up to 55 if needed for parity.
- 2026-05-13: Phase 1 — extract_textbook_text. 21,361 chunks kept after
  normalize/min80/dedupe (physics 8683 / chemistry 5920 / biology 6758).
  Output: data/extracted/textbook_text.json.
- 2026-05-13: Phase 2 — build_repe_suffix_bank. 360 suffixes selected
  (120 per domain; mean tokens phys 39.5 / chem 37.7 / bio 42.8). Filter
  excludes markdown headers, list markers, citation prefixes; score weights
  token band, verb hint, technical term, no-citation, terminal punctuation.
  Output: data/repe_suffixes/science_suffix_bank.jsonl.
- 2026-05-13: Phase 3 — generate_source_a_pairs. Loaded Qwen3-1.7B and 4B
  tokenizers, asserted vocab + token-id equality on probes (vocab=151643).
  8,637 vgel-style pairs written (2,879 per dataset; near-balanced across
  3 domains). Suffix-identical invariant verified globally (0 mismatches
  across 2,879 (suffix_id, trunc_length) groups). 3 missing pairs from the
  8,640 maximum due to one suffix whose truncation lengths deduped to 7
  unique values instead of 8. Output: data/repe_suffixes/source_a_pairs.jsonl.

- 2026-05-13: Quality cleanup of suffix bank per user (limited compute budget,
  every datapoint must be high quality). Tightened Phase 2 filter (drop
  fragments <25 tok, anaphoric starts, figure/table/equation refs, URLs,
  pedagogical scaffolding "First we draw..." / "Notice that..." /
  "you/we will...") and added a parallel gpt-4.1-mini keep/drop judge by
  default (--no_llm_judge to skip). Heuristic kept 701, judge kept 201
  (drop rate 71%). Final bank: physics 73 / chemistry 49 / biology 79.
  Regenerated source_a_pairs.jsonl → 4,824 pairs (1,608 per dataset;
  by domain bio 1896 / phys 1752 / chem 1176).
  - Diagnostics on the cleaned bank: 0 short, 0 no-punct, 0 anaphoric starts,
    0 meta references — all clean.
  - Chemistry came in lowest (49) — the chemistry textbook chunks have a
    higher rate of inline figure/equation references and pedagogical
    scaffolding. If chem coverage matters more than the strict "no figure
    refs" rule, relax PEDAGOGICAL_REFERENCES or META_REFERENCES and re-run.

- 2026-05-13: Widened the funnel to recover chemistry coverage:
  - Hard filter relaxed to char [100,400] and tok [20,80] (was [120,350]/[25,60])
  - Default min_quality_score: 0.0 (was 0.6 — judge sees every hard-pass)
  - Default judge_pool_factor: 5 (was 3)
  - Judge drops now logged to outputs/runs/suffix_bank_drops.jsonl
  - Result: 1,597 candidates → 567 kept (35.5% vs prior 28.7%).
    Final bank: physics 120 / chemistry 120 / biology 120 = 360 suffixes.
  - Source A pairs regenerated: 8,640 (2,880 per dataset, 2,880 per domain,
    perfectly balanced). 7 chemistry entries are 20–25 tokens — concise
    definitions, not fragments.

- 2026-05-13: Phase 6 — validate + split.
  - validate_dataset.py: 215 -> 212 pairs (3 dropped, all
    counterfactual_reasoning, all for pos/neg TF-IDF cosine > 0.85 — pos
    and neg of those pairs differed only by a couple of reasoning words
    while sharing the "If X, then Y because Z" frame).
    Drops -> outputs/runs/dataset_generation_drops.jsonl.
    Generated JSONLs were overwritten in place with passing pairs only.
  - split_dataset.py: stratified 70/15/15 by (dataset, domain), seed=42.
    Final: 147 train / 32 val / 33 test.
    Per-dataset training counts: concept_correct=35, counterfactual=36,
    math=38, mechanistic=38. ALL >= 30 -> LAT stability concern not raised.
  - paraphrase_test.jsonl: 30 pairs (target was 40). Test sets per dataset
    were too small to source 10 paraphrases each (only 7-9 available);
    additionally 3 paraphrases never validated after 3 retries each
    (2 counterfactual, 1 mechanistic). Ratios kept: concept 7/7,
    counterfactual 6/8, math 9/9, mechanistic 8/9.
  - If a full 40-pair paraphrase set matters, easiest fix is to grow
    Source B (e.g. 80+ pairs per dataset) before re-running Phase 6,
    so 15% test = at least 12 pairs per dataset.

- 2026-05-13: Grew Source B to n=80 per dataset (was 50/52/55/55). Added
  --append mode to generate_contrast_pairs.py: reads existing JSONL, seeds
  per-concept seq counter from existing pair_ids, generates only the missing
  pairs. All 4 datasets topped up in parallel (concept_correct +30 with 24
  drops; mechanistic +25 with 7 drops; counterfactual +28 with 2 drops;
  math +25 with 7 drops).
- 2026-05-13: Re-ran Phase 6 on the grown Source B.
  - validate: 320 -> 319 (1 counterfactual pos/neg TF-IDF dup).
  - split: 222 train / 46 val / 51 test.
    train per-dataset: concept 55, counterfactual 55, math 56, mechanistic 56.
    All well above the 30-pair LAT-stability floor.
  - paraphrase_test.jsonl: 37 pairs.
    concept_correct 10/10, counterfactual 10/10, math 10/10,
    mechanistic 7/10 (3 paraphrases never validated after 3 retries).
  - 37/40 is close to the AGENTS.md target; could push to 40 with
    --max_paraphrase_retries 5 if the gap matters.

- 2026-05-13: Audited `colab_repe_pipeline.ipynb` against the Phase 7-13
  AGENTS.md specs and the current script state. Edits applied (all in
  notebook only — no code executed locally):
  - Cell 3: install from a complete dep list (was missing pyyaml, matplotlib,
    tqdm, pydantic).
  - Cell 4: also load GITHUB_TOKEN (cell 34 push needs it); gracefully tolerate
    absence.
  - Cell 8: pre-flight now imports each Phase 7+ module and asserts
    `callable(main)` — catches the stub-script case before any !python -m
    call silently no-ops.
  - Cell 10: added `0.6B` to MODEL_MAP (AGENTS.md spec lists it as the
    required first run).
  - Cell 11: `--dataset` → `--source_b_dataset`, `--source_a` →
    `--source_a_pairs` (consume Phase 3's precomputed
    `data/repe_suffixes/source_a_pairs.jsonl` so we don't re-tokenize),
    dropped `--prompt_mode` (templates are baked into each source).
  - Cell 12 (val) and Cell 13 (test/paraphrase): removed Source A from the
    invocation — val and test are evaluated on Source B contrast pairs only.
    Replaced the `--source_a none` placeholder with simply omitting the flag.
  - Cell 24: `--generations` → `--input` (AGENTS.md Phase 11 spec name).

- CRITICAL CALLOUT: Every Phase 7+ Python script the notebook invokes is
  STILL A DOCSTRING-ONLY STUB (no `def main()`). The notebook will fail at
  the new Cell 8 pre-flight check until those are implemented and pushed.
  Stubs to fill in: src/repe/{collect_activations, train_lat_vectors,
  evaluate_reading_vectors, run_control_generation, control_model,
  model_loader, make_dataset}.py and src/analysis/{evaluate_generations,
  sae_alignment, plot_scaling_trends}.py.

## Tokenizer cache

- Qwen3-1.7B-Base and Qwen3-4B-Base tokenizer files (no weights) were
  downloaded by Phase 3 to the default HF cache (~/.cache/huggingface).
  These two tokenizers are byte-identical (vocab 151643).

## Environment notes

- Python: `../.venv/bin/python` (Python 3.12) with openai 2.36.0 +
  python-dotenv installed in the parent project venv.
- HF_TOKEN is in `.env` but unused so far (no model downloads yet).
- No torch / transformers / Qwen3 weights exercised yet. Per spec: do not
  download large models before Source A and Source B dataset reports exist.

## Next step

- Stop. Awaiting user's go-ahead before scaling to the full 165-pair Source B,
  building the suffix bank, or running any forward passes.
