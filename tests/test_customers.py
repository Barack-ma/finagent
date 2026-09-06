from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_customer_rejects_invalid_email():
    response = client.post(
        "/customers",
        json={
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "not-an-email",
        },
    )

    assert response.status_code == 422