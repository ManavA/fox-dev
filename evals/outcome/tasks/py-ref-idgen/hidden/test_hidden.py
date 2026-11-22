import ast
import pathlib

import pytest

import idgen
from idgen import IdGenerator


def setup_function(_):
    idgen.reset()


def test_module_functions_unchanged():
    assert idgen.next_id() == "id-1"
    assert idgen.next_id() == "id-2"
    assert idgen.issued() == ["id-1", "id-2"]
    idgen.configure("order", start=10)
    assert idgen.next_id() == "order-10"
    assert idgen.issued() == ["order-10"]
    idgen.reset()
    assert idgen.next_id() == "id-1"
    assert idgen.issued() == ["id-1"]


def test_module_configure_validates():
    with pytest.raises(ValueError):
        idgen.configure("")
    with pytest.raises(ValueError):
        idgen.configure("a-b")
    with pytest.raises(ValueError):
        idgen.configure("x", start=-1)


def test_instances_independent():
    a, b = IdGenerator("a"), IdGenerator("b", start=5)
    assert a.next_id() == "a-1"
    assert a.next_id() == "a-2"
    assert b.next_id() == "b-5"
    assert a.issued() == ["a-1", "a-2"]
    assert b.issued() == ["b-5"]


def test_instance_does_not_touch_default():
    g = IdGenerator("zzz")
    g.next_id()
    assert idgen.issued() == []
    assert idgen.next_id() == "id-1"


def test_defaults():
    g = IdGenerator()
    assert g.next_id() == "id-1"


def test_constructor_validates():
    with pytest.raises(ValueError):
        IdGenerator("")
    with pytest.raises(ValueError):
        IdGenerator("1x ")
    with pytest.raises(ValueError):
        IdGenerator("ok", start=-1)


def test_issued_returns_copy():
    g = IdGenerator()
    g.next_id()
    g.issued().append("junk")
    assert g.issued() == ["id-1"]


def test_instance_reset_and_configure():
    g = IdGenerator("p", 3)
    g.next_id()
    g.reset()
    assert g.issued() == []
    assert g.next_id() == "id-1"
    g.configure("q", start=0)
    assert g.next_id() == "q-0"
    assert g.issued() == ["q-0"]


def test_start_zero():
    assert IdGenerator("a", start=0).next_id() == "a-0"


def test_exported_from_package():
    assert "IdGenerator" in idgen.__all__


def test_no_global_statement():
    import idgen.gen as gen

    tree = ast.parse(pathlib.Path(gen.__file__).read_text())
    assert not [n for n in ast.walk(tree) if isinstance(n, ast.Global)]
