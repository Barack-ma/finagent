from app.rag.retriever import PolicyRetriever


def test_late_fee_query_retrieves_policy():
    retriever = PolicyRetriever()

    results = retriever.search(
        "Can the system waive my late fee?",
        top_k=3,
    )

    sources = {
        result.source
        for result in results
    }

    assert "late_payments.txt" in sources


def test_payment_query_retrieves_payment_policy():
    retriever = PolicyRetriever()

    results = retriever.search(
        "Can I pay more than the remaining balance?",
        top_k=3,
    )

    sources = {
        result.source
        for result in results
    }

    assert "payment_processing.txt" in sources