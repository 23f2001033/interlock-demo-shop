from shop.cart import Cart
from shop.orders import place_order
from shop.payments import PaymentGateway
from shop.receipts import render_receipt


def test_receipt_shows_lines_and_totals():
    cart = Cart()
    cart.add("TEE-01", 2)
    receipt = render_receipt(place_order(cart, "cus_1", "US-CA", PaymentGateway()))
    assert "2 x Logo t-shirt @ $19.99  $39.98" in receipt
    assert "Subtotal: $39.98" in receipt
    assert "Shipping: $5.00" in receipt
    assert "Tax (US-CA): $2.90" in receipt
    assert "Total: $47.88" in receipt
    assert "Discount" not in receipt


def test_receipt_shows_discount():
    cart = Cart()
    cart.add("MUG-01", 2)
    cart.add("CAP-01")
    receipt = render_receipt(place_order(cart, "cus_1", "US-CA", PaymentGateway(), code="SAVE10"))
    assert "Subtotal: $40.00" in receipt
    assert "Discount: -$4.00" in receipt
    assert "Tax (US-CA): $2.61" in receipt
    assert "Total: $43.61" in receipt
