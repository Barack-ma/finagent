from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr

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


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate):
    # FastAPI takes the JSON request body
    # Turns into CustomerCreate object
    return {
        "message": "Customer created successfully",
        "customer": customer,
    }

# FastAPI mental model
# GET     → retrieve something
# POST    → create something
# PUT     → replace something
# PATCH   → modify something
# DELETE  → remove something