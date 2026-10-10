"""Plain-text receipts."""

from shop.money import format_money
from shop.orders import Order


def render_receipt(order: Order) -> str:
    out = [f"Receipt for order {order.id}"]
    for line in order.lines:
        out.append(
            f"  {line.qty} x {line.name} @ {format_money(line.unit_price)}"
            f"  {format_money(line.line_total)}"
        )
    out.append(f"Subtotal: {format_money(order.subtotal)}")
    if order.discount:
        out.append(f"Discount: -{format_money(order.discount)}")
    out.append(f"Shipping: {format_money(order.shipping)}")
    out.append(f"Tax ({order.region}): {format_money(order.tax)}")
    out.append(f"Total: {format_money(order.total)}")
    out.append(f"Charged: {order.charge_id}")
    return "\n".join(out)
