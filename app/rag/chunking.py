from dataclasses import dataclass

from app.rag.document_loader import PolicyDocument

@dataclass
class PolicyChunk:
    source: str
    chunk_id: int
    text: str

def chunk_document(
    document: PolicyDocument,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[PolicyChunk]:
    chunks: list[PolicyChunk] = []

    start = 0
    chunk_id = 0

    while start < len(document.text):
        end = start + chunk_size

        chunk_text = document.text[start:end].strip()

        if chunk_text:
            chunks.append(
                PolicyChunk(
                    source=document.source,
                    chunk_id=chunk_id,
                    text=chunk_text,
                )
            )

        chunk_id += 1

        start += chunk_size - overlap

    return chunks


def chunk_documents(
    documents: list[PolicyDocument],
) -> list[PolicyChunk]:
    chunks: list[PolicyChunk] = []

    for document in documents:
        chunks.extend(
            chunk_document(document)
        )

    return chunks