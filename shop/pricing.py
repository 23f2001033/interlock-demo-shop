"""Shipping, tax and order quotes. All amounts are in US dollars."""

from shop.cart import Cart
from shop.money import round_money

TAX_RATES: dict[str, float] = {
    "US-CA": 0.0725,
    "US-NY": 0.04,
    "EU-DE": 0.19,
    "IN-KA": 0.18,
}

SHIPPING_FLAT = 5.00
FREE_SHIPPING_THRESHOLD = 50.00

# code -> (fraction off the subtotal, minimum subtotal in US dollars)
DISCOUNT_CODES: dict[str, tuple[float, float]] = {
    "SAVE10": (0.10, 40.00),
}


def shipping_for(subtotal: float) -> float:
    return 0.0 if subtotal >= FREE_SHIPPING_THRESHOLD else SHIPPING_FLAT


def tax_for(subtotal: float, region: str) -> float:
    if region not in TAX_RATES:
        raise ValueError(f"unsupported region: {region}")
    return round_money(subtotal * TAX_RATES[region])


def discount_for(subtotal: float, code: str | None) -> float:
    """Dollar amount a discount code takes off the subtotal (0 if the subtotal is too low)."""
    if code is None:
        return 0.0
    if code not in DISCOUNT_CODES:
        raise ValueError(f"unknown discount code: {code}")
    rate, minimum = DISCOUNT_CODES[code]
    return round_money(subtotal * rate) if subtotal >= minimum else 0.0


def quote(cart: Cart, region: str, code: str | None = None) -> dict[str, float]:
    """Price breakdown for a cart: subtotal, discount, shipping, tax (on the discounted
    subtotal) and total."""
    subtotal = cart.subtotal()
    discount = discount_for(subtotal, code)
    shipping = shipping_for(subtotal)
    tax = tax_for(subtotal - discount, region)
    return {
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "tax": tax,
        "total": round_money(subtotal - discount + shipping + tax),
    }
