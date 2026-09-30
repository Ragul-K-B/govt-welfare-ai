from schemas.scheme import Scheme, Rule, ConditionGroup, Logic, Operator
from db.mongodb import db


# ============================================================
# 1. Maintenance Allowance to Intellectually Disabled Persons
# ============================================================

maintenance_intellectual = Scheme(
    scheme_id="TN-SCD-MA-ID-001",
    name="Maintenance Allowance to Intellectually Disabled Persons",
    description=(
        "Tamil Nadu Government maintenance allowance for "
        "intellectually disabled persons having 40 percentage "
        "of disability and above."
    ),
    benefits={
        "type": "monthly_allowance",
        "amount": 1500,
        "currency": "INR",
        "frequency": "monthly"
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
        "Bank Account Details"
    ],
    application={
        "mode": "offline",
        "authority": "District Differently Abled Welfare Officer"
    },
    sources=[
        "https://www.scd.tn.gov.in/Mintantance_allowance.php"
    ]
)


# ============================================================
# 2. Travel Concession for Differently Abled Persons
# ============================================================

travel_concession = Scheme(
    scheme_id="TN-SCD-TRAVEL-001",
    name="Travel Concession to Differently Abled Persons",
    description=(
        "Travel concession in State-owned transport corporation "
        "buses for eligible differently abled persons travelling "
        "for education, employment, vocational training, medical "
        "treatment and related purposes."
    ),
    benefits={
        "type": "free_travel_concession",
        "details": [
            "Free travel for eligible visually impaired persons "
            "within specified distance",
            "Free travel for eligible intellectually disabled "
            "persons with one escort",
            "Free travel for eligible speech and hearing impaired "
            "and locomotor differently abled persons for specified purposes"
        ]
    },
    eligibility=ConditionGroup(
        logic=Logic.OR,
        conditions=[
            ConditionGroup(
                logic=Logic.AND,
                conditions=[
                    Rule(
                        attribute="disability_type",
                        operator=Operator.EQUALS,
                        value="Visual Impairment"
                    )
                ]
            ),
            ConditionGroup(
                logic=Logic.AND,
                conditions=[
                    Rule(
                        attribute="disability_type",
                        operator=Operator.EQUALS,
                        value="Intellectual Disability"
                    ),
                    Rule(
                        attribute="requires_escort",
                        operator=Operator.EQUALS,
                        value=True
                    )
                ]
            ),
            ConditionGroup(
                logic=Logic.AND,
                conditions=[
                    Rule(
                        attribute="disability_type",
                        operator=Operator.IN,
                        value=[
                            "Speech and Hearing Impairment",
                            "Locomotor Disability"
                        ]
                    ),
                    Rule(
                        attribute="travel_purpose",
                        operator=Operator.IN,
                        value=[
                            "Education",
                            "Employment",
                            "Vocational Training",
                            "Medical Treatment"
                        ]
                    )
                ]
            )
        ]
    ),
    documents=[
        "Disability Identity Card / National Identity Card"
    ],
    application={
        "mode": "institutional",
        "authority": "State-owned Transport Corporation"
    },
    sources=[
        "https://www.scd.tn.gov.in/social_sec_schemes.php"
    ]
)


# ============================================================
# 3. Readers Allowance to Visually Impaired Persons
# ============================================================

readers_allowance = Scheme(
    scheme_id="TN-SCD-READER-001",
    name="Readers Allowance to Visually Impaired Students",
    description=(
        "Readers allowance for visually impaired students studying "
        "in Class IX and above in recognised institutions."
    ),
    benefits={
        "type": "annual_allowance",
        "amount": {
            "IX_to_XII": 3000,
            "Degree": 5000,
            "Postgraduate_and_Professional": 6000
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
                    "IX",
                    "X",
                    "XI",
                    "XII",
                    "Degree",
                    "Postgraduate",
                    "Professional"
                ]
            ),
            Rule(
                attribute="institution_is_bonafide",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="reader_certificate_available",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "Certificate from Head of Institution",
        "National Identity Card for Differently Abled",
        "Previous Qualifying Examination Marks Statement",
        "Certificate from Reader"
    ],
    application={
        "mode": "offline",
        "authority": "District Differently Abled Welfare Officer"
    },
    sources=[
        "https://www.scd.tn.gov.in/financial_assist.php"
    ]
)


# ============================================================
# 4. Supply of Braille Books
# ============================================================

braille_books = Scheme(
    scheme_id="TN-SCD-BRAILLE-001",
    name="Supply of Braille Books",
    description=(
        "Government scheme providing Braille books to visually "
        "impaired students studying in Government and Government "
        "aided special schools."
    ),
    benefits={
        "type": "educational_material",
        "item": "Braille Books"
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
                attribute="school_type",
                operator=Operator.IN,
                value=[
                    "Government Special School",
                    "Government Aided Special School"
                ]
            ),
            Rule(
                attribute="student_is_in_special_school",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[],
    application={
        "mode": "institutional",
        "application_required": False,
        "authority": "Principal / Head Master of concerned special school"
    },
    sources=[
        "https://scd.tn.gov.in/specialedu.php"
    ]
)


# ============================================================
# 5. Personal Accident Relief for Differently Abled Persons
# ============================================================

accident_relief = Scheme(
    scheme_id="TN-SCD-ACCIDENT-001",
    name="Personal Accident Relief for Differently Abled Persons",
    description=(
        "Accident relief provided to registered differently abled "
        "persons through the Tamil Nadu Welfare Board for "
        "Differently Abled Persons."
    ),
    benefits={
        "type": "accident_relief",
        "amount": {
            "death_or_specified_total_loss": 100000,
            "loss_of_one_hand_or_leg_or_one_eye_sight": 50000,
            "other_total_disablement": 25000
        },
        "currency": "INR"
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
                attribute="has_differently_abled_national_identity_card",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="welfare_board_member",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="accident_occurred",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "Medical Certificates",
        "Original Identity Card issued by Welfare Board"
    ],
    application={
        "mode": "offline",
        "authority": "District Differently Abled Welfare Office"
    },
    sources=[
        "https://www.scd.tn.gov.in/tn_welfare.php"
    ]
)


# ============================================================
# 6. Scholarship to Son/Daughter of Differently Abled Persons
# ============================================================

children_scholarship = Scheme(
    scheme_id="TN-SCD-CHILD-SCHOLAR-001",
    name="Scholarship to Son and Daughter of Differently Abled Persons",
    description=(
        "Educational scholarship for children of differently abled "
        "persons holding the identity card issued by the Welfare Board."
    ),
    benefits={
        "type": "educational_scholarship",
        "amounts": {
            "10th": 1000,
            "11th": 1000,
            "12th": 1500,
            "undergraduate": 1500,
            "undergraduate_with_hostel": 1750,
            "postgraduate": 2000,
            "postgraduate_with_hostel": 3000,
            "professional_degree": 2000,
            "professional_degree_with_hostel": 4000,
            "professional_postgraduate": 4000,
            "professional_postgraduate_with_hostel": 6000
        },
        "currency": "INR"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="is_child_of_differently_abled_person",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="parent_has_welfare_board_identity_card",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "Identity Card issued by Welfare Board",
        "Certificate from Educational Institution"
    ],
    application={
        "mode": "offline",
        "authority": "District Differently Abled Welfare Officer"
    },
    sources=[
        "https://www.scd.tn.gov.in/tn_welfare.php"
    ]
)


# ============================================================
# 7. Marriage Assistance to Differently Abled Persons
# ============================================================

marriage_assistance = Scheme(
    scheme_id="TN-SCD-MARRIAGE-001",
    name="Marriage Assistance to Differently Abled Persons",
    description=(
        "Marriage assistance for eligible differently abled persons "
        "or their children through the Tamil Nadu Welfare Board "
        "for Differently Abled Persons."
    ),
    benefits={
        "type": "marriage_assistance",
        "amount": 2000,
        "currency": "INR"
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="is_child_of_differently_abled_person",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="parent_has_welfare_board_identity_card",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="marriage_age_requirement_satisfied",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "Identity Card issued by Welfare Board",
        "Birth Certificate",
        "Proof of Marriage"
    ],
    application={
        "mode": "offline",
        "authority": "District Differently Abled Welfare Officer"
    },
    sources=[
        "https://www.scd.tn.gov.in/tn_welfare.php"
    ]
)


# ============================================================
# ALL BATCH 6 SCHEMES
# ============================================================

schemes = [
    maintenance_intellectual,
    travel_concession,
    readers_allowance,
    braille_books,
    accident_relief,
    children_scholarship,
    marriage_assistance
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


print("\nBatch 6 completed.")