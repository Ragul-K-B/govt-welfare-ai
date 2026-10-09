
from llm.answer_extractor import extract_followup_answers
from retrieval.search import search_schemes
from services.eligibility_service import evaluate_retrieved_schemes
from services.followup import generate_followup_questions


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

    # 3. Build a retrieval query using the original request
    #    and the updated profile.
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

    # 4. Retrieve relevant schemes again.
    retrieved_schemes = search_schemes(
        query=retrieval_query,
        top_k=top_k
    )

    # 5. Re-evaluate eligibility using the deterministic engine.
    evaluated_schemes = evaluate_retrieved_schemes(
        retrieved_schemes=retrieved_schemes,
        citizen_profile=updated_profile
    )

    # 6. Generate questions only for remaining UNKNOWN schemes.
    next_questions = generate_followup_questions(
        evaluated_schemes=evaluated_schemes,
        citizen_profile=updated_profile
    )

    # 7. Return the updated conversation state.
    return {
        "original_message": original_message,
        "latest_answer": answer_message,
        "extracted_answers": answers,
        "profile": updated_profile,
        "schemes": evaluated_schemes,
        "followup_questions": next_questions
    }
