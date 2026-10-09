import requests

API_URL = "http://127.0.0.1:8000"


def show_results(result):
    print("\n" + "=" * 65)
    print("                 WELFARE AI RESULTS")
    print("=" * 65)

    print("\nCitizen profile:")
    for key, value in result.get("profile", {}).items():
        if value is not None:
            print(f"  {key.replace('_', ' ').title()}: {value}")

    print("\nRelevant schemes:")

    for scheme in result.get("schemes", []):
        print(f"\n  {scheme['name']}")
        print(f"  Scheme ID: {scheme['scheme_id']}")
        print(f"  Eligibility: {scheme['decision']}")

        if scheme.get("score") is not None:
            print(f"  Relevance score: {scheme['score']:.3f}")

        missing = scheme.get("missing_attributes", [])
        if missing:
            print("  Information needed: " + ", ".join(missing))

    questions = result.get("followup_questions", [])

    if questions:
        print("\nWelfare AI needs more information:")
        for number, question in enumerate(questions, start=1):
            print(f"  {number}. {question['question']}")
    else:
        print("\nNo further questions were generated.")

    print("=" * 65)


def post_request(endpoint, payload):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=180
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"\nAPI request failed: {error}")
        if getattr(error, "response", None) is not None:
            print(error.response.text)
        return None


def main():
    print("\nWelcome to Welfare AI!")
    print("Ask about government welfare schemes in normal language.")
    print("Type 'exit' whenever you want to stop.\n")

    original_message = input("You: ").strip()

    if not original_message or original_message.lower() == "exit":
        print("Chat ended.")
        return

    result = post_request(
        "/api/discover",
        {
            "message": original_message,
            "top_k": 5
        }
    )

    if result is None:
        return

    show_results(result)

    profile = result["profile"]
    pending_questions = result.get("followup_questions", [])

    while pending_questions:
        answer = input("\nYou: ").strip()

        if answer.lower() == "exit":
            break

        if not answer:
            print("Please enter an answer.")
            continue

        updated_result = post_request(
            "/api/continue",
            {
                "original_message": original_message,
                "answer_message": answer,
                "citizen_profile": profile,
                "pending_questions": pending_questions,
                "top_k": 5
            }
        )

        if updated_result is None:
            print("The conversation state has been preserved.")
            continue

        profile = updated_result["profile"]
        pending_questions = updated_result.get(
            "followup_questions", []
        )

        show_results(updated_result)

    print("\nThank you for using Welfare AI!")


if __name__ == "__main__":
    main()
