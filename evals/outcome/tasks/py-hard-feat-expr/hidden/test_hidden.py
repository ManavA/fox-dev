import math

import pytest

from calc import CalcError, evaluate


@pytest.mark.parametrize(
    "src,expected",
    [
        ("2 ** 3 ** 2", 512), ("2 ** 3", 8), ("-2 ** 2", -4), ("2 ** -1", 0.5), ("(-2) ** 2", 4), ("2 * 3 ** 2", 18), ("2 ** 2 * 3", 12),
        ("-2 ** -2", -0.25), ("--2 ** 2", 4), ("2 ** 0.5 * 2 ** 0.5", pytest.approx(2.0)),
        ("7 % 3", 1), ("-7 % 3", 2), ("7 % -3", -2), ("10 % 4 * 2", 4), ("2 * 10 % 4", 0), ("10 - 7 % 4", 7), ("5.5 % 2", 1.5),
        ("1e3", 1000), ("2.5E-2", 0.025), ("1e3 + 1", 1001), (".5e1", 5), ("1.e2", 100), ("2e+2", 200),
        ("min(3, 1, 2)", 1), ("max(3, 1, 2)", 3), ("min(5)", 5), ("abs(-4)", 4), ("abs(3 - 10)", 7), ("sqrt(16)", 4), ("sqrt(2) ** 2", pytest.approx(2.0)),
        ("round(2.567, 2)", 2.57), ("round(2.5)", 2), ("round(3.5)", 4), ("round(1234, -2)", 1200), ("max(1 + 2, 2 * 2, 3)", 4), ("min(max(1, 2), 3)", 2),
        ("max(2 ** 3, 7) % 5", 3), ("1 + (2 + 3) * 4", 21), ("4/2", 2.0), ("  3  *  ( 2+1 ) ", 9), ("-(2 + 3)", -5),
    ],
)
def test_values(src, expected):
    assert evaluate(src) == expected


def test_results_are_floats():
    assert isinstance(evaluate("4/2"), float)
    assert isinstance(evaluate("2 ** 3"), float)
    assert isinstance(evaluate("round(2.5)"), float)


def test_variables():
    assert evaluate("x * 2 + y", {"x": 3, "y": 1.5}) == 7.5
    assert evaluate("rate_2 ** 2", {"rate_2": 3}) == 9
    assert evaluate("max(a, b)", {"a": 1, "b": 9}) == 9
    assert evaluate("1 + 2", None) == 3
    assert evaluate("1 + 2", {}) == 3


def test_variables_case_sensitive():
    with pytest.raises(CalcError, match="X"):
        evaluate("X", {"x": 1})


def err(src, vars=None):
    with pytest.raises(CalcError) as e:
        evaluate(src, vars)
    return e.value


def test_unknown_variable_position_and_name():
    e = err("1 + foo * 2")
    assert "foo" in str(e) and e.position == 4


def test_unknown_function():
    e = err("2 * bar(1)")
    assert "bar" in str(e) and e.position == 4


def test_division_and_modulo_by_zero_positions():
    assert err("10 / 0").position == 3
    assert err("1 + 10 % 0").position == 7
    assert err("1 / (2 - 2)").position == 2
    assert "division by zero" in str(err("1 / 0"))


def test_unexpected_end_position():
    assert err("1 +").position == 3
    assert err("2 * ").position == 4
    assert err("max(1,").position == 6


def test_unexpected_token_position():
    assert err("1 2").position == 2
    assert err("(1 + 2))").position == 7
    assert err("1 + * 2").position == 4
    assert err("3 $ 4").position == 2


def test_missing_paren_position():
    assert err("(1 + 2").position == 6
    assert err("max(1, 2 3)").position == 9


def test_wrong_arg_counts():
    for bad in ["abs()", "abs(1, 2)", "sqrt(1, 2)", "round()", "round(1, 2, 3)", "min()", "max()"]:
        err(bad)


def test_sqrt_negative_position():
    e = err("1 + sqrt(0 - 4)")
    assert e.position == 4


def test_function_name_without_paren_is_a_variable():
    assert err("max").position == 0
    assert evaluate("max + 1", {"max": 2}) == 3


def test_existing_messages():
    assert "division by zero" in str(err("1/0"))
    assert str(err("1 +")) == "unexpected end of input"
    assert str(err("(1 + 2")) in ("unexpected end of input", "expected )")


def test_position_attribute_always_present():
    for bad in ["", "(", ")", "1 +", "foo", "1/0", "1 1", "sqrt(-1)", "min()", "abs(1,2)"]:
        assert isinstance(err(bad).position, int)


def test_math_agrees():
    assert evaluate("sqrt(2)") == math.sqrt(2)
