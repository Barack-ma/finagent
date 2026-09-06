from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    amount: Decimal = Field(gt=0)


class Payment(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    loan_id: UUID
    amount: Decimal
    created_at: datetime