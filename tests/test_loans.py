from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_loan_rejects_negative_balance():
    response = client.post(
        "/customers/11111111-1111-1111-1111-111111111111/loans",
        json={
            "loan_type": "mortgage",
            "principal_balance": -1000,
            "interest_rate": 6.5,
        },
    )

    assert response.status_code == 422


def test_create_loan_rejects_invalid_type():
    response = client.post(
        "/customers/11111111-1111-1111-1111-111111111111/loans",
        json={
            "loan_type": "spaceship",
            "principal_balance": 1000,
            "interest_rate": 6.5,
        },
    )

    assert response.status_code == 422