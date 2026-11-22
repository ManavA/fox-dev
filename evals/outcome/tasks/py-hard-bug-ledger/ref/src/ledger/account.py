"""An account is a list of dated transactions in one currency."""
from __future__ import annotations

from dataclasses import dataclass, field

from .money import Money


def date_key(date: str) -> tuple[int, int, int]:
    y, m, d = date.split("-")
    return int(y), int(m), int(d)


@dataclass(frozen=True)
class Txn:
    date: str  # ISO date "YYYY-MM-DD" (month and day may be written without zero padding)
    amount: Money  # positive = money in, negative = money out
    kind: str = "payment"  # "payment" or "refund"
    memo: str = ""


@dataclass
class Account:
    currency: str = "USD"
    txns: list[Txn] = field(default_factory=list)

    def add(self, txn: Txn) -> None:
        if txn.amount.currency != self.currency:
            raise ValueError("currency mismatch")
        self.txns.append(txn)

    def balance(self) -> Money:
        total = Money(0, self.currency)
        for t in self.txns:
            total = total + t.amount
        return total

    def statement(self) -> list[Txn]:
        """Transactions oldest first."""
        return sorted(self.txns, key=lambda t: date_key(t.date))
