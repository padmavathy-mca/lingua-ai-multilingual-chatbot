
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env from the project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

SUPPORTED_LANGUAGE_NAMES = {
    "English",
    "Tamil",
    "Hindi",
    "Telugu",
    "Malayalam",
}


def generate_response(user_text: str, language_name: str) -> str:
    """Generate an LLM response in the detected language."""

    user_text = user_text.strip()

    if not user_text:
        raise ValueError("Please enter a message.")

    if language_name not in SUPPORTED_LANGUAGE_NAMES:
        raise ValueError("Please use one of the five supported languages.")

    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    if not api_key or api_key == "your_actual_api_key_here":
        raise RuntimeError(
            "Gemini API key is missing. Configure it in the .env file."
        )

    client = genai.Client(api_key=api_key)

    system_instruction = f"""
You are a helpful multilingual AI assistant.

The user's detected language is {language_name}.

Rules:
1. Answer entirely in {language_name}, using its native script.
2. Keep every answer concise, useful, and natural.
3. Never exceed 100 whitespace-separated words.
4. Prefer a direct answer and one short example when useful.
5. Avoid unnecessary introductions, repetition, and long explanations.
6. Follow the user's request if they explicitly ask for another language.
"""

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.4,
                max_output_tokens=180,
            ),
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()

    except Exception as exc:
        raise RuntimeError(
            f"Gemini response generation failed: {exc}"
        ) from exc
