from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_payment_rejects_zero_amount():
    response = client.post(
        "/loans/11111111-1111-1111-1111-111111111111/payments",
        json={
            "amount": 0
        },
    )

    assert response.status_code == 422


def test_payment_rejects_negative_amount():
    response = client.post(
        "/loans/11111111-1111-1111-1111-111111111111/payments",
        json={
            "amount": -500
        },
    )

    assert response.status_code == 422