import ast
import json
import pathlib
from decimal import Decimal

import pytest

from invoice import render_invoice
from invoice import pricing

HERE = pathlib.Path(__file__).parent
GOLDEN = json.load(open(HERE / "golden.json"))


@pytest.mark.parametrize("case", GOLDEN, ids=[c["order"]["number"] + str(i) for i, c in enumerate(GOLDEN)])
def test_output_identical(case):
    try:
        out = render_invoice(case["order"])
    except ValueError as e:
        out = "ValueError: " + str(e)
    assert out == case["out"]


def test_money_half_up():
    assert pricing.money(Decimal("0.005")) == Decimal("0.01")
    assert pricing.money(Decimal("2.675")) == Decimal("2.68")
    assert pricing.money(Decimal("1.004")) == Decimal("1.00")
    assert str(pricing.money(Decimal("3"))) == "3.00"


def test_line_total():
    assert pricing.line_total({"sku": "A", "qty": 3, "unit_price": "9.99"}) == Decimal("29.97")
    assert pricing.line_total({"sku": "A", "qty": 120, "unit_price": "0.333"}) == Decimal("39.96")


def test_line_total_validation():
    with pytest.raises(ValueError, match="quantity must be positive: A"):
        pricing.line_total({"sku": "A", "qty": 0, "unit_price": "1"})
    with pytest.raises(ValueError, match="negative price: A"):
        pricing.line_total({"sku": "A", "qty": 1, "unit_price": "-1"})


def test_discount_amount():
    d = pricing.discount_amount
    assert d(Decimal("54.47"), "SAVE10") == Decimal("5.45")
    assert d(Decimal("50.00"), "FIVEOFF") == Decimal("5.00")
    assert d(Decimal("49.99"), "FIVEOFF") == Decimal("0.00")
    assert d(Decimal("10.00"), None) == Decimal("0.00")
    with pytest.raises(ValueError, match="unknown discount code: BAD"):
        d(Decimal("10.00"), "BAD")


def test_tax_amount():
    assert pricing.tax_amount(Decimal("49.02"), "0.08") == Decimal("3.92")
    assert pricing.tax_amount(Decimal("100.00"), "0") == Decimal("0.00")


def test_rounding_expression_only_in_money():
    src = pathlib.Path(pricing.__file__).parent
    hits = [p.name for p in src.glob("*.py") if p.read_text().count("ROUND_HALF_UP") > 0]
    uses = sum(p.read_text().count("quantize(") for p in src.glob("*.py"))
    assert uses == 1, "quantize must appear exactly once in the package"
    assert hits == ["pricing.py"]


def test_no_function_longer_than_20_lines():
    pkg = pathlib.Path(pricing.__file__).parent
    long = []
    for p in pkg.glob("*.py"):
        for node in ast.walk(ast.parse(p.read_text())):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                n = node.end_lineno - node.lineno + 1
                if n > 20:
                    long.append((p.name, node.name, n))
    assert not long, long
