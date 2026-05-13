"""Source A / Source B prompt templates and per-dataset persona labels.

Source A uses science_persona / mechanistic_persona (suffix is identical
pos/neg, only the persona phrase varies). Source B wraps GPT-generated
contrast pairs in neutral_text since the content itself is the signal.
"""

TEMPLATES = {
    "science_persona":
        "Consider the following scientific text, interpreted by someone "
        "with {persona}.\n\n{suffix}",
    "mechanistic_persona":
        "The following scientific text is being interpreted by someone "
        "with {persona}.\n\n{suffix}",
    "neutral_text":
        "Consider the following scientific statement:\n\n{text}\n\nAnalysis:",
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


def wrap_neutral(text: str) -> str:
    """Wrap a single GPT-generated statement in the neutral Source B template."""
    return TEMPLATES["neutral_text"].format(text=text)
