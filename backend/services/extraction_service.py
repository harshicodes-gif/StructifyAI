import json

from backend.cache.cache import get, set_cache
from backend.llm.llama_engine import extract_json
from backend.ocr.easyocr_engine import extract_text


def process_document(file_path: str) -> dict:
    cached_result = get(file_path)

    if cached_result:
        return cached_result

    extracted_text = extract_text(file_path)

    structured_json = extract_json(extracted_text)

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
    }

    set_cache(file_path, result)

    return result