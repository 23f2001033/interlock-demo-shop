import pytest

from shop.cart import Cart


def test_subtotal_multiplies_price_by_quantity():
    cart = Cart()
    cart.add("TEE-01", 2)
    assert cart.subtotal() == 39.98


def test_adding_same_sku_accumulates_quantity():
    cart = Cart()
    cart.add("MUG-01")
    cart.add("MUG-01", 2)
    assert cart.lines() == [("MUG-01", 3)]
    assert cart.subtotal() == 37.50


def test_remove_drops_the_line():
    cart = Cart()
    cart.add("CAP-01")
    cart.remove("CAP-01")
    assert cart.is_empty()


def test_rejects_non_positive_quantity():
    with pytest.raises(ValueError):
        Cart().add("MUG-01", 0)


def test_rejects_unknown_sku():
    with pytest.raises(KeyError):
        Cart().add("NOPE-99")
