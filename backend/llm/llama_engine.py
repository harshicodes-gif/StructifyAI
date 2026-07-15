import json
import os
from functools import lru_cache

import requests
from groq import Groq

from backend.llm.prompts import PROMPT

OLLAMA_URL = "http://localhost:11434"
OLLAMA_TAGS_URL = f"{OLLAMA_URL}/api/tags"
OLLAMA_GENERATE_URL = f"{OLLAMA_URL}/api/generate"

OLLAMA_MODEL = "llama3.2:3b"
GROQ_MODEL = "llama-3.1-8b-instant"


@lru_cache(maxsize=1)
def is_ollama_available() -> bool:
    """Return whether the local Ollama server is running."""
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=2)
        return response.ok
    except requests.RequestException:
        return False


def is_groq_available() -> bool:
    """Return whether a Groq API key is configured."""
    return bool(os.getenv("GROQ_API_KEY"))


def get_llm_mode() -> str:
    """Return the active AI backend."""
    if is_ollama_available():
        return "Ollama"

    if is_groq_available():
        return "Groq"

    return "OCR Only"


def _default_response(error: str = "") -> dict:
    response = {
        "document_type": "Unknown",
    }

    if error:
        response["error"] = error

    return response


def _clean_json(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = (
            text.replace("```json", "")
            .replace("```JSON", "")
            .replace("```", "")
            .strip()
        )

    return text


def _parse_response(text: str) -> dict:
    text = _clean_json(text)

    try:
        data = json.loads(text)

        if isinstance(data, dict):
            data.setdefault("document_type", "Unknown")
            return data

    except Exception:
        pass

    return {
        "document_type": "Unknown",
        "summary": text,
    }


def _extract_with_ollama(prompt: str) -> dict:
    response = requests.post(
        OLLAMA_GENERATE_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        },
        timeout=180,
    )

    response.raise_for_status()

    output = response.json()["response"]

    return _parse_response(output)


def _extract_with_groq(prompt: str) -> dict:
    client = Groq(
        api_key=os.environ["GROQ_API_KEY"],
    )

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    output = completion.choices[0].message.content

    return _parse_response(output)


def extract_json(text: str) -> dict:
    """Convert OCR text into structured JSON."""

    prompt = PROMPT.format(text=text)

    try:

        if is_ollama_available():
            return _extract_with_ollama(prompt)

        if is_groq_available():
            return _extract_with_groq(prompt)

        return _default_response(
            "No AI backend configured."
        )

    except Exception as exc:
        return _default_response(str(exc))
