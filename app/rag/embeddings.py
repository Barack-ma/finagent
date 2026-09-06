import numpy as np
from sentence_transformers import SentenceTransformer

# Turning text into vectors

_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def embed_text(text: str) -> np.ndarray:
    embedding = _model.encode(
        text,
        normalize_embeddings=True,
    )

    return np.asarray(
        embedding,
        dtype=np.float32,
    )


def embed_texts(
    texts: list[str],
) -> np.ndarray:
    embeddings = _model.encode(
        texts,
        normalize_embeddings=True,
    )

    return np.asarray(
        embeddings,
        dtype=np.float32,
    )