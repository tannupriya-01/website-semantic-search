from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("Embedding model loaded successfully!")

def get_embedding(text):
    "Encode one text & return a numpy vector."
    return model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

def get_embeddings(texts):
    "Encode multiple texts together (batch encoding) & return a numpy array."
    return model.encode(
        texts,
        batch_size=32,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )