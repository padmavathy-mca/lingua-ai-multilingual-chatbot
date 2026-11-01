
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.services.language_detector import detect_language
from app.services.llm_service import generate_response
from app.services.translation_service import translate_text

import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    force=True
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Multilingual AI Chatbot API",
    description=(
        "Language detection, multilingual Gemini chat, "
        "and transformer-based translation."
    ),
    version="1.0.0",
)


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class TranslationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    source_language: str
    target_language: str


@app.get("/")
def root():
    return {
        "message": "Multilingual AI Chatbot API is running",
        "supported_languages": [
            "English",
            "Tamil",
            "Hindi",
            "Telugu",
            "Malayalam",
        ],
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/detect-language")
def detect_language_endpoint(request: TextRequest):
    result = detect_language(request.text)

    if result["error"]:
        raise HTTPException(
            status_code=422,
            detail=result["error"],
        )

    return result


@app.post("/chat")
def chat_endpoint(request: TextRequest):
    logger.warning("CHAT ENDPOINT REACHED - TEST 12345")
    detection = detect_language(request.text)

    if detection["error"]:
        raise HTTPException(
            status_code=422,
            detail=detection["error"],
        )

    if not detection["supported"]:
        raise HTTPException(
            status_code=422,
            detail=(
                "Please enter text in English, Tamil, Hindi, "
                "Telugu, or Malayalam."
            ),
        )

    try:
        answer = generate_response(
            request.text,
            detection["language_name"],
        )

        return {
            "detected_language": detection["language_name"],
            "language_code": detection["language_code"],
            "confidence": detection["confidence"],
            "response": answer,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI response generation failed: {exc}",
        ) from exc


@app.post("/translate")
def translate_endpoint(request: TranslationRequest):
    try:
        translated_text = translate_text(
            request.text,
            request.source_language,
            request.target_language
        )

        return {
            "original_text": request.text,
            "translated_text": translated_text,
            "source_language": request.source_language,
            "target_language": request.target_language
        }

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    except Exception as exc:
        print("TRANSLATION ERROR:", repr(exc), flush=True)
        raise HTTPException(
            status_code=503,
            detail="Translation service is temporarily unavailable. Please try again later."
        )