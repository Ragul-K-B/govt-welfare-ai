import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL_NAME = "intfloat/multilingual-e5-base"

DATA_DIR = Path(__file__).parent / "data"

INDEX_PATH = DATA_DIR / "schemes.index"
MAPPING_PATH = DATA_DIR / "scheme_ids.json"


# --------------------------------------------------
# Load resources
# --------------------------------------------------

model = SentenceTransformer(MODEL_NAME)

index = faiss.read_index(str(INDEX_PATH))

with open(MAPPING_PATH, "r", encoding="utf-8") as file:
    scheme_ids = json.load(file)


# --------------------------------------------------
# Search function
# --------------------------------------------------

def search_schemes(query: str, top_k: int = 5):
    """
    Search the FAISS index using a natural-language query.
    """

    # E5 models use "query:" for search queries
    query_text = f"query: {query}"

    # Convert query into a 768-dimensional vector
    query_embedding = model.encode(
        [query_text],
        convert_to_numpy=True
    )

    # FAISS expects float32
    query_embedding = query_embedding.astype(np.float32)

    # Normalize for cosine similarity
    faiss.normalize_L2(query_embedding)

    # Search FAISS
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, index_position in zip(scores[0], indices[0]):

        # FAISS can return -1 when no result exists
        if index_position == -1:
            continue

        scheme_id = scheme_ids[index_position]

        results.append({
            "scheme_id": scheme_id,
            "score": float(score)
        })

    return results


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    query = input("\nEnter your query: ")

    results = search_schemes(query, top_k=5)

    print("\nSearch results:")
    print("------------------------------")

    for rank, result in enumerate(results, start=1):

        print(
            f"{rank}. "
            f"{result['scheme_id']} "
            f"(similarity: {result['score']:.4f})"
        )