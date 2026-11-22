import pytest

from slugkit import slugify


@pytest.mark.parametrize(
    "text,kw,expected",
    [
        ("Hello,   World!!", {}, "hello-world"),
        ("Crème Brûlée", {}, "creme-brulee"),
        ("Hello World", {"max_length": 6}, "hello"),
        ("Hello World", {"max_length": 5}, "hello"),
        ("  a  b  ", {"sep": "_"}, "a_b"),
        ("", {}, ""),
        ("!!!", {}, ""),
        ("---", {}, ""),
        ("Python 3 rocks", {}, "python-3-rocks"),
        ("a b", {"sep": "_"}, "a_b"),
        ("abcdefghij", {"max_length": 4}, "abcd"),
        ("Ünïcödé Tëxt", {}, "unicode-text"),
        ("one--two__three", {}, "one-two-three"),
        ("a b c d", {"max_length": 4}, "a-b"),
        ("a b", {"max_length": 0}, ""),
        ("x y", {"sep": "--"}, "x--y"),
    ],
)
def test_cases(text, kw, expected):
    assert slugify(text, **kw) == expected


def test_never_exceeds_max_length():
    for n in range(0, 12):
        assert len(slugify("The quick brown fox", max_length=n)) <= n
