import re
from typing import Any

MISSING_VALUE = "Not found"

FIELDS = (
    "document_type",
    "asset",
    "operator",
    "issue",
    "priority",
    "recommendation",
    "date",
)

LABEL_PATTERNS = {
    "document_type": ("document type", "type", "report type"),
    "asset": ("asset", "asset id", "equipment", "machine"),
    "operator": (
        "operator",
        "inspector",
        "technician",
        "engineer",
        "assigned to",
    ),
    "issue": ("issue", "problem description", "problem", "fault", "defect", "failure"),
    "priority": ("priority", "severity"),
    "recommendation": (
        "recommendation",
        "recommended action",
        "corrective action",
        "action",
        "resolution",
    ),
    "date": ("date", "timestamp", "reported on"),
}

OCR_LABEL_PATTERNS = {
    "asset": r"a[s5]{1,2}e[t7]|asset\s*id|equipment|machine",
    "operator": r"[o0]perat[o0]r|inspect[o0]r|technician|engineer|assigned\s+to",
    "issue": r"[i1l]ssue|problem\s+description|problem|fault|defect|failure",
    "priority": r"pri[o0]r[i1l]t[yv]|severity",
    "recommendation": (
        r"recommendati[o0]n|recommended\s+acti[o0]n|c[o0]rrective\s+acti[o0]n|"
        r"acti[o0]n|resolution"
    ),
    "date": r"date|timestamp|reported\s+on",
}

STOP_LABEL_PATTERNS = {
    **OCR_LABEL_PATTERNS,
    "inspection_findings": r"inspecti[o0]n\s+findings",
    "status": r"status",
    "safety_precautions": r"safety\s+precauti[o0]ns",
}

INLINE_VALUE_FIELDS = ("asset", "operator", "priority", "date")

DOCUMENT_TYPE_KEYWORDS = (
    ("maintenance", "Maintenance Report"),
    ("inspection", "Inspection Report"),
    ("service", "Service Report"),
    ("invoice", "Invoice"),
    ("purchase order", "Purchase Order"),
    ("sop", "SOP"),
)

DATE_PATTERN = re.compile(
    r"\b(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|"
    r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
    r"\s+\d{1,2},?\s+\d{4})\b",
    re.IGNORECASE,
)


def parse_ocr_text(text: str) -> dict[str, Any]:
    """Create structured JSON directly from OCR text using regex/string rules."""
    lines = _clean_lines(text)
    structured = {field: MISSING_VALUE for field in FIELDS}
    sections = _extract_sections(lines)

    for field, value in sections.items():
        if field in structured and value:
            structured[field] = (
                _normalize_priority(value) if field == "priority" else value
            )

    full_text = "\n".join(lines)

    for field in INLINE_VALUE_FIELDS:
        if structured[field] == MISSING_VALUE:
            structured[field] = _find_labeled_value(full_text, field)

    if structured["issue"] == MISSING_VALUE:
        structured["issue"] = _find_multiline_field(
            full_text,
            "issue",
            ("priority", "inspection_findings"),
        )

    if structured["recommendation"] == MISSING_VALUE:
        structured["recommendation"] = _find_multiline_field(
            full_text,
            "recommendation",
            ("status", "safety_precautions"),
        )

    if structured["document_type"] == MISSING_VALUE:
        structured["document_type"] = _infer_document_type(full_text)

    if structured["date"] == MISSING_VALUE:
        structured["date"] = _find_date(full_text)

    if structured["priority"] == MISSING_VALUE:
        structured["priority"] = _infer_priority(full_text)

    if structured["issue"] == MISSING_VALUE:
        structured["issue"] = _find_line_by_keywords(
            lines,
            ("issue", "problem", "fault", "failure", "defect", "leak", "damage"),
        )

    if structured["recommendation"] == MISSING_VALUE:
        structured["recommendation"] = _find_line_by_keywords(
            lines,
            ("recommend", "replace", "repair", "inspect", "service", "action"),
        )

    structured["processing_mode"] = "OCR Only"
    return structured


def _parse_label_value(line: str) -> tuple[str | None, str | None]:
    match = re.match(
        r"^\s*([A-Za-z][A-Za-z0-9\s_/().-]{1,40})\s*[:=-]\s*(.*?)\s*$",
        line,
    )
    if not match:
        return None, None

    field = _field_for_label(match.group(1))
    value = match.group(2).strip()

    return field, value or None


def _infer_document_type(text: str) -> str:
    lower_text = text.lower()
    for keyword, document_type in DOCUMENT_TYPE_KEYWORDS:
        if keyword in lower_text:
            return document_type

    return MISSING_VALUE


def _find_date(text: str) -> str:
    match = DATE_PATTERN.search(text)
    return match.group(0) if match else MISSING_VALUE


def _infer_priority(text: str) -> str:
    lower_text = text.lower()
    for priority in ("critical", "high", "medium", "low"):
        if re.search(rf"\b{priority}\b", lower_text):
            return priority.title()

    return MISSING_VALUE


def _find_line_by_keywords(lines: list[str], keywords: tuple[str, ...]) -> str:
    for line in lines:
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in keywords):
            return line

    return MISSING_VALUE


def _find_labeled_value(text: str, field: str) -> str:
    label_pattern = OCR_LABEL_PATTERNS[field]
    stop_pattern = _label_stop_pattern()
    separator = r"(?:\s*[:;=\-]\s*|\s+)"
    pattern = re.compile(
        rf"(?:^|\n|\b)(?:{label_pattern}){separator}"
        rf"(.+?)(?=\s+(?:{stop_pattern})\s*(?::|;|=|-|\s)|\n|$)",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return MISSING_VALUE

    value = _clean_extracted_value(match.group(1))
    if not value:
        return MISSING_VALUE

    if field == "priority":
        return _normalize_priority(value)

    if field == "date":
        date = _find_date(value)
        return date if date != MISSING_VALUE else value

    return value


def _find_multiline_field(text: str, field: str, stop_fields: tuple[str, ...]) -> str:
    label_pattern = OCR_LABEL_PATTERNS[field]
    stop_pattern = "|".join(STOP_LABEL_PATTERNS[stop] for stop in stop_fields)
    separator = r"(?:\s*[:;=\-]\s*|\s+)"
    pattern = re.compile(
        rf"(?:^|\n|\b)(?:{label_pattern}){separator}"
        rf"(.+?)(?=\s*(?:{stop_pattern})\s*(?::|;|=|-|\s)|$)",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return _find_labeled_value(text, field)

    value = _clean_extracted_value(match.group(1))
    return value or MISSING_VALUE


def _label_stop_pattern() -> str:
    return "|".join(STOP_LABEL_PATTERNS.values())


def _normalize_priority(value: str) -> str:
    match = re.search(r"\b(critical|high|medium|low)\b", value, re.IGNORECASE)
    return match.group(1).title() if match else value


def _clean_lines(text: str) -> list[str]:
    return [
        re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()
    ]


def _extract_sections(lines: list[str]) -> dict[str, str]:
    sections: dict[str, str] = {}
    active_field: str | None = None
    active_values: list[str] = []

    def flush_active() -> None:
        nonlocal active_field, active_values
        if active_field and active_values and active_field not in sections:
            value = _join_section_value(active_values)
            if value:
                sections[active_field] = value
        active_field = None
        active_values = []

    for line in lines:
        field, value = _parse_label_value(line)
        if field:
            flush_active()
            if value:
                sections.setdefault(field, _clean_extracted_value(value))
            else:
                active_field = field
            continue

        if active_field:
            if _looks_like_unparsed_label(line):
                flush_active()
            else:
                active_values.append(line)

    flush_active()
    return sections


def _join_section_value(values: list[str]) -> str:
    return _clean_extracted_value(" ".join(values))


def _clean_extracted_value(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value.rstrip(" .") + "." if value.endswith(" .") else value


def _looks_like_unparsed_label(line: str) -> bool:
    return bool(re.match(r"^[A-Za-z][A-Za-z0-9\s_/().-]{1,40}\s*[:=-]\s*$", line))


def _field_for_label(label: str) -> str | None:
    normalized = _normalize_label(label)
    return LABEL_TO_FIELD.get(normalized)


def _normalize_label(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


LABEL_TO_FIELD = {
    _normalize_label(alias): field
    for field, aliases in LABEL_PATTERNS.items()
    for alias in aliases
}
