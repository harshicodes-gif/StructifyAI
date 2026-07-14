import json
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image

from backend.database.sqlite import (
    is_persistent_history_available,
    save_document,
)
from backend.services.extraction_service import process_document
from backend.utils.constants import UPLOAD_DIR
from frontend.components.uploader import upload_document


IGNORED_FIELDS = {
    "error",
    "raw_output",
    "raw_text",
}


def _format_key(key: str) -> str:
    """Convert snake_case into readable labels."""
    return key.replace("_", " ").title()


def _display_value(value):
    """Render any JSON value nicely."""

    if value is None:
        st.write("—")
        return

    if isinstance(value, str):
        st.write(value)
        return

    if isinstance(value, (int, float, bool)):
        st.write(value)
        return

    if isinstance(value, dict):

        for k, v in value.items():

            st.markdown(f"**{_format_key(k)}**")

            if isinstance(v, (dict, list)):
                _display_value(v)
            else:
                st.write(v)

        return

    if isinstance(value, list):

        if not value:
            st.write("[]")
            return

        for index, item in enumerate(value, start=1):

            if isinstance(item, dict):

                title = (
                    item.get("title")
                    or item.get("name")
                    or item.get("heading")
                    or item.get("section")
                    or f"Item {index}"
                )

                with st.expander(str(title), expanded=False):

                    for k, v in item.items():

                        if k in {"title", "name", "heading"}:
                            continue

                        st.markdown(f"**{_format_key(k)}**")

                        if isinstance(v, (dict, list)):
                            _display_value(v)
                        else:
                            st.write(v)

            else:
                st.write(f"• {item}")

        return

    st.write(str(value))


def _show_extracted_information(result: dict):
    """Display dynamic structured JSON."""

    structured_json = result.get("structured_json", {})

    if not isinstance(structured_json, dict):
        st.error("Invalid JSON returned.")
        return

    if not structured_json:
        st.warning("No structured information extracted.")
        return

    document_type = structured_json.get("document_type", "Unknown Document")

    st.markdown(f"# {document_type}")

    with st.container(border=True):

        for key, value in structured_json.items():

            if key == "document_type":
                continue

            if key in IGNORED_FIELDS:
                continue

            left, right = st.columns([1, 2])

            with left:
                st.markdown(f"**{_format_key(key)}**")

            with right:
                _display_value(value)


def _save_uploaded_file(uploaded) -> Path:
    """Save uploaded document."""

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

    filename = Path(uploaded.name).name

    filepath = UPLOAD_DIR / f"{timestamp}_{filename}"

    with open(filepath, "wb") as file:
        file.write(uploaded.getbuffer())

    return filepath


def show_upload():
    """Upload page."""

    st.title("Upload Document")

    uploaded = upload_document()

    if uploaded is None:
        st.info("Upload an image or PDF.")
        return

    left, right = st.columns(2)

    with left:

        st.subheader("Document Preview")

        if uploaded.type.startswith("image"):

            image = Image.open(uploaded)
            st.image(image, use_container_width=True)

        else:

            st.success("PDF uploaded successfully.")

    with right:

        st.subheader("Extracted Information")
        st.caption("Process the document to extract structured information.")

        if st.button(
            "Process Document",
            type="primary",
            use_container_width=True,
        ):

            filepath = _save_uploaded_file(uploaded)

            with st.spinner("Analyzing document..."):

                try:

                    result = process_document(str(filepath))

                    structured_json = result.get("structured_json", {})

                    if not isinstance(structured_json, dict):
                        structured_json = {}

                    document_id = save_document(
                        filename=uploaded.name,
                        file_path=filepath,
                        structured_json=structured_json,
                    )

                    st.session_state.selected_history_document_id = document_id

                    st.success("Document processed successfully!")

                    if not is_persistent_history_available():
                        st.info(
                            "History is available only during this session."
                        )

                    _show_extracted_information(result)

                    st.download_button(
                        label="Download JSON",
                        data=json.dumps(
                            structured_json,
                            indent=4,
                            ensure_ascii=False,
                        ),
                        file_name="structured_output.json",
                        mime="application/json",
                        use_container_width=True,
                    )

                except Exception as exc:

                    st.error(f"Processing failed.\n\n{exc}")