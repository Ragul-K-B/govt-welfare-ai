from db.mongodb import schemes_collection


def build_scheme_text(scheme: dict) -> str:
    """
    Convert a MongoDB scheme document into searchable text.
    """

    return f"""
Scheme: {scheme.get("name", "")}

Description: {scheme.get("description", "")}

Benefits: {scheme.get("benefits", "")}

Eligibility: {scheme.get("eligibility", "")}

Documents: {scheme.get("documents", "")}

Application: {scheme.get("application", "")}
""".strip()


def get_scheme_documents():
    """
    Retrieve schemes from MongoDB and prepare them for embedding.
    """

    schemes = []

    for scheme in schemes_collection.find():
        scheme_text = build_scheme_text(scheme)

        schemes.append({
            "scheme_id": scheme["scheme_id"],
            "text": scheme_text
        })

    return schemes