import json
from functools import lru_cache

import requests

from backend.llm.prompts import PROMPT

OLLAMA_URL = "http://localhost:11434"
OLLAMA_TAGS_URL = f"{OLLAMA_URL}/api/tags"
OLLAMA_GENERATE_URL = f"{OLLAMA_URL}/api/generate"

# Default model. Change if you pull a different one.
MODEL_NAME = "llama3.2:1b"


@lru_cache(maxsize=1)
def is_ollama_available() -> bool:
    """Return whether the local Ollama server is running."""
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=2)
        return response.ok
    except requests.RequestException:
        return False


def get_llm_mode() -> str:
    """Return the active LLM mode."""
    return "Ollama" if is_ollama_available() else "OCR Only"


def extract_json(text: str) -> dict:
    """
    Convert OCR text into structured JSON using Ollama.
    """

    if not is_ollama_available():
        return {
            "document_type": "Unknown",
            "asset": "Not found",
            "operator": "Not found",
            "issue": "Not found",
            "priority": "Not found",
            "recommendation": "Not found",
            "date": "Not found",
            "error": "Ollama is not running.",
        }

    prompt = PROMPT.format(text=text)

    try:
        response = requests.post(
            OLLAMA_GENERATE_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=120,
        )

        response.raise_for_status()

        output = response.json().get("response", "{}")

        return json.loads(output)

    except Exception as e:
        return {
            "document_type": "Unknown",
            "asset": "Not found",
            "operator": "Not found",
            "issue": "Not found",
            "priority": "Not found",
            "recommendation": "Not found",
            "date": "Not found",
            "error": str(e),
        }
