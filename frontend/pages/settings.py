import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/tags"
MODEL_NAME = "llama3.2:1b"


def show_settings():
    st.title("Settings")

    engine_columns = st.columns(3)

    with engine_columns[0]:
        st.metric("OCR Engine", "EasyOCR")

    with engine_columns[1]:
        st.metric("LLM Engine", "Ollama")

    with engine_columns[2]:
        st.metric("Model", MODEL_NAME)

    st.subheader("Model Status")

    if _is_ollama_reachable():
        st.success("Ollama connected")
    else:
        st.error("Ollama not running")

    st.subheader("Setup Commands")

    st.code(f"ollama pull {MODEL_NAME}", language="bash")
    st.code("ollama serve", language="bash")


def _is_ollama_reachable() -> bool:
    try:
        response = requests.get(OLLAMA_URL, timeout=2)
    except requests.RequestException:
        return False

    return response.ok
