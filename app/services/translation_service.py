from deep_translator import GoogleTranslator

LANGUAGE_CODES = {
    "en": "en",
    "ta": "ta",
    "hi": "hi",
    "te": "te",
    "ml": "ml",
}


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

    translator = GoogleTranslator(
        source=LANGUAGE_CODES[source_language],
        target=LANGUAGE_CODES[target_language],
    )

    return translator.translate(text)