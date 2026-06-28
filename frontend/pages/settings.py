import streamlit as st


def show_settings():

    st.title("⚙ Settings")

    st.selectbox(

        "OCR Engine",

        [

            "EasyOCR",

        ],

    )

    st.selectbox(

        "LLM",

        [

            "Qwen2.5",

        ],

    )

    st.checkbox(

        "Enable Cache",

        value=True,

    )