from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LoanType(str, Enum):
    mortgage = "mortgage"
    auto = "auto"
    personal = "personal"
    student = "student"


class LoanStatus(str, Enum):
    active = "active"
    paid_off = "paid_off"
    delinquent = "delinquent"


class LoanCreate(BaseModel):
    loan_type: LoanType

    principal_balance: Decimal = Field(
        gt=0
    )

    interest_rate: Decimal = Field(
        ge=0,
        le=100,
    )


class Loan(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    customer_id: UUID

    loan_type: LoanType
    principal_balance: Decimal
    interest_rate: Decimal
    status: LoanStatus