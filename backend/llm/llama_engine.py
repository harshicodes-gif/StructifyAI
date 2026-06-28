import json
from pathlib import Path

from backend.llm.prompts import PROMPT

# Flag to determine whether the local LLM is available
LLM_AVAILABLE = False
llm = None

try:
    from llama_cpp import Llama

    MODEL_PATH = Path("models/qwen2.5-3b-instruct-q4_k_m.gguf")

    if MODEL_PATH.exists():
        llm = Llama(
            model_path=str(MODEL_PATH),
            n_ctx=4096,
            n_threads=8,
        )
        LLM_AVAILABLE = True

except Exception as e:
    print(f"[StructifyAI] Local LLM unavailable: {e}")


def extract_json(text: str) -> dict:
    """
    Convert OCR text into structured JSON.

    Uses the local LLM if available.
    Otherwise returns a mock response so the app continues to work.
    """

    if not LLM_AVAILABLE or llm is None:
        return {
            "asset": "Pump P-101",
            "operator": "John Smith",
            "issue": "Bearing Failure",
            "priority": "High",
            "recommendation": "Replace Bearing",
            "note": "Mock response (llama.cpp not installed or model not found)",
        }

    prompt = PROMPT.format(text=text)

    output = llm(
        prompt,
        max_tokens=512,
        temperature=0,
    )

    response = output["choices"][0]["text"]

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"raw_response": response, "error": "Model did not return valid JSON."}
