
from app.services.transliterator import (
    transliterate_text,
    get_suggestions
)

from app.services.keyboard_service import get_keyboard_layout



def test_tamil_transliteration():
    result = transliterate_text("vanakkam", "Tamil")
    assert result
    print("Tamil:", result)


def test_hindi_transliteration():
    result = transliterate_text("namaste", "Hindi")
    assert result
    print("Hindi:", result)


def test_telugu_transliteration():
    result = transliterate_text("namaskaram", "Telugu")
    assert result
    print("Telugu:", result)


def test_malayalam_transliteration():
    result = transliterate_text("namaskaram", "Malayalam")
    assert result
    print("Malayalam:", result)


def test_keyboard_layout():
    for language in ["Tamil", "Hindi", "Telugu", "Malayalam"]:
        layout = get_keyboard_layout(language)
        assert layout
        print(language, layout)


def test_tamil_suggestions():
    suggestions = get_suggestions("amma", "Tamil")
    assert isinstance(suggestions, list)
