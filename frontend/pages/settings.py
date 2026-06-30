import streamlit as st

from backend.llm.llama_engine import MODEL_NAME, get_llm_mode


def show_settings():
    st.title("Settings")

    llm_mode = get_llm_mode()
    processing_mode = (
        "Ollama (Local)" if llm_mode == "Ollama" else "OCR Only (Hugging Face)"
    )

    engine_columns = st.columns(2)

    with engine_columns[0]:
        st.metric("OCR Engine", "EasyOCR")

    with engine_columns[1]:
        st.metric("LLM Mode", llm_mode)

    st.subheader("Processing")
    st.write("OCR Engine: EasyOCR")
    st.write(f"Processing Mode: {processing_mode}")

    if llm_mode == "Ollama":
        st.subheader("Model")
        st.metric("Model", MODEL_NAME)

        st.subheader("Setup Commands")
        st.code(f"ollama pull {MODEL_NAME}", language="bash")
        st.code("ollama serve", language="bash")
