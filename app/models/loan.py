import uuid
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.schemas.loan import LoanStatus, LoanType


class LoanModel(Base):
    __tablename__ = "loans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        # Ensures every loan must reference a real customer
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )

    loan_type: Mapped[LoanType] = mapped_column(
        Enum(LoanType, name="loan_type_enum"),
        nullable=False,
    )

    principal_balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    interest_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    status: Mapped[LoanStatus] = mapped_column(
        Enum(LoanStatus, name="loan_status_enum"),
        nullable=False,
        default=LoanStatus.active,
    )