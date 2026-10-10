"""Product catalog."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price: float  # unit price in US dollars


CATALOG: dict[str, Product] = {
    "MUG-01": Product("MUG-01", "Ceramic mug", 12.50),
    "TEE-01": Product("TEE-01", "Logo t-shirt", 19.99),
    "CAP-01": Product("CAP-01", "Baseball cap", 15.00),
    "BAG-01": Product("BAG-01", "Tote bag", 9.95),
}


def get_product(sku: str) -> Product:
    try:
        return CATALOG[sku]
    except KeyError:
        raise KeyError(f"unknown sku: {sku}") from None


def price_of(sku: str) -> float:
    """Unit price of a product, in US dollars."""
    return get_product(sku).price
