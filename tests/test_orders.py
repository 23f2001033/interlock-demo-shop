import pytest

from shop.cart import Cart
from shop.orders import place_order
from shop.payments import PaymentGateway


def test_order_charges_total_in_cents():
    cart = Cart()
    cart.add("TEE-01", 2)
    gateway = PaymentGateway()
    order = place_order(cart, "cus_1", "US-CA", gateway)
    assert order.total == 4788
    assert gateway.charges[0].amount_cents == order.total
    assert order.charge_id == gateway.charges[0].id


def test_order_lines_capture_prices():
    cart = Cart()
    cart.add("TEE-01", 2)
    order = place_order(cart, "cus_1", "US-CA", PaymentGateway())
    line = order.lines[0]
    assert (line.sku, line.qty, line.unit_price, line.line_total) == ("TEE-01", 2, 1999, 3998)


def test_empty_cart_cannot_be_ordered():
    with pytest.raises(ValueError):
        place_order(Cart(), "cus_1", "US-CA", PaymentGateway())


def test_gateway_tracks_totals_per_customer():
    gateway = PaymentGateway()
    for _ in range(2):
        cart = Cart()
        cart.add("BAG-01")
        place_order(cart, "cus_2", "EU-DE", gateway)
    assert gateway.total_charged("cus_2") == 2 * 1684
