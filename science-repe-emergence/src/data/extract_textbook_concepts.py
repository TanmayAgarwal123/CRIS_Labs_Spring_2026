"""Identify ~25 teachable concepts (and common misconceptions) per domain.

Calls OpenAI (gpt-4.1-mini by default) over the chunks in
data/extracted/textbook_text.json. Each concept record contains:
  - domain
  - concept_name
  - one_line_definition
  - common_misconception
  - representative_chunk_ids

Writes data/extracted/textbook_concepts.json.

CLI:
  python -m src.data.extract_textbook_concepts \\
      --input data/extracted/textbook_text.json \\
      --output data/extracted/textbook_concepts.json \\
      --model gpt-4.1-mini \\
      --concepts_per_domain 25
"""
