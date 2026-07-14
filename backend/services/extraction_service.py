import json

from backend.cache.cache import get_cache, set_cache
from backend.llm.llama_engine import extract_json, is_ollama_available
from backend.ocr.easyocr_engine import extract_text


def process_document(file_path: str) -> dict:
    """
    Complete document processing pipeline.

    Image / PDF
        ↓
    OCR / Text Extraction
        ↓
    Cache
        ↓
    Ollama (if available)
        ↓
    Dynamic Structured JSON
    """

    cached_result = get_cache(file_path)

    if cached_result is not None:
        return cached_result

    extracted_text = extract_text(file_path)

    processing_mode = "Ollama" if is_ollama_available() else "OCR Only"

    # ---------- Use Ollama whenever available ----------
    if is_ollama_available():
        structured_json = extract_json(extracted_text)
    else:
        structured_json = {
            "document_type": "Unknown",
            "summary": extracted_text[:500],
            "raw_text": extracted_text,
            "note": (
                "Ollama is not available. "
                "Install/start Ollama to enable AI extraction."
            ),
        }

    # ---------- Normalize response ----------
    if isinstance(structured_json, str):
        try:
            structured_json = json.loads(structured_json)
        except json.JSONDecodeError:
            structured_json = {
                "document_type": "Unknown",
                "raw_output": structured_json,
                "raw_text": extracted_text,
            }

    if not isinstance(structured_json, dict):
        structured_json = {
            "document_type": "Unknown",
            "raw_text": extracted_text,
        }

    result = {
        "file_path": file_path,
        "processing_mode": processing_mode,
        "extracted_text": extracted_text,
        "structured_json": structured_json,
    }

    set_cache(file_path, result)

    return result