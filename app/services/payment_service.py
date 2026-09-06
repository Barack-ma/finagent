from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.loan import LoanModel
from app.models.payment import PaymentModel
from app.schemas.loan import LoanStatus
from app.schemas.payment import PaymentCreate


class LoanNotFoundError(Exception):
    pass


class PaymentExceedsBalanceError(Exception):
    pass


class LoanAlreadyPaidOffError(Exception):
    pass

def create_payment(
    db: Session,
    loan_id: UUID,
    payment_data: PaymentCreate,
) -> PaymentModel:
    loan = db.get(LoanModel, loan_id)

    if loan is None:
        raise LoanNotFoundError

    if loan.status == LoanStatus.paid_off:
        raise LoanAlreadyPaidOffError

    amount = payment_data.amount

    if amount > loan.principal_balance:
        raise PaymentExceedsBalanceError

    payment = PaymentModel(
        loan_id=loan.id,
        amount=amount,
    )

    loan.principal_balance -= amount

    if loan.principal_balance == Decimal("0.00"):
        loan.status = LoanStatus.paid_off

    db.add(payment)

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise

    db.refresh(payment)
    db.refresh(loan)

    return payment


def get_payments_by_loan(
    db: Session,
    loan_id: UUID,
) -> list[PaymentModel]:
    loan = db.get(LoanModel, loan_id)

    if loan is None:
        raise LoanNotFoundError

    statement = (
        select(PaymentModel)
        .where(PaymentModel.loan_id == loan_id)
        .order_by(PaymentModel.created_at.desc())
    )

    return list(
        db.scalars(statement).all()
    )