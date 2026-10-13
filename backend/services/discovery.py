
from llm.profile_extractor import extract_citizen_profile
from retrieval.search import search_schemes
from services.eligibility_service import evaluate_retrieved_schemes
from services.relevance_service import validate_scheme_relevance
from services.followup import generate_followup_questions


def discover_schemes(
    message: str,
    top_k: int = 5,
    existing_profile: dict | None = None
) -> dict:
    # 1. Extract facts explicitly provided in the new message.
    extracted_profile = extract_citizen_profile(message)
    new_facts = extracted_profile.model_dump(exclude_none=True)

    # 2. Preserve existing facts and merge newly extracted information.
    citizen = (existing_profile or {}).copy()
    citizen.update(new_facts)

    # Keep all known profile attributes, including None values
    # for attributes not previously collected.
    for key, value in extracted_profile.model_dump().items():
        citizen.setdefault(key, value)

    # 3. Retrieve schemes using the user's actual requested need.
    # Citizen profile details are used for eligibility evaluation,
    # not to redefine the user's requested need.
    retrieval_query = message

    retrieved_schemes = search_schemes(
        query=retrieval_query,
        top_k=top_k
    )

    # 4. Fetch scheme details and evaluate deterministic eligibility.
    candidate_schemes = evaluate_retrieved_schemes(
        retrieved_schemes=retrieved_schemes,
        citizen_profile=citizen
    )

    # 5. Validate whether retrieved schemes address the user's need.
    relevance = validate_scheme_relevance(
        user_need=message,
        schemes=candidate_schemes
    )

    relevant_schemes = relevance["relevant_schemes"]
    uncertain_schemes = relevance["uncertain_schemes"]

    # 6. If every candidate is irrelevant, report no match.
    # Do not generate eligibility questions for irrelevant schemes.
    if not relevant_schemes and not uncertain_schemes:
        return {
            "profile": citizen,
            "retrieval_query": retrieval_query,
            "schemes": [],
            "uncertain_schemes": [],
            "followup_questions": [],
            "no_match": True,
            "message": relevance["message"],
        }

    # 7. Re-evaluate only confidently relevant schemes.
    # This preserves their original FAISS scores and uses the
    # deterministic eligibility engine for the current profile.
    evaluated_schemes = evaluate_retrieved_schemes(
        retrieved_schemes=[
            {
                "scheme_id": scheme["scheme_id"],
                "score": scheme.get("score"),
            }
            for scheme in relevant_schemes
        ],
        citizen_profile=citizen
    )

    # 8. Generate dynamic eligibility questions only for relevant
    # schemes whose eligibility decisions still need information.
    followup_questions = generate_followup_questions(
        evaluated_schemes=evaluated_schemes,
        citizen_profile=citizen
    )

    # 9. Return the discovery results and conversation state.
    return {
        "profile": citizen,
        "retrieval_query": retrieval_query,
        "schemes": evaluated_schemes,
        "uncertain_schemes": uncertain_schemes,
        "followup_questions": followup_questions,
        "no_match": False,
        "message": relevance["message"],
    }
