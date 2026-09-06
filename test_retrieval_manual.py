from app.rag.retriever import PolicyRetriever


retriever = PolicyRetriever()

results = retriever.search(
    "Can the I make a payment larger than my balance?",
    top_k=3,
)

for result in results:
    print(
        f"{result.source} "
        f"(score={result.score:.3f})"
    )
    print(result.text)
    print("-" * 80)