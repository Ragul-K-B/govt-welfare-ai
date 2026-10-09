
from services.discovery import discover_schemes


message = (
    "I'm 23, studying engineering in Tamil Nadu, "
    "and my family income is around 2 lakh per year. "
    "I want financial assistance for my education."
)

result = discover_schemes(message, top_k=5)

print("\n--- EXTRACTED PROFILE ---")
print(result["profile"])

print("\n--- RETRIEVAL QUERY ---")
print(result["retrieval_query"])

print("\n--- RETRIEVED SCHEMES ---")
for scheme in result["schemes"]:
    print(scheme)
