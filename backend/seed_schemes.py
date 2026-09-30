from schemas.scheme import Scheme, Rule, ConditionGroup, Logic, Operator
from db.mongodb import db


# --------------------------------------------------
# 1. Thaimaaman Thanga Mothiram
# --------------------------------------------------

thaimaaman_scheme = Scheme(
    scheme_id="TN-TTMT-001",
    name="Thaimaaman Thanga Mothiram Thittam",
    description=(
        "Tamil Nadu Government scheme providing a one-gram gold ring "
        "for eligible children born in Government hospitals."
    ),
    benefits={
        "type": "in_kind",
        "item": "Gold ring",
        "quantity": "1 gram"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="state_residency",
                operator=Operator.EQUALS,
                value="Tamil Nadu"
            ),
            Rule(
                attribute="delivery_institution_type",
                operator=Operator.EQUALS,
                value="Government Hospital"
            ),
            Rule(
                attribute="child_date_of_birth",
                operator=Operator.GREATER_THAN_OR_EQUAL,
                value="2026-06-22"
            )
        ]
    ),
    documents=[],
    application={
        "mode": "Institutional delivery process"
    },
    sources=[
        "Tamil Nadu Directorate of Information and Public Relations",
        "Tiruvallur District Administration"
    ]
)


# --------------------------------------------------
# 2. Pudhumai Penn
# --------------------------------------------------

pudhumai_penn = Scheme(
    scheme_id="TN-PP-001",
    name="Moovalur Ramamirtham Ammaiyar Ninaivu Pudhumai Penn Thittam",
    description=(
        "Tamil Nadu higher education assistance scheme providing "
        "monthly financial support to eligible girl students from "
        "Government and Government-aided Tamil-medium schools."
    ),
    benefits={
        "amount": 1000,
        "currency": "INR",
        "frequency": "monthly",
        "method": "DBT"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="gender",
                operator=Operator.EQUALS,
                value="Female"
            ),
            Rule(
                attribute="studied_classes_6_to_12_continuously",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="school_type",
                operator=Operator.IN,
                value=[
                    "Government",
                    "Government Aided Tamil Medium"
                ]
            )
        ]
    ),
    documents=[
        "School study certificate",
        "Community certificate",
        "Income certificate",
        "Bank passbook",
        "Aadhaar card",
        "Admission proof"
    ],
    application={
        "mode": "online",
        "portal": "UMIS"
    },
    sources=[
        "Tamil Nadu Institute of Labour Studies"
    ]
)


# --------------------------------------------------
# 3. Tamil Pudhalvan
# --------------------------------------------------

tamil_pudhalvan = Scheme(
    scheme_id="TN-TP-001",
    name="Tamil Pudhalvan Scheme",
    description=(
        "Tamil Nadu higher education assistance scheme providing "
        "monthly financial support to eligible male students from "
        "Government and Government-aided Tamil-medium schools."
    ),
    benefits={
        "amount": 1000,
        "currency": "INR",
        "frequency": "monthly",
        "method": "DBT"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="gender",
                operator=Operator.EQUALS,
                value="Male"
            ),
            Rule(
                attribute="studied_classes_6_to_12_continuously",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="school_type",
                operator=Operator.IN,
                value=[
                    "Government",
                    "Government Aided Tamil Medium"
                ]
            )
        ]
    ),
    documents=[
        "School study certificate",
        "Community certificate",
        "Income certificate",
        "Bank passbook",
        "Aadhaar card",
        "Admission proof"
    ],
    application={
        "mode": "online",
        "portal": "UMIS"
    },
    sources=[
        "Tamil Nadu Institute of Labour Studies",
        "Tamil Nadu Government Budget"
    ]
)


# --------------------------------------------------
# All schemes
# --------------------------------------------------

schemes = [
    thaimaaman_scheme,
    pudhumai_penn,
    tamil_pudhalvan
]


# --------------------------------------------------
# Insert into MongoDB
# --------------------------------------------------

collection = db["schemes"]

for scheme in schemes:

    # Validate using Pydantic
    print(f"Validating: {scheme.scheme_id}")

    # Convert Pydantic model to MongoDB-compatible dictionary
    scheme_data = scheme.model_dump(mode="json")

    # Prevent duplicate insertion
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


print("\nDone.")