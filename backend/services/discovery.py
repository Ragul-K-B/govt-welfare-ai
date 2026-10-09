
from llm.profile_extractor import extract_citizen_profile
from retrieval.search import search_schemes
from services.eligibility_service import evaluate_retrieved_schemes


def discover_schemes(message: str, top_k: int = 5) -> dict:
    # 1. Extract facts explicitly provided by the citizen.
    profile = extract_citizen_profile(message)

    citizen = profile.model_dump()

    # 2. Build a retrieval query using the original message
    #    and the extracted citizen details.
    known_details = profile.model_dump(exclude_none=True)

    profile_text = ", ".join(
        f"{key.replace('_', ' ')}: {value}"
        for key, value in known_details.items()
    )

    retrieval_query = (
        f"{message}\n"
        f"Extracted citizen details: {profile_text}"
    )

    # 3. Retrieve relevant schemes using FAISS.
    retrieved_schemes = search_schemes(
        query=retrieval_query,
        top_k=top_k
    )

    # 4. Evaluate retrieved schemes using MongoDB rules
    #    and the deterministic eligibility engine.
    evaluated_schemes = evaluate_retrieved_schemes(
        retrieved_schemes=retrieved_schemes,
        citizen_profile=citizen
    )

    # 5. Return the profile, retrieval information,
    #    and eligibility decisions.
    return {
        "profile": citizen,
        "retrieval_query": retrieval_query,
        "schemes": evaluated_schemes
    }
