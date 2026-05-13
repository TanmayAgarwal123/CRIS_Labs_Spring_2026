"""Load a Qwen3 base model + tokenizer with bf16 and device_map='auto'.

  load_model_and_tokenizer(model_name, dtype='bfloat16', device_map='auto')

Sets model.eval(); supports output_hidden_states=True at forward time.
"""
