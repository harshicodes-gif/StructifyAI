# backend/ocr/easyocr_engine.py

OCR_AVAILABLE = False
reader = None

try:
    import easyocr

    reader = easyocr.Reader(
        ["en"],
        gpu=False,
    )

    OCR_AVAILABLE = True

except Exception as e:
    print(f"[StructifyAI] OCR unavailable: {e}")


def extract_text(file_path: str) -> str:
    """
    Extract text using EasyOCR.

    Falls back to mock text if EasyOCR is not installed.
    """

    if not OCR_AVAILABLE or reader is None:
        return """
Asset: Pump P-101
Operator: John Smith
Issue: Bearing Failure
Priority: High
Recommendation: Replace Bearing
"""

    result = reader.readtext(file_path)

    text = []

    for _, value, _ in result:
        text.append(value)

    return "\n".join(text)
