from schemas.scheme import Scheme, Rule, ConditionGroup, Logic, Operator
from db.mongodb import db


# ============================================================
# 1. Educational Assistance - Unorganised Workers Welfare Board
# ============================================================

worker_education = Scheme(
    scheme_id="TN-UWWB-EDU-001",
    name="Educational Assistance for Children of Registered Unorganised Workers",
    description=(
        "Educational assistance provided through the Tamil Nadu "
        "Unorganised Workers Welfare Board to eligible children "
        "of registered welfare-board members."
    ),
    benefits={
        "type": "educational_assistance",
        "details": (
            "Educational assistance is available for eligible "
            "children of registered welfare-board members."
        )
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="welfare_board_member",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="registration_status",
                operator=Operator.EQUALS,
                value="LIVE"
            ),
            Rule(
                attribute="is_member_child",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "Welfare Board Registration Card",
        "Ration Card",
        "Aadhaar Card",
        "Bank Passbook",
        "Educational Certificate"
    ],
    application={
        "mode": "online",
        "portal": "Tamil Nadu Unorganised Workers Welfare Board"
    },
    sources=[
        "https://www.tnuwwb.tn.gov.in/claims/login"
    ]
)


# ============================================================
# 2. Marriage Assistance - Unorganised Workers Welfare Board
# ============================================================

worker_marriage = Scheme(
    scheme_id="TN-UWWB-MAR-001",
    name="Marriage Assistance for Registered Unorganised Workers",
    description=(
        "Marriage assistance provided through the Tamil Nadu "
        "Unorganised Workers Welfare Board for eligible registered "
        "welfare-board members or their children."
    ),
    benefits={
        "type": "marriage_assistance",
        "details": (
            "Marriage assistance is available to eligible registered "
            "members for their own marriage or the marriage of their "
            "son or daughter, subject to the board conditions."
        )
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="welfare_board_member",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="registration_status",
                operator=Operator.EQUALS,
                value="LIVE"
            ),
            Rule(
                attribute="marriage_assistance_for",
                operator=Operator.IN,
                value=[
                    "SELF",
                    "SON",
                    "DAUGHTER"
                ]
            )
        ]
    ),
    documents=[
        "Welfare Board Registration Card",
        "Ration Card",
        "Aadhaar Card",
        "Bank Passbook",
        "Marriage Registration Certificate",
        "Marriage Invitation"
    ],
    application={
        "mode": "online",
        "portal": "Tamil Nadu Unorganised Workers Welfare Board"
    },
    sources=[
        "https://www.tnuwwb.tn.gov.in/claims/login"
    ]
)


# ============================================================
# 3. Maternity Assistance - Unorganised Workers Welfare Board
# ============================================================

worker_maternity = Scheme(
    scheme_id="TN-UWWB-MAT-001",
    name="Maternity Assistance for Registered Female Workers",
    description=(
        "Maternity assistance provided through the Tamil Nadu "
        "Unorganised Workers Welfare Board to eligible registered "
        "female members."
    ),
    benefits={
        "type": "maternity_assistance",
        "details": (
            "Maternity, miscarriage and termination-of-pregnancy "
            "assistance is available subject to the conditions "
            "prescribed by the Welfare Board."
        )
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
                attribute="welfare_board_member",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="registration_status",
                operator=Operator.EQUALS,
                value="LIVE"
            ),
            Rule(
                attribute="existing_children",
                operator=Operator.LESS_THAN,
                value=2
            )
        ]
    ),
    documents=[
        "Welfare Board Registration Card",
        "Aadhaar Card",
        "Bank Passbook",
        "Pregnancy Certificate",
        "Employment Verification Certificate"
    ],
    application={
        "mode": "online",
        "portal": "Tamil Nadu Unorganised Workers Welfare Board"
    },
    sources=[
        "https://www.tnuwwb.tn.gov.in/claims/login"
    ]
)


# ============================================================
# 4. Uzhavar Santhai - Farmers Market
# ============================================================

uzhavar_santhai = Scheme(
    scheme_id="TN-AGR-US-001",
    name="Uzhavar Santhai (Farmers Market)",
    description=(
        "Tamil Nadu Government farmers market initiative that "
        "enables farmers cultivating fruits and vegetables to "
        "sell their produce directly to consumers."
    ),
    benefits={
        "type": "market_access",
        "details": [
            "Direct farmer-to-consumer marketing",
            "Better price realization for farmers",
            "Reduced dependence on intermediaries",
            "Fresh fruits and vegetables for consumers"
        ]
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="is_farmer",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="cultivates_fruits_or_vegetables",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="has_horticulture_department_identity_card",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "Identity Card issued by Department of Horticulture and Plantation Crops"
    ],
    application={
        "mode": "offline",
        "authority": (
            "District Collector / Deputy Director of Agriculture "
            "(Agri Business) / Agricultural Officer"
        )
    },
    sources=[
        "https://www.agrimark.tn.gov.in/Infra/fpo",
        "https://www.agritech.tnau.ac.in/govt_schemes_services/Binder1.pdf"
    ]
)


# ============================================================
# 5. KAVIADP - Fallow Land Development
# ============================================================

kaviadp = Scheme(
    scheme_id="TN-AGR-KAVIADP-001",
    name="Kalaignarin All Village Integrated Agricultural Development Programme",
    description=(
        "Tamil Nadu agricultural development programme aimed at "
        "making village panchayats self-sufficient and improving "
        "farmers' livelihoods, including support for bringing "
        "fallow land into cultivation."
    ),
    benefits={
        "type": "agricultural_assistance",
        "components": [
            "Fallow land development",
            "Bush clearance",
            "Land levelling",
            "Ploughing",
            "Other agricultural development activities"
        ]
    },
    eligibility=ConditionGroup(
        logic=Logic.AND,
        conditions=[
            Rule(
                attribute="is_farmer",
                operator=Operator.EQUALS,
                value=True
            ),
            Rule(
                attribute="has_fallow_land",
                operator=Operator.EQUALS,
                value=True
            )
        ]
    ),
    documents=[
        "Land ownership / cultivation document",
        "Aadhaar Card"
    ],
    application={
        "mode": "institutional",
        "authority": "Agriculture Department / Agricultural Extension Centre"
    },
    sources=[
        "https://www.tnagrisnet.tn.gov.in/Scheme_master/seachProduct/",
        "https://dipr.tn.gov.in/"
    ]
)


# ============================================================
# ALL BATCH 4 SCHEMES
# ============================================================

schemes = [
    worker_education,
    worker_marriage,
    worker_maternity,
    uzhavar_santhai,
    kaviadp
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


print("\nBatch 4 completed.")