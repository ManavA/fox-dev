"""Money maths for invoices."""
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

CENT = Decimal("0.01")


def money(x: Decimal) -> Decimal:
    return x.quantize(CENT, rounding=ROUND_HALF_UP)


def unit_price(item: dict) -> Decimal:
    price = Decimal(item["unit_price"])
    if price < 0:
        raise ValueError("negative price: " + item["sku"])
    return price


def line_total(item: dict) -> Decimal:
    if item["qty"] <= 0:
        raise ValueError("quantity must be positive: " + item["sku"])
    return money(unit_price(item) * item["qty"])


def discount_amount(subtotal: Decimal, code: Optional[str]) -> Decimal:
    if code is None:
        return Decimal("0.00")
    if code == "SAVE10":
        return money(subtotal * Decimal("0.10"))
    if code == "FIVEOFF":
        return Decimal("5.00") if subtotal >= Decimal("50.00") else Decimal("0.00")
    raise ValueError("unknown discount code: " + code)


def tax_amount(taxable: Decimal, rate: str) -> Decimal:
    return money(taxable * Decimal(rate))
