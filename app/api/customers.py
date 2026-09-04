from fastapi import FastAPI

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.customer import Customer, CustomerCreate
from app.services.customer_service import (
    create_customer,
    get_all_customers,
    get_customer_by_id,
)


router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.post(
    "",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
)
def create_customer_endpoint(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
):
    return create_customer(db, customer_data)


@router.get(
    "",
    response_model=list[Customer],
)
def get_customers_endpoint(
    db: Session = Depends(get_db),
):
    return get_all_customers(db)


@router.get(
    "/{customer_id}",
    response_model=Customer,
)
def get_customer_endpoint(
    customer_id: UUID,
    db: Session = Depends(get_db),
):
    customer = get_customer_by_id(
        db,
        customer_id,
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer

"""
Create app
    ↓
attach routers
    ↓
define basic infrastructure endpoints
"""