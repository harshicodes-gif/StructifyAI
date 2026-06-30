from collections import Counter
from typing import Any

import streamlit as st

from backend.database.sqlite import list_documents

try:
    import plotly.express as px
except ImportError:
    px = None

MISSING_VALUE = "Unknown"


def show_analytics():
    st.title("Analytics")

    documents = list_documents()

    if not documents:
        st.info("No processed documents yet.")
        return

    rows = [_document_to_row(document) for document in documents]

    st.metric("Total Documents Processed", len(documents))

    type_counts = _count_values(rows, "document_type")
    priority_counts = _count_values(rows, "priority")
    asset_counts = _count_values(rows, "asset")

    chart_row = st.columns(2, gap="large")

    with chart_row[0]:
        _show_bar_chart(
            title="Count by Document Type",
            counts=type_counts,
            x_label="Document Type",
            y_label="Documents",
        )

    with chart_row[1]:
        _show_bar_chart(
            title="Count by Priority",
            counts=priority_counts,
            x_label="Priority",
            y_label="Documents",
        )

    _show_bar_chart(
        title="Top Assets Processed",
        counts=dict(asset_counts.most_common(10)),
        x_label="Asset",
        y_label="Documents",
    )


def _document_to_row(document: dict[str, Any]) -> dict[str, str]:
    structured_json = document.get("structured_json", {})

    if not isinstance(structured_json, dict):
        structured_json = {}

    return {
        "document_type": _clean_value(
            structured_json.get("document_type") or document.get("document_type")
        ),
        "priority": _clean_value(structured_json.get("priority")),
        "asset": _clean_value(structured_json.get("asset")),
    }


def _count_values(rows: list[dict[str, str]], key: str) -> Counter[str]:
    return Counter(row[key] for row in rows)


def _show_bar_chart(
    title: str,
    counts: Counter[str] | dict[str, int],
    x_label: str,
    y_label: str,
) -> None:
    st.subheader(title)

    if not counts:
        st.info("No data available.")
        return

    labels = list(counts.keys())
    values = list(counts.values())

    if px is None:
        st.dataframe(
            {
                x_label: labels,
                y_label: values,
            },
            use_container_width=True,
            hide_index=True,
        )
        return

    figure = px.bar(
        x=labels,
        y=values,
        labels={"x": x_label, "y": y_label},
        text=values,
    )

    figure.update_traces(
        marker_color="#2563eb",
        textposition="outside",
        cliponaxis=False,
    )
    figure.update_layout(
        height=360,
        margin={"l": 10, "r": 10, "t": 20, "b": 10},
        showlegend=False,
        xaxis_title=x_label,
        yaxis_title=y_label,
    )

    st.plotly_chart(figure, use_container_width=True)


def _clean_value(value: Any) -> str:
    if value is None:
        return MISSING_VALUE

    if isinstance(value, str):
        value = value.strip()
        return value if value else MISSING_VALUE

    return str(value)
