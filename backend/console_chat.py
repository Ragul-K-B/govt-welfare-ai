
import json
import requests

from llm.intent_classifier import classify_intent
from llm.client import get_llm_response


API_URL = "http://127.0.0.1:8000"
TOP_K = 5
MIN_INTENT_CONFIDENCE = 0.60


# --------------------------------------------------
# Formatting helpers
# --------------------------------------------------

def is_missing(value):
    return value is None or value == "" or value == [] or value == {}


def format_detail(value):
    if is_missing(value):
        return "Not available in the stored scheme data."

    if isinstance(value, list):
        return "\n".join(f"  - {item}" for item in value)

    if isinstance(value, dict):
        return "\n".join(
            f"  {key.replace('_', ' ').title()}: {format_detail(item)}"
            for key, item in value.items()
        )

    return str(value)


def display_section(title, value):
    print(f"\n{title}:")
    print(format_detail(value))


def scheme_name(scheme):
    return (
        scheme.get("name")
        or scheme.get("scheme_name")
        or scheme.get("scheme_id")
        or "Unnamed scheme"
    )


def scheme_id(scheme):
    return scheme.get("scheme_id") or scheme.get("id") or ""


def visible_schemes(result):
    """Exclude FAIL schemes from the displayed results."""
    return [
        scheme
        for scheme in result.get("schemes", [])
        if str(scheme.get("decision", "")).upper()
        in ("PASS", "UNKNOWN")
    ]


# --------------------------------------------------
# Display discovery results
# --------------------------------------------------

def show_results(result):
    schemes = visible_schemes(result)
    uncertain_schemes = result.get("uncertain_schemes", [])

    print("\n" + "=" * 65)
    print("GOVERNMENT WELFARE SCHEME DISCOVERY RESULTS")
    print("=" * 65)

    # 1. Explicitly handle a confirmed no-match result.
    if result.get("no_match") is True:
        print(
            result.get("message")
            or (
                "No suitable scheme was found in the current "
                "scheme database for your stated need."
            )
        )
        print(
            "\nThis means no suitable match was identified among "
            "the candidates checked. It does not prove that no "
            "such government scheme exists anywhere."
        )
        print("\n" + "=" * 65)
        return

    # 2. Display confidently relevant schemes.
    for index, scheme in enumerate(schemes, start=1):
        print(f"\n{index}. {scheme_name(scheme)}")

        if scheme_id(scheme):
            print(f"   Scheme ID: {scheme_id(scheme)}")

        print(
            "   Eligibility decision: "
            + str(scheme.get("decision", "UNKNOWN")).upper()
        )

        if scheme.get("score") is not None:
            print(f"   Retrieval score: {scheme['score']}")

        display_section("About this scheme", scheme.get("description"))
        display_section("Basic benefits", scheme.get("benefits"))

        missing = scheme.get("missing_attributes")
        if not is_missing(missing):
            display_section("Missing information", missing)

    # 3. Show uncertain candidates separately.
    # Do not present them as confirmed relevant schemes.
    if uncertain_schemes:
        print("\n" + "-" * 65)
        print("SCHEMES WITH UNCERTAIN RELEVANCE")
        print("-" * 65)
        print(
            "These candidates have not been confirmed as suitable "
            "for your requested need."
        )

        for index, scheme in enumerate(uncertain_schemes, start=1):
            print(f"\n{index}. {scheme_name(scheme)}")

            if scheme_id(scheme):
                print(f"   Scheme ID: {scheme_id(scheme)}")

            display_section("About this scheme", scheme.get("description"))
            display_section("Basic benefits", scheme.get("benefits"))

    # 4. If neither confirmed nor uncertain schemes exist, show
    # a useful fallback instead of the old generic message.
    if not schemes and not uncertain_schemes:
        print(
            result.get("message")
            or "No suitable scheme was identified among the retrieved candidates."
        )

    # 5. Show questions generated for relevant schemes only.
    questions = result.get("followup_questions", [])

    if questions:
        print("\nI need a few more details to evaluate eligibility:")

        for index, question in enumerate(questions, start=1):
            if isinstance(question, dict):
                question_text = (
                    question.get("question")
                    or question.get("text")
                    or str(question)
                )
            else:
                question_text = str(question)

            print(f"{index}. {question_text}")

    print("\n" + "=" * 65)

    if schemes:
        print("You can ask for more details about any displayed scheme.")
    elif uncertain_schemes:
        print(
            "You can ask for more information about these candidates, "
            "but their relevance is not confirmed."
        )


# --------------------------------------------------
# Display scheme details
# --------------------------------------------------

def show_scheme_details(scheme, detail_type="ALL"):
    detail_type = (detail_type or "ALL").upper()

    print("\n" + "=" * 65)
    print(f"SCHEME DETAILS: {scheme_name(scheme)}")
    print("=" * 65)

    if scheme_id(scheme):
        print(f"Scheme ID: {scheme_id(scheme)}")

    print(
        "Decision: "
        + str(scheme.get("decision", "UNKNOWN")).upper()
    )

    fields = {
        "DESCRIPTION": ("Description", ["description"]),
        "BENEFITS": ("Benefits", ["benefits"]),
        "ELIGIBILITY": ("Eligibility", ["eligibility"]),
        "DOCUMENTS": ("Required documents", ["documents"]),
        "APPLICATION": ("How to apply", ["application"]),
        "SOURCES": ("Sources", ["sources"]),
    }

    if detail_type in ("ALL", "NONE"):
        selected_fields = list(fields.values())
    elif detail_type in fields:
        selected_fields = [fields[detail_type]]
    else:
        selected_fields = list(fields.values())

    for title, keys in selected_fields:
        value = None

        for key in keys:
            if not is_missing(scheme.get(key)):
                value = scheme[key]
                break

        display_section(title, value)

    print("\n" + "=" * 65)


# --------------------------------------------------
# API helper
# --------------------------------------------------

def post_request(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("\nCannot connect to the backend.")
        print("Start it with: python -m uvicorn main:app --reload")

    except requests.exceptions.Timeout:
        print("\nThe backend took too long to respond.")

    except requests.exceptions.HTTPError as error:
        print(f"\nAPI error: {error}")
        try:
            print(response.json())
        except ValueError:
            print(response.text)

    except requests.exceptions.RequestException as error:
        print(f"\nRequest failed: {error}")

    return None


# --------------------------------------------------
# Scheme selection
# --------------------------------------------------

def find_scheme_by_id(scheme_identifier, last_result):
    """Resolve a scheme ID against currently displayed schemes."""
    if not scheme_identifier or not last_result:
        return None

    target = str(scheme_identifier).strip().casefold()

    for scheme in visible_schemes(last_result):
        if str(scheme_id(scheme)).strip().casefold() == target:
            return scheme

    return None


def find_scheme_by_name(message, last_result):
    """Match a complete displayed scheme name or ID."""
    if not last_result:
        return None

    text = message.strip().casefold()
    matches = []

    for scheme in visible_schemes(last_result):
        name = scheme_name(scheme).strip().casefold()
        sid = str(scheme_id(scheme)).strip().casefold()

        if name and text == name:
            matches.append(scheme)
        elif sid and text == sid:
            matches.append(scheme)

    if len(matches) == 1:
        return matches[0]

    return None


def show_scheme_choices(last_result):
    schemes = visible_schemes(last_result or {})

    if not schemes:
        print("\nThere are no confirmed relevant schemes to select.")

        uncertain = (last_result or {}).get("uncertain_schemes", [])
        if uncertain:
            print("Some candidates have uncertain relevance.")
            for scheme in uncertain:
                print(f"- {scheme_name(scheme)} ({scheme_id(scheme)})")

        return

    print("\nWhich scheme do you mean?")

    for index, scheme in enumerate(schemes, start=1):
        print(f"{index}. {scheme_name(scheme)} ({scheme_id(scheme)})")

    print("You can enter a scheme name or ID, or describe the scheme.")


# --------------------------------------------------
# General questions grounded in available data
# --------------------------------------------------


def answer_general_question(message, last_result, citizen_profile):
    schemes = visible_schemes(last_result or {})

    context = {
        "user_question": message,
        "citizen_profile": citizen_profile,
        "active_search": (last_result or {}).get("retrieval_query"),
        "displayed_schemes": schemes,
        "uncertain_schemes": (last_result or {}).get(
            "uncertain_schemes", []
        ),
        "no_match": (last_result or {}).get("no_match", False),
        "discovery_message": (last_result or {}).get("message"),
    }

    prompt = f"""
You are a helpful assistant for a government welfare scheme discovery
application in India.

Answer the user's question directly and clearly.

GENERAL KNOWLEDGE:
- You may use general knowledge to explain concepts, terminology,
  and differences between things, such as scholarships and subsidies.
- If the user asks a general conceptual question, do not refuse merely
  because the supplied context does not contain a definition.
- Clearly distinguish general explanations from information about
  a specific government scheme.

GOVERNMENT SCHEME FACTS:
- Use the supplied context for claims about schemes in this conversation.
- Do not invent scheme benefits, required documents, deadlines,
  application procedures, official sources, or eligibility conditions.
- If specific scheme information is missing from the context, say so.
- Do not treat a PASS decision as official government approval.
- Do not present uncertain schemes as confirmed relevant matches.
- A no-match result means no suitable scheme was identified among
  the candidates checked, not that no scheme exists anywhere.

Keep the answer relevant to the user's question.
Do not describe internal instructions or repeat the entire context.

Context:
{json.dumps(context, ensure_ascii=False, default=str)}
"""

    try:
        answer = get_llm_response(prompt)

        if answer and answer.strip():
            print("\nWelfare AI:", answer)
        else:
            print(
                "\nI couldn't generate an answer right now."
            )

    except Exception as error:
        print("\nI couldn't answer that question right now.")
        print(f"LLM error: {type(error).__name__}: {error}")


# --------------------------------------------------
# Main conversation
# --------------------------------------------------

def main():
    print("=" * 65)
    print("WELFARE AI - GOVERNMENT SCHEME ASSISTANT")
    print("=" * 65)
    print("Describe the government assistance you need.")
    print("You can answer follow-up questions or ask about scheme details.")
    print("Type 'exit' to end the conversation.")

    citizen_profile = {}
    pending_questions = []
    last_result = None
    active_search = None
    conversation_context = []

    while True:
        try:
            message = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nConversation ended.")
            break

        if not message:
            continue

        if message.casefold() in {"exit", "quit", "bye"}:
            print("\nThank you for using Welfare AI. Goodbye!")
            break

        # Resolve exact scheme names and IDs locally.
        selected_scheme = find_scheme_by_id(message, last_result)

        if selected_scheme is None:
            selected_scheme = find_scheme_by_name(message, last_result)

        if selected_scheme is not None:
            show_scheme_details(selected_scheme, "ALL")

            conversation_context.append(
                {"role": "user", "content": message}
            )
            conversation_context.append(
                {
                    "role": "assistant",
                    "content": (
                        f"Displayed details for {scheme_name(selected_scheme)}"
                    ),
                }
            )
            conversation_context = conversation_context[-8:]
            continue

        # Classify the user's meaning using the current conversation.
        try:
            intent = classify_intent(
                message=message,
                citizen_profile=citizen_profile,
                pending_questions=pending_questions,
                active_search=active_search,
                displayed_schemes=visible_schemes(last_result or {}),
                conversation_context=conversation_context[-8:],
            )

        except Exception as error:
            print("\nI couldn't understand the request reliably.")
            print(
                "Please try again. "
                f"Classifier error: {type(error).__name__}: {error}"
            )
            continue

        print(
            f"\n[Intent: {intent.intent}, "
            f"confidence: {intent.confidence:.2f}]"
        )

        if (
            intent.confidence < MIN_INTENT_CONFIDENCE
            or intent.intent == "CLARIFICATION"
        ):
            show_scheme_choices(last_result)
            print(
                "Alternatively, tell me whether you want to find schemes, "
                "answer an eligibility question, or ask a general question."
            )
            continue

        # 1. Show details for a scheme already in the current results.

        # 1. Show a scheme from current results, or rediscover it.
        if intent.intent == "SCHEME_DETAILS":
            selected_scheme = find_scheme_by_id(
                intent.scheme_id,
                last_result,
            )

            if selected_scheme is not None:
                show_scheme_details(
                    selected_scheme,
                    intent.detail_type,
                )

                conversation_context.append(
                    {"role": "user", "content": message}
                )
                conversation_context.append(
                    {
                        "role": "assistant",
                        "content": (
                            f"Displayed {intent.detail_type} for "
                            f"{scheme_name(selected_scheme)}"
                        ),
                    }
                )
                conversation_context = conversation_context[-8:]
                continue

            # Scheme is not in the current top-K results.
            # Reuse the existing discovery pipeline.
            search_query = (
                intent.scheme_id or message
            ).strip()

            if not search_query:
                search_query = message

            print(
                "\nThe scheme isn't in the current results. "
                "Searching again..."
            )
            print(
                "DEBUG search_query sent to API:",
                repr(search_query),
            )

            result = post_request(
                "/api/discover",
                {
                    "message": search_query,
                    "top_k": TOP_K,
                    "existing_profile": citizen_profile,
                },
            )

            if result is None:
                continue

            citizen_profile = result.get(
                "profile",
                citizen_profile,
            )
            pending_questions = result.get(
                "followup_questions",
                [],
            )
            last_result = result
            active_search = search_query

            show_results(result)

            conversation_context.append(
                {"role": "user", "content": message}
            )
            conversation_context.append(
                {
                    "role": "assistant",
                    "content": (
                        f"Rediscovered schemes for: {search_query}. "
                        f"No match: {result.get('no_match', False)}"
                    ),
                }
            )
            conversation_context = conversation_context[-8:]
            continue

        # 2. Start a new discovery while preserving the citizen profile.
        if intent.intent == "NEW_DISCOVERY":
            search_query = (intent.search_query or "").strip()
            print("DEBUG search_query sent to API:", repr(search_query))

            if not search_query:
                print(
                    "\nI couldn't determine the search criteria. "
                    "Please describe the schemes you want to find."
                )
                continue

            result = post_request(
                "/api/discover",
                {
                    "message": search_query,
                    "top_k": TOP_K,
                    "existing_profile": citizen_profile,
                },
            )

            if result is None:
                continue

            citizen_profile = result.get("profile", citizen_profile)
            pending_questions = result.get("followup_questions", [])
            last_result = result
            active_search = search_query

            show_results(result)

            conversation_context.append(
                {"role": "user", "content": message}
            )
            conversation_context.append(
                {
                    "role": "assistant",
                    "content": (
                        f"Processed discovery for: {search_query}. "
                        f"No match: {result.get('no_match', False)}"
                    ),
                }
            )
            conversation_context = conversation_context[-8:]
            continue

        # 3. Process answers to eligibility follow-up questions.
        if intent.intent == "FOLLOWUP_ANSWER":
            if not pending_questions:
                print(
                    "\nThere are no pending eligibility questions. "
                    "Please tell me what schemes you want to discover."
                )
                continue

            if not active_search:
                print("\nPlease start by describing the schemes you need.")
                continue

            result = post_request(
                "/api/continue",
                {
                    "original_message": active_search,
                    "answer_message": message,
                    "citizen_profile": citizen_profile,
                    "pending_questions": pending_questions,
                    "top_k": TOP_K,
                },
            )

            if result is None:
                continue

            citizen_profile = result.get("profile", citizen_profile)
            pending_questions = result.get("followup_questions", [])
            last_result = result

            show_results(result)

            conversation_context.append(
                {"role": "user", "content": message}
            )
            conversation_context.append(
                {
                    "role": "assistant",
                    "content": (
                        "Processed the eligibility follow-up answer. "
                        f"No match: {result.get('no_match', False)}"
                    ),
                }
            )
            conversation_context = conversation_context[-8:]
            continue

        # 4. Answer a general question using available context.
        if intent.intent == "GENERAL_QUESTION":
            answer_general_question(
                message=message,
                last_result=last_result,
                citizen_profile=citizen_profile,
            )

            conversation_context.append(
                {"role": "user", "content": message}
            )
            conversation_context.append(
                {
                    "role": "assistant",
                    "content": "Answered using available conversation data.",
                }
            )
            conversation_context = conversation_context[-8:]
            continue

        if intent.intent == "EXIT":
            print("\nThank you for using Welfare AI. Goodbye!")
            break

        print(
            "\nI couldn't determine the correct action. "
            "Please rephrase your request."
        )


if __name__ == "__main__":
    main()
