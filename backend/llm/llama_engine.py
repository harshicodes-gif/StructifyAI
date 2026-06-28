import json

from llama_cpp import Llama

from backend.llm.prompts import PROMPT

MODEL_PATH = "models/qwen2.5-3b-instruct-q4_k_m.gguf"

llm = Llama(

    model_path=MODEL_PATH,

    n_ctx=4096,

    n_threads=8,

)


def extract_json(text):

    prompt = PROMPT.format(text=text)

    output = llm(

        prompt,

        max_tokens=512,

        temperature=0,

    )

    response = output["choices"][0]["text"]

    return json.loads(response)