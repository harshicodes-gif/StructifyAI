from backend.ocr.easyocr_engine import extract_text
from backend.llm.llama_engine import extract_json


def process_document(file_path: str) -> dict:
    """
    Complete document processing pipeline.

    Image/PDF
        ↓
    OCR
        ↓
    LLM
        ↓
    Structured JSON
    """

    extracted_text = extract_text(file_path)

    structured_json = extract_json(extracted_text)

    return structured_json