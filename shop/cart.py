"""Shopping cart."""

from shop.catalog import get_product, price_of
from shop.money import round_money


class Cart:
    def __init__(self) -> None:
        self._lines: dict[str, int] = {}  # sku -> quantity

    def add(self, sku: str, qty: int = 1) -> None:
        if qty <= 0:
            raise ValueError("quantity must be positive")
        get_product(sku)  # raises KeyError for unknown skus
        self._lines[sku] = self._lines.get(sku, 0) + qty

    def remove(self, sku: str) -> None:
        self._lines.pop(sku, None)

    def is_empty(self) -> bool:
        return not self._lines

    def lines(self) -> list[tuple[str, int]]:
        """(sku, quantity) pairs in the order they were added."""
        return list(self._lines.items())

    def subtotal(self) -> float:
        """Sum of unit price x quantity, in US dollars."""
        return round_money(sum(price_of(sku) * qty for sku, qty in self._lines.items()))
