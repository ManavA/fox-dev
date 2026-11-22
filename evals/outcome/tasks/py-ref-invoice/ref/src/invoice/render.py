"""Plain-text invoice rendering."""
from decimal import Decimal

from .pricing import discount_amount, line_total, money, tax_amount, unit_price

RULE = "-" * 40


def _row(label: str, amount: str) -> str:
    return "%-30s %9s" % (label, amount)


def _item_line(item: dict) -> str:
    total = line_total(item)
    price = money(unit_price(item))
    return "%-20s %3d x %8s = %9s" % (item["sku"], item["qty"], str(price), str(total))


def render_invoice(order):
    """Render an order as a text invoice.

    ``order`` is a dict: ``{"number": str, "items": [{"sku", "qty", "unit_price"}],
    "discount_code": str | None, "tax_rate": str}``. Prices and rates are decimal strings.
    """
    lines = ["INVOICE " + order["number"], RULE]
    lines += [_item_line(item) for item in order["items"]]
    subtotal = money(sum((line_total(i) for i in order["items"]), Decimal("0.00")))
    lines += [RULE, _row("Subtotal", str(subtotal))]
    code = order.get("discount_code")
    discount = discount_amount(subtotal, code)
    if discount > 0:
        lines.append(_row("Discount (" + code + ")", "-" + str(discount)))
    taxable = subtotal - discount
    tax = tax_amount(taxable, order["tax_rate"])
    lines.append(_row("Tax", str(tax)))
    lines.append(_row("TOTAL", str(money(taxable + tax))))
    return "\n".join(lines)
