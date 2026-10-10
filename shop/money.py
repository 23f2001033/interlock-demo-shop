"""Helpers for money amounts. Amounts are floats in US dollars."""


def round_money(amount: float) -> float:
    """Round a dollar amount to whole cents (half up)."""
    return round(amount + 1e-9, 2)


def format_money(amount: float) -> str:
    """Format a dollar amount for display, e.g. 1234.5 -> '$1,234.50'."""
    return f"${amount:,.2f}"
