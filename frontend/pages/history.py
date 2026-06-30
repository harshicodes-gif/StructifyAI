import base64
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st
from PIL import Image

from backend.database.sqlite import get_document, list_documents

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


def show_history():
    st.title("History")

    documents = list_documents()

    if not documents:
        st.info("Processed documents will appear here.")
        return

    filtered_documents = _show_filters(documents)

    list_column, detail_column = st.columns([1, 2], gap="large")

    with list_column:
        _show_document_list(filtered_documents)

    with detail_column:
        _show_selected_document(filtered_documents)


def _show_filters(documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    with st.container(border=True):
        st.subheader("Search")

        asset_query, operator_query, document_type_filter = st.columns(3)

        with asset_query:
            asset = st.text_input("Asset", placeholder="Search asset")

        with operator_query:
            operator = st.text_input("Operator", placeholder="Search operator")

        with document_type_filter:
            document_types = sorted(
                {
                    _clean_value(document.get("document_type"))
                    for document in documents
                    if _clean_value(document.get("document_type")) != MISSING_VALUE
                }
            )
            document_type = st.selectbox(
                "Document Type",
                ["All", *document_types],
            )

    return [
        document
        for document in documents
        if _matches_filters(document, asset, operator, document_type)
    ]


def _show_document_list(documents: list[dict[str, Any]]) -> None:
    st.subheader("Documents")

    if not documents:
        st.warning("No documents match the current search.")
        return

    selected_id = st.session_state.get("selected_history_document_id")

    for document in documents:
        is_selected = document["id"] == selected_id
        button_type = "primary" if is_selected else "secondary"

        with st.container(border=True):
            name_column, type_column = st.columns([2, 1])

            with name_column:
                if st.button(
                    document["filename"],
                    key=f"history_document_{document['id']}",
                    use_container_width=True,
                    type=button_type,
                ):
                    st.session_state.selected_history_document_id = document["id"]
                    st.rerun()

            with type_column:
                st.caption(_clean_value(document.get("document_type")))

            st.caption(_format_datetime(document.get("created_at", "")))


def _show_selected_document(documents: list[dict[str, Any]]) -> None:
    selected_id = st.session_state.get("selected_history_document_id")
    visible_ids = {document["id"] for document in documents}

    if selected_id not in visible_ids and documents:
        selected_id = documents[0]["id"]
        st.session_state.selected_history_document_id = selected_id

    if selected_id is None or selected_id not in visible_ids:
        st.info("Select a processed document to view details.")
        return

    document = get_document(int(selected_id))

    if document is None:
        st.warning("The selected document could not be found.")
        return

    st.subheader(document["filename"])

    detail_header = st.columns(2)
    detail_header[0].metric(
        "Document Type",
        _clean_value(document.get("document_type")),
    )
    detail_header[1].metric(
        "Upload Date/Time",
        _format_datetime(document.get("created_at", "")),
    )

    preview_tab, extracted_tab = st.tabs(["Document Preview", "Extracted Information"])

    with preview_tab:
        _show_preview(document)

    with extracted_tab:
        _show_extracted_information(document.get("structured_json", {}))


def _show_preview(document: dict[str, Any]) -> None:
    file_path = Path(document.get("file_path") or "")

    if not file_path.exists():
        st.warning("Document file is no longer available for preview.")
        return

    suffix = file_path.suffix.lower()

    if suffix in {".png", ".jpg", ".jpeg"}:
        image = Image.open(file_path)
        st.image(image, use_container_width=True)
        return

    if suffix == ".pdf":
        encoded_pdf = base64.b64encode(file_path.read_bytes()).decode("utf-8")
        st.markdown(
            f"""
            <iframe
                src="data:application/pdf;base64,{encoded_pdf}"
                width="100%"
                height="650"
                type="application/pdf">
            </iframe>
            """,
            unsafe_allow_html=True,
        )
        return

    st.info("Preview is not available for this file type.")


def _show_extracted_information(structured_json: dict[str, Any]) -> None:
    if not isinstance(structured_json, dict):
        structured_json = {}

    fields = {
        label: _clean_value(structured_json.get(field))
        for field, label in DISPLAY_FIELDS.items()
    }

    summary_columns = st.columns(3)

    for index, (label, value) in enumerate(list(fields.items())[:3]):
        with summary_columns[index]:
            st.metric(label=label, value=value)

    with st.container(border=True):
        for label, value in list(fields.items())[3:]:
            label_column, value_column = st.columns([1, 2])
            label_column.markdown(f"**{label}**")
            value_column.write(value)

    with st.expander("Structured JSON"):
        st.json(structured_json)


def _matches_filters(
    document: dict[str, Any],
    asset_query: str,
    operator_query: str,
    document_type_filter: str,
) -> bool:
    structured_json = document.get("structured_json", {})

    if not isinstance(structured_json, dict):
        structured_json = {}

    asset = _clean_value(structured_json.get("asset")).lower()
    operator = _clean_value(structured_json.get("operator")).lower()
    document_type = _clean_value(document.get("document_type"))

    if asset_query.strip().lower() not in asset:
        return False

    if operator_query.strip().lower() not in operator:
        return False

    if document_type_filter != "All" and document_type != document_type_filter:
        return False

    return True


def _clean_value(value: Any) -> str:
    if value is None:
        return MISSING_VALUE

    if isinstance(value, str):
        value = value.strip()
        return value if value else MISSING_VALUE

    return str(value)


def _format_datetime(value: str) -> str:
    if not value:
        return MISSING_VALUE

    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return value

    return parsed.strftime("%Y-%m-%d %H:%M:%S")
