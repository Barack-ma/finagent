from uuid import UUID, uuid4

from app.schemas.customer import Customer, CustomerCreate


customers: dict[UUID, Customer] = {}


def create_customer(customer_data: CustomerCreate) -> Customer:
    customer = Customer(
        id=uuid4(),
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
        email=customer_data.email,
    )

    customers[customer.id] = customer

    return customer


def get_all_customers() -> list[Customer]:
    return list(customers.values())


def get_customer_by_id(customer_id: UUID) -> Customer | None:
    # Given an ID, return a customer if one exist, otherwise return None
    return customers.get(customer_id)

# This only knows the application logic