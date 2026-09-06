from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.loan import LoanModel
from app.schemas.loan import LoanCreate, LoanStatus


def create_loan(
    db: Session,
    customer_id: UUID,
    loan_data: LoanCreate,
) -> LoanModel:
    loan = LoanModel(
        customer_id=customer_id,
        loan_type=loan_data.loan_type,
        principal_balance=loan_data.principal_balance,
        interest_rate=loan_data.interest_rate,
        status=LoanStatus.active,
    )

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan


def get_loans_by_customer(
    db: Session,
    customer_id: UUID,
) -> list[LoanModel]:
    statement = (
        select(LoanModel)
        .where(LoanModel.customer_id == customer_id)
    )

    return list(
        db.scalars(statement).all()
    )


def get_loan_by_id(
    db: Session,
    loan_id: UUID,
) -> LoanModel | None:
    return db.get(LoanModel, loan_id)