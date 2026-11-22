"""A small least-recently-used cache."""
from __future__ import annotations

import time
from collections import OrderedDict
from typing import Any, Callable, Optional


class LRUCache:
    """Fixed-capacity cache that evicts the least recently used entry.

    ``clock`` is a zero-argument callable returning the current time in seconds;
    it exists so tests can control time.
    """

    def __init__(
        self,
        capacity: int,
        clock: Callable[[], float] = time.monotonic,
        *,
        default_ttl: Optional[float] = None,
    ) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.default_ttl = default_ttl
        self._clock = clock
        # key -> (value, expires_at or None)
        self._data: OrderedDict[Any, tuple[Any, Optional[float]]] = OrderedDict()

    def _expired(self, key: Any) -> bool:
        expires_at = self._data[key][1]
        return expires_at is not None and self._clock() >= expires_at

    def _drop_if_expired(self, key: Any) -> bool:
        if key in self._data and self._expired(key):
            del self._data[key]
            return True
        return False

    def purge_expired(self) -> int:
        stale = [k for k in self._data if self._expired(k)]
        for k in stale:
            del self._data[k]
        return len(stale)

    def __len__(self) -> int:
        self.purge_expired()
        return len(self._data)

    def __contains__(self, key: Any) -> bool:
        self._drop_if_expired(key)
        return key in self._data

    def get(self, key: Any, default: Any = None) -> Any:
        self._drop_if_expired(key)
        if key not in self._data:
            return default
        self._data.move_to_end(key)
        return self._data[key][0]

    def set(self, key: Any, value: Any, ttl: Optional[float] = None) -> None:
        if ttl is None:
            ttl = self.default_ttl
        if ttl is not None and ttl <= 0:
            raise ValueError("ttl must be positive")
        expires_at = None if ttl is None else self._clock() + ttl
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = (value, expires_at)
        if len(self._data) > self.capacity:
            self.purge_expired()
        while len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def delete(self, key: Any) -> bool:
        if self._drop_if_expired(key):
            return False
        if key in self._data:
            del self._data[key]
            return True
        return False

    def clear(self) -> None:
        self._data.clear()

    def keys(self) -> list:
        """Keys from least to most recently used."""
        self.purge_expired()
        return list(self._data)
