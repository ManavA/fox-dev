# tinycache

A tiny in-memory LRU cache.

```python
from tinycache import LRUCache
c = LRUCache(2)
c.set("a", 1)
c.get("a")
```
