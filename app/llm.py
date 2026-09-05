import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:1.7b"


def generate_answer(question: str, evidence: str) -> str:
    """
    Generate an answer using the local Qwen3 model.
    """

    prompt = f"""
You are VERITY, an evidence-first AI answer engine.

Answer the user's question using ONLY the provided evidence.

Do not invent facts.
Do not use outside knowledge.
If the evidence is insufficient, clearly say that the evidence is insufficient.

User question:
{question}

Evidence:
{evidence}
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "think": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]