from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.customer import CustomerModel
from app.schemas.customer import CustomerCreate


class DuplicateCustomerEmailError(Exception):
    pass


def create_customer(
    db: Session,
    customer_data: CustomerCreate,
) -> CustomerModel:
    customer = CustomerModel(
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
        email=str(customer_data.email),
    )

    db.add(customer)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateCustomerEmailError

    db.refresh(customer)

    return customer


def get_all_customers(
    db: Session,
) -> list[CustomerModel]:
    statement = select(CustomerModel)
    return list(db.scalars(statement).all())


def get_customer_by_id(
    db: Session,
    customer_id: UUID,
) -> CustomerModel | None:
    return db.get(CustomerModel, customer_id)