"""A fake payment gateway. Like most real gateways, it takes integer cents."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Charge:
    id: str
    customer_id: str
    amount_cents: int
    currency: str = "USD"


class PaymentGateway:
    def __init__(self) -> None:
        self.charges: list[Charge] = []

    def charge(self, customer_id: str, amount_cents: int, currency: str = "USD") -> str:
        if not isinstance(amount_cents, int) or isinstance(amount_cents, bool):
            raise TypeError("amount_cents must be an int")
        if amount_cents <= 0:
            raise ValueError("amount_cents must be positive")
        if not (isinstance(currency, str) and len(currency) == 3 and currency.isascii()
                and currency.isalpha() and currency.isupper()):
            raise ValueError("currency must be a three-letter ISO 4217 code, e.g. 'USD'")
        charge = Charge(f"ch_{len(self.charges) + 1:04d}", customer_id, amount_cents, currency)
        self.charges.append(charge)
        return charge.id

    def total_charged(self, customer_id: str) -> int:
        return sum(c.amount_cents for c in self.charges if c.customer_id == customer_id)
