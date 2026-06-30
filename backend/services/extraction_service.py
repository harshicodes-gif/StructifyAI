import json

from backend.cache.cache import get_cache, set_cache
from backend.llm.llama_engine import extract_json, is_ollama_available
from backend.ocr.easyocr_engine import extract_text
from backend.services.rule_based_parser import parse_ocr_text


def process_document(file_path: str) -> dict:
    """
       Complete document processing pipeline.

       Image/PDF
           ↓
         OCR
           ↓
        Cache
           ↓
         LLM
           ↓
    Structured JSON
    """

    cached_result = get_cache(file_path)

    if cached_result is not None:
        return cached_result

    extracted_text = extract_text(file_path)

    processing_mode = "Ollama" if is_ollama_available() else "OCR Only"

    if processing_mode == "Ollama":
        structured_json = extract_json(extracted_text)
    else:
        structured_json = parse_ocr_text(extracted_text)

    if isinstance(structured_json, str):
        try:
            structured_json = json.loads(structured_json)
        except json.JSONDecodeError:
            structured_json = {
                "document_type": "Unknown",
                "extracted_text": extracted_text,
                "raw_output": structured_json,
            }

    result = {
        "file_path": file_path,
        "extracted_text": extracted_text,
        "structured_json": structured_json,
        "processing_mode": processing_mode,
    }

    set_cache(file_path, result)

    return result
