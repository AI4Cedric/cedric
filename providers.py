import os

from openai import OpenAI
from mistralai import Mistral

print("Mistral version :", getattr(mistralai, "__version__", "unknown"))
print("Mistral module :", mistralai.__file__)
print("Mistral attributes :", dir(mistralai))

openai_client = OpenAI(
api_key=os.getenv("OPENAI_API_KEY")
)

mistral_client = Mistral(
api_key=os.getenv("MISTRAL_API_KEY")
)

async def call_openai(prompt: str):

    response = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

async def call_mistral(prompt: str):

    response = mistral_client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

async def call_ollama(prompt: str):

    import requests

    response = requests.post(
        f"{os.getenv('OLLAMA_URL')}/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]

async def generate_response(
provider: str,
prompt: str
):

    provider = provider.lower()

    if provider == "openai":
        return await call_openai(prompt)

    if provider == "mistral":
        return await call_mistral(prompt)

    if provider == "ollama":
        return await call_ollama(prompt)

    raise Exception("Provider inconnu")
