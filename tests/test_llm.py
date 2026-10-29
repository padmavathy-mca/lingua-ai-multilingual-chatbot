
from app.services.language_detector import detect_language
from app.services.llm_service import generate_response


def test_tamil_language_detection():
    result = detect_language("வணக்கம்! எப்படி இருக்கிறீர்கள்?")

    assert result["language_code"] == "ta"
    assert result["language_name"] == "Tamil"
    assert result["supported"] is True


def test_gemini_tamil_response():
    message = "வணக்கம்! செயற்கை நுண்ணறிவு என்றால் என்ன?"
    detection = detect_language(message)

    answer = generate_response(
        message,
        detection["language_name"],
    )

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0

    print("\nGemini response:", answer)
