
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "intfloat/multilingual-e5-base"

model = SentenceTransformer(MODEL_NAME)

query = (
    "query: government financial assistance and self-employment "
    "loans for unemployed youth starting a small business in Tamil Nadu"
)

documents = [
    (
        "TN-UWWB-MAR-001",
        "passage: Marriage assistance for registered unorganised "
        "workers or their children."
    ),
    (
        "TN-PP-001",
        "passage: Monthly financial support for eligible girl "
        "students pursuing higher education in Tamil Nadu."
    ),
    (
        "TN-DA-UA-001",
        "passage: Monthly unemployment allowance for differently "
        "abled persons registered with the Employment Exchange."
    ),
    (
        "EXAMPLE-SELF-EMPLOYMENT",
        "passage: Financial assistance and loans for unemployed "
        "youth to start small businesses and become self-employed."
    ),
]

query_embedding = model.encode(
    [query],
    convert_to_numpy=True,
    normalize_embeddings=True,
)

document_embeddings = model.encode(
    [text for _, text in documents],
    convert_to_numpy=True,
    normalize_embeddings=True,
)

scores = cosine_similarity(query_embedding, document_embeddings)[0]

for (scheme_id, _), score in sorted(
    zip(documents, scores),
    key=lambda item: item[1],
    reverse=True,
):
    print(f"{scheme_id}: {score:.4f}")
