import streamlit as st


def show_home():

    st.title("🤖 Structify AI")

    st.subheader("Offline CPU-First Document Intelligence")

    st.info(

        """
        Transform unstructured documents into structured JSON.

        ✔ Offline First

        ✔ CPU Only

        ✔ Privacy Focused

        ✔ OCR Powered

        ✔ Local LLM
        """

    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Documents", "0")

    c2.metric("CPU", "--")

    c3.metric("RAM", "--")

    c4.metric("Cache", "0")