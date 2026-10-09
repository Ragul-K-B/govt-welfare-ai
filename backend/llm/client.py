
from groq import Groq

from core.config import settings


if not settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")


client = Groq(api_key=settings.GROQ_API_KEY)


def get_llm_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant for an Indian government "
                    "welfare scheme discovery application. "
                    "Provide clear and accurate responses. "
                    "Never claim that a citizen is eligible for a "
                    "scheme without checking the official eligibility rules."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_completion_tokens=300,
    )

    return response.choices[0].message.content or ""
