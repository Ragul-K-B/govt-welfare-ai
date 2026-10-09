
import json

from core.config import settings
from llm.client import client


def extract_followup_answers(
    message: str,
    pending_questions: list[dict],
    citizen_profile: dict
) -> dict:
    if not pending_questions:
        return {}

    allowed_attributes = [
        item["attribute"] for item in pending_questions
    ]

    prompt = f"""
Extract answers from the citizen's latest message.

Citizen's latest message:
{message}

Existing citizen profile:
{json.dumps(citizen_profile, ensure_ascii=False)}

Attributes we are currently asking about:
{json.dumps(allowed_attributes, ensure_ascii=False)}

Questions and their meanings:
{json.dumps(pending_questions, ensure_ascii=False)}

Rules:
1. Extract only information explicitly stated or
   unambiguously expressed in the latest message.
2. Return only attributes from the allowed list.
3. Do not guess missing answers.
4. Do not change existing profile information unless
   the citizen explicitly corrects it.
5. Use null only when an allowed attribute is mentioned
   but its answer cannot be determined.
6. Preserve appropriate value types, such as numbers
   and booleans, when the meaning is clear.
7. Return only a JSON object in this format:
   {{"answers": {{"attribute_name": "answer"}}}}
"""

    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract citizen answers. "
                    "Never invent facts or eligibility decisions."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_completion_tokens=500,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The LLM returned an empty answer response.")

    try:
        result = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(
            "The LLM returned invalid JSON for citizen answers."
        ) from error

    extracted = result.get("answers", {})

    if not isinstance(extracted, dict):
        raise ValueError("The extracted answers must be a JSON object.")

    # Accept only attributes the application actually asked about.
    allowed_set = set(allowed_attributes)

    return {
        attribute: value
        for attribute, value in extracted.items()
        if attribute in allowed_set and value is not None
    }
