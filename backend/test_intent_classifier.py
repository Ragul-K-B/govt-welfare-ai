
from llm.intent_classifier import classify_intent


displayed_schemes = [
    {
        "scheme_id": "TN-BC-FED-001",
        "name": "Free Education Scholarship for Diploma Students",
        "decision": "PASS",
    },
    {
        "scheme_id": "TN-BC-PMS-001",
        "name": "Post-Matric Scholarship for BC/MBC/DNC College Students",
        "decision": "PASS",
    },
]

tests = [
    "What financial support does this scheme provide?",
    "Find housing assistance schemes in Tamil Nadu.",
    "Tell me everything about the second scheme.",
    "I meant the one for diploma students.",
]

for message in tests:
    print("\n" + "=" * 60)
    print("Message:", message)

    try:
        result = classify_intent(
            message=message,
            citizen_profile={"community_category": "BC"},
            pending_questions=[],
            active_search="Find scholarship schemes in Tamil Nadu.",
            displayed_schemes=displayed_schemes,
        )

        print(result.model_dump())

    except Exception as error:
        print("TEST ERROR:", type(error).__name__, str(error))
