"""Shipping, tax and order quotes. All amounts are in US cents."""

from shop.cart import Cart
from shop.money import apply_rate

TAX_RATES: dict[str, float] = {
    "US-CA": 0.0725,
    "US-NY": 0.04,
    "EU-DE": 0.19,
    "IN-KA": 0.18,
}

SHIPPING_FLAT = 500
FREE_SHIPPING_THRESHOLD = 5000


def shipping_for(subtotal: int) -> int:
    return 0 if subtotal >= FREE_SHIPPING_THRESHOLD else SHIPPING_FLAT


def tax_for(subtotal: int, region: str) -> int:
    if region not in TAX_RATES:
        raise ValueError(f"unsupported region: {region}")
    return apply_rate(subtotal, TAX_RATES[region])


def quote(cart: Cart, region: str) -> dict[str, int]:
    """Price breakdown for a cart: subtotal, shipping, tax (on the subtotal) and total."""
    subtotal = cart.subtotal()
    shipping = shipping_for(subtotal)
    tax = tax_for(subtotal, region)
    return {
        "subtotal": subtotal,
        "shipping": shipping,
        "tax": tax,
        "total": subtotal + shipping + tax,
    }
