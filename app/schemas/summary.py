from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CustomerSummary(BaseModel):
    customer_id: UUID
    total_outstanding_balance: Decimal
    active_loan_count: int
    weighted_average_interest_rate: Decimal
    estimated_monthly_interest: Decimal


class LoanPayoffSummary(BaseModel):
    loan_id: UUID
    principal_balance: Decimal
    annual_interest_rate: Decimal
    estimated_monthly_interest: Decimal
    estimated_payoff_amount: Decimal

# Customers dont send these, we calculate them