"""Placing orders."""

import itertools
from dataclasses import dataclass

from shop.cart import Cart
from shop.catalog import get_product, price_of
from shop.money import round_money
from shop.payments import PaymentGateway
from shop.pricing import quote

_order_numbers = itertools.count(1)


@dataclass(frozen=True)
class OrderLine:
    sku: str
    name: str
    qty: int
    unit_price: float  # US dollars
    line_total: float  # US dollars


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    region: str
    lines: list[OrderLine]
    subtotal: float
    shipping: float
    tax: float
    total: float
    charge_id: str


def place_order(cart: Cart, customer_id: str, region: str, gateway: PaymentGateway) -> Order:
    """Quote the cart, charge the customer and return the order."""
    if cart.is_empty():
        raise ValueError("cart is empty")
    q = quote(cart, region)
    charge_id = gateway.charge(customer_id, int(round(q["total"] * 100)))
    lines = [
        OrderLine(sku, get_product(sku).name, qty, price_of(sku), round_money(price_of(sku) * qty))
        for sku, qty in cart.lines()
    ]
    return Order(
        id=f"ORD-{next(_order_numbers):04d}",
        customer_id=customer_id,
        region=region,
        lines=lines,
        subtotal=q["subtotal"],
        shipping=q["shipping"],
        tax=q["tax"],
        total=q["total"],
        charge_id=charge_id,
    )
