"""Integer-cent money values and currency conversion."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    cents: int
    currency: str = "USD"

    def __add__(self, other: Money) -> Money:
        if other.currency != self.currency:
            raise ValueError("currency mismatch")
        return Money(self.cents + other.cents, self.currency)

    def __neg__(self) -> Money:
        return Money(-self.cents, self.currency)

    def __str__(self) -> str:
        sign = "-" if self.cents < 0 else ""
        c = abs(self.cents)
        return f"{sign}{c // 100}.{c % 100:02d} {self.currency}"


def convert(m: Money, to: str, rates: dict[tuple[str, str], float]) -> Money:
    """Convert ``m`` to currency ``to`` using ``rates[(from, to)]``, rounding to the nearest cent."""
    if m.currency == to:
        return m
    rate = rates[(m.currency, to)]
    return Money(int(m.cents * rate), to)
