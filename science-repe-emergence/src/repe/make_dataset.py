"""vgel-style dataset builder: persona pairs with truncation augmentation.

For each suffix and each (positive_persona, negative_persona) pair:
  1. tokenize suffix with the model's tokenizer
  2. drop the last 5 tokens
  3. produce 10 prefix truncations spaced from ~20% to ~95% of remaining length
  4. for each truncation emit one DatasetEntry where positive and negative
     prompts share the SAME truncated suffix and differ only in persona

Core invariant:  positive suffix == negative suffix (verify exact equality).

Reference: https://vgel.me/posts/representation-engineering/

Suggested dataclass:
  @dataclass
  class DatasetEntry:
      pair_id: str
      dataset: str
      source: str           # "vgel_textbook_suffix" or "gpt_generated_contrast"
      positive: str
      negative: str
      metadata: dict
"""
