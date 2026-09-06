from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.payment import Payment, PaymentCreate
from app.services.payment_service import (
    LoanAlreadyPaidOffError,
    LoanNotFoundError,
    PaymentExceedsBalanceError,
    create_payment,
    get_payments_by_loan,
)


router = APIRouter(
    tags=["payments"],
)


@router.post(
    "/loans/{loan_id}/payments",
    response_model=Payment,
    status_code=status.HTTP_201_CREATED,
)
def create_payment_endpoint(
    loan_id: UUID,
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_payment(
            db,
            loan_id,
            payment_data,
        )

    except LoanNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found",
        )

    except LoanAlreadyPaidOffError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Loan is already paid off",
        )

    except PaymentExceedsBalanceError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Payment amount exceeds remaining loan balance",
        )


@router.get(
    "/loans/{loan_id}/payments",
    response_model=list[Payment],
)
def get_payments_endpoint(
    loan_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return get_payments_by_loan(
            db,
            loan_id,
        )

    except LoanNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found",
        )