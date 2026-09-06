from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.summary import CustomerSummary, LoanPayoffSummary
from app.services.summary_service import (
    CustomerNotFoundError,
    LoanNotFoundError,
    get_customer_summary,
    get_loan_payoff_summary,
)


router = APIRouter(
    tags=["summaries"],
)


@router.get(
    "/customers/{customer_id}/summary",
    response_model=CustomerSummary,
)
def get_customer_summary_endpoint(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return get_customer_summary(
            db,
            customer_id,
        )

    except CustomerNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )


@router.get(
    "/loans/{loan_id}/payoff",
    response_model=LoanPayoffSummary,
)
def get_loan_payoff_endpoint(
    loan_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return get_loan_payoff_summary(
            db,
            loan_id,
        )

    except LoanNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found",
        )