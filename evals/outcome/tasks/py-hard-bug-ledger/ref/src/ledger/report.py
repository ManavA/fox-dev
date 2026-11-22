"""Monthly reporting."""
from __future__ import annotations

from .account import Account
from .money import Money


def month_of(date: str) -> str:
    """"2024-9-5" -> "2024-09"."""
    year, month, _ = date.split("-")
    return f"{int(year):04d}-{int(month):02d}"


def monthly_summary(acct: Account) -> dict[str, Money]:
    """Net amount per month, keyed "YYYY-MM", in chronological key order."""
    out: dict[str, Money] = {}
    for t in acct.statement():
        key = month_of(t.date)
        out[key] = out.get(key, Money(0, acct.currency)) + t.amount
    return out
