
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from retrieval.prepare_documents import get_scheme_documents

MODEL_NAME = "intfloat/multilingual-e5-base"

query = (
    "query: government financial assistance and self-employment "
    "loans for unemployed youth starting a small business in Tamil Nadu"
)

schemes = get_scheme_documents()
model = SentenceTransformer(MODEL_NAME)

query_embedding = model.encode(
    [query],
    convert_to_numpy=True,
    normalize_embeddings=True,
)

texts = [
    f"passage: {scheme['text']}"
    for scheme in schemes
]

document_embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
    batch_size=16,
    show_progress_bar=True,
)

scores = cosine_similarity(
    query_embedding,
    document_embeddings,
)[0]

ranked = sorted(
    zip(schemes, scores),
    key=lambda item: item[1],
    reverse=True,
)

for rank, (scheme, score) in enumerate(ranked, start=1):
    print(
        f"{rank:02}. {scheme['scheme_id']} "
        f"(score: {score:.4f}) - {scheme['text'].splitlines()[1]}"
    )
