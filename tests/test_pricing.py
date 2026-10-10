import pytest

from shop.cart import Cart
from shop.pricing import discount_for, quote, shipping_for, tax_for


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
        "discount": 0.0,
        "shipping": 5.00,
        "tax": 2.90,
        "total": 47.88,
    }


def test_quote_with_free_shipping():
    cart = Cart()
    cart.add("MUG-01", 4)
    q = quote(cart, "US-NY")
    assert q["shipping"] == 0.0
    assert q["total"] == 52.00


def test_save10_takes_ten_percent_at_minimum():
    assert discount_for(40.00, "SAVE10") == 4.00
    assert discount_for(123.45, "SAVE10") == 12.35


def test_save10_does_nothing_below_minimum():
    assert discount_for(39.99, "SAVE10") == 0.0


def test_no_code_means_no_discount():
    assert discount_for(100.00, None) == 0.0


def test_unknown_discount_code():
    with pytest.raises(ValueError):
        discount_for(100.00, "SAVE99")


def test_quote_with_save10_taxes_discounted_subtotal():
    cart = Cart()
    cart.add("MUG-01", 2)
    cart.add("CAP-01")
    assert quote(cart, "US-CA", "SAVE10") == {
        "subtotal": 40.00,
        "discount": 4.00,
        "shipping": 5.00,
        "tax": 2.61,  # 7.25% of 36.00
        "total": 43.61,
    }


def test_quote_with_save10_below_minimum():
    cart = Cart()
    cart.add("TEE-01", 2)
    q = quote(cart, "US-CA", "SAVE10")
    assert q["discount"] == 0.0
    assert q["total"] == 47.88


def test_quote_with_unknown_code():
    cart = Cart()
    cart.add("MUG-01", 4)
    with pytest.raises(ValueError):
        quote(cart, "US-NY", "BOGUS")
