from fastapi import APIRouter

from app.rag.retriever import PolicyRetriever
from app.schemas.policy import (
    PolicySearchRequest,
    PolicySearchResult,
)


router = APIRouter(
    prefix="/policies",
    tags=["policies"],
)


retriever = PolicyRetriever()


@router.post(
    "/search",
    response_model=list[PolicySearchResult],
)
def search_policies(
    request: PolicySearchRequest,
):
    results = retriever.search(
        query=request.query,
        top_k=request.top_k,
    )

    return [
        PolicySearchResult(
            source=result.source,
            chunk_id=result.chunk_id,
            text=result.text,
            score=result.score,
        )
        for result in results
    ]