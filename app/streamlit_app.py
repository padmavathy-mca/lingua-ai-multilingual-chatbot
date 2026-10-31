
import requests
import streamlit as st
import os

import json
from pathlib import Path
import streamlit.components.v1 as components

from services.keyboard_service import KEYBOARD_LAYOUTS

try:
    API_BASE_URL = st.secrets.get(
        "API_BASE_URL",
        os.getenv("API_BASE_URL", "http://127.0.0.1:8000"),
    ).rstrip("/")
except (FileNotFoundError, AttributeError):
    API_BASE_URL = os.getenv(
        "API_BASE_URL",
        "http://127.0.0.1:8000",
    ).rstrip("/")
st.write("Connected API URL:", API_BASE_URL)
#API_BASE_URL = "http://127.0.0.1:8000"

LANGUAGES = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "Malayalam": "ml",
}
CODE_TO_LANGUAGE = {code: name for name, code in LANGUAGES.items()}

st.set_page_config(
    page_title="Lingua AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Dark theme ----------
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
    .status {
        color: #9ca9bd;
        font-size: 13px;
        padding-bottom: 12px;
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
    .stButton > button, .stDownloadButton > button {
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

# ---------- Session state ----------
defaults = {
    "page": "AI Chat",
    "messages": [],
    "last_answer": "",
    "last_language": "",
    "translation_input": "",
    "translation_result": "",
    "translation_source": "English",
    "translation_target": "Tamil",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def clear_chat():
    st.session_state.messages = []
    st.session_state.last_answer = ""
    st.session_state.last_language = ""


def clear_translation():
    st.session_state.translation_input = ""
    st.session_state.translation_result = ""


def load_ai_response_for_translation():
    st.session_state.translation_input = st.session_state.last_answer
    detected = st.session_state.last_language
    if detected in LANGUAGES:
        st.session_state.translation_source = detected
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


# ---------- Sidebar navigation ----------
with st.sidebar:
    st.markdown("## 🌐 Lingua AI")
    st.caption("Multilingual AI Chatbot and Translation Studio")
    st.divider()

    st.radio(
        "WORKSPACE",
        ["AI Chat", "Translation Studio", "Smart Typing"],
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
    else:
        st.markdown(
            '<p class="app-subtitle">'
            'Translate your own text or bring in the latest AI response. '
            'Your translation stays separate from the chat.'
            '</p>',
            unsafe_allow_html=True,
        )

# ---------- Main page ----------
st.title("Lingua AI")

if st.session_state.page == "AI Chat":

    st.markdown(
        '<p class="app-subtitle">'
        'Chat in your language. Your messages are detected automatically.'
        '</p>',
        unsafe_allow_html=True,
    )

    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("language"):
                st.caption(f"Detected Language: {message['language']}")

    # Chat input
    user_text = st.chat_input("Write a message...")

    if user_text:

        # Display user message
        st.session_state.messages.append(
            {"role": "user", "content": user_text}
        )

        with st.chat_message("user"):
            st.markdown(user_text)

        try:
            with st.spinner("Detecting language..."):

                # Call FastAPI
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json={"text": user_text},
                    timeout=120,
                )

                response.raise_for_status()
                data = response.json()

            # Extract response data
            language = data["detected_language"]
            answer = data["response"]

            # Display detected language BELOW user input
            st.caption(f"🌐 Detected Language: {language}")

            # Display AI response
            with st.chat_message("assistant"):
                st.markdown(answer)

            # Save conversation
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "language": language,
                }
            )

            st.session_state.last_answer = answer
            st.session_state.last_language = language

        except requests.exceptions.RequestException as exc:
            st.error(f"Unable to contact the AI service: {exc}")

        except (KeyError, ValueError) as exc:
            st.error(f"Invalid AI service response: {exc}")

    # Transfer action is outside the chat response itself
    if st.session_state.last_answer:
        st.divider()
        st.caption("Want to translate the latest AI response?")
        st.button(
            "Open in Translation Studio →",
            on_click=load_ai_response_for_translation,
        )

else:
    st.markdown(
        '<p class="app-subtitle">'
        'Translate your own text or bring in the latest AI response. '
        'Your translation stays separate from the chat.'
        '</p>',
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

    if translate_clicked:
        text_to_translate = st.session_state.translation_input.strip()
        source = st.session_state.translation_source
        target = st.session_state.translation_target

        if not text_to_translate:
            st.warning("Enter some text before translating.")
        elif source == target:
            st.session_state.translation_result = text_to_translate
            st.info("Both languages are the same; the original text is shown.")
        else:
            try:
                with st.spinner(f"Translating {source} to {target}..."):
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

                st.session_state.translation_result = data["translated_text"]

            except requests.RequestException as exc:
                show_api_error(
                    exc,
                    "Translation failed. Check that FastAPI is running.",
                )
            except (KeyError, ValueError):
                st.error("The translation service returned an invalid response.")

    # Translation output exists only in this workspace
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

    
    # ---------- Smart Typing workspace ----------

    else:

        st.markdown(
            '<p class="app-subtitle">'
            'Type in Indian languages using English phonetics '
            'or a virtual regional keyboard.'
            '</p>',
            unsafe_allow_html=True,
        )

        st.subheader("🌍 Smart Typing Studio")

        language = st.selectbox(
            "Select your language",
            ["Tamil", "Hindi", "Telugu", "Malayalam"],
            key="smart_typing_language"
        )

        script_codes = {
            "Tamil": "tamil",
            "Hindi": "devanagari",
            "Telugu": "telugu",
            "Malayalam": "malayalam"
        }

        script = script_codes[language]

        js_path = (
            Path(__file__).resolve().parent
            / "static"
            / "js"
            / "indic-transliterate.js"
        )

        if not js_path.exists():

            st.error(
                "JavaScript transliteration library not found. "
                "Check static/js/indic-transliterate.js"
            )

        else:

            js_source = js_path.read_text(encoding="utf-8")

            keyboard_json = json.dumps(
                KEYBOARD_LAYOUTS,
                ensure_ascii=False
            )

        html = r"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">

        <style>
        body {
            background: #171b25;
            color: white;
            font-family: Arial;
        }

        textarea {
            width: 100%;
            min-height: 90px;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #343c4d;
            background: #191e29;
            color: white;
            font-size: 18px;
            box-sizing: border-box;
        }

        .output {
            padding: 15px;
            background: #242b39;
            border-radius: 8px;
            font-size: 26px;
            min-height: 45px;
            overflow-wrap: anywhere;
        }

        .keyboard {
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
            margin: 12px 0;
        }

        button {
            padding: 10px 14px;
            border: none;
            border-radius: 7px;
            cursor: pointer;
            font-size: 18px;
        }

        .key {
            background: #343c4d;
            color: white;
        }

        .action {
            background: #2563eb;
            color: white;
            font-size: 14px;
        }

        .row {
            margin-bottom: 8px;
        }
        </style>
        </head>

        <body>

        <h3>1. Phonetic Typing</h3>

        <textarea id="roman"
        placeholder="Type English letters, e.g. vaNakkam"></textarea>

        <h3>Live Transliteration</h3>

        <div class="output" id="preview"></div>

        <div id="suggestions" class="keyboard"></div>

        <button class="action" id="add">
        Add to final text
        </button>

        <hr>

        <h3>2. Virtual Keyboard</h3>

        <div id="keyboard"></div>

        <div class="keyboard">
            <button class="key" id="space">Space</button>
            <button class="key" id="backspace">⌫</button>
            <button class="key" id="clear">Clear</button>
        </div>

        <h3>3. Final Text</h3>

        <textarea id="finalText"
        placeholder="Your regional-language text"></textarea>

        <br><br>

        <button class="action" id="copy">
        Copy Text
        </button>

        <p id="status"></p>

        <script>
        __JS_SOURCE__
        </script>

        <script>

        const layouts = __KEYBOARD_DATA__;

        const script = "__SCRIPT__";

        const roman = document.getElementById("roman");
        const preview = document.getElementById("preview");
        const finalText = document.getElementById("finalText");

        function transliterate() {

            const text = roman.value;

            preview.textContent =
                IndicTransliterate.transliterate(text, script);

            const suggestions =
                document.getElementById("suggestions");

            suggestions.innerHTML = "";

            const match = text.match(/[A-Za-z]+$/);

            if (!match || match[0].length < 2) return;

            const variants =
                IndicTransliterate.suggest(match[0], script);

            variants.forEach(item => {

                const button = document.createElement("button");

                button.className = "key";
                button.textContent = item;

                button.onclick = () => {

                    roman.value =
                        text.slice(0, text.length - match[0].length)
                        + item;

                    transliterate();
                };

                suggestions.appendChild(button);
            });
        }

        roman.addEventListener("input", transliterate);

        document.getElementById("add").onclick = () => {

            if (!preview.textContent) return;

            finalText.value +=
                (finalText.value ? " " : "")
                + preview.textContent;
        };

        function renderKeyboard() {

            const container =
                document.getElementById("keyboard");

            container.innerHTML = "";

            layouts["__LANGUAGE__"].forEach(row => {

                const rowDiv = document.createElement("div");

                rowDiv.className = "keyboard row";

                row.forEach(character => {

                    const button =
                        document.createElement("button");

                    button.className = "key";
                    button.textContent = character;

                    button.onclick = () => {

                        const start = finalText.selectionStart;
                        const end = finalText.selectionEnd;

                        finalText.setRangeText(
                            character,
                            start,
                            end,
                            "end"
                        );

                        finalText.focus();
                    };

                    rowDiv.appendChild(button);
                });

                container.appendChild(rowDiv);
            });
        }

        document.getElementById("space").onclick = () => {
            finalText.setRangeText(
                " ",
                finalText.selectionStart,
                finalText.selectionEnd,
                "end"
            );
            finalText.focus();
        };

        document.getElementById("backspace").onclick = () => {

            const start = finalText.selectionStart;
            const end = finalText.selectionEnd;

            if (start === end && start > 0) {
                finalText.setRangeText(
                    "",
                    start - 1,
                    end,
                    "end"
                );
            } else {
                finalText.setRangeText("", start, end, "end");
            }

            finalText.focus();
        };

        document.getElementById("clear").onclick = () => {
            finalText.value = "";
        };

        document.getElementById("copy").onclick = async () => {

            try {
                await navigator.clipboard.writeText(finalText.value);

                document.getElementById("status").textContent =
                    "Text copied successfully!";
            }
            catch (error) {
                finalText.select();

                document.getElementById("status").textContent =
                    "Press Ctrl+C to copy selected text.";
            }
        };

        renderKeyboard();

        </script>
        </body>
        </html>
        """

        html = (
            html.replace("__JS_SOURCE__", js_source)
            .replace("__KEYBOARD_DATA__", keyboard_json)
            .replace("__SCRIPT__", script)
            .replace("__LANGUAGE__", language)
        )

        components.html(
            html,
            height=1050,
            scrolling=True
        )
st.divider()
st.caption("Lingua AI · Multilingual chat and translation")

