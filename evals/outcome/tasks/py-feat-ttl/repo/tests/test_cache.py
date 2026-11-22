import pytest

from tinycache import LRUCache


def test_set_and_get():
    c = LRUCache(2)
    c.set("a", 1)
    assert c.get("a") == 1
    assert c.get("missing") is None
    assert c.get("missing", 7) == 7


def test_evicts_least_recently_used():
    c = LRUCache(2)
    c.set("a", 1)
    c.set("b", 2)
    c.get("a")
    c.set("c", 3)
    assert "b" not in c
    assert c.keys() == ["a", "c"]


def test_overwrite_moves_to_end():
    c = LRUCache(2)
    c.set("a", 1)
    c.set("b", 2)
    c.set("a", 10)
    assert c.keys() == ["b", "a"]
    assert c.get("a") == 10


def test_delete_and_clear():
    c = LRUCache(3)
    c.set("a", 1)
    c.set("b", 2)
    assert c.delete("a") is True
    assert c.delete("a") is False
    c.clear()
    assert len(c) == 0


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        LRUCache(0)
