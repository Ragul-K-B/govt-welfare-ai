from schemas.scheme import Scheme, Rule, ConditionGroup, Logic, Operator
from db.mongodb import db


# ==================================================
# 1. Rural Girls' Incentive Scheme
# ==================================================

rural_girls_incentive = Scheme(
    scheme_id="TN-BC-RGI-001",
    name="Rural Girls' Incentive Scheme",
    description=(
        "Tamil Nadu Government incentive scheme for girl students "
        "belonging to Most Backward Classes and Denotified Communities "
        "studying in Government or Government-aided schools in rural areas."
    ),
    benefits={
        "type": "financial_assistance",
        "amount": {
            "classes_3_to_5": 500,
            "class_6": 1000
        },
        "currency": "INR",
        "frequency": "annual"
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
                attribute="community_category",
                operator=Operator.IN,
                value=[
                    "MBC",
                    "DNC"
                ]
            ),
            Rule(
                attribute="annual_parental_income",
                operator=Operator.LESS_THAN_OR_EQUAL,
                value=100000
            ),
            Rule(
                attribute="school_type",
                operator=Operator.IN,
                value=[
                    "Government",
                    "Government Aided"
                ]
            ),
            Rule(
                attribute="school_location",
                operator=Operator.EQUALS,
                value="Rural"
            ),
            Rule(
                attribute="district",
                operator=Operator.NOT_EQUALS,
                value="Chennai"
            ),
            Rule(
                attribute="class",
                operator=Operator.IN,
                value=[
                    3,
                    4,
                    5,
                    6
                ]
            )
        ]
    ),
    documents=[],
    application={
        "mode": "offline",
        "authority": "Headmaster of concerned Government/Government-aided school"
    },
    sources=[
        "Tamil Nadu Directorate of Backward Classes Welfare"
    ]
)


# ==================================================
# 2. Free Bicycle Scheme
# ==================================================

free_bicycle = Scheme(
    scheme_id="TN-BC-FBC-001",
    name="Free Bicycle Scheme for 11th Standard Students",
    description=(
        "Tamil Nadu Government scheme providing free bicycles "
        "to students studying in the 11th standard in Government, "
        "Government-aided and partially aided schools."
    ),
    benefits={
        "type": "in_kind",
        "item": "Bicycle",
        "quantity": 1
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="class",
                operator=Operator.EQUALS,
                value=11
            ),
            Rule(
                attribute="school_type",
                operator=Operator.IN,
                value=[
                    "Government",
                    "Government Aided",
                    "Partially Aided"
                ]
            ),
            Rule(
                attribute="staying_in_school_hostel",
                operator=Operator.EQUALS,
                value=False
            ),
            Rule(
                attribute="staying_in_residential_school",
                operator=Operator.EQUALS,
                value=False
            )
        ]
    ),
    documents=[],
    application={
        "mode": "institutional",
        "authority": "Concerned School Headmaster"
    },
    sources=[
        "Tamil Nadu Directorate of Backward Classes Welfare"
    ]
)


# ==================================================
# 3. Post-Matric Scholarship - College Students
# ==================================================

post_matric_college = Scheme(
    scheme_id="TN-BC-PMS-001",
    name="Post-Matric Scholarship for BC/MBC/DNC College Students",
    description=(
        "Tamil Nadu scholarship scheme for eligible BC, MBC and DNC "
        "students pursuing ITI, Diploma, Postgraduate, Professional "
        "and PhD courses."
    ),
    benefits={
        "type": "education_financial_assistance",
        "components": [
            "Tuition fee",
            "Special fee",
            "Examination fee",
            "Book money"
        ],
        "hostel_support": {
            "amount": 4000,
            "currency": "INR",
            "frequency": "annual"
        }
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="community_category",
                operator=Operator.IN,
                value=[
                    "BC",
                    "MBC",
                    "DNC"
                ]
            ),
            Rule(
                attribute="annual_parental_income",
                operator=Operator.LESS_THAN_OR_EQUAL,
                value=250000
            ),
            Rule(
                attribute="course_level",
                operator=Operator.IN,
                value=[
                    "ITI",
                    "Diploma",
                    "Postgraduate",
                    "Professional",
                    "PhD"
                ]
            )
        ]
    ),
    documents=[],
    application={
        "mode": "institutional",
        "portal": "Unified State Scholarship Portal (USSP/UMIS)"
    },
    sources=[
        "Tamil Nadu Directorate of Backward Classes Welfare"
    ]
)


# ==================================================
# 4. Free Education Scholarship - Diploma
# ==================================================

free_education_diploma = Scheme(
    scheme_id="TN-BC-FED-001",
    name="Free Education Scholarship for Diploma Students",
    description=(
        "Tamil Nadu Government free education scholarship for "
        "BC, MBC and DNC students pursuing diploma courses in "
        "Government and Government-aided Polytechnic Colleges."
    ),
    benefits={
        "type": "education_financial_assistance",
        "components": [
            "Tuition fee",
            "Special fee",
            "Non-refundable compulsory fee",
            "Book money",
            "Examination fee"
        ],
        "hostel_support": {
            "amount": 4000,
            "currency": "INR",
            "frequency": "annual"
        }
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="community_category",
                operator=Operator.IN,
                value=[
                    "BC",
                    "MBC",
                    "DNC"
                ]
            ),
            Rule(
                attribute="course_level",
                operator=Operator.EQUALS,
                value="Diploma"
            ),
            Rule(
                attribute="institution_type",
                operator=Operator.IN,
                value=[
                    "Government Polytechnic",
                    "Government Aided Polytechnic"
                ]
            ),
            Rule(
                attribute="annual_parental_income",
                operator=Operator.LESS_THAN_OR_EQUAL,
                value=250000
            ),
            Rule(
                attribute="is_first_diploma_or_graduate_in_family",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[],
    application={
        "mode": "institutional",
        "portal": "Scholarship application through institution"
    },
    sources=[
        "Tamil Nadu Directorate of Backward Classes Welfare"
    ]
)


# ==================================================
# 5. Scholarship for IIT/IIM/IIIT/NIT/Central Universities
# ==================================================

central_institution_scholarship = Scheme(
    scheme_id="TN-BC-CIU-001",
    name="Scholarship for BC/MBC/DNC Students in Central Institutions",
    description=(
        "Tamil Nadu scholarship for BC, MBC and DNC students who "
        "are natives of Tamil Nadu and pursue undergraduate or "
        "postgraduate courses in IITs, IIMs, IIITs, NITs or Central Universities."
    ),
    benefits={
        "type": "education_financial_assistance",
        "maximum_reimbursement": 200000,
        "currency": "INR",
        "frequency": "annual",
        "covered_fees": [
            "Tuition fee",
            "Special fee",
            "Examination fee",
            "Other compulsory fees"
        ]
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="community_category",
                operator=Operator.IN,
                value=[
                    "BC",
                    "MBC",
                    "DNC"
                ]
            ),
            Rule(
                attribute="is_native_of_tamil_nadu",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="course_level",
                operator=Operator.IN,
                value=[
                    "UG",
                    "PG"
                ]
            ),
            Rule(
                attribute="institution_type",
                operator=Operator.IN,
                value=[
                    "IIT",
                    "IIM",
                    "IIIT",
                    "NIT",
                    "Central University"
                ]
            ),
            Rule(
                attribute="annual_family_income",
                operator=Operator.LESS_THAN_OR_EQUAL,
                value=250000
            )
        ]
    ),
    documents=[],
    application={
        "mode": "institutional",
        "authority": "Commissioner of Backward Classes Welfare"
    },
    sources=[
        "Tamil Nadu Directorate of Backward Classes Welfare"
    ]
)


# ==================================================
# All Batch 3 schemes
# ==================================================

schemes = [
    rural_girls_incentive,
    free_bicycle,
    post_matric_college,
    free_education_diploma,
    central_institution_scholarship
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


print("\nBatch 3 completed.")