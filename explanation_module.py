from functools import lru_cache

from config import get_settings
from gemini_client import generate_text


@lru_cache(maxsize=1)
def _load_local_model():

    from transformers import (
        AutoModelForSeq2SeqLM,
        AutoTokenizer,
    )

    model_name = get_settings().local_explainer_model

    tokenizer = AutoTokenizer.from_pretrained(
        model_name
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name
    )

    model.eval()

    return tokenizer, model


def _local_explain(topic: str) -> str:

    import torch

    tokenizer, model = _load_local_model()

    prompt = (
        "Explain the following educational topic "
        "for a beginner using simple English. "
        "Use short paragraphs and a small example if useful. "
        "Topic: "
        + topic
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )

    with torch.no_grad():

        output_ids = model.generate(
            **inputs,
            max_new_tokens=220,
            num_beams=4,
            early_stopping=True,
        )

    return tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True
    ).strip()


def explain_concept(topic: str) -> str:

    settings = get_settings()

    # Try local model if enabled.
    if settings.local_explainer_enabled:

        try:
            result = _local_explain(topic)

            if result:
                return result

        except Exception:
            # If local model fails,
            # automatically use Gemini.
            pass

    return generate_text(
        f"Explain this educational concept: {topic}",
        system_instruction=(
            "You are EduGenie, a patient educational tutor. "
            "Explain concepts in simple English for beginners. "
            "Use clear headings, short paragraphs, "
            "bullet points when useful, and simple examples. "
            "Avoid unnecessarily complicated terminology."
        ),
    )