from schemas.scheme import Rule, ConditionGroup
from eligibility.engine import evaluate_condition, Decision


# ==================================================
# 1. DEEP NESTING
# ==================================================

deep_group = ConditionGroup(
    logic="AND",
    conditions=[
        Rule(
            attribute="age",
            operator=">=",
            value=18
        ),
        ConditionGroup(
            logic="OR",
            conditions=[
                Rule(
                    attribute="state",
                    operator="EQUALS",
                    value="Tamil Nadu"
                ),
                ConditionGroup(
                    logic="AND",
                    conditions=[
                        Rule(
                            attribute="gender",
                            operator="EQUALS",
                            value="female"
                        ),
                        Rule(
                            attribute="income",
                            operator="<=",
                            value=300000
                        )
                    ]
                )
            ]
        )
    ]
)


citizen = {
    "age": 25,
    "gender": "male",
    "state": "Tamil Nadu"
}

print("\nTEST 1 - Deep nesting")
print(evaluate_condition(deep_group, citizen))


# ==================================================
# 2. AND INSIDE OR
# ==================================================

and_inside_or = ConditionGroup(
    logic="OR",
    conditions=[
        Rule(
            attribute="state",
            operator="EQUALS",
            value="Tamil Nadu"
        ),
        ConditionGroup(
            logic="AND",
            conditions=[
                Rule(
                    attribute="age",
                    operator=">=",
                    value=18
                ),
                Rule(
                    attribute="income",
                    operator="<=",
                    value=300000
                )
            ]
        )
    ]
)

citizen = {
    "state": "Kerala",
    "age": 25,
    "income": 200000
}

print("\nTEST 2 - AND inside OR")
print(evaluate_condition(and_inside_or, citizen))


# ==================================================
# 3. OR INSIDE AND
# ==================================================

or_inside_and = ConditionGroup(
    logic="AND",
    conditions=[
        Rule(
            attribute="age",
            operator=">=",
            value=18
        ),
        ConditionGroup(
            logic="OR",
            conditions=[
                Rule(
                    attribute="state",
                    operator="EQUALS",
                    value="Tamil Nadu"
                ),
                Rule(
                    attribute="state",
                    operator="EQUALS",
                    value="Kerala"
                )
            ]
        )
    ]
)

citizen = {
    "age": 25,
    "state": "Kerala"
}

print("\nTEST 3 - OR inside AND")
print(evaluate_condition(or_inside_and, citizen))


# ==================================================
# 4. ALL UNKNOWN
# ==================================================

all_unknown = ConditionGroup(
    logic="AND",
    conditions=[
        Rule(
            attribute="age",
            operator=">=",
            value=18
        ),
        Rule(
            attribute="income",
            operator="<=",
            value=300000
        )
    ]
)

citizen = {}

print("\nTEST 4 - All UNKNOWN")
print(evaluate_condition(all_unknown, citizen))


# ==================================================
# 5. BOUNDARY VALUES
# ==================================================

boundary_rule = Rule(
    attribute="age",
    operator=">=",
    value=18
)

print("\nTEST 5 - Boundary value")

print(
    "Age 18:",
    evaluate_condition(
        boundary_rule,
        {"age": 18}
    )
)

print(
    "Age 17:",
    evaluate_condition(
        boundary_rule,
        {"age": 17}
    )
)


# ==================================================
# 6. IN
# ==================================================

in_rule = Rule(
    attribute="state",
    operator="IN",
    value=[
        "Tamil Nadu",
        "Kerala",
        "Karnataka"
    ]
)

print("\nTEST 6 - IN")

print(
    "Tamil Nadu:",
    evaluate_condition(
        in_rule,
        {"state": "Tamil Nadu"}
    )
)

print(
    "Maharashtra:",
    evaluate_condition(
        in_rule,
        {"state": "Maharashtra"}
    )
)


# ==================================================
# 7. NOT_IN
# ==================================================

not_in_rule = Rule(
    attribute="state",
    operator="NOT_IN",
    value=[
        "Tamil Nadu",
        "Kerala",
        "Karnataka"
    ]
)

print("\nTEST 7 - NOT_IN")

print(
    "Maharashtra:",
    evaluate_condition(
        not_in_rule,
        {"state": "Maharashtra"}
    )
)

print(
    "Tamil Nadu:",
    evaluate_condition(
        not_in_rule,
        {"state": "Tamil Nadu"}
    )
)


# ==================================================
# 8. NONE IN NESTED GROUP
# ==================================================

none_nested = ConditionGroup(
    logic="OR",
    conditions=[
        Rule(
            attribute="age",
            operator=">=",
            value=18
        ),
        Rule(
            attribute="income",
            operator="<=",
            value=300000
        )
    ]
)

citizen = {
    "age": None,
    "income": None
}

print("\nTEST 8 - None values")
print(evaluate_condition(none_nested, citizen))


# ==================================================
# 9. INVALID CONDITION TYPE
# ==================================================

print("\nTEST 9 - Invalid condition type")

try:
    evaluate_condition(
        "this is not a rule",
        {"age": 25}
    )

except TypeError as e:
    print("Correctly rejected:")
    print(e)


# ==================================================
# 10. EMPTY CONDITION GROUP
# ==================================================

print("\nTEST 10 - Empty AND group")

empty_group = ConditionGroup(
    logic="AND",
    conditions=[]
)

try:
    result = evaluate_condition(empty_group, {})
    print("Unexpected result:", result)

except ValueError as e:
    print("Correctly rejected:")
    print(e)