import pytest

from invoice import render_invoice

ORDER = {
    "number": "INV-1",
    "items": [
        {"sku": "WIDGET", "qty": 3, "unit_price": "9.99"},
        {"sku": "GADGET", "qty": 1, "unit_price": "24.50"},
    ],
    "discount_code": "SAVE10",
    "tax_rate": "0.08",
}


def test_render_full():
    out = render_invoice(ORDER)
    assert out.splitlines()[0] == "INVOICE INV-1"
    assert "Subtotal" in out and "54.47" in out
    assert "Discount (SAVE10)" in out and "-5.45" in out
    assert out.splitlines()[-1].startswith("TOTAL")


def test_unknown_code():
    with pytest.raises(ValueError):
        render_invoice(dict(ORDER, discount_code="NOPE"))


def test_bad_quantity():
    with pytest.raises(ValueError):
        render_invoice(dict(ORDER, items=[{"sku": "X", "qty": 0, "unit_price": "1.00"}]))
