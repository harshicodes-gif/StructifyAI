import json
import os
from functools import lru_cache

import requests
import streamlit as st
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


def get_groq_api_key():
    """Return Groq API key from Streamlit Secrets or environment."""

    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    return os.getenv("GROQ_API_KEY")


def is_groq_available() -> bool:
    return bool(get_groq_api_key())


def get_llm_mode() -> str:
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

    return _parse_response(
        response.json()["response"]
    )


def _extract_with_groq(prompt: str) -> dict:

    client = Groq(
        api_key=get_groq_api_key(),
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

    return _parse_response(
        completion.choices[0].message.content
    )


def extract_json(text: str) -> dict:
    """
    Convert OCR text into structured JSON.
    """

    prompt = PROMPT.format(text=text)

    try:

        if is_ollama_available():
            return _extract_with_ollama(prompt)

        if is_groq_available():
            return _extract_with_groq(prompt)

        return {
            "document_type": "Unknown",
            "summary": "No AI backend available.",
            "note": "Configure Ollama locally or add GROQ_API_KEY in Streamlit Secrets.",
        }

    except Exception as exc:

        return {
            "document_type": "Unknown",
            "summary": str(exc),
        }
