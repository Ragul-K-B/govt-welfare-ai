import json
import re

from db.mongodb import schemes_collection
from llm.intent_classifier import classify_intent, IntentResult
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
        if str(scheme.get("decision", "")).upper() in ("PASS", "UNKNOWN")
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


def find_requested_scheme(message: str) -> dict | None:
    """Resolve a scheme ID or an unambiguous scheme-name mention."""
    normalized_message = re.sub(
        r"[^a-z0-9]+",
        " ",
        message.casefold(),
    ).strip()

    # First: look for an explicit scheme ID in the user's message.
    id_match = re.search(
        r"\b[A-Z]{2,}(?:-[A-Z0-9]+)+\b",
        message.upper(),
    )

    if id_match:
        scheme = schemes_collection.find_one(
            {"scheme_id": id_match.group()},
            {"_id": 0},
        )
        if scheme:
            return scheme

    # This is a conservative direct-name fallback. The LLM name resolver
    # below handles names extracted from longer natural-language questions.
    ignored_words = {
        "what", "is", "the", "scheme", "schemes", "explain",
        "tell", "me", "about", "please", "give", "details",
        "detail", "of", "for", "we", "have", "this", "that",
        "information", "on", "can", "you", "describe",
    }

    requested_words = [
        word
        for word in normalized_message.split()
        if word not in ignored_words
    ]

    if not requested_words:
        return None

    matches = []

    for scheme in schemes_collection.find({}, {"_id": 0}):
        normalized_name = re.sub(
            r"[^a-z0-9]+",
            " ",
            str(scheme.get("name", "")).casefold(),
        ).strip()
        name_words = set(normalized_name.split())

        if all(word in name_words for word in requested_words):
            matches.append(scheme)

    return matches[0] if len(matches) == 1 else None


def find_scheme_by_llm_name(
    requested_scheme_name: str | None,
) -> dict | None:
    """
    Resolve the LLM-extracted scheme name against MongoDB.

    The LLM identifies the name; MongoDB remains the source of truth.
    A partial name is accepted only when its meaningful words all occur
    in exactly one stored scheme name.
    """
    if not requested_scheme_name:
        return None

    requested = re.sub(
        r"[^a-z0-9]+",
        " ",
        requested_scheme_name.casefold(),
    ).strip()

    if not requested:
        return None

    requested_words = set(requested.split())
    matches = []

    for scheme in schemes_collection.find({}, {"_id": 0}):
        stored_name = re.sub(
            r"[^a-z0-9]+",
            " ",
            str(scheme.get("name", "")).casefold(),
        ).strip()

        if not stored_name:
            continue

        stored_words = set(stored_name.split())

        # Prefer exact normalized matches. Otherwise allow the LLM to
        # return a short form such as "Uzhavar Santhai" only if it maps
        # unambiguously to one stored scheme name.
        if stored_name == requested or (
            requested_words and requested_words.issubset(stored_words)
        ):
            matches.append(scheme)

    # If a broad/short name maps to multiple schemes, do not guess.
    unique = {scheme.get("scheme_id"): scheme for scheme in matches}
    return next(iter(unique.values())) if len(unique) == 1 else None


def resolve_requested_scheme(
    message: str,
    intent: IntentResult,
    last_result: dict | None,
) -> dict | None:
    """Resolve the scheme using user ID/name, LLM extraction, then context."""
    # Explicit IDs and the existing deterministic direct-name behavior first.
    scheme = find_requested_scheme(message)
    if scheme is not None:
        return scheme

    # Validate any ID selected by the LLM against MongoDB before using it.
    if intent.scheme_id:
        scheme = schemes_collection.find_one(
            {"scheme_id": intent.scheme_id.strip()},
            {"_id": 0},
        )
        if scheme:
            return scheme

    # Resolve the scheme name extracted by the LLM against stored records.
    scheme = find_scheme_by_llm_name(intent.requested_scheme_name)
    if scheme is not None:
        return scheme

    # Finally, support references that exactly match a displayed scheme.
    return find_scheme_by_name(message, last_result)


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

    # Resolve the user's requested scheme using the LLM's extracted name
    # as well as explicit IDs and the existing conversation context.
    requested_scheme = resolve_requested_scheme(message, intent, result)

    # If a known scheme is explicitly identified, protect the details route
    # from an incorrect NEW_DISCOVERY classification.
    if requested_scheme is not None and intent.intent != "SCHEME_DETAILS":
        intent = IntentResult(
            intent="SCHEME_DETAILS",
            scheme_id=requested_scheme.get("scheme_id"),
            requested_scheme_name=requested_scheme.get("name"),
            detail_type=(
                intent.detail_type
                if intent.detail_type != "NONE"
                else "ALL"
            ),
            search_query=None,
            confidence=1.0,
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
        # Rerun the normal discovery pipeline for every named-scheme details
        # request, so retrieval and eligibility evaluation run with the
        # citizen's current profile.
        scheme = requested_scheme or resolve_requested_scheme(
            message,
            intent,
            result,
        )

        if scheme is not None:
            scheme_name = str(scheme.get("name", "")).strip()
            scheme_id = str(scheme.get("scheme_id", "")).strip()
            scheme_query = f"{scheme_name} {scheme_id}".strip()

            refreshed_result = discover_schemes(
                message=scheme_query,
                top_k=top_k,
                existing_profile=profile,
            )

            result = refreshed_result
            profile = refreshed_result.get("profile", profile)
            pending = refreshed_result.get("followup_questions", [])
            search = refreshed_result.get("retrieval_query", scheme_query)

            # Include FAIL candidates too; scheme details remain viewable even
            # when the citizen does not satisfy the eligibility requirements.
            evaluated_scheme = next(
                (
                    candidate
                    for candidate in refreshed_result.get("schemes", [])
                    if str(candidate.get("scheme_id", "")).strip().casefold()
                    == scheme_id.casefold()
                ),
                None,
            )

            if evaluated_scheme is not None:
                # MongoDB provides canonical facts; discovery provides the
                # newly evaluated eligibility decision.
                scheme = {**scheme, **evaluated_scheme}
                details_answer = (
                    f"Here are the requested details for {scheme_name}. "
                    "I've rerun retrieval and eligibility evaluation using "
                    "your current profile."
                )
            else:
                # Do not invent an eligibility decision if retrieval did not
                # evaluate this exact scheme.
                details_answer = (
                    f"I found {scheme_name} in the scheme database and can show "
                    "its stored details, but refreshed retrieval did not return "
                    "this exact scheme for eligibility evaluation. I won't "
                    "label it eligible or ineligible without that check."
                )

            response.update({
                "answer": details_answer,
                "profile": profile,
                "pending_questions": pending,
                "last_result": result,
                "active_search": search,
                "result": refreshed_result,
                "scheme_details": {
                    "scheme": scheme,
                    "detail_type": (
                        "ALL"
                        if intent.detail_type == "NONE"
                        else intent.detail_type
                    ),
                },
            })
        else:
            response["answer"] = (
                "I couldn't confidently identify the exact scheme you mean. "
                "Please provide its scheme ID or full scheme name, "
                "and I'll try again."
            )

    elif intent.intent == "NEW_DISCOVERY":
        # A NEW_DISCOVERY request starts a fresh search.
        # Keep the citizen profile and conversation history, but clear
        # the previous search state before running the new discovery.
        search_query = (intent.search_query or message).strip()

        pending = []
        result = None
        search = None

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

    response["intent"] = intent.intent
    response["conversation_context"] = (
        context
        + [
            {"role": "user", "content": message},
            {
                "role": "assistant",
                "content": response["answer"],
                "intent": intent.intent,
            },
        ]
    )[-8:]

    return response
