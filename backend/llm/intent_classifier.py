
from typing import Literal

from pydantic import BaseModel, Field

from core.config import settings
from llm.client import client


class IntentResult(BaseModel):
    intent: Literal[
        "NEW_DISCOVERY",
        "SCHEME_DETAILS",
        "FOLLOWUP_ANSWER",
        "GENERAL_QUESTION",
        "EXIT",
        "CLARIFICATION",
    ]

    scheme_id: str | None = None

    detail_type: Literal[
        "DESCRIPTION",
        "BENEFITS",
        "ELIGIBILITY",
        "DOCUMENTS",
        "APPLICATION",
        "SOURCES",
        "ALL",
        "NONE",
    ] = "NONE"

    search_query: str | None = None

    confidence: float = Field(ge=0, le=1)


def make_strict_schema(schema: dict) -> dict:
    """Prepare a Pydantic JSON schema for strict structured output."""

    if isinstance(schema, list):
        return [
            make_strict_schema(item) if isinstance(item, dict) else item
            for item in schema
        ]

    if not isinstance(schema, dict):
        return schema

    result = {}

    for key, value in schema.items():
        # Defaults are not needed in a strict output schema.
        if key == "default":
            continue

        if isinstance(value, dict):
            result[key] = make_strict_schema(value)
        elif isinstance(value, list):
            result[key] = make_strict_schema(value)
        else:
            result[key] = value

    if result.get("type") == "object" or "properties" in result:
        result["additionalProperties"] = False
        result["required"] = list(result.get("properties", {}).keys())

    return result


def classify_intent(
    message: str,
    citizen_profile: dict | None = None,
    pending_questions: list[dict] | None = None,
    active_search: str | None = None,
    displayed_schemes: list[dict] | None = None,
    conversation_context: list[dict] | None = None,
) -> IntentResult:

    context = {
        "message": message,
        "citizen_profile": citizen_profile or {},
        "pending_questions": pending_questions or [],
        "active_search": active_search,
        "displayed_schemes": displayed_schemes or [],
        "recent_conversation": conversation_context or [],
    }

    schema = make_strict_schema(
        IntentResult.model_json_schema()
    )

    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You classify messages in an Indian government welfare scheme
discovery assistant. Interpret the meaning and conversation context,
not a fixed list of phrases.

Intents:

NEW_DISCOVERY:
The user wants to discover schemes or changes the search category.

SCHEME_DETAILS:
The user asks about an already displayed scheme, its description,
benefits, eligibility, documents, application, sources, or all details.

FOLLOWUP_ANSWER:
The user answers one or more pending eligibility questions.

GENERAL_QUESTION:
The user asks a general question about the current conversation
or results.

EXIT:
The user wants to end the conversation.

CLARIFICATION:
The intended action or scheme reference is ambiguous.

Rules:
- Understand paraphrases and English or Tamil messages.
- Use pending questions and recent conversation to interpret answers.
- Resolve references such as "that scheme" and "the second one"
  against the displayed schemes when possible.
- Never invent a scheme ID.
- For scheme details, select the appropriate detail_type.
- Use ALL when the user requests all available details.
- For a new discovery, provide a concise search_query describing
  the requested category and location.
- If several schemes could match a reference, request clarification.
- Never determine eligibility. The deterministic Python engine does that.
- Confidence must be between 0 and 1.
- All fields in the requested JSON response are required.
- Use null for scheme_id or search_query when they do not apply.
- Use NONE for detail_type when it does not apply.
"""
            },
            {
                "role": "user",
                "content": str(context),
            },
        ],
        temperature=0,
        max_completion_tokens=400,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "intent_result",
                "strict": True,
                "schema": schema,
            },
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The LLM returned an empty intent response.")

    return IntentResult.model_validate_json(content)
