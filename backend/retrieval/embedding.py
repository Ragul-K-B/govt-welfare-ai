from sentence_transformers import SentenceTransformer


MODEL_NAME = "intfloat/multilingual-e5-base"

model = SentenceTransformer(MODEL_NAME)


def create_embedding(text: str):
    return model.encode(text)