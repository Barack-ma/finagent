from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import CustomerModel
from app.models.loan import LoanModel
from app.schemas.loan import LoanStatus
from app.schemas.summary import CustomerSummary, LoanPayoffSummary


MONEY_QUANTIZER = Decimal("0.01")
RATE_QUANTIZER = Decimal("0.01")


class CustomerNotFoundError(Exception):
    pass


class LoanNotFoundError(Exception):
    pass


def calculate_monthly_interest(
    principal_balance: Decimal,
    annual_interest_rate: Decimal,
) -> Decimal:
    monthly_rate = annual_interest_rate / Decimal("100") / Decimal("12")

    monthly_interest = principal_balance * monthly_rate

    return monthly_interest.quantize(
        MONEY_QUANTIZER,
        rounding=ROUND_HALF_UP,
    )


def get_customer_summary(
    db: Session,
    customer_id: UUID,
) -> CustomerSummary:
    customer = db.get(CustomerModel, customer_id)

    if customer is None:
        raise CustomerNotFoundError

    statement = (
        select(LoanModel)
        .where(
            LoanModel.customer_id == customer_id,
            LoanModel.status == LoanStatus.active,
        )
    )

    loans = list(db.scalars(statement).all())

    if not loans:
        return CustomerSummary(
            customer_id=customer_id,
            total_outstanding_balance=Decimal("0.00"),
            active_loan_count=0,
            weighted_average_interest_rate=Decimal("0.00"),
            estimated_monthly_interest=Decimal("0.00"),
        )

    total_balance = sum(
        (loan.principal_balance for loan in loans),
        Decimal("0.00"),
    )

    weighted_rate_numerator = sum(
        (
            loan.principal_balance * loan.interest_rate
            for loan in loans
        ),
        Decimal("0.00"),
    )

    weighted_average_rate = (
        weighted_rate_numerator / total_balance
    ).quantize(
        RATE_QUANTIZER,
        rounding=ROUND_HALF_UP,
    )

    monthly_interest = sum(
        (
            calculate_monthly_interest(
                loan.principal_balance,
                loan.interest_rate,
            )
            for loan in loans
        ),
        Decimal("0.00"),
    )

    return CustomerSummary(
        customer_id=customer_id,
        total_outstanding_balance=total_balance.quantize(
            MONEY_QUANTIZER
        ),
        active_loan_count=len(loans),
        weighted_average_interest_rate=weighted_average_rate,
        estimated_monthly_interest=monthly_interest.quantize(
            MONEY_QUANTIZER
        ),
    )


def get_loan_payoff_summary(
    db: Session,
    loan_id: UUID,
) -> LoanPayoffSummary:
    loan = db.get(LoanModel, loan_id)

    if loan is None:
        raise LoanNotFoundError

    monthly_interest = calculate_monthly_interest(
        loan.principal_balance,
        loan.interest_rate,
    )

    estimated_payoff_amount = (
        loan.principal_balance + monthly_interest
    ).quantize(
        MONEY_QUANTIZER,
        rounding=ROUND_HALF_UP,
    )

    return LoanPayoffSummary(
        loan_id=loan.id,
        principal_balance=loan.principal_balance,
        annual_interest_rate=loan.interest_rate,
        estimated_monthly_interest=monthly_interest,
        estimated_payoff_amount=estimated_payoff_amount,
    )