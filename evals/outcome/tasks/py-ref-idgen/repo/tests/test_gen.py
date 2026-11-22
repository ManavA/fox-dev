import pytest

import idgen


def setup_function(_):
    idgen.reset()


def test_sequence():
    assert idgen.next_id() == "id-1"
    assert idgen.next_id() == "id-2"
    assert idgen.issued() == ["id-1", "id-2"]


def test_configure():
    idgen.configure("order", start=10)
    assert idgen.next_id() == "order-10"


def test_configure_validates():
    with pytest.raises(ValueError):
        idgen.configure("")
    with pytest.raises(ValueError):
        idgen.configure("a-b")
    with pytest.raises(ValueError):
        idgen.configure("x", start=-1)
