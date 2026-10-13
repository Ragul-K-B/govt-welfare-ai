
from llm.answer_extractor import extract_followup_answers
from retrieval.search import search_schemes
from services.eligibility_service import evaluate_retrieved_schemes
from services.followup import generate_followup_questions
from services.relevance_service import validate_scheme_relevance


def continue_discovery(
    original_message: str,
    answer_message: str,
    citizen_profile: dict,
    pending_questions: list[dict],
    top_k: int = 5
) -> dict:
    # 1. Extract answers to the questions we actually asked.
    answers = extract_followup_answers(
        message=answer_message,
        pending_questions=pending_questions,
        citizen_profile=citizen_profile
    )

    # 2. Preserve the existing profile and merge new answers.
    updated_profile = citizen_profile.copy()
    updated_profile.update(answers)

    # 3. Build the retrieval query using the original request
    # and the updated profile.
    known_details = {
        key: value
        for key, value in updated_profile.items()
        if value is not None
    }

    profile_text = ", ".join(
        f"{key.replace('_', ' ')}: {value}"
        for key, value in known_details.items()
    )

    retrieval_query = (
        f"{original_message}\n"
        f"Citizen's latest answer: {answer_message}\n"
        f"Updated citizen details: {profile_text}"
    )

    # 4. Retrieve candidates again using FAISS.
    retrieved_schemes = search_schemes(
        query=retrieval_query,
        top_k=top_k
    )

    # 5. Fetch scheme details and evaluate eligibility.
    candidate_schemes = evaluate_retrieved_schemes(
        retrieved_schemes=retrieved_schemes,
        citizen_profile=updated_profile
    )

    # 6. Validate relevance against the original requested need.
    # The citizen's answer updates eligibility facts; it does not
    # automatically redefine the original need.
    relevance = validate_scheme_relevance(
        user_need=original_message,
        schemes=candidate_schemes
    )

    relevant_schemes = relevance["relevant_schemes"]
    uncertain_schemes = relevance["uncertain_schemes"]

    # 7. If no candidate is relevant or uncertain, report no match.
    if not relevant_schemes and not uncertain_schemes:
        return {
            "original_message": original_message,
            "latest_answer": answer_message,
            "extracted_answers": answers,
            "profile": updated_profile,
            "retrieval_query": retrieval_query,
            "schemes": [],
            "uncertain_schemes": [],
            "followup_questions": [],
            "no_match": True,
            "message": relevance["message"],
        }

    # 8. Re-evaluate only confidently relevant schemes.
    evaluated_schemes = evaluate_retrieved_schemes(
        retrieved_schemes=[
            {
                "scheme_id": scheme["scheme_id"],
                "score": scheme.get("score"),
            }
            for scheme in relevant_schemes
        ],
        citizen_profile=updated_profile
    )

    # 9. Generate questions only for relevant schemes that still
    # need additional information for eligibility evaluation.
    next_questions = generate_followup_questions(
        evaluated_schemes=evaluated_schemes,
        citizen_profile=updated_profile
    )

    # 10. Return the updated conversation state.
    return {
        "original_message": original_message,
        "latest_answer": answer_message,
        "extracted_answers": answers,
        "profile": updated_profile,
        "retrieval_query": retrieval_query,
        "schemes": evaluated_schemes,
        "uncertain_schemes": uncertain_schemes,
        "followup_questions": next_questions,
        "no_match": False,
        "message": relevance["message"],
    }
