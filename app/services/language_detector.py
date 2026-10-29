
from langdetect import detect, detect_langs, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Make detection more reproducible
DetectorFactory.seed = 0

SUPPORTED_LANGUAGES = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "te": "Telugu",
    "ml": "Malayalam",
}


def detect_language(text: str) -> dict:
    """Detect the language of the user's input."""

    text = text.strip()

    if not text:
        return {
            "language_code": None,
            "language_name": "Unknown",
            "confidence": 0.0,
            "supported": False,
            "error": "Please enter some text.",
        }

    try:
        predictions = detect_langs(text)
        prediction = predictions[0]
        language_code = prediction.lang

        return {
            "language_code": language_code,
            "language_name": SUPPORTED_LANGUAGES.get(
                language_code, "Other / Unsupported"
            ),
            "confidence": round(float(prediction.prob), 4),
            "supported": language_code in SUPPORTED_LANGUAGES,
            "error": None,
        }

    except LangDetectException:
        return {
            "language_code": None,
            "language_name": "Unknown",
            "confidence": 0.0,
            "supported": False,
            "error": "Unable to detect the language. Try a longer message.",
        }
