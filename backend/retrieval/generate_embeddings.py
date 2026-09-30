import numpy as np
from sentence_transformers import SentenceTransformer

from retrieval.prepare_documents import get_scheme_documents


MODEL_NAME = "intfloat/multilingual-e5-base"


def main():
    # Load the embedding model
    model = SentenceTransformer(MODEL_NAME)

    # Get scheme IDs and searchable text from MongoDB
    schemes = get_scheme_documents()

    print("Number of schemes:", len(schemes))

    # E5 models use "passage:" for documents being indexed
    texts = [
        f"passage: {scheme['text']}"
        for scheme in schemes
    ]

    # Generate embeddings
    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    print("Embedding shape:", embeddings.shape)

    # Keep the mapping between each vector and its scheme ID
    scheme_ids = [
        scheme["scheme_id"]
        for scheme in schemes
    ]

    print("Number of scheme IDs:", len(scheme_ids))

    # Verify expected dimensions
    expected_schemes = 31
    expected_dimensions = 768

    assert embeddings.shape == (
        expected_schemes,
        expected_dimensions
    ), (
        f"Expected ({expected_schemes}, {expected_dimensions}) "
        f"but got {embeddings.shape}"
    )

    assert len(scheme_ids) == expected_schemes, (
        f"Expected {expected_schemes} scheme IDs "
        f"but got {len(scheme_ids)}"
    )

    print("Embedding verification: PASSED")
    print(f"{expected_schemes} schemes × {expected_dimensions} dimensions")

    # Show a few mappings so we can verify everything
    print("\nFirst 3 scheme mappings:")

    for i in range(min(3, len(scheme_ids))):
        print(
            f"Vector {i} → {scheme_ids[i]}"
        )

    # Show the first few values of the first embedding
    print("\nFirst 10 values of first embedding:")
    print(embeddings[0][:10])


if __name__ == "__main__":
    main()

