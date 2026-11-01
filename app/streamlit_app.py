import requests
import streamlit as st
import os

from components.multilingual_keyboard import multilingual_keyboard


# ---------- API Configuration ----------

# try:
#     API_BASE_URL = st.secrets.get(
#         "API_BASE_URL",
#         os.getenv("API_BASE_URL", "http://127.0.0.1:8000"),
#     ).rstrip("/")
# except (FileNotFoundError, AttributeError):
#     API_BASE_URL = os.getenv(
#         "API_BASE_URL",
#         "http://127.0.0.1:8000",
#     ).rstrip("/")

API_BASE_URL = "http://127.0.0.1:8000"
# ---------- Page Configuration ----------

st.set_page_config(
    page_title="Lingua AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

LANGUAGES = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "Malayalam": "ml",
}

CODE_TO_LANGUAGE = {
    code: name for name, code in LANGUAGES.items()
}


# ---------- Dark Theme ----------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #10131a;
        color: #e6eaf2;
    }

    [data-testid="stHeader"] {
        background: #10131a;
    }

    [data-testid="stSidebar"] {
        background: #171b25;
        border-right: 1px solid #2b3140;
    }

    .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #f4f6fb;
    }

    p, label, .stCaption {
        color: #b7c0d0;
    }

    .app-subtitle {
        color: #aab5c8;
        margin-top: -10px;
        margin-bottom: 28px;
    }

    div[data-testid="stChatMessage"] {
        background: #191e29;
        border: 1px solid #2b3140;
        border-radius: 14px;
        padding: 14px;
    }

    div[data-testid="stTextArea"] textarea {
        background: #191e29;
        color: #f4f6fb;
        border: 1px solid #343c4d;
        border-radius: 10px;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #191e29;
        border-color: #343c4d;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 9px;
        min-height: 40px;
        font-weight: 600;
    }

    hr {
        border-color: #2b3140;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Session State ----------

defaults = {
    "page": "AI Chat",
    "messages": [],
    "last_answer": "",
    "last_language": "",
    "last_submission_id": None,
    "translation_input": "",
    "translation_result": "",
    "translation_source": "English",
    "translation_target": "Tamil",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# Reset invalid workspace selection

if st.session_state.page not in ["AI Chat", "Translation Studio"]:
    st.session_state.page = "AI Chat"

if "input_reset_id" not in st.session_state:
    st.session_state.input_reset_id = 0
    
# ---------- Helper Functions ----------

def clear_chat():
    st.session_state.messages = []
    st.session_state.last_answer = ""
    st.session_state.last_language = ""

    # Keep last_submission_id to prevent an old component
    # submission from being processed again.


def clear_translation():
    st.session_state.translation_input = ""
    st.session_state.translation_result = ""


def load_ai_response_for_translation():

    st.session_state.translation_input = (
        st.session_state.last_answer
    )

    detected = st.session_state.last_language

    # Support both language names and language codes

    if detected in LANGUAGES:
        st.session_state.translation_source = detected

    elif detected in CODE_TO_LANGUAGE:
        st.session_state.translation_source = (
            CODE_TO_LANGUAGE[detected]
        )

    st.session_state.page = "Translation Studio"


def show_api_error(exc, default_message):

    message = default_message
    response = getattr(exc, "response", None)

    if response is not None:
        try:
            message = response.json().get("detail", message)
        except (ValueError, requests.RequestException):
            pass

    st.error(str(message))


# ---------- Sidebar Navigation ----------

with st.sidebar:

    st.markdown("## 🌐 Lingua AI")
    st.caption("Multilingual AI Chatbot and Translation Studio")

    st.divider()

    st.radio(
        "WORKSPACE",
        ["AI Chat", "Translation Studio"],
        key="page",
        label_visibility="visible",
    )

    st.divider()

    st.caption("SUPPORTED LANGUAGES")
    st.write("English · தமிழ் · हिन्दी · తెలుగు · മലയാളം")

    st.divider()

    st.caption("Powered by Gemini, FastAPI and Transformers")

    if st.session_state.page == "AI Chat":

        st.button(
            "Clear conversation",
            use_container_width=True,
            on_click=clear_chat,
        )

    elif st.session_state.page == "Translation Studio":

        st.button(
            "Clear translation",
            use_container_width=True,
            on_click=clear_translation,
        )


# ---------- Main Page ----------

st.title("Lingua AI")


# ==================================================
# AI CHAT WORKSPACE
# ==================================================

if st.session_state.page == "AI Chat":

    st.markdown(
        """
        <p class="app-subtitle">
        Chat in your language. Your messages are detected automatically.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # ---------- Display Chat History ----------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            # Display detected language below USER prompt
            if message["role"] == "user" and message.get("language"):

                st.caption(
                    f"🌐 Detected Language: {message['language']}"
                )
    # ---------- Multilingual Keyboard Component ----------


    keyboard_result = multilingual_keyboard(
        language="Tamil",
        key="keyboard_test",
        default=None
    )

    # ---------- Process Submitted Message ----------

    if isinstance(keyboard_result, dict):

        if keyboard_result.get("submitted") is True:

            user_text = keyboard_result.get("text", "").strip()

            submission_id = keyboard_result.get("submission_id")

            # Process only new, valid submissions
            if (
                user_text
                and submission_id is not None
                and submission_id != st.session_state.last_submission_id
            ):

                # Mark this submission as processed
                st.session_state.last_submission_id = submission_id

                try:

                    with st.spinner("Detecting language..."):

                        response = requests.post(
                            f"{API_BASE_URL}/chat",
                            json={"text": user_text},
                            timeout=120,
                        )

                        response.raise_for_status()

                        data = response.json()

                    # Extract API response
                    language = data["detected_language"]
                    answer = data["response"]

                    # Save USER message with detected language
                    st.session_state.messages.append({
                        "role": "user",
                        "content": user_text,
                        "language": language,
                    })

                    # Save AI response
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                    })

                    # Save latest response for Translation Studio
                    st.session_state.last_answer = answer
                    st.session_state.last_language = language

                    st.session_state.input_reset_id += 1

                    # Refresh chat history
                    st.rerun()

                except requests.exceptions.RequestException as exc:

                    show_api_error(
                        exc,
                        "Unable to contact the AI service. "
                        "Check that FastAPI is running.",
                    )

                except (KeyError, ValueError) as exc:

                    st.error(
                        f"Invalid AI service response: {exc}"
                    )

    # ---------- Transfer AI Response to Translation Studio ----------

    if st.session_state.last_answer:

        st.divider()

        st.caption(
            "Want to translate the latest AI response?"
        )

        st.button(
            "🌐 Open in Translation Studio →",
            use_container_width=True,
            on_click=load_ai_response_for_translation,
        )


# ==================================================
# TRANSLATION STUDIO WORKSPACE
# ==================================================

elif st.session_state.page == "Translation Studio":

    st.markdown(
        """
        <p class="app-subtitle">
        Translate your own text or bring in the latest AI response.
        Your translation stays separate from the chat.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Translation settings")

    source_col, target_col = st.columns(2)

    with source_col:

        st.selectbox(
            "Source language",
            options=list(LANGUAGES.keys()),
            key="translation_source",
        )

    with target_col:

        st.selectbox(
            "Target language",
            options=list(LANGUAGES.keys()),
            key="translation_target",
        )

    st.subheader("Input text")

    st.text_area(
        "Text to translate",
        placeholder="Type or paste your text here...",
        key="translation_input",
        height=200,
        label_visibility="collapsed",
    )

    translate_col, clear_col = st.columns([3, 1])

    with translate_col:

        translate_clicked = st.button(
            "Translate",
            type="primary",
            use_container_width=True,
        )

    with clear_col:

        st.button(
            "Clear",
            use_container_width=True,
            on_click=clear_translation,
        )

    # ---------- Translation API Call ----------

    if translate_clicked:

        text_to_translate = (
            st.session_state.translation_input.strip()
        )

        source = st.session_state.translation_source
        target = st.session_state.translation_target

        if not text_to_translate:

            st.warning(
                "Enter some text before translating."
            )

        elif source == target:

            st.session_state.translation_result = text_to_translate

            st.info(
                "Both languages are the same; "
                "the original text is shown."
            )

        else:

            try:

                with st.spinner(
                    f"Translating {source} to {target}..."
                ):

                    response = requests.post(
                        f"{API_BASE_URL}/translate",
                        json={
                            "text": text_to_translate,
                            "source_language": LANGUAGES[source],
                            "target_language": LANGUAGES[target],
                        },
                        timeout=300,
                    )

                    response.raise_for_status()

                    data = response.json()

                st.session_state.translation_result = (
                    data["translated_text"]
                )

            except requests.RequestException as exc:

                show_api_error(
                    exc,
                    "Translation failed. Check that FastAPI is running.",
                )

            except (KeyError, ValueError):

                st.error(
                    "The translation service returned an invalid response."
                )

    # ---------- Display Translation Result ----------

    if st.session_state.translation_result:

        st.divider()

        st.subheader("Translated text")

        st.caption(
            f"{st.session_state.translation_source} → "
            f"{st.session_state.translation_target}"
        )

        st.text_area(
            "Translation result",
            value=st.session_state.translation_result,
            height=200,
            disabled=True,
        )

        st.download_button(
            "Download translation",
            data=st.session_state.translation_result,
            file_name="translated_text.txt",
            mime="text/plain",
        )


# ---------- Footer ----------

st.divider()

st.caption(
    "Lingua AI · Multilingual chat and translation"
)