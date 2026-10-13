
from db.mongodb import schemes_collection
from eligibility.engine import Decision, evaluate_condition
from schemas.scheme import ConditionGroup


def get_relevant_missing_attributes(condition, citizen: dict) -> set[str]:
    """
    Find missing attributes that could change an UNKNOWN decision.
    Do not ask questions when the decision is already determined.
    """

    decision = evaluate_condition(condition, citizen)

    if decision != Decision.UNKNOWN:
        return set()

    if isinstance(condition, ConditionGroup):
        child_results = [
            evaluate_condition(item, citizen)
            for item in condition.conditions
        ]

        if condition.logic.value == "AND":
            relevant_conditions = [
                item
                for item, result in zip(
                    condition.conditions, child_results
                )
                if result == Decision.UNKNOWN
            ]
        else:  # OR
            relevant_conditions = [
                item
                for item, result in zip(
                    condition.conditions, child_results
                )
                if result == Decision.UNKNOWN
            ]

        missing = set()

        for item in relevant_conditions:
            missing.update(
                get_relevant_missing_attributes(item, citizen)
            )

        return missing

    # This is an individual Rule whose result is UNKNOWN.
    return {condition.attribute}



def evaluate_retrieved_schemes(
    retrieved_schemes: list[dict],
    citizen_profile: dict
) -> list[dict]:
    """
    Evaluate FAISS-retrieved schemes using MongoDB rules
    and return complete scheme details.
    """

    scheme_ids = [
        item["scheme_id"]
        for item in retrieved_schemes
    ]

    if not scheme_ids:
        return []

    # Fetch eligibility rules and scheme details from MongoDB.
    projection = {
        "_id": 0,
        "scheme_id": 1,
        "name": 1,
        "description": 1,
        "benefits": 1,
        "documents": 1,
        "application": 1,
        "sources": 1,
        "eligibility": 1,
    }

    documents = schemes_collection.find(
        {"scheme_id": {"$in": scheme_ids}},
        projection
    )

    documents_by_id = {
        document["scheme_id"]: document
        for document in documents
    }

    results = []

    # Preserve the ranking returned by FAISS.
    for retrieved in retrieved_schemes:
        scheme_id = retrieved["scheme_id"]
        document = documents_by_id.get(scheme_id)

        if document is None:
            continue

        eligibility = ConditionGroup.model_validate(
            document["eligibility"]
        )

        decision = evaluate_condition(
            eligibility,
            citizen_profile
        )

        missing_attributes = []

        if decision == Decision.UNKNOWN:
            missing_attributes = sorted(
                get_relevant_missing_attributes(
                    eligibility,
                    citizen_profile
                )
            )

        results.append({
            "scheme_id": scheme_id,
            "name": document.get("name"),
            "description": document.get("description"),
            "benefits": document.get("benefits"),
            "documents": document.get("documents"),
            "application": document.get("application"),
            "sources": document.get("sources"),
            "score": retrieved.get("score"),
            "decision": decision.value,
            "missing_attributes": missing_attributes
        })

    return results
