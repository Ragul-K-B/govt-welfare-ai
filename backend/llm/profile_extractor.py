
from pydantic import ValidationError

from core.config import settings
from schemas.citizen import CitizenProfile
from llm.client import client


def extract_citizen_profile(message: str) -> CitizenProfile:
    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You extract citizen attributes for an Indian government
welfare scheme discovery application.

Extract only facts explicitly stated or unambiguously expressed
in the citizen's message.

Rules:
- Never guess missing information.
- Use null for unknown attributes.
- Convert annual income such as "2 lakh per year" to 200000.
- Convert clear age, percentage and income values to numbers.
- Do not determine scheme eligibility.
- The message may be in English or Tamil.
"""
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0,
        max_completion_tokens=500,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "citizen_profile",
                "strict": True,
                "schema": {
    **CitizenProfile.model_json_schema(),
    "required": list(
        CitizenProfile.model_fields.keys()
    )
}
            }
        }
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The LLM returned an empty response.")

    try:
        return CitizenProfile.model_validate_json(content)
    except ValidationError as error:
        raise ValueError(
            "The LLM returned an invalid citizen profile."
        ) from error
