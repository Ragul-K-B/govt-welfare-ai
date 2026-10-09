
from services.discovery import discover_schemes

message = (
    "I am 23 years old, studying engineering in Tamil Nadu. "
    "My family income is around 2 lakh per year. "
    "I need financial assistance for my education."
)

result = discover_schemes(message, top_k=5)

print("\n--- CITIZEN PROFILE ---")
print(result["profile"])

print("\n--- RETRIEVAL QUERY ---")
print(result["retrieval_query"])

print("\n--- SCHEME ELIGIBILITY RESULTS ---")

for scheme in result["schemes"]:
    print(f"\nScheme: {scheme['name']}")
    print(f"Scheme ID: {scheme['scheme_id']}")
    print(f"Similarity score: {scheme['score']}")
    print(f"Eligibility: {scheme['decision']}")
    print(f"Missing attributes: {scheme['missing_attributes']}")
