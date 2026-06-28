from backend.cache.cache import get, set
from backend.llm.llama_engine import extract_json
from backend.ocr.easyocr_engine import extract_text


def process_document(file_path: str) -> dict:
    """
    Complete document processing pipeline.

    Image/PDF
        ↓
    OCR
        ↓
    Cache Lookup
        ↓
    Local LLM
        ↓
    Structured JSON
    """

    text = extract_text(file_path)

    cached = get(text)

    if cached is not None:
        return cached

    result = extract_json(text)

    set(text, result)

    return result