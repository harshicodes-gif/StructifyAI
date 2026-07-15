import streamlit as st

from backend.llm.llama_engine import (
    get_llm_mode,
    OLLAMA_MODEL,
    GROQ_MODEL,
)


def show_settings():
    st.title("Settings")

    llm_mode = get_llm_mode()

    st.subheader("Current Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("OCR Engine", "EasyOCR")

    with col2:
        st.metric("AI Backend", llm_mode)

    st.divider()

    if llm_mode == "Ollama":

        st.success("Running locally using Ollama.")

        st.metric("Model", OLLAMA_MODEL)

        st.code(
            f"ollama pull {OLLAMA_MODEL}",
            language="bash",
        )

        st.code(
            "ollama serve",
            language="bash",
        )

    elif llm_mode == "Groq":

        st.success("Running on Groq Cloud API.")

        st.metric("Model", GROQ_MODEL)

        st.info(
            "Using the GROQ_API_KEY configured in Streamlit Secrets."
        )

    else:

        st.warning("AI model unavailable.")

        st.write(
            "The application is running in OCR-only mode."
        )
