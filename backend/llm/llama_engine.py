import json
from pathlib import Path

from backend.llm.prompts import PROMPT

LLM_AVAILABLE = False
llm = None

try:
    from llama_cpp import Llama

    # Path to your GGUF model
    MODEL_PATH = Path("models/qwen.gguf")

    print(f"Looking for model at: {MODEL_PATH.resolve()}")
    print(f"Model exists: {MODEL_PATH.exists()}")

    if MODEL_PATH.exists():
        print("Loading Qwen model...")

        llm = Llama(
            model_path=str(MODEL_PATH),
            n_ctx=4096,
            n_threads=8,
            verbose=False,
        )

        LLM_AVAILABLE = True
        print("✅ Qwen model loaded successfully!")

    else:
        print("❌ Model file not found!")

except Exception as e:
    print("❌ Failed to initialize llama.cpp")
    print(e)


def extract_json(text: str) -> dict:
    """
    Converts OCR text into structured JSON using the local Qwen model.
    Falls back to a mock response if the model isn't available.
    """

    if not LLM_AVAILABLE or llm is None:
        return {
            "asset": "Pump P-101",
            "operator": "John Smith",
            "issue": "Bearing Failure",
            "priority": "High",
            "recommendation": "Replace Bearing",
            "note": "Mock response (Qwen model unavailable)",
        }

    prompt = PROMPT.format(text=text)

    try:
        output = llm(
            prompt,
            max_tokens=512,
            temperature=0,
        )

        response = output["choices"][0]["text"].strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return {
                "error": "Model did not return valid JSON.",
                "raw_response": response,
            }

    except Exception as e:
        return {"error": f"LLM inference failed: {e}"}
