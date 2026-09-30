
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from retrieval.prepare_documents import get_scheme_documents


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL_NAME = "intfloat/multilingual-e5-base"

EXPECTED_SCHEMES = 31
EMBEDDING_DIMENSION = 768

# Directory where the FAISS index and mapping will be stored
DATA_DIR = Path(__file__).parent / "data"

INDEX_PATH = DATA_DIR / "schemes.index"
MAPPING_PATH = DATA_DIR / "scheme_ids.json"


# --------------------------------------------------
# Build FAISS index
# --------------------------------------------------

def main():

    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # ----------------------------------------------
    # 1. Load schemes from MongoDB
    # ----------------------------------------------

    schemes = get_scheme_documents()

    print("Number of schemes:", len(schemes))

    if len(schemes) != EXPECTED_SCHEMES:
        raise ValueError(
            f"Expected {EXPECTED_SCHEMES} schemes, "
            f"but found {len(schemes)}"
        )

    # ----------------------------------------------
    # 2. Prepare text for E5
    # ----------------------------------------------

    texts = [
        f"passage: {scheme['text']}"
        for scheme in schemes
    ]

    # ----------------------------------------------
    # 3. Load embedding model
    # ----------------------------------------------

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    # ----------------------------------------------
    # 4. Generate embeddings
    # ----------------------------------------------

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    print("Embedding shape:", embeddings.shape)

    # ----------------------------------------------
    # 5. Verify embedding dimensions
    # ----------------------------------------------

    if embeddings.shape != (
        EXPECTED_SCHEMES,
        EMBEDDING_DIMENSION
    ):
        raise ValueError(
            f"Expected embeddings with shape "
            f"({EXPECTED_SCHEMES}, {EMBEDDING_DIMENSION}), "
            f"but got {embeddings.shape}"
        )

    # ----------------------------------------------
    # 6. Convert to float32
    # ----------------------------------------------

    embeddings = embeddings.astype(np.float32)

    # ----------------------------------------------
    # 7. Normalize vectors
    # ----------------------------------------------
    #
    # After normalization, inner product becomes
    # equivalent to cosine similarity.
    #

    faiss.normalize_L2(embeddings)

    # ----------------------------------------------
    # 8. Create FAISS index
    # ----------------------------------------------

    index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)

    # ----------------------------------------------
    # 9. Add embeddings to FAISS
    # ----------------------------------------------

    index.add(embeddings)

    print("FAISS index created.")
    print("Number of vectors:", index.ntotal)

    # ----------------------------------------------
    # 10. Create scheme ID mapping
    # ----------------------------------------------

    scheme_ids = [
        scheme["scheme_id"]
        for scheme in schemes
    ]

    # Make sure the mapping matches FAISS vectors
    if len(scheme_ids) != index.ntotal:
        raise ValueError(
            "Number of scheme IDs does not match "
            "number of FAISS vectors."
        )

    # ----------------------------------------------
    # 11. Save FAISS index
    # ----------------------------------------------

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    print(f"FAISS index saved to: {INDEX_PATH}")

    # ----------------------------------------------
    # 12. Save scheme ID mapping
    # ----------------------------------------------

    with open(
        MAPPING_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            scheme_ids,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Scheme ID mapping saved to: {MAPPING_PATH}")

    # ----------------------------------------------
    # 13. Final verification
    # ----------------------------------------------

    print("\nVerification:")
    print("------------------------------")
    print("Expected schemes :", EXPECTED_SCHEMES)
    print("FAISS vectors    :", index.ntotal)
    print("Embedding size   :", EMBEDDING_DIMENSION)
    print("Scheme IDs       :", len(scheme_ids))
    print("------------------------------")

    if (
        index.ntotal == EXPECTED_SCHEMES
        and len(scheme_ids) == EXPECTED_SCHEMES
    ):
        print("FAISS index verification: PASSED")


# --------------------------------------------------
# Entry point
# --------------------------------------------------

if __name__ == "__main__":
    main()

