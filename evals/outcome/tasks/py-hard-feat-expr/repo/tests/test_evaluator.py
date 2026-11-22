import pytest

from calc import CalcError, evaluate


def test_basic():
    assert evaluate("1 + 2 * 3") == 7
    assert evaluate("(1 + 2) * 3") == 9
    assert evaluate("10 / 4") == 2.5


def test_unary_minus():
    assert evaluate("-3 + 5") == 2
    assert evaluate("--3") == 3
    assert evaluate("2 * -3") == -6


def test_errors():
    with pytest.raises(CalcError):
        evaluate("1 / 0")
    with pytest.raises(CalcError):
        evaluate("1 +")
    with pytest.raises(CalcError):
        evaluate("(1 + 2")
    with pytest.raises(CalcError):
        evaluate("1 2")
