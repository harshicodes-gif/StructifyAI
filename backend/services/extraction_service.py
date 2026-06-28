from backend.cache.cache import get

from backend.cache.cache import set

from backend.llm.llama_engine import extract_json

from backend.ocr.easyocr_engine import extract_text


def process_document(image_path):

    text = extract_text(image_path)

    cached = get(text)

    if cached:

        return cached

    result = extract_json(text)

    set(text, result)

    return result