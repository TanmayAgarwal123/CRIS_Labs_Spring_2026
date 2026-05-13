"""Run control generation across coefficients and prompts.

Loads control prompts from configs/control_prompts.yaml, the LAT vector for
one model+dataset, and generates one continuation per (prompt, coefficient).
Default deterministic decode (do_sample=false), max_new_tokens=160,
repetition_penalty=1.1.

Writes one JSONL row per generation:
  {prompt_id, domain, concept, coefficient, prompt, generation, model, vector,
   layers, decode_config}

CLI:
  python -m src.repe.run_control_generation \\
      --model Qwen/Qwen3-1.7B \\
      --vectors outputs/vectors/qwen3_1.7b/mechanistic_explanation_vs_surface_lat.pt \\
      --prompts configs/control_prompts.yaml \\
      --coefficients -2 -1 0 1 2 \\
      --output outputs/generations/qwen3_1.7b_mechanistic_control.jsonl
"""
