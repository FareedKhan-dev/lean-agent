import time
from collections import OrderedDict


class TTLCache:
    """Entries expire `ttl` seconds after they are set; at most `max_size` entries, the least
    recently used evicted first; stats() counts hits, misses and evictions."""

    def __init__(self, max_size, ttl, clock=time.monotonic):
        self.max_size, self.ttl, self.clock = max_size, ttl, clock
        self._items = OrderedDict()   # key -> (expires_at, value), least recently used first
        self._stats = {"hits": 0, "misses": 0, "evictions": 0}

    def get(self, key, default=None):
        entry = self._items.get(key)
        if entry is None or entry[0] <= self.clock():
            self._items.pop(key, None)
            self._stats["misses"] += 1
            return default
        self._items.move_to_end(key)
        self._stats["hits"] += 1
        return entry[1]

    def set(self, key, value):
        if key not in self._items and len(self._items) >= self.max_size:
            self._items.popitem(last=False)
            self._stats["evictions"] += 1
        self._items[key] = (self.clock() + self.ttl, value)
        self._items.move_to_end(key)

    def stats(self):
        return dict(self._stats)
