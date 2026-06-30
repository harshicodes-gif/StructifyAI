import json

import requests

from backend.llm.prompts import PROMPT


def extract_json(text: str) -> dict:
    prompt = PROMPT.format(text=text)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
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
