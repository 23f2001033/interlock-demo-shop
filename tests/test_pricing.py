import pytest

from shop.cart import Cart
from shop.pricing import fee_for, quote, shipping_for, tax_for


def test_flat_shipping_below_threshold():
    assert shipping_for(4999) == 500


def test_free_shipping_at_threshold():
    assert shipping_for(5000) == 0


def test_tax_is_rounded_to_cents():
    assert tax_for(3998, "US-CA") == 290
    assert tax_for(995, "EU-DE") == 189


def test_tax_rounds_half_cents_up():
    # 200 x 0.0725 = 14.5 cents exactly; as floats it is 14.499999999999998.
    assert tax_for(200, "US-CA") == 15
    assert tax_for(10, "US-CA") == 1  # 0.725 cents


def test_unsupported_region():
    with pytest.raises(ValueError):
        tax_for(1000, "XX-00")


def test_quote_breakdown():
    cart = Cart()
    cart.add("TEE-01", 2)
    assert quote(cart, "US-CA") == {
        "subtotal": 3998,
        "shipping": 500,
        "fee": 0,
        "tax": 290,
        "total": 4788,
    }


def test_quote_amounts_are_int_cents():
    cart = Cart()
    cart.add("TEE-01", 3)
    cart.add("BAG-01")
    q = quote(cart, "IN-KA")
    assert all(type(v) is int for v in q.values())
    assert q["total"] == q["subtotal"] + q["shipping"] + q["fee"] + q["tax"]


def test_quote_with_free_shipping():
    cart = Cart()
    cart.add("MUG-01", 4)
    q = quote(cart, "US-NY")
    assert q["shipping"] == 0
    assert q["total"] == 5200


def test_small_order_fee_below_threshold():
    assert fee_for(1499) == 150


def test_no_small_order_fee_at_threshold():
    assert fee_for(1500) == 0


def test_quote_with_small_order_fee():
    cart = Cart()
    cart.add("BAG-01")
    assert quote(cart, "EU-DE") == {
        "subtotal": 995,
        "shipping": 500,
        "fee": 150,
        "tax": 189,  # tax is on the subtotal only, not the fee
        "total": 1834,
    }
