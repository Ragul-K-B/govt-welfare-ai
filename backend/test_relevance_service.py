
from services.relevance_service import validate_scheme_relevance


schemes = [
    {
        "scheme_id": "TN-UWWB-MAR-001",
        "name": "Marriage Assistance for Registered Unorganised Workers",
        "description": (
            "Marriage assistance for eligible registered "
            "welfare-board members or their children."
        ),
        "benefits": {
            "type": "marriage_assistance",
            "details": "Financial assistance for marriage."
        },
    },
    {
        "scheme_id": "TN-PP-001",
        "name": "Pudhumai Penn",
        "description": (
            "Monthly financial support for eligible girl students "
            "pursuing higher education."
        ),
        "benefits": {
            "amount": 1000,
            "currency": "INR",
            "frequency": "monthly",
        },
    },
    {
        "scheme_id": "TN-DA-UA-001",
        "name": "Unemployment Allowance for Differently Abled Persons",
        "description": (
            "Monthly unemployment allowance for differently abled "
            "persons registered with the Employment Exchange."
        ),
        "benefits": {
            "amount": {
                "SSLC_and_below": 600,
                "higher_secondary": 750,
                "degree_and_above": 1000,
            },
            "currency": "INR",
            "frequency": "monthly",
        },
    },
]


user_need = (
    "Find startup funding or a self-employment loan for "
    "unemployed youth who want to start a small business "
    "in Tamil Nadu. I do not want scholarships or marriage assistance."
)


result = validate_scheme_relevance(
    user_need=user_need,
    schemes=schemes,
)

print("\nRelevance validation result")
print("=" * 50)
print("No match:", result["no_match"])
print("Message:", result["message"])

print("\nRelevant schemes:")
for scheme in result["relevant_schemes"]:
    print("-", scheme["scheme_id"], scheme["name"])

print("\nUncertain schemes:")
for scheme in result["uncertain_schemes"]:
    print("-", scheme["scheme_id"], scheme["name"])
