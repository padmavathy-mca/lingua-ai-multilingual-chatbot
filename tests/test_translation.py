
from app.services.translation_service import translate_text


def test_same_language_translation():
    text = "வணக்கம்"

    result = translate_text(
        text,
        source_language="ta",
        target_language="ta",
    )

    assert result == text


def test_tamil_to_english():
    result = translate_text(
        "வணக்கம், எப்படி இருக்கிறீர்கள்?",
        source_language="ta",
        target_language="en",
    )

    print("\nTamil to English:", result)

    assert isinstance(result, str)
    assert len(result) > 0


def test_english_to_hindi():
    result = translate_text(
        "Good morning. How are you?",
        source_language="en",
        target_language="hi",
    )

    print("\nEnglish to Hindi:", result)

    assert isinstance(result, str)
    assert len(result) > 0
