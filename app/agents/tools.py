from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.rag.retriever import PolicyRetriever
from app.schemas.payment import PaymentCreate
from app.services.loan_service import get_loan_by_id
from app.services.payment_service import create_payment
from app.services.summary_service import (
    get_customer_summary,
    get_loan_payoff_summary,
)


policy_retriever = PolicyRetriever()


def tool_get_customer_summary(
    db: Session,
    customer_id: str,
) -> dict:
    summary = get_customer_summary(
        db,
        UUID(customer_id),
    )

    return {
        "customer_id": str(summary.customer_id),
        "total_outstanding_balance": str(
            summary.total_outstanding_balance
        ),
        "active_loan_count": summary.active_loan_count,
        "weighted_average_interest_rate": str(
            summary.weighted_average_interest_rate
        ),
        "estimated_monthly_interest": str(
            summary.estimated_monthly_interest
        ),
    }


def tool_get_loan(
    db: Session,
    loan_id: str,
) -> dict:
    loan = get_loan_by_id(
        db,
        UUID(loan_id),
    )

    if loan is None:
        return {
            "error": "loan_not_found"
        }

    return {
        "id": str(loan.id),
        "customer_id": str(loan.customer_id),
        "loan_type": loan.loan_type.value,
        "principal_balance": str(
            loan.principal_balance
        ),
        "interest_rate": str(
            loan.interest_rate
        ),
        "status": loan.status.value,
    }


def tool_get_payoff_estimate(
    db: Session,
    loan_id: str,
) -> dict:
    payoff = get_loan_payoff_summary(
        db,
        UUID(loan_id),
    )

    return {
        "loan_id": str(payoff.loan_id),
        "principal_balance": str(
            payoff.principal_balance
        ),
        "annual_interest_rate": str(
            payoff.annual_interest_rate
        ),
        "estimated_monthly_interest": str(
            payoff.estimated_monthly_interest
        ),
        "estimated_payoff_amount": str(
            payoff.estimated_payoff_amount
        ),
    }


def tool_search_policy(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    results = policy_retriever.search(
        query=query,
        top_k=top_k,
    )

    return [
        {
            "source": result.source,
            "chunk_id": result.chunk_id,
            "text": result.text,
            "score": result.score,
        }
        for result in results
    ]


def tool_make_payment(
    db: Session,
    loan_id: str,
    amount: str,
) -> dict:
    payment = create_payment(
        db,
        UUID(loan_id),
        PaymentCreate(
            amount=Decimal(amount)
        ),
    )

    return {
        "payment_id": str(payment.id),
        "loan_id": str(payment.loan_id),
        "amount": str(payment.amount),
        "created_at": payment.created_at.isoformat(),
    }