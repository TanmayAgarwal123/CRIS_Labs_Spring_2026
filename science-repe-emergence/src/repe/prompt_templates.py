"""Source A prompt templates and per-dataset persona labels.

The template (and persona) is the most important design decision for LAT
quality. Source A uses the science_persona / mechanistic_persona templates
(suffix is identical pos/neg, only persona phrase varies). Source B falls
back to neutral_text since its content carries the signal.

  TEMPLATES = {
    "science_persona":     "Consider the following scientific text, "
                           "interpreted by someone with {persona}.\\n\\n{suffix}",
    "mechanistic_persona": "The following scientific text is being "
                           "interpreted by someone with {persona}.\\n\\n{suffix}",
    "neutral_text":        "Consider the following scientific statement:\\n\\n"
                           "{text}\\n\\nAnalysis:",
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

Personas must be parallel and differ only in the intended reasoning property.
"""
