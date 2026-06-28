import streamlit as st

from frontend.styles import apply_theme
from backend.database.sqlite import initialize_database

st.set_page_config(
    page_title="Structify AI",
    page_icon="🤖",
    layout="wide"
)

apply_theme()

initialize_database()

st.title("🤖 Structify AI")

st.subheader("Offline AI Document Intelligence")

st.info(
    "Upload a document to transform unstructured information into structured JSON."
)

st.success("Application initialized successfully.")