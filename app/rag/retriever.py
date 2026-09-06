from dataclasses import dataclass

import numpy as np

from app.rag.chunking import (
    PolicyChunk,
    chunk_documents,
)
from app.rag.document_loader import (
    load_policy_documents,
)
from app.rag.embeddings import (
    embed_text,
    embed_texts,
)


@dataclass
class RetrievalResult:
    source: str
    chunk_id: int
    text: str
    score: float


class PolicyRetriever:
    def __init__(self):
        documents = load_policy_documents()

        self.chunks: list[PolicyChunk] = (
            chunk_documents(documents)
        )

        texts = [
            chunk.text
            for chunk in self.chunks
        ]

        self.embeddings = embed_texts(texts)

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievalResult]:
        query_embedding = embed_text(query)

        scores = (
            self.embeddings
            @ query_embedding
            # Dot product here gives us a similarity score
        )

        top_indices = np.argsort(scores)[::-1][:top_k]

        results: list[RetrievalResult] = []

        for index in top_indices:
            chunk = self.chunks[index]

            results.append(
                RetrievalResult(
                    source=chunk.source,
                    chunk_id=chunk.chunk_id,
                    text=chunk.text,
                    score=float(scores[index]),
                )
            )

        return results