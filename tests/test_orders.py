import pytest

from shop.cart import Cart
from shop.orders import place_order
from shop.payments import PaymentGateway


def test_order_charges_total_in_cents():
    cart = Cart()
    cart.add("TEE-01", 2)
    gateway = PaymentGateway()
    order = place_order(cart, "cus_1", "US-CA", gateway)
    assert order.total == 47.88
    assert gateway.charges[0].amount_cents == 4788
    assert order.charge_id == gateway.charges[0].id


def test_order_lines_capture_prices():
    cart = Cart()
    cart.add("TEE-01", 2)
    order = place_order(cart, "cus_1", "US-CA", PaymentGateway())
    line = order.lines[0]
    assert (line.sku, line.qty, line.unit_price, line.line_total) == ("TEE-01", 2, 19.99, 39.98)


def test_empty_cart_cannot_be_ordered():
    with pytest.raises(ValueError):
        place_order(Cart(), "cus_1", "US-CA", PaymentGateway())


def test_order_with_save10_charges_discounted_total():
    cart = Cart()
    cart.add("MUG-01", 2)
    cart.add("CAP-01")
    gateway = PaymentGateway()
    order = place_order(cart, "cus_1", "US-CA", gateway, code="SAVE10")
    assert (order.subtotal, order.discount, order.tax, order.total) == (40.00, 4.00, 2.61, 43.61)
    assert gateway.charges[0].amount_cents == 4361


def test_order_with_unknown_code_is_not_charged():
    cart = Cart()
    cart.add("MUG-01", 4)
    gateway = PaymentGateway()
    with pytest.raises(ValueError):
        place_order(cart, "cus_1", "US-NY", gateway, code="BOGUS")
    assert gateway.charges == []


def test_gateway_tracks_totals_per_customer():
    gateway = PaymentGateway()
    for _ in range(2):
        cart = Cart()
        cart.add("BAG-01")
        place_order(cart, "cus_2", "EU-DE", gateway)
    assert gateway.total_charged("cus_2") == 2 * 1684
