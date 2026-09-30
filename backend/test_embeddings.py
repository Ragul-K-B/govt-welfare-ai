from retrieval.embedding import create_embedding


text = "Tamil Nadu scholarship for college students"

embedding = create_embedding(text)

print("Embedding type:", type(embedding))
print("Embedding shape:", embedding.shape)
print("First 10 values:", embedding[:10])