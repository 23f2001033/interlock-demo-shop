from shop.banner import free_shipping_banner
from shop.cart import Cart


def test_banner_shows_amount_left_for_free_shipping():
    cart = Cart()
    cart.add("BAG-01")
    assert free_shipping_banner(cart) == "Add $40.05 more for free shipping"


def test_banner_when_free_shipping_unlocked():
    cart = Cart()
    cart.add("MUG-01", 4)
    assert free_shipping_banner(cart) == "You've unlocked free shipping!"
