from slugkit import slugify


def test_simple():
    assert slugify("Hello World") == "hello-world"


def test_digits_kept():
    assert slugify("Python 3 rocks") == "python-3-rocks"


def test_custom_separator():
    assert slugify("a b", sep="_") == "a_b"


def test_max_length():
    assert slugify("abcdefghij", max_length=4) == "abcd"
