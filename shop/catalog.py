"""Product catalog."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price: int  # unit price in US cents


CATALOG: dict[str, Product] = {
    "MUG-01": Product("MUG-01", "Ceramic mug", 1250),
    "TEE-01": Product("TEE-01", "Logo t-shirt", 1999),
    "CAP-01": Product("CAP-01", "Baseball cap", 1500),
    "BAG-01": Product("BAG-01", "Tote bag", 995),
}


def get_product(sku: str) -> Product:
    try:
        return CATALOG[sku]
    except KeyError:
        raise KeyError(f"unknown sku: {sku}") from None


def price_of(sku: str) -> int:
    """Unit price of a product, in US cents."""
    return get_product(sku).price
