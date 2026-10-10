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

SMALL_ORDER_FEE = 150
SMALL_ORDER_THRESHOLD = 1500

# code -> (fraction off the subtotal, minimum subtotal in US cents)
DISCOUNT_CODES: dict[str, tuple[float, int]] = {
    "SAVE10": (0.10, 4000),
}


def shipping_for(subtotal: int) -> int:
    return 0 if subtotal >= FREE_SHIPPING_THRESHOLD else SHIPPING_FLAT


def fee_for(subtotal: int) -> int:
    return SMALL_ORDER_FEE if subtotal < SMALL_ORDER_THRESHOLD else 0


def tax_for(subtotal: int, region: str) -> int:
    if region not in TAX_RATES:
        raise ValueError(f"unsupported region: {region}")
    return apply_rate(subtotal, TAX_RATES[region])


def discount_for(subtotal: int, code: str | None) -> int:
    """Amount a discount code takes off the subtotal (0 if the subtotal is too low)."""
    if code is None:
        return 0
    if code not in DISCOUNT_CODES:
        raise ValueError(f"unknown discount code: {code}")
    rate, minimum = DISCOUNT_CODES[code]
    return apply_rate(subtotal, rate) if subtotal >= minimum else 0


def quote(cart: Cart, region: str, code: str | None = None) -> dict[str, int]:
    """Price breakdown for a cart: subtotal, discount, shipping, small-order fee, tax (on the
    discounted subtotal) and total."""
    subtotal = cart.subtotal()
    discount = discount_for(subtotal, code)
    shipping = shipping_for(subtotal)
    fee = fee_for(subtotal)
    tax = tax_for(subtotal - discount, region)
    return {
        "subtotal": subtotal,
        "discount": discount,
        "shipping": shipping,
        "fee": fee,
        "tax": tax,
        "total": subtotal - discount + shipping + fee + tax,
    }
