from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests, TranslationNotFound

LANGUAGE_CODES = {
    "en": "en",
    "ta": "ta",
    "hi": "hi",
    "te": "te",
    "ml": "ml",
}


def translate_text(text, source_language, target_language):
    text = text.strip()

    if not text:
        raise ValueError("Please enter text to translate.")

    if source_language not in LANGUAGE_CODES:
        raise ValueError("Unsupported source language.")

    if target_language not in LANGUAGE_CODES:
        raise ValueError("Unsupported target language.")

    if source_language == target_language:
        return text

    try:
        translator = GoogleTranslator(
            source=LANGUAGE_CODES[source_language],
            target=LANGUAGE_CODES[target_language],
        )

        return translator.translate(text)

    except TooManyRequests as exc:
        raise RuntimeError(
            "Translation service is temporarily rate-limited. Please try again later."
        ) from exc

    except TranslationNotFound as exc:
        raise RuntimeError(
            "Translation could not be found."
        ) from exc