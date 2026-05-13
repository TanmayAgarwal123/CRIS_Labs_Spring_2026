# AGENTS.md — RepE Science Emergence Project

## Project Objective

Build a research codebase that tests whether **natural-science reasoning representations become more linearly readable, robust, and controllable across Qwen3 model scale**.

Use Representation Engineering / LAT-style activation analysis. Do **not** fine-tune Qwen3 models.

The project tests three claims:

1. **Reading:** a linear direction can distinguish correct/mechanistic scientific reasoning from flawed/surface reasoning.
2. **Control:** adding or subtracting that direction during generation changes scientific-explanation behavior.
3. **Scaling:** the readability/control behavior changes across Qwen3 model sizes.

Correct framing:

```text
We test whether representations associated with scientific reasoning become more
linearly decodable, robust to paraphrase, and steerable across Qwen3 scale.
```

Avoid:

```text
We prove that models understand science.
```

---

## 40-Hour Sprint Scope — Read First

This is a tight MVP. Do not expand scope until the required pipeline works end-to-end.

```text
TEXTBOOK INPUTS:
  Use these processed JSON files as the primary textbook source:
    data/preprocessed/processed_textbook_physics.json
    data/preprocessed/processed_textbook_chemistry.json
    data/preprocessed/processed_textbook_biology.json

DATASETS TO BUILD:
  Source A — vgel/repeng-style textbook suffix pairs
    - textbook suffix is identical in positive/negative prompts
    - only the persona/framing phrase changes
    - used as the primary RepE/LAT training signal

  Source B — GPT-generated contrast pairs
    - concept_correct_vs_misconception     (~55 pairs)
    - mechanistic_explanation_vs_surface   (~55 pairs)
    - counterfactual_reasoning             (~55 pairs)
    - total target: ~165 pairs

SKIP:
  - math_formal_reasoning
  - transfer_application
  - cross_domain_scientific_reasoning
  - notebooks unless the script pipeline already works

MODELS:
  1. Qwen/Qwen3-0.6B-Base    required first run
  2. Qwen/Qwen3-1.7B-Base    required second run
  3. Qwen/Qwen3-4B-Base      strong target if time/memory permits
  4. Qwen/Qwen3-8B-Base      optional, needs >=24GB
  5. Qwen/Qwen3-14B-Base     optional, needs >=40GB

CONTROL GENERATION:
  - one model only, preferably 1.7B or 4B
  - 8 prompts x 5 coefficients = 40 generations

SAE BRIDGE:
  - required
  - use existing Qwen3-1.7B SAEs at CRISMechInterp/Qwen3_SAEs
  - btop128 + btop256, hook_resid_post middle layer, expansion 4
  - compute cosine between LAT vector and every SAE decoder row
  - save top-k aligned features and alignment-spectrum plot
```

---

## Research Question

```text
Do scientific-reasoning representations become more linearly readable, robust,
and behaviorally controllable as Qwen3 model size increases?
```

Operational definitions:

```text
positive = correct, mechanistic, conceptually sound explanation
negative = plausible misconception, shallow explanation, or flawed reasoning
```

---

## Repository Structure

```text
science-repe-emergence/
  README.md
  AGENTS.md
  CLAUDE.md
  requirements.txt
  .env.example
  .env                         # gitignored

  data/
    preprocessed/
      processed_textbook_physics.json
      processed_textbook_chemistry.json
      processed_textbook_biology.json

    extracted/
      textbook_text.json
      textbook_concepts.json

    repe_suffixes/
      science_suffix_bank.jsonl
      source_a_vgel_pairs_preview.jsonl

    generated/
      concept_correct_vs_misconception.jsonl
      mechanistic_explanation_vs_surface.jsonl
      counterfactual_reasoning.jsonl

    processed/
      all_pairs.jsonl
      train.jsonl
      val.jsonl
      test.jsonl
      paraphrase_test.jsonl

  src/
    data/
      extract_textbook_text.py
      build_repe_suffix_bank.py
      build_source_a_prompt_preview.py
      extract_textbook_concepts.py
      generate_contrast_pairs.py
      validate_dataset.py
      split_dataset.py

    repe/
      model_loader.py
      prompt_templates.py
      make_dataset.py
      collect_activations.py
      train_lat_vectors.py
      evaluate_reading_vectors.py
      control_model.py
      run_control_generation.py

    analysis/
      evaluate_generations.py
      plot_layer_scores.py
      plot_scaling_trends.py
      compare_vector_alignment.py
      sae_alignment.py
      build_report.py

    utils/
      io.py
      logging.py
      openai_client.py
      seed.py

  configs/
    models.yaml
    dataset_generation.yaml
    repe.yaml
    control_prompts.yaml

  outputs/
    activations/
    vectors/
    generations/
    evaluations/
    plots/
    sae_alignment/
    reports/
    runs/
```

---

## Environment

Create `.env.example`:

```bash
OPENAI_API_KEY=your_key_here
HF_TOKEN=optional_huggingface_token_here
```

Do not hardcode API keys.

`requirements.txt` should include:

```text
torch
transformers
accelerate
bitsandbytes
scikit-learn
numpy
pandas
matplotlib
tqdm
pydantic
python-dotenv
openai
sentencepiece
protobuf
huggingface_hub
```

---

## Dataset Overview

This project uses **two complementary dataset sources**.

### Source A — vgel/repeng-style textbook suffix pairs

Primary RepE training source.

```text
positive prompt = template with positive persona + same suffix
negative prompt = template with negative persona + same suffix
```

The suffix is identical. Only the persona/framing phrase changes. This controls for topic, length, domain, and wording.

Example:

```text
Positive:
Consider the following scientific text, interpreted by someone with a precise
and accurate understanding of this scientific concept.

When two carts collide on a nearly frictionless track, the forces they exert on
each other are equal in magnitude and opposite in direction during the collision.

Negative:
Consider the following scientific text, interpreted by someone with a common
misconception about this scientific concept.

When two carts collide on a nearly frictionless track, the forces they exert on
each other are equal in magnitude and opposite in direction during the collision.
```

### Source B — GPT-generated contrast pairs

Secondary source for explicit concept coverage and held-out evaluation.

Each row contains one positive and one negative example about the same concept.

```json
{
    "pair_id": "physics_momentum_001",
    "source": "gpt_generated_contrast",
    "dataset": "concept_correct_vs_misconception",
    "domain": "physics",
    "textbook": "physics",
    "chapter_or_section": "unknown",
    "concept": "conservation_of_momentum",
    "positive": "In an isolated collision, total momentum stays constant because the internal forces between objects are equal and opposite, so no external force changes the system's total momentum.",
    "negative": "In an isolated collision, total momentum stays constant because the heavier object keeps most of the motion and passes some of it to the lighter object.",
    "positive_label": 1,
    "negative_label": 0,
    "reasoning_type": "conceptual",
    "difficulty": "intro",
    "shared_anchors": ["isolated collision", "total momentum"],
    "notes": "negative reflects heavier-object dominance misconception"
}
```

---

## Textbook Use Policy

Source A may use textbook chunks directly as suffixes because the positive/negative distinction comes only from persona framing.

Source B must **not** copy or closely paraphrase textbook sentences. Use textbooks only to identify:

```text
1. domains
2. concepts
3. vocabulary level
4. common misconception areas
5. mechanistic/counterfactual axes
```

---

# Phase 1 — Extract Textbook Text

Use the three processed JSON files only for the MVP.

Command:

```bash
python -m src.data.extract_textbook_text \
  --json_inputs \
    data/preprocessed/processed_textbook_physics.json \
    data/preprocessed/processed_textbook_chemistry.json \
    data/preprocessed/processed_textbook_biology.json \
  --output data/extracted/textbook_text.json \
  --dedupe_by_hash true
```

`extract_textbook_text.py` must support JSON files shaped as either:

```text
1. list[str]
2. list[dict] with one of: text, content, paragraph, chunk, body
```

For each chunk:

```json
{
    "chunk_id": "physics_json_000001",
    "domain": "physics",
    "source_file": "processed_textbook_physics.json",
    "chapter_or_section": "unknown",
    "text": "...",
    "char_count": 1234,
    "approx_token_count": 210
}
```

Rules:

```text
- infer domain from filename: physics/phys, chemistry/chem, biology/bio
- normalize whitespace
- drop chunks shorter than 80 characters
- drop obvious junk: page numbers, copyright text, answer keys, index fragments,
  glossary-only fragments, table-only fragments, references
- deduplicate with md5(normalized_text)
- preserve chapter/section if present in the JSON object; otherwise use "unknown"
- print raw/kept/dropped/deduped counts per domain
```

---

# Phase 2 — Build Source A Suffix Bank

Command:

```bash
python -m src.data.build_repe_suffix_bank \
  --input data/extracted/textbook_text.json \
  --output data/repe_suffixes/science_suffix_bank.jsonl \
  --max_per_domain 120 \
  --min_tokens 40 \
  --max_tokens 180
```

Select high-quality suffixes for vgel-style prompt pairs.

Prefer chunks that are:

```text
- explanatory
- causal
- mechanistic
- counterfactual
- concept-rich
```

Prioritize chunks containing terms like:

```text
because, therefore, causes, results in, depends on, increases, decreases,
changes, leads to, equilibrium, gradient, force, energy, momentum,
concentration, membrane, enzyme, selection, reaction, field, pressure,
diffusion, osmosis, conservation, rate
```

Avoid:

```text
- isolated equations
- captions
- tables
- exercise-only chunks
- answer keys
- glossary-only definitions
- lists with no explanation
```

Output JSONL schema:

```json
{
    "suffix_id": "physics_suffix_000001",
    "domain": "physics",
    "source_chunk_id": "physics_json_000123",
    "chapter_or_section": "unknown",
    "text": "...",
    "approx_token_count": 92,
    "quality_score": 4,
    "why_selected": "causal/mechanistic explanation"
}
```

Target:

```text
~100-120 suffixes per domain
~300-360 suffixes total
```

---

# Phase 3 — Build Source A Prompt Preview

This is a debug/inspection file. Do not precompute the full truncation-augmented dataset here.

Command:

```bash
python -m src.data.build_source_a_prompt_preview \
  --suffix_bank data/repe_suffixes/science_suffix_bank.jsonl \
  --output data/repe_suffixes/source_a_vgel_pairs_preview.jsonl \
  --report outputs/reports/source_a_dataset_report.md \
  --examples_per_dataset 30
```

The report should summarize raw chunk counts, kept suffix counts by domain, average suffix length, preview-pair counts, and three inspected positive/negative prompt pairs.

Datasets:

```text
concept_correct_vs_misconception
mechanistic_explanation_vs_surface
counterfactual_reasoning
```

Output schema:

```json
{
    "pair_id": "sourceA_physics_000001_concept_correct_vs_misconception",
    "source": "vgel_textbook_suffix",
    "dataset": "concept_correct_vs_misconception",
    "domain": "physics",
    "suffix_id": "physics_suffix_000001",
    "positive_persona": "a precise and accurate understanding of this scientific concept",
    "negative_persona": "a common misconception about this scientific concept",
    "positive_prompt": "...",
    "negative_prompt": "...",
    "suffix": "...",
    "suffix_identical": true
}
```

Set `suffix_identical=true` only after exact string equality is verified for the suffix portion.

---

## Source A Prompt Templates

Implement in `src/repe/prompt_templates.py`.

```python
TEMPLATES = {
    "science_persona": "Consider the following scientific text, interpreted by someone with {persona}.\n\n{suffix}",
    "mechanistic_persona": "The following scientific text is being interpreted by someone with {persona}.\n\n{suffix}",
    "neutral_text": "Consider the following scientific statement:\n\n{text}\n\nAnalysis:",
}

PERSONA_LABELS = {
    "concept_correct_vs_misconception": {
        "template": "science_persona",
        "positive": "a precise and accurate understanding of this scientific concept",
        "negative": "a common misconception about this scientific concept",
    },
    "mechanistic_explanation_vs_surface": {
        "template": "mechanistic_persona",
        "positive": "a deep understanding of the underlying causal mechanism",
        "negative": "a shallow, surface-level pattern-matching understanding",
    },
    "counterfactual_reasoning": {
        "template": "mechanistic_persona",
        "positive": "careful reasoning about how changing one variable affects the system",
        "negative": "incorrectly applying a memorized rule without adjusting for the changed condition",
    },
}
```

Personas should be parallel and should differ only in the intended reasoning property.

---

## Source A Truncation Augmentation

Implement in `src/repe/make_dataset.py`.

For each suffix:

```text
1. tokenize suffix with the Qwen tokenizer
2. drop the last 5 tokens
3. create 10 prefix truncations from ~20% to ~95% of remaining length
4. for each truncation, create positive/negative prompts using the same truncated suffix
5. return prompt pairs for activation collection
```

Core invariant:

```text
positive suffix == negative suffix
```

Suggested dataclass:

```python
@dataclass
class DatasetEntry:
    pair_id: str
    dataset: str
    source: str
    positive: str
    negative: str
    metadata: dict
```

---

# Phase 4 — Extract Concepts for Source B

Command:

```bash
python -m src.data.extract_textbook_concepts \
  --input data/extracted/textbook_text.json \
  --output data/extracted/textbook_concepts.json \
  --model gpt-4.1-mini \
  --concepts_per_domain 25
```

Each concept:

```json
{
    "concept_id": "physics_conservation_of_momentum",
    "domain": "physics",
    "concept_name": "conservation of momentum",
    "chapter_or_section": "unknown",
    "one_line_definition": "...",
    "mechanistic_core": "...",
    "common_misconception": "...",
    "counterfactual_axis": "...",
    "anchor_terms": ["momentum", "isolated system", "external force"],
    "representative_chunk_ids": ["physics_json_000123"]
}
```

Choose concepts that support correct, flawed, mechanistic, and counterfactual reasoning.

Good concept types:

```text
Physics: momentum, Newton's laws, fields, force vs acceleration, energy, waves
Chemistry: equilibrium, rates, catalysts, acids/bases, redox, gas laws
Biology: diffusion, osmosis, enzymes, natural selection, homeostasis, respiration
```

---

# Phase 5 — Generate Source B Contrast Pairs

Command:

```bash
python -m src.data.generate_contrast_pairs \
  --concepts data/extracted/textbook_concepts.json \
  --config configs/dataset_generation.yaml \
  --output_dir data/generated
```

Generate only:

```text
concept_correct_vs_misconception.jsonl     ~55 pairs
mechanistic_explanation_vs_surface.jsonl   ~55 pairs
counterfactual_reasoning.jsonl             ~55 pairs
```

Generation constraints:

```text
- positive and negative discuss the same concept
- length ratio <= 20%
- share at least 2 anchor terms
- similar register/formality
- negative is plausible, not silly
- no giveaway tokens: correct, incorrect, wrong, misconception, false, true,
  actually, in fact, no, yes
- do not copy or closely paraphrase textbook sentences
```

Source B examples:

```json
{
    "domain": "chemistry",
    "concept": "catalysts and activation energy",
    "positive": "A catalyst increases reaction rate by providing a pathway with lower activation energy, so a larger fraction of molecular collisions can form products at the same temperature.",
    "negative": "A catalyst increases reaction rate because it is a substance related to the reaction, so the reaction happens faster when the catalyst is present.",
    "shared_anchors": ["catalyst", "reaction rate", "reaction"],
    "reasoning_type": "mechanistic"
}
```

```json
{
    "domain": "biology",
    "concept": "osmosis",
    "positive": "If the solution outside a cell becomes more concentrated, water tends to leave the cell because the water potential is lower outside than inside.",
    "negative": "If the solution outside a cell becomes more concentrated, water tends to enter the cell because cells always take in water when surrounded by more solute.",
    "shared_anchors": ["solution outside", "cell", "water"],
    "reasoning_type": "counterfactual"
}
```

---

# Phase 6 — Validate and Split Source B

Validate:

```bash
python -m src.data.validate_dataset \
  --input_dir data/generated \
  --textbook_text data/extracted/textbook_text.json \
  --output outputs/reports/dataset_validation_warnings.md
```

Validation checks:

```text
- required fields exist
- positive/negative non-empty
- length ratio <= 20%
- shared anchor terms >= 2
- no giveaway tokens
- same concept/domain
- no near-duplicates
- no copied textbook passages in Source B
- plausible negative
```

Invalid pairs must be dropped or regenerated. Do not silently keep invalid pairs.

Split:

```bash
python -m src.data.split_dataset \
  --input_dir data/generated \
  --output_dir data/processed \
  --train 0.70 \
  --val 0.15 \
  --test 0.15
```

Split by `pair_id`, not individual rows.

Flattened row format:

```json
{
    "example_id": "physics_momentum_001_pos",
    "pair_id": "physics_momentum_001",
    "text": "...",
    "label": 1,
    "label_name": "positive",
    "dataset": "concept_correct_vs_misconception",
    "domain": "physics",
    "concept": "conservation_of_momentum",
    "reasoning_type": "conceptual",
    "split": "train"
}
```

Create `data/processed/paraphrase_test.jsonl` from held-out test examples only.

---

# Phase 7 — Collect Activations

Use both sources and merge before PCA.

Command for 1.7B:

```bash
python -m src.repe.collect_activations \
  --model Qwen/Qwen3-1.7B-Base \
  --source_a_suffixes data/repe_suffixes/science_suffix_bank.jsonl \
  --source_b_dataset data/processed/train.jsonl \
  --output outputs/activations/qwen3_0.6b/train.pt \
  --prompt_mode science_persona \
  --truncation_levels 10
```

Repeat for Qwen3 4B.

Activation collection rules:

```text
- use torch.no_grad()
- model.eval()
- output_hidden_states=True
- collect final-token hidden state for every layer
- compute diff = h_positive[-1] - h_negative[-1]
- save diffs, not raw activations, unless --save_raw is passed
- tag every diff with source = source_a_vgel or source_b_gpt
- support source ablations: Source A only, Source B only, Source A+B
```

---

# Phase 8 — Train LAT Vectors

Command:

```bash
python -m src.repe.train_lat_vectors \
  --activations outputs/activations/qwen3_0.6b/train.pt \
  --output outputs/vectors/qwen3_0.6b
```

For each model, dataset, source setting, and layer:

```text
1. load positive-minus-negative diff vectors
2. run PCA(n_components=1)
3. normalize the first component
4. flip sign if validation accuracy indicates it points negative
5. save vector, explained variance, pair count, skipped pairs, mean diff norm
```

Saved vector format:

```python
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
```

---

# Phase 9 — Evaluate Reading Vectors

Command:

```bash
python -m src.repe.evaluate_reading_vectors \
  --model Qwen/Qwen3-0.6B-Base \
  --vectors outputs/vectors/qwen3_0.6b \
  --dataset data/processed/test.jsonl \
  --output outputs/evaluations/qwen3_0.6b_test.json
```

Pairwise scoring:

```text
score_positive = dot(h_positive_layer, v_layer)
score_negative = dot(h_negative_layer, v_layer)
correct = score_positive > score_negative
```

Report:

```text
- pairwise accuracy per layer
- AUC per layer
- positive-negative margin per layer
- best layer
- best-layer accuracy
- bootstrap 95% CI
```

Also evaluate:

```text
- paraphrase_test.jsonl
- cross-dataset transfer
- Source A only vs Source B only vs combined vectors, if time permits
- random-vector baseline
- label-shuffle baseline
```

---

# Phase 10 — Control Generation

Control tests whether the LAT vector is only diagnostic or also behaviorally useful.

Intervention:

```python
hidden_states = hidden_states + coefficient * control_vector
```

Default control layers:

```python
def default_control_layers(num_layers: int) -> list[int]:
    return [
        int(num_layers * 0.45),
        int(num_layers * 0.55),
        int(num_layers * 0.65),
        int(num_layers * 0.75),
    ]
```

Command:

```bash
python -m src.repe.run_control_generation \
  --model Qwen/Qwen3-1.7B-Base \
  --vectors outputs/vectors/qwen3_1.7b/mechanistic_explanation_vs_surface_lat.pt \
  --prompts configs/control_prompts.yaml \
  --coefficients -2 -1 0 1 2 \
  --output outputs/generations/qwen3_1.7b_mechanistic_control.jsonl
```

Interpretation:

```text
negative coefficient = suppress science-reasoning direction
zero coefficient = baseline
positive coefficient = amplify science-reasoning direction
```

Generation settings:

```yaml
do_sample: false
temperature: null
max_new_tokens: 160
repetition_penalty: 1.1
```

Control prompts should be physics/chemistry/biology only. Do not include math prompts in the MVP.

---

# Phase 11 — Evaluate Generations

Command:

```bash
python -m src.analysis.evaluate_generations \
  --input outputs/generations/qwen3_1.7b_mechanistic_control.jsonl \
  --output outputs/evaluations/qwen3_1.7b_mechanistic_control_eval.json
```

Rubric:

```text
scientific_correctness: 1-5
mechanistic_depth: 1-5
misconception_presence: 1-5  # 1 = none, 5 = severe
clarity: 1-5
contains_major_error: true/false
brief_reason: string
```

Report whether positive control improves correctness/depth and whether negative control degrades them. Also note if control mostly changes verbosity, confidence, or style.

---

# Phase 12 — SAE Bridge

This is required and connects behavioral RepE to teammates' SAE work.

Command:

```bash
python -m src.analysis.sae_alignment \
  --lat_vectors outputs/vectors/qwen3_1.7b \
  --sae_repo CRISMechInterp/Qwen3_SAEs \
  --sae_subfolders qwen3_1p7b_middle_btop128_exp4 qwen3_1p7b_middle_btop256_exp4 \
  --sae_layer_hint hook_resid_post \
  --top_k 20 \
  --output_dir outputs/sae_alignment/qwen3_1.7b
```

For each SAE and dataset:

```text
1. load SAE decoder rows
2. orient decoder as [n_features, d_model]
3. L2-normalize rows
4. load 1.7B LAT vector at the SAE layer
5. compute cos_i = decoder_row_i · lat_vector
6. save full cosine spectrum
7. save top-k features by |cos_i|
8. plot sorted |cos_i| with random-baseline reference
9. compare btop128 vs btop256 top-aligned features
```

Required outputs:

```text
outputs/sae_alignment/qwen3_1.7b/btop128/{dataset}_cos.npy
outputs/sae_alignment/qwen3_1.7b/btop128/{dataset}_top_features.json
outputs/sae_alignment/qwen3_1.7b/btop128/{dataset}_spectrum.png
outputs/sae_alignment/qwen3_1.7b/btop256/{dataset}_cos.npy
outputs/sae_alignment/qwen3_1.7b/btop256/{dataset}_top_features.json
outputs/sae_alignment/qwen3_1.7b/btop256/{dataset}_spectrum.png
outputs/sae_alignment/qwen3_1.7b/btop128_vs_btop256_splits.json
```

Interpretation:

```text
RepE identifies dense behavioral directions associated with scientific reasoning.
SAE alignment asks whether those dense directions concentrate on a small set of
sparse candidate features.
```

Do not claim that an aligned SAE feature proves scientific understanding.

---

# Phase 13 — Scaling Plots and Bootstrap CIs

Command:

```bash
python -m src.analysis.plot_scaling_trends \
  --evaluations_dir outputs/evaluations \
  --output_dir outputs/plots \
  --n_boot 1000
```

For each model/dataset/layer:

```text
- resample pairs with replacement
- recompute accuracy, AUC, and margin
- save mean, 2.5 percentile, 97.5 percentile
```

Save:

```text
outputs/evaluations/{model}_{dataset}_bootstrap.json
```

Headline plot:

```text
x-axis = model size, preferably log scale
y-axis = best-layer reading accuracy
error bars = bootstrap 95% CI
chance line = 0.5
```

If a CI crosses 0.5, the report must say that readability is not significantly above chance for that setting.

---

# Phase 14 — Report

Command:

```bash
python -m src.analysis.build_report \
  --outputs_dir outputs \
  --output outputs/reports/science_repe_scaling_report.md
```

The report should answer:

```text
1. Which model has the highest best-layer reading accuracy?
2. Which layers are most informative?
3. Does best-layer accuracy improve with model size, with bootstrap CIs?
4. Do vectors generalize to paraphrases?
5. Does positive control improve explanation quality?
6. Does negative control degrade explanation quality?
7. Which SAE features align most with the 1.7B LAT direction?
8. Is the alignment spectrum sparse compared with random-vector baseline?
9. Are top btop128 features split across btop256 features?
10. What are the limitations?
```

Suggested report sections:

```text
I. Introduction
II. Background
III. Dataset Construction
IV. Method
V. Reading-Vector Results
VI. Control-Generation Results
VII. SAE Bridge
VIII. Ablations and Robustness
IX. Limitations
X. Conclusion
```

Useful figures/tables:

```text
Table 1: dataset statistics
Table 2: example Source A and Source B pairs
Figure 1: pipeline diagram
Figure 2: layerwise reading accuracy
Table 3: best-layer accuracy/AUC/margin with bootstrap CIs
Figure 3: scaling trend
Table 4: control generation scores
Figure 4: SAE alignment spectrum
Table 5: top SAE-aligned features
```

---

## Config Files

### `configs/models.yaml`

```yaml
models:
    - name: Qwen/Qwen3-0.6B-Base
      short_name: qwen3_0.6b
      dtype: bfloat16
      tier: 1

    - name: Qwen/Qwen3-1.7B-Base
      short_name: qwen3_1.7b
      dtype: bfloat16
      tier: 1

    - name: Qwen/Qwen3-4B-Base
      short_name: qwen3_4b
      dtype: bfloat16
      tier: 1

    - name: Qwen/Qwen3-8B-Base
      short_name: qwen3_8b
      dtype: bfloat16
      tier: 2

    - name: Qwen/Qwen3-14B-Base
      short_name: qwen3_14b
      dtype: bfloat16
      tier: 3
```

### `configs/dataset_generation.yaml`

```yaml
total_target_pairs: 165

datasets:
    concept_correct_vs_misconception:
        target_pairs: 55
    mechanistic_explanation_vs_surface:
        target_pairs: 55
    counterfactual_reasoning:
        target_pairs: 55

splits:
    train: 0.70
    val: 0.15
    test: 0.15

paraphrase_test:
    source_split: test
    n_per_dataset: 10
    paraphrase_model: gpt-4.1-mini

generation:
    model: gpt-4.1-mini
    temperature: 0.7
    max_retries: 3
    batch_size: 5
    length_ratio_tolerance: 0.20
    min_shared_anchors: 2
```

### `configs/repe.yaml`

```yaml
source_a:
    suffix_bank: data/repe_suffixes/science_suffix_bank.jsonl
    prompt_mode: science_persona
    truncation_levels: 10
    min_truncation_pct: 0.20
    max_truncation_pct: 0.95
    drop_last_n_tokens: 5

source_b:
    fallback_prompt_mode: neutral_text

batch_size: 1
final_token_only: true
save_raw_activations: false
pca_components: 1
normalize_vectors: true
flip_by_validation_accuracy: true

control:
    default_coefficients: [-2.0, -1.0, 0.0, 1.0, 2.0]
    layer_strategy: middle_late
    max_new_tokens: 160
    do_sample: false
    repetition_penalty: 1.1
```

---

## Acceptance Criteria

MVP is complete when these files exist:

```text
data/extracted/textbook_text.json
data/repe_suffixes/science_suffix_bank.jsonl
data/repe_suffixes/source_a_vgel_pairs_preview.jsonl
data/extracted/textbook_concepts.json
data/generated/concept_correct_vs_misconception.jsonl
data/generated/mechanistic_explanation_vs_surface.jsonl
data/generated/counterfactual_reasoning.jsonl
data/processed/train.jsonl
data/processed/val.jsonl
data/processed/test.jsonl
data/processed/paraphrase_test.jsonl

outputs/reports/source_a_dataset_report.md
outputs/reports/dataset_validation_warnings.md

outputs/activations/qwen3_0.6b/train.pt
outputs/activations/qwen3_1.7b/train.pt
outputs/vectors/qwen3_0.6b/*.pt
outputs/vectors/qwen3_1.7b/*.pt
outputs/evaluations/*.json
outputs/evaluations/*_bootstrap.json
outputs/plots/*.png
outputs/generations/*.jsonl

outputs/sae_alignment/qwen3_1.7b/btop128/*.npy
outputs/sae_alignment/qwen3_1.7b/btop128/*.json
outputs/sae_alignment/qwen3_1.7b/btop128/*.png
outputs/sae_alignment/qwen3_1.7b/btop256/*.npy
outputs/sae_alignment/qwen3_1.7b/btop256/*.json
outputs/sae_alignment/qwen3_1.7b/btop256/*.png

outputs/reports/science_repe_scaling_report.md
```

4B outputs are a strong target but not required if time or GPU memory runs out.

---

## Required Limitations Section

The final report must explicitly include:

```text
1. Linear decodability is not understanding. A linear direction that separates
   correct from incorrect explanations does not imply the model knows the concept.

2. PCA on difference vectors can capture surface artifacts such as length,
   formality, hedging, confidence, or science-like register. Source A controls
   many confounds; Source B validation and paraphrase tests mitigate but do not
   eliminate them.

3. Dataset size is small (~165 GPT-generated pairs plus textbook suffix pairs).
   Accuracy/AUC/margin values require bootstrap 95% CIs.

4. GPT-generated misconceptions reflect the generator's biases, not necessarily
   real student misconceptions.

5. LLM-judge generation evaluation is noisy and can reward verbosity or
   confidence. Manual audit of a small sample should be reported if possible.

6. Control vectors may alter tone, confidence, or verbosity rather than only
   reasoning quality.

7. Results depend on prompt template, layer choice, and final-token aggregation.

8. Cross-model dense-vector cosine is not meaningful because Qwen3 hidden sizes
   differ across scale. Use per-model reading metrics and SAE-feature analysis.

9. Qwen3 may have STEM-heavy pretraining/post-training. Scaling trends reflect
   training data and objectives, not pure architecture.

10. Base models are preferred. If instruct models are substituted, flag this in
    metadata and results.

11. SAE bridge results depend on the specific 1.7B BatchTopK SAE recipe and do
    not imply robustness across all possible SAE bases.
```

---

## Do-Not-Do List

```text
- Do not fine-tune Qwen3.
- Do not build skipped datasets during the MVP.
- Do not use textbook sentences as Source B positives/negatives.
- Do not precompute all Source A truncation pairs into JSONL unless needed.
- Do not compare dense LAT vectors across model sizes when hidden dimensions differ.
- Do not claim that linear decodability proves understanding.
- Do not start large model downloads before Source A and Source B dataset reports exist.
```
