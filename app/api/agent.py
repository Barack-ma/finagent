from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agents.finagent import run_finagent
from app.core.database import get_db
from app.schemas.agent import (
    AgentRequest,
    AgentResponse,
)


router = APIRouter(
    prefix="/agent",
    tags=["agent"],
)


@router.post(
    "/chat",
    response_model=AgentResponse,
)
def chat_with_agent(
    request: AgentRequest,
    db: Session = Depends(get_db),
):
    response = run_finagent(
        db,
        request.message,
    )

    return AgentResponse(
        response=response
    )