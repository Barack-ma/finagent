from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.loan import Loan, LoanCreate
from app.services.customer_service import get_customer_by_id
from app.services.loan_service import (
    create_loan,
    get_loan_by_id,
    get_loans_by_customer,
)


router = APIRouter(
    tags=["loans"],
)


@router.post(
    "/customers/{customer_id}/loans",
    response_model=Loan,
    status_code=status.HTTP_201_CREATED,
)
def create_loan_endpoint(
    customer_id: UUID,
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
):
    customer = get_customer_by_id(
        db,
        customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return create_loan(
        db,
        customer_id,
        loan_data,
    )


@router.get(
    "/customers/{customer_id}/loans",
    response_model=list[Loan],
)
def get_customer_loans_endpoint(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    customer = get_customer_by_id(
        db,
        customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return get_loans_by_customer(
        db,
        customer_id,
    )


@router.get(
    "/loans/{loan_id}",
    response_model=Loan,
)
def get_loan_endpoint(
    loan_id: UUID,
    db: Session = Depends(get_db),
):
    loan = get_loan_by_id(
        db,
        loan_id,
    )

    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found",
        )

    return loan