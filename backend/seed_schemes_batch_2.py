from schemas.scheme import Scheme, Rule, ConditionGroup, Logic, Operator
from db.mongodb import db


# ==================================================
# 1. Unemployment Allowance for Differently Abled
# ==================================================

unemployment_allowance = Scheme(
    scheme_id="TN-DA-UA-001",
    name="Unemployment Allowance for Differently Abled Persons",
    description=(
        "Tamil Nadu Government unemployment allowance scheme "
        "for differently abled persons registered with the "
        "Employment Exchange."
    ),
    benefits={
        "type": "financial_assistance",
        "amount": {
            "SSLC_and_below": 600,
            "higher_secondary": 750,
            "degree_and_above": 1000
        },
        "currency": "INR",
        "frequency": "monthly"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="is_differently_abled",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="employment_exchange_live_months",
                operator=Operator.GREATER_THAN,
                value=12
            )
        ]
    ),
    documents=[
        "Employment Registration Card",
        "National Identity Card for Differently Abled"
    ],
    application={
        "mode": "offline",
        "authority": "Employment Exchange"
    },
    sources=[
        "Tamil Nadu Commissionerate for Welfare of Differently Abled Persons"
    ]
)


# ==================================================
# 2. Maintenance Allowance for Intellectually
#    Disabled Persons
# ==================================================

intellectual_disability_maintenance = Scheme(
    scheme_id="TN-DA-MA-001",
    name="Maintenance Allowance to Intellectually Disabled Persons",
    description=(
        "Tamil Nadu Government maintenance allowance for "
        "intellectually disabled persons with 40 percent "
        "or above disability."
    ),
    benefits={
        "type": "financial_assistance",
        "amount": 1500,
        "currency": "INR",
        "frequency": "monthly",
        "payment_method": "ECS"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="is_intellectually_disabled",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="disability_percentage",
                operator=Operator.GREATER_THAN_OR_EQUAL,
                value=40
            )
        ]
    ),
    documents=[
        "National Identity Card for Differently Abled",
        "Family Card",
        "Bank account details"
    ],
    application={
        "mode": "offline",
        "authority": "District Differently Abled Welfare Officer"
    },
    sources=[
        "Tamil Nadu Commissionerate for Welfare of Differently Abled Persons"
    ]
)


# ==================================================
# 3. Personal Assistance Allowance for Persons
#    with High Support Needs
# ==================================================

personal_assistance = Scheme(
    scheme_id="TN-DA-PA-001",
    name="Personal Assistance Allowance to Person with High Support Need",
    description=(
        "Tamil Nadu Government personal assistance allowance "
        "for differently abled persons who require assistance "
        "for activities of daily living."
    ),
    benefits={
        "type": "financial_assistance",
        "amount": 1000,
        "currency": "INR",
        "frequency": "monthly",
        "payment_method": "ECS"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="is_differently_abled",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="has_high_support_needs",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "Recommendation Certificate from High Support Need Assessment Board"
    ],
    application={
        "mode": "offline",
        "authority": "District Differently Abled Welfare Officer"
    },
    sources=[
        "Tamil Nadu Commissionerate for Welfare of Differently Abled Persons"
    ]
)


# ==================================================
# 4. Readers Allowance for Visually Impaired Students
# ==================================================

readers_allowance = Scheme(
    scheme_id="TN-DA-RA-001",
    name="Readers Allowance for Visually Impaired Students",
    description=(
        "Tamil Nadu Government readers allowance for visually "
        "impaired students studying in Class IX and above "
        "in a bona fide educational institution."
    ),
    benefits={
        "type": "financial_assistance",
        "amount": {
            "class_9_to_12": 3000,
            "degree": 5000,
            "postgraduate_and_professional": 6000
        },
        "currency": "INR",
        "frequency": "annual"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="is_visually_impaired",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="education_level",
                operator=Operator.IN,
                value=[
                    "Class 9",
                    "Class 10",
                    "Class 11",
                    "Class 12",
                    "Degree",
                    "Postgraduate",
                    "Professional"
                ]
            ),
            Rule(
                attribute="studying_in_bonafide_institution",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "Certificate from Reader",
        "Certificate from Head of Institution",
        "National Identity Card for Differently Abled",
        "Statement of marks in previous qualifying examination"
    ],
    application={
        "mode": "offline",
        "authority": "District Differently Abled Welfare Officer"
    },
    sources=[
        "Tamil Nadu Commissionerate for Welfare of Differently Abled Persons"
    ]
)


# ==================================================
# 5. Marriage Assistance to Normal Persons
#    Marrying Visually Impaired Persons
# ==================================================

marriage_assistance = Scheme(
    scheme_id="TN-DA-MA-002",
    name="Marriage Assistance to Normal Persons Marrying Visually Impaired Persons",
    description=(
        "Tamil Nadu Government marriage assistance for a normal "
        "person marrying a visually impaired person."
    ),
    benefits={
        "type": "financial_assistance",
        "amount": {
            "basic": 25000,
            "degree_or_diploma_holder": 50000
        },
        "currency": "INR",
        "additional_benefit": "8 gram gold coin for Thirumangalyam"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="one_partner_is_visually_impaired",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="other_partner_is_normal",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="both_partners_age_above_18",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[],
    application={
        "mode": "offline",
        "authority": "District Differently Abled Welfare Officer"
    },
    sources=[
        "Tamil Nadu Commissionerate for Welfare of Differently Abled Persons"
    ]
)


# ==================================================
# All Batch 2 schemes
# ==================================================

schemes = [
    unemployment_allowance,
    intellectual_disability_maintenance,
    personal_assistance,
    readers_allowance,
    marriage_assistance
]


# ==================================================
# Insert into MongoDB
# ==================================================

collection = db["schemes"]

for scheme in schemes:

    print(f"Validating: {scheme.scheme_id}")

    scheme_data = scheme.model_dump(mode="json")

    existing = collection.find_one(
        {"scheme_id": scheme.scheme_id}
    )

    if existing:
        print(
            f"Already exists: {scheme.scheme_id} - skipping"
        )
        continue

    result = collection.insert_one(scheme_data)

    print(
        f"Inserted: {scheme.scheme_id} "
        f"| MongoDB ID: {result.inserted_id}"
    )


print("\nBatch 2 completed.")