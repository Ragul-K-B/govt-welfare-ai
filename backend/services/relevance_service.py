
import json

from llm.client import get_llm_response


def validate_scheme_relevance(
    user_need: str,
    schemes: list[dict],
) -> dict:
    """
    Determine whether retrieved schemes address the user's need.

    Relevance validation is separate from eligibility evaluation.
    """

    no_match_message = (
        "No suitable scheme was identified among the candidates "
        "checked in the current scheme database."
    )

    if not schemes:
        return {
            "relevant_schemes": [],
            "uncertain_schemes": [],
            "no_match": True,
            "message": no_match_message,
        }

    candidates = [
        {
            "scheme_id": scheme.get("scheme_id"),
            "name": scheme.get("name"),
            "description": scheme.get("description"),
            "benefits": scheme.get("benefits"),
        }
        for scheme in schemes
    ]

    prompt = f"""
Classify each government scheme against the user's requested need.

USER NEED:
{user_need}

CANDIDATES:
{json.dumps(candidates, ensure_ascii=False, default=str)}

Rules:
- RELEVANT means the scheme's stated purpose or benefits directly
  address the requested need.
- NOT_RELEVANT means they do not address the requested need.
- UNCERTAIN means the supplied information is insufficient.
- Financial assistance in general does not automatically mean a
  scheme provides a business loan or startup funding.
- Do not determine citizen eligibility.
- Do not invent facts.
- Include every candidate exactly once.
- Use the exact scheme IDs provided.
- Return ONLY compact, valid JSON. No Markdown fences or extra text.
- Do not include reasons or explanations.

Required format:
{{"results":[{{"scheme_id":"EXACT_ID","status":"RELEVANT"}}]}}

Allowed statuses: RELEVANT, NOT_RELEVANT, UNCERTAIN.
"""

    response = get_llm_response(prompt)

    try:
        result = json.loads(response)
    except (json.JSONDecodeError, TypeError) as error:
        print("\n--- INVALID RELEVANCE VALIDATOR RESPONSE ---")
        print(repr(response))
        print("--- END INVALID RESPONSE ---\n")

        raise ValueError(
            "Relevance validator returned invalid or incomplete JSON. "
            "No relevance decision was made."
        ) from error

    returned_results = result.get("results")

    if not isinstance(returned_results, list):
        raise ValueError(
            "Relevance validator response must contain a results list."
        )

    candidate_ids = {
        str(scheme.get("scheme_id"))
        for scheme in schemes
    }

    status_by_id = {}

    for item in returned_results:
        if not isinstance(item, dict):
            raise ValueError(
                "Relevance validator returned an invalid result item."
            )

        scheme_id = str(item.get("scheme_id", ""))
        status = item.get("status")

        if scheme_id not in candidate_ids:
            raise ValueError(
                f"Unknown scheme ID returned: {scheme_id}"
            )

        if scheme_id in status_by_id:
            raise ValueError(
                f"Duplicate scheme ID returned: {scheme_id}"
            )

        if status not in {"RELEVANT", "NOT_RELEVANT", "UNCERTAIN"}:
            raise ValueError(
                f"Invalid relevance status: {status}"
            )

        status_by_id[scheme_id] = status

    if set(status_by_id) != candidate_ids:
        raise ValueError(
            "Relevance validator did not classify every candidate. "
            f"Expected {len(candidate_ids)} candidates, "
            f"received {len(status_by_id)} valid classifications."
        )

    relevant_schemes = [
        scheme
        for scheme in schemes
        if status_by_id[str(scheme.get("scheme_id"))] == "RELEVANT"
    ]

    uncertain_schemes = [
        scheme
        for scheme in schemes
        if status_by_id[str(scheme.get("scheme_id"))] == "UNCERTAIN"
    ]

    no_match = not relevant_schemes and not uncertain_schemes

    if no_match:
        message = no_match_message
    elif uncertain_schemes and not relevant_schemes:
        message = (
            "I couldn't confidently identify a suitable scheme among "
            "the candidates checked. More information or a broader "
            "search may be needed."
        )
    else:
        message = (
            f"I found {len(relevant_schemes)} relevant scheme(s) "
            "among the candidates checked. Review the eligibility "
            "results and answer any follow-up questions below."
        )

    return {
        "relevant_schemes": relevant_schemes,
        "uncertain_schemes": uncertain_schemes,
        "no_match": no_match,
        "message": message,
    }
