"""Plain-text invoice rendering."""
from decimal import ROUND_HALF_UP, Decimal


def render_invoice(order):
    """Render an order as a text invoice.

    ``order`` is a dict: ``{"number": str, "items": [{"sku", "qty", "unit_price"}],
    "discount_code": str | None, "tax_rate": str}``. Prices and rates are decimal strings.
    """
    lines = []
    lines.append("INVOICE " + order["number"])
    lines.append("-" * 40)
    subtotal = Decimal("0.00")
    for item in order["items"]:
        if item["qty"] <= 0:
            raise ValueError("quantity must be positive: " + item["sku"])
        price = Decimal(item["unit_price"])
        if price < 0:
            raise ValueError("negative price: " + item["sku"])
        total = (price * item["qty"]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        subtotal += total
        lines.append("%-20s %3d x %8s = %9s" % (item["sku"], item["qty"], str(price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)), str(total)))
    lines.append("-" * 40)
    subtotal = subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    lines.append("%-30s %9s" % ("Subtotal", str(subtotal)))
    code = order.get("discount_code")
    discount = Decimal("0.00")
    if code is not None:
        if code == "SAVE10":
            discount = (subtotal * Decimal("0.10")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        elif code == "FIVEOFF":
            if subtotal >= Decimal("50.00"):
                discount = Decimal("5.00")
        else:
            raise ValueError("unknown discount code: " + code)
    if discount > 0:
        lines.append("%-30s %9s" % ("Discount (" + code + ")", "-" + str(discount)))
    taxable = subtotal - discount
    tax = (taxable * Decimal(order["tax_rate"])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    lines.append("%-30s %9s" % ("Tax", str(tax)))
    grand = (taxable + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    lines.append("%-30s %9s" % ("TOTAL", str(grand)))
    return "\n".join(lines)
