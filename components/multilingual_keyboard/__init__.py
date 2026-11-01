import streamlit.components.v1 as components
from pathlib import Path

COMPONENT_DIR = Path(__file__).resolve().parent

_component_func = components.declare_component(
    "multilingual_keyboard",
    path=str(COMPONENT_DIR)
)

def multilingual_keyboard(language="Tamil", key=None, default=None):
    return _component_func(
        language=language,
        key=key,
        default=default
    )