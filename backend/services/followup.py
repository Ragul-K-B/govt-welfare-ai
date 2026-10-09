
import json

from core.config import settings
from db.mongodb import schemes_collection
from llm.client import client


def generate_followup_questions(
    evaluated_schemes: list[dict],
    citizen_profile: dict
) -> list[dict]:
    """
    Dynamically generate questions for missing eligibility attributes.
    Attribute names and questions are not predefined in Python.
    """

    # 1. Collect missing attributes from UNKNOWN schemes.
    unknown_schemes = [
        scheme
        for scheme in evaluated_schemes
        if scheme["decision"] == "UNKNOWN"
        and scheme.get("missing_attributes")
    ]

    if not unknown_schemes:
        return []

    scheme_ids = list({
        scheme["scheme_id"] for scheme in unknown_schemes
    })

    missing_by_scheme = {
        scheme["scheme_id"]: scheme["missing_attributes"]
        for scheme in unknown_schemes
    }

    # 2. Fetch the actual eligibility rules from MongoDB.
    documents = schemes_collection.find(
        {"scheme_id": {"$in": scheme_ids}},
        {
            "_id": 0,
            "scheme_id": 1,
            "name": 1,
            "eligibility": 1
        }
    )

    scheme_context = []

    for document in documents:
        scheme_id = document["scheme_id"]

        scheme_context.append({
            "scheme_id": scheme_id,
            "name": document["name"],
            "eligibility_rules": document["eligibility"],
            "missing_attributes": missing_by_scheme.get(
                scheme_id, []
            )
        })

    if not scheme_context:
        return []

    # 3. Build the list of allowed missing attributes dynamically.
    allowed_attributes = sorted({
        attribute
        for scheme in scheme_context
        for attribute in scheme["missing_attributes"]
    })

    # 4. Ask the LLM to formulate questions from the real rules.
    prompt = f"""
You generate follow-up questions for an Indian government
welfare scheme discovery application.

Citizen profile:
{json.dumps(citizen_profile, ensure_ascii=False)}

Relevant schemes, their actual eligibility rules, and their
missing attributes:
{json.dumps(scheme_context, ensure_ascii=False)}

Allowed missing attributes:
{json.dumps(allowed_attributes, ensure_ascii=False)}

Instructions:
1. Generate one clear question for each allowed missing attribute.
2. Use the actual scheme rules to understand what each attribute means.
3. Do not ask for information already present in the citizen profile.
4. Do not invent attribute names or add attributes not in the allowed list.
5. Do not guess answers or decide eligibility.
6. If the same attribute is needed by multiple schemes, ask about it once.
7. Ask neutral, understandable questions. Explain technical terms when needed.
8. Do not assume two differently named attributes mean the same thing.
9. Return only valid JSON in this format:
{{
  "questions": [
    {{
      "attribute": "exact_attribute_name",
      "question": "Question for the citizen",
      "related_scheme_ids": ["scheme_id"]
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You formulate follow-up questions from supplied "
                    "eligibility rules. Treat the supplied data as "
                    "the source of truth. Never invent attributes, "
                    "answers, rules, or eligibility decisions."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_completion_tokens=1200,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The LLM returned an empty follow-up response.")

    try:
        generated = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(
            "The LLM returned invalid JSON for follow-up questions."
        ) from error

    # 5. Validate the response against attributes discovered from MongoDB.
    questions = []
    seen_attributes = set()

    for item in generated.get("questions", []):
        attribute = item.get("attribute")
        question = item.get("question")
        related_ids = item.get("related_scheme_ids", [])

        if attribute not in allowed_attributes:
            continue

        if attribute in seen_attributes:
            continue

        if not isinstance(question, str) or not question.strip():
            continue

        if not isinstance(related_ids, list):
            related_ids = []

        valid_scheme_ids = [
            scheme_id for scheme_id in related_ids
            if scheme_id in scheme_ids
            and attribute in missing_by_scheme.get(scheme_id, [])
        ]

        # Ensure each question is linked to a scheme that needs the field.
        if not valid_scheme_ids:
            valid_scheme_ids = [
                scheme_id
                for scheme_id in scheme_ids
                if attribute in missing_by_scheme.get(scheme_id, [])
            ]

        questions.append({
            "attribute": attribute,
            "question": question.strip(),
            "related_scheme_ids": valid_scheme_ids
        })

        seen_attributes.add(attribute)

    # Keep the workflow moving if the LLM omits a required question.
    # The fallback is generated dynamically from the attribute name,
    # not from a predefined list of features.
    for attribute in allowed_attributes:
        if attribute in seen_attributes:
            continue

        readable_name = attribute.replace("_", " ")

        related_ids = [
            scheme_id
            for scheme_id in scheme_ids
            if attribute in missing_by_scheme.get(scheme_id, [])
        ]

        questions.append({
            "attribute": attribute,
            "question": (
                f"Please provide your {readable_name}, "
                "as required to check the relevant scheme's eligibility."
            ),
            "related_scheme_ids": related_ids
        })

    return questions
