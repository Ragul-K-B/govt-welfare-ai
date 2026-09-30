from schemas.scheme import Scheme, Rule, ConditionGroup, Logic, Operator
from db.mongodb import db


# ============================================================
# 1. Chief Minister's Girl Child Protection Scheme - Scheme I
# ============================================================

girl_child_scheme_1 = Scheme(
    scheme_id="TN-SW-GCPS-001",
    name="Chief Minister's Girl Child Protection Scheme - Scheme I",
    description=(
        "Tamil Nadu Government scheme for families having one girl child, "
        "intended to promote girl child education, discourage preference "
        "for male children and promote the small family norm."
    ),
    benefits={
        "type": "fixed_deposit",
        "amount": 50000,
        "currency": "INR",
        "maturity_age": 18,
        "beneficiary": "Girl child"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="number_of_girl_children",
                operator=Operator.EQUALS,
                value=1
            ),
            Rule(
                attribute="number_of_male_children",
                operator=Operator.EQUALS,
                value=0
            ),
            Rule(
                attribute="annual_family_income",
                operator=Operator.LESS_THAN_OR_EQUAL,
                value=72000
            ),
            Rule(
                attribute="parent_or_grandparent_tamil_nadu_domicile_years",
                operator=Operator.GREATER_THAN_OR_EQUAL,
                value=10
            ),
            Rule(
                attribute="parent_underwent_sterilisation_before_age",
                operator=Operator.LESS_THAN_OR_EQUAL,
                value=40
            ),
            Rule(
                attribute="application_child_age",
                operator=Operator.LESS_THAN,
                value=3
            )
        ]
    ),
    documents=[
        "Birth Certificate",
        "Parents Age Proof",
        "Sterilisation Certificate",
        "Income Certificate",
        "No Male Child Certificate"
    ],
    application={
        "mode": "online",
        "portal": "Tamil Nadu e-Sevai",
        "deadline": "Before the girl child completes 3 years of age"
    },
    sources=[
        "https://tnlegalservices.tn.gov.in/swwe/Annexure_English.pdf"
    ]
)


# ============================================================
# 2. Chief Minister's Girl Child Protection Scheme - Scheme II
# ============================================================

girl_child_scheme_2 = Scheme(
    scheme_id="TN-SW-GCPS-002",
    name="Chief Minister's Girl Child Protection Scheme - Scheme II",
    description=(
        "Tamil Nadu Government scheme for families having two girl children "
        "and no male child, intended to promote girl child education and "
        "the small family norm."
    ),
    benefits={
        "type": "fixed_deposit",
        "amount_per_girl_child": 25000,
        "total_amount": 50000,
        "currency": "INR",
        "maturity_age": 18,
        "beneficiary": "Two girl children"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="number_of_girl_children",
                operator=Operator.EQUALS,
                value=2
            ),
            Rule(
                attribute="number_of_male_children",
                operator=Operator.EQUALS,
                value=0
            ),
            Rule(
                attribute="annual_family_income",
                operator=Operator.LESS_THAN_OR_EQUAL,
                value=72000
            ),
            Rule(
                attribute="parent_or_grandparent_tamil_nadu_domicile_years",
                operator=Operator.GREATER_THAN_OR_EQUAL,
                value=10
            ),
            Rule(
                attribute="parent_underwent_sterilisation_before_age",
                operator=Operator.LESS_THAN_OR_EQUAL,
                value=40
            ),
            Rule(
                attribute="application_second_child_age",
                operator=Operator.LESS_THAN,
                value=3
            )
        ]
    ),
    documents=[
        "Birth Certificates",
        "Parents Age Proof",
        "Sterilisation Certificate",
        "Income Certificate",
        "No Male Child Certificate"
    ],
    application={
        "mode": "online",
        "portal": "Tamil Nadu e-Sevai",
        "deadline": "Before the second girl child completes 3 years of age"
    },
    sources=[
        "https://tnlegalservices.tn.gov.in/swwe/Annexure_English.pdf"
    ]
)


# ============================================================
# 3. Unemployment Allowance for Differently Abled Persons
# ============================================================

disabled_unemployment = Scheme(
    scheme_id="TN-SCD-UNEMP-001",
    name="Unemployment Allowance for Differently Abled Persons",
    description=(
        "Tamil Nadu assistance scheme providing monthly unemployment "
        "allowance to differently abled persons who have remained in "
        "the live register of the employment exchange for more than one year."
    ),
    benefits={
        "type": "monthly_allowance",
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
                attribute="employment_exchange_live_register_years",
                operator=Operator.GREATER_THAN,
                value=1
            )
        ]
    ),
    documents=[
        "Employment Registration Card",
        "National Identity Card for Differently Abled Persons"
    ],
    application={
        "mode": "offline",
        "authority": "District Employment Officer"
    },
    sources=[
        "https://www.scd.tn.gov.in/social_sec_schemes.php"
    ]
)


# ============================================================
# 4. Personal Assistance Allowance
# ============================================================

personal_assistance = Scheme(
    scheme_id="TN-SCD-PAA-001",
    name="Personal Assistance Allowance for Persons with High Support Needs",
    description=(
        "Tamil Nadu assistance scheme providing monthly personal assistance "
        "allowance to differently abled persons with high support needs who "
        "require assistance for activities of daily living."
    ),
    benefits={
        "type": "monthly_allowance",
        "amount": 1000,
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
                attribute="has_high_support_needs",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "High Support Need Assessment Board Recommendation Certificate"
    ],
    application={
        "mode": "offline",
        "authority": "District Differently Abled Welfare Officer"
    },
    sources=[
        "https://www.scd.tn.gov.in/social_sec_schemes.php"
    ]
)


# ============================================================
# 5. Indira Gandhi National Old Age Pension Scheme
# ============================================================

ignoaps = Scheme(
    scheme_id="TN-SSP-IGNOAPS-001",
    name="Indira Gandhi National Old Age Pension Scheme",
    description=(
        "Social security pension scheme providing monthly financial "
        "assistance to eligible elderly persons belonging to vulnerable "
        "and economically weaker sections."
    ),
    benefits={
        "type": "monthly_pension",
        "amount": 1200,
        "currency": "INR",
        "frequency": "monthly"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="age",
                operator=Operator.GREATER_THAN_OR_EQUAL,
                value=60
            ),
            Rule(
                attribute="is_economically_vulnerable",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "Aadhaar Card",
        "Aadhaar Consent Form",
        "Smart Card / Ration Card / Address Proof",
        "Bank Passbook",
        "Identity Proof"
    ],
    application={
        "mode": "online",
        "portal": "Tamil Nadu e-Sevai",
        "authority": "Revenue Department"
    },
    sources=[
        "https://cra.tn.gov.in/about_schemes_t.php",
        "https://oap.tn.gov.in/"
    ]
)


# ============================================================
# ALL BATCH 5 SCHEMES
# ============================================================

schemes = [
    girl_child_scheme_1,
    girl_child_scheme_2,
    disabled_unemployment,
    personal_assistance,
    ignoaps
]


# ============================================================
# INSERT INTO MONGODB
# ============================================================

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


print("\nBatch 5 completed.")