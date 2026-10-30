
from functools import lru_cache

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "facebook/nllb-200-distilled-600M"

# NLLB language codes are different from langdetect codes.
LANGUAGE_CODES = {
    "en": "eng_Latn",
    "ta": "tam_Taml",
    "hi": "hin_Deva",
    "te": "tel_Telu",
    "ml": "mal_Mlym",
}


@lru_cache(maxsize=1)
def load_translation_model():
    """Load the tokenizer and model once, then reuse them."""

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )
    model.to(device)
    model.eval()

    return tokenizer, model, device


def translate_text(
    text: str,
    source_language: str,
    target_language: str,
) -> str:
    """Translate text between the five supported languages."""

    text = text.strip()

    if not text:
        raise ValueError("Please enter text to translate.")

    if source_language not in LANGUAGE_CODES:
        raise ValueError("Unsupported source language.")

    if target_language not in LANGUAGE_CODES:
        raise ValueError("Unsupported target language.")
