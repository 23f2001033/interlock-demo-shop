"""Placing orders."""

import itertools
from dataclasses import dataclass

from shop.cart import Cart
from shop.catalog import get_product, price_of
from shop.payments import PaymentGateway
from shop.pricing import quote

_order_numbers = itertools.count(1)


@dataclass(frozen=True)
class OrderLine:
    sku: str
    name: str
    qty: int
    unit_price: int  # US cents
    line_total: int  # US cents


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    region: str
    lines: list[OrderLine]
    subtotal: int  # US cents
    discount: int  # US cents
    shipping: int  # US cents
    tax: int  # US cents
    total: int  # US cents
    charge_id: str


def place_order(
    cart: Cart, customer_id: str, region: str, gateway: PaymentGateway, code: str | None = None
) -> Order:
    """Quote the cart (with an optional discount code), charge the customer and return the order."""
    if cart.is_empty():
        raise ValueError("cart is empty")
    q = quote(cart, region, code)
    charge_id = gateway.charge(customer_id, q["total"])
    lines = [
        OrderLine(sku, get_product(sku).name, qty, price_of(sku), price_of(sku) * qty)
        for sku, qty in cart.lines()
    ]
    return Order(
        id=f"ORD-{next(_order_numbers):04d}",
        customer_id=customer_id,
        region=region,
        lines=lines,
        subtotal=q["subtotal"],
        discount=q["discount"],
        shipping=q["shipping"],
        tax=q["tax"],
        total=q["total"],
        charge_id=charge_id,
    )
