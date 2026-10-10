import pytest

from shop.payments import PaymentGateway


def test_charge_defaults_to_usd():
    gateway = PaymentGateway()
    gateway.charge("cus_1", 500)
    assert gateway.charges[0].currency == "USD"


def test_charge_records_explicit_currency():
    gateway = PaymentGateway()
    gateway.charge("cus_1", 500, currency="EUR")
    gateway.charge("cus_1", 700, "GBP")
    assert [c.currency for c in gateway.charges] == ["EUR", "GBP"]


@pytest.mark.parametrize("currency", ["usd", "US", "USDX", "", "U$D", None])
def test_charge_rejects_invalid_currency(currency):
    gateway = PaymentGateway()
    with pytest.raises(ValueError):
        gateway.charge("cus_1", 500, currency)
    assert gateway.charges == []
