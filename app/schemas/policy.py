from pydantic import BaseModel, Field


class PolicySearchRequest(BaseModel):
    query: str = Field(
        min_length=3,
        max_length=500,
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
    )


class PolicySearchResult(BaseModel):
    source: str
    chunk_id: int
    text: str
    score: float