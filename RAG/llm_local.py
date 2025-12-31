import requests
import json

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"


def ask_llm(context: str, question: str) -> str:
    if context and context.strip():
        prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""
    else:
        prompt = question

    payload = {
        "model": "local-model",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(
        LM_STUDIO_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    if response.status_code != 200:
        return "Local model is not responding."

    return response.json()["choices"][0]["message"]["content"].strip()
