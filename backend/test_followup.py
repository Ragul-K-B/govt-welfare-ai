
from services.discovery import discover_schemes
from services.followup import generate_followup_questions

message = (
    "I am 23 years old, studying engineering in Tamil Nadu. "
    "My family income is around 2 lakh per year. "
    "I need financial assistance for my education."
)

result = discover_schemes(message, top_k=5)

questions = generate_followup_questions(
    evaluated_schemes=result["schemes"],
    citizen_profile=result["profile"]
)

print("\n--- DYNAMIC FOLLOW-UP QUESTIONS ---")

for item in questions:
    print(f"\nAttribute: {item['attribute']}")
    print(f"Question: {item['question']}")
    print(f"Related schemes: {item['related_scheme_ids']}")