
from services.eligibility_service import evaluate_retrieved_schemes

citizen = {
    "community_category": "BC",
    "course_level": "Diploma",
    "institution_type": "Government Polytechnic",
    "annual_parental_income": 200000,
    "is_first_diploma_or_graduate_in_family": True
}

retrieved_schemes = [
    {
        "scheme_id": "TN-BC-FED-001",
        "score": 0.84
    }
]

results = evaluate_retrieved_schemes(
    retrieved_schemes,
    citizen
)

for result in results:
    print(result)
