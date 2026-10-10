"""Storefront banner for the cart page."""

from shop.cart import Cart
from shop.money import format_money
from shop.pricing import FREE_SHIPPING_THRESHOLD


def free_shipping_banner(cart: Cart) -> str:
    remaining = FREE_SHIPPING_THRESHOLD - cart.subtotal()
    if remaining <= 0:
        return "You've unlocked free shipping!"
    return f"Add {format_money(remaining)} more for free shipping"
