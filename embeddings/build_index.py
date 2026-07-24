import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
import faiss
import numpy as np
import pickle
from database import get_connection, get_all_scraped_pages
from embeddings.model import get_embeddings
from embeddings.utils import clean_markdown, chunk_text

def build_index():
    conn, cursor = get_connection()
    pages = get_all_scraped_pages(cursor)
    print(f"Found {len(pages)} pages")
    all_chunks = []
    metadata = []
    total_pages = len(pages)
    
    for i, page in enumerate(pages, start=1):

        print(f"Processing page {i}/{total_pages}")
        clean_text = clean_markdown(page["content"])
        chunks = chunk_text(clean_text)

        for chunk in chunks:
            slug = page["url"].rstrip("/").split("/")[-1]
            if slug:
                title = slug.replace("-", " ").replace("_", " ").title()
            else:
                title = "Home"
            embedding_text = f"""
        Title: {title}
        URL: {page["url"]}
        Content:
        {chunk}
        """

            all_chunks.append(embedding_text)
            words = re.findall(r"[A-Za-z]{4,}", clean_text.lower())

            stopwords = {
                "this","that","with","from","have","your","their",
                "about","which","there","would","could","should",
                "https","www","http","into","also","been","being",
                "than","when","where","while","what","will"
            }

            keywords = []

            for word in words:
                if word not in stopwords and word not in keywords:
                    keywords.append(word)

            keywords = keywords[:4]
            metadata.append(
                {
                    "id": page["id"],
                    "url": page["url"],
                    "title": title,
                    "summary": chunk, 
                    "content": chunk,
                    "keywords": keywords,
                    "embedding_text" : embedding_text
                }
            )
            
    print(f"\nTotal chunks: {len(all_chunks)}")
    print("Generating embeddings in batches...")
    embeddings = get_embeddings(all_chunks)
    print("Embedding generation completed!")
    embeddings = embeddings.astype("float32")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, "embeddings/faiss.index")

    with open("embeddings/metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("FAISS index created successfully!")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    build_index()