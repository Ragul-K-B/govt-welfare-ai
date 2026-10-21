
import json

from llm.intent_classifier import classify_intent
from llm.client import get_llm_response
from services.discovery import discover_schemes
from services.conversation import continue_discovery


MIN_INTENT_CONFIDENCE = 0.60
TOP_K = 5


def visible_schemes(result: dict | None) -> list[dict]:
    """Return only PASS and UNKNOWN schemes for display."""
    if not result:
        return []

    return [
        scheme
        for scheme in result.get("schemes", [])
        if str(scheme.get("decision", "")).upper()
        in ("PASS", "UNKNOWN")
    ]


def find_scheme_by_id(
    scheme_identifier: str | None,
    last_result: dict | None,
) -> dict | None:
    """Resolve a scheme ID against currently displayed schemes."""
    if not scheme_identifier or not last_result:
        return None

    target = str(scheme_identifier).strip().casefold()

    for scheme in visible_schemes(last_result):
        if str(scheme.get("scheme_id", "")).strip().casefold() == target:
            return scheme

    return None


def find_scheme_by_name(
    message: str,
    last_result: dict | None,
) -> dict | None:
    """Match an exact displayed scheme name or ID."""
    if not last_result:
        return None

    target = message.strip().casefold()
    matches = []

    for scheme in visible_schemes(last_result):
        name = str(scheme.get("name", "")).strip().casefold()
        scheme_id = str(scheme.get("scheme_id", "")).strip().casefold()

        if target and target in (name, scheme_id):
            matches.append(scheme)

    return matches[0] if len(matches) == 1 else None


def answer_general_question(
    message: str,
    last_result: dict | None,
    citizen_profile: dict,
) -> str:
    """Answer general questions without triggering scheme retrieval."""
    result = last_result or {}

    context = {
        "user_question": message,
        "citizen_profile": citizen_profile,
        "active_search": result.get("retrieval_query"),
        "displayed_schemes": visible_schemes(result),
        "uncertain_schemes": result.get("uncertain_schemes", []),
        "no_match": result.get("no_match", False),
        "discovery_message": result.get("message"),
    }

    prompt = f"""
You are a helpful assistant for a government welfare scheme discovery
application in India.

Answer the user's question directly and clearly.

GENERAL KNOWLEDGE:
- You may explain general concepts and terminology, including the
  difference between a subsidy, scholarship, and government scheme.
- Do not refuse a general conceptual question just because the
  supplied context does not contain a definition.
- Distinguish general explanations from facts about a specific scheme.

GOVERNMENT SCHEME FACTS:
- Use the supplied context for claims about schemes in this conversation.
- Never invent scheme benefits, required documents, deadlines,
  application procedures, official sources, or eligibility conditions.
- If specific scheme information is missing, say so.
- A PASS decision is not official government approval.
- Do not present uncertain schemes as confirmed relevant matches.
- A no-match result means no suitable scheme was identified among
  the candidates checked; it does not prove no scheme exists anywhere.

Keep the answer relevant. Do not repeat the entire context.

Context:
{json.dumps(context, ensure_ascii=False, default=str)}
"""

    answer = get_llm_response(prompt)

    if answer and answer.strip():
        return answer.strip()

    return "I couldn't generate an answer right now. Please try again."


def handle_chat(
    message: str,
    citizen_profile: dict | None = None,
    pending_questions: list[dict] | None = None,
    last_result: dict | None = None,
    active_search: str | None = None,
    conversation_context: list[dict] | None = None,
    top_k: int = TOP_K,
) -> dict:
    """Route one chat message and return the updated conversation state."""

    profile = (citizen_profile or {}).copy()
    pending = pending_questions or []
    context = (conversation_context or [])[-8:]
    result = last_result
    search = active_search or (
        result.get("retrieval_query") if result else None
    )

    intent = classify_intent(
        message=message,
        citizen_profile=profile,
        pending_questions=pending,
        active_search=search,
        displayed_schemes=visible_schemes(result),
        conversation_context=context,
    )

    response = {
        "intent": intent.intent,
        "answer": "",
        "profile": profile,
        "pending_questions": pending,
        "last_result": result,
        "active_search": search,
        "conversation_context": context,
        "result": None,
        "scheme_details": None,
        "ended": False,
    }

    if (
        intent.confidence < MIN_INTENT_CONFIDENCE
        or intent.intent == "CLARIFICATION"
    ):
        response["answer"] = (
            "I'm not sure what you'd like me to do. You can ask about "
            "a displayed scheme, answer an eligibility question, ask "
            "a general question, or describe the schemes you need."
        )

    elif intent.intent == "EXIT":
        response["answer"] = (
            "Thank you for using Welfare AI. You can continue chatting "
            "whenever you need help with government welfare schemes."
        )
        response["ended"] = True

    elif intent.intent == "GENERAL_QUESTION":
        try:
            response["answer"] = answer_general_question(
                message=message,
                last_result=result,
                citizen_profile=profile,
            )
        except Exception:
            response["answer"] = (
                "I couldn't answer that question right now. Please try again."
            )

    elif intent.intent == "SCHEME_DETAILS":
        scheme = find_scheme_by_id(intent.scheme_id, result)

        if scheme is None:
            scheme = find_scheme_by_name(message, result)

        if scheme is not None:
            response["scheme_details"] = {
                "scheme": scheme,
                "detail_type": (
                    "ALL"
                    if intent.detail_type == "NONE"
                    else intent.detail_type
                ),
            }
            response["answer"] = (
                f"Here are the requested details for {scheme.get('name', 'the scheme')}."
            )
        else:
            search_query = intent.search_query or intent.scheme_id or message
            new_result = discover_schemes(
                message=search_query,
                top_k=top_k,
                existing_profile=profile,
            )
            result = new_result
            profile = new_result.get("profile", profile)
            pending = new_result.get("followup_questions", [])
            search = new_result.get("retrieval_query", search_query)

            response.update({
                "answer": new_result.get("message", ""),
                "profile": profile,
                "pending_questions": pending,
                "last_result": result,
                "active_search": search,
                "result": new_result,
            })

    elif intent.intent == "NEW_DISCOVERY":
        search_query = intent.search_query or message

        new_result = discover_schemes(
            message=search_query,
            top_k=top_k,
            existing_profile=profile,
        )

        result = new_result
        profile = new_result.get("profile", profile)
        pending = new_result.get("followup_questions", [])
        search = new_result.get("retrieval_query", search_query)

        response.update({
            "answer": new_result.get("message", ""),
            "profile": profile,
            "pending_questions": pending,
            "last_result": result,
            "active_search": search,
            "result": new_result,
        })

    elif intent.intent == "FOLLOWUP_ANSWER":
        if not pending or not search:
            response["answer"] = (
                "There are no pending eligibility questions to answer. "
                "Please describe the schemes you are looking for."
            )
        else:
            continued_result = continue_discovery(
                original_message=search,
                answer_message=message,
                citizen_profile=profile,
                pending_questions=pending,
                top_k=top_k,
            )

            result = continued_result
            profile = continued_result.get("profile", profile)
            pending = continued_result.get("followup_questions", [])
            search = continued_result.get("retrieval_query", search)

            response.update({
                "answer": continued_result.get("message", ""),
                "profile": profile,
                "pending_questions": pending,
                "last_result": result,
                "active_search": search,
                "result": continued_result,
            })

    response["conversation_context"] = (
        context
        + [
            {"role": "user", "content": message},
            {
                "role": "assistant",
                "content": response["answer"],
                "intent": response["intent"],
            },
        ]
    )[-8:]

    return response
