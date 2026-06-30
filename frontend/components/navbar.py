import streamlit as st


def show_navigation():

    with st.sidebar:
        st.title("🤖 Structify AI")

        page = st.radio(
            "Navigation",
            [
                "Home",
                "Upload",
                "History",
                "Analytics",
                "Settings",
            ],
        )

    return page
