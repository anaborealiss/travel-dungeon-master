import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    return client


def ask_llm(messages):
    client = get_client()

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4
    )

    return response.choices[0].message.content