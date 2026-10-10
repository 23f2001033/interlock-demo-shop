import pytest

from shop.cart import Cart
from shop.pricing import fee_for, quote, shipping_for, tax_for


def test_flat_shipping_below_threshold():
    assert shipping_for(49.99) == 5.00


def test_free_shipping_at_threshold():
    assert shipping_for(50.00) == 0.0


def test_tax_is_rounded_to_cents():
    assert tax_for(39.98, "US-CA") == 2.90
    assert tax_for(9.95, "EU-DE") == 1.89


def test_unsupported_region():
    with pytest.raises(ValueError):
        tax_for(10.0, "XX-00")


def test_quote_breakdown():
    cart = Cart()
    cart.add("TEE-01", 2)
    assert quote(cart, "US-CA") == {
        "subtotal": 39.98,
        "shipping": 5.00,
        "fee": 0.0,
        "tax": 2.90,
        "total": 47.88,
    }


def test_quote_with_free_shipping():
    cart = Cart()
    cart.add("MUG-01", 4)
    q = quote(cart, "US-NY")
    assert q["shipping"] == 0.0
    assert q["total"] == 52.00


def test_small_order_fee_below_threshold():
    assert fee_for(14.99) == 1.50


def test_no_small_order_fee_at_threshold():
    assert fee_for(15.00) == 0.0


def test_quote_with_small_order_fee():
    cart = Cart()
    cart.add("BAG-01")
    assert quote(cart, "EU-DE") == {
        "subtotal": 9.95,
        "shipping": 5.00,
        "fee": 1.50,
        "tax": 1.89,  # tax is on the subtotal only, not the fee
        "total": 18.34,
    }
