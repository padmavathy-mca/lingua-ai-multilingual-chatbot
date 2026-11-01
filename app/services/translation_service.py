
from functools import lru_cache

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "facebook/nllb-200-distilled-600M"

LANGUAGE_CODES = {
    "en": "eng_Latn",
    "ta": "tam_Taml",
    "hi": "hin_Deva",
    "te": "tel_Telu",
    "ml": "mal_Mlym",
}


@lru_cache(maxsize=1)
def load_translation_model():
    """Load the model once and reuse it."""

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

    text = text.strip()

    if not text:
        raise ValueError("Please enter text to translate.")

    if source_language not in LANGUAGE_CODES:
        raise ValueError("Unsupported source language.")

    if target_language not in LANGUAGE_CODES:
        raise ValueError("Unsupported target language.")

    if source_language == target_language:
        return text

    tokenizer, model, device = load_translation_model()

    tokenizer.src_lang = LANGUAGE_CODES[source_language]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    ).to(device)

    target_token_id = tokenizer.convert_tokens_to_ids(
        LANGUAGE_CODES[target_language]
    )

    with torch.inference_mode():
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=target_token_id,
            max_new_tokens=256,
        )

    translated_text = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True,
    )[0]

    return translated_text
