import json
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image

from backend.database.sqlite import is_persistent_history_available, save_document
from backend.services.extraction_service import process_document
from backend.utils.constants import UPLOAD_DIR
from frontend.components.uploader import upload_document

DISPLAY_FIELDS = {
    "document_type": "Document Type",
    "asset": "Asset",
    "operator": "Operator",
    "issue": "Issue",
    "priority": "Priority",
    "recommendation": "Recommendation",
    "date": "Date",
}

MISSING_VALUE = "Not found"


def _clean_value(value):
    """Return a user-facing field value."""

    if value is None:
        return MISSING_VALUE

    if isinstance(value, str):
        value = value.strip()
        return value if value else MISSING_VALUE

    return value


def _extract_display_fields(result: dict) -> dict:
    """Map backend extraction output into upload page summary fields."""

    structured_json = result.get("structured_json", {})

    if not isinstance(structured_json, dict):
        structured_json = {}

    return {
        label: _clean_value(structured_json.get(field))
        for field, label in DISPLAY_FIELDS.items()
    }


def _show_extracted_information(result: dict) -> None:
    """Display extracted information without exposing OCR text or raw JSON."""

    fields = _extract_display_fields(result)

    summary_columns = st.columns(3)
    for index, (label, value) in enumerate(list(fields.items())[:3]):
        with summary_columns[index]:
            st.metric(label=label, value=value)

    with st.container(border=True):
        for label, value in list(fields.items())[3:]:
            field_label, field_value = st.columns([1, 2])
            field_label.markdown(f"**{label}**")
            field_value.write(value)


def _save_uploaded_file(uploaded) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    safe_name = Path(uploaded.name).name
    filepath = UPLOAD_DIR / f"{timestamp}_{safe_name}"

    with open(filepath, "wb") as file:
        file.write(uploaded.getbuffer())

    return filepath


def show_upload():
    """Display the upload page."""

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
        st.caption("Process the document to view structured fields.")

        if st.button("Process Document", use_container_width=True, type="primary"):
            filepath = _save_uploaded_file(uploaded)

            with st.spinner("Processing document..."):
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
                        st.info("History is available only during the current session.")

                    _show_extracted_information(result)

                    st.download_button(
                        label="Download JSON",
                        data=json.dumps(result, indent=4),
                        file_name="structured_output.json",
                        mime="application/json",
                        use_container_width=True,
                    )

                except Exception as e:
                    st.error(f"Processing failed.\n\n{e}")
