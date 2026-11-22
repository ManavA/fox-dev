from ledger import Account, Money, Txn, convert, monthly_summary


def test_money_str():
    assert str(Money(1234)) == "12.34 USD"
    assert str(Money(-5)) == "-0.05 USD"


def test_balance():
    a = Account()
    a.add(Txn("2024-01-05", Money(1000)))
    a.add(Txn("2024-01-06", Money(-250)))
    assert a.balance() == Money(750)


def test_convert_simple():
    assert convert(Money(1000), "EUR", {("USD", "EUR"): 0.5}) == Money(500, "EUR")


def test_statement_order():
    a = Account()
    a.add(Txn("2024-02-01", Money(1)))
    a.add(Txn("2024-01-15", Money(2)))
    assert [t.date for t in a.statement()] == ["2024-01-15", "2024-02-01"]


def test_summary_single_month():
    a = Account()
    a.add(Txn("2024-03-01", Money(500)))
    a.add(Txn("2024-03-09", Money(700)))
    assert monthly_summary(a) == {"2024-03": Money(1200)}
