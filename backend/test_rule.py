from schemas.scheme import Rule, ConditionGroup
from eligibility.engine import evaluate_condition, Decision


# --------------------------------------------------
# Simple AND
# --------------------------------------------------

and_group = ConditionGroup(
    logic="AND",
    conditions=[
        Rule(
            attribute="age",
            operator=">=",
            value=18
        ),
        Rule(
            attribute="state",
            operator="EQUALS",
            value="Tamil Nadu"
        )
    ]
)


print("\nAND TESTS")
print("=" * 50)


citizen = {
    "age": 24,
    "state": "Tamil Nadu"
}

print(
    "PASS + PASS:",
    evaluate_condition(and_group, citizen)
)


citizen = {
    "age": 24,
    "state": "Kerala"
}

print(
    "PASS + FAIL:",
    evaluate_condition(and_group, citizen)
)


citizen = {
    "age": 24
}

print(
    "PASS + UNKNOWN:",
    evaluate_condition(and_group, citizen)
)


citizen = {
    "age": 16
}

print(
    "FAIL + UNKNOWN:",
    evaluate_condition(and_group, citizen)
)


# --------------------------------------------------
# Simple OR
# --------------------------------------------------

or_group = ConditionGroup(
    logic="OR",
    conditions=[
        Rule(
            attribute="gender",
            operator="EQUALS",
            value="female"
        ),
        Rule(
            attribute="disability_percentage",
            operator=">=",
            value=40
        )
    ]
)


print("\nOR TESTS")
print("=" * 50)


citizen = {
    "gender": "female",
    "disability_percentage": 20
}

print(
    "PASS + FAIL:",
    evaluate_condition(or_group, citizen)
)


citizen = {
    "gender": "male",
    "disability_percentage": 50
}

print(
    "FAIL + PASS:",
    evaluate_condition(or_group, citizen)
)


citizen = {
    "gender": "female"
}

print(
    "PASS + UNKNOWN:",
    evaluate_condition(or_group, citizen)
)


citizen = {
    "gender": "male"
}

print(
    "FAIL + UNKNOWN:",
    evaluate_condition(or_group, citizen)
)


citizen = {}

print(
    "UNKNOWN + UNKNOWN:",
    evaluate_condition(or_group, citizen)
)