import streamlit as st


def upload_document():

    uploaded = st.file_uploader(

        "Upload Document",

        type=["png", "jpg", "jpeg", "pdf"],

    )

    return uploaded