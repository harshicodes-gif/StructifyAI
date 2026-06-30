import json
from functools import lru_cache

import requests

from backend.llm.prompts import PROMPT

OLLAMA_URL = "http://localhost:11434"
OLLAMA_TAGS_URL = f"{OLLAMA_URL}/api/tags"
OLLAMA_GENERATE_URL = f"{OLLAMA_URL}/api/generate"
MODEL_NAME = "llama3.2:1b"


@lru_cache(maxsize=1)
def is_ollama_available() -> bool:
    """Return whether local Ollama is reachable."""
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=2)
    except requests.RequestException:
        return False

    return response.ok


def get_llm_mode() -> str:
    """Return the active processing mode label."""
    return "Ollama" if is_ollama_available() else "OCR Only"


def extract_json(text: str) -> dict:
    if not is_ollama_available():
        raise RuntimeError("Ollama is not available.")

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

        data = response.json()
        output = data.get("response", "{}")

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
