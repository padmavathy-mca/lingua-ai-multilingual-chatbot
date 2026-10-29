# 🌐 Lingua AI — Multilingual AI Chatbot

A multilingual AI assistant that combines Generative AI, automatic language detection, and neural machine translation to support communication across five languages.

## 🚀 Features

- 💬 **AI Chat:** Generate responses using Google Gemini.
- 🌍 **Language Detection:** Automatically identify the user's input language.
- 🗣️ **Five Languages:** English, Tamil, Hindi, Telugu, and Malayalam.
- 🔄 **Text Translation:** Translate user-provided text between supported languages.
- 🤖 **AI Response Translation:** Send AI-generated responses to a dedicated translation workspace.
- 🎨 **Dark-Themed UI:** Clean interface built with Streamlit.
- ⚡ **REST API:** Backend endpoints built with FastAPI.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Frontend UI |
| FastAPI | REST API backend |
| Google Gemini | AI response generation |
| Hugging Face Transformers | Neural machine translation |
| NLLB-200 | Multilingual translation model |
| langdetect | Automatic language detection |
| PyTorch | Transformer model inference |

## 🏗️ Architecture

```text
User
  ↓
Streamlit UI
  ├── AI Chat
  │     ↓
  │   FastAPI /chat
  │     ↓
  │   Language Detection
  │     ↓
  │   Google Gemini
  │     ↓
  │   AI Response
  │
  └── Translation Studio
        ↓
      FastAPI /translate
        ↓
      Hugging Face NLLB-200
        ↓
      Translated Text
```

## 🌐 Supported Languages

| Language | Code |
|---|---|
| English | `en` |
| Tamil | `ta` |
| Hindi | `hi` |
| Telugu | `te` |
| Malayalam | `ml` |

## 📁 Project Structure

```text
multilingual-chatbot/
├── app/
│   ├── __init__.py
│   ├── streamlit_app.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│   └── services/
│       ├── __init__.py
│       ├── language_detector.py
│       ├── llm_service.py
│       └── translation_service.py
├── tests/
├── requirements.txt
├── .env
└── .gitignore
```

## ⚙️ Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/lingua-ai-multilingual-chatbot.git
cd lingua-ai-multilingual-chatbot
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Never commit your real API key to GitHub.

### 5. Start the FastAPI backend

```bash
python -m uvicorn app.api.main:app --reload --port 8000
```

API documentation: `http://127.0.0.1:8000/docs`

### 6. Start the Streamlit frontend

Open another terminal, activate the virtual environment, and run:

```bash
python -m streamlit run app/streamlit_app.py
```

Open the local URL displayed in the terminal.

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/detect-language` | Detect input language |
| POST | `/chat` | Generate an AI response |
| POST | `/translate` | Translate text |

## 🔐 Environment Variables

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | Authentication for Gemini |
| `GEMINI_MODEL` | Gemini model selection |
| `API_BASE_URL` | FastAPI URL used by the Streamlit frontend |

## 💡 Key Learning Outcomes

- Integrating an LLM into a Python application.
- Building REST APIs with FastAPI.
- Detecting languages using NLP techniques.
- Applying pretrained multilingual transformer models.
- Separating frontend, backend, and AI service logic.
- Managing API credentials using environment variables.

## 🔮 Future Enhancements

- Voice input and multilingual speech output.
- Conversation history and persistent storage.
- Streaming AI responses.
- Translation quality evaluation.
- Optimized model inference and cloud deployment.

## 👩‍💻 Author

**Padmavathy**

GitHub: [padmavathy-mca](https://github.com/padmavathy-mca)

---

⭐ If you find this project useful, consider starring the repository.

**Technologies:** Python · Generative AI · NLP · Google Gemini · FastAPI · Streamlit · Hugging Face Transformers
