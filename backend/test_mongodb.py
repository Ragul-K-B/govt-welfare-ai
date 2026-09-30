from db.mongodb import db
from schemas.scheme import Scheme
from eligibility.engine import evaluate_condition


# Get schemes collection
schemes_collection = db["schemes"]


# Retrieve TEST-001 from MongoDB
document = schemes_collection.find_one(
    {"scheme_id": "TEST-001"}
)


# Check whether scheme was found
if document is None:
    print("Scheme not found")
    exit()


print("Scheme retrieved from MongoDB:")
print(document)


# Convert MongoDB document back into our Scheme model
scheme = Scheme.model_validate(document)


print("\nScheme validated successfully:")
print(scheme)


# --------------------------------------------------
# TEST 1: Eligible citizen
# --------------------------------------------------

citizen_1 = {
    "age": 22,
    "state": "Tamil Nadu"
}

decision_1 = evaluate_condition(
    scheme.eligibility,
    citizen_1
)

print("\nTest 1")
print("Citizen:", citizen_1)
print("Decision:", decision_1.value)


# --------------------------------------------------
# TEST 2: Not eligible citizen
# --------------------------------------------------

citizen_2 = {
    "age": 17,
    "state": "Tamil Nadu"
}

decision_2 = evaluate_condition(
    scheme.eligibility,
    citizen_2
)

print("\nTest 2")
print("Citizen:", citizen_2)
print("Decision:", decision_2.value)


# --------------------------------------------------
# TEST 3: Missing information
# --------------------------------------------------

citizen_3 = {
    "age": 22
}

decision_3 = evaluate_condition(
    scheme.eligibility,
    citizen_3
)

print("\nTest 3")
print("Citizen:", citizen_3)
print("Decision:", decision_3.value)