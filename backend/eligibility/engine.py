from enum import Enum

from schemas.scheme import Rule, ConditionGroup


class Decision(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


def evaluate_rule(rule: Rule, citizen: dict) -> Decision:

    # Attribute is missing
    if rule.attribute not in citizen:
        return Decision.UNKNOWN

    # Get citizen value
    citizen_value = citizen[rule.attribute]

    # Attribute exists but value is unknown
    if citizen_value is None:
        return Decision.UNKNOWN

    expected_value = rule.value
    operator = rule.operator.value

    # EQUALS
    if operator == "EQUALS":
        result = citizen_value == expected_value

    # NOT_EQUALS
    elif operator == "NOT_EQUALS":
        result = citizen_value != expected_value

    # GREATER THAN
    elif operator == ">":
        result = citizen_value > expected_value

    # GREATER THAN OR EQUAL
    elif operator == ">=":
        result = citizen_value >= expected_value

    # LESS THAN
    elif operator == "<":
        result = citizen_value < expected_value

    # LESS THAN OR EQUAL
    elif operator == "<=":
        result = citizen_value <= expected_value

    # IN
    elif operator == "IN":
        result = citizen_value in expected_value

    # NOT IN
    elif operator == "NOT_IN":
        result = citizen_value not in expected_value

    else:
        raise ValueError(
            f"Unsupported operator: {rule.operator}"
        )

    # Convert boolean result to Decision
    if result:
        return Decision.PASS

    return Decision.FAIL


def evaluate_condition(condition, citizen: dict) -> Decision:

    # --------------------------------------------------
    # SINGLE RULE
    # --------------------------------------------------

    if isinstance(condition, Rule):
        return evaluate_rule(condition, citizen)

    # --------------------------------------------------
    # CONDITION GROUP
    # --------------------------------------------------

    if isinstance(condition, ConditionGroup):

        # Empty groups are invalid
        if not condition.conditions:
            raise ValueError(
                "ConditionGroup must contain at least one condition"
            )

        # Recursively evaluate every condition
        results = [
            evaluate_condition(item, citizen)
            for item in condition.conditions
        ]

        # --------------------------------------------------
        # AND LOGIC
        # --------------------------------------------------

        if condition.logic.value == "AND":

            # One FAIL is enough to make the whole AND fail
            if Decision.FAIL in results:
                return Decision.FAIL

            # No FAIL, but something is UNKNOWN
            if Decision.UNKNOWN in results:
                return Decision.UNKNOWN

            # Everything passed
            return Decision.PASS

        # --------------------------------------------------
        # OR LOGIC
        # --------------------------------------------------

        elif condition.logic.value == "OR":

            # One PASS is enough to make the whole OR pass
            if Decision.PASS in results:
                return Decision.PASS

            # No PASS, but something is UNKNOWN
            if Decision.UNKNOWN in results:
                return Decision.UNKNOWN

            # Everything failed
            return Decision.FAIL

        else:
            raise ValueError(
                f"Unsupported logic: {condition.logic}"
            )

    # --------------------------------------------------
    # INVALID CONDITION TYPE
    # --------------------------------------------------

    raise TypeError(
        f"Unsupported condition type: {type(condition)}"
    )