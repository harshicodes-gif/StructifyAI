import json
import os

import streamlit as st
from PIL import Image

from backend.services.extraction_service import process_document
from frontend.components.uploader import upload_document


def show_upload():
    """Display the upload page."""

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

        if st.button("🚀 Process Document", use_container_width=True):
            os.makedirs("uploads", exist_ok=True)

            filepath = os.path.join("uploads", uploaded.name)

            with open(filepath, "wb") as file:
                file.write(uploaded.getbuffer())

            with st.spinner("Running OCR and Local AI..."):
                try:
                    result = process_document(filepath)

                    st.success("Document processed successfully!")

                    st.json(result)

                    st.download_button(
                        label="📥 Download JSON",
                        data=json.dumps(result, indent=4),
                        file_name="structured_output.json",
                        mime="application/json",
                        use_container_width=True,
                    )

                except Exception as e:
                    st.error(f"Processing failed.\n\n{e}")
