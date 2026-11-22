from ledger import Account, Money, Txn, convert, monthly_summary

R = {("USD", "EUR"): 0.9, ("EUR", "USD"): 1.1, ("USD", "JPY"): 150.0, ("USD", "GBP"): 0.5}


def test_convert_issue_example():
    assert convert(Money(1001), "EUR", R) == Money(901, "EUR")


def test_convert_rounds_half_away_from_zero():
    assert convert(Money(5), "GBP", R) == Money(3, "GBP")  # 2.5 -> 3
    assert convert(Money(3), "GBP", R) == Money(2, "GBP")  # 1.5 -> 2
    assert convert(Money(-5), "GBP", R) == Money(-3, "GBP")  # -2.5 -> -3
    assert convert(Money(-1001), "EUR", R) == Money(-901, "EUR")


def test_convert_nearest():
    assert convert(Money(1000), "EUR", R) == Money(900, "EUR")
    assert convert(Money(1), "EUR", R) == Money(1, "EUR")  # 0.9 -> 1
    assert convert(Money(1), "GBP", R) == Money(1, "GBP")  # 0.5 -> 1
    assert convert(Money(7), "JPY", R) == Money(1050, "JPY")


def test_convert_same_currency_and_missing_rate():
    import pytest

    assert convert(Money(123), "USD", R) == Money(123)
    with pytest.raises(KeyError):
        convert(Money(1), "CHF", R)


def acct(*items):
    a = Account()
    for d, c, k in items:
        a.add(Txn(d, Money(c), k))
    return a


def test_summary_is_net_with_refunds():
    a = acct(("2024-03-01", 1000, "payment"), ("2024-03-05", -300, "refund"), ("2024-03-06", -100, "payment"))
    assert monthly_summary(a) == {"2024-03": Money(600)}
    assert sum(m.cents for m in monthly_summary(a).values()) == a.balance().cents


def test_summary_sum_matches_balance_multi_month():
    a = acct(("2024-1-1", 500, "payment"), ("2024-2-3", -200, "refund"), ("2024-2-4", 50, "payment"), ("2025-01-01", -75, "payment"))
    assert sum(m.cents for m in monthly_summary(a).values()) == a.balance().cents


def test_statement_numeric_date_order():
    a = acct(("2024-10-01", 1, "payment"), ("2024-9-15", 2, "payment"), ("2024-09-02", 3, "payment"), ("2024-9-3", 4, "payment"), ("2023-12-31", 5, "payment"))
    assert [t.date for t in a.statement()] == ["2023-12-31", "2024-09-02", "2024-9-3", "2024-9-15", "2024-10-01"]


def test_statement_day_order_within_month():
    a = acct(("2024-05-10", 1, "payment"), ("2024-5-9", 2, "payment"), ("2024-05-1", 3, "payment"))
    assert [t.date for t in a.statement()] == ["2024-05-1", "2024-5-9", "2024-05-10"]


def test_summary_keys_padded_and_chronological():
    a = acct(("2024-10-01", 1, "payment"), ("2024-9-15", 2, "payment"), ("2024-09-02", 3, "payment"), ("2024-2-1", 4, "payment"))
    s = monthly_summary(a)
    assert list(s) == ["2024-02", "2024-09", "2024-10"]
    assert s["2024-09"] == Money(5)


def test_existing_behaviour():
    assert str(Money(1234)) == "12.34 USD"
    a = acct(("2024-01-05", 1000, "payment"), ("2024-01-06", -250, "payment"))
    assert a.balance() == Money(750)
    assert monthly_summary(a) == {"2024-01": Money(750)}
