import pickle
import faiss
import numpy as np
from embeddings.model import get_embedding

print("Loading FAISS index...")
index = faiss.read_index("embeddings/faiss.index")
print("FAISS loaded.")

print("Loading metadata...")

with open("embeddings/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

print(f"Loaded {len(metadata)} chunks")

def semantic_search(query , top_k=300):

    query_vector = get_embedding(query)
    query_vector = np.array([query_vector]).astype("float32")
    distances, indices = index.search(query_vector, top_k)
    results = []
    query_words = set(query.lower().split())
    scored_results = []
    
    for rank, idx in enumerate(indices[0]):
        if idx == -1:
            continue

        item = metadata[idx]

        text = item.get("content", "").lower()
        query_lower = query.lower()
        exact_phrase = query_lower in text

        keyword_matches = sum(
            1 
            for word in query_words
            if word in text
        )

        distance = distances[0][rank]
        score = -distance * 100

        if exact_phrase:
            score += 1000

        score += keyword_matches * 20
        final_score = score

        scored_results.append((final_score, item))

    scored_results.sort(key=lambda x: x[0], reverse=True)
    seen_urls = set()
    results = []

    for _, item in scored_results:
        if item["url"] not in seen_urls:
            seen_urls.add(item["url"])
            results.append(item)

    return results