from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr

from uuid import UUID, uuid4

app = FastAPI(
    title="FinAgent API",
    description="AI-powered lending operations agent",
    version="0.1.0",
)


class CustomerCreate(BaseModel):
    # A valid customer must have personal details
    first_name: str
    last_name: str
    email: EmailStr

class Customer(BaseModel):
    id: UUID  # Unique identifier for the customer
    first_name: str
    last_name: str
    email: EmailStr

customers: dict[UUID, Customer] = {}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/customers",
    status_code=status.HTTP_201_CREATED
)
def create_customer(customer_data: CustomerCreate):
    customer = Customer(
        id=uuid4(),
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
        email=customer_data.email,
    )

    customers[customer.id] = customer

    return customer


@app.get("/customers", response_model=list[Customer])
def get_customers():
    return list(customers.values())


@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: UUID):
    customer = customers.get(customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer

"""
FastAPI mental model
GET     → retrieve something
POST    → create something
PUT     → replace something
PATCH   → modify something
DELETE  → remove something


schemas/
    What does the data look like?

services/
    What does the application do with the data?

api/
    Which HTTP endpoints expose that behavior?

main.py
    Assemble the application.
"""