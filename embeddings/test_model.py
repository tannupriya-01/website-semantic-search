from embeddings.model import get_embedding
text = "How can I delete my account?"
embedding = get_embedding(text)
print("Embedding Dimension:", len(embedding))
print("First 10 values:")
print(embedding[:10])