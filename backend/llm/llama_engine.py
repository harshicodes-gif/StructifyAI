import json
from functools import lru_cache

import requests

from backend.llm.prompts import PROMPT

OLLAMA_URL = "http://localhost:11434"
OLLAMA_TAGS_URL = f"{OLLAMA_URL}/api/tags"
OLLAMA_GENERATE_URL = f"{OLLAMA_URL}/api/generate"

MODEL_NAME = "llama3.2:3b"


@lru_cache(maxsize=1)
def is_ollama_available() -> bool:
    """Return whether the local Ollama server is running."""
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=2)
        return response.ok
    except requests.RequestException:
        return False


def get_llm_mode() -> str:
    """Return the active processing mode."""
    return "Ollama" if is_ollama_available() else "OCR Only"


def _default_response(error: str = "") -> dict:
    """Return a default structured response."""
    return {
        "document_type": "Unknown",
        "asset": "Not found",
        "operator": "Not found",
        "issue": "Not found",
        "priority": "Not found",
        "recommendation": "Not found",
        "date": "Not found",
        "error": error,
    }


def extract_json(text: str) -> dict:
    """
    Convert OCR text into structured JSON using Ollama.
    """

    if not is_ollama_available():
        return _default_response("Ollama is not running.")

    try:
        prompt = PROMPT.format(text=text)

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

        payload = response.json()

        output = payload.get("response", "")

        if not isinstance(output, str):
            return _default_response("Invalid response returned by Ollama.")

        output = output.strip()

        # Remove markdown fences if present
        if output.startswith("```"):
            output = (
                output.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        try:
            structured = json.loads(output)
        except json.JSONDecodeError:
            return _default_response(
                f"Invalid JSON returned by Ollama:\n\n{output}"
            )

        if not isinstance(structured, dict):
            return _default_response("Model returned non-dictionary JSON.")

        defaults = _default_response()

        for key, value in defaults.items():
            structured.setdefault(key, value)

        return structured

    except Exception as exc:
        return _default_response(str(exc))