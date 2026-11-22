import pytest

from tinycache import LRUCache


class Clock:
    def __init__(self):
        self.t = 100.0

    def __call__(self):
        return self.t


def make(cap=3, **kw):
    clk = Clock()
    return LRUCache(cap, clock=clk, **kw), clk


def test_default_ttl_expires_at_exact_boundary():
    c, clk = make(default_ttl=10)
    c.set("a", 1)
    clk.t += 9.99
    assert c.get("a") == 1
    clk.t += 0.01
    assert c.get("a") is None
    assert "a" not in c


def test_per_call_ttl_overrides_default():
    c, clk = make(default_ttl=10)
    c.set("a", 1, ttl=2)
    c.set("b", 2)
    clk.t += 3
    assert "a" not in c
    assert "b" in c


def test_no_ttl_never_expires():
    c, clk = make()
    c.set("a", 1)
    clk.t += 10**9
    assert c.get("a") == 1


def test_invalid_ttl():
    c, _ = make()
    with pytest.raises(ValueError):
        c.set("a", 1, ttl=0)
    with pytest.raises(ValueError):
        c.set("a", 1, ttl=-5)
    c2, _ = make(default_ttl=5)
    with pytest.raises(ValueError):
        c2.set("a", 1, ttl=0)


def test_invalid_default_ttl_is_rejected_at_construction_or_at_set():
    try:
        c, _ = make(default_ttl=-1)
    except ValueError:
        return
    with pytest.raises(ValueError):
        c.set("a", 1)


def test_default_ttl_is_keyword_only():
    with pytest.raises(TypeError):
        LRUCache(3, Clock(), 5)


def test_len_and_keys_ignore_expired():
    c, clk = make(default_ttl=5)
    c.set("a", 1)
    clk.t += 3
    c.set("b", 2)
    clk.t += 3
    assert len(c) == 1
    assert c.keys() == ["b"]


def test_get_does_not_extend_lifetime():
    c, clk = make()
    c.set("a", 1, ttl=10)
    clk.t += 6
    assert c.get("a") == 1
    clk.t += 5
    assert c.get("a") is None


def test_set_restarts_ttl():
    c, clk = make()
    c.set("a", 1, ttl=10)
    clk.t += 8
    c.set("a", 2, ttl=10)
    clk.t += 8
    assert c.get("a") == 2
    clk.t += 3
    assert c.get("a") is None


def test_set_without_ttl_on_existing_clears_old_ttl():
    c, clk = make()
    c.set("a", 1, ttl=1)
    c.set("a", 2)
    clk.t += 100
    assert c.get("a") == 2


def test_full_cache_drops_expired_before_evicting_lru():
    c, clk = make(cap=2)
    c.set("a", 1)
    c.set("b", 2, ttl=1)
    clk.t += 2
    c.set("c", 3)
    assert c.keys() == ["a", "c"]


def test_full_cache_still_evicts_lru_when_nothing_expired():
    c, _ = make(cap=2, default_ttl=100)
    c.set("a", 1)
    c.set("b", 2)
    c.set("c", 3)
    assert c.keys() == ["b", "c"]


def test_purge_expired_returns_count():
    c, clk = make(default_ttl=5)
    c.set("a", 1)
    c.set("b", 2)
    c.set("c", 3, ttl=50)
    clk.t += 6
    assert c.purge_expired() == 2
    assert c.purge_expired() == 0
    assert c.keys() == ["c"]


def test_delete_expired_returns_false():
    c, clk = make(default_ttl=1)
    c.set("a", 1)
    clk.t += 2
    assert c.delete("a") is False


def test_get_default_for_expired():
    c, clk = make(default_ttl=1)
    c.set("a", 1)
    clk.t += 1
    assert c.get("a", "dflt") == "dflt"
