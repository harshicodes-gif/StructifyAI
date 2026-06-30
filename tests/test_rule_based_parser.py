from backend.services.rule_based_parser import parse_ocr_text


def test_parse_ocr_text_extracts_known_fields():
    result = parse_ocr_text("""
        Maintenance Report
        Asset: Pump P-101
        Operator: John Smith
        Issue: Bearing Failure
        Priority: High
        Recommendation: Replace Bearing
        Date: 2026-06-30
        """)

    assert result["document_type"] == "Maintenance Report"
    assert result["asset"] == "Pump P-101"
    assert result["operator"] == "John Smith"
    assert result["issue"] == "Bearing Failure"
    assert result["priority"] == "High"
    assert result["recommendation"] == "Replace Bearing"
    assert result["date"] == "2026-06-30"
    assert result["processing_mode"] == "OCR Only"


def test_parse_ocr_text_uses_not_found_for_missing_fields():
    result = parse_ocr_text("Unlabelled scanned text")

    assert result["asset"] == "Not found"
    assert result["operator"] == "Not found"
    assert result["issue"] == "Not found"
    assert result["priority"] == "Not found"
    assert result["recommendation"] == "Not found"
    assert result["date"] == "Not found"


def test_parse_ocr_text_extracts_multiline_maintenance_report():
    result = parse_ocr_text("""
        MAINTENANCE REPORT

        Report ID: MR-2026-001
        Date: 30-06-2026

        Department: Production

        Asset: Pump P-101
        Operator: Adwitha Reddy

        Issue:
        Excessive vibration and oil leakage observed near the pump bearing.

        Priority: High

        Recommendation:
        Replace the damaged bearing, inspect the shaft alignment, and refill lubricating oil before restarting the equipment.
        """)

    assert result["document_type"] == "Maintenance Report"
    assert result["asset"] == "Pump P-101"
    assert result["operator"] == "Adwitha Reddy"
    assert (
        result["issue"]
        == "Excessive vibration and oil leakage observed near the pump bearing."
    )
    assert result["priority"] == "High"
    assert (
        result["recommendation"]
        == "Replace the damaged bearing, inspect the shaft alignment, and refill lubricating oil before restarting the equipment."
    )
    assert result["date"] == "30-06-2026"
