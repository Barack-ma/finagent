from uuid import UUID

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class Customer(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr