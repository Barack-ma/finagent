from decimal import Decimal

from app.services.summary_service import calculate_monthly_interest


def test_calculate_monthly_interest():
    result = calculate_monthly_interest(
        principal_balance=Decimal("10000.00"),
        annual_interest_rate=Decimal("6.00"),
    )

    assert result == Decimal("50.00")

def test_zero_interest_rate():
    result = calculate_monthly_interest(
        principal_balance=Decimal("10000.00"),
        annual_interest_rate=Decimal("0.00"),
    )

    assert result == Decimal("0.00")