"""Helpers for money amounts. Amounts are integer US cents."""

from decimal import ROUND_HALF_UP, Decimal


def apply_rate(cents: int, rate: float) -> int:
    """A fraction of an amount (e.g. tax), rounded to whole cents (half up).

    The rate goes through its decimal string so e.g. 0.0725 is exact, not the nearest float.
    """
    exact = Decimal(cents) * Decimal(str(rate))
    return int(exact.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def format_money(cents: int) -> str:
    """Format an amount in cents for display, e.g. 123450 -> '$1,234.50'."""
    sign = "-" if cents < 0 else ""
    dollars, rest = divmod(abs(cents), 100)
    return f"{sign}${dollars:,}.{rest:02d}"
