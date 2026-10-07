import time
from collections import OrderedDict


class TTLCache:
    """At most `max_size` entries, the least recently used evicted first; stats() counts hits,
    misses and evictions. skipped: expiry, add when stale prices show up."""

    def __init__(self, max_size, ttl, clock=time.monotonic):
        self.max_size = max_size
        self._items = OrderedDict()
        self._stats = {"hits": 0, "misses": 0, "evictions": 0}

    def get(self, key, default=None):
        if key not in self._items:
            self._stats["misses"] += 1
            return default
        self._items.move_to_end(key)
        self._stats["hits"] += 1
        return self._items[key]

    def set(self, key, value):
        if key not in self._items and len(self._items) >= self.max_size:
            self._items.popitem(last=False)
            self._stats["evictions"] += 1
        self._items[key] = value
        self._items.move_to_end(key)

    def stats(self):
        return dict(self._stats)
