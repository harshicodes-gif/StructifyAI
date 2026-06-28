import streamlit as st

from PIL import Image

from frontend.components.uploader import upload_document

from frontend.components.json_viewer import show_json


def show_upload():

    st.title("📄 Upload Document")

    uploaded = upload_document()

    if uploaded is None:

        st.info("Upload an image or PDF.")

        return

    left, right = st.columns(2)

    with left:

        st.subheader("Preview")

        if uploaded.type.startswith("image"):

            image = Image.open(uploaded)

            st.image(image, use_container_width=True)

        else:

            st.success("PDF uploaded successfully.")

    with right:

        st.subheader("Structured JSON")

        show_json()