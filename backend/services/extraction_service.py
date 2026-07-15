import json

from backend.cache.cache import get_cache, set_cache
from backend.llm.llama_engine import extract_json, get_llm_mode
from backend.ocr.easyocr_engine import extract_text


def process_document(file_path: str) -> dict:
    """
    Complete document processing pipeline.

    Image/PDF
        ↓
    OCR/Text Extraction
        ↓
    AI (Ollama or Groq)
        ↓
    Structured JSON
    """

    cached_result = get_cache(file_path)

    if cached_result is not None:
        return cached_result

    extracted_text = extract_text(file_path)

    processing_mode = get_llm_mode()

    # Always call the LLM.
    # extract_json() will automatically choose:
    #   Ollama
    #   Groq
    #   OCR fallback
    structured_json = extract_json(extracted_text)

    # Normalize response
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
