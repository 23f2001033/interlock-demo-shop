"""Shipping, tax and order quotes. All amounts are in US dollars."""

from shop.cart import Cart
from shop.money import round_money

TAX_RATES: dict[str, float] = {
    "US-CA": 0.0725,
    "US-NY": 0.04,
    "EU-DE": 0.19,
    "IN-KA": 0.18,
    "IN-MH": 0.18,
}

SHIPPING_FLAT = 5.00
FREE_SHIPPING_THRESHOLD = 50.00


def shipping_for(subtotal: float) -> float:
    return 0.0 if subtotal >= FREE_SHIPPING_THRESHOLD else SHIPPING_FLAT


def tax_for(subtotal: float, region: str) -> float:
    if region not in TAX_RATES:
        raise ValueError(f"unsupported region: {region}")
    return round_money(subtotal * TAX_RATES[region])


def quote(cart: Cart, region: str) -> dict[str, float]:
    """Price breakdown for a cart: subtotal, shipping, tax (on the subtotal) and total."""
    subtotal = cart.subtotal()
    shipping = shipping_for(subtotal)
    tax = tax_for(subtotal, region)
    return {
        "subtotal": subtotal,
        "shipping": shipping,
        "tax": tax,
        "total": round_money(subtotal + shipping + tax),
    }
