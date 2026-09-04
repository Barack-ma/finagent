from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class Customer(BaseModel):
    model_config = ConfigDict(
        # Building a response from attributes on an ORM object
        from_attributes=True
    )

    id: UUID
    first_name: str
    last_name: str
    email: EmailStr