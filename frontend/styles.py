import streamlit as st


def apply_theme() -> None:
    """Apply custom Streamlit styling."""

    st.markdown(
        """
        <style>

        .main {
            padding: 2rem;
        }

        h1 {
            color: #0E76A8;
        }

        .stButton>button {
            border-radius:10px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
