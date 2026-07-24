from embeddings.search import semantic_search

results = semantic_search("delete account")

for r in results:
    print("=" * 80)
    print(r["url"])
    print()
    print(r["content"][:500])