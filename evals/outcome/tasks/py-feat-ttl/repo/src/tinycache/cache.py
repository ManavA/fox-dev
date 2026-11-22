"""A small least-recently-used cache."""
from __future__ import annotations

import time
from collections import OrderedDict
from typing import Any, Callable


class LRUCache:
    """Fixed-capacity cache that evicts the least recently used entry.

    ``clock`` is a zero-argument callable returning the current time in seconds;
    it exists so tests can control time.
    """

    def __init__(self, capacity: int, clock: Callable[[], float] = time.monotonic) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._clock = clock
        self._data: OrderedDict[Any, Any] = OrderedDict()

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: Any) -> bool:
        return key in self._data

    def get(self, key: Any, default: Any = None) -> Any:
        if key not in self._data:
            return default
        self._data.move_to_end(key)
        return self._data[key]

    def set(self, key: Any, value: Any) -> None:
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        while len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def delete(self, key: Any) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False

    def clear(self) -> None:
        self._data.clear()

    def keys(self) -> list:
        """Keys from least to most recently used."""
        return list(self._data)
